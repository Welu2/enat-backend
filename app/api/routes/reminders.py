from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.db.pagination import PAGE_RESPONSE
from app.dependencies import get_current_user_id

router = APIRouter(prefix="/reminders", tags=["reminders"])
dev_router = APIRouter(prefix="/reminders", tags=["development"])


@router.get("", responses=PAGE_RESPONSE)
def list_reminders(
    response: Response,
    user_id: UUID = Depends(get_current_user_id),
    limit: int = Query(50, ge=1, le=100),
    cursor: str | None = Query(None, max_length=256),
) -> list[dict]:
    from app.core.clock import utc_now
    from app.db.pagination import page

    rows, next_cursor = page("reminders", user_id, limit, cursor, due=utc_now())
    if next_cursor:
        response.headers["X-Next-Cursor"] = next_cursor
    return rows


@dev_router.post("/run-daily")
def run_daily_reminders() -> dict:
    raise HTTPException(410, "Run the separate scheduler process")
