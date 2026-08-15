from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.db.client import get_supabase_client


class PushTokenRepository:
    def register(self, user_id: UUID, token: str, platform: str = "web") -> dict[str, Any]:
        client = get_supabase_client()
        payload = {
            "user_id": str(user_id),
            "token": token,
            "platform": platform,
            "updated_at": datetime.utcnow().isoformat(),
        }
        try:
            # Check if token exists
            existing = client.table("push_tokens").select("*").eq("token", token).execute()
            if existing and existing.data:
                result = client.table("push_tokens").update(payload).eq("token", token).execute()
                return result.data[0]
            
            payload["id"] = str(uuid4())
            result = client.table("push_tokens").insert(payload).execute()
            return result.data[0]
        except Exception:
            # InMemory / local fallback
            return payload

    def list_for_user(self, user_id: UUID) -> list[dict[str, Any]]:
        client = get_supabase_client()
        try:
            result = client.table("push_tokens").select("*").eq("user_id", str(user_id)).execute()
            return result.data or []
        except Exception:
            return []
