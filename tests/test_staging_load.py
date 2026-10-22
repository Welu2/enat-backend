import json
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from scripts import staging_load

USER = "00000000-0000-4000-8000-000000000001"
ACCOUNTS = [
    {
        "user_id": USER,
        "access_token": "private-synthetic-jwt",
        "expires_at": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
    }
]


@pytest.mark.asyncio
async def test_all_scheduled_requests_and_failures_are_counted():
    counter = 0

    def handle(request):
        nonlocal counter
        counter += 1
        if counter == 1:
            return httpx.Response(200, json={"id": USER})
        if counter == 2:
            return httpx.Response(503, text="private-payload")
        if counter == 3:
            raise httpx.ConnectError("private-token", request=request)
        return httpx.Response(200, json=[])

    async with httpx.AsyncClient(
        base_url="https://staging.invalid", transport=httpx.MockTransport(handle)
    ) as client:
        report = await staging_load.exercise(client, ACCOUNTS, 100, 0.04)
    assert report["scheduled_requests"] == report["measured_requests"] == 4
    assert report["errors"] == {"http_503": 1, "transport": 1}
    assert report["error_rate"] == 0.5
    assert not report["passed"]
    assert "private" not in json.dumps(report)


@pytest.mark.asyncio
async def test_wrong_user_blocks_before_load():
    calls = []

    def handle(request):
        calls.append(request)
        return httpx.Response(200, json={"id": "wrong"})

    async with httpx.AsyncClient(
        base_url="https://staging.invalid", transport=httpx.MockTransport(handle)
    ) as client:
        with pytest.raises(ValueError, match="identity"):
            await staging_load.exercise(client, ACCOUNTS, 100, 0.04)
    assert len(calls) == 1


def test_quota_and_private_config_guards(tmp_path):
    path = tmp_path / "tokens.json"
    config = {
        "environment": "staging",
        "api_origin": "https://staging.invalid",
        "synthetic_accounts_only": True,
        "environment_id": "synthetic",
        "auth_kind": "supabase",
        "accounts": ACCOUNTS,
    }
    path.write_text(json.dumps(config))
    path.chmod(0o600)
    assert staging_load.configuration(path, config["api_origin"], 1, 60)
    with pytest.raises(ValueError, match="quotas"):
        staging_load.configuration(path, config["api_origin"], 50, 60)
    path.chmod(0o644)
    with pytest.raises(ValueError, match="private"):
        staging_load.configuration(path, config["api_origin"], 1, 60)


@pytest.mark.asyncio
async def test_success_status_with_invalid_body_is_counted_as_failure():
    calls = 0

    def handle(request):
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(200, json={"id": USER})
        return httpx.Response(200, text="invalid response body")

    async with httpx.AsyncClient(
        base_url="https://staging.invalid", transport=httpx.MockTransport(handle)
    ) as client:
        report = await staging_load.exercise(client, ACCOUNTS, 100, 0.02)
    assert report["errors"] == {"invalid_response": 2}
    assert report["error_rate"] == 1
    assert not report["passed"]
