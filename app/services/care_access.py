import hashlib
import secrets
from typing import Any
from uuid import UUID

from app.config import get_settings
from app.core.errors import Conflict, FeatureUnavailable, InvalidMutation, NotFound
from app.db.repositories.care_connections import call
from app.models.care import CareInviteRequest


def require_portal() -> None:
    if not get_settings().enable_care_portal:
        raise FeatureUnavailable("Care portal is disabled")


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def invite(payload: CareInviteRequest) -> dict[str, Any]:
    require_portal()
    token = secrets.token_urlsafe(32)
    result = call(
        "enat_care_invite",
        payload.recipient_id,
        payload.relationship,
        token_hash(token),
    )
    if result is None:
        raise NotFound("Recipient unavailable")
    if result.get("conflict"):
        raise Conflict("An active or pending connection already exists")
    return {**result, "token": token}


def accept(token: str) -> dict[str, Any]:
    require_portal()
    result = call("enat_care_accept", token_hash(token))
    if result is None:
        raise NotFound("Invitation unavailable")
    return dict(result)


def revoke(connection_id: UUID) -> None:
    # Access removal remains available while new sharing is disabled.
    if not call("enat_care_revoke", connection_id):
        raise NotFound("Connection unavailable")


def uuid_cursor(cursor: str | None) -> UUID | None:
    try:
        return UUID(cursor) if cursor else None
    except ValueError as exc:
        raise InvalidMutation("Invalid cursor") from exc


def connections(
    limit: int, cursor: str | None
) -> tuple[list[dict[str, Any]], str | None]:
    rows = call("enat_care_connections", limit, uuid_cursor(cursor))
    if rows is None:
        raise NotFound("Account unavailable")
    return rows[:limit], str(rows[limit - 1]["id"]) if len(rows) > limit else None
