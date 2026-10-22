"""Committed results share the domain transaction; no provider call belongs here."""

import hashlib
import json
import re

from psycopg.types.json import Jsonb

from app.core.errors import Conflict, InvalidMutation
from app.db.data import normalize, transaction


def request_hash(payload):
    return hashlib.sha256(
        json.dumps(
            normalize(payload), sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    ).hexdigest()


def validate_key(key):
    if key is not None and not re.fullmatch(r"[A-Za-z0-9_.:-]{8,128}", key):
        raise InvalidMutation("Invalid idempotency key")


def lookup(user_id, operation, key, payload):
    validate_key(key)
    if key is None:
        return None
    with transaction() as conn:
        row = conn.execute(
            "SELECT request_hash, result FROM mutation_results WHERE user_id=%s AND operation=%s AND key=%s",
            (user_id, operation, key),
        ).fetchone()
        if row:
            if row["request_hash"] != request_hash(payload):
                raise Conflict("Idempotency key reused for different input")
            return row["result"]
    return None


def execute(user_id, operation, key, payload, action):
    validate_key(key)
    with transaction() as conn:
        if key is not None:
            lock = request_hash([str(user_id), operation, key])
            conn.execute(
                "SELECT pg_advisory_xact_lock(hashtextextended(%s,0))", (lock,)
            )
            previous = lookup(user_id, operation, key, payload)
            if previous is not None:
                return previous
        result = normalize(action())
        if key is not None:
            conn.execute(
                "INSERT INTO mutation_results(user_id,operation,key,request_hash,result) VALUES (%s,%s,%s,%s,%s)",
                (user_id, operation, key, request_hash(payload), Jsonb(result)),
            )
        return result


def emit(user_id, event_type, aggregate_id, payload=None):
    from app.core.observability import trace_headers

    body = dict(payload or {})
    if parent := trace_headers().get("traceparent"):
        body["_traceparent"] = parent
    with transaction() as conn:
        conn.execute(
            "INSERT INTO domain_outbox(user_id,event_type,aggregate_id,payload) VALUES (%s,%s,%s,%s) ON CONFLICT (event_type,aggregate_id) DO NOTHING",
            (user_id, event_type, aggregate_id, Jsonb(body)),
        )
