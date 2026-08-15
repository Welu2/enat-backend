from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from supabase import create_client

from app.config import get_settings
from app.db.repositories.users import UserRepository
from app.models.user import AuthCredentials, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=AuthResponse)
def signup(credentials: AuthCredentials) -> AuthResponse:
    settings = get_settings()
    client = create_client(settings.supabase_url, settings.supabase_service_role_key)

    try:
        created = client.auth.admin.create_user(
            {
                "email": credentials.email,
                "password": credentials.password,
                "email_confirm": True,
            }
        )
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not created or not created.user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Signup failed")

    user_id = UUID(created.user.id)
    UserRepository().upsert(user_id, credentials.email)

    try:
        session_result = client.auth.sign_in_with_password(
            {"email": credentials.email, "password": credentials.password}
        )
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not session_result.session:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Failed to create session")

    return AuthResponse(
        access_token=session_result.session.access_token,
        user_id=user_id,
        email=credentials.email,
    )


@router.post("/login", response_model=AuthResponse)
def login(credentials: AuthCredentials) -> AuthResponse:
    settings = get_settings()
    client = create_client(settings.supabase_url, settings.supabase_service_role_key)

    try:
        result = client.auth.sign_in_with_password(
            {"email": credentials.email, "password": credentials.password}
        )
    except Exception as exc:
        error_msg = str(exc)
        # If user was created earlier without email confirmation, auto-confirm and retry login
        if "Email not confirmed" in error_msg:
            try:
                # Find user by email and confirm email via admin API
                users = client.auth.admin.list_users()
                target_user = next((u for u in users if u.email == credentials.email), None)
                if target_user:
                    client.auth.admin.update_user_by_id(target_user.id, {"email_confirm": True})
                    result = client.auth.sign_in_with_password(
                        {"email": credentials.email, "password": credentials.password}
                    )
                else:
                    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=error_msg) from exc
            except Exception:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=error_msg) from exc
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=error_msg) from exc

    if not result.user or not result.session:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_id = UUID(result.user.id)
    UserRepository().upsert(user_id, credentials.email)

    return AuthResponse(
        access_token=result.session.access_token,
        user_id=user_id,
        email=credentials.email,
    )
