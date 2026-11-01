from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status

from app.core.errors import NotFound
from app.db import idempotency
from app.db.repositories.calendar_items import CalendarItemRepository
from app.dependencies import get_current_user
from app.models.calendar import (
    CalendarItemCreate,
    CalendarItemResponse,
    CalendarItemType,
    CalendarItemUpdate,
)

router = APIRouter(prefix="/users/me/calendar/items", tags=["calendar"])


@router.get("", response_model=list[CalendarItemResponse])
def list_calendar_items(
    from_date: date | None = Query(default=None),
    to_date: date | None = Query(default=None),
    type: CalendarItemType | None = Query(default=None),
    current_user: dict = Depends(get_current_user),
) -> list[CalendarItemResponse]:
    """List calendar events and tasks for the authenticated mother."""
    user_id = UUID(current_user["id"])
    repo = CalendarItemRepository()
    items = repo.list_by_user(
        user_id=user_id,
        from_date=from_date.isoformat() if from_date else None,
        to_date=to_date.isoformat() if to_date else None,
        item_type=type,
    )
    return [CalendarItemResponse(**item) for item in items]


@router.post("", response_model=CalendarItemResponse, status_code=status.HTTP_201_CREATED)
def create_calendar_item(
    payload: CalendarItemCreate,
    key: str | None = Header(default=None, alias="Idempotency-Key", max_length=128),
    current_user: dict = Depends(get_current_user),
) -> CalendarItemResponse:
    """Create a new calendar event or task."""
    user_id = UUID(current_user["id"])
    data = payload.model_dump()
    data["date"] = payload.date.isoformat()
    if payload.time:
        data["time"] = payload.time.isoformat()
    if payload.reminder_at:
        data["reminder_at"] = payload.reminder_at.isoformat()

    repo = CalendarItemRepository()
    if key:
        created = idempotency.execute(
            user_id,
            "calendar_item:create",
            key,
            data,
            lambda: repo.create(user_id, data),
        )
    else:
        created = repo.create(user_id, data)

    return CalendarItemResponse(**created)


@router.get("/{item_id}", response_model=CalendarItemResponse)
def get_calendar_item(
    item_id: UUID,
    current_user: dict = Depends(get_current_user),
) -> CalendarItemResponse:
    """Retrieve a specific calendar event or task."""
    user_id = UUID(current_user["id"])
    item = CalendarItemRepository().get_by_id(user_id, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar item not found",
        )
    return CalendarItemResponse(**item)


@router.put("/{item_id}", response_model=CalendarItemResponse)
def update_calendar_item(
    item_id: UUID,
    payload: CalendarItemUpdate,
    current_user: dict = Depends(get_current_user),
) -> CalendarItemResponse:
    """Update a calendar event or task."""
    user_id = UUID(current_user["id"])
    data = payload.model_dump(exclude_unset=True)
    if "date" in data and data["date"] is not None:
        data["date"] = data["date"].isoformat()
    if "time" in data and data["time"] is not None:
        data["time"] = data["time"].isoformat()
    if "reminder_at" in data and data["reminder_at"] is not None:
        data["reminder_at"] = data["reminder_at"].isoformat()

    try:
        updated = CalendarItemRepository().update(user_id, item_id, data)
    except NotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar item not found",
        )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar item not found",
        )
    return CalendarItemResponse(**updated)


@router.delete("/{item_id}")
def delete_calendar_item(
    item_id: UUID,
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    """Delete a calendar event or task."""
    user_id = UUID(current_user["id"])
    deleted = CalendarItemRepository().delete(user_id, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar item not found",
        )
    return {"status": "deleted"}
