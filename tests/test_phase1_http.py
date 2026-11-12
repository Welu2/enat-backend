import io
import wave
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from starlette.datastructures import Headers, UploadFile

from app.config import get_settings
from app.core.errors import InvalidAudio, PayloadTooLarge
from app.dependencies import get_current_user
from app.main import app, create_app
from app.services.audio_upload import read_audio
from app.services.sharing import structured_content


def test_signup_never_returns_session_or_auto_confirms(monkeypatch):
    provider = Mock(return_value={"user": {"id": str(uuid4())}})
    monkeypatch.setattr("app.api.routes.auth.auth_request", provider)
    response = TestClient(app).post(
        "/auth/signup", json={"email": "patient@example.org", "password": "abcdefgh"}
    )
    assert response.status_code == 202
    assert "access_token" not in response.json()
    assert provider.call_args.args == ("POST", "signup")
    assert "email_confirm" not in str(provider.call_args)


def test_signup_rejects_provider_confirmation_misconfiguration(monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.auth.auth_request",
        Mock(return_value={"access_token": "secret"}),
    )
    response = TestClient(app).post(
        "/auth/signup", json={"email": "patient@example.org", "password": "abcdefgh"}
    )
    assert response.status_code == 503
    assert "secret" not in response.text


def test_login_error_does_not_confirm_or_leak_provider_details(monkeypatch):
    provider = Mock(side_effect=ValueError("Email not confirmed: patient@example.org"))
    monkeypatch.setattr("app.api.routes.auth.auth_request", provider)
    response = TestClient(app).post(
        "/auth/login", json={"email": "patient@example.org", "password": "abcdefgh"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
    provider.assert_called_once()


def test_recovery_requires_recovery_hash_and_consumes_it(monkeypatch):
    provider = Mock(side_effect=[{"access_token": "recovery-session"}, {}, {}])
    monkeypatch.setattr("app.api.routes.auth.auth_request", provider)
    monkeypatch.setattr(
        "app.api.routes.auth.decode_access_token",
        Mock(return_value={"sub": str(uuid4())}),
    )
    monkeypatch.setattr(
        "app.api.routes.auth.transaction",
        Mock(
            return_value=__import__("unittest.mock", fromlist=["MagicMock"]).MagicMock()
        ),
    )
    response = TestClient(app).post(
        "/auth/reset-password",
        json={"token_hash": "recovery-hash-123456789", "new_password": "new-password"},
    )
    assert response.status_code == 200
    assert provider.call_args_list[0].kwargs["body"]["type"] == "recovery"
    assert provider.call_args_list[1].kwargs["token"] == "recovery-session"
    invalid = TestClient(app).post(
        "/auth/reset-password",
        json={"access_token": "ordinary-jwt", "new_password": "new-password"},
    )
    assert invalid.status_code == 422
    assert "ordinary-jwt" not in invalid.text


def test_legacy_tts_and_unauthenticated_post_never_call_provider(monkeypatch):
    provider = AsyncMock()
    monkeypatch.setattr("app.api.routes.tts.AddisAIClient.synthesize_speech", provider)
    client = TestClient(app)
    assert client.get("/tts?text=private-patient-text").status_code == 410
    assert client.post("/tts", json={"text": "private-patient-text"}).status_code == 401
    provider.assert_not_called()


def test_authenticated_tts_no_shared_cache_and_private_headers(monkeypatch):
    provider = AsyncMock(return_value=b"audio")
    monkeypatch.setattr("app.api.routes.tts.AddisAIClient.synthesize_speech", provider)
    app.dependency_overrides[get_current_user] = lambda: {"id": str(uuid4())}
    try:
        response = TestClient(app).post("/tts", json={"text": "patient text"})
        assert response.status_code == 200
        assert response.headers["cache-control"] == "no-store"
        assert response.headers["referrer-policy"] == "no-referrer"
    finally:
        app.dependency_overrides.clear()


def test_oversized_chunked_body_rejected_before_route(monkeypatch):
    provider = Mock()
    monkeypatch.setattr("app.api.routes.auth.auth_request", provider)
    response = TestClient(app).post(
        "/auth/login",
        content=iter([b"x" * 40000, b"y" * 40000]),
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 413
    provider.assert_not_called()


def test_validation_redacts_input_and_trusted_host_blocks():
    client = TestClient(app)
    response = client.post(
        "/auth/login", json={"email": "private-invalid-value", "password": "secret"}
    )
    assert response.status_code == 422
    assert (
        "private-invalid-value" not in response.text and "secret" not in response.text
    )
    assert (
        client.get("/health", headers={"host": "attacker.invalid"}).status_code == 400
    )


def test_sharing_whitelist_discards_free_text_and_unknown_fields():
    content = {
        "raw_text": "PRIVATE",
        "email": "PRIVATE",
        "danger_signs": [
            {
                "category": "high_fever",
                "date": "2026-10-13",
                "raw_text": "PRIVATE",
                "severity": "PRIVATE",
            }
        ],
        "closing_mentions": [{"raw_text": "PRIVATE"}],
        "supplement_adherence": {"taken_days": 2, "raw_text": "PRIVATE"},
    }
    shared = structured_content(content)
    assert "PRIVATE" not in str(shared)
    assert shared["danger_signs"] == [{"category": "high_fever", "date": "2026-10-13"}]


@pytest.mark.asyncio
async def test_audio_type_and_streamed_size_rejected_before_probe(monkeypatch):
    probe = Mock()
    monkeypatch.setattr("app.services.audio_upload.inspect_audio", probe)
    with pytest.raises(InvalidAudio):
        await read_audio(
            UploadFile(
                io.BytesIO(b"audio"), headers=Headers({"content-type": "text/plain"})
            )
        )
    settings = get_settings().model_copy(update={"max_audio_bytes": 1024})
    monkeypatch.setattr("app.services.audio_upload.get_settings", lambda: settings)
    with pytest.raises(PayloadTooLarge):
        await read_audio(
            UploadFile(
                io.BytesIO(b"x" * 1025), headers=Headers({"content-type": "audio/wav"})
            )
        )
    probe.assert_not_called()


@pytest.mark.asyncio
async def test_real_audio_probe_validates_format_and_duration(monkeypatch):
    output = io.BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(8000)
        audio.writeframes(b"\x00\x00" * 16000)
    payload = output.getvalue()

    def upload(mime):
        return UploadFile(io.BytesIO(payload), headers=Headers({"content-type": mime}))

    assert await read_audio(upload("audio/wav")) == payload
    with pytest.raises(InvalidAudio):
        await read_audio(upload("audio/webm"))
    settings = get_settings().model_copy(update={"max_audio_seconds": 1})
    monkeypatch.setattr("app.services.audio_upload.get_settings", lambda: settings)
    with pytest.raises(PayloadTooLarge):
        await read_audio(upload("audio/wav"))


def test_access_log_drops_query_text_and_share_tokens():
    import logging

    from app.core.http_security import AccessLogFilter

    record = logging.LogRecord(
        "uvicorn.access",
        20,
        "",
        0,
        '%s - "%s %s HTTP/%s" %d',
        ("peer", "GET", "/summary/PRIVATE?text=PRIVATE", "1.1", 200),
        None,
    )
    AccessLogFilter().filter(record)
    assert "PRIVATE" not in record.getMessage()


def test_distributed_limit_failure_has_documented_429(monkeypatch):
    from app.core.errors import RateLimited

    application = create_app(
        get_settings().model_copy(update={"enable_request_limits": True})
    )
    monkeypatch.setattr(
        "app.core.http_security.take_rate", Mock(side_effect=RateLimited())
    )
    response = TestClient(application).post(
        "/auth/login", json={"email": "a@example.org", "password": "abcdefgh"}
    )
    assert response.status_code == 429
    assert response.headers["retry-after"] == "60"
