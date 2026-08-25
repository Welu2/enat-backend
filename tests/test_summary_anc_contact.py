from datetime import date, datetime, timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_current_user
from app.services.summary import SummaryService


@pytest.fixture
def test_user() -> dict:
    return {
        "id": str(uuid4()),
        "email": "mother@example.com",
        "effective_lnmp_date": "2026-05-01",
        "lnmp_date": "2026-05-01",
        "estimated_due_date": "2027-02-05",
        "created_at": "2026-05-01T00:00:00",
    }


def test_summary_generation_attaches_anc_contact_metadata(test_user: dict) -> None:
    service = SummaryService()
    user_id = uuid4()

    user_data = {
        "id": str(user_id),
        "created_at": "2026-05-01T00:00:00",
        "effective_lnmp_date": "2026-05-01",
    }
    apt_data = {
        "id": str(uuid4()),
        "user_id": str(user_id),
        "appointment_date": "2026-07-24",
        "anc_contact_number": 1,
        "anc_contact_title": "1st ANC Contact (Up to 12 Weeks)",
        "anc_contact_title_am": "1ኛ የቅድመ ወሊድ ክትትል (እስከ 12 ሳምንት)",
        "target_gestational_weeks": 12,
    }

    check_ins = [
        {
            "timestamp": "2026-07-20T10:00:00",
            "symptoms": [
                {
                    "category": "severe_headache",
                    "danger_sign": True,
                    "raw_text": "ከባድ ራስ ምታት",
                    "confirmed": True,
                },
                {
                    "category": None,
                    "danger_sign": False,
                    "raw_text": "ቀላል ድካም",
                    "confirmed": True,
                },
            ],
            "food_log": {"raw_text": "እንጀራ በሽሮ", "food_groups": ["grains", "proteins"], "confirmed": True},
            "supplement_check": {"taken_today": True, "confirmed": True},
        }
    ]

    def mock_create_summary(uid, data):
        return {
            "id": str(uuid4()),
            "user_id": str(uid),
            "generated_at": datetime.utcnow().isoformat(),
            **data,
        }

    with patch.object(service.users, "get_by_id", return_value=user_data), \
         patch.object(service.appointments, "get_by_user", return_value=apt_data), \
         patch.object(service.check_ins, "list_in_period", return_value=check_ins), \
         patch.object(service.appointments, "update_last_summary_generated_at"), \
         patch("app.services.summary.upload_qr_code", return_value="https://qr.test.png"), \
         patch.object(service.summaries, "create", side_effect=mock_create_summary):

        summary = service.generate(user_id)

        assert summary["anc_contact_number"] == 1
        assert "1st ANC Contact" in summary["anc_contact_title"]
        assert summary["target_gestational_weeks"] == 12

        content = summary["content_json"]
        assert len(content["danger_signs"]) == 1
        assert len(content["recorded_symptoms"]) == 1
        assert content["recorded_symptoms"][0]["raw_text"] == "ቀላል ድካም"
        assert content["anc_contact"]["contact_number"] == 1
        assert content["anc_contact"]["schedule_next_weeks"] == 8


def test_auto_summary_advances_anc_appointment(test_user: dict) -> None:
    service = SummaryService()
    user_id = uuid4()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    user_data = {
        "id": str(user_id),
        "created_at": "2026-01-01T00:00:00",
        "effective_lnmp_date": "2026-01-01",
        "lnmp_date": "2026-01-01",
    }
    apt_data = {
        "id": str(uuid4()),
        "user_id": str(user_id),
        "appointment_date": tomorrow,
        "anc_contact_number": 1,
        "last_summary_generated_at": None,
    }

    upserted_apt = []

    def mock_upsert(uid, data):
        record = {"user_id": str(uid), **data}
        upserted_apt.append(record)
        return record

    with patch.object(service.users, "get_by_id", return_value=user_data), \
         patch.object(service.appointments, "get_by_user", return_value=apt_data), \
         patch.object(service, "generate", return_value={"id": str(uuid4())}), \
         patch.object(service.appointments, "upsert", side_effect=mock_upsert):

        res = service.check_and_generate_auto_summary(user_id)
        assert res is not None
        assert res["auto_reason"] == "pre_appointment_1_day_before"

        # Verify appointment advanced from Contact 1 to Contact 2
        assert len(upserted_apt) == 1
        assert upserted_apt[0]["anc_contact_number"] == 2
        assert upserted_apt[0]["target_gestational_weeks"] == 20


def test_get_user_anc_schedule_endpoint(test_user: dict) -> None:
    app.dependency_overrides[get_current_user] = lambda: test_user
    client = TestClient(app)

    with patch("app.api.routes.users.UserRepository.get_by_id", return_value=test_user):
        resp = client.get("/users/me/anc-schedule")
        assert resp.status_code == 200
        data = resp.json()
        assert "all_contacts" in data
        assert len(data["all_contacts"]) == 8
        assert "next_anc_contact" in data
        assert data["next_anc_contact"]["contact_number"] >= 1

    app.dependency_overrides.clear()
