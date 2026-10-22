"""Bound calls to the narrowly scoped care database interface."""

from typing import Any

from psycopg import sql

from app.db.data import normalize, transaction

FUNCTIONS = frozenset(
    {
        "enat_care_invite",
        "enat_care_connections",
        "enat_care_accept",
        "enat_care_revoke",
        "enat_portal_me",
        "enat_portal_patients",
        "enat_portal_read",
        "enat_portal_acknowledge",
    }
)


def call(name: str, *params: Any) -> Any:
    if name not in FUNCTIONS:
        raise ValueError("Unknown care operation")
    query = sql.SQL("SELECT public.{}({}) AS value").format(
        sql.Identifier(name), sql.SQL(",").join(sql.Placeholder() for _ in params)
    )
    with transaction() as conn:
        return normalize(conn.execute(query, params).fetchone()["value"])
