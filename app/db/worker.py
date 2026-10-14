"""Separate restricted worker pool, with no API credential fallback."""

from contextlib import contextmanager
from functools import lru_cache

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config import get_settings
from app.core.errors import DataUnavailable
from app.db import data


def _configure(conn):
    data.validate_role(conn, "enat_worker")


@lru_cache
def get_pool():
    url = get_settings().worker_database_url
    if not url:
        raise DataUnavailable("Worker database is not configured")
    return ConnectionPool(
        url,
        min_size=0,
        max_size=get_settings().worker_pool_size,
        timeout=5,
        kwargs={"row_factory": dict_row, "connect_timeout": 5},
        configure=_configure,
        open=True,
    )


@contextmanager
def worker_context(user_id=None):
    pool_token = data.pool_override.set(get_pool())
    identity_token = data.current_user_id.set(str(user_id) if user_id else None)
    try:
        yield
    finally:
        data.current_user_id.reset(identity_token)
        data.pool_override.reset(pool_token)


def close_pool():
    if get_pool.cache_info().currsize:
        get_pool().close()
        get_pool.cache_clear()
