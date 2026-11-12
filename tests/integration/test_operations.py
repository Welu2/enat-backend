import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg.rows import dict_row

from app.core.errors import InvalidMutation
from app.core.readiness import SCHEMA_COUNT, database_ready
from app.db import data
from app.db.pagination import page
from app.main import app
from app.migrate import migrate
from tests.integration.test_security_database import acting, db  # noqa: F401

pytestmark = [
    pytest.mark.enable_socket,
    pytest.mark.skipif(
        not os.environ.get("ENAT_TEST_ADMIN_DSN"),
        reason="isolated database runner required",
    ),
]


@pytest.fixture
def empty_database():
    name = "rehearsal_" + uuid4().hex
    with psycopg.connect(os.environ["ENAT_TEST_ADMIN_DSN"], autocommit=True) as admin:
        admin.execute(
            psycopg.sql.SQL("CREATE DATABASE {}").format(psycopg.sql.Identifier(name))
        )
        dsn = psycopg.conninfo.make_conninfo(
            os.environ["ENAT_TEST_ADMIN_DSN"], dbname=name
        )
        try:
            yield dsn
        finally:
            admin.execute(
                psycopg.sql.SQL("DROP DATABASE {} WITH (FORCE)").format(
                    psycopg.sql.Identifier(name)
                )
            )


def test_migrations_serialize_detect_drift_and_rollback(empty_database, tmp_path):
    migration = tmp_path / "001_probe.sql"
    migration.write_text(
        "CREATE TABLE probe(id int PRIMARY KEY); INSERT INTO probe VALUES(1);"
    )
    with ThreadPoolExecutor(max_workers=2) as workers:
        list(workers.map(lambda _: migrate(empty_database, tmp_path), range(2)))
    with psycopg.connect(empty_database, autocommit=True, row_factory=dict_row) as conn:
        assert conn.execute("SELECT count(*) AS n FROM probe").fetchone()["n"] == 1
        migration.write_text("CREATE TABLE changed(id int);")
        with pytest.raises(RuntimeError, match="checksum"):
            migrate(empty_database, tmp_path)
        migration.write_text(
            "CREATE TABLE probe(id int PRIMARY KEY); INSERT INTO probe VALUES(1);"
        )
        bad = tmp_path / "002_failure.sql"
        bad.write_text("CREATE TABLE should_rollback(id int); SELECT 1/0;")
        with pytest.raises(RuntimeError, match="rolled back"):
            migrate(empty_database, tmp_path)
        assert (
            conn.execute("SELECT to_regclass('should_rollback') AS t").fetchone()["t"]
            is None
        )
        assert conn.execute(
            "SELECT status,error_code FROM enat_ops.migrations WHERE name='002_failure.sql'"
        ).fetchone() == {"status": "failed", "error_code": "22012"}
        with pytest.raises(RuntimeError, match="rolled back"):
            migrate(empty_database, tmp_path)
        assert (
            conn.execute(
                "SELECT attempts FROM enat_ops.migrations WHERE name='002_failure.sql'"
            ).fetchone()["attempts"]
            == 2
        )


def test_keyset_ties_insert_boundary_and_cross_user_cursor(db):
    admin, a, b = db
    stamp = datetime(2026, 10, 1, tzinfo=timezone.utc)
    for uid in (a["id"], b["id"]):
        admin.execute(
            "INSERT INTO check_ins(user_id,timestamp) SELECT %s,%s FROM generate_series(1,207)",
            (uid, stamp),
        )
    admin.commit()
    with acting(a["id"]):
        batch, cursor = page("check_ins", a["id"], 50)
        assert len(batch) == 50 and cursor
        admin.execute(
            "INSERT INTO check_ins(user_id,timestamp) VALUES(%s,now())", (a["id"],)
        )
        admin.commit()
        seen = [r["id"] for r in batch]
        while cursor:
            batch, cursor = page("check_ins", a["id"], 50, cursor)
            assert all(r["user_id"] == a["id"] for r in batch)
            seen.extend(r["id"] for r in batch)
        assert len(seen) == len(set(seen)) == 207
        _, cursor = page("check_ins", a["id"], 1)
    with acting(b["id"]):
        rows, _ = page("check_ins", b["id"], 100, cursor)
        assert rows and all(r["user_id"] == b["id"] for r in rows)
        with pytest.raises(InvalidMutation):
            page("check_ins", b["id"], cursor="invalid")


def test_ready_requires_schema_and_is_independent_of_providers(db):
    admin, _, _ = db
    assert database_ready()
    admin.execute(
        "UPDATE enat_ops.migrations SET status='failed' WHERE name='009_operations.sql'"
    )
    admin.commit()
    try:
        assert not database_ready()
        client = TestClient(app)
        assert client.get("/health").status_code == 200
        assert client.get("/ready").status_code == 503
    finally:
        admin.execute(
            "UPDATE enat_ops.migrations SET status='applied' WHERE name='009_operations.sql'"
        )
        admin.commit()
    assert TestClient(app).get("/ready").status_code == 200


def test_http_page_limits_cursor_and_private_headers(db):
    admin, a, _ = db
    token = "enat_" + uuid4().hex
    admin.execute(
        "INSERT INTO app_sessions(token_hash,source_hash,user_id,expires_at) VALUES(%s,%s,%s,now()+interval '1 hour')",
        (hashlib.sha256(token.encode()).hexdigest(), uuid4().hex, a["id"]),
    )
    admin.execute(
        "INSERT INTO check_ins(user_id) SELECT %s FROM generate_series(1,55)",
        (a["id"],),
    )
    admin.commit()
    client = TestClient(app)
    headers = {"Authorization": "Bearer " + token}
    response = client.get("/checkin/history", headers=headers)
    assert response.status_code == 200 and len(response.json()) == 50
    assert response.headers["cache-control"] == "no-store"
    assert (
        len(
            client.get(
                "/checkin/history",
                params={"cursor": response.headers["x-next-cursor"]},
                headers=headers,
            ).json()
        )
        == 5
    )
    assert client.get("/checkin/history?limit=101", headers=headers).status_code == 422
    assert client.get("/checkin/history?cursor=bad", headers=headers).status_code == 422


def test_cleanup_expires_drafts_without_erasing_patient_content(db):
    admin, a, _ = db
    row = admin.execute(
        """INSERT INTO check_in_sessions(user_id,current_stage,stage_order,expires_at,draft_data)
        VALUES(%s,'symptoms','["symptoms"]',now()-interval '1 hour','{"symptoms":[{"raw_text":"synthetic"}]}') RETURNING id""",
        (a["id"],),
    ).fetchone()
    admin.commit()
    with admin.transaction():
        admin.execute("SET LOCAL ROLE enat_worker")
        admin.execute("SELECT enat_cleanup_security_state()")
    saved = admin.execute(
        "SELECT status,draft_data FROM check_in_sessions WHERE id=%s", (row["id"],)
    ).fetchone()
    assert (
        saved["status"] == "expired"
        and saved["draft_data"]["symptoms"][0]["raw_text"] == "synthetic"
    )


def test_history_query_uses_bounded_index_on_production_shaped_data(db):
    admin, a, _ = db
    admin.execute(
        "INSERT INTO check_ins(user_id,timestamp) SELECT %s,now()-make_interval(secs=>i) FROM generate_series(1,10000) i",
        (a["id"],),
    )
    admin.execute("ANALYZE check_ins")
    admin.commit()
    with acting(a["id"]), data.transaction() as conn:
        plan = conn.execute(
            "EXPLAIN (ANALYZE,BUFFERS,FORMAT JSON) SELECT * FROM check_ins WHERE user_id=%s ORDER BY timestamp DESC,id DESC LIMIT 51",
            (a["id"],),
        ).fetchone()["QUERY PLAN"]
    assert "checkin_history_cursor" in str(plan)
    assert plan[0]["Plan"]["Actual Rows"] == 51
    destination = Path("artifacts/operations")
    destination.mkdir(parents=True, exist_ok=True)
    import json

    (destination / "history-query-plan.json").write_text(json.dumps(plan, indent=2))


def test_encrypted_restore_authenticates_and_matches_database_objects(
    db, empty_database, tmp_path
):
    import json
    import secrets
    from time import monotonic

    from cryptography.exceptions import InvalidTag

    from scripts.backup_restore import backup, restore

    admin, a, _ = db
    objects = tmp_path / "source-objects"
    (objects / "audio-prompts").mkdir(parents=True)
    artifact = objects / "audio-prompts" / "rehearsal.wav"
    artifact.write_bytes(b"RIFF synthetic backup fixture")
    admin.execute(
        "INSERT INTO stage_audio_prompts(stage,prompt_am,prompt_en,category_am,category_en,audio_url) VALUES('restore-test','synthetic','synthetic','synthetic','synthetic','https://storage.invalid/storage/v1/object/public/audio-prompts/rehearsal.wav') ON CONFLICT(stage) DO UPDATE SET audio_url=excluded.audio_url"
    )
    admin.commit()
    key, archive = secrets.token_bytes(32), tmp_path / "backup.encrypted"
    manifest = backup(
        os.environ["ENAT_TEST_ADMIN_DSN"], objects, archive, key, tmp_path
    )
    corrupt = tmp_path / "corrupt.encrypted"
    damaged = bytearray(archive.read_bytes())
    damaged[-1] ^= 1
    corrupt.write_bytes(damaged)
    with pytest.raises(InvalidTag):
        restore(empty_database, corrupt, tmp_path / "restored-objects", key, tmp_path)
    with psycopg.connect(empty_database) as restored:
        assert restored.execute("SELECT to_regclass('users')").fetchone()[0] is None
    start = monotonic()
    actual = restore(
        empty_database, archive, tmp_path / "restored-objects", key, tmp_path
    )
    elapsed = monotonic() - start
    assert actual == manifest
    assert (
        tmp_path / "restored-objects" / "audio-prompts" / "rehearsal.wav"
    ).read_bytes() == artifact.read_bytes()
    with psycopg.connect(empty_database) as restored:
        assert restored.execute(
            "SELECT id FROM users WHERE id=%s", (a["id"],)
        ).fetchone()
        assert (
            restored.execute(
                "SELECT count(*) FROM enat_ops.migrations WHERE status='applied'"
            ).fetchone()[0]
            == SCHEMA_COUNT
        )
        assert not restored.execute(
            "SELECT has_table_privilege('anon','check_ins','SELECT')"
        ).fetchone()[0]
    with pytest.raises(ValueError, match="empty isolated"):
        restore(empty_database, archive, tmp_path / "another-target", key, tmp_path)
    destination = Path("artifacts/operations")
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "restore.json").write_text(
        json.dumps(
            {
                "synthetic_only": True,
                "restore_seconds": elapsed,
                "encrypted_bytes": archive.stat().st_size,
                "objects_verified": len(manifest["objects"]),
                "authenticated_corruption_rejected": True,
                "restricted_grants_preserved": True,
            },
            indent=2,
        )
    )
