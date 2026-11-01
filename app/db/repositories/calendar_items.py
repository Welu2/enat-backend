from typing import Any
from uuid import UUID, uuid4

from app.core.clock import utc_now
from app.core.errors import NotFound
from app.db.data import get_data_client


class CalendarItemRepository:
    def __init__(self, clock=utc_now):
        self.clock = clock

    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_data_client()
        now = self.clock().isoformat()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "created_at": now,
            "updated_at": now,
            **data,
        }
        result = client.table("calendar_items").insert(payload).execute()
        return result.data[0]

    def list_by_user(
        self,
        user_id: UUID,
        from_date: str | None = None,
        to_date: str | None = None,
        item_type: str | None = None,
    ) -> list[dict[str, Any]]:
        client = get_data_client()
        query = (
            client.table("calendar_items")
            .select("*")
            .eq("user_id", str(user_id))
        )
        if from_date:
            query = query.gte("date", from_date)
        if to_date:
            query = query.lte("date", to_date)
        if item_type:
            query = query.eq("type", item_type)

        query = query.order("date", desc=False)
        result = query.execute()
        items = result.data or []
        items.sort(key=lambda r: (r.get("date") or "", r.get("time") or ""))
        return items

    def get_by_id(self, user_id: UUID, item_id: UUID) -> dict[str, Any] | None:
        client = get_data_client()
        result = (
            client.table("calendar_items")
            .select("*")
            .eq("id", str(item_id))
            .eq("user_id", str(user_id))
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def update(
        self, user_id: UUID, item_id: UUID, data: dict[str, Any]
    ) -> dict[str, Any]:
        client = get_data_client()
        payload = {
            **data,
            "updated_at": self.clock().isoformat(),
        }
        result = (
            client.table("calendar_items")
            .update(payload)
            .eq("id", str(item_id))
            .eq("user_id", str(user_id))
            .execute()
        )
        if not result.data:
            raise NotFound("Calendar item not found")
        return result.data[0]

    def delete(self, user_id: UUID, item_id: UUID) -> bool:
        client = get_data_client()
        result = (
            client.table("calendar_items")
            .delete()
            .eq("id", str(item_id))
            .eq("user_id", str(user_id))
            .execute()
        )
        return bool(result.data if result else False)
