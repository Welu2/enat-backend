"""Backend-only PostgreSQL adapter. All values are bound; identifiers are quoted.

The small query interface supports existing repository operations while enforcing
transaction-local identity even when an application ownership filter is missing.
Auth and Storage clients never enter this data path.
"""

import json
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import date, datetime, time
from functools import lru_cache, wraps
from types import SimpleNamespace
from typing import Callable, ParamSpec, TypeVar
from uuid import UUID

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool

from app.config import get_settings
from app.core.errors import DataUnavailable

current_user_id: ContextVar[str | None] = ContextVar("current_user_id", default=None)
pool_override: ContextVar[object | None] = ContextVar("pool_override", default=None)
_active_transaction: ContextVar[object | None] = ContextVar(
    "active_transaction", default=None
)

P = ParamSpec("P")
R = TypeVar("R")


def atomic(action: Callable[P, R]) -> Callable[P, R]:
    """Keep a synchronous application mutation in one repository transaction."""

    @wraps(action)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        with transaction():
            return action(*args, **kwargs)

    return wrapped


TABLES = {
    "users",
    "supplements",
    "appointments",
    "check_ins",
    "summaries",
    "check_in_sessions",
    "reminders",
    "push_tokens",
    "summary_shares",
    "stage_audio_prompts",
}


def _configure(conn):
    validate_role(conn, "enat_app")


def validate_role(conn, expected_role):
    row = conn.execute(
        "SELECT current_user AS name, rolsuper, rolbypassrls FROM pg_roles WHERE rolname=current_user"
    ).fetchone()
    owns_tables = conn.execute(
        "SELECT EXISTS(SELECT 1 FROM pg_class c JOIN pg_roles r ON r.oid=c.relowner WHERE r.rolname=current_user AND c.relnamespace='public'::regnamespace) AS value"
    ).fetchone()["value"]
    conn.commit()
    if owns_tables:
        raise DataUnavailable("Application role must not own application tables")
    if row["name"] != expected_role or row["rolsuper"] or row["rolbypassrls"]:
        raise DataUnavailable(
            "Database credential must match its restricted process role"
        )


@lru_cache
def get_pool():
    settings = get_settings()
    if not settings.database_url:
        raise DataUnavailable("Database is not configured")
    return ConnectionPool(
        settings.database_url,
        min_size=0,
        max_size=settings.database_pool_size,
        timeout=5,
        kwargs={"row_factory": dict_row, "connect_timeout": 5},
        configure=_configure,
        open=True,
    )


@contextmanager
def transaction():
    active = _active_transaction.get()
    if active is not None:
        # Nested repositories participate in the caller's atomic unit of work.
        yield active
        return
    try:
        with (pool_override.get() or get_pool()).connection() as conn:
            with conn.transaction():
                conn.execute(
                    "SELECT set_config('app.user_id', %s, true)",
                    (current_user_id.get() or "",),
                )
                conn.execute("SET LOCAL TIME ZONE 'UTC'")
                conn.execute("SET LOCAL statement_timeout = '5s'")
                token = _active_transaction.set(conn)
                try:
                    yield conn
                finally:
                    _active_transaction.reset(token)
    except (psycopg.Error, TimeoutError) as exc:
        raise DataUnavailable("Database operation unavailable") from exc


def normalize(value):
    def encode(item):
        if isinstance(item, (date, datetime, time)):
            return item.isoformat()
        if isinstance(item, UUID):
            return str(item)
        raise TypeError("Unsupported database value")

    return json.loads(json.dumps(value, default=encode))


class Query:
    def __init__(self, table):
        if table not in TABLES:
            raise ValueError("Unknown application table")
        self.table = table
        self.operation = "select"
        self.columns = "*"
        self.payload = {}
        self.filters = []
        self.sort = None
        self.count = None
        self.single = False

    def select(self, fields="*"):
        self.columns = fields
        return self

    def insert(self, data):
        self.operation, self.payload = "insert", data
        return self

    def upsert(self, data):
        self.operation, self.payload = "upsert", data
        return self

    def update(self, data):
        self.operation, self.payload = "update", data
        return self

    def delete(self):
        self.operation = "delete"
        return self

    def eq(self, key, value):
        self.filters.append((key, "=", value))
        return self

    def gte(self, key, value):
        self.filters.append((key, ">=", value))
        return self

    def lt(self, key, value):
        self.filters.append((key, "<", value))
        return self

    def lte(self, key, value):
        self.filters.append((key, "<=", value))
        return self

    def order(self, key, desc=False):
        self.sort = (key, desc)
        return self

    def limit(self, count):
        self.count = max(1, min(int(count), 1000))
        return self

    def maybe_single(self):
        self.single = True
        return self

    def execute(self):
        table = sql.Identifier("public", self.table)
        fields = (
            sql.SQL("*")
            if self.columns == "*"
            else sql.SQL(", ").join(
                sql.Identifier(c.strip()) for c in self.columns.split(",")
            )
        )
        values = []
        if self.operation == "select":
            query = sql.SQL("SELECT {} FROM {}").format(fields, table)
        elif self.operation == "delete":
            query = sql.SQL("DELETE FROM {}").format(table)
        else:
            keys = list(self.payload)
            if not keys:
                raise ValueError("Empty mutation")
            values = [
                Jsonb(v) if isinstance(v, (dict, list)) else v
                for v in self.payload.values()
            ]
            if self.operation == "update":
                query = sql.SQL("UPDATE {} SET {}").format(
                    table,
                    sql.SQL(", ").join(
                        sql.SQL("{} = %s").format(sql.Identifier(k)) for k in keys
                    ),
                )
            else:
                query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    table,
                    sql.SQL(", ").join(map(sql.Identifier, keys)),
                    sql.SQL(", ").join(sql.Placeholder() for _ in keys),
                )
                if self.operation == "upsert":
                    query += sql.SQL(" ON CONFLICT (id) DO UPDATE SET {} ").format(
                        sql.SQL(", ").join(
                            sql.SQL("{} = EXCLUDED.{}").format(
                                sql.Identifier(k), sql.Identifier(k)
                            )
                            for k in keys
                            if k != "id"
                        )
                    )
        if self.filters:
            query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(
                sql.SQL("{} {} %s").format(sql.Identifier(k), sql.SQL(op))
                for k, op, _ in self.filters
            )
            values.extend(v for _, _, v in self.filters)
        if self.operation == "select":
            if self.sort:
                query += sql.SQL(" ORDER BY {} {}").format(
                    sql.Identifier(self.sort[0]),
                    sql.SQL("DESC" if self.sort[1] else "ASC"),
                )
            if self.count:
                query += sql.SQL(" LIMIT %s")
                values.append(self.count)
        else:
            query += sql.SQL(" RETURNING *")
        with transaction() as conn:
            rows = normalize(conn.execute(query, values).fetchall())
        if self.single and len(rows) > 1:
            raise DataUnavailable("Expected at most one row")
        return SimpleNamespace(
            data=(rows[0] if rows else None) if self.single else rows
        )


class DataClient:
    def table(self, name):
        return Query(name)


def get_data_client():
    return DataClient()


def resolve_identity(provider, subject, email=None, first_name=None, username=None):
    with transaction() as conn:
        return normalize(
            conn.execute(
                "SELECT public.enat_resolve_identity(%s,%s,%s,%s,%s) AS value",
                (provider, subject, email, first_name, username),
            ).fetchone()["value"]
        )


def close_pool():
    if get_pool.cache_info().currsize:
        get_pool().close()
        get_pool.cache_clear()
