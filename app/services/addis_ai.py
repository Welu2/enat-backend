import json
from typing import Any

import httpx

from app.config import get_settings


class AddisAIClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        content_type: str = "audio/wav",
        language: str = "am",
        **kwargs: Any,
    ) -> str:
        """Send audio to Addis AI STT and return the transcript string.

        Addis AI STT supports Amharic ('am') and Afaan Oromo ('om').
        """
        url = f"{self.settings.addis_api_base_url}/api/v2/stt"
        headers = {"x-api-key": self.settings.addis_api_key}
        clean_lang = "om" if str(language).lower().startswith("om") else "am"
        # target_language / language_code tells the ASR which language to decode.
        request_data = json.dumps({"language_code": clean_lang})

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                headers=headers,
                files={"audio": (filename, audio_bytes, content_type)},
                data={"request_data": request_data},
            )
            response.raise_for_status()
            payload = response.json()

        data = payload.get("data") or payload
        transcription = data.get("transcription") or data.get("text")
        if not transcription:
            raise ValueError("ASR response missing transcription")
        return transcription

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
    ) -> str:
        """Call the Addis AI chat-generate endpoint and return the raw text response.

        Notes:
        - `target_language` is intentionally omitted here.  That field instructs
          the model to respond in Amharic, but the extraction schema uses English
          keys/values (JSON).  Including it caused the LLM to mix Amharic into
          the JSON output, breaking parsing.
        - `maxOutputTokens` is set to 2048 to safely accommodate responses that
          contain multiple extracted symptoms in a single session turn.
        """
        url = f"{self.settings.addis_api_base_url}/api/v1/chat_generate"
        headers = {
            "x-api-key": self.settings.addis_api_key,
            "Content-Type": "application/json",
        }
        body = {
            "prompt": user_prompt,
            "system": system_prompt,
            "generation_config": {
                "temperature": temperature,
                "maxOutputTokens": 2048,
            },
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=body)
            response.raise_for_status()
            payload = response.json()

        text = self._extract_text(payload)
        if not text:
            raise ValueError("LLM response missing text")
        return text

    @staticmethod
    def _extract_text(payload: dict[str, Any]) -> str:
        for k in ("response_text", "response", "text", "content"):
            if k in payload and isinstance(payload[k], str):
                return payload[k]
        if "data" in payload:
            data = payload["data"]
            if isinstance(data, dict):
                for key in ("response_text", "response", "text", "content"):
                    if key in data and isinstance(data[key], str):
                        return data[key]
            elif isinstance(data, str):
                return data
        if "choices" in payload and payload["choices"]:
            choice = payload["choices"][0]
            if isinstance(choice, dict):
                message = choice.get("message") or choice
                if isinstance(message, dict):
                    for k in ("response_text", "content", "text"):
                        if k in message and isinstance(message[k], str):
                            return message[k]
        return ""

    async def generate_with_tools(
        self,
        system_prompt: str,
        user_prompt: str,
        tools: list[dict[str, Any]],
        tool_choice: str | dict[str, Any] = "auto",
        temperature: float = 0.1,
        target_language: str = "am",
    ) -> list[tuple[str, dict[str, Any]]]:
        """Call Addis AI endpoint with function tools and return list of (tool_name, parsed_args) tuples."""
        url = f"{self.settings.addis_api_base_url}/api/v1/chat_generate"
        headers = {
            "x-api-key": self.settings.addis_api_key,
            "Content-Type": "application/json",
        }
        body = {
            "prompt": user_prompt,
            "system": system_prompt,
            "target_language": target_language,
            "tools": tools,
            "tool_choice": tool_choice,
            "generation_config": {
                "temperature": temperature,
                "maxOutputTokens": 2048,
            },
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=body)
            response.raise_for_status()
            payload = response.json()

        return self._extract_tool_calls(payload)

    @staticmethod
    def _extract_tool_calls(payload: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
        """Extract and parse tool calls from diverse response structures into (name, arguments_dict)."""
        raw_calls: list[Any] = []

        # 1. OpenAI-style choices format: choices[0].message.tool_calls
        if "choices" in payload and isinstance(payload["choices"], list) and payload["choices"]:
            choice = payload["choices"][0]
            if isinstance(choice, dict):
                msg = choice.get("message") or choice
                if isinstance(msg, dict) and "tool_calls" in msg and isinstance(msg["tool_calls"], list):
                    raw_calls = msg["tool_calls"]

        # 2. Native chat_generate envelope format: data.tool_calls
        if not raw_calls and "data" in payload and isinstance(payload["data"], dict):
            if "tool_calls" in payload["data"] and isinstance(payload["data"]["tool_calls"], list):
                raw_calls = payload["data"]["tool_calls"]

        # 3. Top-level tool_calls
        if not raw_calls and "tool_calls" in payload and isinstance(payload["tool_calls"], list):
            raw_calls = payload["tool_calls"]

        results: list[tuple[str, dict[str, Any]]] = []
        for call in raw_calls:
            if not isinstance(call, dict):
                continue
            name = ""
            raw_arguments: Any = {}

            if "function" in call and isinstance(call["function"], dict):
                name = call["function"].get("name", "")
                raw_arguments = call["function"].get("arguments", {})
            else:
                name = call.get("name", "")
                raw_arguments = call.get("arguments", call.get("parameters", {}))

            if not name:
                continue

            # Arguments can be JSON string or pre-parsed dict
            if isinstance(raw_arguments, str):
                try:
                    parsed_args = json.loads(raw_arguments)
                except Exception:
                    parsed_args = {}
            elif isinstance(raw_arguments, dict):
                parsed_args = raw_arguments
            else:
                parsed_args = {}

            if isinstance(parsed_args, dict):
                results.append((name, parsed_args))

        return results

    async def synthesize_speech(
        self,
        text: str,
        voice_id: str | None = None,
        language: str = "am",
        **kwargs: Any,
    ) -> bytes:
        """Synthesize Amharic text into audio bytes (MP3) via TTS with robust fallback."""
        clean_text = text.strip()
        if not clean_text:
            return b""

        # 1. First try upstream Addis AI API if configured and available
        if self.settings.addis_api_key:
            url = f"{self.settings.addis_api_base_url}/api/v1/tts"
            headers = {
                "x-api-key": self.settings.addis_api_key,
                "Content-Type": "application/json",
            }
            body: dict[str, Any] = {
                "text": clean_text,
                "language_code": "am",
            }
            if voice_id:
                body["voice_id"] = voice_id

            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(url, headers=headers, json=body)
                    if response.status_code == 200:
                        content_type = response.headers.get("content-type", "")
                        if "audio" in content_type or "mpeg" in content_type or "octet-stream" in content_type:
                            return response.content

                        payload = response.json()
                        data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
                        for key in ("audio_base64", "audio_content", "audio"):
                            if isinstance(data, dict) and key in data and isinstance(data[key], str):
                                import base64
                                return base64.b64decode(data[key])
                        return response.content
            except Exception:
                pass

        # 2. Synthesize using high quality Amharic engine (gTTS)
        try:
            import asyncio
            from io import BytesIO
            from gtts import gTTS

            def _run_gtts() -> bytes:
                tts = gTTS(text=clean_text, lang="am")
                fp = BytesIO()
                tts.write_to_fp(fp)
                return fp.getvalue()

            return await asyncio.to_thread(_run_gtts)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).error(f"TTS synthesis error: {exc}", exc_info=True)
            return b""
