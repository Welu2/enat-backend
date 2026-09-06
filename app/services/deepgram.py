import io
import logging
from typing import Any
import httpx

from app.config import get_settings
from app.services.addis_ai import AddisAIClient

logger = logging.getLogger(__name__)


class DeepgramClient:
    """Client for Deepgram Voice API (Aura TTS and Listen STT).

    Note: Deepgram does not support Amharic. When Amharic is requested,
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
        """Synthesize speech audio using Deepgram Aura Text-to-Speech API.

        If language is Amharic, delegates to AddisAIClient.
        If API key is missing or call fails, falls back to gTTS English synthesis.
        """
        clean_lang = "en" if str(language).lower().startswith("en") else "am"
        if clean_lang == "am":
            logger.info(
                "[Deepgram TTS] Deepgram does not support Amharic. Delegating to Addis AI."
            )
            return await self.addis_client.synthesize_speech(text, voice_id=voice_id, language="am")

        api_key = self.settings.deepgram_api_key.strip()
        if not api_key:
            logger.info("[Deepgram TTS] DEEPGRAM_API_KEY is not configured; falling back to gTTS.")
            return self._synthesize_with_gtts(text, lang="en")

        model_name = voice_id or self.settings.deepgram_tts_model.strip() or "aura-asteria-en"
        base_url = self.settings.deepgram_api_base_url.rstrip("/")
        url = f"{base_url}/v1/speak?model={model_name}"

        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                return resp.content
        except Exception as exc:
            logger.warning(
                f"[Deepgram TTS] Request failed ({exc}); falling back to gTTS English synthesis.",
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
        """Transcribe speech audio into English text using Deepgram Listen STT API.

        If language is Amharic, delegates to AddisAIClient.
        """
        clean_lang = "en" if str(language).lower().startswith("en") else "am"
        if clean_lang == "am":
            logger.info(
                "[Deepgram ASR] Deepgram does not support Amharic. Delegating to Addis AI."
            )
            return await self.addis_client.transcribe(
                audio_bytes, filename, content_type, language="am"
            )

        api_key = self.settings.deepgram_api_key.strip()
        if not api_key:
            raise RuntimeError(
                "DEEPGRAM_API_KEY is not configured. Please add DEEPGRAM_API_KEY to your .env file."
            )

        base_url = self.settings.deepgram_api_base_url.rstrip("/")
        model_name = self.settings.deepgram_stt_model.strip() or "nova-2"
        url = f"{base_url}/v1/listen?model={model_name}&smart_format=true&language=en"

        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": content_type or "audio/wav",
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, headers=headers, content=audio_bytes)
                resp.raise_for_status()
                payload = resp.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"[Deepgram ASR] HTTP error {exc.response.status_code}: {exc.response.text}")
            raise RuntimeError(f"Deepgram ASR request failed: {exc.response.text}") from exc
        except Exception as exc:
            logger.error(f"[Deepgram ASR] Unexpected transcription error: {exc}", exc_info=True)
            raise RuntimeError(f"Deepgram ASR communication failure: {exc}") from exc

        channels = (payload.get("results") or {}).get("channels") or []
        if channels:
            alternatives = channels[0].get("alternatives") or []
            if alternatives:
                return str(alternatives[0].get("transcript") or "").strip()

        return ""

    def _synthesize_with_gtts(self, text: str, lang: str = "en") -> bytes:
        """Fallback synthesis using gTTS for high-quality standard English audio."""
        from gtts import gTTS

        buf = io.BytesIO()
        tts = gTTS(text=text, lang=lang)
        tts.write_to_fp(buf)
        return buf.getvalue()
