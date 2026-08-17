from datetime import date, datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.check_ins import CheckInRepository
from app.db.repositories.summaries import SummaryRepository
from app.db.repositories.users import UserRepository
from app.services.extraction import _category_display
from app.services.qr import (
    build_share_url,
    generate_share_slug,
    upload_qr_code,
)

_MUAC_REMINDER = "MUAC screening due — check at visit"
_PROVENANCE_NOTE = (
    "All data in this summary is self-reported by the patient "
    "(no device-measured data)."
)


def _parse_datetime(val: str | datetime | date | None) -> datetime:
    if not val:
        return datetime.utcnow()
    if isinstance(val, datetime):
        dt = val
    elif isinstance(val, date):
        dt = datetime.combine(val, datetime.min.time())
    else:
        clean_str = str(val).replace("Z", "+00:00")
        if len(clean_str) == 10 and "-" in clean_str:
            dt = datetime.fromisoformat(f"{clean_str}T00:00:00")
        else:
            dt = datetime.fromisoformat(clean_str)
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


class SummaryService:
    def __init__(self) -> None:
        self.summaries = SummaryRepository()
        self.check_ins = CheckInRepository()
        self.appointments = AppointmentRepository()
        self.users = UserRepository()

    def _resolve_period_start(
        self, user: dict[str, Any], period_end: datetime
    ) -> datetime:
        created_at = _parse_datetime(user.get("created_at"))
        default_start = min(created_at, period_end - timedelta(days=30))
        apt = self.appointments.get_by_user(user["id"])
        if apt and apt.get("previous_appointment_date"):
            return _parse_datetime(apt["previous_appointment_date"])
        return default_start

    def _fetch_check_ins(
        self, user_id: UUID, start_dt: datetime, end_dt: datetime
    ) -> tuple[list[dict[str, Any]], datetime]:
        try:
            records = self.check_ins.list_in_period(
                user_id, start_dt, end_dt
            )
            if records:
                return records, start_dt
        except Exception:
            pass

        if hasattr(self.check_ins, "list_by_user"):
            records = self.check_ins.list_by_user(user_id) or []
            if records:
                dates = [
                    _parse_datetime(
                        r.get("timestamp") or r.get("created_at")
                    )
                    for r in records
                    if r.get("timestamp") or r.get("created_at")
                ]
                return records, (min(dates) if dates else start_dt)
        return [], start_dt

    def generate(self, user_id: UUID) -> dict[str, Any]:
        user = self.users.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        period_end = datetime.utcnow()
        init_start = self._resolve_period_start(user, period_end)
        check_ins, period_start = self._fetch_check_ins(
            user_id, init_start, period_end
        )

        content_json = self._aggregate(check_ins)
        slug = generate_share_slug()
        share_url = build_share_url(slug)
        qr_code_url = upload_qr_code(slug, share_url)

        summary = self.summaries.create(
            user_id,
            {
                "period_start": period_start.date().isoformat(),
                "period_end": period_end.date().isoformat(),
                "content_json": content_json,
                "share_link_slug": slug,
                "qr_code_url": qr_code_url,
            },
        )

        apt = self.appointments.get_by_user(user_id)
        if apt:
            self.appointments.update_last_summary_generated_at(
                user_id, period_end
            )

        return summary

    def get_latest(self, user_id: UUID) -> dict[str, Any] | None:
        return self.summaries.get_latest(user_id)

    def get_public(self, slug: str) -> dict[str, Any] | None:
        return self.summaries.get_by_slug(slug)

    def check_and_generate_auto_summary(
        self, user_id: UUID
    ) -> dict[str, Any] | None:
        user = self.users.get_by_id(user_id)
        if not user:
            return None

        apt = self.appointments.get_by_user(user_id)
        today, now = date.today(), datetime.utcnow()

        if apt and apt.get("appointment_date"):
            apt_date = date.fromisoformat(apt["appointment_date"])
            if 0 <= (apt_date - today).days <= 1:
                last_gen = apt.get("last_summary_generated_at")
                if not last_gen or (now - _parse_datetime(last_gen)).days >= 3:
                    summary = self.generate(user_id)
                    summary["auto_reason"] = "pre_appointment_1_day_before"
                    return summary
        else:
            latest = self.summaries.get_latest(user_id)
            prev_gen = latest.get("generated_at") if latest else None
            ref_dt = (
                _parse_datetime(prev_gen)
                if prev_gen
                else _parse_datetime(user.get("created_at"))
            )
            if (now - ref_dt).days >= 30:
                summary = self.generate(user_id)
                summary["auto_reason"] = "monthly_auto_summary"
                return summary
        return None

    @staticmethod
    def _extract_symptoms(
        check_in: dict[str, Any],
        date_str: str,
        danger_signs: list[dict[str, Any]],
        general_symptoms: list[dict[str, Any]],
    ) -> None:
        items = (
            check_in.get("symptoms")
            or check_in.get("symptom_items")
            or check_in.get("items")
            or []
        )
        for s in items:
            if not isinstance(s, dict) or s.get("confirmed") is False:
                continue
            text = (
                s.get("raw_text") or s.get("symptom") or s.get("name") or ""
            ).strip()
            if not text:
                continue

            raw_cat = s.get("category")
            is_danger = bool(s.get("danger_sign"))
            if (
                not raw_cat
                or raw_cat in ("none", "null", "no_danger_sign_detected")
                or not is_danger
            ):
                cat_key = "no_danger_sign_detected"
            else:
                cat_key = raw_cat

            entry = {
                "date": date_str,
                "category": cat_key,
                "category_display": _category_display(cat_key, lang="am"),
                "category_display_en": _category_display(cat_key, lang="en"),
                "raw_text": text,
                "duration": s.get("duration"),
                "severity": s.get("severity") or "unspecified",
            }
            if is_danger:
                danger_signs.append(entry)
            else:
                general_symptoms.append(entry)

    @staticmethod
    def _extract_food_logs(
        check_in: dict[str, Any],
        date_str: str,
        food_logs: list[dict[str, Any]],
    ) -> None:
        foods = (
            check_in.get("food_log")
            or check_in.get("food_logs")
            or check_in.get("foods")
        )
        if isinstance(foods, list):
            for f in foods:
                text = (
                    f.get("raw_text") if isinstance(f, dict) else str(f)
                ) or ""
                if text.strip():
                    food_logs.append({"date": date_str, "raw_text": text.strip()})
        elif isinstance(foods, dict) and foods.get("confirmed") is not False:
            text = (foods.get("raw_text") or "").strip()
            if text:
                food_logs.append({"date": date_str, "raw_text": text})
        elif isinstance(foods, str) and foods.strip():
            food_logs.append({"date": date_str, "raw_text": foods.strip()})

    @staticmethod
    def _aggregate(check_ins: list[dict[str, Any]]) -> dict[str, Any]:
        danger_signs: list[dict[str, Any]] = []
        general_symptoms: list[dict[str, Any]] = []
        food_logs: list[dict[str, Any]] = []
        closing_mentions: list[dict[str, Any]] = []
        supp_taken, supp_tracked = 0, 0

        for c in check_ins:
            raw_ts = (
                c.get("timestamp") or c.get("created_at") or c.get("date") or ""
            )
            c_date = str(raw_ts)[:10]

            SummaryService._extract_symptoms(
                c, c_date, danger_signs, general_symptoms
            )
            SummaryService._extract_food_logs(c, c_date, food_logs)

            supp = (
                c.get("supplement_check")
                or c.get("supplement")
                or c.get("supplements")
            )
            if (
                isinstance(supp, dict)
                and supp.get("confirmed") is not False
            ):
                supp_tracked += 1
                if supp.get("taken_today") or supp.get("taken"):
                    supp_taken += 1

            for m in c.get("closing_mentions") or []:
                if isinstance(m, dict) and m.get("confirmed") is not False:
                    m_text = (m.get("raw_text") or "").strip()
                    if m_text:
                        closing_mentions.append(
                            {
                                "date": c_date,
                                "topic": m.get("topic"),
                                "raw_text": m_text,
                            }
                        )

        adherence = None
        if supp_tracked > 0:
            adherence = {
                "taken_days": supp_taken,
                "tracked_days": supp_tracked,
                "total_reported": supp_tracked,
                "percentage": round((supp_taken / supp_tracked) * 100),
            }

        return {
            "danger_signs": danger_signs,
            "general_symptoms": general_symptoms,
            "food_logs": food_logs,
            "supplement_adherence": adherence,
            "closing_mentions": closing_mentions,
            "muac_reminder": _MUAC_REMINDER,
            "provenance_note": _PROVENANCE_NOTE,
        }
