import copy
import json
from datetime import datetime, timedelta, timezone

import pytest

from scripts import deploy_release, release_record


@pytest.fixture
def bundle(tmp_path):
    now = datetime.now(timezone.utc)
    image_id = "sha256:" + "b" * 64
    locks = {
        name: release_record.sha256(release_record.ROOT / name)
        for name in ("requirements.lock", "requirements-dev.lock")
    }
    reports = {
        "security/manifest.json": {
            "passed": True,
            "generated_at": now.isoformat(),
            "sha256": locks,
        },
        "security/container-gate.json": {
            "passed": True,
            "generated_at": now.isoformat(),
            "image_id": image_id,
            "blockers": [],
        },
        "operations/load-compose.json": {
            "passed": True,
            "execution": "compose",
            "deployment": {
                "image": image_id,
                "scheduler_worker_outbox_delivered_once": True,
                "local_alert_notifications": ["EnatApiUnavailable"],
            },
            "duration_seconds": 1800,
            "target_rps": 50,
            "scheduled_requests": 90000,
            "p95_seconds": 0.2,
            "p99_seconds": 0.7,
            "error_rate": 0.001,
            "both_ready_after_recovery": True,
        },
    }
    for relative, value in reports.items():
        path = tmp_path / relative
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(value))
    record = release_record.create(
        "a" * 40, "ghcr.io/example/enat@sha256:" + "c" * 64, image_id, tmp_path
    )
    return record, tmp_path


def test_candidate_is_not_patient_approval(bundle):
    record, root = bundle
    release_record.validate(record, root)
    for mode in ("pilot", "production"):
        with pytest.raises(ValueError, match="acceptance pending"):
            release_record.validate(record, root, mode=mode)


def test_evidence_tampering_and_escape_rejected(bundle, tmp_path):
    record, root = bundle
    (root / "security/manifest.json").write_text('{"passed":true}')
    with pytest.raises(ValueError, match="hash mismatch"):
        release_record.validate(record, root)
    outside = tmp_path.parent / "outside-evidence.json"
    outside.write_text("{}")
    with pytest.raises(ValueError, match="inside"):
        release_record.evidence_file(root, "../outside-evidence.json")


@pytest.mark.parametrize(
    "field,value",
    [
        ("image", "ghcr.io/example/enat:latest"),
        ("image_id", "sha256:" + "d" * 64),
        ("source_revision", "short"),
    ],
)
def test_wrong_artifact_rejected(bundle, field, value):
    record, root = bundle
    record[field] = value
    with pytest.raises(ValueError):
        release_record.validate(record, root)


def test_stale_candidate_rejected(bundle):
    record, root = bundle
    with pytest.raises(ValueError, match="seven days"):
        release_record.validate(
            record, root, now=datetime.now(timezone.utc) + timedelta(days=8)
        )


def test_short_capacity_run_rejected_even_with_pass_flag(bundle):
    record, root = bundle
    item = record["evidence"]["capacity"]
    path = root / item["path"]
    report = json.loads(path.read_text())
    report["duration_seconds"] = 120
    path.write_text(json.dumps(report))
    item["sha256"] = release_record.sha256(path)
    with pytest.raises(ValueError, match="30-minute"):
        release_record.validate(record, root)


def test_pilot_requires_bound_decision_and_production_requires_pilot_results(bundle):
    record, root = bundle
    proof = root / "review.json"
    proof.write_text('{"synthetic_test_only": true}')
    accepted = datetime.now(timezone.utc).isoformat()
    for name in release_record.GATES[:7]:
        record["gates"][name].update(
            status="accepted",
            owner="test-owner",
            reviewer="test-reviewer",
            accepted_at=accepted,
            evidence=[{"path": proof.name, "sha256": release_record.sha256(proof)}],
        )
    record["decision"] = {
        "mode": "pilot",
        "environment_id": "synthetic",
        "rollback_image": "ghcr.io/example/enat@sha256:" + "e" * 64,
        "approved_at": accepted,
        "approvers": {
            role: "synthetic-reviewer" for role in ("clinical", "privacy", "operations")
        },
    }
    release_record.validate(record, root, mode="pilot")
    with pytest.raises(ValueError, match="R8"):
        release_record.validate(record, root, mode="production")
    altered = copy.deepcopy(record)
    altered["gates"]["R1"]["image"] = "different"
    with pytest.raises(ValueError, match="image mismatch"):
        release_record.validate(altered, root, mode="pilot")


def fake_docker(record, fail_service=None):
    calls = []
    old = "sha256:" + "f" * 64

    def execute(command, env):
        calls.append((command, env["ENAT_IMAGE"]))
        if command[:3] == ["docker", "image", "inspect"]:
            if "Config.Labels" in command[-2]:
                return record["source_revision"]
            return record["image_id"]
        if command[:2] == ["docker", "inspect"]:
            return old
        if "ps" in command:
            return "container-" + command[-1]
        if (
            "exec" in command
            and fail_service in command
            and env["ENAT_IMAGE"] == record["image"]
        ):
            raise RuntimeError("synthetic readiness failure")
        return ""

    return execute, calls, old


def test_failed_rollout_restores_changed_services(bundle):
    record, _ = bundle
    execute, calls, old = fake_docker(record, "api-b")
    with pytest.raises(RuntimeError, match="previous services restored"):
        deploy_release.deploy(
            record,
            "staging",
            {"ENAT_IMAGE": record["image"]},
            execute=execute,
            pause=lambda _: None,
        )
    changes = [(command[-1], image) for command, image in calls if "up" in command]
    assert changes == [
        ("api-a", record["image"]),
        ("api-b", record["image"]),
        ("api-b", old),
        ("api-a", old),
    ]
    assert sum("migrate" in command for command, _ in calls) == 1
    assert not any("down" in command for command, _ in calls)


def test_digest_mismatch_stops_before_migration(bundle):
    record, _ = bundle
    execute, calls, _ = fake_docker(record)
    altered = {**record, "image_id": "sha256:" + "0" * 64}
    with pytest.raises(ValueError, match="tested image"):
        deploy_release.deploy(
            altered, "staging", {"ENAT_IMAGE": record["image"]}, execute=execute
        )
    assert not any("migrate" in command for command, _ in calls)


def test_private_environment_files_required(tmp_path):
    path = tmp_path / "api.env"
    path.write_text("SYNTHETIC=true")
    path.chmod(0o644)
    with pytest.raises(ValueError):
        deploy_release.private_file(str(path))
    path.chmod(0o600)
    assert deploy_release.private_file(str(path)) == str(path)


def test_first_pilot_requires_explicit_bootstrap_and_full_fallback(bundle):
    record, _ = bundle
    fallback = "ghcr.io/example/enat@sha256:" + "e" * 64
    old = "sha256:" + "f" * 64
    record["decision"] = {"rollback_image": fallback, "bootstrap": True}
    calls = []

    def execute(command, env):
        calls.append((command, env["ENAT_IMAGE"]))
        if command[:3] == ["docker", "image", "inspect"]:
            if "Config.Labels" in command[-2]:
                return record["source_revision"]
            return old if command[-1] == fallback else record["image_id"]
        if "ps" in command:
            return ""
        if (
            "exec" in command
            and "api-a" in command
            and env["ENAT_IMAGE"] == record["image"]
        ):
            raise RuntimeError("synthetic failure")
        return ""

    env = {"ENAT_IMAGE": record["image"]}
    with pytest.raises(ValueError, match="rollback image"):
        deploy_release.deploy(
            record, "pilot", env, execute=execute, pause=lambda _: None
        )
    assert not any("migrate" in command for command, _ in calls)
    calls.clear()
    with pytest.raises(RuntimeError, match="restored"):
        deploy_release.deploy(
            record, "pilot", env, bootstrap=True, execute=execute, pause=lambda _: None
        )
    restored = [
        command[-1] for command, image in calls if "up" in command and image == old
    ]
    assert restored == list(deploy_release.SERVICES)


def test_failed_compensating_rollback_reports_intervention(bundle):
    record, _ = bundle
    delegate, _, _ = fake_docker(record, "api-b")

    def execute(command, env):
        if "up" in command and env["ENAT_IMAGE"] != record["image"]:
            raise RuntimeError("synthetic rollback failure")
        return delegate(command, env)

    with pytest.raises(RuntimeError, match="operator intervention"):
        deploy_release.deploy(
            record,
            "staging",
            {"ENAT_IMAGE": record["image"]},
            execute=execute,
            pause=lambda _: None,
        )


def test_image_revision_mismatch_stops_before_migration(bundle):
    record, _ = bundle
    execute, calls, _ = fake_docker(record)
    changed = {**record, "source_revision": "0" * 40}
    with pytest.raises(ValueError, match="source label"):
        deploy_release.deploy(
            changed, "staging", {"ENAT_IMAGE": record["image"]}, execute=execute
        )
    assert not any("migrate" in command for command, _ in calls)
