import hashlib
import hmac
import json
from datetime import datetime, timezone
from unittest.mock import Mock
from urllib.parse import urlencode
from uuid import uuid4

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from app.core.errors import AuthenticationUnavailable
from app.core.security import decode_access_token
from app.core.telegram import verify_telegram_init_data


def signed_token(**overrides):
    key = ec.generate_private_key(ec.SECP256R1()).private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    payload = {
        "sub": str(uuid4()),
        "session_id": str(uuid4()),
        "aud": "authenticated",
        "iss": "https://example.supabase.co/auth/v1",
        "exp": int(datetime.now(timezone.utc).timestamp()) + 600,
        "iat": int(datetime.now(timezone.utc).timestamp()),
        **overrides,
    }
    return jwt.encode(payload, key, algorithm="ES256"), payload


def test_valid_token_requires_auth_verification(monkeypatch):
    token, payload = signed_token()
    provider = Mock(
        return_value={
            "id": payload["sub"],
            "email": "patient@example.org",
            "email_confirmed_at": "2026-01-01T00:00:00Z",
        }
    )
    monkeypatch.setattr("app.core.security.auth_request", provider)
    assert decode_access_token(token)["sub"] == payload["sub"]
    provider.assert_called_once_with("GET", "user", token=token)


@pytest.mark.parametrize(
    "overrides",
    [
        {"exp": 0},
        {"aud": "anon"},
        {"iss": "https://attacker.invalid"},
        {"sub": "not-a-uuid"},
        {"session_id": None},
        {"nbf": 9999999999},
        {"exp": True},
    ],
)
def test_invalid_claims_rejected_before_auth(monkeypatch, overrides):
    token, _ = signed_token(**overrides)
    provider = Mock()
    monkeypatch.setattr("app.core.security.auth_request", provider)
    with pytest.raises(ValueError):
        decode_access_token(token)
    provider.assert_not_called()


def test_hs256_has_no_automatic_fallback(monkeypatch):
    token = jwt.encode(
        {"sub": str(uuid4()), "aud": "authenticated"},
        "test-jwt-secret",
        algorithm="HS256",
    )
    with pytest.raises(ValueError):
        decode_access_token(token)


def test_auth_outage_is_not_invalid_credentials_or_fallback(monkeypatch):
    token, _ = signed_token()
    monkeypatch.setattr(
        "app.core.security.auth_request", Mock(side_effect=AuthenticationUnavailable())
    )
    with pytest.raises(AuthenticationUnavailable):
        decode_access_token(token)


@pytest.mark.parametrize("user", [{}, {"id": "wrong", "email_confirmed_at": "yes"}])
def test_unverified_or_mismatched_user_rejected(monkeypatch, user):
    token, _ = signed_token()
    monkeypatch.setattr("app.core.security.auth_request", Mock(return_value=user))
    with pytest.raises(ValueError):
        decode_access_token(token)


def telegram_data(bot="secret", now=1000, **overrides):
    values = {
        "auth_date": str(now),
        "user": json.dumps({"id": 42, "first_name": "Patient"}),
        **overrides,
    }
    checked = "\n".join(f"{k}={v}" for k, v in sorted(values.items()))
    key = hmac.new(b"WebAppData", bot.encode(), hashlib.sha256).digest()
    values["hash"] = hmac.new(key, checked.encode(), hashlib.sha256).hexdigest()
    return urlencode(values)


def test_valid_telegram_launch():
    assert (
        verify_telegram_init_data(telegram_data(), "secret", now=1000)["user"]["id"]
        == 42
    )


@pytest.mark.parametrize(
    "data,bot,now",
    [
        (telegram_data(), "", 1000),
        (telegram_data(), "wrong", 1000),
        (telegram_data(), "secret", 1301),
        (telegram_data(now=1031), "secret", 1000),
        (telegram_data() + "&auth_date=1000", "secret", 1000),
        (telegram_data() + "&broken=%XX", "secret", 1000),
        (telegram_data(user='{"id":true}'), "secret", 1000),
        (telegram_data(user='{"id":-2}'), "secret", 1000),
        (telegram_data(auth_date="no"), "secret", 1000),
    ],
)
def test_invalid_telegram_launch(data, bot, now):
    with pytest.raises(ValueError):
        verify_telegram_init_data(data, bot, now=now)
