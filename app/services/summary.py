from datetime import date, datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.check_ins import CheckInRepository
from app.db.repositories.summaries import SummaryRepository
from app.db.repositories.users import UserRepository
from app.services.anc_schedule import (
    WHO_ANC_CONTACTS,
    _CONTACT_BY_NUM,
    advance_to_next_anc_contact,
    get_next_anc_contact,
)
from app.services.extraction import _category_display
from app.services.nutrition import calculate_food_group_shares, classify_ethiopian_food
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

    def _resolve_fetch_window(
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
    ) -> list[dict[str, Any]]:
        try:
            records = self.check_ins.list_in_period(
                user_id, start_dt, end_dt
            )
            if records:
                return records
        except Exception:
            pass

        if hasattr(self.check_ins, "list_by_user"):
            return self.check_ins.list_by_user(user_id) or []
        return []

    def generate(self, user_id: UUID) -> dict[str, Any]:
        user = self.users.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        period_end = datetime.utcnow()
        window_start = self._resolve_fetch_window(user, period_end)
        check_ins = self._fetch_check_ins(
            user_id, window_start, period_end
        )

        # Set period_start to the earliest actual check-in date
        if check_ins:
            dates = [
                _parse_datetime(
                    c.get("timestamp") or c.get("created_at") or c.get("date")
                )
                for c in check_ins
                if c.get("timestamp") or c.get("created_at") or c.get("date")
            ]
            period_start = min(dates) if dates else period_end
        else:
            period_start = period_end

        # Resolve ANC contact info
        apt = self.appointments.get_by_user(user_id)
        contact_spec = None
        if apt and apt.get("anc_contact_number"):
            contact_spec = _CONTACT_BY_NUM.get(apt["anc_contact_number"])
        if not contact_spec:
            eff_lnmp_str = user.get("effective_lnmp_date") or user.get("lnmp_date")
            if eff_lnmp_str:
                contact_spec = get_next_anc_contact(date.fromisoformat(eff_lnmp_str[:10]))
            else:
                contact_spec = WHO_ANC_CONTACTS[0]

        anc_info = {
            "contact_number": contact_spec.get("contact_number", 1),
            "title_en": contact_spec.get("title_en"),
            "title_am": contact_spec.get("title_am"),
            "target_gestational_weeks": contact_spec.get("gestational_weeks", 12),
            "trimester": contact_spec.get("trimester"),
            "schedule_next_weeks": contact_spec.get("schedule_next_weeks"),
        }

        content_json = self._aggregate(check_ins, period_start=period_start, period_end=period_end)
        content_json["anc_contact"] = anc_info

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
                "anc_contact_number": anc_info["contact_number"],
                "anc_contact_title": anc_info["title_en"],
                "anc_contact_title_am": anc_info["title_am"],
                "target_gestational_weeks": anc_info["target_gestational_weeks"],
            },
        )

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

                    # Advance to next WHO ANC contact appointment
                    current_contact_num = apt.get("anc_contact_number", 1) or 1
                    eff_lnmp_str = user.get("effective_lnmp_date") or user.get("lnmp_date")
                    eff_lnmp = date.fromisoformat(eff_lnmp_str[:10]) if eff_lnmp_str else None
                    next_anc = advance_to_next_anc_contact(
                        current_contact_num=current_contact_num,
                        current_appointment_date=apt_date,
                        effective_lnmp=eff_lnmp,
                    )
                    if next_anc:
                        self.appointments.upsert(
                            user_id,
                            {
                                "appointment_date": next_anc["appointment_date"],
                                "anc_contact_number": next_anc["contact_number"],
                                "anc_contact_title": next_anc["title_en"],
                                "anc_contact_title_am": next_anc["title_am"],
                                "target_gestational_weeks": next_anc["gestational_weeks"],
                                "previous_appointment_date": apt_date.isoformat(),
                            },
                        )

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
        seen_symptoms: set[tuple[str, str]],
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

            dedup_key = (date_str, text.lower())
            if dedup_key in seen_symptoms:
                continue
            seen_symptoms.add(dedup_key)

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
        seen_foods: set[tuple[str, str]],
    ) -> None:
        foods = (
            check_in.get("food_log")
            or check_in.get("food_logs")
            or check_in.get("foods")
        )
        items_to_add: list[dict[str, Any]] = []
        if isinstance(foods, list):
            for f in foods:
                text = (
                    f.get("raw_text") if isinstance(f, dict) else str(f)
                ) or ""
                groups = f.get("food_groups") if isinstance(f, dict) else None
                if text.strip():
                    items_to_add.append({"text": text.strip(), "groups": groups or classify_ethiopian_food(text)})
        elif isinstance(foods, dict) and foods.get("confirmed") is not False:
            text = (foods.get("raw_text") or "").strip()
            groups = foods.get("food_groups") or (classify_ethiopian_food(text) if text else [])
            if text or groups:
                items_to_add.append({"text": text or "የተመገቡት ምግብ", "groups": groups})
        elif isinstance(foods, str) and foods.strip():
            items_to_add.append({"text": foods.strip(), "groups": classify_ethiopian_food(foods)})

        for item_data in items_to_add:
            text = item_data["text"]
            dedup_key = (date_str, text.lower())
            if dedup_key not in seen_foods:
                seen_foods.add(dedup_key)
                food_logs.append({
                    "date": date_str,
                    "raw_text": text,
                    "food_groups": item_data["groups"],
                })

    @staticmethod
    def _aggregate(
        check_ins: list[dict[str, Any]],
        period_start: Any = None,
        period_end: Any = None,
    ) -> dict[str, Any]:
        danger_signs: list[dict[str, Any]] = []
        general_symptoms: list[dict[str, Any]] = []
        food_logs: list[dict[str, Any]] = []
        closing_mentions: list[dict[str, Any]] = []
        seen_symptoms: set[tuple[str, str]] = set()
        seen_foods: set[tuple[str, str]] = set()
        tracked_dates: set[str] = set()
        taken_dates: set[str] = set()

        for c in check_ins:
            raw_ts = (
                c.get("timestamp") or c.get("created_at") or c.get("date") or ""
            )
            c_date = str(raw_ts)[:10]
            if not c_date or len(c_date) < 10:
                continue

            SummaryService._extract_symptoms(
                c, c_date, danger_signs, general_symptoms, seen_symptoms
            )
            SummaryService._extract_food_logs(c, c_date, food_logs, seen_foods)

            supp = (
                c.get("supplement_check")
                or c.get("supplement")
                or c.get("supplements")
            )
            if isinstance(supp, dict) and supp.get("confirmed") is not False:
                tracked_dates.add(c_date)
                if supp.get("taken_today") or supp.get("taken"):
                    taken_dates.add(c_date)

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

        nutritional_variation = calculate_food_group_shares(food_logs)

        adherence = None
        total_tracked = len(tracked_dates)
        total_taken = len(taken_dates)

        total_days_in_period = total_tracked
        if period_start and period_end:
            p_start_d = period_start.date() if isinstance(period_start, datetime) else period_start
            p_end_d = period_end.date() if isinstance(period_end, datetime) else period_end
            if isinstance(p_start_d, str):
                p_start_d = date.fromisoformat(p_start_d)
            if isinstance(p_end_d, str):
                p_end_d = date.fromisoformat(p_end_d)
            if isinstance(p_start_d, date) and isinstance(p_end_d, date):
                total_days_in_period = max(1, (p_end_d - p_start_d).days + 1)

        if total_tracked > 0 or total_days_in_period > 0:
            pct = round((total_taken / total_days_in_period) * 100) if total_days_in_period > 0 else 0
            adherence = {
                "taken_days": total_taken,
                "tracked_days": total_tracked,
                "total_days_in_period": total_days_in_period,
                "total_reported": total_tracked,
                "percentage": pct,
                "tracked_percentage": round((total_taken / total_tracked) * 100) if total_tracked > 0 else 0,
            }

        return {
            "danger_signs": danger_signs,
            "general_symptoms": general_symptoms,
            "recorded_symptoms": general_symptoms,
            "food_logs": food_logs,
            "nutritional_variation": nutritional_variation,
            "supplement_adherence": adherence,
            "closing_mentions": closing_mentions,
            "muac_reminder": _MUAC_REMINDER,
            "provenance_note": _PROVENANCE_NOTE,
        }
