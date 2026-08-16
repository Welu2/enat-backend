from datetime import date, datetime, time
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class AuthCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID
    email: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    access_token: str
    new_password: str = Field(min_length=6)


class PushTokenRegister(BaseModel):
    token: str
    platform: Literal["web", "android", "ios"] = "web"


class UserProfile(BaseModel):
    id: UUID
    email: str | None
    created_at: datetime
    supplements: list["SupplementResponse"] = []
    appointment: "AppointmentResponse | None" = None
    pending_reminders: list[dict[str, Any]] = []


class SupplementCreate(BaseModel):
    name: str
    active: bool = True
    reminder_enabled: bool = True
    reminder_time: time | None = None


class SupplementUpdate(BaseModel):
    name: str | None = None
    active: bool | None = None
    reminder_enabled: bool | None = None
    reminder_time: time | None = None


class SupplementResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    active: bool
    reminder_enabled: bool
    reminder_time: time | None
    created_at: datetime


class AppointmentCreate(BaseModel):
    appointment_date: date
    reminder_lead_days: int = 2


class AppointmentUpdate(BaseModel):
    appointment_date: date | None = None
    reminder_lead_days: int | None = None


class AppointmentResponse(BaseModel):
    id: UUID
    user_id: UUID
    appointment_date: date
    last_summary_generated_at: datetime | None
    reminder_lead_days: int


class SupplementSettingsItem(BaseModel):
    id: UUID | None = None
    name: str | None = None
    active: bool | None = None
    reminder_enabled: bool | None = None
    reminder_time: time | None = None


class UserSettingsUpdate(BaseModel):
    appointment: AppointmentUpdate | None = None
    supplements: list[SupplementSettingsItem] | None = None


class SupplementVerifyRequest(BaseModel):
    supplement_id: UUID | None = None
    supplement_name: str | None = None
    taken_today: bool = True
    raw_text: str | None = None


class SupplementVerifyResponse(BaseModel):
    status: str = "verified"
    supplement_name: str
    taken_today: bool
    logged_at: datetime
