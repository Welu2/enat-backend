from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_current_user
from app.services.checkin_session import CheckInSessionService


@pytest.fixture
def test_user() -> dict:
    return {
        "id": str(uuid4()),
        "email": "mother@example.com",
        "created_at": datetime.utcnow().isoformat(),
    }


def test_manual_food_logging_endpoint(test_user: dict) -> None:
    app.dependency_overrides[get_current_user] = lambda: test_user
    client = TestClient(app)

    created_checkins = []

    def mock_create(user_id, data):
        checkin_record = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "timestamp": datetime.utcnow().isoformat(),
            **data,
        }
        created_checkins.append(checkin_record)
        return checkin_record

    with patch("app.api.routes.users.CheckInRepository.create", side_effect=mock_create):
        payload = {
            "food_groups": ["grains", "proteins", "fruits_and_vegetables"],
            "raw_text": "እንጀራ፣ ሽሮ እና ሰላጣ",
            "items": ["እንጀራ", "ሽሮ", "ሰላጣ"],
        }
        resp = client.post("/users/me/food/verify", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "verified"
        assert data["food_groups"] == ["grains", "proteins", "fruits_and_vegetables"]
        assert len(created_checkins) == 1
        assert created_checkins[0]["food_log"]["confirmed"] is True

    app.dependency_overrides.clear()


def test_build_stage_order_skips_food_when_already_logged_today() -> None:
    service = CheckInSessionService()
    user_id = uuid4()

    # Case 1: Neither food nor supplement logged today, user has active supplement
    with patch.object(service.check_ins, "has_food_logged_today", return_value=False), \
         patch.object(service.check_ins, "has_supplement_logged_today", return_value=False), \
         patch.object(service.supplements, "list_active", return_value=[{"name": "iron"}]):
        stages = service._build_stage_order(user_id)
        assert stages == ["symptoms", "food", "supplement", "closing"]

    # Case 2: Food logged today, supplement not logged today
    with patch.object(service.check_ins, "has_food_logged_today", return_value=True), \
         patch.object(service.check_ins, "has_supplement_logged_today", return_value=False), \
         patch.object(service.supplements, "list_active", return_value=[{"name": "iron"}]):
        stages = service._build_stage_order(user_id)
        assert stages == ["symptoms", "supplement", "closing"]

    # Case 3: Both food and supplement logged today
    with patch.object(service.check_ins, "has_food_logged_today", return_value=True), \
         patch.object(service.check_ins, "has_supplement_logged_today", return_value=True), \
         patch.object(service.supplements, "list_active", return_value=[{"name": "iron"}]):
        stages = service._build_stage_order(user_id)
        assert stages == ["symptoms", "closing"]
