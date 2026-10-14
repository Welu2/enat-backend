from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Header,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from fastapi.responses import Response

from app.db.pagination import PAGE_RESPONSE
from app.db.repositories.check_ins import CheckInRepository
from app.dependencies import get_current_user_id
from app.models.checkin import (
    CheckInHistoryItem,
    CheckInRespondResponse,
    CheckInStartResponse,
    CheckInStateResponse,
    CompleteStageRequest,
    CompleteStageResponse,
    VerifyItemRequest,
    VerifyItemResponse,
    VoiceCorrectItemResponse,
)
from app.services.audio_upload import read_audio
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


@router.get(
    "/prompts/{stage}/audio",
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
async def get_stage_prompt_audio(stage: str) -> Response:
    """Streams the stored/pre-cached Amharic question prompt audio for the given stage (zero redundant TTS calls)."""
    audio_bytes = await get_or_synthesize_stage_audio(stage)
    return Response(
        content=audio_bytes,
        media_type="audio/wav" if audio_bytes.startswith(b"RIFF") else "audio/mpeg",
        headers={"Content-Disposition": "inline"},
    )


@router.post("/start", response_model=CheckInStartResponse)
def start_checkin(
    user_id: UUID = Depends(get_current_user_id),
    key: str = Header(..., alias="Idempotency-Key", min_length=8, max_length=128),
) -> CheckInStartResponse:
    result = CheckInSessionService().start_session(user_id, key=key)
    return CheckInStartResponse(**result)


@router.post("/{session_id}/respond", response_model=CheckInRespondResponse)
async def respond_to_checkin(
    session_id: UUID,
    expected_version: int = Header(..., alias="X-Session-Version", ge=0),
    key: str = Header(..., alias="Idempotency-Key", min_length=8, max_length=128),
    audio: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
) -> CheckInRespondResponse:
    audio_bytes = await read_audio(audio)
    result = await CheckInSessionService().respond(
        user_id,
        session_id,
        audio_bytes,
        audio.filename or "audio.webm",
        audio.content_type or "audio/webm",
        expected_version=expected_version,
        key=key,
    )
    return CheckInRespondResponse(**result)


@router.post("/{session_id}/verify", response_model=VerifyItemResponse)
def verify_checkin_item(
    session_id: UUID,
    payload: VerifyItemRequest,
    expected_version: int = Header(..., alias="X-Session-Version", ge=0),
    key: str = Header(..., alias="Idempotency-Key", min_length=8, max_length=128),
    user_id: UUID = Depends(get_current_user_id),
) -> VerifyItemResponse:
    items_payload = [item.model_dump(exclude_unset=True) for item in payload.items]
    result = CheckInSessionService().verify_item(
        user_id,
        session_id,
        items_payload=items_payload,
        expected_version=expected_version,
        key=key,
    )
    return VerifyItemResponse(**result)


@router.post(
    "/{session_id}/items/{item_id}/voice-correct",
    response_model=VoiceCorrectItemResponse,
)
async def voice_correct_item(
    session_id: UUID,
    item_id: str,
    expected_version: int = Header(..., alias="X-Session-Version", ge=0),
    key: str = Header(..., alias="Idempotency-Key", min_length=8, max_length=128),
    audio: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
) -> VoiceCorrectItemResponse:
    audio_bytes = await read_audio(audio)
    result = await CheckInSessionService().voice_correct_item(
        user_id,
        session_id,
        item_id,
        audio_bytes,
        audio.filename or "correction.webm",
        audio.content_type or "audio/webm",
        expected_version=expected_version,
        key=key,
    )
    return VoiceCorrectItemResponse(**result)


@router.post("/{session_id}/complete", response_model=CompleteStageResponse)
def complete_checkin_stage(
    session_id: UUID,
    payload: CompleteStageRequest,
    expected_version: int = Header(..., alias="X-Session-Version", ge=0),
    key: str = Header(..., alias="Idempotency-Key", min_length=8, max_length=128),
    user_id: UUID = Depends(get_current_user_id),
) -> CompleteStageResponse:
    result = CheckInSessionService().complete_stage(
        user_id,
        session_id,
        expected_version=expected_version,
        key=key,
        skip=payload.skip,
    )
    return CompleteStageResponse(**result)


@router.get(
    "/history", response_model=list[CheckInHistoryItem], responses=PAGE_RESPONSE
)
def get_checkin_history(
    response: Response,
    user_id: UUID = Depends(get_current_user_id),
    limit: int = Query(50, ge=1, le=100),
    cursor: str | None = Query(None, max_length=256),
) -> list[CheckInHistoryItem]:
    from app.db.pagination import page

    rows, next_cursor = page("check_ins", user_id, limit, cursor)
    if next_cursor:
        response.headers["X-Next-Cursor"] = next_cursor
    return [CheckInHistoryItem(**row) for row in rows]


@router.get("/history/{checkin_id}", response_model=CheckInHistoryItem)
def get_checkin_history_detail(
    checkin_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> CheckInHistoryItem:
    row = CheckInRepository().get_by_id(user_id, checkin_id)
    if not row:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Check-in record not found"
        )
    return CheckInHistoryItem(**row)


@router.get("/{session_id}/state", response_model=CheckInStateResponse)
def get_checkin_state(session_id: UUID, user_id: UUID = Depends(get_current_user_id)):
    return CheckInSessionService().get_state(user_id, session_id)
