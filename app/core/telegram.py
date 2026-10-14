import hashlib
import hmac
import json
import re
import time
from urllib.parse import parse_qsl


def verify_telegram_init_data(
    init_data: str, bot_token: str, *, now=None, max_age=300, clock_skew=30
) -> dict:
    if not bot_token.strip() or not init_data or len(init_data) > 16384:
        raise ValueError("Invalid Telegram credentials")
    try:
        if re.search(r"%(?![0-9a-fA-F]{2})", init_data):
            raise ValueError("Malformed encoding")
        pairs = parse_qsl(
            init_data,
            keep_blank_values=True,
            strict_parsing=True,
            errors="strict",
            max_num_fields=20,
        )
        payload = dict(pairs)
        if len(payload) != len(pairs):
            raise ValueError("Duplicate parameter")
        signature = payload.pop("hash")
        if not re.fullmatch(r"[0-9a-fA-F]{64}", signature):
            raise ValueError("Invalid signature")
        checked = "\n".join(f"{key}={value}" for key, value in sorted(payload.items()))
        secret = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        digest = hmac.new(secret, checked.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature.lower(), digest):
            raise ValueError("Invalid signature")
        auth_date = int(payload["auth_date"])
        instant = time.time() if now is None else now
        if instant - auth_date > max_age or auth_date - instant > clock_skew:
            raise ValueError("Expired launch data")
        user = json.loads(payload["user"])
        if (
            not isinstance(user, dict)
            or type(user.get("id")) is not int
            or user["id"] <= 0
        ):
            raise ValueError("Invalid Telegram user")
        return {**payload, "user": user, "auth_date": auth_date, "source_hash": digest}
    except (KeyError, ValueError, TypeError, UnicodeError) as exc:
        raise ValueError("Invalid Telegram credentials") from exc
