import hashlib
import logging
import re
from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import Response
from pydantic import BaseModel

from app.services.speech import get_tts_client, normalize_language, normalize_voice_model

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tts", tags=["tts"])

# In-memory audio cache for frequent prompts (e.g., standard check-in questions)
_audio_cache: dict[str, bytes] = {}


class TTSRequest(BaseModel):
    text: str
    voice_id: str | None = None
    model: str = "addisai"
    language: str = "am"


def sanitize_text(text: str) -> str:
    """Strip complex punctuation marks that cause synthesis failures."""
    # Replace Ethiopian & standard punctuation with spaces
    cleaned = re.sub(r"[።፤፥፣\.\!\?\:\-\_\(\)\[\]\"']", " ", text)
    # Collapse multiple whitespace characters into a single space
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


# Backward compatibility alias
sanitize_amharic_text = sanitize_text


def build_tts_url(text: str, model: str = "addisai", language: str = "am") -> str:
    """Helper to generate a clean /tts audio URL for any text string."""
    encoded = quote(text)
    params = [f"text={encoded}"]
    if model and model.lower() != "addisai":
        params.append(f"model={quote(model)}")
    if language and language.lower() != "am":
        params.append(f"language={quote(language)}")
    return f"/tts?{'&'.join(params)}"


@router.post("")
async def synthesize_post(payload: TTSRequest) -> Response:
    """Synthesize Amharic or English text into MP3/WAV audio via POST request."""
    clean_text = sanitize_text(payload.text)
    if not clean_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty or contain only punctuation",
        )

    model = payload.model or "addisai"
    lang = normalize_language(payload.language)
    # Check cache
    cache_key = hashlib.md5(f"{clean_text}:{payload.voice_id}:{model}:{lang}".encode()).hexdigest()
    if cache_key in _audio_cache:
        return Response(
            content=_audio_cache[cache_key],
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )

    try:
        client = get_tts_client(model, language=lang)
        audio_bytes = await client.synthesize_speech(clean_text, payload.voice_id, language=lang)
        if not audio_bytes:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to synthesize audio from upstream service",
            )

        # Cache up to 100 entries
        if len(_audio_cache) < 100:
            _audio_cache[cache_key] = audio_bytes

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"[{model} TTS POST ({lang})] Unexpected synthesis failure: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS synthesis error: {str(exc)}",
        )


@router.get("")
async def synthesize_get(
    text: str = Query(..., description="Text to speak"),
    model: str = Query("addisai", description="Voice engine ('addisai', 'sahara', 'elevenlabs', or 'deepgram')"),
    language: str = Query("am", description="Language of text ('am' or 'en')"),
) -> Response:
    """Synthesize Amharic or English text into MP3/WAV audio via GET request (FastAPI automatically decodes text)."""
    clean_text = sanitize_text(text)
    if not clean_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty or contain only punctuation",
        )

    lang = normalize_language(language)
    # Check cache
    cache_key = hashlib.md5(f"{clean_text}:{model}:{lang}".encode()).hexdigest()
    if cache_key in _audio_cache:
        return Response(
            content=_audio_cache[cache_key],
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )

    try:
        client = get_tts_client(model, language=lang)
        audio_bytes = await client.synthesize_speech(clean_text, language=lang)
        if not audio_bytes:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to synthesize audio from upstream service",
            )

        if len(_audio_cache) < 100:
            _audio_cache[cache_key] = audio_bytes

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"[{model} TTS GET ({lang})] Unexpected synthesis failure for text '{clean_text}': {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS synthesis error: {str(exc)}",
        )
