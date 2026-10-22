"""Run database security tests in a disposable local PostgreSQL cluster.

Usage: .venv/bin/python scripts/test_database.py
Requires PostgreSQL binaries (override PG_BIN); no live services or credentials.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.migrate import apply_one, initialize  # noqa: E402


def main():
    pg_bin = Path(os.environ.get("PG_BIN", "/usr/lib/postgresql/16/bin"))
    with tempfile.TemporaryDirectory(prefix="enat-security-") as directory:
        data = str(Path(directory) / "data")
        subprocess.run(
            [
                str(pg_bin / "initdb"),
                "-D",
                data,
                "-A",
                "trust",
                "--no-locale",
                "--encoding=UTF8",
            ],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                str(pg_bin / "pg_ctl"),
                "-D",
                data,
                "-l",
                str(Path(directory) / "postgres.log"),
                "-o",
                f"-k {directory} -h '' -p 55483",
                "-w",
                "start",
            ],
            check=True,
            capture_output=True,
        )
        try:
            psql = [
                str(pg_bin / "psql"),
                "-h",
                directory,
                "-p",
                "55483",
                "-d",
                "postgres",
                "-v",
                "ON_ERROR_STOP=1",
            ]
            # Match Supabase client roles when testing grant revocation.
            subprocess.run(
                psql
                + [
                    "-c",
                    "CREATE ROLE anon; CREATE ROLE authenticated; CREATE ROLE service_role BYPASSRLS; CREATE SCHEMA storage; CREATE TABLE storage.buckets(id text primary key,public boolean); CREATE TABLE storage.objects(id int,bucket_id text); ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY; GRANT USAGE ON SCHEMA storage TO anon; GRANT SELECT ON storage.objects TO anon; CREATE POLICY legacy_public_read ON storage.objects FOR SELECT TO anon USING(true); INSERT INTO storage.buckets VALUES('summary-qr-codes',true),('audio-prompts',true); INSERT INTO storage.objects VALUES(1,'summary-qr-codes'),(2,'audio-prompts');",
                ],
                check=True,
                capture_output=True,
            )
            for migration in sorted(Path("migrations").glob("*.sql")):
                with psycopg.connect(
                    f"host={directory} port=55483 dbname=postgres",
                    autocommit=True,
                    row_factory=dict_row,
                ) as conn:
                    initialize(conn)
                    apply_one(conn, migration)
                print("Applied", migration, flush=True)
                if migration.name.startswith("004") and "--fresh" not in sys.argv:
                    subprocess.run(
                        psql
                        + [
                            "-c",
                            "INSERT INTO users(id,email,created_at) VALUES('00000000-0000-4000-8000-000000000001','legacy@example.org','2020-01-01T00:00:00Z'); INSERT INTO summaries(id,user_id,period_start,period_end,content_json,share_link_slug,qr_code_url) VALUES('00000000-0000-4000-8000-000000000002','00000000-0000-4000-8000-000000000001',current_date,current_date,'{}','legacy-secret','https://example.invalid/qr.png'); INSERT INTO check_ins(user_id,food_log,supplement_check) VALUES('00000000-0000-4000-8000-000000000001','{\"raw_text\":\"legacy food\"}','{\"supplement_name\":\"iron\",\"taken_today\":true}');",
                        ],
                        check=True,
                        capture_output=True,
                    )
            subprocess.run(
                psql
                + ["-c", "ALTER ROLE enat_app LOGIN; ALTER ROLE enat_worker LOGIN;"],
                check=True,
                capture_output=True,
            )
            env = dict(
                os.environ,
                ENAT_TEST_HAS_LEGACY="0" if "--fresh" in sys.argv else "1",
                ENAT_TEST_ADMIN_DSN=f"host={directory} port=55483 dbname=postgres",
                ENAT_TEST_APP_DSN=f"host={directory} port=55483 dbname=postgres user=enat_app",
                ENAT_TEST_WORKER_DSN=f"host={directory} port=55483 dbname=postgres user=enat_worker",
            )
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/integration", "-q", "-x"],
                env=env,
            ).returncode
            if result == 0 and "--demo" in sys.argv:
                result = subprocess.run(
                    [sys.executable, "scripts/care_demo.py"], env=env
                ).returncode
            if result == 0 and "--load" in sys.argv:
                return subprocess.run(
                    [sys.executable, "scripts/load_rehearsal.py"], env=env
                ).returncode
            if result == 0 and "--containers" in sys.argv:
                return subprocess.run(
                    [sys.executable, "scripts/rehearse_images.py"], env=env
                ).returncode
            return result
        finally:
            subprocess.run(
                [str(pg_bin / "pg_ctl"), "-D", data, "-m", "fast", "-w", "stop"],
                check=True,
                capture_output=True,
            )


if __name__ == "__main__":
    raise SystemExit(main())
