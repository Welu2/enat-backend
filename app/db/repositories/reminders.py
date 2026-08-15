from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.db.client import get_supabase_client


class ReminderRepository:
    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "dismissed": False,
            "created_at": datetime.utcnow().isoformat(),
            **data,
        }
        result = client.table("reminders").insert(payload).execute()
        return result.data[0]

    def list_pending(self, user_id: UUID) -> list[dict[str, Any]]:
        client = get_supabase_client()
        now = datetime.utcnow().isoformat()
        result = (
            client.table("reminders")
            .select("*")
            .eq("user_id", str(user_id))
            .eq("dismissed", False)
            .lte("due_at", now)
            .order("due_at", desc=False)
            .execute()
        )
        return result.data or []

    def exists_for_today(self, user_id: UUID, reminder_type: str, due_at: datetime) -> bool:
        client = get_supabase_client()
        start = due_at.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        end = due_at.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()
        result = (
            client.table("reminders")
            .select("id")
            .eq("user_id", str(user_id))
            .eq("type", reminder_type)
            .gte("due_at", start)
            .lte("due_at", end)
            .execute()
        )
        return bool(result.data if result else False)

    def dismiss(self, user_id: UUID, reminder_id: UUID) -> dict[str, Any]:
        client = get_supabase_client()
        result = (
            client.table("reminders")
            .update({"dismissed": True})
            .eq("id", str(reminder_id))
            .eq("user_id", str(user_id))
            .execute()
        )
        if not result or not result.data:
            raise ValueError("Notification not found")
        return result.data[0]
