from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.db.client import get_supabase_client


class SummaryRepository:
    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_supabase_client()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "generated_at": datetime.utcnow().isoformat(),
            **data,
        }
        result = client.table("summaries").insert(payload).execute()
        return result.data[0]

    def get_latest(self, user_id: UUID) -> dict[str, Any] | None:
        client = get_supabase_client()
        result = (
            client.table("summaries")
            .select("*")
            .eq("user_id", str(user_id))
            .order("generated_at", desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def get_by_slug(self, slug: str) -> dict[str, Any] | None:
        client = get_supabase_client()
        result = (
            client.table("summaries")
            .select(
                "period_start, period_end, generated_at, content_json, "
                "anc_contact_number, anc_contact_title, anc_contact_title_am, target_gestational_weeks"
            )
            .eq("share_link_slug", slug)
            .maybe_single()
            .execute()
        )
        return result.data if result else None
