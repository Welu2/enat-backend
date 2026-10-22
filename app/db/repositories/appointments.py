from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.core.errors import NotFound
from app.db.data import get_data_client


class AppointmentRepository:
    def __init__(self, clock=None):
        from app.core.clock import utc_now

        self.clock = clock or utc_now

    def create(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        from app.core.errors import InvalidMutation
        from app.services.anc_schedule import _CONTACT_BY_NUM

        contact = data.get("anc_contact_number") or 1
        spec = _CONTACT_BY_NUM.get(contact)
        if not spec or not data.get("appointment_date"):
            raise InvalidMutation("Appointment date and valid contact required")
        data = {
            **data,
            "anc_contact_number": contact,
            "anc_contact_title": spec["title_en"],
            "anc_contact_title_am": spec["title_am"],
            "target_gestational_weeks": spec["gestational_weeks"],
        }
        client = get_data_client()
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            **data,
        }
        result = client.table("appointments").insert(payload).execute()
        return result.data[0]

    def update(self, user_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
        client = get_data_client()
        result = (
            client.table("appointments")
            .update(data)
            .eq("user_id", str(user_id))
            .execute()
        )
        if not result.data:
            raise NotFound("Appointment not found")
        return result.data[0]

    def get_by_user(self, user_id: UUID) -> dict[str, Any] | None:
        client = get_data_client()
        result = (
            client.table("appointments")
            .select("*")
            .eq("user_id", str(user_id))
            .maybe_single()
            .execute()
        )
        return result.data if result else None

    def update_last_summary_generated_at(
        self, user_id: UUID, generated_at: datetime
    ) -> None:
        client = get_data_client()
        client.table("appointments").update(
            {"last_summary_generated_at": generated_at.isoformat()}
        ).eq("user_id", str(user_id)).execute()

    def upsert(self, user_id, data):
        from app.core.errors import Conflict, InvalidMutation
        from app.db.data import transaction

        values = dict(data)
        version = values.pop("version", None)
        with transaction() as conn:
            conn.execute(
                "SELECT pg_advisory_xact_lock(hashtextextended(%s,0))",
                (f"appointment:{user_id}",),
            )
            existing = self.get_by_user(user_id)
            if existing:
                if version is None or version != existing["version"]:
                    raise Conflict("Supply the current appointment version")
                # Date changes are explicit reschedules, retaining an audit event.
                if "appointment_date" in values:
                    result = self.transition(
                        user_id,
                        "rescheduled",
                        version,
                        values.pop("appointment_date"),
                        values.pop("anc_contact_number", None),
                    )
                    values.pop("anc_contact_title", None)
                    values.pop("anc_contact_title_am", None)
                    values.pop("target_gestational_weeks", None)
                    return self.update(user_id, values) if values else result
                if any(
                    k.startswith("anc_") or k == "target_gestational_weeks"
                    for k in values
                ):
                    raise InvalidMutation(
                        "Use an explicit reschedule to change ANC contact"
                    )
                # Lock and compare once more in case an attendance transition raced.
                locked = conn.execute(
                    "SELECT version FROM appointments WHERE user_id=%s FOR UPDATE",
                    (user_id,),
                ).fetchone()
                if locked["version"] != version:
                    raise Conflict("Appointment changed")
                return self.update(user_id, {**values, "version": version + 1})
            if version is not None:
                raise Conflict("Appointment no longer exists")
            return self.create(user_id, values)

    def delete(self, user_id: UUID) -> bool:
        client = get_data_client()
        result = (
            client.table("appointments").delete().eq("user_id", str(user_id)).execute()
        )
        return bool(result.data if result else False)

    def transition(
        self, user_id, action, version, appointment_date=None, anc_contact_number=None
    ):
        from app.core.clock import LOCAL_ZONE
        from app.core.errors import Conflict, InvalidMutation, NotFound
        from app.db.data import normalize, transaction
        from app.services.anc_schedule import _CONTACT_BY_NUM

        with transaction() as conn:
            row = conn.execute(
                "SELECT * FROM appointments WHERE user_id=%s FOR UPDATE", (user_id,)
            ).fetchone()
            if not row:
                raise NotFound("Appointment not found")
            if row["version"] != version:
                raise Conflict("Appointment changed")
            if action not in ("completed", "missed", "rescheduled"):
                raise InvalidMutation("Unknown appointment action")
            if action != "rescheduled" and row["status"] != "scheduled":
                raise Conflict("Appointment already terminal")
            if (
                action != "rescheduled"
                and row["appointment_date"] > self.clock().astimezone(LOCAL_ZONE).date()
            ):
                raise InvalidMutation(
                    "Future appointments cannot be completed or missed"
                )
            data = {"status": "scheduled" if action == "rescheduled" else action}
            if action == "rescheduled":
                if not appointment_date:
                    raise InvalidMutation("Reschedule date required")
                data["appointment_date"] = appointment_date
                if anc_contact_number is not None:
                    spec = _CONTACT_BY_NUM.get(anc_contact_number)
                    if not spec:
                        raise InvalidMutation("Unknown ANC contact")
                    data.update(
                        anc_contact_number=anc_contact_number,
                        anc_contact_title=spec["title_en"],
                        anc_contact_title_am=spec["title_am"],
                        target_gestational_weeks=spec["gestational_weeks"],
                    )
            elif action == "completed":
                data["previous_appointment_date"] = row["appointment_date"].isoformat()
            from psycopg import sql

            assignments = sql.SQL(", ").join(
                sql.SQL("{}=%s").format(sql.Identifier(k)) for k in data
            )
            updated = conn.execute(
                sql.SQL(
                    "UPDATE appointments SET {},version=version+1 WHERE user_id=%s RETURNING *"
                ).format(assignments),
                [*data.values(), user_id],
            ).fetchone()
            conn.execute(
                "INSERT INTO appointment_events(user_id,appointment_id,action,previous_date,new_date) VALUES (%s,%s,%s,%s,%s)",
                (user_id, row["id"], action, row["appointment_date"], appointment_date),
            )
            return normalize(updated)
