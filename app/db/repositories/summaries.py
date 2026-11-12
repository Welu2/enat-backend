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
        slug = data.get("share_link_slug") or f"report-{uuid4().hex[:12]}"
        qr = data.get("qr_code_url") or f"/summary/{slug}/qr"
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "generated_at": self.clock().isoformat(),
            "period_start": data.get("period_start"),
            "period_end": data.get("period_end"),
            "content_json": data.get("content_json"),
            "share_link_slug": slug,
            "qr_code_url": qr,
            "anc_contact_number": data.get("anc_contact_number"),
            "anc_contact_title": data.get("anc_contact_title"),
            "anc_contact_title_am": data.get("anc_contact_title_am"),
            "target_gestational_weeks": data.get("target_gestational_weeks"),
        }
        if "generation_key" in data and data["generation_key"]:
            payload["generation_key"] = data["generation_key"]
        if "window_start" in data and data["window_start"]:
            payload["window_start"] = data["window_start"]
        if "window_end" in data and data["window_end"]:
            payload["window_end"] = data["window_end"]

        try:
            result = client.table("summaries").insert(payload).execute()
        except Exception:
            for col in ("generation_key", "window_start", "window_end"):
                payload.pop(col, None)
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
