from jose import JWTError, jwt
from supabase import create_client

from app.config import get_settings


def decode_access_token(token: str) -> dict:
    settings = get_settings()

    # 1. Primary verification via Supabase Auth API.
    # Handles modern ES256, RS256, and HS256 tokens issued by Supabase.
    try:
        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        user_res = client.auth.get_user(token)
        if user_res and user_res.user:
            return {
                "sub": str(user_res.user.id),
                "email": user_res.user.email,
            }
    except Exception:
        pass

    # 2. Fallback local secret verification (for HS256 tokens and test environment)
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
        user_id = payload.get("sub")
        if user_id:
            return payload
    except JWTError:
        pass

    raise ValueError("Invalid or expired token")
