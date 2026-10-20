import os

# Override inherited credentials before importing any application module.
os.environ.update(
    {
        "ENVIRONMENT": "test",
        "PROCESS_ROLE": "api",
        "WORKER_DATABASE_URL": "",
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "test-service-role-key",
        "SUPABASE_JWT_SECRET": "test-jwt-secret",
        "ADDIS_API_KEY": "test-addis-api-key",
        "ADDIS_API_BASE_URL": "https://provider.invalid",
        "PUBLIC_BASE_URL": "http://localhost:3000",
        "CORS_ORIGINS": "http://localhost:3000",
        "TELEGRAM_BOT_TOKEN": "",
        "ENABLE_DEV_ROUTES": "false",
        "ENABLE_EMBEDDED_SCHEDULER": "false",
        "REMINDER_CRON_HOUR": "6",
        "SUPABASE_PUBLISHABLE_KEY": "test-publishable-key",
        "DATABASE_URL": "",
        "ENABLE_REQUEST_LIMITS": "false",
        "ENABLE_SUMMARY_SHARING": "false",
        "ENABLE_PRIVACY_TOOLS": "false",
        "PRIVACY_POLICY_VERSION": "",
        "PRIVACY_SUPPORT_URL": "",
        "RATE_LIMIT_SECRET": "test-limit-secret-at-least-32-characters",
        "TRUSTED_HOSTS": "testserver,localhost",
        "LEGACY_HS256_UNTIL": "",
        "METRICS_TOKEN": "test-metrics-token-at-least-32-characters",
        "OTLP_ENDPOINT": "",
    }
)

# Install the network guard before collection (including application imports).
# Unix sockets are required by asyncio/TestClient; TCP/UDP and DNS stay blocked.
import pytest_socket

pytest_socket.disable_socket(allow_unix_socket=True)
