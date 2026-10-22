from typing import Any

from app.db.data import transaction
from app.services.clinical_policy import confirmed_items, danger


def create_for_checkin(record: dict[str, Any]) -> str | None:
    categories = sorted(
        {i["category"] for i in confirmed_items(record["symptoms"]) if danger(i)}
    )
    if not categories:
        return None
    with transaction() as conn:
        row = conn.execute(
            "INSERT INTO emergency_alerts(patient_id,check_in_id,categories,recorded_at,received_at,policy_version) "
            "VALUES(%s,%s,%s,%s,%s,%s) ON CONFLICT(check_in_id) DO NOTHING RETURNING id",
            (
                record["user_id"],
                record["id"],
                categories,
                record["recorded_at"],
                record["received_at"],
                record["policy_version"],
            ),
        ).fetchone()
        if row is None:
            row = conn.execute(
                "SELECT id FROM emergency_alerts WHERE check_in_id=%s", (record["id"],)
            ).fetchone()
        return str(row["id"])
