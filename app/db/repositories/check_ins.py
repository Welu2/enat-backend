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

    def get_by_id(self, user_id: UUID, checkin_id: UUID) -> dict[str, Any] | None:
        client = get_supabase_client()
        result = (
            client.table("check_ins")
            .select("*")
            .eq("id", str(checkin_id))
            .eq("user_id", str(user_id))
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def has_supplement_logged_today(self, user_id: UUID) -> bool:
        client = get_supabase_client()
        today_start = datetime.combine(datetime.utcnow().date(), datetime.min.time()).isoformat()
        try:
            result = (
                client.table("check_ins")
                .select("supplement_check")
                .eq("user_id", str(user_id))
                .gte("timestamp", today_start)
                .execute()
            )
            if result and result.data:
                for row in result.data:
                    supp = row.get("supplement_check")
                    if supp and isinstance(supp, dict) and supp.get("confirmed"):
                        return True
        except Exception:
            pass
        return False
