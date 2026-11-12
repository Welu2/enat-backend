from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query

from app.dependencies import get_current_user_id
from app.models.privacy import (
    DeletionRequest,
    ExportManifest,
    ExportPage,
    ExportSection,
    PrivacyRequestResponse,
)
from app.services import privacy

router = APIRouter(prefix="/users/me/privacy", tags=["privacy"])


@router.get("/export", response_model=ExportManifest)
def export_manifest(user_id: UUID = Depends(get_current_user_id)):
    return privacy.manifest()


@router.get("/export/{section}", response_model=ExportPage)
def export_page(
    section: ExportSection,
    limit: int = Query(50, ge=1, le=100),
    after: UUID | None = None,
    user_id: UUID = Depends(get_current_user_id),
):
    return privacy.export_page(user_id, section, limit, after)


@router.post("/requests", response_model=PrivacyRequestResponse, status_code=202)
def request_deletion(
    payload: DeletionRequest,
    user_id: UUID = Depends(get_current_user_id),
    key: str = Header(..., alias="Idempotency-Key", min_length=8, max_length=128),
):
    return privacy.create_deletion_request(user_id, key)


@router.post("/requests/{request_id}/cancel", response_model=PrivacyRequestResponse)
def cancel_request(request_id: UUID, user_id: UUID = Depends(get_current_user_id)):
    return privacy.cancel_request(user_id, request_id)
