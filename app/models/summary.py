from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class SummaryGenerateResponse(BaseModel):
    id: UUID
    period_start: date
    period_end: date
    generated_at: datetime
    share_link_slug: str
    qr_code_url: str | None
    anc_contact_number: int | None = None
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None
    content_json: dict[str, Any]


class SummaryLatestResponse(BaseModel):
    id: UUID
    period_start: date
    period_end: date
    generated_at: datetime
    share_link_slug: str
    qr_code_url: str | None
    anc_contact_number: int | None = None
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None
    content_json: dict[str, Any]


class PublicSummaryResponse(BaseModel):
    period_start: date
    period_end: date
    generated_at: datetime
    anc_contact_number: int | None = None
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None
    content_json: dict[str, Any]
