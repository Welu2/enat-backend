from datetime import date, datetime, timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_current_user


@pytest.fixture
def test_user() -> dict:
    return {
        "id": str(uuid4()),
        "email": "mother@example.com",
        "created_at": datetime.utcnow().isoformat(),
        "onboarding_completed": False,
    }


def test_public_calculate_gestational_age_endpoint() -> None:
    client = TestClient(app)
    payload = {
        "pregnancy_counting_method": "lnmp",
        "lnmp_date": "2026-05-01",
        "as_of_date": "2026-08-25",
    }
    response = client.post("/users/calculate-gestational-age", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["gestational_age_weeks"] == 16
    assert data["gestational_age_days"] == 4
    assert data["trimester"] == "second_trimester"
    assert data["trimester_info"]["number"] == 2
    assert data["estimated_due_date"] == "2027-02-05"


def test_onboarding_submission_and_supplement_seeding(test_user: dict) -> None:
    app.dependency_overrides[get_current_user] = lambda: test_user
    client = TestClient(app)

    user_db = dict(test_user)
    created_supplements = []

    def mock_update_profile(user_id, update_data):
        user_db.update(update_data)
        return user_db

    def mock_get_by_id(user_id):
        return user_db

    def mock_supp_create(user_id, data):
        supp_record = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "created_at": datetime.utcnow().isoformat(),
            **data,
        }
        created_supplements.append(supp_record)
        return supp_record

    def mock_supp_list_all(user_id):
        return created_supplements

    with patch("app.api.routes.users.UserRepository.update_profile", side_effect=mock_update_profile), \
         patch("app.api.routes.users.UserRepository.get_by_id", side_effect=mock_get_by_id), \
         patch("app.api.routes.users.SupplementRepository.create", side_effect=mock_supp_create), \
         patch("app.api.routes.users.SupplementRepository.list_all", side_effect=mock_supp_list_all), \
         patch("app.api.routes.users.AppointmentRepository.get_by_user", return_value=None), \
         patch("app.api.routes.users.AppointmentRepository.create", return_value={"id": str(uuid4())}), \
         patch("app.api.routes.users.ReminderRepository.list_pending", return_value=[]):

        onboarding_payload = {
            "age": 26,
            "area": "urban",
            "pregnancy_counting_method": "lnmp",
            "lnmp_date": (date.today() - timedelta(days=70)).isoformat(),
            "total_pregnancies": 2,
            "live_births": 1,
            "had_c_section": False,
            "child_passed_away": False,
            "past_pregnancy_complications": ["preterm_birth"],
            "known_medical_conditions": ["hypertension", "other"],
            "custom_medical_condition": "Mild asthma",
            "malaria_endemic_area": True,
            "current_medications": "Methyldopa 250mg",
            "supplements": ["iron & folic acid", "calcium"],
            "hospital": "St. Paul's Hospital Millennium Medical College",
        }

        response = client.post("/users/me/onboarding", json=onboarding_payload)
        assert response.status_code == 200
        data = response.json()

        assert data["age"] == 26
        assert data["area"] == "urban"
        assert data["onboarding_completed"] is True
        assert data["hospital"] == "St. Paul's Hospital Millennium Medical College"
        assert data["gestational_age_weeks"] == 10
        assert data["trimester"] == "first_trimester"
        assert data["total_pregnancies"] == 2
        assert data["live_births"] == 1
        assert data["had_c_section"] is False
        assert data["malaria_endemic_area"] is True
        assert data["custom_medical_condition"] == "Mild asthma"
        assert data["current_pregnancy_status"] is not None
        assert data["current_pregnancy_status"]["gestational_age_weeks"] == 10

        # Verify supplements were seeded into the supplements repo
        assert len(created_supplements) == 2
        supp_names = [s["name"] for s in created_supplements]
        assert "iron & folic acid" in supp_names
        assert "calcium" in supp_names

    app.dependency_overrides.clear()


def test_update_hospital_endpoint(test_user: dict) -> None:
    app.dependency_overrides[get_current_user] = lambda: test_user
    client = TestClient(app)

    user_db = dict(test_user)

    def mock_update_hospital(user_id, hospital):
        user_db["hospital"] = hospital
        return user_db

    def mock_get_by_id(user_id):
        return user_db

    with patch("app.api.routes.users.UserRepository.update_hospital", side_effect=mock_update_hospital), \
         patch("app.api.routes.users.UserRepository.get_by_id", side_effect=mock_get_by_id), \
         patch("app.api.routes.users.SupplementRepository.list_all", return_value=[]), \
         patch("app.api.routes.users.AppointmentRepository.get_by_user", return_value=None), \
         patch("app.api.routes.users.ReminderRepository.list_pending", return_value=[]):

        resp = client.put("/users/me/hospital", json={"hospital": "Tikur Anbessa Specialized Hospital"})
        assert resp.status_code == 200
        assert resp.json()["hospital"] == "Tikur Anbessa Specialized Hospital"

    app.dependency_overrides.clear()
