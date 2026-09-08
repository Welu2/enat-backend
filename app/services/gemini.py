import base64
import logging
from typing import Any
import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)


class GeminiTranscribeClient:
    """Client for Google Gemini 3.5 Transcribe audio speech-to-text API."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        content_type: str = "audio/wav",
        language_code: str = "am-ET",
        language: str | None = None,
        model: str | None = None,
    ) -> str:
        """Transcribe speech audio into Amharic or English text using Google Gemini generateContent."""
        is_english = str(language or language_code).lower().startswith("en")
        api_key = self.settings.gemini_api_key.strip()
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Please add GEMINI_API_KEY to your .env file."
            )

        base_url = self.settings.gemini_api_base_url.rstrip("/")
        
        # Model resolution: explicit param -> live .env on disk -> os.environ -> cached settings
        model_name = (model or "").strip()
        if not model_name:
            try:
                from dotenv import dotenv_values
                model_name = (dotenv_values(".env").get("GEMINI_TRANSCRIBE_MODEL") or "").strip()
            except Exception:
                model_name = ""
        if not model_name:
            model_name = (os.getenv("GEMINI_TRANSCRIBE_MODEL") or getattr(self.settings, "gemini_transcribe_model", "") or "").strip()
        if not model_name:
            model_name = "gemini-3.5-transcribe"

        logger.info(f"[Gemini Transcribe] Transcribing audio with model: {model_name}")

        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        url = f"{base_url}/v1beta/models/{model_name}:generateContent?key={api_key}"

        if is_english:
            prompt_instruction = (
                "Transcribe this audio verbatim in English. "
                "Return ONLY the raw transcription without explanations, quotes, or markdown."
            )
        else:
            prompt_instruction = (
                "Transcribe this audio verbatim in Amharic. "
                "Preserve any English medical or technical terms used (code-switching). "
                "Return ONLY the raw transcription without explanations, quotes, or markdown."
            )

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_instruction},
                        {
                            "inline_data": {
                                "mime_type": content_type,
                                "data": b64_audio,
                            }
                        },
                    ]
                }
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"[Gemini Transcribe] HTTP error {exc.response.status_code}: {exc.response.text}")
            raise RuntimeError(f"Gemini Transcribe request failed: {exc.response.text}") from exc
        except Exception as exc:
            logger.error(f"[Gemini Transcribe] Communication failure: {exc}", exc_info=True)
            raise RuntimeError(f"Gemini Transcribe communication failure: {exc}") from exc

        candidates = data.get("candidates") or []
        if not candidates:
            raise RuntimeError(f"No candidates in generateContent response: {data}")

        parts = (candidates[0].get("content") or {}).get("parts") or []
        for part in parts:
            if "text" in part and part["text"]:
                return str(part["text"]).strip()

        raise RuntimeError(f"No text returned in generateContent response: {data}")

    async def generate_with_tools(
        self,
        system_prompt: str,
        user_prompt: str,
        tools: list[dict[str, Any]],
        tool_choice: str | dict[str, Any] = "auto",
        temperature: float = 0.1,
    ) -> list[tuple[str, dict[str, Any]]]:
        """Call Google Gemini generateContent with function declarations and extract tool calls."""
        api_key = self.settings.gemini_api_key.strip()
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Please add GEMINI_API_KEY to your .env file."
            )

        base_url = self.settings.gemini_api_base_url.rstrip("/")
        raw_model = getattr(self.settings, "gemini_chat_model", "gemini-2.5-flash").strip() or "gemini-2.5-flash"
        model_name = "gemini-2.5-flash" if raw_model in ("gemini-2.0-flash", "gemini-2.0-flash-exp") else raw_model

        declarations = []
        for tool in tools:
            func = tool.get("function", {}) if "function" in tool else tool
            name = func.get("name")
            if not name:
                continue
            declarations.append({
                "name": name,
                "description": func.get("description", ""),
                "parameters": to_gemini_parameter_schema(func.get("parameters", {})),
            })

        payload: dict[str, Any] = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}],
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 2048,
            },
        }

        if system_prompt and system_prompt.strip():
            payload["system_instruction"] = {
                "parts": [{"text": system_prompt.strip()}],
            }

        if declarations:
            payload["tools"] = [{"function_declarations": declarations}]
            payload["tool_config"] = {
                "function_calling_config": {
                    "mode": "AUTO",
                }
            }

        url = f"{base_url}/v1beta/models/{model_name}:generateContent?key={api_key}"

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()

        return self._extract_gemini_tool_calls(data)

    @staticmethod
    def _extract_gemini_tool_calls(payload: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
        """Extract tool calls from Gemini response candidates."""
        results: list[tuple[str, dict[str, Any]]] = []
        candidates = payload.get("candidates") or []
        for candidate in candidates:
            parts = (candidate.get("content") or {}).get("parts") or []
            for part in parts:
                if isinstance(part, dict) and "functionCall" in part:
                    fc = part["functionCall"]
                    if isinstance(fc, dict):
                        name = fc.get("name", "")
                        args = fc.get("args") or {}
                        if name:
                            results.append((name, args if isinstance(args, dict) else {}))
        return results


def to_gemini_parameter_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Convert standard JSON Schema / OpenAPI schema into Gemini-compliant function parameters."""
    if not isinstance(schema, dict):
        return schema
    res: dict[str, Any] = {}

    t = schema.get("type")
    if isinstance(t, list):
        types = [x.lower() for x in t if x is not None]
        is_nullable = "null" in types
        non_null_types = [x for x in types if x != "null"]
        main_type = non_null_types[0] if non_null_types else "string"
        res["type"] = main_type.upper()
        if is_nullable:
            res["nullable"] = True
    elif isinstance(t, str):
        res["type"] = t.upper()

    if "description" in schema:
        res["description"] = schema["description"]

    if "enum" in schema:
        res["enum"] = [str(x) for x in schema["enum"] if x is not None]

    if "required" in schema:
        res["required"] = schema["required"]

    if "properties" in schema and isinstance(schema["properties"], dict):
        res["properties"] = {
            k: to_gemini_parameter_schema(v) for k, v in schema["properties"].items()
        }

    if "items" in schema and isinstance(schema["items"], dict):
        res["items"] = to_gemini_parameter_schema(schema["items"])

    return res


# Alias for general use
GeminiClient = GeminiTranscribeClient
