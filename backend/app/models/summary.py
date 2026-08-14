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
    content_json: dict[str, Any]


class SummaryLatestResponse(BaseModel):
    id: UUID
    period_start: date
    period_end: date
    generated_at: datetime
    share_link_slug: str
    qr_code_url: str | None
    content_json: dict[str, Any]


class PublicSummaryResponse(BaseModel):
    period_start: date
    period_end: date
    generated_at: datetime
    content_json: dict[str, Any]
