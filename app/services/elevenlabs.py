import io
import logging
from typing import Any
import httpx

from app.config import get_settings
from app.services.addis_ai import AddisAIClient

logger = logging.getLogger(__name__)


class ElevenLabsClient:
    """Client for ElevenLabs Voice API (TTS and Scribe STT).

    Note: ElevenLabs does not support Amharic. When Amharic is requested,
    the client automatically delegates to AddisAIClient for full Amharic support.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self._addis_client: AddisAIClient | None = None

    @property
    def addis_client(self) -> AddisAIClient:
        if self._addis_client is None:
            self._addis_client = AddisAIClient()
        return self._addis_client

    async def synthesize_speech(
        self,
        text: str,
        voice_id: str | None = None,
        language: str = "en",
        **kwargs: Any,
    ) -> bytes:
        """Synthesize speech audio using ElevenLabs Text-to-Speech API.

        If language is Amharic, delegates to AddisAIClient.
        If API key is missing or call fails, falls back to gTTS English synthesis.
        """
        clean_lang = "en" if str(language).lower().startswith("en") else "am"
        if clean_lang == "am":
            logger.info(
                "[ElevenLabs TTS] ElevenLabs does not support Amharic. Delegating to Addis AI."
            )
            return await self.addis_client.synthesize_speech(text, voice_id=voice_id, language="am")

        api_key = self.settings.elevenlabs_api_key.strip()
        if not api_key:
            logger.info("[ElevenLabs TTS] ELEVENLABS_API_KEY is not configured; falling back to gTTS.")
            return self._synthesize_with_gtts(text, lang="en")

        vid = voice_id or self.settings.elevenlabs_voice_id.strip() or "21m00Tcm4TlvDq8ikWAM"
        model_id = self.settings.elevenlabs_model_id.strip() or "eleven_multilingual_v2"
        base_url = self.settings.elevenlabs_api_base_url.rstrip("/")
        url = f"{base_url}/v1/text-to-speech/{vid}"

        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }
        payload: dict[str, Any] = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                return resp.content
        except Exception as exc:
            logger.warning(
                f"[ElevenLabs TTS] Request failed ({exc}); falling back to gTTS English synthesis.",
                exc_info=True,
            )
            return self._synthesize_with_gtts(text, lang="en")

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        content_type: str = "audio/wav",
        language: str = "en",
    ) -> str:
        """Transcribe speech audio into English text using ElevenLabs Scribe STT API.

        If language is Amharic, delegates to AddisAIClient.
        """
        clean_lang = "en" if str(language).lower().startswith("en") else "am"
        if clean_lang == "am":
            logger.info(
                "[ElevenLabs ASR] ElevenLabs does not support Amharic. Delegating to Addis AI."
            )
            return await self.addis_client.transcribe(
                audio_bytes, filename, content_type, language="am"
            )

        api_key = self.settings.elevenlabs_api_key.strip()
        if not api_key:
            raise RuntimeError(
                "ELEVENLABS_API_KEY is not configured. Please add ELEVENLABS_API_KEY to your .env file."
            )

        base_url = self.settings.elevenlabs_api_base_url.rstrip("/")
        model_id = self.settings.elevenlabs_stt_model_id.strip() or "scribe_v1"
        url = f"{base_url}/v1/speech-to-text"

        headers = {
            "xi-api-key": api_key,
        }
        files = {
            "file": (filename, audio_bytes, content_type),
        }
        data = {
            "model_id": model_id,
            "language_code": "en",
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, headers=headers, files=files, data=data)
                resp.raise_for_status()
                payload = resp.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"[ElevenLabs ASR] HTTP error {exc.response.status_code}: {exc.response.text}")
            raise RuntimeError(f"ElevenLabs ASR request failed: {exc.response.text}") from exc
        except Exception as exc:
            logger.error(f"[ElevenLabs ASR] Unexpected transcription error: {exc}", exc_info=True)
            raise RuntimeError(f"ElevenLabs ASR communication failure: {exc}") from exc

        text = payload.get("text")
        if text is None:
            text = (payload.get("data") or {}).get("text", "")
        return str(text).strip()

    def _synthesize_with_gtts(self, text: str, lang: str = "en") -> bytes:
        """Fallback synthesis using gTTS for high-quality standard English audio."""
        from gtts import gTTS

        buf = io.BytesIO()
        tts = gTTS(text=text, lang=lang)
        tts.write_to_fp(buf)
        return buf.getvalue()
