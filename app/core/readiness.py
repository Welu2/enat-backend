"""Local database/schema readiness, deliberately independent of speech providers."""

from threading import Lock

from app.db.data import get_pool

SCHEMA_VERSION = "009_operations.sql"
_probe_running = Lock()


def database_ready():
    # Keep at most one DB probe alive even if an HTTP timeout abandons a
    # worker thread during a network partition. Later probes fail immediately.
    if not _probe_running.acquire(blocking=False):
        return False
    try:
        with get_pool().connection(timeout=0.5) as conn, conn.transaction():
            conn.execute("SET LOCAL statement_timeout='500ms'")
            # This reviewed migration is additive and transactional. The bridge
            # can serve schema 009 while 010 is running, applied or rolled back.
            # All other ledger entries still have to match the required schema.
            row = conn.execute("""SELECT count(*) AS total,
                count(*) FILTER(WHERE status='applied') AS applied, max(name) AS latest
                FROM enat_ops.migrations
                WHERE name <> '010_privacy_workflows.sql'""").fetchone()
            return row == {"total": 9, "applied": 9, "latest": SCHEMA_VERSION}
    except Exception:
        # Probe errors contain DSNs/SQL; expose only the bounded boolean outcome.
        return False
    finally:
        _probe_running.release()
