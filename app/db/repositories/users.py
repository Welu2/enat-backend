from datetime import datetime
from typing import Any
from uuid import UUID

from app.db.client import get_supabase_client


class UserRepository:
    def upsert(self, user_id: UUID, email: str | None) -> dict[str, Any]:
        client = get_supabase_client()
        payload = {
            "id": str(user_id),
            "email": email,
            "created_at": datetime.utcnow().isoformat(),
        }
        result = client.table("users").upsert(payload).execute()
        return result.data[0]

    def get_by_id(self, user_id: UUID) -> dict[str, Any] | None:
        client = get_supabase_client()
        result = (
            client.table("users")
            .select("*")
            .eq("id", str(user_id))
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def list_all(self) -> list[dict[str, Any]]:
        client = get_supabase_client()
        result = client.table("users").select("*").execute()
        return result.data or []

    def update_profile(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        result = (
            client.table("users")
            .update(data)
            .eq("id", str(user_id))
            .execute()
        )
        if not result.data:
            raise ValueError("User not found")
        return result.data[0]

    def update_hospital(self, user_id: UUID, hospital: str) -> dict[str, Any]:
        return self.update_profile(user_id, {"hospital": hospital})
