"""Bounded constant-rate staging reads with real supplied authentication tokens.

Use synthetic staging identities and an agreed provider/Auth quota. No token or
response body is retained. This is not voice, write or failure-injection coverage.
"""

import argparse
import asyncio
import json
import math
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from uuid import UUID

import httpx


def configuration(path, origin, rps, seconds):
    config = json.loads(path.read_text())
    url = urlsplit(origin)
    if (
        config["environment"] != "staging"
        or config["api_origin"] != origin
        or config["synthetic_accounts_only"] is not True
        or not config["environment_id"].strip()
        or url.scheme != "https"
        or not url.hostname
        or url.username
        or url.password
        or url.path
        or url.query
        or url.fragment
    ):
        raise ValueError("Explicit HTTPS staging target required")
    if not (math.isfinite(rps) and 0.1 <= rps <= 50 and 10 <= seconds <= 1800):
        raise ValueError("Rate/duration outside bound")
    if path.stat().st_mode & 0o077:
        raise ValueError("Token configuration must be private (0600)")
    accounts = config["accounts"]
    if not accounts or len(accounts) > 1000:
        raise ValueError("Supply 1–1000 synthetic identities")
    ids, tokens = set(), set()
    kind = config["auth_kind"]
    if kind not in ("supabase", "opaque"):
        raise ValueError("Explicit auth kind required")
    for account in accounts:
        user_id = str(UUID(account["user_id"]))
        token = account["access_token"]
        expiry = datetime.fromisoformat(account["expires_at"].replace("Z", "+00:00"))
        if (
            not isinstance(token, str)
            or not 1 <= len(token) <= 16000
            or user_id in ids
            or token in tokens
            or token.startswith("enat_") != (kind == "opaque")
            or expiry.tzinfo is None
            or expiry.timestamp() < time.time() + seconds + 60
        ):
            raise ValueError("Duplicate, invalid or expiring test credentials")
        ids.add(user_id)
        tokens.add(token)
    # Leave headroom under the app's 120 authenticated requests/minute per user.
    if rps * 60 / len(accounts) > 100:
        raise ValueError("Add identities or reduce rate to respect user quotas")
    return config


async def exercise(client, accounts, rps, seconds, *, concurrency=100):
    # Validate identity before load, failing without retaining returned profiles.
    for account in accounts:
        response = await client.get(
            "/users/me", headers={"Authorization": "Bearer " + account["access_token"]}
        )
        if (
            response.status_code != 200
            or response.json().get("id") != account["user_id"]
        ):
            raise ValueError("Staging identity preflight failed")
    total = math.ceil(rps * seconds)
    errors = Counter()
    latencies, delays = [], []
    pending = set()
    started = time.monotonic()

    async def request(index, scheduled):
        delays.append(max(0, time.monotonic() - scheduled))
        account = accounts[index % len(accounts)]
        path = "/users/me" if index % 5 == 0 else "/checkin/history?limit=1"
        try:
            response = await client.get(
                path, headers={"Authorization": "Bearer " + account["access_token"]}
            )
            if response.status_code != 200:
                errors["http_" + str(response.status_code)] += 1
            else:
                try:
                    payload = response.json()
                    valid = (
                        isinstance(payload, list)
                        if path.startswith("/checkin/")
                        else isinstance(payload, dict)
                        and payload.get("id") == account["user_id"]
                    )
                    if not valid:
                        errors["invalid_response"] += 1
                except ValueError:
                    errors["invalid_response"] += 1
        except httpx.HTTPError:
            errors["transport"] += 1
        finally:
            latencies.append(max(0, time.monotonic() - scheduled))

    for index in range(total):
        scheduled = started + index / rps
        await asyncio.sleep(max(0, scheduled - time.monotonic()))
        if len(pending) >= concurrency:
            errors["generator_capacity"] += 1
            delay = max(0, time.monotonic() - scheduled)
            latencies.append(delay)
            delays.append(delay)
            continue
        task = asyncio.create_task(request(index, scheduled))
        pending.add(task)
        task.add_done_callback(pending.discard)
    if pending:
        await asyncio.gather(*pending)

    def percentile(values, fraction):
        return sorted(values)[
            min(len(values) - 1, math.ceil(len(values) * fraction) - 1)
        ]

    p95, p99 = percentile(latencies, 0.95), percentile(latencies, 0.99)
    error_rate = sum(errors.values()) / total
    return {
        "scheduled_requests": total,
        "measured_requests": len(latencies),
        "target_rps": rps,
        "duration_seconds": seconds,
        "p95_seconds": p95,
        "p99_seconds": p99,
        "scheduler_p99_seconds": percentile(delays, 0.99),
        "errors": dict(errors),
        "error_rate": error_rate,
        "passed": p95 <= 0.5 and p99 <= 1 and error_rate < 0.01,
        "scope": "80_percent_history_20_percent_profile_reads",
        "voice_tested": False,
        "writes_tested": False,
        "fault_injection": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--confirm-origin", required=True)
    parser.add_argument("--rps", type=float, default=1)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        config = configuration(args.config, args.confirm_origin, args.rps, args.seconds)
        if args.output.exists():
            raise ValueError("Use a new report path")

        async def run():
            async with httpx.AsyncClient(
                base_url=config["api_origin"],
                timeout=10,
                follow_redirects=False,
                trust_env=False,
                limits=httpx.Limits(max_connections=100),
            ) as client:
                return await exercise(
                    client, config["accounts"], args.rps, args.seconds
                )

        report = asyncio.run(run())
        report.update(
            schema_version=1,
            generated_at=datetime.now(timezone.utc).isoformat(),
            environment_id=config["environment_id"],
            auth_kind=config["auth_kind"],
        )
        with args.output.open("x") as stream:
            json.dump(report, stream, indent=2)
            stream.write("\n")
    except (ValueError, KeyError, TypeError, OSError, httpx.HTTPError):
        raise SystemExit(
            "Staging load refused or preflight failed; verify target, identities, quota and output."
        ) from None
    print("Staging read load " + ("passed" if report["passed"] else "failed"))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
