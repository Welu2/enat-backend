import base64
import json

import httpx
from pydantic import ValidationError

from app.config import get_settings
from app.core.errors import InvalidMutation, ProviderUnavailable
from app.models.provider import ProviderEnvelope, ProviderFields
from app.services.provider_runtime import runtime_client


class AddisAIClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    @staticmethod
    def _json(response: httpx.Response) -> ProviderEnvelope:
        try:
            return ProviderEnvelope.model_validate_json(response.content)
        except (ValidationError, ValueError) as exc:
            raise ProviderUnavailable("Malformed provider response") from exc

    async def transcribe(
        self, audio_bytes: bytes, filename: str, content_type: str
    ) -> str:
        if len(audio_bytes) > self.settings.max_audio_bytes:
            raise InvalidMutation("Audio exceeds provider input bound")
        async with runtime_client() as client:
            response = await client.request(
                "/api/v2/stt",
                files={"audio": (filename, audio_bytes, content_type)},
                data={"request_data": json.dumps({"language_code": "am"})},
            )
        payload = self._json(response)
        data = payload.data if isinstance(payload.data, ProviderFields) else payload
        transcription = data.transcription or data.text
        if not transcription or not transcription.strip() or len(transcription) > 8000:
            raise ProviderUnavailable("ASR response missing transcription")
        return transcription

    async def generate_json(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.1
    ) -> str:
        if len(user_prompt) > 16000 or len(system_prompt) > 32000:
            raise InvalidMutation("Extraction input exceeds bound")
        async with runtime_client() as client:
            response = await client.request(
                "/api/v1/chat_generate",
                json={
                    "prompt": user_prompt,
                    "system": system_prompt,
                    "generation_config": {
                        "temperature": temperature,
                        "maxOutputTokens": 2048,
                    },
                },
            )
        text = self._extract_text(self._json(response))
        if not text or len(text) > 32000:
            raise ProviderUnavailable("LLM response missing text")
        return text

    @staticmethod
    def _extract_text(payload: ProviderEnvelope) -> str:
        if text := payload.generated_text():
            return text
        if isinstance(payload.data, str):
            return payload.data
        if isinstance(payload.data, ProviderFields) and (
            text := payload.data.generated_text()
        ):
            return text
        if payload.choices:
            choice = payload.choices[0]
            return (choice.message or choice).generated_text()
        return ""

    async def synthesize_speech(self, text: str, voice_id: str | None = None) -> bytes:
        text = text.strip()
        if not text or len(text) > 2000:
            raise InvalidMutation("Speech input outside bound")
        body = {"text": text, "language_code": "am"}
        if voice_id:
            body["voice_id"] = voice_id
        async with runtime_client() as client:
            response = await client.request(
                "/api/v1/tts", max_bytes=5_400_000, json=body
            )
        content_type = response.headers.get("content-type", "").split(";")[0]
        try:
            if content_type in (
                "audio/mpeg",
                "audio/mp3",
                "audio/wav",
                "audio/x-wav",
                "application/octet-stream",
            ):
                return self._validated_audio(response.content)
            payload = self._json(response)
            data = payload.data if isinstance(payload.data, ProviderFields) else payload
            encoded = data.audio_base64 or data.audio_content or data.audio
            if encoded:
                return self._validated_audio(base64.b64decode(encoded, validate=True))
            raise ValueError("Provider returned non-audio content")
        except ValueError as exc:
            raise ProviderUnavailable("Invalid provider audio") from exc

    @staticmethod
    def _validated_audio(value: bytes) -> bytes:
        mp3 = value.startswith(b"ID3") or (
            len(value) > 2 and value[0] == 255 and value[1] & 224 == 224
        )
        wav = value.startswith(b"RIFF") and value[8:12] == b"WAVE"
        if not value or len(value) > 4_000_000 or not (mp3 or wav):
            raise ValueError("Invalid speech provider audio")
        return value
