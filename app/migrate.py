"""Serialized, checksum-verified migrations using a separately provisioned owner DSN.

Run `MIGRATION_DATABASE_URL=... python -m app.migrate`. Never use an API DSN.
Failed attempts remain recorded; retries rerun the entire rolled-back migration.
Existing untracked schemas must be rehearsed and explicitly baselined by an owner.
"""

import argparse
import hashlib
import os
import re
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

LOCK = 836916285


def initialize(conn):
    conn.execute("CREATE SCHEMA IF NOT EXISTS enat_ops")
    conn.execute("REVOKE ALL ON SCHEMA enat_ops FROM PUBLIC")
    conn.execute("""CREATE TABLE IF NOT EXISTS enat_ops.migrations (
        name text PRIMARY KEY, checksum text NOT NULL,
        status text NOT NULL CHECK(status IN ('running','applied','failed')),
        attempts integer NOT NULL DEFAULT 1, started_at timestamptz NOT NULL DEFAULT now(),
        finished_at timestamptz, error_code text)""")
    conn.execute("REVOKE ALL ON enat_ops.migrations FROM PUBLIC")


def apply_one(conn, path):
    source = path.read_text()
    checksum = hashlib.sha256(source.encode()).hexdigest()
    row = conn.execute(
        "SELECT * FROM enat_ops.migrations WHERE name=%s", (path.name,)
    ).fetchone()
    if row and row["checksum"] != checksum:
        raise RuntimeError(f"Migration checksum changed: {path.name}")
    if row and row["status"] == "applied":
        return False
    # Earlier migrations carry an outer transaction. The runner owns it now so
    # schema effects and the applied ledger record are committed together.
    body = re.sub(r"^\s*(?:begin|commit);\s*$", "", source, flags=re.I | re.M)
    conn.execute(
        """INSERT INTO enat_ops.migrations(name,checksum,status) VALUES(%s,%s,'running')
        ON CONFLICT(name) DO UPDATE SET status='running',attempts=enat_ops.migrations.attempts+1,
        started_at=now(),finished_at=NULL,error_code=NULL""",
        (path.name, checksum),
    )
    try:
        with conn.transaction():
            conn.execute("SET LOCAL lock_timeout='5s'")
            conn.execute("SET LOCAL statement_timeout='120s'")
            conn.execute(body, prepare=False)
            conn.execute(
                "UPDATE enat_ops.migrations SET status='applied',finished_at=now() WHERE name=%s",
                (path.name,),
            )
    except Exception as exc:
        conn.execute(
            "UPDATE enat_ops.migrations SET status='failed',finished_at=now(),error_code=%s WHERE name=%s",
            (
                exc.sqlstate if isinstance(exc, psycopg.Error) else "runner_error",
                path.name,
            ),
        )
        # SQL errors can contain patient rows or secrets; never echo them.
        raise RuntimeError(f"Migration failed and rolled back: {path.name}") from None
    return True


def migrate(dsn, directory=Path("migrations")):
    with psycopg.connect(
        dsn, autocommit=True, row_factory=dict_row, connect_timeout=5
    ) as conn:
        conn.execute("SET statement_timeout='30s'")
        conn.execute("SELECT pg_advisory_lock(%s)", (LOCK,))
        try:
            initialize(conn)
            paths = sorted(directory.glob("[0-9][0-9][0-9]_*.sql"))
            if not paths:
                raise RuntimeError("No migrations found")
            known = {p.name for p in paths}
            if any(
                r["name"] not in known
                for r in conn.execute("SELECT name FROM enat_ops.migrations")
            ):
                raise RuntimeError(
                    "Database has migrations unknown to this image; use a compatible runner"
                )
            for path in paths:
                if apply_one(conn, path):
                    print("Applied", path.name, flush=True)
        finally:
            conn.execute("SELECT pg_advisory_unlock(%s)", (LOCK,))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path("migrations"))
    args = parser.parse_args()
    dsn = os.environ.get("MIGRATION_DATABASE_URL")
    if not dsn:
        parser.error("MIGRATION_DATABASE_URL is required")
    try:
        migrate(dsn, args.directory)
    except (psycopg.Error, RuntimeError):
        raise SystemExit(
            "Migration failed; inspect the protected ledger and database logs"
        ) from None


if __name__ == "__main__":
    main()
