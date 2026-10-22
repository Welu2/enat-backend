"""Fail closed on dependency or source findings and preserve reports plus runtime SBOM."""

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT / "artifacts/security"
    output.mkdir(parents=True, exist_ok=True)
    failed = False
    for lock, name in (
        ("requirements.lock", "runtime"),
        ("requirements-dev.lock", "development"),
    ):
        command = [
            sys.executable,
            "-m",
            "pip_audit",
            "--disable-pip",
            "--require-hashes",
            "-r",
            lock,
            "--format",
            "json",
            "--output",
            str(output / f"{name}-audit.json"),
        ]
        failed |= subprocess.run(command, cwd=ROOT, check=False).returncode != 0
    failed |= (
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip_audit",
                "--disable-pip",
                "--require-hashes",
                "-r",
                "requirements.lock",
                "--format",
                "cyclonedx-json",
                "--output",
                str(output / "runtime.cdx.json"),
            ],
            cwd=ROOT,
            check=False,
        ).returncode
        != 0
    )
    failed |= (
        subprocess.run(
            [
                sys.executable,
                "-m",
                "bandit",
                "-c",
                "pyproject.toml",
                "-r",
                "app",
                "scripts/backup_restore.py",
                "scripts/release_record.py",
                "scripts/deploy_release.py",
                "scripts/staging_verify.py",
                "scripts/staging_load.py",
                "scripts/evaluate_voice.py",
                "scripts/manage_clinician.py",
                "-f",
                "json",
                "-o",
                str(output / "bandit.json"),
            ],
            cwd=ROOT,
            check=False,
        ).returncode
        != 0
    )
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tools": {name: version(name) for name in ("pip-audit", "bandit")},
        "sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("requirements.lock", "requirements-dev.lock")
        },
        "passed": not failed,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    raise SystemExit(int(failed))


if __name__ == "__main__":
    main()
