import uuid
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from app.db.client import get_supabase_client


class UserRepository:
    def upsert(self, user_id: UUID, email: str | None) -> dict[str, Any]:
        client = get_supabase_client()
        payload = {
            "id": str(user_id),
            "email": email,
            "created_at": datetime.now(timezone.utc).isoformat(),
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

    def get_by_telegram_id(self, telegram_id: str) -> dict[str, Any] | None:
        """Fetch a user record using their unique Telegram ID."""
        client = get_supabase_client()
        result = (
            client.table("users")
            .select("*")
            .eq("telegram_id", str(telegram_id))
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def create_from_telegram(self, tg_user: dict[str, Any]) -> dict[str, Any]:
        """Auto-provisions a new user profile upon first Telegram Mini App launch."""
        client = get_supabase_client()
        new_uuid = str(uuid.uuid4())
        payload = {
            "id": new_uuid,
            "telegram_id": str(tg_user.get("id")),
            "first_name": tg_user.get("first_name"),
            "username": tg_user.get("username"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        result = client.table("users").insert(payload).execute()
        if not result.data:
            raise ValueError("Failed to create user from Telegram data")
        return result.data[0]

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