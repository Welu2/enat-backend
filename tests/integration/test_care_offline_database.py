"""Care authorization and durable offline ingestion with actual restricted roles."""

from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.core.clock import utc_now
from app.core.errors import Conflict, DataUnavailable, InvalidMutation, NotFound
from app.db import data
from app.db.repositories.check_ins import CheckInRepository
from app.main import create_app
from app.models.care import CareInviteRequest
from app.models.offline_checkin import OfflineCheckInRequest
from app.services import care_access, offline_checkin, portal, privacy
from app.services.clinical_policy import normalize_item
from app.services.summary import SummaryService
from tests.integration.test_patient_journey import identity
from tests.integration.test_security_database import acting, db, pytestmark  # noqa: F401


@pytest.fixture
def care_db(db, monkeypatch):
    config = get_settings().model_copy(
        update={
            "enable_care_portal": True,
            "enable_offline_checkins": True,
            "enable_privacy_tools": True,
            "privacy_policy_version": "test-v1",
            "privacy_support_url": "https://support.invalid",
        }
    )
    for module in (care_access, offline_checkin, privacy):
        monkeypatch.setattr(module, "get_settings", lambda: config)
    admin, patient, clinician = db
    admin.execute(
        "INSERT INTO clinician_profiles(user_id,display_name) VALUES(%s,'Synthetic clinician')",
        (clinician["id"],),
    )
    admin.commit()
    return db


def connect(patient, recipient, relationship="clinician"):
    with acting(patient["id"]):
        invite = care_access.invite(
            CareInviteRequest(
                recipient_id=recipient["id"], relationship=relationship, consent=True
            )
        )
    with acting(recipient["id"]):
        assert care_access.accept(invite["token"])["status"] == "active"
    return invite


def payload(*, identifier=None, when=None, dangerous=True):
    when = when or utc_now() - timedelta(minutes=1)
    return OfflineCheckInRequest(
        schema_version=1,
        client_submission_id=identifier or uuid4(),
        recorded_at=when,
        client_confirmed_at=when,
        confirmed=True,
        symptoms=[
            {
                "raw_text": "synthetic private report",
                "category": "high_fever" if dangerous else None,
            }
        ],
        food_log=[],
        supplement_check=[],
        closing_mentions=[],
    )


def submit(patient, value=None):
    value = value or payload()
    with acting(patient["id"]):
        return offline_checkin.sync(
            UUID(patient["id"]), value, str(value.client_submission_id)
        )


def test_invite_accept_revoke_and_no_token_disclosure(care_db):
    admin, patient, clinician = care_db
    with acting(patient["id"]):
        invitation = care_access.invite(
            CareInviteRequest(
                recipient_id=clinician["id"], relationship="clinician", consent=True
            )
        )
        assert "token" not in str(care_access.connections(50, None)[0])
        assert invitation["recipient_display_name"] == "Synthetic clinician"
        with pytest.raises(NotFound):
            care_access.accept(invitation["token"])
        with pytest.raises(Conflict):
            care_access.invite(
                CareInviteRequest(
                    recipient_id=clinician["id"], relationship="clinician", consent=True
                )
            )

    def accept(_):
        with acting(clinician["id"]):
            return care_access.accept(invitation["token"])

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(accept, range(4)))
    assert all(r == results[0] for r in results)
    with acting(clinician["id"]):
        assert portal.patients(50, None)[0][0]["id"] == patient["id"]
        assert portal.read(UUID(patient["id"]), "patient")["pregnancy_as_of"] is None
    with acting(patient["id"]):
        care_access.revoke(UUID(invitation["id"]))
        care_access.revoke(UUID(invitation["id"]))
    with acting(clinician["id"]):
        with pytest.raises(NotFound):
            portal.read(UUID(patient["id"]), "patient")
        with pytest.raises(NotFound):
            care_access.accept(invitation["token"])
    events = admin.execute(
        "SELECT * FROM care_access_events WHERE patient_id=%s", (patient["id"],)
    ).fetchall()
    assert [r["action"] for r in events].count("accepted") == 1
    assert [r["action"] for r in events].count("revoked") == 1
    assert invitation["token"] not in str(events)
    assert care_access.token_hash(invitation["token"]) not in str(events)


def test_trusted_person_projection_and_activation_boundary(care_db):
    _, patient, trusted = care_db
    old = submit(patient)
    connect(patient, trusted, "trusted_person")
    new = submit(patient)
    with acting(trusted["id"]):
        for resource in ("patient", "check_ins", "summary"):
            with pytest.raises(NotFound):
                portal.read(UUID(patient["id"]), resource)
        rows, _ = portal.history(UUID(patient["id"]), "alerts", 50, None)
        assert [row["id"] for row in rows] == [new["alert_id"]]
        assert old["alert_id"] not in str(rows)
        assert "synthetic private report" not in str(rows)
        assert "acknowledged_by" not in rows[0]
        assert rows[0]["category_labels"][0]["en"]
        with pytest.raises(NotFound):
            portal.acknowledge(
                UUID(patient["id"]), UUID(new["alert_id"]), "trusted-attempt"
            )
        assert portal.read(UUID(patient["id"]), "appointment") is None


def test_permissions_functions_and_clinician_deactivation(care_db):
    admin, patient, clinician = care_db
    connect(patient, clinician)
    record = submit(patient)
    with acting(clinician["id"]):
        with data.transaction() as conn:
            assert (
                conn.execute(
                    "SELECT * FROM check_ins WHERE user_id=%s", (patient["id"],)
                ).fetchall()
                == []
            )
            assert (
                conn.execute(
                    "SELECT * FROM emergency_alerts WHERE patient_id=%s",
                    (patient["id"],),
                ).fetchall()
                == []
            )
        for statement in (
            "UPDATE clinician_profiles SET active=true",
            "DELETE FROM care_access_events",
            "UPDATE care_connections SET status='active'",
            "SELECT _enat_care_connection('" + patient["id"] + "')",
        ):
            with pytest.raises(DataUnavailable), data.transaction() as conn:
                conn.execute(statement)
        assert (
            portal.read(UUID(patient["id"]), "check_ins")[0]["id"]
            == record["check_in_id"]
        )
    functions = admin.execute(
        "SELECT oid::regprocedure::text AS name FROM pg_proc WHERE pronamespace='public'::regnamespace AND (proname LIKE 'enat_care_%' OR proname LIKE 'enat_portal_%' OR proname LIKE '\\_enat\\_care\\_%' OR proname LIKE '\\_enat\\_portal\\_%')"
    ).fetchall()
    assert functions
    for role in ("anon", "authenticated", "service_role", "enat_worker"):
        for f in functions:
            assert not admin.execute(
                "SELECT has_function_privilege(%s,%s,'EXECUTE') AS allowed",
                (role, f["name"]),
            ).fetchone()["allowed"]
    admin.execute(
        "UPDATE clinician_profiles SET active=false WHERE user_id=%s",
        (clinician["id"],),
    )
    admin.commit()
    with acting(clinician["id"]):
        assert portal.patients(50, None)[0] == []
        with pytest.raises(NotFound):
            portal.read(UUID(patient["id"]), "patient")


def test_expiry_self_invite_and_concurrent_trusted_slot(care_db):
    admin, patient, recipient = care_db
    with acting(patient["id"]), pytest.raises(NotFound):
        care_access.invite(
            CareInviteRequest(
                recipient_id=patient["id"], relationship="trusted_person", consent=True
            )
        )

    def invite(_):
        with acting(patient["id"]):
            try:
                return care_access.invite(
                    CareInviteRequest(
                        recipient_id=recipient["id"],
                        relationship="trusted_person",
                        consent=True,
                    )
                )
            except Conflict:
                return None

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = [r for r in pool.map(invite, range(4)) if r]
    assert len(results) == 1
    invitation = results[0]
    admin.execute(
        "UPDATE care_connections SET created_at=now()-interval '3 days',expires_at=now()-interval '1 day' WHERE id=%s",
        (invitation["id"],),
    )
    admin.commit()
    with acting(recipient["id"]), pytest.raises(NotFound):
        care_access.accept(invitation["token"])
    assert invite(0)


def test_offline_concurrent_retry_conflict_and_permanent_dedup(care_db):
    admin, patient, _ = care_db
    value = payload()
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _: submit(patient, value), range(8)))
    assert all(result == results[0] for result in results)
    for table, owner in (
        ("check_ins", "user_id"),
        ("emergency_alerts", "patient_id"),
        ("domain_outbox", "user_id"),
    ):
        assert (
            admin.execute(
                f"SELECT count(*) AS n FROM {table} WHERE {owner}=%s", (patient["id"],)
            ).fetchone()["n"]
            == 1
        )
    admin.execute("DELETE FROM mutation_results WHERE user_id=%s", (patient["id"],))
    admin.commit()
    assert submit(patient, value) == results[0]
    with pytest.raises(Conflict):
        submit(
            patient,
            payload(
                identifier=value.client_submission_id,
                when=value.recorded_at,
                dangerous=False,
            ),
        )
    with acting(patient["id"]), pytest.raises(InvalidMutation):
        offline_checkin.sync(UUID(patient["id"]), value, str(uuid4()))


def test_acknowledgement_conflicts_and_revoked_replays(care_db):
    admin, patient, clinician = care_db
    invitation = connect(patient, clinician)
    record, other = submit(patient), submit(patient)

    def acknowledge(_):
        with acting(clinician["id"]):
            return portal.acknowledge(
                UUID(patient["id"]), UUID(record["alert_id"]), "ack-same-key"
            )

    with ThreadPoolExecutor(max_workers=4) as pool:
        responses = list(pool.map(acknowledge, range(4)))
    assert all(r == responses[0] for r in responses)
    with acting(clinician["id"]), pytest.raises(Conflict):
        portal.acknowledge(UUID(patient["id"]), UUID(other["alert_id"]), "ack-same-key")
    assert (
        admin.execute(
            "SELECT status FROM emergency_alerts WHERE id=%s", (other["alert_id"],)
        ).fetchone()["status"]
        == "unacknowledged"
    )
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM care_access_events WHERE patient_id=%s AND action='acknowledged'",
            (patient["id"],),
        ).fetchone()["n"]
        == 1
    )
    with acting(patient["id"]):
        care_access.revoke(UUID(invitation["id"]))
    with acting(clinician["id"]), pytest.raises(NotFound):
        portal.acknowledge(
            UUID(patient["id"]), UUID(record["alert_id"]), "ack-same-key"
        )


@pytest.mark.parametrize("table", ["emergency_alerts", "domain_outbox"])
def test_failed_offline_write_is_atomic(care_db, table):
    admin, patient, _ = care_db
    admin.execute(
        "CREATE FUNCTION reject_mvp_test() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'synthetic failure'; END $$"
    )
    admin.execute(
        f"CREATE TRIGGER reject_mvp_test BEFORE INSERT ON {table} FOR EACH ROW EXECUTE FUNCTION reject_mvp_test()"
    )
    admin.commit()
    try:
        with pytest.raises(DataUnavailable):
            submit(patient)
        for name, owner in (
            ("check_ins", "user_id"),
            ("emergency_alerts", "patient_id"),
            ("mutation_results", "user_id"),
        ):
            assert (
                admin.execute(
                    f"SELECT count(*) AS n FROM {name} WHERE {owner}=%s",
                    (patient["id"],),
                ).fetchone()["n"]
                == 0
            )
    finally:
        admin.execute(f"DROP TRIGGER reject_mvp_test ON {table}")
        admin.execute("DROP FUNCTION reject_mvp_test()")
        admin.commit()


def test_audit_failure_prevents_read_and_revocation(care_db):
    admin, patient, clinician = care_db
    invitation = connect(patient, clinician)
    admin.execute(
        "CREATE FUNCTION reject_care_audit() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'synthetic failure'; END $$"
    )
    admin.execute(
        "CREATE TRIGGER reject_care_audit BEFORE INSERT ON care_access_events FOR EACH ROW EXECUTE FUNCTION reject_care_audit()"
    )
    admin.commit()
    try:
        with acting(clinician["id"]), pytest.raises(DataUnavailable):
            portal.read(UUID(patient["id"]), "patient")
        with acting(patient["id"]), pytest.raises(DataUnavailable):
            care_access.revoke(UUID(invitation["id"]))
        assert (
            admin.execute(
                "SELECT status FROM care_connections WHERE id=%s", (invitation["id"],)
            ).fetchone()["status"]
            == "active"
        )
    finally:
        admin.execute("DROP TRIGGER reject_care_audit ON care_access_events")
        admin.execute("DROP FUNCTION reject_care_audit()")
        admin.commit()


def test_late_observations_daily_checks_summary_and_exports(care_db):
    _, patient, _ = care_db
    now = utc_now()
    body = payload(when=now - timedelta(days=4)).model_dump()
    body["food_log"] = [{"raw_text": "synthetic meal", "food_groups": ["grains"]}]
    body["supplement_check"] = [
        {"raw_text": "taken", "supplement_name": "iron", "taken_today": True}
    ]
    result = submit(patient, OfflineCheckInRequest.model_validate(body))
    with acting(patient["id"]):
        repo = CheckInRepository()
        assert not repo.has_food_logged_today(UUID(patient["id"]))
        row = repo.get_by_id(UUID(patient["id"]), UUID(result["check_in_id"]))
        report = SummaryService._aggregate(
            [row],
            period_start=now - timedelta(days=1),
            period_end=utc_now() + timedelta(seconds=1),
        )
        assert report["food_logs"] == [] and report["supplement_adherence"] is None
        assert report["late_observations"][0]["check_in_id"] == result["check_in_id"]
        for section in (
            "check_ins",
            "care_connections",
            "emergency_alerts",
            "care_audit",
        ):
            exported = privacy.export_page(patient["id"], section)
            assert "submission_hash" not in str(
                exported
            ) and "invite_token_hash" not in str(exported)


def test_http_portal_offline_limits_and_disabled_revocation(care_db, monkeypatch):
    _, patient, clinician = care_db
    invitation = connect(patient, clinician)
    client = TestClient(create_app())
    headers = identity(monkeypatch, patient)
    value = payload()
    response = client.post(
        "/checkin/offline-sync",
        json=value.model_dump(mode="json"),
        headers={**headers, "Idempotency-Key": str(value.client_submission_id)},
    )
    assert response.status_code == 200, response.text
    assert response.headers["cache-control"] == "no-store"
    assert (
        client.post(
            "/checkin/offline-sync",
            content=b"x" * 65537,
            headers={**headers, "Content-Type": "multipart/form-data"},
        ).status_code
        == 413
    )
    headers = identity(monkeypatch, clinician)
    for path in (
        "/portal/me",
        "/portal/patients",
        f"/portal/patients/{patient['id']}",
        f"/portal/patients/{patient['id']}/alerts",
        f"/portal/patients/{patient['id']}/check-ins",
    ):
        response = client.get(path, headers=headers)
        assert response.status_code == 200, response.text
        assert response.headers["cache-control"] == "no-store"
    disabled = get_settings().model_copy(
        update={"enable_care_portal": False, "enable_offline_checkins": False}
    )
    monkeypatch.setattr(care_access, "get_settings", lambda: disabled)
    monkeypatch.setattr(offline_checkin, "get_settings", lambda: disabled)
    assert client.get("/portal/me", headers=headers).status_code == 503
    headers = identity(monkeypatch, patient)
    assert (
        client.delete(
            f"/users/me/care-connections/{invitation['id']}", headers=headers
        ).status_code
        == 204
    )


def test_online_finalization_creates_alert_and_ignores_caller_flag(care_db):
    admin, patient, _ = care_db
    with acting(patient["id"]):
        row = CheckInRepository().create(
            UUID(patient["id"]),
            {
                "symptoms": [
                    normalize_item(
                        "symptoms",
                        {"raw_text": "synthetic", "category": "high_fever"},
                        confirm=True,
                    )
                ],
                "danger_sign_triggered": False,
            },
        )
    assert row["danger_sign_triggered"] is True
    assert row["recorded_at"] == row["received_at"] == row["timestamp"]
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM emergency_alerts WHERE check_in_id=%s",
            (row["id"],),
        ).fetchone()["n"]
        == 1
    )
