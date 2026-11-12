import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from uuid import uuid4

import psycopg
import pytest
from psycopg.rows import dict_row

from app.config import get_settings
from app.core import limits
from app.core.errors import Conflict, DataUnavailable, RateLimited
from app.db import data
from app.services import sharing

pytestmark = [
    pytest.mark.enable_socket,
    pytest.mark.skipif(
        not os.environ.get("ENAT_TEST_ADMIN_DSN"),
        reason="Run scripts/test_database.py for isolated database tests",
    ),
]


@pytest.fixture
def db(monkeypatch):
    settings = get_settings().model_copy(
        update={
            "database_url": os.environ["ENAT_TEST_APP_DSN"],
            "enable_request_limits": True,
            "enable_summary_sharing": True,
        }
    )
    monkeypatch.setattr(data, "get_settings", lambda: settings)
    monkeypatch.setattr(sharing, "get_settings", lambda: settings)
    monkeypatch.setattr(limits, "get_settings", lambda: settings)
    data.get_pool.cache_clear()
    with psycopg.connect(
        os.environ["ENAT_TEST_ADMIN_DSN"], row_factory=dict_row
    ) as admin:
        a = data.resolve_identity("supabase", str(uuid4()), "a@example.org")
        b = data.resolve_identity("supabase", str(uuid4()), "b@example.org")
        yield admin, a, b
    if data.get_pool.cache_info().currsize:
        data.get_pool().close()
    data.get_pool.cache_clear()


def acting(uid):
    from contextlib import contextmanager

    @contextmanager
    def context():
        token = data.current_user_id.set(str(uid) if uid else None)
        try:
            yield
        finally:
            data.current_user_id.reset(token)

    return context()


def add_rows(admin, a, b, table):
    values = {
        "supplements": "name",
        "appointments": "appointment_date",
        "check_ins": None,
        "check_in_sessions": "current_stage,stage_order,expires_at",
        "reminders": "type,message,due_at",
        "push_tokens": "token,platform",
        "summaries": "period_start,period_end,content_json",
    }
    for user in (a, b):
        extra = {
            "supplements": "'iron'",
            "appointments": "current_date",
            "check_ins": "",
            "check_in_sessions": "'symptoms','[\"symptoms\"]',now()+interval '1 hour'",
            "reminders": "'test','message',now()",
            "push_tokens": f"'{uuid4()}','web'",
            "summaries": "current_date,current_date,'{}'",
        }[table]
        admin.execute(
            f"INSERT INTO {table}(user_id{',' + values[table] if values[table] else ''}) VALUES(%s{',' + extra if extra else ''})",
            (user["id"],),
        )
    admin.commit()


@pytest.mark.parametrize(
    "table",
    [
        "supplements",
        "appointments",
        "check_ins",
        "check_in_sessions",
        "reminders",
        "push_tokens",
        "summaries",
    ],
)
def test_rls_blocks_unfiltered_cross_user_reads_and_writes(db, table):
    admin, a, b = db
    add_rows(admin, a, b, table)
    with acting(a["id"]):
        rows = data.get_data_client().table(table).select().execute().data
        assert rows and all(row["user_id"] == a["id"] for row in rows)
        assert (
            data.get_data_client()
            .table(table)
            .select()
            .eq("user_id", b["id"])
            .execute()
            .data
            == []
        )
        if table != "summaries":
            with pytest.raises(DataUnavailable):
                data.get_data_client().table(table).update({"user_id": b["id"]}).eq(
                    "user_id", a["id"]
                ).execute()
    with acting(None):
        assert data.get_data_client().table(table).select().execute().data == []


def test_identity_mapping_preserves_ids_created_at_and_disabled_state(db):
    admin, a, b = db
    again = data.resolve_identity("supabase", a["id"], "a@example.org")
    assert again["id"] == a["id"] and again["created_at"] == a["created_at"]
    admin.execute("UPDATE users SET disabled_at=now() WHERE id=%s", (a["id"],))
    admin.commit()
    assert data.resolve_identity("supabase", a["id"], "a@example.org") is None
    with acting(a["id"]):
        assert data.get_data_client().table("users").select().execute().data == []


def test_client_roles_have_no_patient_or_privileged_function_access(db):
    admin, _, _ = db
    for role in ("anon", "authenticated", "service_role"):
        for table in (
            "users",
            "summaries",
            "check_ins",
            "summary_shares",
            "user_identities",
            "push_tokens",
            "stage_audio_prompts",
        ):
            assert not admin.execute(
                "SELECT has_table_privilege(%s,%s,'SELECT') AS allowed", (role, table)
            ).fetchone()["allowed"]
        assert not admin.execute(
            "SELECT has_function_privilege(%s,'enat_read_share(text)','EXECUTE') AS allowed",
            (role,),
        ).fetchone()["allowed"]
    assert not admin.execute(
        "SELECT has_table_privilege('enat_worker','check_ins','UPDATE') AS allowed"
    ).fetchone()["allowed"]
    assert admin.execute(
        "SELECT has_table_privilege('enat_worker','reminders','INSERT') AS allowed"
    ).fetchone()["allowed"]
    with acting(None):
        with data.transaction() as conn:
            role = conn.execute(
                "SELECT current_user AS name,rolbypassrls FROM pg_roles WHERE rolname=current_user"
            ).fetchone()
            assert role == {"name": "enat_app", "rolbypassrls": False}


def test_linking_never_merges_an_existing_other_account(db):
    _, a, b = db
    with acting(a["id"]):
        with data.transaction() as conn:
            assert not conn.execute(
                "SELECT enat_link_identity('supabase',%s) AS ok", (b["id"],)
            ).fetchone()["ok"]
            assert conn.execute(
                "SELECT enat_link_identity('telegram',%s) AS ok", (str(uuid4()),)
            ).fetchone()["ok"]


def test_concurrent_telegram_exchange_has_one_winner_and_revocation(db):
    _, _, _ = db
    subject = str(uuid4())
    source = uuid4().hex

    def exchange(_):
        token = uuid4().hex
        with data.transaction() as conn:
            result = conn.execute(
                "SELECT enat_telegram_session(%s,NULL,NULL,%s,%s,now()+interval '10 minutes') AS value",
                (subject, token, source),
            ).fetchone()["value"]
        return token, result

    with ThreadPoolExecutor(max_workers=4) as workers:
        results = list(workers.map(exchange, range(4)))
    winners = [(t, u) for t, u in results if u]
    assert len(winners) == 1
    token, user = winners[0]
    with data.transaction() as conn:
        assert (
            conn.execute("SELECT enat_get_session(%s) AS value", (token,)).fetchone()[
                "value"
            ]["id"]
            == user["id"]
        )
        conn.execute("SELECT enat_revoke_session(%s)", (token,))
        assert (
            conn.execute("SELECT enat_get_session(%s) AS value", (token,)).fetchone()[
                "value"
            ]
            is None
        )


def test_shares_require_owner_expire_revoke_and_remove_text(db):
    admin, a, b = db
    with acting(a["id"]):
        summary = (
            data.get_data_client()
            .table("summaries")
            .insert(
                {
                    "user_id": a["id"],
                    "period_start": "2026-10-01",
                    "period_end": "2026-10-13",
                    "content_json": {
                        "raw_text": "PRIVATE",
                        "danger_signs": [
                            {
                                "category": "high_fever",
                                "date": "2026-10-13",
                                "raw_text": "PRIVATE",
                            }
                        ],
                    },
                }
            )
            .execute()
            .data[0]
        )
        shared = sharing.create_share(
            a["id"], summary["id"], sharing.ShareRequest(consent=True)
        )
    token = shared["share_url"].rsplit("/", 1)[1]
    assert "PRIVATE" not in str(sharing.read_share(token))
    row = admin.execute(
        "SELECT * FROM summary_shares WHERE id=%s", (shared["id"],)
    ).fetchone()
    assert row["token_hash"] == hashlib.sha256(token.encode()).hexdigest()
    assert token not in str(row)
    with acting(b["id"]):
        from app.core.errors import NotFound

        with pytest.raises(NotFound):
            sharing.create_share(
                b["id"], summary["id"], sharing.ShareRequest(consent=True)
            )
        with pytest.raises(NotFound):
            sharing.revoke_share(b["id"], shared["id"])
    with acting(a["id"]):
        sharing.revoke_share(a["id"], shared["id"])
    assert sharing.read_share(token) is None
    with acting(a["id"]):
        expiring = sharing.create_share(
            a["id"], summary["id"], sharing.ShareRequest(consent=True)
        )
    admin.execute(
        "UPDATE summary_shares SET created_at=now()-interval '2 days',expires_at=now()-interval '1 day' WHERE id=%s",
        (expiring["id"],),
    )
    admin.commit()
    assert sharing.read_share(expiring["share_url"].rsplit("/", 1)[1]) is None


def test_limits_are_atomic_across_connections(db):
    key = uuid4().hex

    def consume(_):
        try:
            limits.take_rate(key, "test", 3)
            return True
        except RateLimited:
            return False

    with ThreadPoolExecutor(max_workers=8) as workers:
        assert sum(workers.map(consume, range(8))) == 3


def test_provider_leases_bound_concurrency_and_recover_expired(db):
    admin, _, _ = db
    with data.transaction() as conn:
        first = conn.execute("SELECT enat_acquire_provider(1) AS lease").fetchone()[
            "lease"
        ]
        assert first
        assert (
            conn.execute("SELECT enat_acquire_provider(1) AS lease").fetchone()["lease"]
            is None
        )
    admin.execute("UPDATE provider_leases SET expires_at=now()-interval '1 second'")
    admin.commit()
    with data.transaction() as conn:
        second = conn.execute("SELECT enat_acquire_provider(1) AS lease").fetchone()[
            "lease"
        ]
        assert second != first
        conn.execute("SELECT enat_release_provider(%s)", (second,))


def test_pool_does_not_reuse_previous_request_identity(db):
    _, a, b = db
    with acting(a["id"]):
        assert (
            data.get_data_client().table("users").select().execute().data[0]["id"]
            == a["id"]
        )
    with acting(b["id"]):
        rows = data.get_data_client().table("users").select().execute().data
        assert len(rows) == 1 and rows[0]["id"] == b["id"]
    with acting(None):
        assert data.get_data_client().table("users").select().execute().data == []


@pytest.mark.skipif(
    os.environ.get("ENAT_TEST_HAS_LEGACY") != "1", reason="Upgrade-only fixture"
)
def test_upgrade_preserves_legacy_identity_but_invalidates_public_credentials(db):
    admin, _, _ = db
    user = data.resolve_identity(
        "supabase", "00000000-0000-4000-8000-000000000001", "legacy@example.org"
    )
    assert user["created_at"].startswith("2020-01-01")
    row = admin.execute(
        "SELECT share_link_slug,qr_code_url FROM summaries WHERE id='00000000-0000-4000-8000-000000000002'"
    ).fetchone()
    assert row == {"share_link_slug": None, "qr_code_url": None}
    assert not admin.execute(
        "SELECT public FROM storage.buckets WHERE id='summary-qr-codes'"
    ).fetchone()["public"]
    with admin.transaction():
        admin.execute("SET LOCAL ROLE anon")
        rows = admin.execute("SELECT bucket_id FROM storage.objects").fetchall()
        assert rows == [{"bucket_id": "audio-prompts"}]


def test_password_reset_and_logout_invalidate_old_sessions(db):
    _, a, _ = db
    sid = uuid4()
    with data.transaction() as conn:
        assert not conn.execute(
            "SELECT enat_auth_revoked(%s,%s,%s) AS value", (sid, a["id"], 1)
        ).fetchone()["value"]
        conn.execute("SELECT enat_revoke_user_auth(%s)", (a["id"],))
        assert conn.execute(
            "SELECT enat_auth_revoked(%s,%s,%s) AS value", (sid, a["id"], 1)
        ).fetchone()["value"]
        future = datetime.now(timezone.utc).timestamp() + 60
        assert not conn.execute(
            "SELECT enat_auth_revoked(%s,%s,%s) AS value", (sid, a["id"], future)
        ).fetchone()["value"]
        conn.execute("SELECT enat_revoke_auth(%s,now()+interval '1 day')", (sid,))
        assert conn.execute(
            "SELECT enat_auth_revoked(%s,%s,%s) AS value", (sid, a["id"], future)
        ).fetchone()["value"]


def test_token_cannot_transfer_between_users(db):
    _, a, b = db
    from app.db.repositories.push_tokens import PushTokenRepository

    token = uuid4().hex
    with acting(a["id"]):
        PushTokenRepository().register(a["id"], token)
    with acting(b["id"]):
        with pytest.raises((DataUnavailable, Conflict)):
            PushTokenRepository().register(b["id"], token)
    with acting(a["id"]):
        assert PushTokenRepository().list_for_user(a["id"])[0]["token"] == token


def test_http_identity_context_isolated_across_requests_and_logout(db, monkeypatch):
    admin, a, b = db
    add_rows(admin, a, b, "check_ins")
    from fastapi.testclient import TestClient

    import app.api.routes.auth as auth
    import app.dependencies as dependencies
    from app.main import app

    sessions = {"token-a": str(uuid4()), "token-b": str(uuid4())}

    def decode(token):
        user = a if token == "token-a" else b
        return {
            "sub": user["id"],
            "email": user["email"],
            "session_id": sessions[token],
            "iat": datetime.now(timezone.utc).timestamp(),
        }

    monkeypatch.setattr(dependencies, "decode_access_token", decode)
    monkeypatch.setattr(auth, "decode_access_token", decode)
    monkeypatch.setattr(auth, "auth_request", lambda *args, **kwargs: {})
    client = TestClient(app)

    def read(token):
        response = client.get(
            "/checkin/history", headers={"Authorization": "Bearer " + token}
        )
        assert response.status_code == 200
        return response.json()[0]["id"]

    with ThreadPoolExecutor(max_workers=2) as workers:
        ids = list(workers.map(read, ["token-a", "token-b"]))
    assert ids[0] != ids[1]
    assert (
        client.get(
            "/checkin/history/" + ids[0], headers={"Authorization": "Bearer token-b"}
        ).status_code
        == 404
    )
    assert (
        client.post(
            "/auth/logout", headers={"Authorization": "Bearer token-a"}
        ).status_code
        == 204
    )
    assert (
        client.get(
            "/checkin/history", headers={"Authorization": "Bearer token-a"}
        ).status_code
        == 401
    )
    assert (
        client.get(
            "/checkin/history", headers={"Authorization": "Bearer token-b"}
        ).status_code
        == 200
    )


def test_repository_round_trip_preserves_time_and_json_types(db):
    _, a, _ = db
    from app.db.repositories.check_in_sessions import CheckInSessionRepository
    from app.db.repositories.supplements import SupplementRepository

    with acting(a["id"]):
        supplement = SupplementRepository().create(
            a["id"], {"name": "iron", "reminder_time": "09:30:00"}
        )
        assert supplement["reminder_time"] == "09:30:00"
        session = CheckInSessionRepository().create(
            a["id"],
            {
                "current_stage": "symptoms",
                "stage_order": ["symptoms"],
                "draft_data": {"symptoms": []},
            },
        )
        loaded = CheckInSessionRepository().get(session["id"], a["id"])
        assert loaded["draft_data"] == {"symptoms": []}
