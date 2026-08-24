from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import Response

from app.dependencies import get_current_user_id
from app.db.repositories.check_ins import CheckInRepository
from app.models.checkin import (
    CheckInHistoryItem,
    CheckInRespondResponse,
    CheckInStartResponse,
    CompleteStageResponse,
    VerifyItemRequest,
    VerifyItemResponse,
    VoiceCorrectItemResponse,
)
from app.services.checkin_session import CheckInSessionService
from app.services.stage_audio import (
    get_all_stage_prompts_metadata,
    get_or_synthesize_stage_audio,
)

router = APIRouter(prefix="/checkin", tags=["checkin"])


@router.get("/prompts")
def list_checkin_prompts() -> list[dict]:
    """Returns all 4 standard check-in stage prompt questions, localized categories, and audio playback URLs."""
    return get_all_stage_prompts_metadata()


@router.get("/prompts/{stage}/audio")
async def get_stage_prompt_audio(stage: str) -> Response:
    """Streams the stored/pre-cached Amharic question prompt audio for the given stage (zero redundant TTS calls)."""
    try:
        audio_bytes = await get_or_synthesize_stage_audio(stage)
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"inline; filename=prompt_{stage}.mp3"},
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Audio retrieval failed: {exc}") from exc


@router.post("/start", response_model=CheckInStartResponse)
def start_checkin(user_id: UUID = Depends(get_current_user_id)) -> CheckInStartResponse:
    result = CheckInSessionService().start_session(user_id)
    return CheckInStartResponse(**result)


@router.post("/{session_id}/respond", response_model=CheckInRespondResponse)
async def respond_to_checkin(
    session_id: UUID,
    audio: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
) -> CheckInRespondResponse:
    audio_bytes = await audio.read()
    try:
        result = await CheckInSessionService().respond(
            user_id,
            session_id,
            audio_bytes,
            audio.filename or "audio.webm",
            audio.content_type or "audio/webm",
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CheckInRespondResponse(**result)


@router.post("/{session_id}/verify", response_model=VerifyItemResponse)
def verify_checkin_item(
    session_id: UUID,
    payload: VerifyItemRequest,
    user_id: UUID = Depends(get_current_user_id),
) -> VerifyItemResponse:
    try:
        items_payload = [item.model_dump() for item in payload.items] if payload.items else None
        result = CheckInSessionService().verify_item(
            user_id,
            session_id,
            payload.item_id,
            payload.confirmed,
            payload.corrected_value,
            items_payload=items_payload,
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return VerifyItemResponse(**result)


@router.post("/{session_id}/items/{item_id}/voice-correct", response_model=VoiceCorrectItemResponse)
async def voice_correct_item(
    session_id: UUID,
    item_id: str,
    audio: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
) -> VoiceCorrectItemResponse:
    audio_bytes = await audio.read()
    try:
        result = await CheckInSessionService().voice_correct_item(
            user_id,
            session_id,
            item_id,
            audio_bytes,
            audio.filename or "correction.webm",
            audio.content_type or "audio/webm",
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return VoiceCorrectItemResponse(**result)


@router.post("/{session_id}/complete", response_model=CompleteStageResponse)
def complete_checkin_stage(
    session_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> CompleteStageResponse:
    try:
        result = CheckInSessionService().complete_stage(user_id, session_id)
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CompleteStageResponse(**result)


@router.get("/history", response_model=list[CheckInHistoryItem])
def get_checkin_history(user_id: UUID = Depends(get_current_user_id)) -> list[CheckInHistoryItem]:
    rows = CheckInRepository().list_by_user(user_id)
    return [CheckInHistoryItem(**row) for row in rows]


@router.get("/history/{checkin_id}", response_model=CheckInHistoryItem)
def get_checkin_history_detail(
    checkin_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> CheckInHistoryItem:
    row = CheckInRepository().get_by_id(user_id, checkin_id)
    if not row:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Check-in record not found")
    return CheckInHistoryItem(**row)
