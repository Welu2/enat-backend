from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from app.config import get_settings
from app.core.clock import utc_now
from app.core.errors import Conflict, FeatureUnavailable, InvalidMutation
from app.db import idempotency
from app.db.data import normalize, transaction
from app.db.repositories.check_ins import CheckInRepository
from app.models.clinical import STAGE_KEYS
from app.models.offline_checkin import OfflineCheckInRequest
from app.services.clinical_policy import normalize_item


def sync(
    user_id: UUID,
    payload: OfflineCheckInRequest,
    key: str,
    clock: Callable[[], datetime] = utc_now,
) -> dict[str, Any]:
    if not get_settings().enable_offline_checkins:
        raise FeatureUnavailable(
            "Offline ingestion is disabled; retain pending submissions"
        )
    if key != str(payload.client_submission_id):
        raise InvalidMutation("Retry key must equal submission ID")
    body = payload.model_dump(mode="json")
    digest = idempotency.request_hash(body)

    def action() -> dict[str, Any]:
        with transaction() as conn:
            conn.execute(
                "SELECT pg_advisory_xact_lock(hashtextextended(%s,0))",
                (f"offline:{user_id}:{key}",),
            )
            record = conn.execute(
                "SELECT * FROM check_ins WHERE user_id=%s AND client_submission_id=%s",
                (user_id, payload.client_submission_id),
            ).fetchone()
            if record:
                if record["submission_hash"] != digest:
                    raise Conflict("Submission ID reused with changed input")
            else:
                now = clock()
                if payload.client_confirmed_at > now + timedelta(minutes=5):
                    raise InvalidMutation("Device timestamp is in the future")
                draft = {
                    field: [
                        normalize_item(
                            stage, item, source="offline_form", now=now, confirm=True
                        )
                        for item in body[field]
                    ]
                    for stage, field in STAGE_KEYS.items()
                }
                record = CheckInRepository(lambda: now).create(
                    user_id,
                    {
                        **draft,
                        "recorded_at": payload.recorded_at.isoformat(),
                        "client_confirmed_at": payload.client_confirmed_at.isoformat(),
                        "capture_source": "offline_form",
                        "client_submission_id": key,
                        "submission_hash": digest,
                    },
                )
                idempotency.emit(user_id, "checkin.completed", record["id"])
            alert = conn.execute(
                "SELECT id FROM emergency_alerts WHERE check_in_id=%s", (record["id"],)
            ).fetchone()
            return dict(
                normalize(
                    {
                        "client_submission_id": record["client_submission_id"],
                        "check_in_id": record["id"],
                        "status": "synced",
                        "recorded_at": record["recorded_at"],
                        "received_at": record["received_at"],
                        "danger_sign_triggered": record["danger_sign_triggered"],
                        "alert_id": alert["id"] if alert else None,
                    }
                )
            )

    return dict(idempotency.execute(user_id, "offline:sync", key, body, action))
