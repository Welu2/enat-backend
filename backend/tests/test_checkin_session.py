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


def test_build_stage_order_includes_supplement_when_active(service: CheckInSessionService) -> None:
    user_id = uuid4()
    with patch.object(service.supplements, "list_active", return_value=[{"id": str(uuid4())}]):
        stages = service._build_stage_order(user_id)
    assert stages == ["symptoms", "food", "supplement", "closing"]


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
