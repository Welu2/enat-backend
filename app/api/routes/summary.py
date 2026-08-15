from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user_id
from app.models.summary import PublicSummaryResponse, SummaryGenerateResponse, SummaryLatestResponse
from app.services.summary import SummaryService

router = APIRouter(prefix="/summary", tags=["summary"])


@router.post("/generate", response_model=SummaryGenerateResponse)
def generate_summary(user_id: UUID = Depends(get_current_user_id)) -> SummaryGenerateResponse:
    try:
        summary = SummaryService().generate(user_id)
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return SummaryGenerateResponse(**summary)


@router.get("/latest", response_model=SummaryLatestResponse)
def get_latest_summary(user_id: UUID = Depends(get_current_user_id)) -> SummaryLatestResponse:
    summary = SummaryService().get_latest(user_id)
    if not summary:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No summary found")
    return SummaryLatestResponse(**summary)


@router.get("/public/{share_link_slug}", response_model=PublicSummaryResponse)
def get_public_summary(share_link_slug: str) -> PublicSummaryResponse:
    summary = SummaryService().get_public(share_link_slug)
    if not summary:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Summary not found")
    return PublicSummaryResponse(**summary)


@router.post("/check-automatic")
def check_automatic_summary(user_id: UUID = Depends(get_current_user_id)) -> dict:
    summary = SummaryService().check_and_generate_auto_summary(user_id)
    if not summary:
        return {"status": "no_summary_due", "message": "No automatic summary is due at this time."}
    return {"status": "summary_generated", "summary": summary}
