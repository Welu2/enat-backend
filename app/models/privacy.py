from datetime import datetime
from typing import Literal, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, JsonValue, StrictBool, model_validator

ExportSection = Literal[
    "profile",
    "supplements",
    "appointments",
    "appointment_events",
    "check_ins",
    "drafts",
    "summaries",
    "reminders",
    "shares",
    "requests",
    "audit",
    "care_connections",
    "emergency_alerts",
    "care_audit",
]


class DeletionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confirm: StrictBool

    @model_validator(mode="after")
    def consent(self) -> Self:
        if not self.confirm:
            raise ValueError("Explicit confirmation is required")
        return self


class PrivacyRequestResponse(BaseModel):
    id: UUID
    kind: Literal["deletion"]
    status: Literal["requested", "cancelled"]
    created_at: datetime
    cancelled_at: datetime | None


class ExportManifest(BaseModel):
    format_version: Literal["personal-data-v1"] = "personal-data-v1"
    sections: list[ExportSection]
    page_limit: int = 100
    consistency: Literal["per-page"] = "per-page"
    policy_version: str
    support_url: str
    excluded: list[str]


class ExportPage(BaseModel):
    format_version: Literal["personal-data-v1"] = "personal-data-v1"
    section: ExportSection
    generated_at: datetime
    records: list[dict[str, JsonValue]]
    next_cursor: UUID | None
