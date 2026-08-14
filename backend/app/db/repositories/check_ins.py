from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.db.client import get_supabase_client


class CheckInRepository:
    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "timestamp": datetime.utcnow().isoformat(),
            **data,
        }
        result = client.table("check_ins").insert(payload).execute()
        return result.data[0]

    def list_by_user(self, user_id: UUID) -> list[dict[str, Any]]:
        client = get_supabase_client()
        result = (
            client.table("check_ins")
            .select("*")
            .eq("user_id", str(user_id))
            .order("timestamp", desc=True)
            .execute()
        )
        return result.data or []

    def list_in_period(
        self, user_id: UUID, period_start: datetime, period_end: datetime
    ) -> list[dict[str, Any]]:
        client = get_supabase_client()
        result = (
            client.table("check_ins")
            .select("*")
            .eq("user_id", str(user_id))
            .gte("timestamp", period_start.isoformat())
            .lte("timestamp", period_end.isoformat())
            .order("timestamp", desc=False)
            .execute()
        )
        return result.data or []
