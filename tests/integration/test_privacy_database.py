import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
from uuid import UUID, uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.core.errors import DataUnavailable, NotFound
from app.db import data, jobs, worker
from app.db.worker import worker_context
from app.main import create_app
from app.services import privacy, sharing
from tests.integration.test_patient_journey import identity
from tests.integration.test_security_database import acting, db, pytestmark  # noqa: F401


@pytest.fixture
def privacy_db(db, monkeypatch):
    config = get_settings().model_copy(
        update={
            "enable_privacy_tools": True,
            "privacy_policy_version": "synthetic-policy-1",
            "privacy_support_url": "https://support.invalid",
        }
    )
    monkeypatch.setattr(privacy, "get_settings", lambda: config)
    return db


def test_export_pages_cover_large_owned_history_and_audit_without_payloads(privacy_db):
    admin, a, b = privacy_db
    admin.execute(
        "INSERT INTO check_ins(user_id,summary_text_en) SELECT %s,'private synthetic text' FROM generate_series(1,1051)",
        (a["id"],),
    )
    admin.execute(
        "INSERT INTO check_ins(user_id,summary_text_en) VALUES(%s,'other patient')",
        (b["id"],),
    )
    admin.commit()
    seen, after = set(), None
    with acting(a["id"]):
        while True:
            page = privacy.export_page(a["id"], "check_ins", 100, after)
            assert len(page["records"]) <= 100
            for row in page["records"]:
                assert row["summary_text_en"] == "private synthetic text"
                assert row["id"] not in seen
                seen.add(row["id"])
            after = page["next_cursor"]
            if after is None:
                break
        assert len(seen) == 1051
        assert privacy.export_page(b["id"], "check_ins")["records"] == []
        audit = privacy.export_page(a["id"], "audit")["records"]
        assert len(audit) == 12
        assert all(row["event"] == "export_page" for row in audit)
        assert "private synthetic text" not in str(audit)
        # Reading audit pages must not grow the exported audit list.
        assert privacy.export_page(a["id"], "audit")["records"] == audit


def test_export_is_allowlisted_and_excludes_bearer_material(privacy_db):
    admin, a, _ = privacy_db
    summary = uuid4()
    admin.execute(
        "INSERT INTO summaries(id,user_id,period_start,period_end,content_json,share_link_slug,qr_code_url) VALUES(%s,%s,current_date,current_date,'{}','legacy-bearer','https://private.invalid/token')",
        (summary, a["id"]),
    )
    admin.execute(
        "INSERT INTO summary_shares(user_id,summary_id,token_hash,scope,expires_at) VALUES(%s,%s,'sensitive-hash','structured-v1',now()+interval '1 hour')",
        (a["id"], summary),
    )
    admin.commit()
    with acting(a["id"]):
        for section in privacy.SECTIONS:
            page = privacy.export_page(a["id"], section)
            assert "sensitive-hash" not in str(page)
            assert "legacy-bearer" not in str(page)
            assert "https://private.invalid/token" not in str(page)
        assert privacy.manifest()["policy_version"] == "synthetic-policy-1"


def test_requests_are_idempotent_cancelable_and_do_not_delete_patient_data(privacy_db):
    admin, a, b = privacy_db
    with acting(a["id"]):
        request = privacy.create_deletion_request(a["id"], "privacy-request-key")
        assert request["status"] == "requested"
        assert (
            privacy.create_deletion_request(a["id"], "privacy-request-key") == request
        )
        assert (
            privacy.create_deletion_request(a["id"], "another-request-key")["id"]
            == request["id"]
        )
    with acting(b["id"]):
        with pytest.raises(NotFound):
            privacy.cancel_request(b["id"], request["id"])
        assert privacy.export_page(b["id"], "requests")["records"] == []
    with acting(a["id"]):
        cancelled = privacy.cancel_request(a["id"], request["id"])
        assert cancelled["status"] == "cancelled"
        assert privacy.cancel_request(a["id"], request["id"]) == cancelled
        events = privacy.export_page(a["id"], "audit")["records"]
        assert sorted(row["event"] for row in events) == [
            "request_cancelled",
            "request_created",
        ]
    assert (
        admin.execute("SELECT count(*) FROM users WHERE id=%s", (a["id"],)).fetchone()[
            "count"
        ]
        == 1
    )


def test_concurrent_request_keys_create_only_one_pending_request(privacy_db):
    _, a, _ = privacy_db

    def submit(index):
        with acting(a["id"]):
            return privacy.create_deletion_request(a["id"], f"privacy-key-{index}")[
                "id"
            ]

    with ThreadPoolExecutor(max_workers=4) as pool:
        assert len(set(pool.map(submit, range(8)))) == 1


def test_audit_failure_rolls_back_privacy_request(privacy_db):
    admin, a, _ = privacy_db
    admin.execute(
        "CREATE FUNCTION reject_privacy_test() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'synthetic failure'; END $$"
    )
    admin.execute(
        "CREATE TRIGGER reject_privacy_test BEFORE INSERT ON privacy_events FOR EACH ROW EXECUTE FUNCTION reject_privacy_test()"
    )
    admin.commit()
    try:
        with acting(a["id"]), pytest.raises(DataUnavailable):
            privacy.create_deletion_request(a["id"], "failed-request-key")
        assert (
            admin.execute(
                "SELECT count(*) FROM privacy_requests WHERE user_id=%s", (a["id"],)
            ).fetchone()["count"]
            == 0
        )
    finally:
        admin.execute("DROP TRIGGER reject_privacy_test ON privacy_events")
        admin.execute("DROP FUNCTION reject_privacy_test()")
        admin.commit()


def test_grants_prevent_forgery_and_audit_rewriting(privacy_db):
    admin, a, _ = privacy_db
    with acting(a["id"]):
        request = privacy.create_deletion_request(a["id"], "private-audit-key")
        for statement in (
            "UPDATE privacy_events SET event='share_read'",
            "DELETE FROM privacy_events",
            "UPDATE privacy_requests SET status='cancelled'",
            "SELECT enat_privacy_queue()",
        ):
            with pytest.raises(DataUnavailable), data.transaction() as conn:
                conn.execute(statement)
    for role in ("anon", "authenticated", "service_role", "enat_worker"):
        assert not admin.execute(
            "SELECT has_table_privilege(%s,'privacy_requests','SELECT') AS allowed",
            (role,),
        ).fetchone()["allowed"]
    assert admin.execute(
        "SELECT has_table_privilege('enat_privacy_operator','privacy_requests','SELECT') AS allowed"
    ).fetchone()["allowed"]
    assert not admin.execute(
        "SELECT has_table_privilege('enat_privacy_operator','check_ins','SELECT') AS allowed"
    ).fetchone()["allowed"]
    admin.commit()
    with pytest.raises(psycopg.errors.CheckViolation):
        admin.execute(
            "DELETE FROM privacy_events WHERE resource_id=%s", (request["id"],)
        )
    admin.rollback()


def test_public_share_access_and_revocation_have_durable_audit(privacy_db):
    admin, a, _ = privacy_db
    summary = uuid4()
    admin.execute(
        "INSERT INTO summaries(id,user_id,period_start,period_end,content_json) VALUES(%s,%s,current_date,current_date,'{}')",
        (summary, a["id"]),
    )
    admin.commit()
    with acting(a["id"]):
        share = sharing.create_share(
            UUID(a["id"]), summary, sharing.ShareRequest(consent=True)
        )
    token = share["share_url"].rsplit("/", 1)[-1]
    with acting(None):
        assert sharing.read_share(token)
    with acting(a["id"]):
        sharing.revoke_share(a["id"], share["id"])
        sharing.revoke_share(a["id"], share["id"])
    with acting(None):
        assert sharing.read_share(token) is None
    with acting(a["id"]):
        events = privacy.export_page(a["id"], "audit")["records"]
        assert sorted(row["event"] for row in events) == [
            "share_created",
            "share_read",
            "share_revoked",
        ]
        assert token not in str(events) and hashlib.sha256(
            token.encode()
        ).hexdigest() not in str(events)


def test_http_privacy_workflow_and_no_store(privacy_db, monkeypatch):
    _, a, _ = privacy_db
    headers = identity(monkeypatch, a)
    client = TestClient(create_app())
    response = client.get("/users/me/privacy/export", headers=headers)
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert "check_ins" in response.json()["sections"]
    response = client.post(
        "/users/me/privacy/requests",
        headers={**headers, "Idempotency-Key": "http-privacy-key"},
        json={"confirm": True},
    )
    assert response.status_code == 202
    assert "user_id" not in response.json()
    assert (
        client.post(
            f"/users/me/privacy/requests/{response.json()['id']}/cancel",
            headers=headers,
        ).json()["status"]
        == "cancelled"
    )


def test_worker_queue_metrics_are_aggregate_only(privacy_db, monkeypatch):
    admin, a, _ = privacy_db
    config = get_settings().model_copy(
        update={"worker_database_url": os.environ["ENAT_TEST_WORKER_DSN"]}
    )
    monkeypatch.setattr(worker, "get_settings", lambda: config)
    worker.get_pool.cache_clear()
    with acting(a["id"]):
        privacy.create_deletion_request(a["id"], "queue-metric-request")
    try:
        with worker_context():
            stats = jobs.stats()["privacy_queue"]
            assert set(stats) == {"pending", "oldest_seconds"}
            assert stats["pending"] >= 1
            with pytest.raises(DataUnavailable), data.transaction() as conn:
                conn.execute("SELECT * FROM privacy_requests")
    finally:
        worker.close_pool()
