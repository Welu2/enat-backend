import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core import errors
from app.main import create_app
from app.models.user import OnboardingSubmitRequest


@pytest.mark.parametrize(
    "failure,status",
    [
        (errors.AuthenticationUnavailable, 503),
        (errors.DataUnavailable, 503),
        (errors.ProviderUnavailable, 503),
        (errors.ArtifactUnavailable, 503),
        (errors.FeatureUnavailable, 503),
        (errors.NotFound, 404),
        (errors.Conflict, 409),
        (errors.InvalidMutation, 422),
        (errors.ConsentRequired, 400),
        (errors.InvalidAudio, 415),
        (errors.PayloadTooLarge, 413),
        (errors.RateLimited, 429),
        (RuntimeError, 500),
    ],
)
def test_domain_errors_share_redacted_private_http_boundary(failure, status, caplog):
    app = create_app()

    @app.get("/injected-error")
    def fail():
        raise failure("PRIVATE patient detail or credential")

    response = TestClient(app).get("/injected-error")
    assert response.status_code == status
    assert "PRIVATE" not in response.text and "PRIVATE" not in caplog.text
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["x-request-id"]
    if failure is errors.ProviderUnavailable:
        assert response.json()["draft_preserved"] is True
        assert response.json()["recovery"] == ["retry", "manual_input"]


@pytest.mark.parametrize(
    "supplements", [[7], [{"name": "iron", "user_id": "other"}], [{}], [""]]
)
def test_onboarding_rejects_untyped_supplement_payloads(supplements):
    with pytest.raises(ValidationError):
        OnboardingSubmitRequest(supplements=supplements)


def test_unexpected_qr_bug_is_not_suppressed(monkeypatch):
    from app.services import qr

    def bug(*args):
        raise RuntimeError("programming error")

    monkeypatch.setattr(qr, "_render_png", bug)
    with pytest.raises(RuntimeError, match="programming error"):
        qr.generate_qr_png("https://example.org/share")


@pytest.mark.parametrize(
    "regression", ["authentication", "session_version", "error_envelope"]
)
def test_contract_gate_rejects_security_and_concurrency_regressions(regression):
    from scripts.check_contracts import invariants

    schema = create_app().openapi()
    operation = schema["paths"]["/checkin/{session_id}/complete"]["post"]
    if regression == "authentication":
        operation.pop("security")
    elif regression == "session_version":
        operation["parameters"] = [
            parameter
            for parameter in operation["parameters"]
            if parameter["name"] != "X-Session-Version"
        ]
    else:
        operation["responses"]["422"]["content"]["application/json"]["schema"] = {
            "type": "object"
        }
    with pytest.raises(SystemExit):
        invariants(schema)
