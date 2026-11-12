"""Bounded durable queue operations. All lease mutations are token-fenced."""

import random
from uuid import uuid4

from app.config import get_settings
from app.db.data import transaction


def schedule_page(token, limit=100):
    with transaction() as conn:
        return conn.execute(
            "SELECT enat_schedule_page(%s,%s,%s) AS n",
            (token, limit, get_settings().reminder_cron_hour),
        ).fetchone()["n"]


def dispatch_outbox(limit=100):
    with transaction() as conn:
        rows = conn.execute(
            """SELECT * FROM domain_outbox o WHERE delivered_at IS NULL
            AND NOT EXISTS(SELECT 1 FROM background_jobs j WHERE j.dedupe_key='outbox:'||o.id)
            ORDER BY created_at,id LIMIT %s FOR UPDATE SKIP LOCKED""",
            (limit,),
        ).fetchall()
        for row in rows:
            from psycopg.types.json import Jsonb

            conn.execute(
                """INSERT INTO background_jobs(user_id,kind,dedupe_key,payload,due_at)
                VALUES(%s,'outbox.deliver',%s,%s,%s) ON CONFLICT DO NOTHING""",
                (
                    row["user_id"],
                    "outbox:" + str(row["id"]),
                    Jsonb(
                        {
                            "outbox_id": str(row["id"]),
                            "_traceparent": row["payload"].get("_traceparent"),
                        }
                    ),
                    row["created_at"],
                ),
            )
        return len(rows)


def claim(lease_seconds=60):
    with transaction() as conn:
        # Expired final attempts enter the failed queue instead of disappearing.
        conn.execute("""UPDATE background_jobs SET status='failed',finished_at=now(),
            last_error='lease_expired',lease_token=NULL,lease_until=NULL WHERE id IN
            (SELECT id FROM background_jobs WHERE status='running' AND lease_until<=now()
             AND attempts>=max_attempts ORDER BY lease_until LIMIT 100 FOR UPDATE SKIP LOCKED)""")
        return conn.execute(
            """WITH candidate AS (
            SELECT id FROM background_jobs WHERE attempts<max_attempts AND
            ((status='pending' AND due_at<=now()) OR (status='running' AND lease_until<=now()))
            ORDER BY due_at,id LIMIT 1 FOR UPDATE SKIP LOCKED)
            UPDATE background_jobs j SET status='running',attempts=attempts+1,
            lease_token=%s,lease_until=now()+make_interval(secs=>%s),heartbeat_at=now()
            FROM candidate c WHERE j.id=c.id RETURNING j.*""",
            (uuid4(), lease_seconds),
        ).fetchone()


def heartbeat(job, lease_seconds=60):
    with transaction() as conn:
        return (
            conn.execute(
                """UPDATE background_jobs SET heartbeat_at=now(),
            lease_until=now()+make_interval(secs=>%s) WHERE id=%s AND lease_token=%s
            AND status='running' AND lease_until>now() RETURNING id""",
                (lease_seconds, job["id"], job["lease_token"]),
            ).fetchone()
            is not None
        )


def finish(job):
    with transaction() as conn:
        return (
            conn.execute(
                """UPDATE background_jobs SET status='succeeded',finished_at=now(),
            last_error=NULL,lease_token=NULL,lease_until=NULL WHERE id=%s AND lease_token=%s
            AND status='running' AND lease_until>now() RETURNING id""",
                (job["id"], job["lease_token"]),
            ).fetchone()
            is not None
        )


def fail(job):
    # Retry scheduling only; credentials use secrets/UUID elsewhere.
    delay = random.uniform(0.5, 1.5) * min(3600, 5 * 2 ** (job["attempts"] - 1))  # nosec B311
    with transaction() as conn:
        conn.execute(
            """UPDATE background_jobs SET
            status=CASE WHEN attempts>=max_attempts THEN 'failed' ELSE 'pending' END,
            finished_at=CASE WHEN attempts>=max_attempts THEN now() ELSE NULL END,
            due_at=now()+make_interval(secs=>%s),last_error='handler_failed',
            lease_token=NULL,lease_until=NULL WHERE id=%s AND lease_token=%s
            AND status='running' AND lease_until>now()""",
            (delay, job["id"], job["lease_token"]),
        )


def replay(job_id):
    with transaction() as conn:
        return (
            conn.execute(
                """UPDATE background_jobs SET status='pending',attempts=0,
            due_at=now(),finished_at=NULL,last_error=NULL,replay_count=replay_count+1
            WHERE id=%s AND status='failed' RETURNING id""",
                (job_id,),
            ).fetchone()
            is not None
        )


def stats():
    with transaction() as conn:
        row = conn.execute("""SELECT count(*) FILTER(WHERE status='failed') AS failed,
            count(*) FILTER(WHERE status='pending') AS pending,
            count(*) FILTER(WHERE status='running') AS running,
            coalesce(extract(epoch FROM now()-min(due_at) FILTER
            (WHERE status IN ('pending','running') AND due_at<now())),0) AS oldest_due_seconds
            FROM background_jobs""").fetchone()
        row["scheduler_lag_seconds"] = conn.execute(
            """SELECT coalesce(max(greatest(0,
            extract(epoch FROM now()-((occurrence+make_interval(hours=>%s))
            AT TIME ZONE 'Africa/Addis_Ababa')))),0) AS lag FROM scheduler_state""",
            (get_settings().reminder_cron_hour,),
        ).fetchone()["lag"]
        row["privacy_queue"] = conn.execute(
            "SELECT enat_privacy_queue() AS value"
        ).fetchone()["value"]
        return row
