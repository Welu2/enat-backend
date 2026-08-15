from datetime import datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

from app.db.client import get_supabase_client


class CheckInSessionRepository:
    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        now = datetime.utcnow()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "status": "in_progress",
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(hours=2)).isoformat(),
            **data,
        }
        result = client.table("check_in_sessions").insert(payload).execute()
        return result.data[0]

    def get(self, session_id: UUID, user_id: UUID) -> dict[str, Any] | None:
        client = get_supabase_client()
        result = (
            client.table("check_in_sessions")
            .select("*")
            .eq("id", str(session_id))
            .eq("user_id", str(user_id))
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def update(self, session_id: UUID, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        result = (
            client.table("check_in_sessions")
            .update(data)
            .eq("id", str(session_id))
            .eq("user_id", str(user_id))
            .execute()
        )
        if not result.data:
            raise ValueError("Session not found")
        return result.data[0]
