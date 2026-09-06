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
    ) -> str:
        """Transcribe speech audio into Amharic or English text using Gemini 3.5 Transcribe."""
        is_english = str(language or language_code).lower().startswith("en")
        effective_lang_code = "en-US" if is_english else "am-ET"
        api_key = self.settings.gemini_api_key.strip()
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Please add GEMINI_API_KEY to your .env file."
            )

        base_url = self.settings.gemini_api_base_url.rstrip("/")
        model_name = self.settings.gemini_transcribe_model.strip() or "gemini-3.5-transcribe"
        uploaded_file_name: str | None = None

        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                try:
                    # 1. Initiate resumable upload via Google AI Files API
                    init_url = f"{base_url}/upload/v1beta/files?key={api_key}"
                    init_headers = {
                        "X-Goog-Upload-Protocol": "resumable",
                        "X-Goog-Upload-Command": "start",
                        "X-Goog-Upload-Header-Content-Length": str(len(audio_bytes)),
                        "X-Goog-Upload-Header-Content-Type": content_type,
                        "Content-Type": "application/json",
                    }
                    init_resp = await client.post(
                        init_url,
                        headers=init_headers,
                        json={"file": {"display_name": filename}},
                    )
                    init_resp.raise_for_status()

                    upload_url = init_resp.headers.get("x-goog-upload-url") or init_resp.headers.get(
                        "X-Goog-Upload-URL"
                    )
                    if not upload_url:
                        raise RuntimeError(f"Files API did not return an upload URL: {init_resp.text}")

                    # 2. Upload actual audio bytes
                    upload_headers = {
                        "Content-Length": str(len(audio_bytes)),
                        "X-Goog-Upload-Offset": "0",
                        "X-Goog-Upload-Command": "upload, finalize",
                    }
                    upload_resp = await client.post(
                        upload_url,
                        headers=upload_headers,
                        content=audio_bytes,
                    )
                    upload_resp.raise_for_status()
                    file_info = upload_resp.json().get("file") or {}
                    file_uri = file_info.get("uri")
                    uploaded_file_name = file_info.get("name")

                    if not file_uri:
                        raise RuntimeError(f"Files API response missing uri: {upload_resp.text}")

                    # 3. Call Interactions API for gemini-3.5-transcribe
                    interactions_url = f"{base_url}/v1beta/interactions?key={api_key}"
                    interaction_payload = {
                        "model": model_name,
                        "input": [
                            {
                                "type": "audio",
                                "uri": file_uri,
                                "mime_type": content_type,
                            }
                        ],
                        "generation_config": {
                            "transcription_config": {
                                "language_codes": [effective_lang_code],
                            }
                        },
                    }

                    interaction_resp = await client.post(
                        interactions_url,
                        json=interaction_payload,
                    )
                    interaction_resp.raise_for_status()
                    data = interaction_resp.json()

                    # 4. Extract transcript from Interactions response
                    if "output_text" in data and data["output_text"]:
                        return str(data["output_text"]).strip()

                    for step in data.get("steps", []):
                        for item in step.get("content", []):
                            if item.get("type") == "text" and item.get("text"):
                                return str(item["text"]).strip()

                    raise RuntimeError(f"No transcript text found in Interactions response: {data}")

                except Exception as primary_exc:
                    logger.warning(
                        f"[Gemini Transcribe] Primary Interactions API flow failed ({primary_exc}). "
                        f"Attempting generateContent fallback..."
                    )
                    return await self._fallback_generate_content(
                        client, base_url, api_key, audio_bytes, content_type, is_english=is_english
                    )

                finally:
                    # Clean up uploaded file if name is known
                    if uploaded_file_name:
                        try:
                            delete_url = f"{base_url}/v1beta/{uploaded_file_name}?key={api_key}"
                            await client.delete(delete_url)
                        except Exception as del_err:
                            logger.debug(f"[Gemini Transcribe] Failed to delete temporary file: {del_err}")

        except httpx.HTTPStatusError as exc:
            logger.error(f"[Gemini Transcribe] HTTP error {exc.response.status_code}: {exc.response.text}")
            raise RuntimeError(f"Gemini Transcribe request failed: {exc.response.text}") from exc
        except Exception as exc:
            logger.error(f"[Gemini Transcribe] Communication failure: {exc}", exc_info=True)
            raise RuntimeError(f"Gemini Transcribe communication failure: {exc}") from exc

    async def _fallback_generate_content(
        self,
        client: httpx.AsyncClient,
        base_url: str,
        api_key: str,
        audio_bytes: bytes,
        content_type: str,
        is_english: bool = False,
    ) -> str:
        """Fallback to standard Gemini multimodal generateContent with inline base64 audio."""
        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        url = f"{base_url}/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
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
                        {
                            "text": prompt_instruction
                        },
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
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        candidates = data.get("candidates") or []
        if not candidates:
            raise RuntimeError(f"No candidates in fallback generateContent response: {data}")

        parts = (candidates[0].get("content") or {}).get("parts") or []
        for part in parts:
            if "text" in part and part["text"]:
                return str(part["text"]).strip()

        raise RuntimeError(f"No text returned in fallback generateContent response: {data}")

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
