from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.config import get_settings
from app.core.clock import utc_now
from app.core.errors import FeatureUnavailable, InvalidMutation
from app.main import create_app
from app.models.care import CareInviteRequest
from app.models.offline_checkin import OfflineCheckInRequest
from app.services import care_access, offline_checkin


def body():
    now = utc_now().isoformat()
    return {
        "schema_version": 1,
        "client_submission_id": str(uuid4()),
        "recorded_at": now,
        "client_confirmed_at": now,
        "confirmed": True,
        "symptoms": [{"raw_text": "No symptoms reported", "category": None}],
        "food_log": [],
        "supplement_check": [],
        "closing_mentions": [],
    }


@pytest.mark.parametrize(
    "change",
    [
        {"confirmed": False},
        {"confirmed": "true"},
        {"schema_version": True},
        {"schema_version": 2},
        {"schema_version": "1"},
        {"symptoms": []},
        {"recorded_at": "2026-10-22T08:30:00"},
        {"patient_id": str(uuid4())},
        {"danger_sign_triggered": False},
        {"symptoms": [{"raw_text": "test", "danger_sign": False}]},
        {"symptoms": [{"raw_text": "test", "category": "invented"}]},
        {"symptoms": [{"raw_text": "test"}] * 51},
        {"recorded_at": (utc_now() + timedelta(days=1)).isoformat()},
    ],
)
def test_offline_input_rejects_unconfirmed_invalid_and_server_owned_fields(change):
    with pytest.raises(ValidationError):
        OfflineCheckInRequest.model_validate({**body(), **change})


def test_total_item_limit_and_timezone_normalization():
    value = body()
    value.update(
        symptoms=[{"raw_text": "test"}] * 50,
        food_log=[{"raw_text": "meal"}] * 50,
        closing_mentions=[{"raw_text": "closing"}],
    )
    with pytest.raises(ValidationError):
        OfflineCheckInRequest.model_validate(value)
    value = body()
    value.update(
        recorded_at="2026-10-22T09:00:00+03:00",
        client_confirmed_at="2026-10-22T06:00:00Z",
    )
    request = OfflineCheckInRequest.model_validate(value)
    assert request.recorded_at == request.client_confirmed_at
    assert request.recorded_at.utcoffset() == timedelta(0)


def test_flags_default_off_and_no_self_assigned_clinician_role():
    config = get_settings()
    assert not config.enable_care_portal and not config.enable_offline_checkins
    with pytest.raises(FeatureUnavailable):
        care_access.require_portal()
    value = OfflineCheckInRequest.model_validate(body())
    with pytest.raises(FeatureUnavailable):
        offline_checkin.sync(uuid4(), value, str(value.client_submission_id))
    with pytest.raises(ValidationError):
        CareInviteRequest(recipient_id=uuid4(), relationship="clinician", consent=False)


def test_key_validation_occurs_before_database_access(monkeypatch):
    monkeypatch.setattr(
        offline_checkin,
        "get_settings",
        lambda: get_settings().model_copy(update={"enable_offline_checkins": True}),
    )
    value = OfflineCheckInRequest.model_validate(body())
    with pytest.raises(InvalidMutation):
        offline_checkin.sync(uuid4(), value, str(uuid4()))


def test_endpoints_require_authentication_and_keep_responses_private():
    client = TestClient(create_app())
    for path in ("/portal/me", "/portal/patients", "/users/me/care-connections"):
        response = client.get(path)
        assert response.status_code == 401
        assert response.headers["cache-control"] == "no-store"
    response = client.post("/checkin/offline-sync", json=body())
    assert response.status_code == 401
    assert UUID(response.headers["x-request-id"])
