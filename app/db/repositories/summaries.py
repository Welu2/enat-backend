from typing import Any
from uuid import UUID, uuid4

from app.core.clock import utc_now
from app.db.data import get_data_client


class SummaryRepository:
    def __init__(self, clock=utc_now):
        self.clock = clock

    def get_by_generation_key(self, user_id, key):
        return (
            get_data_client()
            .table("summaries")
            .select()
            .eq("user_id", str(user_id))
            .eq("generation_key", key)
            .maybe_single()
            .execute()
            .data
        )

    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_data_client()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "generated_at": self.clock().isoformat(),
            **data,
        }
        result = client.table("summaries").insert(payload).execute()
        return result.data[0]

    def get_latest(self, user_id: UUID) -> dict[str, Any] | None:
        client = get_data_client()
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
        # Legacy slugs are intentionally invalid after migration 005.
        from app.services.sharing import read_share

        return read_share(slug)
