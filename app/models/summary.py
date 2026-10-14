from datetime import date, datetime
from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, JsonValue, model_validator


class SummaryGenerateResponse(BaseModel):
    window_start: datetime | None = None
    window_end: datetime | None = None
    id: UUID
    period_start: date
    period_end: date
    generated_at: datetime
    share_link_slug: str | None = None
    qr_code_url: str | None = None
    anc_contact_number: int | None = None
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None
    content_json: dict[str, JsonValue]


class SummaryLatestResponse(BaseModel):
    window_start: datetime | None = None
    window_end: datetime | None = None
    id: UUID
    period_start: date
    period_end: date
    generated_at: datetime
    share_link_slug: str | None = None
    qr_code_url: str | None = None
    anc_contact_number: int | None = None
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None
    content_json: dict[str, JsonValue]


class PublicSummaryResponse(BaseModel):
    period_start: date
    period_end: date
    generated_at: datetime
    anc_contact_number: int | None = None
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None
    content_json: dict[str, JsonValue]


class SummaryGenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    period_start: AwareDatetime | None = None
    period_end: AwareDatetime | None = None

    @model_validator(mode="after")
    def paired_window(self) -> Self:
        if (self.period_start is None) != (self.period_end is None):
            raise ValueError("Provide both window bounds")
        return self
