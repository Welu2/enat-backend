import re
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.core.errors import InvalidMutation, ProviderUnavailable
from app.dependencies import get_current_user_id
from app.models.errors import ErrorResponse
from app.services.addis_ai import AddisAIClient

router = APIRouter(prefix="/tts", tags=["tts"])


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    voice_id: str | None = Field(
        default=None, max_length=64, pattern=r"^[A-Za-z0-9_-]+$"
    )


def sanitize_amharic_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


@router.post(
    "",
    response_class=Response,
    responses={
        200: {
            "content": {
                media: {"schema": {"type": "string", "format": "binary"}}
                for media in ("audio/mpeg", "audio/wav")
            }
        }
    },
)
async def synthesize_post(
    payload: TTSRequest, user_id: UUID = Depends(get_current_user_id)
) -> Response:
    text = sanitize_amharic_text(payload.text)
    if not text:
        raise InvalidMutation("Text cannot be empty")
    audio = await AddisAIClient().synthesize_speech(text, payload.voice_id)
    if not audio:
        raise ProviderUnavailable("Speech provider unavailable")
    return Response(
        content=audio,
        media_type="audio/wav" if audio.startswith(b"RIFF") else "audio/mpeg",
        headers={"Cache-Control": "no-store"},
    )


@router.get("", status_code=410, responses={410: {"model": ErrorResponse}})
def retired_query_tts():
    raise HTTPException(
        410, "Use authenticated POST /tts with text in the request body"
    )
