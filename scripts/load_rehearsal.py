"""Synthetic two-process capacity/restart rehearsal, only inside test_database.py."""

import asyncio
import hashlib
import json
import os
import platform
import socket
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from uuid import uuid4

import httpx
import psycopg


def port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


async def exercise(env, tokens, reminders, duration, directory, backend=None):
    ports = backend.ports if backend else [port(), port()]
    urls = backend.urls if backend else [f"http://127.0.0.1:{p}" for p in ports]
    processes, logs = [], []

    def launch(index):
        output = open(Path(directory) / f"api-{index}.log", "ab")
        logs.append(output)
        return subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(ports[index]),
                "--proxy-headers",
                "--forwarded-allow-ips",
                "127.0.0.1",
                "--limit-concurrency",
                "100",
                "--no-access-log",
            ],
            env=env,
            stdout=output,
            stderr=subprocess.STDOUT,
        )

    if backend is None:
        processes.extend(launch(i) for i in range(2))
    outage_seconds = 150 if backend and duration >= 450 else min(3, duration / 6)
    latencies, errors, healthy = [], Counter(), [False, False]
    request_times, scheduling_delays, slow_windows = [], [], []
    stopped, restarted, stop_probe = False, False, False
    async with httpx.AsyncClient(
        timeout=3,
        trust_env=False,
        headers={"Host": "localhost"} if backend else {},
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=100),
    ) as client:

        async def probe():
            async def check(index):
                try:
                    healthy[index] = (
                        await client.get(
                            urls[index] + "/ready",
                            timeout=httpx.Timeout(1.5, connect=0.25),
                        )
                    ).status_code == 200
                except httpx.HTTPError:
                    healthy[index] = False

            while not stop_probe:
                # A failed replica must not delay health checks of the survivor.
                await asyncio.gather(*(check(i) for i in range(2)))
                await asyncio.sleep(0.25)

        monitor = asyncio.create_task(probe())
        fault = None
        try:
            for _ in range(100):
                if all(healthy):
                    break
                await asyncio.sleep(0.1)
            if not all(healthy):
                raise RuntimeError("Both APIs must become schema-ready")
            started = time.monotonic()
            pending = set()

            async def inject_failure():
                nonlocal stopped, restarted
                await asyncio.sleep(duration / 3)
                if backend:
                    await asyncio.to_thread(backend.kill)
                else:
                    processes[0].kill()
                    await asyncio.to_thread(processes[0].wait, timeout=5)
                stopped = True
                await asyncio.sleep(
                    max(0, started + duration / 3 + outage_seconds - time.monotonic())
                )
                if backend:
                    await asyncio.to_thread(backend.restart)
                else:
                    processes[0] = await asyncio.to_thread(launch, 0)
                restarted = True

            # Docker operations must not pause scheduling and turn constant-rate
            # traffic into a catch-up burst at the surviving API.
            fault = asyncio.create_task(inject_failure())

            async def request(number, planned):
                dispatched = time.monotonic()
                scheduling_delays.append(dispatched - planned)
                candidates = [i for i in range(2) if healthy[i]]
                if not candidates:
                    errors["no_ready_backend"] += 1
                    return
                index = candidates[number % len(candidates)]
                user = number % len(tokens)
                headers = {
                    "Authorization": "Bearer " + tokens[user],
                    "X-Forwarded-For": f"10.20.{user // 250}.{user % 250 + 1}",
                }
                kind = number % 10
                path = (
                    "/checkin/history?limit=50"
                    if kind < 8
                    else "/users/me"
                    if kind == 8
                    else f"/notifications/{reminders[user]}/dismiss"
                )
                try:
                    response = await client.request(
                        "POST" if kind == 9 else "GET",
                        urls[index] + path,
                        headers=headers,
                    )
                    if response.status_code != 200:
                        errors[str(response.status_code)] += 1
                except httpx.HTTPError:
                    errors["transport"] += 1
                latencies.append(time.monotonic() - planned)
                request_times.append(time.monotonic() - dispatched)
                if latencies[-1] > 1 and len(slow_windows) < 30:
                    slow_windows.append(
                        {
                            "scheduled_second": round(planned - started, 2),
                            "scheduler_delay": round(dispatched - planned, 3),
                            "request_seconds": round(request_times[-1], 3),
                        }
                    )

            for number in range(duration * 50):
                planned = started + number / 50
                await asyncio.sleep(max(0, planned - time.monotonic()))
                if len(pending) >= 200:
                    errors["overload"] += 1
                    continue
                task = asyncio.create_task(request(number, planned))
                pending.add(task)
                task.add_done_callback(pending.discard)
                if number and number % 3000 == 0:
                    print(
                        f"Load: {number} scheduled, {sum(errors.values())} errors, max recent scheduling lag {max(scheduling_delays[-3000:], default=0):.3f}s",
                        flush=True,
                    )
            await asyncio.gather(*pending)
            await fault
            values = sorted(latencies)
            request_times.sort()
            scheduling_delays.sort()
            metrics = []
            for index in range(2):
                response = await client.get(
                    urls[index] + "/metrics",
                    headers={"Authorization": "Bearer " + env["METRICS_TOKEN"]},
                )
                metrics.append(response.text)
            destination = Path("artifacts/operations")
            destination.mkdir(parents=True, exist_ok=True)
            prefix = "load-compose" if backend else "load"
            (destination / (prefix + "-server-metrics.txt")).write_text(
                "\n".join(metrics)
            )
            total = duration * 50
            return {
                "duration_seconds": duration,
                "scheduled_requests": total,
                "completed_requests": len(values),
                "target_rps": 50,
                "p95_seconds": values[int(len(values) * 0.95)],
                "p99_seconds": values[int(len(values) * 0.99)],
                "request_p99_seconds": request_times[int(len(request_times) * 0.99)],
                "scheduler_p99_seconds": scheduling_delays[
                    int(len(scheduling_delays) * 0.99)
                ],
                "slow_samples": slow_windows,
                "errors": dict(errors),
                "error_rate": sum(errors.values()) / total,
                "api_processes": 2,
                "execution": "compose" if backend else "host processes",
                "outage_seconds": outage_seconds,
                "api_pool_per_process": 10,
                "synthetic_users": 1000,
                "history_rows": 100000,
                "instance_killed": stopped,
                "instance_restarted": restarted,
                "both_ready_after_recovery": all(healthy),
                "python": platform.python_version(),
                "platform": platform.platform(),
                "logical_cpus": os.cpu_count(),
                "provider_calls": 0,
                "auth": "real opaque sessions, restricted DB role; no external Auth calls",
                "passed": values[int(len(values) * 0.95)] <= 0.5
                and values[int(len(values) * 0.99)] <= 1
                and sum(errors.values()) / total < 0.01
                and all(healthy),
            }
        finally:
            if fault is not None:
                # Join any in-flight Docker operation before removing services.
                await asyncio.gather(fault, return_exceptions=True)
            stop_probe = True
            await monitor
            for process in processes:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=35)
            for output in logs:
                output.close()


def main():
    dsn = os.environ.get("ENAT_TEST_ADMIN_DSN", "")
    if (
        not psycopg.conninfo.conninfo_to_dict(dsn)
        .get("host", "")
        .startswith("/tmp/enat-security-")
    ):
        raise SystemExit("Only disposable test_database.py clusters are supported")
    users = [uuid4() for _ in range(1000)]
    tokens = ["enat_" + uuid4().hex for _ in users]
    reminders = [uuid4() for _ in users]
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO users(id) VALUES(%s)", [(u,) for u in users]
            )
            cursor.executemany(
                "INSERT INTO app_sessions(token_hash,source_hash,user_id,expires_at) VALUES(%s,%s,%s,now()+interval '2 hours')",
                [
                    (hashlib.sha256(t.encode()).hexdigest(), uuid4().hex, u)
                    for t, u in zip(tokens, users, strict=True)
                ],
            )
            cursor.executemany(
                "INSERT INTO reminders(id,user_id,type,message,due_at) VALUES(%s,%s,'test','synthetic',now())",
                list(zip(reminders, users, strict=True)),
            )
        conn.execute(
            "INSERT INTO check_ins(user_id,timestamp) SELECT u,now()-make_interval(secs=>n) FROM unnest(%s::uuid[]) u CROSS JOIN generate_series(1,100) n",
            (users,),
        )
        conn.execute("ANALYZE")
    env = dict(
        os.environ,
        ENVIRONMENT="test",
        PROCESS_ROLE="api",
        DATABASE_URL=os.environ["ENAT_TEST_APP_DSN"],
        WORKER_DATABASE_URL="",
        ENABLE_REQUEST_LIMITS="true",
        RATE_LIMIT_SECRET="synthetic-load-limit-secret-32-characters",
        METRICS_TOKEN="synthetic-load-metrics-token-32-characters",
        OTLP_ENDPOINT="",
        SUPABASE_URL="https://example.supabase.co",
        SUPABASE_SERVICE_ROLE_KEY="synthetic-placeholder",
        ADDIS_API_KEY="synthetic-placeholder",
        TRUSTED_HOSTS="127.0.0.1",
        ENABLE_DEV_ROUTES="false",
    )
    with tempfile.TemporaryDirectory(prefix="enat-load-") as directory:
        duration = int(os.environ.get("ENAT_LOAD_SECONDS", "1800"))
        if duration < 10 or duration > 3600:
            raise SystemExit("Load duration must be between 10 and 3600 seconds")
        backend = None
        if os.environ.get("ENAT_LOAD_COMPOSE") == "1":
            from compose_rehearsal import ComposeStack

            backend = ComposeStack(env, directory)
        try:
            if backend:
                backend.start()
            result = asyncio.run(
                exercise(env, tokens, reminders, duration, directory, backend)
            )
            if backend:
                result["deployment"] = backend.finish(require_alert=duration >= 450)
        finally:
            if backend:
                backend.close()
    destination = Path("artifacts/operations")
    destination.mkdir(parents=True, exist_ok=True)
    prefix = "load-compose" if backend else "load"
    previous = destination / (prefix + ".json")
    if previous.exists():
        (
            destination / (prefix + "-previous-" + str(time.time_ns()) + ".json")
        ).write_text(previous.read_text())
    previous.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
