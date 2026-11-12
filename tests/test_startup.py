import importlib
import pkgutil
import socket

import pytest
import pytest_socket
from fastapi.testclient import TestClient
from pydantic import ValidationError

import app
from app.config import Settings
from app.main import create_app


def settings_for(**overrides):
    if overrides.get("environment") in {"staging", "production"}:
        overrides = {
            "database_url": "postgresql://enat_app@localhost/test",
            "enable_request_limits": True,
            **overrides,
        }
    return Settings(_env_file=None, **overrides)


def test_all_application_modules_import():
    for module in pkgutil.walk_packages(app.__path__, prefix="app."):
        importlib.import_module(module.name)


def test_network_guard_blocks_outbound_access():
    with pytest.raises(pytest_socket.SocketBlockedError):
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def test_default_lifespan_has_no_scheduled_work():
    from app.services.provider_runtime import _runtimes

    application = create_app(settings_for())
    for _ in range(2):
        with TestClient(application) as client:
            assert client.get("/health").json() == {"status": "ok"}
            assert len(_runtimes) == 1
        assert not _runtimes


def test_development_scheduler_shuts_down_on_lifespan_error():
    with pytest.raises(ValidationError, match="Embedded scheduling has been removed"):
        settings_for(enable_embedded_scheduler=True)


def test_worker_settings_need_no_api_or_provider_credentials():
    settings = settings_for(
        environment="production",
        process_role="worker",
        worker_database_url="postgresql://enat_worker@localhost/test",
        database_url="",
        supabase_url="",
        supabase_service_role_key="",
        addis_api_key="",
        supabase_publishable_key="",
        rate_limit_secret="",
    )
    with pytest.raises(ValueError, match="cannot start the API"):
        create_app(settings)


@pytest.mark.parametrize(
    "environment", ["development", "test", "staging", "production"]
)
def test_debug_routes_absent_by_default(environment):
    application = create_app(
        settings_for(
            environment=environment,
            public_base_url="https://frontend.example.org",
            cors_origins="https://frontend.example.org",
        )
    )
    paths = application.openapi()["paths"]
    assert "/dev/asr-test" not in paths
    assert "/reminders/run-daily" not in paths
    assert "/reminders" in paths
    with TestClient(application) as client:
        assert client.post("/dev/asr-test").status_code == 404
        assert client.post("/reminders/run-daily").status_code == 404


def test_development_routes_require_opt_in():
    paths = create_app(settings_for(enable_dev_routes=True)).openapi()["paths"]
    assert "/dev/asr-test" in paths
    assert "/reminders/run-daily" in paths


@pytest.mark.parametrize("environment", ["staging", "production"])
@pytest.mark.parametrize(
    "overrides",
    [
        {"enable_dev_routes": True},
        {"enable_embedded_scheduler": True},
        {"public_base_url": "http://frontend.example.org"},
        {"public_base_url": "https://localhost"},
        {"public_base_url": "https://127.0.0.1"},
        {"supabase_url": "http://database.example.org"},
        {"addis_api_base_url": "http://provider.example.org"},
        {"cors_origins": "*"},
        {"cors_origins": ""},
        {"cors_origins": "https://*.example.org"},
        {"cors_origins": "https://frontend.example.org/path"},
        {"cors_origins": "https://user:password@frontend.example.org"},
        {"cors_origins": "https://localhost."},
        {"cors_origins": "https://[::1]"},
    ],
)
def test_unsafe_deployment_configuration_fails(environment, overrides):
    values = {
        "environment": environment,
        "public_base_url": "https://frontend.example.org",
        "cors_origins": "https://frontend.example.org",
        **overrides,
    }
    with pytest.raises(ValidationError):
        settings_for(**values)


def test_cors_uses_only_configured_origins():
    application = create_app(settings_for(cors_origins="https://frontend.example.org"))
    with TestClient(application) as client:
        allowed = client.options(
            "/health",
            headers={
                "Origin": "https://frontend.example.org",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert (
            allowed.headers["access-control-allow-origin"]
            == "https://frontend.example.org"
        )
        denied = client.options(
            "/health",
            headers={
                "Origin": "https://web.telegram.org",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert denied.status_code == 400
        assert "access-control-allow-origin" not in denied.headers
