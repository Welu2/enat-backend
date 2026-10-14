from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel

from app.api.routes.reminders import list_reminders
from app.db.pagination import PAGE_RESPONSE
from app.db.repositories.reminders import ReminderRepository
from app.dependencies import get_current_user_id


class NotificationItem(BaseModel):
    id: UUID
    user_id: UUID
    type: str
    message: str
    due_at: datetime
    dismissed: bool
    created_at: datetime
    extra_data: dict[str, Any] | None = None


router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationItem], responses=PAGE_RESPONSE)
@router.get("/", response_model=list[NotificationItem], responses=PAGE_RESPONSE)
def get_notifications(
    response: Response,
    user_id: UUID = Depends(get_current_user_id),
    limit: int = Query(50, ge=1, le=100),
    cursor: str | None = Query(None, max_length=256),
) -> list[NotificationItem]:
    """Retrieve active notification messages for supplements, appointments, and generated reports."""
    notifications = list_reminders(response, user_id, limit, cursor)
    return [NotificationItem(**item) for item in notifications]


@router.post("/{notification_id}/dismiss")
def dismiss_notification(
    notification_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> dict[str, Any]:
    """Dismiss a specific notification."""
    updated = ReminderRepository().dismiss(user_id, notification_id)
    return {"status": "dismissed", "notification": updated}
