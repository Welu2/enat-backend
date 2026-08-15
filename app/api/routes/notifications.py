from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.db.repositories.reminders import ReminderRepository
from app.dependencies import get_current_user_id
from app.services.reminders import ReminderService


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


@router.get("", response_model=list[NotificationItem])
@router.get("/", response_model=list[NotificationItem])
def get_notifications(user_id: UUID = Depends(get_current_user_id)) -> list[NotificationItem]:
    """Retrieve active notification messages for supplements, appointments, and generated reports."""
    notifications = ReminderService().list_pending(user_id)
    return [NotificationItem(**item) for item in notifications]


@router.post("/{notification_id}/dismiss")
def dismiss_notification(
    notification_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> dict[str, Any]:
    """Dismiss a specific notification."""
    try:
        updated = ReminderRepository().dismiss(user_id, notification_id)
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return {"status": "dismissed", "notification": updated}
