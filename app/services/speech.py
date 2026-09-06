from typing import Any
import logging
from app.services.addis_ai import AddisAIClient
from app.services.deepgram import DeepgramClient
from app.services.elevenlabs import ElevenLabsClient
from app.services.gemini import GeminiTranscribeClient
from app.services.sahara import SaharaVoiceClient

logger = logging.getLogger(__name__)

DEFAULT_VOICE_MODEL = "addisai"
SUPPORTED_VOICE_MODELS = (
    "addisai",
    "sahara",
    "intron",
    "gemini",
    "google",
    "elevenlabs",
    "eleven_labs",
    "deepgram",
    "deep_gram",
)
DEFAULT_LANGUAGE = "am"
SUPPORTED_LANGUAGES = ("am", "en")


def normalize_language(language: str | None) -> str:
    """Normalize language string to canonical 'am' or 'en'."""
    if not language or not str(language).strip():
        return DEFAULT_LANGUAGE
    cleaned = str(language).strip().lower()
    if cleaned in ("en", "english", "en-us", "en-gb", "eng"):
        return "en"
    return "am"


def normalize_voice_model(model: str | None) -> str:
    """Normalize model string to standard canonical name ('addisai', 'sahara', 'gemini', 'elevenlabs', or 'deepgram')."""
    if not model or not str(model).strip():
        return DEFAULT_VOICE_MODEL
    cleaned = str(model).strip().lower()
    if cleaned in ("sahara", "intron", "sahara_voice", "saharavoice"):
        return "sahara"
    if cleaned in ("gemini", "google", "gemini-3.5-transcribe", "gemini_transcribe", "gemini-transcribe"):
        return "gemini"
    if cleaned in ("elevenlabs", "eleven_labs", "eleven", "11labs"):
        return "elevenlabs"
    if cleaned in ("deepgram", "deep_gram", "deepgram_voice"):
        return "deepgram"
    return "addisai"


def get_asr_client(model: str = DEFAULT_VOICE_MODEL) -> Any:
    """Return the speech-to-text (ASR) client matching the requested model."""
    canonical = normalize_voice_model(model)
    if canonical == "sahara":
        return SaharaVoiceClient()
    if canonical == "gemini":
        return GeminiTranscribeClient()
    if canonical == "elevenlabs":
        return ElevenLabsClient()
    if canonical == "deepgram":
        return DeepgramClient()
    return AddisAIClient()


def get_tts_client(model: str = DEFAULT_VOICE_MODEL, language: str = DEFAULT_LANGUAGE) -> Any:
    """Return the text-to-speech (TTS) client matching the requested model and language."""
    canonical_model = normalize_voice_model(model)
    canonical_lang = normalize_language(language)

    if canonical_lang == "en":
        if canonical_model == "deepgram":
            return DeepgramClient()
        if canonical_model == "elevenlabs":
            return ElevenLabsClient()
        if canonical_model == "sahara":
            return SaharaVoiceClient()
        logger.info(
            f"[TTS] English TTS requested for model '{model}'. Addis AI does not support English; "
            f"using Sahara English TTS engine."
        )
        return SaharaVoiceClient()

    # Amharic language requested
    if canonical_model in ("elevenlabs", "deepgram"):
        logger.info(
            f"[TTS] {canonical_model} does not support Amharic; routing Amharic TTS to Addis AI."
        )
        return AddisAIClient()

    if canonical_model == "sahara":
        return SaharaVoiceClient()
    return AddisAIClient()


