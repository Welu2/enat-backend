"""Readiness-only overlay for the pinned schema-010 fallback source.

Accept only reviewed additive care migrations. This file replaces
app/core/readiness.py in the fallback build, never in the candidate.
"""

from threading import Lock

from app.db.data import get_pool

BASE_MIGRATIONS = (
    "001_initial_schema.sql",
    "002_maternal_onboarding_and_hospital.sql",
    "003_anc_contacts_and_checkin_summary.sql",
    "004_stage_audio_prompts.sql",
    "005_identity_isolation_and_shares.sql",
    "006_resource_limits.sql",
    "007_workflow_integrity.sql",
    "008_durable_jobs.sql",
    "009_operations.sql",
    "010_privacy_workflows.sql",
)
ADDITIVE_MIGRATIONS = ("011_care_portal.sql", "012_offline_checkins.sql")
_probe_running = Lock()


def database_ready():
    if not _probe_running.acquire(blocking=False):
        return False
    try:
        with get_pool().connection(timeout=0.5) as conn, conn.transaction():
            conn.execute("SET LOCAL statement_timeout='500ms'")
            rows = conn.execute(
                "SELECT name,status FROM enat_ops.migrations ORDER BY name"
            ).fetchall()
            names = tuple(row["name"] for row in rows)
            if names not in tuple(
                BASE_MIGRATIONS + ADDITIVE_MIGRATIONS[:n] for n in range(3)
            ):
                return False
            if any(row["status"] != "applied" for row in rows[:10]):
                return False
            additions = rows[10:]
            # Only the last attempted migration can be incomplete.
            return all(row["status"] == "applied" for row in additions[:-1]) and (
                not additions
                or additions[-1]["status"] in {"applied", "running", "failed"}
            )
    except Exception:
        return False
    finally:
        _probe_running.release()
