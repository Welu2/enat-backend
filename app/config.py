from datetime import datetime, timedelta, timezone
from functools import lru_cache
from ipaddress import ip_address
from typing import Literal, Self
from urllib.parse import urlsplit

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _secure_url(value: str, *, origin_only: bool = False) -> bool:
    try:
        parsed = urlsplit(value)
        host = parsed.hostname
        port = parsed.port
    except ValueError:
        return False
    if (
        parsed.scheme != "https"
        or not host
        or "*" in value
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or port == 0
    ):
        return False
    host = host.rstrip(".").lower()
    if host == "localhost" or host.endswith(".localhost"):
        return False
    try:
        address = ip_address(host)
        if address.is_loopback or address.is_unspecified:
            return False
    except ValueError:
        pass
    return not origin_only or parsed.path == ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

    environment: Literal["development", "test", "staging", "production"] = "development"
    process_role: Literal["api", "worker"] = "api"
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""  # Deprecated; never used for local JWT verification.
    addis_api_key: str = ""
    addis_api_base_url: str = "https://api.addisassistant.com"
    public_base_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000"
    enable_dev_routes: bool = False
    # Retained only to reject obsolete deployments explicitly.
    enable_embedded_scheduler: bool = False
    reminder_cron_hour: int = Field(default=6, ge=0, le=23)
    telegram_bot_token: str = ""

    database_url: str = ""
    database_pool_size: int = Field(default=10, ge=1, le=30)
    worker_pool_size: int = Field(default=4, ge=1, le=10)
    metrics_token: str = ""
    otlp_endpoint: str = ""
    worker_database_url: str = ""
    provider_operation_seconds: float = Field(default=45, gt=0, le=60)
    provider_request_seconds: float = Field(default=20, gt=0, le=30)
    io_thread_limit: int = Field(default=16, ge=1, le=64)
    supabase_publishable_key: str = ""
    legacy_hs256_until: str = ""  # Explicit UTC deadline; default rejects HS256.
    telegram_max_age_seconds: int = Field(default=300, ge=30, le=600)
    telegram_clock_skew_seconds: int = Field(default=30, ge=0, le=60)
    enable_summary_sharing: bool = False
    enable_care_portal: bool = False
    enable_offline_checkins: bool = False
    enable_privacy_tools: bool = False
    privacy_policy_version: str = Field(default="", max_length=64)
    privacy_support_url: str = ""
    enable_request_limits: bool = True
    rate_limit_secret: str = ""
    trusted_hosts: str = "localhost,127.0.0.1,testserver"
    max_request_bytes: int = Field(default=8_000_000, ge=1024, le=16_000_000)
    max_audio_bytes: int = Field(default=6_000_000, ge=1024, le=12_000_000)
    max_audio_seconds: int = Field(default=120, ge=1, le=300)
    provider_daily_user_calls: int = Field(default=100, ge=1, le=1000)
    provider_daily_global_calls: int = Field(default=10000, ge=1)
    provider_concurrency: int = Field(default=20, ge=1, le=100)

    @model_validator(mode="after")
    def validate_deployment(self) -> Self:
        if self.enable_privacy_tools and (
            not self.privacy_policy_version.strip()
            or not _secure_url(self.privacy_support_url)
        ):
            raise ValueError(
                "Privacy tools require a policy version and HTTPS support URL"
            )
        if (
            self.environment in {"staging", "production"}
            and len(self.metrics_token) < 32
        ):
            raise ValueError("A 32-character metrics_token is required")
        if self.enable_embedded_scheduler:
            raise ValueError(
                "Embedded scheduling has been removed; run app.jobs scheduler"
            )
        if self.process_role == "worker":
            if not self.worker_database_url:
                raise ValueError("Workers require worker_database_url")
            if self.enable_dev_routes:
                raise ValueError("Workers cannot enable development routes")
            return self
        if not all(
            (self.supabase_url, self.supabase_service_role_key, self.addis_api_key)
        ):
            raise ValueError(
                "API requires Supabase URL, Storage key, and Addis API key"
            )
        if self.legacy_hs256_until:
            deadline = datetime.fromisoformat(
                self.legacy_hs256_until.replace("Z", "+00:00")
            )
            if deadline.tzinfo is None or deadline > datetime.now(
                timezone.utc
            ) + timedelta(days=30):
                raise ValueError(
                    "Legacy HS256 deadline must be timezone-aware and within 30 days"
                )
        if self.environment in {"staging", "production"}:
            if not self.database_url or not self.supabase_publishable_key:
                raise ValueError(
                    "database_url and supabase_publishable_key are required"
                )
            if not self.enable_request_limits or len(self.rate_limit_secret) < 32:
                raise ValueError(
                    "Distributed request limits and a 32-character rate_limit_secret are required"
                )
            if not self.trusted_hosts.strip() or "*" in self.trusted_hosts:
                raise ValueError("Explicit trusted_hosts are required")
            if self.enable_dev_routes or self.enable_embedded_scheduler:
                raise ValueError(
                    "Development routes and embedded scheduling are forbidden in staging/production"
                )
            for name in ("supabase_url", "addis_api_base_url", "public_base_url"):
                if not _secure_url(getattr(self, name)):
                    raise ValueError(
                        f"{name} must use HTTPS with a non-loopback host and no credentials/query/fragment"
                    )
            if not self.cors_origin_list or not all(
                _secure_url(origin, origin_only=True)
                for origin in self.cors_origin_list
            ):
                raise ValueError(
                    "cors_origins must be an explicit list of HTTPS origins without paths or wildcards"
                )
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]

    @property
    def is_telegram_configured(self) -> bool:
        return bool(self.telegram_bot_token.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()
