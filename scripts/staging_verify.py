"""Opt-in live checks using two designated synthetic staging accounts.

No .env loading, admin credentials, response bodies or tokens in reports.
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from uuid import UUID, uuid4

import httpx


def configuration(path, confirmed_origin, environ):
    config = json.loads(path.read_text())
    origin = config["api_origin"]
    url = urlsplit(origin)
    if (
        config.get("environment") != "staging"
        or config.get("synthetic_accounts_only") is not True
        or not config.get("environment_id", "").strip()
        or origin != confirmed_origin
        or url.scheme != "https"
        or not url.hostname
        or url.username
        or url.password
        or url.path
        or url.query
        or url.fragment
    ):
        raise ValueError(
            "Explicit HTTPS staging origin and synthetic fixtures required"
        )
    users = [str(UUID(config["user_ids"][name])) for name in ("a", "b")]
    if users[0] == users[1]:
        raise ValueError("Two distinct staging identities required")
    credentials = []
    for suffix in ("A", "B"):
        email = environ[f"ENAT_STAGING_EMAIL_{suffix}"]
        password = environ[f"ENAT_STAGING_PASSWORD_{suffix}"]
        if not email or not password:
            raise ValueError("Staging credentials missing")
        credentials.append({"email": email, "password": password})
    if credentials[0]["email"] == credentials[1]["email"]:
        raise ValueError("Two distinct accounts required")
    return config, credentials


class CheckFailed(Exception):
    pass


class Checks:
    def __init__(self, client):
        self.client = client
        self.results = []

    def request(
        self, name, method, path, expected, *, token=None, extra_headers=None, **kwargs
    ):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        headers.update(extra_headers or {})
        try:
            response = self.client.request(method, path, headers=headers, **kwargs)
            passed = response.status_code == expected
            self.results.append(
                {"check": name, "passed": passed, "status": response.status_code}
            )
        except httpx.HTTPError:
            self.results.append({"check": name, "passed": False, "status": None})
            raise CheckFailed from None
        if not passed:
            raise CheckFailed
        return response

    def assert_value(self, name, condition):
        self.results.append({"check": name, "passed": bool(condition)})
        if not condition:
            raise CheckFailed


def exercise(client, config, credentials):
    checks = Checks(client)
    issued = []
    cleanup_ok = True
    try:
        checks.request("liveness", "GET", "/health", 200)
        checks.request("readiness", "GET", "/ready", 200)
        checks.request("metrics_private", "GET", "/metrics", 404)
        checks.request("profile_requires_auth", "GET", "/users/me", 401)
        sessions = []
        for index, label in enumerate(("a", "b")):
            response = checks.request(
                f"login_{label}", "POST", "/auth/login", 200, json=credentials[index]
            ).json()
            token = response["access_token"]
            checks.assert_value(
                "token_shape", isinstance(token, str) and len(token) > 0
            )
            issued.append(token)
            checks.assert_value(
                f"identity_{label}",
                response["user_id"] == config["user_ids"][label]
                and not token.startswith("enat_")
                and bool(response.get("refresh_token")),
            )
            profile = checks.request(
                f"profile_{label}", "GET", "/users/me", 200, token=token
            ).json()
            checks.assert_value(
                f"profile_owner_{label}", profile["id"] == config["user_ids"][label]
            )
            sessions.append(response)
        a, b = sessions
        # No voice calls or clinical finalizations: create only an empty draft.
        draft = checks.request(
            "start_draft",
            "POST",
            "/checkin/start",
            200,
            token=a["access_token"],
            extra_headers={"Idempotency-Key": "staging-" + uuid4().hex},
        ).json()
        draft_id = str(UUID(draft["session_id"]))
        checks.request(
            "own_draft",
            "GET",
            f"/checkin/{draft_id}/state",
            200,
            token=a["access_token"],
        )
        checks.request(
            "cross_user_draft",
            "GET",
            f"/checkin/{draft_id}/state",
            404,
            token=b["access_token"],
        )
        checks.request(
            "bounded_history",
            "GET",
            "/checkin/history?limit=1",
            200,
            token=a["access_token"],
        )
        fresh = checks.request(
            "refresh",
            "POST",
            "/auth/refresh",
            200,
            json={"refresh_token": a["refresh_token"]},
        ).json()
        checks.assert_value(
            "refreshed_token_shape", isinstance(fresh["access_token"], str)
        )
        issued.append(fresh["access_token"])
        checks.assert_value(
            "refresh_owner", fresh["user_id"] == config["user_ids"]["a"]
        )
        checks.request(
            "logout", "POST", "/auth/logout", 204, token=fresh["access_token"]
        )
        checks.request(
            "logged_out_token_rejected",
            "GET",
            "/users/me",
            401,
            token=fresh["access_token"],
        )
        checks.request(
            "old_family_token_rejected",
            "GET",
            "/users/me",
            401,
            token=a["access_token"],
        )
        checks.request(
            "revoked_refresh_rejected",
            "POST",
            "/auth/refresh",
            401,
            json={"refresh_token": fresh["refresh_token"]},
        )
        checks.request(
            "other_account_unaffected", "GET", "/users/me", 200, token=b["access_token"]
        )
    except (CheckFailed, KeyError, ValueError, TypeError):
        checks.results.append({"check": "journey_completed", "passed": False})
    finally:
        for token in dict.fromkeys(issued):
            try:
                response = client.post(
                    "/auth/logout", headers={"Authorization": f"Bearer {token}"}
                )
                cleanup_ok &= response.status_code in (204, 401)
            except httpx.HTTPError:
                cleanup_ok = False
        checks.results.append({"check": "session_cleanup", "passed": cleanup_ok})
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "environment": "staging",
        "environment_id": config["environment_id"],
        "scope": "live_auth_and_draft_isolation",
        "passed": all(item["passed"] for item in checks.results),
        "checks": checks.results,
        "not_covered": [
            "email_confirmation_and_recovery_delivery",
            "signing_key_rotation",
            "banned_accounts",
            "telegram",
            "direct_database_and_storage_grants",
            "clinical_quality",
            "frontend",
            "capacity",
            "restore",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--confirm-origin", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        config, credentials = configuration(
            args.config, args.confirm_origin, os.environ
        )
        if args.output.exists():
            raise ValueError("Use a new report path")
        with httpx.Client(
            base_url=config["api_origin"],
            timeout=30,
            follow_redirects=False,
            trust_env=False,
        ) as client:
            report = exercise(client, config, credentials)
        with args.output.open("x") as stream:
            json.dump(report, stream, indent=2)
            stream.write("\n")
    except (ValueError, KeyError, TypeError, OSError):
        raise SystemExit(
            "Staging verification refused: check explicit configuration and output path."
        ) from None
    print(
        "Staging checks "
        + ("passed" if report["passed"] else "failed")
        + "; no response bodies retained."
    )
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
