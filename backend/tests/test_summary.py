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
    assert captured["fields"] == "period_start, period_end, generated_at, content_json"
    assert "email" not in captured["fields"]
    assert result is not None
