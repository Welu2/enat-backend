from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.core.clock import local_day_bounds, utc_now
from app.core.errors import NotFound
from app.db.data import get_data_client, transaction


class ReminderRepository:
    def create_once(self, user_id, kind, message, due_at, occurrence_key):
        with transaction() as conn:
            return conn.execute(
                """INSERT INTO reminders(user_id,type,message,due_at,occurrence_key)
                VALUES(%s,%s,%s,%s,%s) ON CONFLICT(user_id,occurrence_key)
                WHERE occurrence_key IS NOT NULL DO NOTHING RETURNING id""",
                (user_id, kind, message, due_at, occurrence_key),
            ).fetchone()

    def __init__(self, clock=utc_now):
        self.clock = clock

    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_data_client()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "dismissed": False,
            "created_at": self.clock().isoformat(),
            **data,
        }
        result = client.table("reminders").insert(payload).execute()
        return result.data[0]

    def list_pending(self, user_id: UUID) -> list[dict[str, Any]]:
        client = get_data_client()
        now = self.clock().isoformat()
        result = (
            client.table("reminders")
            .select("*")
            .eq("user_id", str(user_id))
            .eq("dismissed", False)
            .lte("due_at", now)
            .order("due_at", desc=False)
            .limit(50)
            .execute()
        )
        return result.data or []

    def exists_for_today(
        self, user_id: UUID, reminder_type: str, due_at: datetime
    ) -> bool:
        client = get_data_client()
        day_start, day_end = local_day_bounds(due_at)
        start, end = day_start.isoformat(), day_end.isoformat()
        result = (
            client.table("reminders")
            .select("id")
            .eq("user_id", str(user_id))
            .eq("type", reminder_type)
            .gte("due_at", start)
            .lt("due_at", end)
            .execute()
        )
        return bool(result.data if result else False)

    def dismiss(self, user_id: UUID, reminder_id: UUID) -> dict[str, Any]:
        client = get_data_client()
        result = (
            client.table("reminders")
            .update({"dismissed": True})
            .eq("id", str(reminder_id))
            .eq("user_id", str(user_id))
            .execute()
        )
        if not result or not result.data:
            raise NotFound("Notification not found")
        return result.data[0]
