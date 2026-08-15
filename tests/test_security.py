from uuid import uuid4
from jose import jwt
import pytest

from app.core.security import decode_access_token


def test_decode_access_token_hs256_fallback() -> None:
    user_id = str(uuid4())
    token = jwt.encode(
        {"sub": user_id, "aud": "authenticated"},
        "test-jwt-secret",
        algorithm="HS256",
    )
    payload = decode_access_token(token)
    assert payload["sub"] == user_id


def test_decode_access_token_invalid_raises() -> None:
    with pytest.raises(ValueError, match="Invalid or expired token"):
        decode_access_token("invalid.token.here")
