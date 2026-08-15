from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.db.client import get_supabase_client


class SupplementRepository:
    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "created_at": datetime.utcnow().isoformat(),
            **data,
        }
        result = client.table("supplements").insert(payload).execute()
        return result.data[0]

    def update(self, user_id: UUID, supplement_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        result = (
            client.table("supplements")
            .update(data)
            .eq("id", str(supplement_id))
            .eq("user_id", str(user_id))
            .execute()
        )
        if not result.data:
            raise ValueError("Supplement not found")
        return result.data[0]

    def list_active(self, user_id: UUID) -> list[dict[str, Any]]:
        client = get_supabase_client()
        result = (
            client.table("supplements")
            .select("*")
            .eq("user_id", str(user_id))
            .eq("active", True)
            .execute()
        )
        return result.data or []

    def list_all(self, user_id: UUID) -> list[dict[str, Any]]:
        client = get_supabase_client()
        result = (
            client.table("supplements")
            .select("*")
            .eq("user_id", str(user_id))
            .execute()
        )
        return result.data or []
