import math
from datetime import datetime, timezone
from uuid import UUID

import httpx
import jwt
from jwt import PyJWTError

from app.config import get_settings
from app.core.errors import AuthenticationUnavailable


def auth_request(method: str, path: str, *, body=None, token=None):
    settings = get_settings()
    if not settings.supabase_publishable_key:
        raise AuthenticationUnavailable("Authentication is not configured")
    headers = {"apikey": settings.supabase_publishable_key}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with httpx.Client(
            timeout=httpx.Timeout(10, connect=3), follow_redirects=False
        ) as client:
            response = client.request(
                method,
                settings.supabase_url.rstrip("/") + "/auth/v1/" + path,
                headers=headers,
                json=body,
            )
    except httpx.HTTPError as exc:
        raise AuthenticationUnavailable(
            "Authentication temporarily unavailable"
        ) from exc
    if response.status_code >= 500 or response.status_code == 429:
        raise AuthenticationUnavailable("Authentication temporarily unavailable")
    if not response.is_success:
        raise ValueError("Invalid authentication request")
    try:
        payload = response.json() if response.content else {}
        if not isinstance(payload, dict):
            raise ValueError("Invalid authentication payload")
        return payload
    except ValueError as exc:
        raise AuthenticationUnavailable("Invalid authentication response") from exc


def decode_access_token(token: str) -> dict:
    """One verification policy: Supabase Auth validates signature and account.

    Claims parsed below are trusted only after Auth accepts the identical token
    and returns a matching verified user. Network errors never weaken policy.
    """
    settings = get_settings()
    try:
        header = jwt.get_unverified_header(token)
        # Parsing only; the same token must still pass online Supabase validation.
        claims = jwt.decode(token, options={"verify_signature": False})
        allowed = {"ES256", "RS256"}
        now = datetime.now(timezone.utc)
        if settings.legacy_hs256_until and now < datetime.fromisoformat(
            settings.legacy_hs256_until.replace("Z", "+00:00")
        ):
            allowed.add("HS256")
        if header.get("alg") not in allowed:
            raise ValueError("Invalid token algorithm")
        if claims.get("iss") != settings.supabase_url.rstrip("/") + "/auth/v1":
            raise ValueError("Invalid token issuer")
        if claims.get("aud") != "authenticated":
            raise ValueError("Invalid token audience")
        if (
            not isinstance(claims.get("exp"), (int, float))
            or isinstance(claims["exp"], bool)
            or claims["exp"] <= now.timestamp()
        ):
            raise ValueError("Expired token")
        if (
            claims.get("nbf", 0) > now.timestamp()
            or claims.get("iat", 0) > now.timestamp() + 30
        ):
            raise ValueError("Invalid token time")
        if not all(
            type(claims.get(key)) in (int, float) and math.isfinite(claims[key])
            for key in ("iat", "exp")
        ):
            raise ValueError("Invalid token timestamps")
        UUID(claims["sub"])
        UUID(claims["session_id"])
        user = auth_request("GET", "user", token=token)
        if user.get("id") != claims["sub"] or not user.get("email_confirmed_at"):
            raise ValueError("Unverified identity")
        if (
            user.get("banned_until")
            and datetime.fromisoformat(user["banned_until"].replace("Z", "+00:00"))
            > now
        ):
            raise ValueError("Disabled account")
        return {**claims, "email": user.get("email")}
    except (PyJWTError, KeyError, TypeError, ValueError) as exc:
        raise ValueError("Invalid or expired token") from exc
