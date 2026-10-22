import hashlib
import hmac
from contextlib import asynccontextmanager

import anyio
from starlette.concurrency import run_in_threadpool

from app.config import get_settings
from app.core.errors import RateLimited
from app.db.data import current_user_id, transaction


def take_rate(identity: str, category: str, limit: int, seconds: int = 60):
    settings = get_settings()
    if not settings.enable_request_limits:
        return
    if len(settings.rate_limit_secret) < 32:
        from app.core.errors import DataUnavailable

        raise DataUnavailable("Rate limiting is not configured")
    key = hmac.new(
        settings.rate_limit_secret.encode(),
        f"{category}:{identity}".encode(),
        hashlib.sha256,
    ).hexdigest()
    with transaction() as conn:
        allowed = conn.execute(
            "SELECT enat_take_rate(%s,%s,%s) AS value", (key, limit, seconds)
        ).fetchone()["value"]
    if not allowed:
        raise RateLimited("Request budget exceeded")


def _admit_provider():
    settings = get_settings()
    uid = current_user_id.get()
    if not uid:
        raise RateLimited("Provider work requires verified identity")
    take_rate(uid, "provider-day", settings.provider_daily_user_calls, 86400)
    take_rate("global", "provider-day", settings.provider_daily_global_calls, 86400)
    if not settings.enable_request_limits:
        return None
    with transaction() as conn:
        lease = conn.execute(
            "SELECT enat_acquire_provider(%s) AS value",
            (settings.provider_concurrency,),
        ).fetchone()["value"]
    if not lease:
        raise RateLimited("Provider capacity exhausted")
    return lease


def _release(lease):
    with transaction() as conn:
        conn.execute("SELECT enat_release_provider(%s)", (lease,))


@asynccontextmanager
async def provider_budget():
    lease = await run_in_threadpool(_admit_provider)
    try:
        with anyio.fail_after(65):
            yield
    finally:
        if lease:
            with anyio.CancelScope(shield=True):
                await run_in_threadpool(_release, lease)
