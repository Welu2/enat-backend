from uuid import UUID

from fastapi import APIRouter, Depends

from app.config import get_settings
from app.dependencies import get_current_user_id
from app.services.reminders import ReminderService

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.get("")
def list_reminders(user_id: UUID = Depends(get_current_user_id)) -> list[dict]:
    return ReminderService().list_pending(user_id)


@router.post("/run-daily")
def run_daily_reminders() -> dict:
    settings = get_settings()
    if not settings.enable_dev_routes:
        return {"detail": "Daily reminder route disabled"}
    return ReminderService().run_daily_job()
