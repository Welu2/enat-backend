"""Stable keyset pages. Cursors are validated data, never authorization."""

import base64
import binascii
import json
from datetime import datetime
from uuid import UUID

from psycopg import sql

from app.core.errors import InvalidMutation
from app.db.data import normalize, transaction

TABLES = {"check_ins": "timestamp", "reminders": "due_at", "supplements": "created_at"}
PAGE_RESPONSE = {
    200: {
        "headers": {
            "X-Next-Cursor": {
                "description": "Opaque next page cursor; absent on the final page",
                "schema": {"type": "string"},
            }
        }
    }
}


def encode(row, field):
    return (
        base64.urlsafe_b64encode(json.dumps([str(row[field]), str(row["id"])]).encode())
        .decode()
        .rstrip("=")
    )


def decode(cursor):
    try:
        if len(cursor) > 256:
            raise ValueError()
        stamp, identifier = json.loads(
            base64.b64decode(
                cursor + "=" * (-len(cursor) % 4), altchars=b"-_", validate=True
            )
        )
        if not isinstance(stamp, str) or not isinstance(identifier, str):
            raise ValueError()
        value = datetime.fromisoformat(stamp)
        if value.tzinfo is None:
            raise ValueError()
        return value, UUID(identifier)
    except (ValueError, TypeError, binascii.Error) as exc:
        raise InvalidMutation("Invalid page cursor") from exc


def page(table, user_id, limit=50, cursor=None, *, start=None, end=None, due=None):
    field = TABLES[table]
    if not 1 <= limit <= 100:
        raise InvalidMutation("Page size must be between 1 and 100")
    descending = table == "check_ins"
    conditions = [sql.SQL("user_id=%s")]
    values = [user_id]
    if cursor:
        stamp, identifier = decode(cursor)
        conditions.append(
            sql.SQL("({},id) {} (%s,%s)").format(
                sql.Identifier(field), sql.SQL("<" if descending else ">")
            )
        )
        values.extend([stamp, identifier])
    for boundary, operator in ((start, ">="), (end, "<"), (due, "<=")):
        if boundary is not None:
            conditions.append(
                sql.SQL("{} {} %s").format(sql.Identifier(field), sql.SQL(operator))
            )
            values.append(boundary)
    if table == "reminders":
        conditions.append(sql.SQL("NOT dismissed"))
    query = sql.SQL("SELECT * FROM {} WHERE {} ORDER BY {} {}, id {} LIMIT %s").format(
        sql.Identifier(table),
        sql.SQL(" AND ").join(conditions),
        sql.Identifier(field),
        sql.SQL("DESC" if descending else "ASC"),
        sql.SQL("DESC" if descending else "ASC"),
    )
    with transaction() as conn:
        rows = normalize(conn.execute(query, [*values, limit + 1]).fetchall())
    return rows[:limit], encode(rows[limit - 1], field) if len(rows) > limit else None
