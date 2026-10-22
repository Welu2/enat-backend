from datetime import datetime
from typing import Literal, Self
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    StrictBool,
    model_validator,
)

from app.models.clinical import (
    ClosingCorrection,
    FoodCorrection,
    SupplementCorrection,
    SymptomCorrection,
)

CheckInStage = Literal["symptoms", "food", "supplement", "closing"]


class CheckInStartResponse(BaseModel):
    version: int
    stage_status: str
    session_id: UUID
    stage: CheckInStage
    question_prompt: str
    question_audio_url: str | None = None


class CheckInRespondResponse(BaseModel):
    version: int
    stage_status: str
    session_id: UUID
    stage: CheckInStage
    transcript: str
    pending_items: list[dict[str, JsonValue]]


class ItemVerificationPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["verify", "add", "discard"] = "verify"
    item_id: str | None = Field(default=None, max_length=64)
    confirmed: StrictBool = True
    corrected_value: (
        SymptomCorrection
        | FoodCorrection
        | SupplementCorrection
        | ClosingCorrection
        | None
    ) = None

    @model_validator(mode="after")
    def operation_fields(self) -> Self:
        if self.action == "add":
            if self.item_id is not None or self.corrected_value is None:
                raise ValueError("Manual addition requires fields and no ID")
        elif not self.item_id:
            raise ValueError("Item ID required")
        if self.action == "discard" and self.corrected_value is not None:
            raise ValueError("Discard cannot include corrections")
        return self


class VerifyItemRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[ItemVerificationPayload] = Field(min_length=1, max_length=50)


class CompleteStageRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skip: StrictBool = False


class VerifyItemResponse(BaseModel):
    version: int
    stage_status: str
    session_id: UUID
    stage: CheckInStage
    pending_items: list[dict[str, JsonValue]]
    confirmed_count: int
    danger_sign_triggered: bool


class VoiceCorrectItemResponse(BaseModel):
    version: int
    stage_status: str
    session_id: UUID
    stage: CheckInStage
    correction_transcript: str
    item_updated: bool
    pending_items: list[dict[str, JsonValue]]


class CompleteStageResponse(BaseModel):
    version: int
    stage_status: str
    session_id: UUID
    stage_completed: CheckInStage
    danger_sign_triggered: bool
    summary_text_am: str | None = None
    summary_text_en: str | None = None
    next_stage: CheckInStage | None = None
    question_prompt: str | None = None
    question_audio_url: str | None = None
    session_completed: bool = False
    check_in_id: UUID | None = None


class CheckInHistoryItem(BaseModel):
    id: UUID
    timestamp: datetime
    recorded_at: datetime | None = None
    received_at: datetime | None = None
    client_confirmed_at: datetime | None = None
    capture_source: Literal["online", "offline_form"] = "online"
    symptoms: list[dict[str, JsonValue]] | None = None
    food_log: list[dict[str, JsonValue]] = Field(default_factory=list)
    supplement_check: list[dict[str, JsonValue]] = Field(default_factory=list)
    closing_mentions: list[dict[str, JsonValue]] | None = None
    danger_sign_triggered: bool
    summary_text_am: str | None = None
    summary_text_en: str | None = None


class CheckInStateResponse(BaseModel):
    id: UUID
    version: int
    status: str
    current_stage: CheckInStage
    stage_order: list[CheckInStage]
    stage_status: str
    pending_items: list[dict[str, JsonValue]]
    draft_data: dict[str, JsonValue]
    completed_stages: dict[str, str]
    terminal_result: dict[str, JsonValue] | None
    expires_at: datetime
