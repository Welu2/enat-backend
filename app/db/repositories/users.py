from typing import Any
from uuid import UUID

from app.core.errors import NotFound
from app.db.data import get_data_client


class UserRepository:
    def get_by_id(self, user_id: UUID) -> dict[str, Any] | None:
        client = get_data_client()
        result = (
            client.table("users")
            .select("*")
            .eq("id", str(user_id))
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def list_all(self) -> list[dict[str, Any]]:
        client = get_data_client()
        result = client.table("users").select("*").execute()
        return result.data or []

    def update_profile(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_data_client()
        result = client.table("users").update(data).eq("id", str(user_id)).execute()
        if not result.data:
            raise NotFound("User not found")
        return result.data[0]

    def update_hospital(self, user_id: UUID, hospital: str) -> dict[str, Any]:
        return self.update_profile(user_id, {"hospital": hospital})
