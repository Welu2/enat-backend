from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import Response

from app.dependencies import get_current_user_id
from app.models.summary import (
    PublicSummaryResponse,
    SummaryGenerateRequest,
    SummaryGenerateResponse,
    SummaryLatestResponse,
)
from app.services.sharing import (
    ShareQRRequest,
    ShareRequest,
    create_share,
    render_share_qr,
    revoke_share,
)
from app.services.summary import SummaryService

router = APIRouter(prefix="/summary", tags=["summary"])


@router.post("/generate", response_model=SummaryGenerateResponse)
def generate_summary(
    payload: SummaryGenerateRequest,
    key: str = Header(..., alias="Idempotency-Key", min_length=8, max_length=128),
    user_id: UUID = Depends(get_current_user_id),
) -> SummaryGenerateResponse:
    summary = SummaryService().generate(
        user_id,
        period_start=payload.period_start,
        period_end=payload.period_end,
        key=key,
    )
    return SummaryGenerateResponse(**summary)


@router.get("/latest", response_model=SummaryLatestResponse)
def get_latest_summary(
    user_id: UUID = Depends(get_current_user_id),
) -> SummaryLatestResponse:
    summary = SummaryService().get_latest(user_id)
    if not summary:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No summary found")
    return SummaryLatestResponse(**summary)


@router.get("/{share_link_slug}", response_model=PublicSummaryResponse)
def get_public_summary(share_link_slug: str) -> PublicSummaryResponse:
    summary = SummaryService().get_public(share_link_slug)
    if not summary:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Summary not found")
    return PublicSummaryResponse(**summary)


@router.post("/check-automatic")
def check_automatic_summary(user_id: UUID = Depends(get_current_user_id)) -> dict:
    summary = SummaryService().check_and_generate_auto_summary(user_id)
    if not summary:
        return {
            "status": "no_summary_due",
            "message": "No automatic summary is due at this time.",
        }
    return {"status": "summary_generated", "summary": summary}


@router.post("/{summary_id}/shares", status_code=201)
def share_summary(
    summary_id: UUID,
    payload: ShareRequest,
    user_id: UUID = Depends(get_current_user_id),
):
    return create_share(user_id, summary_id, payload)


@router.delete("/shares/{share_id}", status_code=204)
def revoke_summary_share(share_id: UUID, user_id: UUID = Depends(get_current_user_id)):
    revoke_share(user_id, share_id)


@router.post(
    "/shares/{share_id}/qr",
    response_class=Response,
    responses={
        200: {
            "content": {"image/png": {"schema": {"type": "string", "format": "binary"}}}
        }
    },
)
def retry_share_qr(
    share_id: UUID,
    payload: ShareQRRequest,
    user_id: UUID = Depends(get_current_user_id),
):
    return Response(
        render_share_qr(user_id, share_id, payload.token), media_type="image/png"
    )
