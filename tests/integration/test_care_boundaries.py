from datetime import timedelta, timezone
from uuid import UUID, uuid4

import pytest
from psycopg.types.json import Jsonb

from app.core.clock import utc_now
from app.core.errors import InvalidMutation, NotFound
from app.db import data
from app.services import care_access, offline_checkin, portal
from tests.integration.test_care_offline_database import (  # noqa: F401
    care_db,
    connect,
    payload,
    submit,
)
from tests.integration.test_security_database import acting, db, pytestmark  # noqa: F401


def test_pagination_reauthorizes_and_filters_other_patients(care_db):
    _, patient, clinician = care_db
    other = data.resolve_identity("supabase", str(uuid4()), "unrelated@example.org")
    connection = connect(patient, clinician)
    a, b = submit(patient), submit(patient)
    unrelated = submit(other)
    with acting(clinician["id"]):
        for resource in ("patient", "check_ins", "summary", "appointment", "alerts"):
            with pytest.raises(NotFound):
                portal.read(UUID(other["id"]), resource)
        rows, cursor = portal.history(UUID(patient["id"]), "alerts", 1, None)
        assert cursor and len(rows) == 1
        rest, end = portal.history(UUID(patient["id"]), "alerts", 1, cursor)
        assert end is None
        assert {rows[0]["id"], rest[0]["id"]} == {a["alert_id"], b["alert_id"]}
        assert unrelated["alert_id"] not in str(rows + rest)
        with pytest.raises(InvalidMutation):
            portal.history(UUID(patient["id"]), "alerts", 50, "forged")
        with pytest.raises(NotFound):
            portal.acknowledge(
                UUID(patient["id"]), UUID(unrelated["alert_id"]), "wrong-patient-alert"
            )
    with acting(patient["id"]):
        care_access.revoke(UUID(connection["id"]))
    with acting(clinician["id"]), pytest.raises(NotFound):
        portal.history(UUID(patient["id"]), "alerts", 1, cursor)


def test_second_clinician_cannot_overwrite_acknowledgement(care_db):
    admin, patient, first = care_db
    second = data.resolve_identity("supabase", str(uuid4()), "second@example.org")
    admin.execute(
        "INSERT INTO clinician_profiles(user_id,display_name) VALUES(%s,'Second')",
        (second["id"],),
    )
    admin.commit()
    connect(patient, first)
    connect(patient, second)
    result = submit(patient)
    with acting(first["id"]):
        initial = portal.acknowledge(
            UUID(patient["id"]), UUID(result["alert_id"]), "first-ack"
        )
    with acting(second["id"]):
        assert (
            portal.acknowledge(
                UUID(patient["id"]), UUID(result["alert_id"]), "second-ack"
            )
            == initial
        )
    row = admin.execute(
        "SELECT acknowledged_by FROM emergency_alerts WHERE id=%s",
        (result["alert_id"],),
    ).fetchone()
    assert str(row["acknowledged_by"]) == first["id"]


@pytest.mark.parametrize("disabled_party", ["patient", "clinician"])
def test_disabled_account_loses_portal_access(care_db, disabled_party):
    admin, patient, clinician = care_db
    connect(patient, clinician)
    who = patient if disabled_party == "patient" else clinician
    admin.execute("UPDATE users SET disabled_at=now() WHERE id=%s", (who["id"],))
    admin.commit()
    with acting(clinician["id"]), pytest.raises(NotFound):
        portal.read(UUID(patient["id"]), "appointment")


def test_appointment_summary_and_history_are_allowlisted(care_db):
    admin, patient, clinician = care_db
    connect(patient, clinician)
    admin.execute(
        "INSERT INTO appointments(user_id,appointment_date) VALUES(%s,current_date+7)",
        (patient["id"],),
    )
    admin.execute(
        "INSERT INTO summaries(user_id,period_start,period_end,content_json,share_link_slug,qr_code_url) VALUES(%s,current_date,current_date,%s,'secret-bearer',NULL)",
        (patient["id"], Jsonb({"danger_signs": []})),
    )
    admin.commit()
    with acting(clinician["id"]):
        appointment = portal.read(UUID(patient["id"]), "appointment")
        assert set(appointment) == {
            "appointment_date",
            "hospital",
            "anc_contact_title",
            "anc_contact_title_am",
            "status",
            "version",
        }
        summary = portal.read(UUID(patient["id"]), "summary")
        assert "secret" not in str(summary)
    admin.execute(
        "UPDATE appointments SET status='completed' WHERE user_id=%s", (patient["id"],)
    )
    admin.commit()
    with acting(clinician["id"]):
        assert portal.read(UUID(patient["id"]), "appointment") is None


def test_future_clock_skew_and_equivalent_offsets(care_db):
    _, patient, _ = care_db
    with pytest.raises(InvalidMutation):
        submit(patient, payload(when=utc_now() + timedelta(hours=1)))
    value = payload(dangerous=False)
    result = submit(patient, value)
    assert not result["danger_sign_triggered"] and result["alert_id"] is None
    equivalent = value.model_dump(mode="json")
    zone = timezone(timedelta(hours=3))
    for field in ("recorded_at", "client_confirmed_at"):
        equivalent[field] = getattr(value, field).astimezone(zone).isoformat()
    with acting(patient["id"]):
        assert (
            offline_checkin.sync(
                UUID(patient["id"]),
                type(value).model_validate(equivalent),
                str(value.client_submission_id),
            )
            == result
        )
