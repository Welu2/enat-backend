import hmac
import hashlib
import json
from urllib.parse import parse_qsl

def verify_and_parse_telegram_data(init_data: str, bot_token: str) -> dict | None:
    """
    Verifies Telegram HMAC-SHA256 signature and returns user data if valid.
    """
    try:
        parsed_data = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = parsed_data.pop("hash", None)
        if not received_hash:
            return None

        # 1. Construct data_check_string
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))

        # 2. Derive secret key and calculate hash
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        # 3. Constant-time comparison
        if not hmac.compare_digest(calculated_hash, received_hash):
            return None

        # 4. Extract user dictionary
        if "user" in parsed_data:
            parsed_data["user"] = json.loads(parsed_data["user"])

        return parsed_data
    except Exception:
        return None