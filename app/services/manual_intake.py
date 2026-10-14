from app.core.clock import utc_now
from app.core.errors import InvalidMutation, NotFound
from app.db import idempotency
from app.db.repositories.check_ins import CheckInRepository
from app.db.repositories.supplements import SupplementRepository
from app.services.clinical_policy import normalize_item
from app.services.extraction import _supplement_display
from app.services.nutrition import classify_ethiopian_food


def log_food(user_id, payload, key, clock=utc_now):
    def action():
        raw = payload.raw_text or ", ".join(payload.items or payload.food_groups)
        if not raw:
            raise InvalidMutation("Food information required")
        groups = payload.food_groups or classify_ethiopian_food(raw)
        now = clock()
        # This form describes one meal observation. Preserve every supplied
        # item and the patient's explicit group selections together.
        items = [
            normalize_item(
                "food",
                {"raw_text": raw, "food_groups": groups, "items": payload.items},
                now=now,
                confirm=True,
            )
        ]
        record = CheckInRepository(clock).create(
            user_id,
            {
                "symptoms": [],
                "food_log": items,
                "supplement_check": [],
                "closing_mentions": [],
                "danger_sign_triggered": False,
            },
        )
        idempotency.emit(user_id, "checkin.completed", record["id"])
        return {
            "status": "verified",
            "food_groups": groups,
            "raw_text": raw,
            "logged_at": now,
        }

    return idempotency.execute(
        user_id, "manual:food", key, payload.model_dump(mode="json"), action
    )


def log_supplement(user_id, payload, target_id, key, clock=utc_now):
    def action():
        name = payload.supplement_name
        if target_id:
            match = next(
                (
                    s
                    for s in SupplementRepository().list_all(user_id)
                    if str(s["id"]) == str(target_id)
                ),
                None,
            )
            if not match:
                raise NotFound("Supplement not found")
            name = match["name"]
        if not name or name.casefold() in ("unknown", "other", "none"):
            raise InvalidMutation("Choose the supplement explicitly")
        raw = payload.raw_text or (
            f"የ{_supplement_display(name)} ወስጃለሁ"
            if payload.taken_today
            else f"የ{_supplement_display(name)} አልወሰድኩም"
        )
        now = clock()
        item = normalize_item(
            "supplement",
            {
                "raw_text": raw,
                "supplement_name": name,
                "taken_today": payload.taken_today,
            },
            now=now,
            confirm=True,
        )
        record = CheckInRepository(clock).create(
            user_id,
            {
                "symptoms": [],
                "food_log": [],
                "supplement_check": [item],
                "closing_mentions": [],
                "danger_sign_triggered": False,
            },
        )
        idempotency.emit(user_id, "checkin.completed", record["id"])
        # Unrelated reminders must not be dismissed. Explicit reminder dismissal
        # remains available; related-occurrence matching belongs to Phase 3.
        return {
            "status": "verified",
            "supplement_name": name,
            "taken_today": payload.taken_today,
            "logged_at": now,
        }

    return idempotency.execute(
        user_id,
        "manual:supplement",
        key,
        {
            "payload": payload.model_dump(mode="json"),
            "supplement_id": str(target_id) if target_id else None,
        },
        action,
    )
