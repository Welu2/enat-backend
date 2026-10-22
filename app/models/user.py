from datetime import date, datetime, time
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    JsonValue,
    StrictBool,
    model_validator,
)

from app.models.clinical import FoodGroup, Text


class AuthCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class SignupCredentials(AuthCredentials):
    password: str = Field(min_length=8, max_length=128)


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str = "bearer"
    user_id: UUID
    email: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token_hash: str = Field(min_length=16, max_length=512)
    new_password: str = Field(min_length=8, max_length=128)


class PushTokenRegister(BaseModel):
    token: str = Field(min_length=1, max_length=4096)
    platform: Literal["web", "android", "ios"] = "web"


class TrimesterInfo(BaseModel):
    number: int
    key: str
    name_en: str
    name_am: str
    week_range: str


class GestationalAgeCalculateRequest(BaseModel):
    pregnancy_counting_method: str = "lnmp"  # 'lnmp', 'ultrasound', 'manual'
    lnmp_date: date | None = None
    ultrasound_date: date | None = None
    ultrasound_weeks: int | None = None
    ultrasound_days: int | None = None
    manual_gestational_weeks: int | None = None
    manual_gestational_days: int | None = None
    as_of_date: date | None = None


class GestationalAgeCalculateResponse(BaseModel):
    gestational_age_weeks: int | None = None
    gestational_age_days: int | None = None
    gestational_age_total_days: int | None = None
    formatted_age_am: str | None = None
    formatted_age_en: str | None = None
    trimester: str | None = None
    trimester_info: TrimesterInfo | None = None
    estimated_due_date: date | None = None
    effective_lnmp_date: date | None = None
    is_gestational_age_manual: bool = False
    days_until_edd: int | None = None


class OnboardingSupplement(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=200)


class OnboardingSubmitRequest(BaseModel):
    age: int | None = None
    area: Literal["urban", "rural"] | str | None = None
    pregnancy_counting_method: str = "lnmp"  # 'lnmp', 'ultrasound', 'manual'
    lnmp_date: date | None = None
    ultrasound_date: date | None = None
    ultrasound_weeks: int | None = None
    ultrasound_days: int | None = None
    manual_gestational_weeks: int | None = None
    manual_gestational_days: int | None = None
    gestational_age_weeks: int | None = None
    gestational_age_days: int | None = None
    total_pregnancies: int | None = None
    live_births: int | None = None
    had_c_section: bool | None = None
    child_passed_away: bool | None = None
    past_pregnancy_complications: list[str] = []
    known_medical_conditions: list[str] = []
    custom_medical_condition: str | None = None
    malaria_endemic_area: bool | None = None
    current_medications: str | None = None
    supplements: list[
        Annotated[str, Field(min_length=1, max_length=200)] | OnboardingSupplement
    ] = Field(default_factory=list, max_length=50)
    hospital: str | None = None


class MaternalProfileUpdate(BaseModel):
    age: int | None = None
    area: str | None = None
    pregnancy_counting_method: str | None = None
    lnmp_date: date | None = None
    ultrasound_date: date | None = None
    ultrasound_weeks: int | None = None
    gestational_age_weeks: int | None = None
    gestational_age_days: int | None = None
    is_gestational_age_manual: bool | None = None
    estimated_due_date: date | None = None
    total_pregnancies: int | None = None
    live_births: int | None = None
    had_c_section: bool | None = None
    child_passed_away: bool | None = None
    past_pregnancy_complications: list[str] | None = None
    known_medical_conditions: list[str] | None = None
    custom_medical_condition: str | None = None
    malaria_endemic_area: bool | None = None
    current_medications: str | None = None
    hospital: str | None = None


class HospitalUpdateRequest(BaseModel):
    hospital: str


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
    model_config = ConfigDict(extra="forbid")
    version: int | None = Field(default=None, ge=0)
    appointment_date: date
    reminder_lead_days: int = 2
    anc_contact_number: int | None = Field(default=None, ge=1, le=8)
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None


class AppointmentUpdate(BaseModel):
    version: int | None = Field(default=None, ge=0)
    appointment_date: date | None = None
    reminder_lead_days: int | None = None
    anc_contact_number: int | None = Field(default=None, ge=1, le=8)
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None


class AppointmentResponse(BaseModel):
    version: int = 0
    status: Literal["scheduled", "completed", "missed"] = "scheduled"
    id: UUID
    user_id: UUID
    appointment_date: date
    last_summary_generated_at: datetime | None = None
    reminder_lead_days: int = 2
    anc_contact_number: int = 1
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None
    previous_appointment_date: date | None = None


class ANCScheduleResponse(BaseModel):
    current_gestational_age_weeks: int
    current_gestational_age_days: int
    effective_lnmp_date: date | None = None
    estimated_due_date: date | None = None
    next_anc_contact: dict[str, JsonValue]
    all_contacts: list[dict[str, JsonValue]]


class SupplementSettingsItem(BaseModel):
    id: UUID | None = None
    name: str | None = None
    active: bool | None = None
    reminder_enabled: bool | None = None
    reminder_time: time | None = None


class UserSettingsUpdate(BaseModel):
    hospital: str | None = None
    appointment: AppointmentUpdate | None = None
    supplements: list[SupplementSettingsItem] | None = None
    maternal_profile: MaternalProfileUpdate | None = None


class UserProfile(BaseModel):
    id: UUID
    email: str | None
    created_at: datetime

    # Maternal Onboarding & Pregnancy Profile
    age: int | None = None
    area: str | None = None
    pregnancy_counting_method: str | None = None
    lnmp_date: date | None = None
    ultrasound_date: date | None = None
    ultrasound_weeks: int | None = None
    gestational_age_weeks: int | None = None
    gestational_age_days: int | None = None
    is_gestational_age_manual: bool = False
    effective_lnmp_date: date | None = None
    estimated_due_date: date | None = None
    trimester: str | None = None
    total_pregnancies: int | None = None
    live_births: int | None = None
    had_c_section: bool | None = None
    child_passed_away: bool | None = None
    past_pregnancy_complications: list[str] = []
    known_medical_conditions: list[str] = []
    custom_medical_condition: str | None = None
    malaria_endemic_area: bool | None = None
    current_medications: str | None = None
    hospital: str | None = None
    onboarding_completed: bool = False

    # Dynamic real-time calculation of current pregnancy status
    current_pregnancy_status: GestationalAgeCalculateResponse | None = None

    # Supplements, Appointments, Reminders
    supplements: list[SupplementResponse] = []
    appointment: AppointmentResponse | None = None
    pending_reminders: list[dict[str, JsonValue]] = []


class SupplementVerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    supplement_id: UUID | None = None
    supplement_name: str | None = Field(default=None, min_length=1, max_length=200)
    taken_today: StrictBool
    raw_text: Text | None = None


class SupplementVerifyResponse(BaseModel):
    status: str = "verified"
    supplement_name: str
    taken_today: bool
    logged_at: datetime


class FoodVerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    food_groups: list[FoodGroup] = Field(default_factory=list, max_length=4)
    raw_text: Text | None = None
    items: list[Text] = Field(default_factory=list, max_length=50)


class FoodVerifyResponse(BaseModel):
    status: str = "verified"
    food_groups: list[str]
    raw_text: str
    logged_at: datetime


class AppointmentTransition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["completed", "missed", "rescheduled"]
    version: int = Field(ge=0)
    appointment_date: date | None = None
    anc_contact_number: int | None = Field(default=None, ge=1, le=8)

    @model_validator(mode="after")
    def transition_fields(self) -> Self:
        if self.action == "rescheduled":
            if self.appointment_date is None:
                raise ValueError("New date required")
        elif self.appointment_date is not None or self.anc_contact_number is not None:
            raise ValueError("Only rescheduling accepts a new date/contact")
        return self
