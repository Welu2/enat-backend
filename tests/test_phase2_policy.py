from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from app.core.clock import local_day_bounds
from app.core.errors import DataUnavailable, InvalidMutation
from app.models.checkin import VerifyItemRequest
from app.services.anc_schedule import generate_checkin_summary_text
from app.services.clinical_policy import normalize_item
from app.services.summary import SummaryService


@pytest.mark.parametrize(
    "field,value",
    [
        ("item_id", "forged"),
        ("danger_sign", False),
        ("confirmed_at", "2026-01-01"),
        ("confirmed", True),
        ("policy_version", "forged"),
        ("source_item_id", "forged"),
        ("verification_phrase", "forged"),
        ("user_id", "another-user"),
    ],
)
def test_server_owned_correction_fields_rejected(field, value):
    with pytest.raises(ValidationError):
        VerifyItemRequest.model_validate(
            {"items": [{"item_id": "known", "corrected_value": {field: value}}]}
        )
    with pytest.raises(InvalidMutation):
        normalize_item("symptoms", {"raw_text": "test"}, {field: value})


@pytest.mark.parametrize(
    "fields",
    [
        {"category": "invented"},
        {"severity": "critical"},
        {"duration": {"value": -1, "unit": "day"}},
        {"duration": {"value": 3, "unit": "century"}},
        {"duration": {"value": "3", "unit": "day"}},
        {"duration": {"value": True, "unit": "day"}},
        {"duration": {"value": 3, "unit": "unspecified"}},
        {"duration": "three days"},
    ],
)
def test_malformed_clinical_fields_rejected(fields):
    with pytest.raises(InvalidMutation):
        normalize_item("symptoms", {"raw_text": "test", **fields})


@pytest.mark.parametrize("confirmed", [None, False, 1, "true", "false"])
def test_missing_or_non_boolean_confirmation_never_enters_report(confirmed):
    item = {
        "raw_text": "test",
        "category": "vaginal_bleeding",
        "supplement_name": "iron",
        "taken_today": True,
    }
    if confirmed is not None:
        item["confirmed"] = confirmed
    record = {
        "timestamp": "2026-10-10T12:00:00Z",
        "symptoms": [item],
        "food_log": [item],
        "supplement_check": [item],
        "closing_mentions": [item],
    }
    report = SummaryService._aggregate([record])
    assert (
        report["danger_signs"]
        == report["food_logs"]
        == report["closing_mentions"]
        == []
    )
    assert report["supplement_adherence"] is None
    assert (
        generate_checkin_summary_text([item])["summary_text_en"]
        == "No confirmed symptom assessment is available."
    )


def test_shared_policy_keeps_mild_category_in_extraction_correction_persistence_and_report():
    from app.services.clinical_policy import validated_draft
    from app.services.extraction import _attach_item_ids

    fields = {
        "raw_text": "test report",
        "category": "vaginal_bleeding",
        "severity": "mild",
    }
    extracted = _attach_item_ids("symptoms", {"symptoms": [fields]})[0]
    corrected = normalize_item(
        "symptoms", extracted, {"duration": {"value": 2, "unit": "day"}}, confirm=True
    )
    saved = validated_draft({"symptoms": [corrected]})
    report = SummaryService._aggregate([{**saved, "timestamp": "2026-10-10T12:00:00Z"}])
    assert (
        extracted["danger_sign"]
        and corrected["danger_sign"]
        and saved["symptoms"][0]["danger_sign"]
    )
    assert len(report["danger_signs"]) == 1
    assert report["danger_signs"][0]["source_item_id"] == extracted["item_id"]
    assert generate_checkin_summary_text(saved["symptoms"])["danger_sign_triggered"]


def test_adherence_missing_and_conflicting_observations_are_unknown():
    start = datetime(2026, 10, 1, tzinfo=timezone.utc)

    def record(day, value):
        return {
            "timestamp": start + timedelta(days=day),
            "supplement_check": [
                {"confirmed": True, "supplement_name": "iron", "taken_today": value}
            ],
        }

    result = SummaryService._aggregate(
        [
            record(0, True),
            record(1, False),
            record(2, True),
            record(2, False),
            record(3, None),
        ],
        start,
        start + timedelta(days=5),
    )
    detail = result["supplement_adherence"]["by_supplement"][0]
    assert detail["percentage"] == 50
    assert (
        detail["tracked_days"] == 2
        and detail["taken_days"] == 1
        and detail["not_taken_days"] == 1
    )
    assert detail["unknown_days"] >= 3


def test_local_midnight_uses_addis_calendar_not_utc_date():
    now = datetime(2026, 10, 12, 21, 30, tzinfo=timezone.utc)
    start, end = local_day_bounds(now)
    assert start == datetime(2026, 10, 12, 21, tzinfo=timezone.utc)
    assert end == datetime(2026, 10, 13, 21, tzinfo=timezone.utc)


def test_summary_empty_and_failed_period_queries_never_fall_back():
    service = SummaryService()
    service.check_ins.list_by_user = Mock(
        side_effect=AssertionError("all-history fallback")
    )
    service.check_ins.list_in_period = Mock(return_value=[])
    now = datetime.now(timezone.utc)
    assert service._fetch_check_ins("user", now - timedelta(days=1), now) == []
    service.check_ins.list_in_period.side_effect = DataUnavailable()
    with pytest.raises(DataUnavailable):
        service._fetch_check_ins("user", now - timedelta(days=1), now)
    service.check_ins.list_by_user.assert_not_called()
