from datetime import date, datetime, time, timedelta

from app.core.clock import LOCAL_ZONE, as_utc, utc_now
from app.core.errors import InvalidMutation
from app.db import idempotency
from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.check_ins import CheckInRepository
from app.db.repositories.summaries import SummaryRepository
from app.db.repositories.users import UserRepository
from app.services.anc_schedule import (
    _CONTACT_BY_NUM,
    WHO_ANC_CONTACTS,
    get_next_anc_contact,
)
from app.services.clinical_policy import POLICY_VERSION, confirmed_items, danger
from app.services.extraction import _category_display
from app.services.nutrition import calculate_food_group_shares, classify_ethiopian_food


def _parse_datetime(value):
    return as_utc(value)


def _provenance(item, checkin):
    return {
        "check_in_id": checkin.get("id"),
        "source_item_id": item.get("source_item_id") or item.get("item_id"),
        "confirmed_at": item.get("confirmed_at"),
        "source": item.get("source", "legacy"),
        "policy_version": item.get("policy_version"),
        "prompt_version": item.get("prompt_version"),
        "model_version": item.get("model_version"),
        "confirmation_provenance": "recorded"
        if item.get("confirmed_at")
        else "legacy_timestamp_unknown",
    }


class SummaryService:
    def __init__(self, clock=utc_now):
        self.clock = clock
        self.summaries = SummaryRepository(clock)
        self.check_ins = CheckInRepository(clock)
        self.appointments = AppointmentRepository(clock)
        self.users = UserRepository()

    def _resolve_fetch_window(self, user, period_end):
        start = max(as_utc(user["created_at"]), period_end - timedelta(days=30))
        apt = self.appointments.get_by_user(user["id"])
        if apt and apt.get("previous_appointment_date"):
            previous = datetime.combine(
                date.fromisoformat(str(apt["previous_appointment_date"])[:10]),
                time.min,
                LOCAL_ZONE,
            )
            start = max(start, as_utc(previous))
        return start

    def _fetch_check_ins(self, user_id, start_dt, end_dt):
        # Direct PostgreSQL query has no PostgREST page cap. Empty stays empty;
        # database failures propagate as a retriable DataUnavailable error.
        return self.check_ins.list_in_period(user_id, start_dt, end_dt)

    def generate(
        self,
        user_id,
        *,
        period_start=None,
        period_end=None,
        key=None,
        generation_key=None,
    ):
        request = {
            "period_start": period_start,
            "period_end": period_end,
            "generation_key": generation_key,
        }

        def action():
            user = self.users.get_by_id(user_id)
            if not user:
                raise InvalidMutation("User not found")
            if generation_key:
                existing = self.summaries.get_by_generation_key(user_id, generation_key)
                if existing:
                    return existing
            end = as_utc(period_end) if period_end is not None else self.clock()
            start = (
                as_utc(period_start)
                if period_start is not None
                else self._resolve_fetch_window(user, end)
            )
            if start >= end or end > self.clock() or end - start > timedelta(days=366):
                raise InvalidMutation("Invalid report window")
            records = self._fetch_check_ins(user_id, start, end)
            apt = self.appointments.get_by_user(user_id)
            contact = (
                _CONTACT_BY_NUM.get(apt.get("anc_contact_number")) if apt else None
            )
            if not contact:
                lnmp = user.get("effective_lnmp_date") or user.get("lnmp_date")
                contact = (
                    get_next_anc_contact(
                        date.fromisoformat(str(lnmp)[:10]),
                        self.clock().astimezone(LOCAL_ZONE).date(),
                    )
                    if lnmp
                    else WHO_ANC_CONTACTS[0]
                )
            anc = {
                "contact_number": contact["contact_number"],
                "title_en": contact["title_en"],
                "title_am": contact["title_am"],
                "target_gestational_weeks": contact["gestational_weeks"],
                "trimester": contact["trimester"],
                "schedule_next_weeks": contact["schedule_next_weeks"],
            }
            content = self._aggregate(records, period_start=start, period_end=end)
            content.update(
                anc_contact=anc,
                policy_version=POLICY_VERSION,
                window={
                    "start": start.isoformat(),
                    "end_exclusive": end.isoformat(),
                    "calendar_timezone": "Africa/Addis_Ababa",
                },
            )
            snapshot = self.summaries.create(
                user_id,
                {
                    "period_start": start.astimezone(LOCAL_ZONE).date().isoformat(),
                    "period_end": (end - timedelta(microseconds=1))
                    .astimezone(LOCAL_ZONE)
                    .date()
                    .isoformat(),
                    "window_start": start.isoformat(),
                    "window_end": end.isoformat(),
                    "generation_key": generation_key,
                    "content_json": content,
                    "share_link_slug": None,
                    "qr_code_url": None,
                    "anc_contact_number": anc["contact_number"],
                    "anc_contact_title": anc["title_en"],
                    "anc_contact_title_am": anc["title_am"],
                    "target_gestational_weeks": anc["target_gestational_weeks"],
                },
            )
            idempotency.emit(user_id, "summary.created", snapshot["id"])
            return snapshot

        # Automatic snapshots use a stable identity, independent of patient retry keys.
        if generation_key:
            return idempotency.execute(
                user_id,
                "summary:auto",
                idempotency.request_hash(generation_key),
                {"generation_key": generation_key},
                action,
            )
        return idempotency.execute(user_id, "summary:generate", key, request, action)

    def get_latest(self, user_id):
        return self.summaries.get_latest(user_id)

    def get_public(self, slug):
        from app.services.sharing import read_share

        return read_share(slug)

    def check_and_generate_auto_summary(self, user_id):
        user = self.users.get_by_id(user_id)
        if not user:
            return None
        apt = self.appointments.get_by_user(user_id)
        now = self.clock()
        today = now.astimezone(LOCAL_ZONE).date()
        if apt and apt.get("status", "scheduled") == "scheduled":
            apt_date = date.fromisoformat(str(apt["appointment_date"])[:10])
            if 0 <= (apt_date - today).days <= 1:
                reason = "pre_appointment_1_day_before"
                generation_key = f"{reason}:{apt.get('id')}:{apt_date}:{apt.get('anc_contact_number')}"
            else:
                return None
        else:
            latest = self.summaries.get_latest(user_id)
            reference = as_utc(latest["generated_at"] if latest else user["created_at"])
            if now - reference < timedelta(days=30):
                return None
            reason = "monthly_auto_summary"
            generation_key = f"{reason}:{today.year}-{today.month:02d}"
        # No appointment mutation. Concurrent schedulers converge on one snapshot.
        result = self.generate(user_id, generation_key=generation_key)
        return {**result, "auto_reason": reason}

    @staticmethod
    def _aggregate(check_ins, period_start=None, period_end=None):
        dangers, symptoms, foods, closing, supplements = [], [], [], [], []
        observations = {}
        for record in check_ins:
            timestamp = (
                record.get("timestamp")
                or record.get("created_at")
                or record.get("date")
            )
            if not timestamp:
                continue
            instant = as_utc(timestamp)
            if period_start is not None and instant < as_utc(period_start):
                continue
            if period_end is not None and instant >= as_utc(period_end):
                continue
            day = instant.astimezone(LOCAL_ZONE).date().isoformat()
            for item in confirmed_items(record.get("symptoms")):
                is_danger = danger(item)
                category = item.get("category") if is_danger else None
                entry = {
                    "date": day,
                    "category": category,
                    "category_display": _category_display(category, "am"),
                    "category_display_en": _category_display(category, "en"),
                    "raw_text": item.get("raw_text", ""),
                    "duration": item.get("duration"),
                    "severity": item.get("severity") or "unspecified",
                    "assessment": "recognized_danger_category"
                    if is_danger
                    else "unclassified",
                    **_provenance(item, record),
                }
                (dangers if is_danger else symptoms).append(entry)
            for item in confirmed_items(record.get("food_log")):
                foods.append(
                    {
                        "date": day,
                        "raw_text": item.get("raw_text", ""),
                        "items": item.get("items") or [],
                        "food_groups": item.get("food_groups")
                        or classify_ethiopian_food(item.get("raw_text")),
                        **_provenance(item, record),
                    }
                )
            for item in confirmed_items(record.get("supplement_check")):
                name = str(item.get("supplement_name") or "unknown").strip()
                value = item.get("taken_today")
                value = value if type(value) is bool else None
                supplements.append(
                    {
                        "date": day,
                        "supplement_name": name,
                        "taken_today": value,
                        **_provenance(item, record),
                    }
                )
                if name.casefold() not in ("unknown", "other", "none", ""):
                    observations.setdefault((name.casefold(), day), set()).add(value)
            for item in confirmed_items(record.get("closing_mentions")):
                closing.append(
                    {
                        "date": day,
                        "topic": item.get("topic"),
                        "raw_text": item.get("raw_text", ""),
                        **_provenance(item, record),
                    }
                )
        period_days = 0
        if period_start is not None and period_end is not None:
            first = as_utc(period_start).astimezone(LOCAL_ZONE).date()
            last = (
                (as_utc(period_end) - timedelta(microseconds=1))
                .astimezone(LOCAL_ZONE)
                .date()
            )
            period_days = max(0, (last - first).days + 1)
        adherence = None
        if observations:
            details = []
            for name in sorted({name for name, _ in observations}):
                daily = {
                    day: values
                    for (n, day), values in observations.items()
                    if n == name
                }
                taken = sum(v == {True} for v in daily.values())
                not_taken = sum(v == {False} for v in daily.values())
                known = taken + not_taken
                total = period_days or len(daily)
                details.append(
                    {
                        "supplement_name": name,
                        "taken_days": taken,
                        "not_taken_days": not_taken,
                        "tracked_days": known,
                        "unknown_days": max(0, total - known),
                        "percentage": round(taken / known * 100) if known else None,
                    }
                )
            known = sum(d["tracked_days"] for d in details)
            taken = sum(d["taken_days"] for d in details)
            adherence = {
                "by_supplement": details,
                "taken_days": taken,
                "tracked_days": known,
                "total_reported": known,
                "total_days_in_period": period_days,
                "percentage": round(taken / known * 100) if known else None,
                "tracked_percentage": round(taken / known * 100) if known else None,
                "denominator": "known supplement-day observations; missing or conflicting reports are unknown",
            }
        return {
            "danger_signs": dangers,
            "general_symptoms": symptoms,
            "recorded_symptoms": symptoms,
            "food_logs": foods,
            "nutritional_variation": calculate_food_group_shares(foods),
            "supplement_observations": supplements,
            "supplement_adherence": adherence,
            "closing_mentions": closing,
            "muac_reminder": "MUAC screening due — check at visit",
            "provenance_note": "Confirmed patient self-report; missing confirmation is excluded. This report is not a diagnosis.",
        }
