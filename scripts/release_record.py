"""Create and validate a portable release evidence bundle; never infer approval."""

import argparse
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

GATES = tuple(f"R{i}" for i in range(1, 9))
SHA = re.compile(r"[0-9a-f]{40}")
IMAGE = re.compile(r"[a-z0-9][a-z0-9./:_-]*@sha256:[0-9a-f]{64}")
ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Evidence timestamps need a timezone")
    return parsed


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence_file(root, relative):
    require(isinstance(relative, str), "Evidence path must be relative")
    require(not Path(relative).is_absolute(), "Evidence path must be relative")
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), "Evidence must stay inside its bundle")
    require(path.is_file(), "Evidence file missing")
    return path


def validate(record, root, *, mode="staging", now=None):
    """Validate evidence integrity, freshness and explicit release decisions.

    This is a consistency gate, not a signature or identity verification service.
    Access to the bundle and approval process must be controlled externally.
    """
    now = now or datetime.now(timezone.utc)
    require(mode in {"staging", "pilot", "production"}, "Unknown release mode")
    require(record["schema_version"] == 1, "Unsupported release record")
    require(SHA.fullmatch(record["source_revision"]), "Full source SHA required")
    require(IMAGE.fullmatch(record["image"]), "Immutable registry digest required")
    require(
        re.fullmatch(r"sha256:[0-9a-f]{64}", record["image_id"]),
        "Container image ID required",
    )
    created = timestamp(record["created_at"])
    require(
        now - timedelta(days=7) <= created <= now + timedelta(minutes=5),
        "Candidate evidence must be at most seven days old",
    )
    require(set(record["gates"]) == set(GATES), "All R1–R8 gates must be present")
    evidence = record["evidence"]
    for name in ("source_security", "container_security", "capacity"):
        item = evidence[name]
        path = evidence_file(root, item["path"])
        require(sha256(path) == item["sha256"], f"{name}: evidence hash mismatch")
    source = json.loads(
        evidence_file(root, evidence["source_security"]["path"]).read_text()
    )
    container = json.loads(
        evidence_file(root, evidence["container_security"]["path"]).read_text()
    )
    capacity = json.loads(evidence_file(root, evidence["capacity"]["path"]).read_text())
    for report in (source, container):
        require(report["passed"] is True, "Security gate failed")
        scanned = timestamp(report["generated_at"])
        require(
            created - timedelta(days=1) <= scanned <= created, "Stale security scan"
        )
    require(not container["blockers"], "Unresolved container findings")
    require(container["image_id"] == record["image_id"], "Scanned image mismatch")
    require(source["sha256"] == record["lock_sha256"], "Dependency lock mismatch")
    require(capacity["passed"] is True, "Capacity gate failed")
    require(capacity["execution"] == "compose", "Compose capacity evidence required")
    require(
        capacity["deployment"]["image"] == record["image_id"],
        "Load-tested image mismatch",
    )
    require(
        capacity["duration_seconds"] >= 1800, "Full 30-minute capacity run required"
    )
    require(capacity["target_rps"] >= 50, "Capacity rate below target")
    require(capacity["scheduled_requests"] >= 90000, "Capacity sample below target")
    require(0 <= capacity["p95_seconds"] <= 0.5, "Capacity p95 failed")
    require(
        capacity["p95_seconds"] <= capacity["p99_seconds"] <= 1, "Capacity p99 failed"
    )
    require(0 <= capacity["error_rate"] < 0.01, "Capacity error budget failed")
    require(capacity["both_ready_after_recovery"] is True, "Recovery failed")
    require(
        capacity["deployment"]["scheduler_worker_outbox_delivered_once"] is True,
        "Outbox evidence missing",
    )
    require(
        "EnatApiUnavailable" in capacity["deployment"]["local_alert_notifications"],
        "Outage alert evidence missing",
    )
    required = () if mode == "staging" else GATES[:7] if mode == "pilot" else GATES
    for gate in required:
        value = record["gates"][gate]
        require(value["status"] == "accepted", f"{gate}: acceptance pending")
        require(
            all(
                isinstance(value.get(k), str) and value[k].strip()
                for k in ("owner", "reviewer")
            ),
            f"{gate}: named owner/reviewer required",
        )
        require(
            value["source_revision"] == record["source_revision"],
            f"{gate}: source mismatch",
        )
        require(value["image"] == record["image"], f"{gate}: image mismatch")
        require(
            created <= timestamp(value["accepted_at"]) <= now,
            f"{gate}: invalid approval date",
        )
        require(bool(value["evidence"]), f"{gate}: evidence required")
        for item in value["evidence"]:
            require(
                sha256(evidence_file(root, item["path"])) == item["sha256"],
                f"{gate}: evidence hash mismatch",
            )
    if mode != "staging":
        decision = record["decision"]
        require(decision["mode"] == mode, "Explicit pilot/production decision required")
        require(bool(decision["environment_id"].strip()), "Target environment required")
        require(
            IMAGE.fullmatch(decision["rollback_image"])
            and decision["rollback_image"] != record["image"],
            "Distinct compatible rollback digest required",
        )
        require(
            all(
                decision["approvers"].get(role, "").strip()
                for role in ("clinical", "privacy", "operations")
            ),
            "Clinical, privacy and operations approvers required",
        )
        require(
            created <= timestamp(decision["approved_at"]) <= now,
            "Invalid decision date",
        )
    return record


def create(source_revision, image, image_id, root):
    evidence = {}
    for name, relative in (
        ("source_security", "security/manifest.json"),
        ("container_security", "security/container-gate.json"),
        ("capacity", "operations/load-compose.json"),
    ):
        evidence[name] = {
            "path": relative,
            "sha256": sha256(evidence_file(root, relative)),
        }
    record = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_revision": source_revision,
        "image": image,
        "image_id": image_id,
        "lock_sha256": {
            name: sha256(ROOT / name)
            for name in ("requirements.lock", "requirements-dev.lock")
        },
        "evidence": evidence,
        "gates": {
            name: {
                "status": "pending",
                "owner": "",
                "reviewer": "",
                "accepted_at": None,
                "source_revision": source_revision,
                "image": image,
                "evidence": [],
            }
            for name in GATES
        },
        "decision": None,
    }
    return validate(record, root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("create")
    build.add_argument("--source-revision", required=True)
    build.add_argument("--image", required=True)
    build.add_argument("--image-id", required=True)
    build.add_argument("--bundle", type=Path, required=True)
    check = commands.add_parser("validate")
    check.add_argument("record", type=Path)
    check.add_argument(
        "--mode", choices=("staging", "pilot", "production"), default="staging"
    )
    args = parser.parse_args()
    try:
        if args.command == "create":
            record = create(
                args.source_revision, args.image, args.image_id, args.bundle
            )
            with (args.bundle / "release.json").open("x") as stream:
                json.dump(record, stream, indent=2)
                stream.write("\n")
        else:
            validate(
                json.loads(args.record.read_text()), args.record.parent, mode=args.mode
            )
    except (ValueError, KeyError, TypeError, AttributeError, OSError):
        # Never print arbitrary evidence contents, URLs or exception payloads.
        raise SystemExit(
            "Release gate failed: inspect bundle completeness, dates, hashes and approvals."
        ) from None
    print(
        "Release evidence validated; staging eligibility is not patient-release approval."
    )


if __name__ == "__main__":
    main()
