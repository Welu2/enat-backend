"""Compatibility import for callers of the old validator; one implementation."""

from app.core.telegram import verify_telegram_init_data


def verify_and_parse_telegram_data(init_data: str, bot_token: str) -> dict | None:
    try:
        return verify_telegram_init_data(init_data, bot_token)
    except ValueError:
        return None
