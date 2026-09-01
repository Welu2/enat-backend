import hashlib
import hmac
import json
import os
from urllib.parse import parse_qsl
from uuid import UUID

from fastapi import Header, HTTPException, status

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.repositories.users import UserRepository

TELEGRAM_BOT_TOKEN = getattr(
    settings, "TELEGRAM_BOT_TOKEN", os.getenv("TELEGRAM_BOT_TOKEN", "")
)


def verify_telegram_init_data(init_data: str, bot_token: str) -> dict:
    """Validates Telegram HMAC-SHA256 signature and returns parsed payload."""
    try:
        parsed_data = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = parsed_data.pop("hash", None)
        if not received_hash:
            raise ValueError("Missing hash parameter in initData")

        # Telegram validation requires alphabetically sorted key=value pairs joined by \n
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed_data.items())
        )

        secret_key = hmac.new(
            b"WebAppData", bot_token.encode(), hashlib.sha256
        ).digest()
        calculated_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(calculated_hash, received_hash):
            raise ValueError("Invalid Telegram signature")

        if "user" in parsed_data:
            parsed_data["user"] = json.loads(parsed_data["user"])

        return parsed_data
    except Exception as exc:
        raise ValueError(f"Telegram auth failed: {exc}") from exc


def get_current_user(
    authorization: str | None = Header(None),
) -> dict:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    user_repo = UserRepository()

    # --- 1. Telegram Mini App Auth (tma <initData>) ---
    if authorization.startswith("tma "):
        init_data = authorization[4:].strip()
        try:
            tg_data = verify_telegram_init_data(init_data, TELEGRAM_BOT_TOKEN)
            tg_user = tg_data.get("user")
            if not tg_user or "id" not in tg_user:
                raise ValueError("User profile missing from Telegram payload")

            telegram_id = str(tg_user["id"])
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc

        # Look up by telegram_id (or auto-create user on first launch)
        user = getattr(user_repo, "get_by_telegram_id", lambda _: None)(telegram_id)
        
        if not user and hasattr(user_repo, "create_from_telegram"):
            user = user_repo.create_from_telegram(tg_user)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not registered. Please sign up first.",
            )
        return user

    # --- 2. Regular Web JWT Auth (Bearer <token>) ---
    elif authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        try:
            payload = decode_access_token(token)
            user_id = UUID(payload["sub"])
        except (ValueError, KeyError, TypeError) as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc

        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authorization scheme. Expected 'Bearer' or 'tma'.",
    )


def get_current_user_id(
    current_user: dict = Depends(get_current_user),
) -> UUID:
    """Helper for endpoints that only require user_id UUID."""
    user_id = current_user.get("id") if isinstance(current_user, dict) else getattr(current_user, "id", None)
    if isinstance(user_id, UUID):
        return user_id
    return UUID(str(user_id))