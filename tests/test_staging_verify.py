import json

import httpx
import pytest

from scripts import staging_verify

A = "00000000-0000-4000-8000-000000000001"
B = "00000000-0000-4000-8000-000000000002"
CONFIG = {
    "environment": "staging",
    "environment_id": "synthetic",
    "api_origin": "https://staging.invalid",
    "synthetic_accounts_only": True,
    "user_ids": {"a": A, "b": B},
}
CREDS = [
    {"email": "a@example.invalid", "password": "secret-a"},
    {"email": "b@example.invalid", "password": "secret-b"},
]


def transport(*, leak=False, failure=False):
    revoked = set()
    calls = []

    def handle(request):
        calls.append(request.url.path)
        path = request.url.path
        token = request.headers.get("Authorization", "").removeprefix("Bearer ")
        if path == "/health":
            return httpx.Response(200)
        if path == "/ready":
            return httpx.Response(200)
        if path == "/metrics":
            return httpx.Response(404)
        if path == "/auth/login":
            user = "a" if json.loads(request.content)["email"].startswith("a") else "b"
            return httpx.Response(
                200,
                json={
                    "access_token": "jwt-" + user,
                    "refresh_token": "refresh-" + user,
                    "user_id": A if user == "a" else B,
                },
            )
        if path == "/auth/refresh":
            if "jwt-a" in revoked:
                return httpx.Response(401)
            return httpx.Response(
                200,
                json={
                    "access_token": "jwt-new",
                    "refresh_token": "refresh-new",
                    "user_id": A,
                },
            )
        if not token or token in revoked:
            return httpx.Response(401)
        if path == "/auth/logout":
            revoked.add(token)
            if token == "jwt-new":
                revoked.add("jwt-a")
            return httpx.Response(204)
        if path == "/users/me":
            return httpx.Response(200, json={"id": B if token == "jwt-b" else A})
        if path == "/checkin/start":
            assert request.headers["Idempotency-Key"].startswith("staging-")
            return httpx.Response(200, json={"session_id": A})
        if path.endswith("/state"):
            if failure:
                raise httpx.ConnectError("SECRET-IN-ERROR", request=request)
            return httpx.Response(200 if token != "jwt-b" or leak else 404)
        if path == "/checkin/history":
            return httpx.Response(200, json=[])
        raise AssertionError(path)

    return httpx.MockTransport(handle), calls, revoked


def test_real_auth_journey_and_redacted_report():
    mock, calls, revoked = transport()
    with httpx.Client(base_url=CONFIG["api_origin"], transport=mock) as client:
        report = staging_verify.exercise(client, CONFIG, CREDS)
    assert report["passed"]
    assert {"jwt-a", "jwt-b", "jwt-new"} <= revoked
    assert "/auth/refresh" in calls
    assert "jwt-" not in json.dumps(report)
    assert "secret-" not in json.dumps(report)
    assert "direct_database_and_storage_grants" in report["not_covered"]


@pytest.mark.parametrize("kwargs", [{"leak": True}, {"failure": True}])
def test_isolation_or_network_failure_blocks_and_cleans_sessions(kwargs):
    mock, _, revoked = transport(**kwargs)
    with httpx.Client(base_url=CONFIG["api_origin"], transport=mock) as client:
        report = staging_verify.exercise(client, CONFIG, CREDS)
    assert not report["passed"]
    assert {"jwt-a", "jwt-b"} <= revoked
    assert "SECRET-IN-ERROR" not in json.dumps(report)


@pytest.mark.parametrize(
    "change,origin",
    [
        ({"environment": "production"}, CONFIG["api_origin"]),
        ({}, "https://other.invalid"),
        ({"synthetic_accounts_only": False}, CONFIG["api_origin"]),
        ({"api_origin": "http://staging.invalid"}, "http://staging.invalid"),
        ({"user_ids": {"a": A, "b": A}}, CONFIG["api_origin"]),
    ],
)
def test_guard_refuses_wrong_target_before_network(tmp_path, change, origin):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({**CONFIG, **change}))
    with pytest.raises(ValueError):
        staging_verify.configuration(path, origin, {})
