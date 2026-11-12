from datetime import datetime, timezone
from typing import Literal, Self
from uuid import UUID

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    field_validator,
    model_validator,
)

from app.models.clinical import (
    ClosingFields,
    FoodFields,
    SupplementFields,
    SymptomFields,
)


class OfflineCheckInRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal[1]
    client_submission_id: UUID
    recorded_at: AwareDatetime
    client_confirmed_at: AwareDatetime
    confirmed: StrictBool
    symptoms: list[SymptomFields] = Field(max_length=50)
    food_log: list[FoodFields] = Field(max_length=50)
    supplement_check: list[SupplementFields] = Field(max_length=50)
    closing_mentions: list[ClosingFields] = Field(max_length=50)

    @field_validator("schema_version", mode="before")
    @classmethod
    def integer_version(cls, value: object) -> object:
        if type(value) is not int:
            raise ValueError("Integer schema version required")
        return value

    @field_validator("recorded_at", "client_confirmed_at")
    @classmethod
    def utc_time(cls, value: datetime) -> datetime:
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def confirmed_observations(self) -> Self:
        count = (
            len(self.symptoms)
            + len(self.food_log)
            + len(self.supplement_check)
            + len(self.closing_mentions)
        )
        if self.confirmed is not True or not 1 <= count <= 100:
            raise ValueError("Explicitly confirm between 1 and 100 observations")
        if self.recorded_at > self.client_confirmed_at:
            raise ValueError("Confirmation precedes observation")
        return self


class OfflineCheckInResponse(BaseModel):
    client_submission_id: UUID
    check_in_id: UUID
    status: Literal["synced"]
    recorded_at: datetime
    received_at: datetime
    danger_sign_triggered: bool
    alert_id: UUID | None
