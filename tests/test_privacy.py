from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.config import Settings
from app.dependencies import get_current_user_id
from app.main import create_app
from app.models.privacy import DeletionRequest


@pytest.mark.parametrize(
    "payload",
    [
        {"confirm": False},
        {"confirm": "true"},
        {"confirm": 1},
        {"confirm": True, "user_id": "other"},
    ],
)
def test_deletion_requires_explicit_typed_confirmation(payload):
    with pytest.raises(ValidationError):
        DeletionRequest.model_validate(payload)


def test_privacy_is_disabled_until_configured_and_always_requires_auth():
    app = create_app()
    with TestClient(app) as client:
        assert client.get("/users/me/privacy/export").status_code == 401
        app.dependency_overrides[get_current_user_id] = lambda: UUID(int=1)
        response = client.get("/users/me/privacy/export")
        assert response.status_code == 503
        assert response.headers["cache-control"] == "no-store"
        assert (
            client.get("/users/me/privacy/export/check_ins?limit=101").status_code
            == 422
        )
        assert client.get("/users/me/privacy/export/credentials").status_code == 422
        assert (
            client.get("/users/me/privacy/export/check_ins?after=bad").status_code
            == 422
        )


@pytest.mark.parametrize(
    "policy,support",
    [
        ("", "https://support.invalid"),
        ("policy-1", "http://support.invalid"),
        ("policy-1", ""),
    ],
)
def test_enabling_privacy_requires_policy_and_support(policy, support):
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            enable_privacy_tools=True,
            privacy_policy_version=policy,
            privacy_support_url=support,
        )
