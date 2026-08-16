from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from app.services.checkin_session import CheckInSessionService


@pytest.fixture
def service() -> CheckInSessionService:
    return CheckInSessionService()


def test_build_stage_order_skips_supplement_when_none_active(service: CheckInSessionService) -> None:
    user_id = uuid4()
    with patch.object(service.supplements, "list_active", return_value=[]):
        stages = service._build_stage_order(user_id)
    assert stages == ["symptoms", "food", "closing"]


def test_build_stage_order_includes_supplement_when_active_and_not_logged_today(service: CheckInSessionService) -> None:
    user_id = uuid4()
    with patch.object(service.supplements, "list_active", return_value=[{"id": str(uuid4())}]):
        with patch.object(service.check_ins, "has_supplement_logged_today", return_value=False):
            stages = service._build_stage_order(user_id)
    assert stages == ["symptoms", "food", "supplement", "closing"]


def test_build_stage_order_skips_supplement_when_already_logged_today(service: CheckInSessionService) -> None:
    user_id = uuid4()
    with patch.object(service.supplements, "list_active", return_value=[{"id": str(uuid4())}]):
        with patch.object(service.check_ins, "has_supplement_logged_today", return_value=True):
            stages = service._build_stage_order(user_id)
    assert stages == ["symptoms", "food", "closing"]


def test_verify_item_moves_confirmed_symptom_to_draft(service: CheckInSessionService) -> None:
    user_id = uuid4()
    session_id = uuid4()
    item_id = str(uuid4())
    session = {
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "food", "closing"],
        "draft_data": {"symptoms": [], "food_log": None, "supplement_check": None, "closing_mentions": []},
        "pending_items": [
            {
                "item_id": item_id,
                "raw_text": "headache",
                "category": "severe_headache",
                "confirmed": False,
            }
        ],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session):
        with patch.object(service.sessions, "update") as update_mock:
            result = service.verify_item(user_id, session_id, item_id, True, None)

    assert result["confirmed_count"] == 1
    update_mock.assert_called_once()
    draft_data = update_mock.call_args[0][2]["draft_data"]
    assert draft_data["symptoms"][0]["danger_sign"] is True


def test_verify_item_manual_edit_updates_phrase_and_danger_sign(service: CheckInSessionService) -> None:
    user_id = uuid4()
    session_id = uuid4()
    item_id = str(uuid4())
    session = {
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "food", "closing"],
        "draft_data": {"symptoms": [], "food_log": None, "supplement_check": None, "closing_mentions": []},
        "pending_items": [
            {
                "item_id": item_id,
                "raw_text": "mild headache",
                "category": "mild_headache",
                "confirmed": False,
            }
        ],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    corrected = {"category": "severe_headache", "duration": {"value": 3, "unit": "day"}}
    with patch.object(service, "_get_active_session", return_value=session):
        with patch.object(service.sessions, "update") as update_mock:
            result = service.verify_item(user_id, session_id, item_id, True, corrected)

    assert result["confirmed_count"] == 1
    draft = update_mock.call_args[0][2]["draft_data"]["symptoms"][0]
    assert draft["danger_sign"] is True
    assert "ከባድ ራስ ምታት" in draft["verification_phrase"]
    assert "3 ቀን" in draft["verification_phrase"]


@pytest.mark.asyncio
async def test_voice_correct_item_updates_pending_item(service: CheckInSessionService) -> None:
    user_id = uuid4()
    session_id = uuid4()
    item_id = str(uuid4())
    session = {
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "food", "closing"],
        "draft_data": {"symptoms": []},
        "pending_items": [
            {
                "item_id": item_id,
                "raw_text": "headache",
                "category": "severe_headache",
                "duration": {"value": 1, "unit": "day"},
                "confirmed": False,
            }
        ],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session):
        with patch.object(service.asr, "transcribe", new=pytest.importorskip("unittest.mock").AsyncMock(return_value="ሶስት ቀን ነው")):
            with patch.object(
                service.extraction,
                "extract",
                new=pytest.importorskip("unittest.mock").AsyncMock(
                    return_value=[{"category": "severe_headache", "duration": {"value": 3, "unit": "day"}}]
                ),
            ):
                with patch.object(service.sessions, "update"):
                    res = await service.voice_correct_item(user_id, session_id, item_id, b"audio", "correction.webm", "audio/webm")

    assert res["item_updated"] is True
    updated_item = res["pending_items"][0]
    assert updated_item["duration"] == {"value": 3, "unit": "day"}
    assert "3 ቀን" in updated_item["verification_phrase"]


def test_verify_items_bulk_confirms_multiple_items_at_once(service: CheckInSessionService) -> None:
    user_id = uuid4()
    session_id = uuid4()
    item1 = str(uuid4())
    item2 = str(uuid4())
    session = {
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "food", "closing"],
        "draft_data": {"symptoms": []},
        "pending_items": [
            {"item_id": item1, "raw_text": "ማቅለሽለሽ", "category": "persistent_nausea_vomiting", "confirmed": False},
            {"item_id": item2, "raw_text": "ትኩሳት", "category": "high_fever", "confirmed": False},
        ],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    items_payload = [
        {"item_id": item1, "confirmed": True},
        {"item_id": item2, "confirmed": True},
    ]

    with patch.object(service, "_get_active_session", return_value=session):
        with patch.object(service.sessions, "update") as update_mock:
            result = service.verify_item(user_id, session_id, items_payload=items_payload)

    assert result["confirmed_count"] == 2
    assert result["pending_items"] == []
    draft_data = update_mock.call_args[0][2]["draft_data"]
    assert len(draft_data["symptoms"]) == 2
