from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.db.client import get_supabase_client


class AppointmentRepository:
    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            **data,
        }
        result = client.table("appointments").insert(payload).execute()
        return result.data[0]

    def update(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        result = (
            client.table("appointments")
            .update(data)
            .eq("user_id", str(user_id))
            .execute()
        )
        if not result.data:
            raise ValueError("Appointment not found")
        return result.data[0]

    def get_by_user(self, user_id: UUID) -> dict[str, Any] | None:
        client = get_supabase_client()
        result = (
            client.table("appointments")
            .select("*")
            .eq("user_id", str(user_id))
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def update_last_summary_generated_at(self, user_id: UUID, generated_at: datetime) -> None:
        client = get_supabase_client()
        client.table("appointments").update(
            {"last_summary_generated_at": generated_at.isoformat()}
        ).eq("user_id", str(user_id)).execute()
