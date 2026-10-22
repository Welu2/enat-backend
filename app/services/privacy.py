"""Owned, bounded personal-data pages and non-destructive privacy requests."""

from uuid import UUID

from psycopg import sql

from app.config import get_settings
from app.core.clock import utc_now
from app.core.errors import FeatureUnavailable, InvalidMutation, NotFound
from app.db import idempotency
from app.db.data import normalize, transaction

# Explicit columns: new database columns are never silently included in exports.
SECTIONS = {
    "profile": (
        "users",
        "id",
        "id email created_at telegram_id first_name username age area pregnancy_counting_method lnmp_date ultrasound_date ultrasound_weeks gestational_age_weeks gestational_age_days is_gestational_age_manual effective_lnmp_date estimated_due_date trimester total_pregnancies live_births had_c_section child_passed_away past_pregnancy_complications known_medical_conditions custom_medical_condition malaria_endemic_area current_medications hospital onboarding_completed",
    ),
    "supplements": (
        "supplements",
        "user_id",
        "id name active reminder_enabled reminder_time created_at",
    ),
    "appointments": (
        "appointments",
        "user_id",
        "id appointment_date last_summary_generated_at reminder_lead_days anc_contact_number anc_contact_title anc_contact_title_am target_gestational_weeks previous_appointment_date status version",
    ),
    "appointment_events": (
        "appointment_events",
        "user_id",
        "id appointment_id action previous_date new_date created_at",
    ),
    "check_ins": (
        "check_ins",
        "user_id",
        "id timestamp recorded_at received_at client_confirmed_at capture_source client_submission_id symptoms food_log supplement_check closing_mentions danger_sign_triggered summary_text_am summary_text_en session_id policy_version",
    ),
    "drafts": (
        "check_in_sessions",
        "user_id",
        "id current_stage stage_order draft_data pending_items status created_at expires_at version stage_status completed_stages",
    ),
    "summaries": (
        "summaries",
        "user_id",
        "id period_start period_end generated_at content_json anc_contact_number anc_contact_title anc_contact_title_am target_gestational_weeks window_start window_end",
    ),
    "reminders": (
        "reminders",
        "user_id",
        "id type message due_at dismissed created_at",
    ),
    "shares": (
        "summary_shares",
        "user_id",
        "id summary_id scope consent_at expires_at revoked_at created_at",
    ),
    "requests": (
        "privacy_requests",
        "user_id",
        "id kind status created_at cancelled_at",
    ),
    "care_connections": (
        "care_connections",
        "patient_id",
        "id recipient_id relationship status consent_version consented_at created_at accepted_at revoked_at expires_at",
    ),
    "emergency_alerts": (
        "emergency_alerts",
        "patient_id",
        "id check_in_id categories recorded_at received_at created_at policy_version status acknowledged_at acknowledged_by",
    ),
    "care_audit": (
        "care_access_events",
        "patient_id",
        "id actor_id connection_id action resource resource_id row_count occurred_at",
    ),
    "audit": (
        "privacy_events",
        "user_id",
        "id event actor resource resource_id row_count occurred_at",
    ),
}


def settings():
    value = get_settings()
    if not value.enable_privacy_tools:
        raise FeatureUnavailable("Privacy tools require an approved operating policy")
    return value


def manifest():
    config = settings()
    return {
        "sections": list(SECTIONS),
        "policy_version": config.privacy_policy_version,
        "support_url": config.privacy_support_url,
        "excluded": [
            "authentication_credentials",
            "push_delivery_tokens",
            "internal_job_and_retry_payloads",
            "external_processor_records",
            "backups",
            "object_bytes",
            "invitation_credentials_and_submission_hashes",
        ],
    }


def export_page(user_id, section, limit=50, after=None):
    settings()
    if section not in SECTIONS or type(limit) is not int or not 1 <= limit <= 100:
        raise InvalidMutation("Invalid export section or page bound")
    if after is not None:
        try:
            after = UUID(str(after))
        except (ValueError, TypeError) as exc:
            raise InvalidMutation("Invalid export cursor") from exc
    table, owner, columns = SECTIONS[section]
    query = sql.SQL("SELECT {} FROM {} WHERE {}=%s").format(
        sql.SQL(",").join(map(sql.Identifier, columns.split())),
        sql.Identifier(table),
        sql.Identifier(owner),
    )
    params = [user_id]
    if after is not None:
        query += sql.SQL(" AND id>%s")
        params.append(after)
    query += sql.SQL(" ORDER BY id LIMIT %s")
    with transaction() as conn:
        rows = normalize(conn.execute(query, [*params, limit + 1]).fetchall())
        # Auditing audit-page reads would grow the very list being exported.
        if section not in {"audit", "care_audit"}:
            conn.execute(
                "SELECT enat_privacy_event(%s,%s)", (section, min(len(rows), limit))
            )
    return {
        "section": section,
        "generated_at": utc_now(),
        "records": rows[:limit],
        "next_cursor": rows[limit - 1]["id"] if len(rows) > limit else None,
    }


def create_deletion_request(user_id, key):
    settings()

    def action():
        with transaction() as conn:
            return conn.execute("SELECT enat_privacy_request() AS value").fetchone()[
                "value"
            ]

    return idempotency.execute(
        user_id, "privacy.deletion", key, {"confirm": True}, action
    )


def cancel_request(user_id, request_id):
    settings()
    with transaction() as conn:
        result = conn.execute(
            "SELECT enat_privacy_request(%s) AS value", (request_id,)
        ).fetchone()["value"]
    if result is None:
        raise NotFound("Privacy request not found")
    return normalize(result)
