import logging
from typing import Any
import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)


class SaharaVoiceClient:
    """Client for Sahara / Intron Voice API (ASR and TTS)."""

    def __init__(self, language: str = "am", **kwargs: Any) -> None:
        self.settings = get_settings()
        self.default_language = language

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        content_type: str = "audio/wav",
        language: str = "am",
    ) -> str:
        """Transcribe speech audio into Amharic or English text using Intron STT."""
        clean_lang = "en" if str(language).lower().startswith("en") else "am"
        url = f"{self.settings.intron_api_base_url}/file/v1/upload/sync"
        headers = {
            "Authorization": f"Bearer {self.settings.intron_api_key}",
        }
        files = {
            "audio_file_blob": (filename, audio_bytes, content_type),
        }
        data = {
            "audio_file_name": filename,
            "use_language_asr_input": clean_lang,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, files=files, data=data)
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"[Sahara ASR] HTTP error {exc.response.status_code}: {exc.response.text}")
            raise RuntimeError(f"Sahara ASR request failed: {exc.response.text}") from exc
        except Exception as exc:
            logger.error(f"[Sahara ASR] Unexpected transcription error: {exc}", exc_info=True)
            raise RuntimeError(f"Sahara ASR communication failure: {exc}") from exc

        data_obj = payload.get("data") or {}
        transcript = data_obj.get("audio_transcript")
        if transcript is None:
            transcript = payload.get("transcript") or payload.get("audio_transcript", "")

        return str(transcript).strip()

    async def synthesize_speech(
        self,
        text: str,
        voice_id: str | None = None,
        voice_gender: str = "female",
        voice_accent: str | None = None,
        language: str = "am",
    ) -> bytes:
        """Synthesize Amharic or English text into speech audio using Intron TTS with gTTS fallback."""
        clean_lang = "en" if str(language).lower().startswith("en") else "am"
        accent = voice_accent
        if not accent or (clean_lang == "en" and accent == "amharic"):
            accent = "nigerian" if clean_lang == "en" else "amharic"

        # If Intron API key is missing or English synthesis fallback is needed
        if not self.settings.intron_api_key.strip() and clean_lang == "en":
            return self._synthesize_with_gtts(text, lang="en")

        url = f"{self.settings.intron_api_base_url}/tts/v1/generate"
        headers = {
            "Authorization": f"Bearer {self.settings.intron_api_key}",
            "Content-Type": "application/json",
        }
        body: dict[str, Any] = {
            "text": text,
            "voice_language": clean_lang,
            "voice_accent": accent,
            "voice_gender": voice_gender,
        }
        if voice_id:
            body["voice_id"] = voice_id

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=body)
                response.raise_for_status()
                payload = response.json()

                if payload.get("status") == "Error" or (payload.get("status") != "Ok" and "data" not in payload):
                    msg = payload.get("message") or "Unknown TTS error"
                    raise RuntimeError(f"Sahara TTS generation rejected: {msg}")

                audio_path = (payload.get("data") or {}).get("audio_path")
                if not audio_path:
                    raise RuntimeError(f"Sahara TTS response did not provide an audio_path: {payload}")

                # Download audio bytes from audio_path
                audio_resp = await client.get(audio_path)
                audio_resp.raise_for_status()
                return audio_resp.content

        except Exception as exc:
            if clean_lang == "en":
                logger.info(f"[Sahara TTS] Intron English TTS unavailable ({exc}); falling back to gTTS.")
                return self._synthesize_with_gtts(text, lang="en")

            if isinstance(exc, httpx.HTTPStatusError):
                logger.error(f"[Sahara TTS] HTTP error {exc.response.status_code}: {exc.response.text}")
                raise RuntimeError(f"Sahara TTS request failed: {exc.response.text}") from exc
            logger.error(f"[Sahara TTS] Unexpected synthesis error: {exc}", exc_info=True)
            raise RuntimeError(f"Sahara TTS communication failure: {exc}") from exc

    def _synthesize_with_gtts(self, text: str, lang: str = "en") -> bytes:
        """Fallback synthesis using gTTS for high-quality standard English audio."""
        import io
        from gtts import gTTS

        buf = io.BytesIO()
        tts = gTTS(text=text, lang=lang)
        tts.write_to_fp(buf)
        return buf.getvalue()
