from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.core.clock import local_day_bounds, utc_now
from app.db.data import atomic, get_data_client, normalize, transaction
from app.services.clinical_policy import (
    POLICY_VERSION,
    confirmed_items,
    danger,
    validated_draft,
)


class CheckInRepository:
    def __init__(self, clock=utc_now):
        self.clock = clock

    @atomic
    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        from app.services.alerts import create_for_checkin

        client = get_data_client()
        data = {**data, **validated_draft(data), "policy_version": POLICY_VERSION}
        now = self.clock().isoformat()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            **data,
            "timestamp": now,
            "received_at": now,
            "recorded_at": data.get("recorded_at", now),
            "danger_sign_triggered": any(danger(i) for i in data["symptoms"]),
        }
        result = client.table("check_ins").insert(payload).execute()
        create_for_checkin(result.data[0])
        return result.data[0]

    def list_by_user(self, user_id: UUID) -> list[dict[str, Any]]:
        client = get_data_client()
        result = (
            client.table("check_ins")
            .select("*")
            .eq("user_id", str(user_id))
            .order("timestamp", desc=True)
            .execute()
        )
        return result.data or []

    def list_in_period(
        self, user_id: UUID, period_start: datetime, period_end: datetime
    ) -> list[dict[str, Any]]:
        from app.db.pagination import page

        rows, cursor = [], None
        while True:
            batch, cursor = page(
                "check_ins", user_id, 100, cursor, start=period_start, end=period_end
            )
            rows.extend(batch)
            if cursor is None:
                return list(reversed(rows))

    def get_by_id(self, user_id: UUID, checkin_id: UUID) -> dict[str, Any] | None:
        client = get_data_client()
        result = (
            client.table("check_ins")
            .select("*")
            .eq("id", str(checkin_id))
            .eq("user_id", str(user_id))
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def _logged_today(self, user_id, key):
        start, end = local_day_bounds(self.clock())
        return any(
            confirmed_items(row.get(key))
            for row in self.list_observed_in_period(user_id, start, end)
        )

    def list_observed_in_period(self, user_id, start, end):
        with transaction() as conn:
            return normalize(
                conn.execute(
                    "SELECT * FROM check_ins WHERE user_id=%s AND recorded_at>=%s AND recorded_at<%s ORDER BY recorded_at,id",
                    (user_id, start, end),
                ).fetchall()
            )

    def has_supplement_logged_today(self, user_id):
        # All active named supplements must have a confirmed observation today.
        from app.db.repositories.supplements import SupplementRepository

        names = {
            s["name"].strip().casefold()
            for s in SupplementRepository(self.clock).list_active(user_id)
        }
        start, end = local_day_bounds(self.clock())
        observed = {
            i.get("supplement_name", "").strip().casefold()
            for r in self.list_observed_in_period(user_id, start, end)
            for i in confirmed_items(r.get("supplement_check"))
            if type(i.get("taken_today")) is bool
        }
        return bool(names) and names <= observed

    def has_food_logged_today(self, user_id):
        return self._logged_today(user_id, "food_log")
