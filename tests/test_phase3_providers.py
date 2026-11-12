import asyncio
from contextlib import asynccontextmanager
from copy import deepcopy
from time import monotonic
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import httpx
import pytest

from app.config import get_settings
from app.core.errors import ProviderUnavailable
from app.services import provider_runtime as runtime
from app.services.addis_ai import AddisAIClient
from app.services.checkin_session import CheckInSessionService


@asynccontextmanager
async def provider(monkeypatch, handler, **overrides):
    settings = get_settings().model_copy(update=overrides)
    monkeypatch.setattr(runtime, "get_settings", lambda: settings)
    admission = Mock(return_value=None)
    monkeypatch.setattr("app.core.limits._admit_provider", admission)
    client = runtime.ProviderRuntime(settings, transport=httpx.MockTransport(handler))
    loop = asyncio.get_running_loop()
    runtime._runtimes[loop] = client
    try:
        yield client, admission
    finally:
        runtime._runtimes.pop(loop, None)
        await client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,attempts", [(429, 2), (503, 2), (500, 1), (401, 1), (302, 1)]
)
async def test_only_selected_transient_responses_retry_and_every_attempt_is_charged(
    monkeypatch, status, attempts
):
    calls = []

    def respond(request):
        calls.append(request)
        return httpx.Response(status, json={"error": "private"})

    async with provider(monkeypatch, respond) as (client, admission):
        with pytest.raises(ProviderUnavailable):
            await client.request("/test", json={})
        assert len(calls) == admission.call_count == attempts


@pytest.mark.asyncio
async def test_ambiguous_read_timeout_is_not_retried(monkeypatch):
    def timeout(request):
        raise httpx.ReadTimeout("private provider error")

    async with provider(monkeypatch, timeout) as (client, admission):
        with pytest.raises(ProviderUnavailable):
            await client.request("/test")
        assert admission.call_count == 1


@pytest.mark.asyncio
async def test_long_retry_after_is_not_ignored(monkeypatch):
    async with provider(
        monkeypatch, lambda _: httpx.Response(429, headers={"Retry-After": "60"})
    ) as (client, admission):
        with pytest.raises(ProviderUnavailable):
            await client.request("/test")
        assert admission.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload", [[], None, {"data": []}, {"data": {"text": 4}}, {"text": "x" * 8001}]
)
async def test_malformed_asr_is_recoverable(monkeypatch, payload):
    async with provider(monkeypatch, lambda _: httpx.Response(200, json=payload)):
        with pytest.raises(ProviderUnavailable):
            await AddisAIClient().transcribe(b"audio", "x.wav", "audio/wav")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "content_type,body",
    [
        ("audio/mpeg", b'{"error":"private"}'),
        ("application/json", b'{"audio_base64":"not base64"}'),
        ("application/json", b"[]"),
    ],
)
async def test_invalid_audio_cannot_be_successful_audio(
    monkeypatch, content_type, body
):
    async with provider(
        monkeypatch,
        lambda _: httpx.Response(
            200, headers={"content-type": content_type}, content=body
        ),
    ):
        with pytest.raises(ProviderUnavailable):
            await AddisAIClient().synthesize_speech("test")


@pytest.mark.asyncio
async def test_provider_response_body_bound(monkeypatch):
    async with provider(
        monkeypatch, lambda _: httpx.Response(200, content=b"x" * 101)
    ) as (client, _):
        with pytest.raises(ProviderUnavailable, match="bound"):
            await client.request("/test", max_bytes=100)


@pytest.mark.asyncio
async def test_compressed_provider_response_is_decoded_once(monkeypatch):
    import gzip

    def response(_):
        return httpx.Response(
            200,
            headers={"content-type": "application/json", "content-encoding": "gzip"},
            content=gzip.compress(b'{"text":"test"}'),
        )

    async with provider(monkeypatch, response):
        assert (
            await AddisAIClient().transcribe(b"audio", "x.wav", "audio/wav") == "test"
        )


@pytest.mark.asyncio
async def test_asr_and_extraction_share_one_total_deadline_and_preserve_draft(
    monkeypatch,
):
    calls = []

    async def delayed(request):
        calls.append(request.url.path)
        await asyncio.sleep(0.2)
        return httpx.Response(200, json={"text": "test"})

    service = CheckInSessionService()
    state = {
        "version": 0,
        "pending_items": [],
        "current_stage": "symptoms",
        "draft_data": {"food_log": [{"raw_text": "saved"}]},
    }
    before = deepcopy(state)
    monkeypatch.setattr(service, "_get_active_session", Mock(return_value=state))
    update = Mock()
    monkeypatch.setattr(service.sessions, "update", update)
    async with provider(monkeypatch, delayed, provider_operation_seconds=0.3):
        start = monotonic()
        with pytest.raises(ProviderUnavailable):
            await service.respond(
                uuid4(), uuid4(), b"audio", "x.wav", "audio/wav", expected_version=0
            )
        assert monotonic() - start < 0.9
        assert calls == ["/api/v2/stt", "/api/v1/chat_generate"]
    update.assert_not_called()
    assert state == before


@pytest.mark.asyncio
async def test_circuit_opens_and_single_probe_recovers(monkeypatch):
    status = 500
    async with provider(
        monkeypatch, lambda _: httpx.Response(status, json={"text": "ok"})
    ) as (client, admission):
        for _ in range(3):
            with pytest.raises(ProviderUnavailable):
                await client.request("/test")
        with pytest.raises(ProviderUnavailable, match="circuit"):
            await client.request("/test")
        assert admission.call_count == 3
        status = 200
        client.open_until = 0
        assert (await client.request("/test")).json() == {"text": "ok"}
        assert client.failures == 0


@pytest.mark.asyncio
async def test_operation_attempt_budget_bounds_retry_multiplication(monkeypatch):
    calls = 0

    def respond(_):
        nonlocal calls
        calls += 1
        return httpx.Response(503 if calls % 2 else 200, json={"text": "ok"})

    async with provider(monkeypatch, respond) as (client, admission):
        async with runtime.operation():
            await client.request("/test")
            await client.request("/test")
            with pytest.raises(ProviderUnavailable, match="budget"):
                await client.request("/test")
        assert admission.call_count == 4


@pytest.mark.asyncio
async def test_pool_reuse_concurrency_and_shutdown(monkeypatch):
    active = peak = 0

    async def respond(_):
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.01)
        active -= 1
        return httpx.Response(200, json={"text": "ok"})

    async with provider(monkeypatch, respond, provider_concurrency=1) as (client, _):
        async with runtime.runtime_client() as a, runtime.runtime_client() as b:
            assert a is b is client
        await asyncio.gather(*(client.request("/test") for _ in range(3)))
        assert peak == 1
    assert client.client.is_closed


def test_provider_failure_http_contract_preserves_private_response(monkeypatch):
    from fastapi.testclient import TestClient

    from app.dependencies import get_current_user_id
    from app.main import app

    app.dependency_overrides[get_current_user_id] = lambda: uuid4()
    monkeypatch.setattr(
        AddisAIClient,
        "synthesize_speech",
        AsyncMock(side_effect=ProviderUnavailable("private provider content")),
    )
    try:
        with TestClient(app) as client:
            response = client.post("/tts", json={"text": "private patient text"})
        assert response.status_code == 503
        assert response.json()["draft_preserved"] is True
        assert response.json()["recovery"] == ["retry", "manual_input"]
        assert "private" not in response.text
        assert response.headers["cache-control"] == "no-store"
    finally:
        app.dependency_overrides.clear()
