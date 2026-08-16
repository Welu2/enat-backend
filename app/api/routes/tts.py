from urllib.parse import quote, unquote

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import Response
from pydantic import BaseModel

from app.services.addis_ai import AddisAIClient

router = APIRouter(prefix="/tts", tags=["tts"])


class TTSRequest(BaseModel):
    text: str
    voice_id: str | None = None


def build_tts_url(text: str) -> str:
    """Helper to generate a clean /tts audio URL for any text string."""
    encoded = quote(text)
    return f"/tts?text={encoded}"


@router.post("")
async def synthesize_post(payload: TTSRequest) -> Response:
    """Synthesize Amharic text into MP3/WAV audio via POST request."""
    if not payload.text.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Text cannot be empty")

    audio_bytes = await AddisAIClient().synthesize_speech(payload.text, payload.voice_id)
    if not audio_bytes:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to synthesize audio")

    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=speech.mp3"},
    )


@router.get("")
async def synthesize_get(text: str = Query(..., description="Amharic text to speak")) -> Response:
    """Synthesize Amharic text into MP3/WAV audio via GET request (usable in HTML <audio src="...">)."""
    clean_text = unquote(text).strip()
    if not clean_text:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Text cannot be empty")

    audio_bytes = await AddisAIClient().synthesize_speech(clean_text)
    if not audio_bytes:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to synthesize audio")

    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=speech.mp3"},
    )
