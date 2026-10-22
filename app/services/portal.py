from typing import Any
from uuid import UUID

from app.core.errors import NotFound
from app.db import idempotency
from app.db.data import current_user_id, transaction
from app.db.pagination import decode, encode
from app.db.repositories.care_connections import call
from app.services.care_access import require_portal, uuid_cursor
from app.services.extraction import _category_display


def identity() -> dict[str, Any]:
    require_portal()
    result = call("enat_portal_me")
    if result is None:
        raise NotFound("Account unavailable")
    return dict(result)


def patients(limit: int, cursor: str | None) -> tuple[list[dict[str, Any]], str | None]:
    require_portal()
    rows = call("enat_portal_patients", limit, uuid_cursor(cursor))
    if rows is None:
        raise NotFound("Account unavailable")
    return rows[:limit], str(rows[limit - 1]["id"]) if len(rows) > limit else None


def read(
    patient_id: UUID,
    resource: str,
    limit: int = 50,
    cursor: str | None = None,
    status: str | None = None,
) -> Any:
    require_portal()
    stamp, identifier = decode(cursor) if cursor else (None, None)
    result = call(
        "enat_portal_read", patient_id, resource, limit, stamp, identifier, status
    )
    if result is None:
        raise NotFound("Patient unavailable")
    value = result["data"]
    if value is None and resource != "appointment":
        raise NotFound("Resource unavailable")
    return value


def label_alert(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "category_labels": [
            {
                "category": c,
                "en": _category_display(c, "en"),
                "am": _category_display(c, "am"),
            }
            for c in row["categories"]
        ],
    }


def history(
    patient_id: UUID,
    resource: str,
    limit: int,
    cursor: str | None,
    status: str | None = None,
) -> tuple[list[dict[str, Any]], str | None]:
    rows = read(patient_id, resource, limit, cursor, status)
    field = "created_at" if resource == "alerts" else "timestamp"
    next_cursor = encode(rows[limit - 1], field) if len(rows) > limit else None
    return (
        [label_alert(r) for r in rows[:limit]] if resource == "alerts" else rows[:limit]
    ), next_cursor


def acknowledge(patient_id: UUID, alert_id: UUID, key: str) -> dict[str, Any]:
    require_portal()
    idempotency.validate_key(key)
    # Reauthorize before replay; conflicting keys roll back the tentative transition.
    with transaction():
        result = call("enat_portal_acknowledge", patient_id, alert_id)
        if result is None:
            raise NotFound("Alert unavailable")
        return dict(
            idempotency.execute(
                current_user_id.get(),
                "portal:acknowledge",
                key,
                {"patient_id": str(patient_id), "alert_id": str(alert_id)},
                lambda: label_alert(result),
            )
        )
