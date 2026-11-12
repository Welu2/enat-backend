from datetime import datetime
from typing import Literal, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StrictBool, model_validator

Relationship = Literal["clinician", "trusted_person"]


class CareInviteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    recipient_id: UUID
    relationship: Relationship
    consent: StrictBool

    @model_validator(mode="after")
    def explicit_consent(self) -> Self:
        if self.consent is not True:
            raise ValueError("Patient consent required")
        return self


class CareAcceptRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(min_length=43, max_length=43, pattern=r"^[A-Za-z0-9_-]+$")


class CareConnection(BaseModel):
    id: UUID
    recipient_id: UUID
    recipient_display_name: str
    relationship: Relationship
    status: Literal["pending", "active", "revoked", "expired"]
    consent_version: str
    consented_at: datetime
    created_at: datetime
    accepted_at: datetime | None
    revoked_at: datetime | None
    expires_at: datetime


class CareInviteResponse(CareConnection):
    token: str


class CareAccepted(BaseModel):
    id: UUID
    relationship: Relationship
    status: Literal["active"]
