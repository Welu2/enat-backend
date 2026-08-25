from datetime import datetime
from uuid import uuid4

from app.services.summary import SummaryService


def test_summary_aggregation_includes_only_confirmed_items() -> None:
    check_ins = [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "symptoms": [
                {
                    "confirmed": True,
                    "danger_sign": True,
                    "category": "severe_headache",
                    "raw_text": "headache",
                },
                {
                    "confirmed": False,
                    "danger_sign": True,
                    "category": "high_fever",
                    "raw_text": "fever",
                },
            ],
            "food_log": {"confirmed": True, "raw_text": "injera"},
            "supplement_check": {"confirmed": True, "taken_today": True},
            "closing_mentions": [
                {"confirmed": True, "topic": "breastfeeding_intent", "raw_text": "plan"}
            ],
        }
    ]

    content = SummaryService._aggregate(check_ins)
    assert len(content["danger_signs"]) == 1
    assert content["food_logs"][0]["raw_text"] == "injera"
    assert content["supplement_adherence"]["taken_days"] == 1
    assert content["closing_mentions"][0]["topic"] == "breastfeeding_intent"
    assert "nutritional_variation" in content
    assert content["nutritional_variation"]["percentages"]["grains"] == 100
    assert sum(content["nutritional_variation"]["percentages"].values()) == 100


def test_public_summary_repository_selects_limited_fields(monkeypatch) -> None:
    captured = {}

    class FakeQuery:
        def select(self, fields):
            captured["fields"] = fields
            return self

        def eq(self, *_):
            return self

        def maybe_single(self):
            return self

        def execute(self):
            class Result:
                data = {
                    "period_start": "2026-08-01",
                    "period_end": "2026-08-14",
                    "generated_at": "2026-08-14T09:00:00",
                    "content_json": {"danger_signs": []},
                }

            return Result()

    class FakeClient:
        def table(self, name):
            captured["table"] = name
            return FakeQuery()

    monkeypatch.setattr(
        "app.db.repositories.summaries.get_supabase_client",
        lambda: FakeClient(),
    )

    from app.db.repositories.summaries import SummaryRepository

    result = SummaryRepository().get_by_slug("abc123")
    assert "period_start" in captured["fields"]
    assert "content_json" in captured["fields"]
    assert "anc_contact_number" in captured["fields"]
    assert "email" not in captured["fields"]
    assert result is not None


def test_check_and_generate_auto_summary_pre_appointment(monkeypatch) -> None:
    from datetime import date, timedelta
    service = SummaryService()
    user_id = uuid4()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    monkeypatch.setattr(service.users, "get_by_id", lambda uid: {"id": str(uid), "created_at": "2026-01-01T00:00:00"})
    monkeypatch.setattr(
        service.appointments,
        "get_by_user",
        lambda uid: {"appointment_date": tomorrow, "last_summary_generated_at": None, "anc_contact_number": 1},
    )
    monkeypatch.setattr(
        service.appointments,
        "upsert",
        lambda uid, data: data,
    )
    monkeypatch.setattr(
        service,
        "generate",
        lambda uid: {"id": uuid4(), "auto_reason": "pre_appointment_1_day_before"},
    )

    result = service.check_and_generate_auto_summary(user_id)
    assert result is not None
    assert result["auto_reason"] == "pre_appointment_1_day_before"


def test_check_and_generate_auto_summary_monthly_fallback(monkeypatch) -> None:
    service = SummaryService()
    user_id = uuid4()

    monkeypatch.setattr(service.users, "get_by_id", lambda uid: {"id": str(uid), "created_at": "2026-01-01T00:00:00"})
    monkeypatch.setattr(service.appointments, "get_by_user", lambda uid: None)
    monkeypatch.setattr(
        service.summaries,
        "get_latest",
        lambda uid: {"generated_at": "2026-01-01T00:00:00"},
    )
    monkeypatch.setattr(
        service,
        "generate",
        lambda uid: {"id": uuid4(), "auto_reason": "monthly_auto_summary"},
    )

    result = service.check_and_generate_auto_summary(user_id)
    assert result is not None
    assert result["auto_reason"] == "monthly_auto_summary"
