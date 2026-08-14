from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


CheckInStage = Literal["symptoms", "food", "supplement", "closing"]


class SymptomItem(BaseModel):
    item_id: str
    raw_text: str
    category: str
    duration: str | None = None
    severity: str | None = None
    danger_sign: bool = False
    confirmed: bool = False


class FoodLogItem(BaseModel):
    item_id: str
    raw_text: str
    confirmed: bool = False


class SupplementCheckItem(BaseModel):
    item_id: str
    supplement_name: str
    taken_today: bool
    raw_text: str
    confirmed: bool = False


class ClosingMentionItem(BaseModel):
    item_id: str
    raw_text: str
    topic: str
    confirmed: bool = False


class CheckInStartResponse(BaseModel):
    session_id: UUID
    stage: CheckInStage
    question_prompt: str


class CheckInRespondResponse(BaseModel):
    session_id: UUID
    stage: CheckInStage
    transcript: str
    pending_items: list[dict[str, Any]]


class VerifyItemRequest(BaseModel):
    item_id: str
    confirmed: bool
    corrected_value: dict[str, Any] | None = None


class VerifyItemResponse(BaseModel):
    session_id: UUID
    stage: CheckInStage
    pending_items: list[dict[str, Any]]
    confirmed_count: int


class CompleteStageResponse(BaseModel):
    session_id: UUID
    stage_completed: CheckInStage
    danger_sign_triggered: bool
    next_stage: CheckInStage | None = None
    question_prompt: str | None = None
    session_completed: bool = False
    check_in_id: UUID | None = None


class CheckInHistoryItem(BaseModel):
    id: UUID
    timestamp: datetime
    symptoms: list[dict[str, Any]] | None = None
    food_log: dict[str, Any] | None = None
    supplement_check: dict[str, Any] | None = None
    closing_mentions: list[dict[str, Any]] | None = None
    danger_sign_triggered: bool
