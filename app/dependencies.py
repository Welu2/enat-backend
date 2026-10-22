import hashlib
from uuid import UUID

from fastapi import Depends, Header, HTTPException, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.concurrency import run_in_threadpool

from app.core.security import decode_access_token
from app.db.data import current_user_id, normalize, resolve_identity, transaction

bearer_scheme = HTTPBearer(auto_error=False)


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def authenticate(authorization: str | None) -> dict:
    if (
        not authorization
        or not authorization.startswith("Bearer ")
        or len(authorization) > 16384
    ):
        raise HTTPException(401, "Invalid credentials")
    token = authorization[7:]
    try:
        if token.startswith("enat_"):
            with transaction() as conn:
                user = normalize(
                    conn.execute(
                        "SELECT public.enat_get_session(%s) AS value",
                        (token_hash(token),),
                    ).fetchone()["value"]
                )
        else:
            payload = decode_access_token(token)
            with transaction() as conn:
                revoked = conn.execute(
                    "SELECT public.enat_auth_revoked(%s,%s,%s) AS value",
                    (payload["session_id"], payload["sub"], payload["iat"]),
                ).fetchone()["value"]
            if revoked:
                raise ValueError("Revoked session")
            user = resolve_identity("supabase", payload["sub"], payload.get("email"))
        if not user:
            raise ValueError("Disabled account")
        return user
    except ValueError as exc:
        raise HTTPException(401, "Invalid credentials") from exc


async def get_current_user(
    request: Request,
    authorization: str | None = Header(None),
    _credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
):
    user = await run_in_threadpool(authenticate, authorization)
    from app.core.limits import take_rate

    await run_in_threadpool(take_rate, str(user["id"]), "authenticated", 120)
    context = current_user_id.set(str(user["id"]))
    try:
        yield user
    finally:
        current_user_id.reset(context)


def get_current_user_id(current_user: dict = Depends(get_current_user)) -> UUID:
    return UUID(str(current_user["id"]))
