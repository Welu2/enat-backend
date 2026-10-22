"""Host-side digest promotion with readiness checks and compensating rollback.

Run from the matching reviewed checkout on the provisioned Docker host.
TLS ingress must route only to ready APIs. Cloud configuration is not inferred.
"""

import argparse
import fcntl
import json
import os

# Fixed Docker/Git executables, argument arrays only.
import subprocess  # nosec B404
import time
from pathlib import Path

if __package__:
    from .release_record import ROOT, validate
else:
    from release_record import ROOT, validate

SERVICES = ("api-a", "api-b", "worker", "scheduler")


def run(command, env):
    # Internal command lists, with no shell interpolation.
    result = subprocess.run(  # nosec B603
        command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=300
    )
    if result.returncode:
        raise RuntimeError("Deployment command failed; inspect protected host logs")
    return result.stdout.strip()


def private_file(value):
    path = Path(value)
    if not path.is_absolute() or not path.is_file() or path.stat().st_mode & 0o077:
        raise ValueError("Use absolute private environment files (0600)")
    return str(path)


def deploy(record, mode, env, *, bootstrap=False, execute=run, pause=time.sleep):
    compose = ["docker", "compose", "-f", str(ROOT / "deploy/compose.yaml")]
    execute(["docker", "pull", record["image"]], env)
    actual = execute(
        ["docker", "image", "inspect", "--format", "{{.Id}}", record["image"]], env
    )
    if actual != record["image_id"]:
        raise ValueError("Registry digest does not match tested image ID")
    revision = execute(
        [
            "docker",
            "image",
            "inspect",
            "--format",
            '{{index .Config.Labels "org.opencontainers.image.revision"}}',
            record["image"],
        ],
        env,
    )
    if revision != record["source_revision"]:
        raise ValueError("Image source label does not match release revision")
    execute([*compose, "config", "--quiet"], env)
    previous = {}
    bootstrapped = False
    for service in SERVICES:
        container = execute([*compose, "ps", "-q", service], env)
        if container:
            previous[service] = execute(
                ["docker", "inspect", "--format", "{{.Image}}", container], env
            )
    if mode != "staging":
        rollback = record["decision"]["rollback_image"]
        execute(["docker", "pull", rollback], env)
        rollback_id = execute(
            ["docker", "image", "inspect", "--format", "{{.Id}}", rollback], env
        )
        if not previous and bootstrap and record["decision"].get("bootstrap") is True:
            # A first pilot still needs a separately tested compatible fallback.
            previous = dict.fromkeys(SERVICES, rollback_id)
            bootstrapped = True
        if len(previous) != len(SERVICES) or set(previous.values()) != {rollback_id}:
            raise ValueError("Running services do not match approved rollback image")

    def ready(service, service_env):
        probe = "ready" if service.startswith("api-") else "worker"
        for _ in range(45):
            try:
                execute(
                    [
                        *compose,
                        "exec",
                        "-T",
                        service,
                        "python",
                        "-m",
                        "app.probes",
                        probe,
                    ],
                    service_env,
                )
                return
            except RuntimeError:
                pause(2)
        raise RuntimeError("Service did not become ready")

    # Schema changes must be additive and compatible with the rollback image.
    execute([*compose, "--profile", "tools", "run", "--rm", "migrate"], env)
    changed = []
    try:
        for service in SERVICES:
            changed.append(service)
            execute([*compose, "up", "-d", "--no-deps", service], env)
            ready(service, env)
    except (RuntimeError, subprocess.TimeoutExpired):
        rollback_failed = False
        for service in SERVICES if bootstrapped else reversed(changed):
            try:
                if service in previous:
                    rollback_env = {**env, "ENAT_IMAGE": previous[service]}
                    execute([*compose, "up", "-d", "--no-deps", service], rollback_env)
                    ready(service, rollback_env)
                else:
                    execute([*compose, "stop", service], env)
            except (RuntimeError, subprocess.TimeoutExpired):
                rollback_failed = True
        if rollback_failed:
            raise RuntimeError(
                "Deployment and rollback failed; operator intervention required"
            ) from None
        raise RuntimeError(
            "Deployment failed; previous services restored; additive schema retained"
        ) from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument(
        "--mode", choices=("staging", "pilot", "production"), required=True
    )
    parser.add_argument("--environment-id", required=True)
    parser.add_argument(
        "--target", type=Path, required=True, help="Provisioned host target descriptor"
    )
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="First pilot only; requires explicit decision.bootstrap",
    )
    parser.add_argument(
        "--apply", action="store_true", help="Without this, validate only"
    )
    args = parser.parse_args()
    try:
        record = validate(
            json.loads(args.record.read_text()), args.record.parent, mode=args.mode
        )
        if (
            args.mode != "staging"
            and record["decision"]["environment_id"] != args.environment_id
        ):
            raise ValueError("Approved target does not match")
        target = json.loads(args.target.read_text())
        expected_environment = "staging" if args.mode == "staging" else "production"
        if (
            target["environment_id"] != args.environment_id
            or target["environment"] != expected_environment
        ):
            raise ValueError("Provisioned host target mismatch")
        if args.bootstrap and args.mode != "pilot":
            raise ValueError("Bootstrap is only for first pilot")
        env = {
            **os.environ,
            "DEPLOYMENT_ENV": "staging" if args.mode == "staging" else "production",
            "ENAT_IMAGE": record["image"],
        }
        for key in ("API_ENV_FILE", "WORKER_ENV_FILE", "MIGRATION_ENV_FILE"):
            env[key] = private_file(target[key.lower()])
        env.pop("COMPOSE_PROJECT_NAME", None)
        env.pop("COMPOSE_FILE", None)
        if run(["git", "rev-parse", "HEAD"], env) != record["source_revision"]:
            raise ValueError("Checkout must match release revision")
        if run(["git", "status", "--porcelain", "--untracked-files=normal"], env):
            raise ValueError("Deployment checkout must be clean")
        if not args.apply:
            print("Preflight passed; use --apply on the configured deployment host.")
            return
        lock_path = ROOT / ".cache/deployment.lock"
        lock_path.parent.mkdir(exist_ok=True)
        with lock_path.open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            deploy(record, args.mode, env, bootstrap=args.bootstrap)
    except (
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
        OSError,
        subprocess.TimeoutExpired,
    ):
        raise SystemExit(
            "Deployment refused: verify record, checkout, private configuration and host lock."
        ) from None
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from None
    print("Digest deployed; all four services passed readiness checks.")


if __name__ == "__main__":
    main()
