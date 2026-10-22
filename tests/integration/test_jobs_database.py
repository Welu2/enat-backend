"""Worker recovery, concurrent scheduling, deduplication, and actual role grants."""

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, time, timedelta
from uuid import uuid4

import pytest
from psycopg.types.json import Jsonb

from app.config import get_settings
from app.core.clock import LOCAL_ZONE, utc_now
from app.core.errors import DataUnavailable
from app.db import data, idempotency, jobs, worker
from app.db.repositories.supplements import SupplementRepository
from app.jobs import handle, process_one
from app.services.reminders import ReminderService
from tests.integration.test_security_database import acting, db, pytestmark  # noqa: F401


@pytest.fixture
def queue(db, monkeypatch):
    settings = get_settings().model_copy(
        update={"worker_database_url": os.environ["ENAT_TEST_WORKER_DSN"]}
    )
    monkeypatch.setattr(worker, "get_settings", lambda: settings)
    admin, a, b = db
    admin.execute("TRUNCATE background_jobs,scheduler_state")
    admin.execute("UPDATE domain_outbox SET delivered_at=now()")
    admin.commit()
    worker.get_pool.cache_clear()
    yield admin, a, b
    worker.close_pool()


def enqueue(admin, uid, kind="user.daily", payload=None, max_attempts=5):
    return admin.execute(
        """INSERT INTO background_jobs(user_id,kind,dedupe_key,payload,max_attempts)
        VALUES(%s,%s,%s,%s,%s) RETURNING *""",
        (
            uid,
            kind,
            uuid4().hex,
            Jsonb(
                payload
                or {"occurrence": utc_now().astimezone(LOCAL_ZONE).date().isoformat()}
            ),
            max_attempts,
        ),
    ).fetchone()


def test_scheduler_pages_resume_after_lease_expiry_and_deduplicate(queue):
    admin, a, b = queue
    today = utc_now().astimezone(LOCAL_ZONE).date()
    admin.execute(
        "INSERT INTO scheduler_state(name,occurrence) VALUES('daily',%s)",
        (today - timedelta(days=1),),
    )
    # Seed over the former 1,000-row scan cap with deterministic, active users.
    admin.execute("""INSERT INTO users(id,created_at) SELECT gen_random_uuid(),now()-interval '3 days'
                      FROM generate_series(1,1005)""")
    admin.commit()
    first, second = uuid4(), uuid4()
    with worker.worker_context():
        assert jobs.schedule_page(first, 100) == 100
        assert jobs.schedule_page(second, 100) == 0
    checkpoint = admin.execute("SELECT * FROM scheduler_state").fetchone()
    assert checkpoint["cursor_id"]
    admin.execute("UPDATE scheduler_state SET lease_until=now()-interval '1 second'")
    admin.commit()
    with worker.worker_context():
        for _ in range(30):
            jobs.schedule_page(second, 100)
    rows = admin.execute(
        "SELECT dedupe_key,count(*) AS n FROM background_jobs GROUP BY dedupe_key"
    ).fetchall()
    assert len(rows) > 1000 and all(r["n"] == 1 for r in rows)
    expected = admin.execute(
        "SELECT count(*) AS n FROM users WHERE disabled_at IS NULL AND created_at < %s",
        (datetime.combine(today, time.min, LOCAL_ZONE),),
    ).fetchone()["n"]
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM background_jobs WHERE payload->>'occurrence'=%s",
            ((today - timedelta(days=1)).isoformat(),),
        ).fetchone()["n"]
        == expected
    )
    # Rewind a completed page to model a repeated scheduler invocation.
    admin.execute(
        "UPDATE scheduler_state SET occurrence=%s,cursor_id=NULL",
        (today - timedelta(days=1),),
    )
    admin.commit()
    with worker.worker_context():
        jobs.schedule_page(second, 100)
    assert admin.execute("SELECT count(*) AS n FROM background_jobs").fetchone()[
        "n"
    ] == len(rows)


def test_two_schedulers_cannot_own_the_same_page(queue):
    admin, a, _ = queue
    admin.execute(
        "UPDATE users SET created_at=now()-interval '3 days' WHERE id=%s", (a["id"],)
    )
    admin.execute(
        "INSERT INTO scheduler_state(name,occurrence) VALUES('daily',current_date-1)"
    )
    admin.commit()

    def schedule(_):
        with worker.worker_context():
            return jobs.schedule_page(uuid4(), 10)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(schedule, range(2)))
    assert sum(value > 0 for value in results) == 1


def test_claim_heartbeat_fencing_terminal_failure_and_replay(queue):
    admin, a, _ = queue
    row = enqueue(admin, a["id"], max_attempts=2)
    admin.commit()
    with worker.worker_context():
        first = jobs.claim()
        assert first["attempts"] == 1 and jobs.claim() is None
        assert jobs.heartbeat(first)
    admin.execute("UPDATE background_jobs SET lease_until=now()-interval '1 second'")
    admin.commit()
    with worker.worker_context():
        second = jobs.claim()
        assert second["attempts"] == 2 and second["lease_token"] != first["lease_token"]
        assert not jobs.finish(first) and not jobs.heartbeat(first)
        jobs.fail(first)
        assert jobs.heartbeat(second)
    admin.execute("UPDATE background_jobs SET lease_until=now()-interval '1 second'")
    admin.commit()
    with worker.worker_context():
        assert jobs.claim() is None
        assert jobs.stats()["failed"] == 1
        assert jobs.replay(row["id"])
        assert not jobs.replay(row["id"])
        assert jobs.claim()["attempts"] == 1


def test_parallel_workers_claim_each_job_once(queue):
    admin, a, _ = queue
    for _ in range(10):
        enqueue(admin, a["id"])
    admin.commit()

    def claim(_):
        with worker.worker_context():
            return jobs.claim()["id"]

    with ThreadPoolExecutor(max_workers=10) as pool:
        ids = list(pool.map(claim, range(10)))
    assert len(set(ids)) == 10


def test_crash_after_domain_effect_retries_without_duplicate_reminders(queue):
    admin, a, _ = queue
    with acting(a["id"]):
        for name in ("iron", "calcium"):
            SupplementRepository().create(
                a["id"],
                {"name": name, "reminder_enabled": True, "reminder_time": "09:00:00"},
            )
    enqueue(admin, a["id"])
    admin.commit()
    with worker.worker_context(a["id"]):
        first = jobs.claim()
        handle(first)  # Simulate death before queue acknowledgement.
    admin.execute("UPDATE background_jobs SET lease_until=now()-interval '1 second'")
    admin.commit()
    assert process_one()
    rows = admin.execute(
        "SELECT * FROM reminders WHERE user_id=%s", (a["id"],)
    ).fetchall()
    assert len([r for r in rows if r["type"] == "supplement"]) == 2
    assert len(rows) == 3
    assert (
        admin.execute("SELECT status FROM background_jobs").fetchone()["status"]
        == "succeeded"
    )


def test_failed_user_does_not_block_another_and_retry_is_delayed(queue):
    admin, a, b = queue
    bad = enqueue(admin, a["id"], kind="unsupported")
    enqueue(admin, b["id"])
    admin.commit()
    assert process_one() and process_one()
    row = admin.execute(
        "SELECT * FROM background_jobs WHERE id=%s", (bad["id"],)
    ).fetchone()
    assert row["status"] == "pending" and row["due_at"] > utc_now()
    assert row["last_error"] == "handler_failed"
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM reminders WHERE user_id=%s", (b["id"],)
        ).fetchone()["n"]
        == 1
    )


def test_outbox_delivery_survives_lost_acknowledgement(queue):
    admin, a, _ = queue
    with acting(a["id"]):
        idempotency.emit(a["id"], "checkin.completed", uuid4())
    with worker.worker_context(a["id"]):
        assert jobs.dispatch_outbox() == 1
        assert jobs.dispatch_outbox() == 0
        first = jobs.claim()
        handle(first)
    admin.execute("UPDATE background_jobs SET lease_until=now()-interval '1 second'")
    admin.commit()
    assert process_one()
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM reminders WHERE user_id=%s", (a["id"],)
        ).fetchone()["n"]
        == 1
    )
    assert admin.execute(
        "SELECT delivered_at FROM domain_outbox WHERE user_id=%s", (a["id"],)
    ).fetchone()["delivered_at"]


def test_outbox_notification_and_delivery_marker_rollback_together(queue, monkeypatch):
    admin, a, _ = queue
    with acting(a["id"]):
        idempotency.emit(a["id"], "summary.created", uuid4())
    from app.db.repositories.reminders import ReminderRepository

    original = ReminderRepository.create_once

    def crash(*args, **kwargs):
        original(*args, **kwargs)
        raise RuntimeError("crash after notification")

    with worker.worker_context(a["id"]):
        jobs.dispatch_outbox()
        job = jobs.claim()
        monkeypatch.setattr(ReminderRepository, "create_once", crash)
        with pytest.raises(RuntimeError):
            handle(job)
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM reminders WHERE user_id=%s", (a["id"],)
        ).fetchone()["n"]
        == 0
    )
    assert (
        admin.execute(
            "SELECT delivered_at FROM domain_outbox WHERE user_id=%s", (a["id"],)
        ).fetchone()["delivered_at"]
        is None
    )


def test_worker_patient_scope_and_api_queue_denial(queue):
    admin, a, b = queue
    with worker.worker_context(a["id"]):
        assert [
            r["id"]
            for r in data.get_data_client().table("users").select().execute().data
        ] == [a["id"]]
        assert (
            data.get_data_client()
            .table("users")
            .select()
            .eq("id", b["id"])
            .execute()
            .data
            == []
        )
        for table in ("push_tokens", "summary_shares", "user_identities"):
            with pytest.raises(DataUnavailable):
                with data.transaction() as conn:
                    conn.execute("SELECT * FROM " + table)
    with acting(a["id"]):
        with pytest.raises(DataUnavailable):
            jobs.claim()
        with pytest.raises(DataUnavailable):
            jobs.schedule_page(uuid4())
    with worker.worker_context():
        assert data.get_data_client().table("users").select().execute().data == []


def test_stale_daily_work_does_not_send_old_dose_prompts(queue):
    admin, a, _ = queue
    with worker.worker_context(a["id"]):
        ReminderService().run_user_day(
            a["id"], utc_now().astimezone(LOCAL_ZONE).date() - timedelta(days=1)
        )
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM reminders WHERE user_id=%s", (a["id"],)
        ).fetchone()["n"]
        == 0
    )


def test_worker_automatic_summary_retry_creates_one_immutable_snapshot(queue):
    admin, a, _ = queue
    admin.execute(
        "UPDATE users SET created_at=now()-interval '40 days' WHERE id=%s", (a["id"],)
    )
    enqueue(admin, a["id"])
    admin.commit()
    with worker.worker_context(a["id"]):
        first = jobs.claim()
        handle(first)
    admin.execute("UPDATE background_jobs SET lease_until=now()-interval '1 second'")
    admin.commit()
    assert process_one()
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM summaries WHERE user_id=%s", (a["id"],)
        ).fetchone()["n"]
        == 1
    )
    with worker.worker_context(a["id"]):
        with pytest.raises(DataUnavailable):
            with data.transaction() as conn:
                conn.execute(
                    "UPDATE summaries SET content_json='{}' WHERE user_id=%s",
                    (a["id"],),
                )
        assert jobs.dispatch_outbox() == 1
    assert process_one()
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM reminders WHERE user_id=%s AND type='summary.created'",
            (a["id"],),
        ).fetchone()["n"]
        == 1
    )


def test_real_worker_process_death_and_cli_restart(queue):
    admin, a, _ = queue
    enqueue(admin, a["id"])
    admin.commit()
    env = {
        **os.environ,
        "PROCESS_ROLE": "worker",
        "WORKER_DATABASE_URL": os.environ["ENAT_TEST_WORKER_DSN"],
        "DATABASE_URL": "",
        "ADDIS_API_KEY": "",
        "SUPABASE_SERVICE_ROLE_KEY": "",
        "SUPABASE_URL": "",
    }
    crash = """import os
from app.db.worker import worker_context
from app.db import jobs
from app.jobs import handle
with worker_context():
    job = jobs.claim()
with worker_context(job['user_id']):
    handle(job)
os._exit(9)
"""
    result = subprocess.run(
        [sys.executable, "-c", crash], env=env, capture_output=True, timeout=20
    )
    assert result.returncode == 9, result.stderr.decode()
    admin.execute("UPDATE background_jobs SET lease_until=now()-interval '1 second'")
    admin.commit()
    result = subprocess.run(
        [sys.executable, "-m", "app.jobs", "worker", "--once"],
        env=env,
        capture_output=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr.decode()
    assert admin.execute("SELECT status,attempts FROM background_jobs").fetchone() == {
        "status": "succeeded",
        "attempts": 2,
    }
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM reminders WHERE user_id=%s", (a["id"],)
        ).fetchone()["n"]
        == 1
    )
