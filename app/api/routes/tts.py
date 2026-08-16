import hashlib
import logging
import re
from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import Response
from pydantic import BaseModel

from app.services.addis_ai import AddisAIClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tts", tags=["tts"])

# In-memory audio cache for frequent prompts (e.g., standard check-in questions)
_audio_cache: dict[str, bytes] = {}


class TTSRequest(BaseModel):
    text: str
    voice_id: str | None = None


def sanitize_amharic_text(text: str) -> str:
    """Strip complex punctuation marks that cause Addis AI synthesis failures."""
    # Replace Ethiopian & standard punctuation with spaces
    cleaned = re.sub(r"[።፤፥፣\.\!\?\:\-\_\(\)\[\]\"']", " ", text)
    # Collapse multiple whitespace characters into a single space
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def build_tts_url(text: str) -> str:
    """Helper to generate a clean /tts audio URL for any text string."""
    encoded = quote(text)
    return f"/tts?text={encoded}"


@router.post("")
async def synthesize_post(payload: TTSRequest) -> Response:
    """Synthesize Amharic text into MP3/WAV audio via POST request."""
    clean_text = sanitize_amharic_text(payload.text)
    if not clean_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty or contain only punctuation",
        )

    # Check cache
    cache_key = hashlib.md5(f"{clean_text}:{payload.voice_id}".encode()).hexdigest()
    if cache_key in _audio_cache:
        return Response(
            content=_audio_cache[cache_key],
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )

    try:
        client = AddisAIClient()
        audio_bytes = await client.synthesize_speech(clean_text, payload.voice_id)
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
        logger.error(f"[AddisAI TTS POST] Unexpected synthesis failure: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS synthesis error: {str(exc)}",
        )


@router.get("")
async def synthesize_get(text: str = Query(..., description="Amharic text to speak")) -> Response:
    """Synthesize Amharic text into MP3/WAV audio via GET request (FastAPI automatically decodes text)."""
    # Note: text is already decoded by FastAPI/Starlette query parser
    clean_text = sanitize_amharic_text(text)
    if not clean_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty or contain only punctuation",
        )

    # Check cache
    cache_key = hashlib.md5(clean_text.encode()).hexdigest()
    if cache_key in _audio_cache:
        return Response(
            content=_audio_cache[cache_key],
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )

    try:
        client = AddisAIClient()
        audio_bytes = await client.synthesize_speech(clean_text)
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
        logger.error(f"[AddisAI TTS GET] Unexpected synthesis failure for text '{clean_text}': {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS synthesis error: {str(exc)}",
        )
