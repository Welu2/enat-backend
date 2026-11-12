import base64
import hashlib
import re
import secrets
from datetime import date, timedelta
from uuid import UUID

from pydantic import BaseModel, Field, StrictBool

from app.config import get_settings
from app.core.constants import DANGER_SIGN_CATEGORIES
from app.core.errors import (
    ArtifactUnavailable,
    ConsentRequired,
    FeatureUnavailable,
    NotFound,
)
from app.db.data import normalize, transaction
from app.services.qr import generate_qr_png


class ShareRequest(BaseModel):
    consent: StrictBool
    expires_in_hours: int = Field(default=24, ge=1, le=168)


def enabled():
    if not get_settings().enable_summary_sharing:
        raise FeatureUnavailable("Summary sharing is awaiting privacy review")


def create_share(user_id: UUID, summary_id: UUID, payload: ShareRequest):
    enabled()
    if not payload.consent:
        raise ConsentRequired("Explicit consent is required")
    token = secrets.token_urlsafe(32)
    digest = hashlib.sha256(token.encode()).hexdigest()
    with transaction() as conn:
        # Database time controls both creation and expiry; no clock-skew gap.
        row = conn.execute(
            """INSERT INTO summary_shares(summary_id,user_id,token_hash,scope,expires_at)
            SELECT id,user_id,%s,'structured-v1',now()+%s::interval FROM summaries
            WHERE id=%s AND user_id=%s RETURNING id,expires_at""",
            (digest, timedelta(hours=payload.expires_in_hours), summary_id, user_id),
        ).fetchone()
    if not row:
        raise NotFound("Summary not found")
    url = get_settings().public_base_url.rstrip("/") + "/summary/" + token
    # QR is an independent artifact after commit. Preserve the usable share
    # response if rendering fails so the owner can retry without a new snapshot.
    try:
        qr = base64.b64encode(generate_qr_png(url)).decode()
    except ArtifactUnavailable:
        qr = None
    return {
        **normalize(row),
        "scope": "structured-v1",
        "share_url": url,
        "qr_code_base64": qr,
        "qr_status": "ready" if qr is not None else "retry_required",
    }


def revoke_share(user_id: UUID, share_id: UUID):
    with transaction() as conn:
        row = conn.execute(
            "UPDATE summary_shares SET revoked_at=coalesce(revoked_at,now()) WHERE id=%s AND user_id=%s RETURNING id",
            (share_id, user_id),
        ).fetchone()
    if not row:
        raise NotFound("Share not found")


def structured_content(content):
    """Versioned allowlist. Never forward free text or arbitrary nested JSON."""
    result = {"scope": "structured-v1", "danger_signs": [], "general_symptoms": []}
    categories = set(DANGER_SIGN_CATEGORIES) | {
        "no_danger_sign_detected",
        "unclassified",
    }
    for group in ("danger_signs", "general_symptoms"):
        for item in content.get(group, [])[:500]:
            if (
                isinstance(item, dict)
                and item.get("category") is None
                and item.get("assessment") == "unclassified"
            ):
                item = {**item, "category": "unclassified"}
            if not isinstance(item, dict) or item.get("category") not in categories:
                continue
            entry = {"category": item["category"]}
            try:
                entry["date"] = date.fromisoformat(item["date"]).isoformat()
            except (ValueError, TypeError, KeyError):
                continue
            if item.get("severity") in {"mild", "moderate", "severe", "unspecified"}:
                entry["severity"] = item["severity"]
            result[group].append(entry)
    adherence = content.get("supplement_adherence", {})
    if isinstance(adherence, dict):
        result["supplement_adherence"] = {
            k: v
            for k, v in adherence.items()
            if k in {"taken_days", "tracked_days"} and type(v) is int and 0 <= v <= 3660
        }
        result["supplement_adherence"]["denominator"] = (
            "known supplement-day observations"
        )
    return result


def read_share(token: str):
    enabled()
    if not re.fullmatch(r"[A-Za-z0-9_-]{43}", token):
        return None
    with transaction() as conn:
        row = conn.execute(
            "SELECT enat_read_share(%s) AS value",
            (hashlib.sha256(token.encode()).hexdigest(),),
        ).fetchone()["value"]
    if not row:
        return None
    row["content_json"] = structured_content(row.get("content_json") or {})
    return row


class ShareQRRequest(BaseModel):
    token: str = Field(pattern=r"^[A-Za-z0-9_-]{43}$")


def render_share_qr(user_id, share_id, token):
    enabled()
    digest = hashlib.sha256(token.encode()).hexdigest()
    with transaction() as conn:
        row = conn.execute(
            "SELECT id FROM summary_shares WHERE id=%s AND user_id=%s AND token_hash=%s AND revoked_at IS NULL AND expires_at>now()",
            (share_id, user_id, digest),
        ).fetchone()
    if not row:
        raise NotFound("Share not found")
    return generate_qr_png(
        get_settings().public_base_url.rstrip("/") + "/summary/" + token
    )
