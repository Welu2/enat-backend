"""Rehearse forward/rollback/forward on synthetic state in the disposable DB runner."""

import hashlib
import json
import os
import subprocess
from pathlib import Path
from time import monotonic
from uuid import uuid4

import psycopg

PROBE = r"""
import json, os, signal, subprocess, time, urllib.request
server = subprocess.Popen(['bash','scripts/run_api.sh'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(100):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8000/ready',timeout=2) as response:
                assert response.status == 200
            break
        except OSError:
            time.sleep(.1)
    else:
        raise RuntimeError('Candidate failed schema readiness')
    request = urllib.request.Request('http://127.0.0.1:8000/checkin/history',headers={'Authorization':'Bearer '+os.environ['SYNTHETIC_TOKEN']})
    with urllib.request.urlopen(request,timeout=2) as response:
        rows = json.load(response)
        assert len(rows) == 1 and rows[0]['id'] == os.environ['SYNTHETIC_ROW']
finally:
    server.terminate()
    assert server.wait(timeout=35) in (0,-signal.SIGTERM)
print('Schema readiness and persisted owned history passed')
"""


def main():
    dsn = os.environ.get("ENAT_TEST_ADMIN_DSN", "")
    directory = psycopg.conninfo.conninfo_to_dict(dsn).get("host", "")
    if not directory.startswith("/tmp/enat-security-"):
        raise SystemExit("Only disposable test_database.py clusters are supported")
    images = os.environ.get("ENAT_REHEARSAL_IMAGES", "").split(",")
    if len(images) != 2 or images[0] == images[1]:
        raise SystemExit(
            "Provide previous,current candidate images in ENAT_REHEARSAL_IMAGES"
        )
    uid, row, token = uuid4(), uuid4(), "enat_" + uuid4().hex
    with psycopg.connect(dsn) as conn:
        conn.execute("INSERT INTO users(id) VALUES(%s)", (uid,))
        conn.execute("INSERT INTO check_ins(id,user_id) VALUES(%s,%s)", (row, uid))
        conn.execute(
            "INSERT INTO app_sessions(token_hash,source_hash,user_id,expires_at) VALUES(%s,%s,%s,now()+interval '1 hour')",
            (hashlib.sha256(token.encode()).hexdigest(), uuid4().hex, uid),
        )
    # Only expose the synthetic cluster's socket to the container UID; the data
    # directory remains 0700 and the mount is read-only. No live credentials.
    os.chmod(directory, 0o755)
    env = {
        "ENVIRONMENT": "test",
        "PROCESS_ROLE": "api",
        "DATABASE_URL": os.environ["ENAT_TEST_APP_DSN"],
        "ENABLE_REQUEST_LIMITS": "false",
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "synthetic-placeholder",
        "ADDIS_API_KEY": "synthetic-placeholder",
        "SYNTHETIC_TOKEN": token,
        "SYNTHETIC_ROW": str(row),
        "OTLP_ENDPOINT": "",
    }
    steps = []
    for image, ledger_status in (
        (images[0], "running"),
        (images[0], "failed"),
        (images[1], "applied"),
        (images[0], "applied"),
        (images[1], "applied"),
    ):
        # Isolated fault injection: an additive migration attempt must not take
        # the bridge out of rotation. No production ledger is ever modified.
        with psycopg.connect(dsn) as conn:
            conn.execute(
                "UPDATE enat_ops.migrations SET status=%s WHERE name='012_offline_checkins.sql'",
                (ledger_status,),
            )
        start = monotonic()
        command = [
            "docker",
            "run",
            "--rm",
            "--network=none",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=64m",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges",
            "-v",
            f"{directory}:{directory}:ro",
        ]
        for key, value in env.items():
            command.extend(["-e", f"{key}={value}"])
        result = subprocess.run(
            [*command, image, "python", "-c", PROBE],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode:
            raise SystemExit(
                f"Rollback probe failed for {image} with schema 012 {ledger_status}: "
                + result.stderr[-2000:]
            )
        identifier = subprocess.check_output(
            ["docker", "image", "inspect", "--format", "{{.Id}}", image], text=True
        ).strip()
        steps.append(
            {
                "image": identifier,
                "offline_ledger_status": ledger_status,
                "seconds": monotonic() - start,
                "ready_and_history": True,
            }
        )
    destination = Path("artifacts/operations")
    destination.mkdir(parents=True, exist_ok=True)
    report = {
        "synthetic_only": True,
        "schema_version": 12,
        "schema_rolled_back": False,
        "steps": steps,
    }
    (destination / "image-rollback.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(
        "Candidate forward/rollback/forward passed with schema and patient-row identity retained"
    )


if __name__ == "__main__":
    main()
