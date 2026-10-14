import secrets
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from app.config import get_settings
from app.core.errors import AuthenticationUnavailable
from app.core.security import auth_request, decode_access_token
from app.core.telegram import verify_telegram_init_data
from app.db.data import resolve_identity, transaction
from app.dependencies import get_current_user, token_hash
from app.models.user import (
    AuthCredentials,
    AuthResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    SignupCredentials,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=1, max_length=4096)


class TelegramRequest(BaseModel):
    init_data: str = Field(min_length=1, max_length=16384)


class LinkRequest(BaseModel):
    access_token: str | None = Field(default=None, max_length=16384)
    init_data: str | None = Field(default=None, max_length=16384)


def session_response(result) -> AuthResponse:
    token = result.get("access_token")
    if not token:
        raise HTTPException(401, "Invalid credentials")
    try:
        claims = decode_access_token(token)
        with transaction() as conn:
            if conn.execute(
                "SELECT enat_auth_revoked(%s,%s,%s) AS value",
                (claims["session_id"], claims["sub"], claims["iat"]),
            ).fetchone()["value"]:
                raise ValueError("Revoked session")
        user = resolve_identity("supabase", claims["sub"], claims.get("email"))
        if not user:
            raise ValueError("Disabled account")
    except ValueError as exc:
        raise HTTPException(401, "Invalid credentials") from exc
    return AuthResponse(
        access_token=token,
        refresh_token=result.get("refresh_token"),
        expires_in=result.get("expires_in"),
        user_id=UUID(user["id"]),
        email=claims["email"],
    )


@router.post("/signup", status_code=202)
def signup(credentials: SignupCredentials):
    try:
        result = auth_request("POST", "signup", body=credentials.model_dump())
        if result.get("access_token") or result.get("session"):
            raise AuthenticationUnavailable(
                "Email confirmation must be enabled in Supabase"
            )
    except ValueError:
        pass  # Do not reveal account existence or provider detail.
    return {
        "status": "verification_required",
        "message": "Check your email to complete signup if eligible.",
    }


@router.post("/login", response_model=AuthResponse)
def login(credentials: AuthCredentials):
    try:
        result = auth_request(
            "POST", "token?grant_type=password", body=credentials.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(401, "Invalid credentials") from exc
    return session_response(result)


@router.post("/refresh", response_model=AuthResponse)
def refresh(payload: RefreshRequest):
    try:
        result = auth_request(
            "POST", "token?grant_type=refresh_token", body=payload.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(401, "Invalid credentials") from exc
    return session_response(result)


@router.post("/forgot-password", status_code=202)
def forgot_password(payload: ForgotPasswordRequest):
    try:
        auth_request("POST", "recover", body=payload.model_dump())
    except ValueError:
        pass
    return {
        "status": "accepted",
        "message": "If eligible, a recovery email will be sent.",
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest):
    # Only a recovery OTP/hash may enter this flow. Ordinary access tokens do
    # not prove a recovery event. Supabase consumes this OTP exactly once.
    try:
        result = auth_request(
            "POST",
            "verify",
            body={"token_hash": payload.token_hash, "type": "recovery"},
        )
        token = result.get("access_token")
        if not token:
            raise ValueError("Missing recovery session")
        claims = decode_access_token(token)
        auth_request(
            "PUT", "user", body={"password": payload.new_password}, token=token
        )
        with transaction() as conn:
            conn.execute("SELECT enat_revoke_user_auth(%s)", (claims["sub"],))
        auth_request("POST", "logout?scope=global", token=token)
    except ValueError as exc:
        raise HTTPException(400, "Invalid or expired recovery request") from exc
    return {"status": "success"}


@router.post("/telegram")
def telegram_login(payload: TelegramRequest):
    settings = get_settings()
    try:
        data = verify_telegram_init_data(
            payload.init_data,
            settings.telegram_bot_token,
            max_age=settings.telegram_max_age_seconds,
            clock_skew=settings.telegram_clock_skew_seconds,
        )
    except ValueError as exc:
        raise HTTPException(401, "Invalid credentials") from exc
    token = "enat_" + secrets.token_urlsafe(32)
    expiry = datetime.fromtimestamp(data["auth_date"] + 900, timezone.utc)
    user = data["user"]
    with transaction() as conn:
        result = conn.execute(
            "SELECT enat_telegram_session(%s,%s,%s,%s,%s,%s) AS value",
            (
                str(user["id"]),
                user.get("first_name"),
                user.get("username"),
                token_hash(token),
                data["source_hash"],
                expiry,
            ),
        ).fetchone()["value"]
    if not result:
        raise HTTPException(401, "Invalid or previously exchanged credentials")
    return {
        "access_token": token,
        "token_type": "bearer",  # nosec B105
        "expires_at": expiry,
        "user_id": result["id"],
    }


@router.post("/link")
def link_identity(payload: LinkRequest, user=Depends(get_current_user)):
    if bool(payload.access_token) == bool(payload.init_data):
        raise HTTPException(422, "Supply one additional identity proof")
    try:
        if payload.access_token:
            claims = decode_access_token(payload.access_token)
            with transaction() as conn:
                if conn.execute(
                    "SELECT enat_auth_revoked(%s,%s,%s) AS value",
                    (claims["session_id"], claims["sub"], claims["iat"]),
                ).fetchone()["value"]:
                    raise ValueError("Revoked proof")
            provider, subject = "supabase", claims["sub"]
        else:
            settings = get_settings()
            data = verify_telegram_init_data(
                payload.init_data,
                settings.telegram_bot_token,
                max_age=settings.telegram_max_age_seconds,
                clock_skew=settings.telegram_clock_skew_seconds,
            )
            provider, subject = "telegram", str(data["user"]["id"])
    except ValueError as exc:
        raise HTTPException(401, "Invalid additional identity proof") from exc
    with transaction() as conn:
        linked = conn.execute(
            "SELECT enat_link_identity(%s,%s) AS value", (provider, subject)
        ).fetchone()["value"]
    if not linked:
        raise HTTPException(
            409, "Identity already linked; account merging requires review"
        )
    return {"status": "linked"}


@router.post("/logout", status_code=204)
def logout(user=Depends(get_current_user), authorization: str = Header()):
    token = authorization[7:]
    if token.startswith("enat_"):
        with transaction() as conn:
            conn.execute("SELECT enat_revoke_session(%s)", (token_hash(token),))
            conn.execute("DELETE FROM push_tokens WHERE user_id=%s", (user["id"],))
    else:
        claims = decode_access_token(token)
        with transaction() as conn:
            # Keep the family revoked beyond the current access-token expiry.
            conn.execute(
                "SELECT enat_revoke_auth(%s,%s)",
                (claims["session_id"], datetime(9999, 1, 1, tzinfo=timezone.utc)),
            )
        with transaction() as conn:
            conn.execute("DELETE FROM push_tokens WHERE user_id=%s", (user["id"],))
        try:
            auth_request("POST", "logout?scope=local", token=token)
        except ValueError:
            pass
