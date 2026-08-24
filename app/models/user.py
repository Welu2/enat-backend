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
    supplements: list[Any] = []  # list of names or dicts e.g. ["iron & folic acid", "calcium"]
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
    appointment_date: date
    reminder_lead_days: int = 2
    anc_contact_number: int | None = None
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None


class AppointmentUpdate(BaseModel):
    appointment_date: date | None = None
    reminder_lead_days: int | None = None
    anc_contact_number: int | None = None
    anc_contact_title: str | None = None
    anc_contact_title_am: str | None = None
    target_gestational_weeks: int | None = None


class AppointmentResponse(BaseModel):
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
    next_anc_contact: dict[str, Any]
    all_contacts: list[dict[str, Any]]


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
    pending_reminders: list[dict[str, Any]] = []


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


class FoodVerifyRequest(BaseModel):
    food_groups: list[str] = []
    raw_text: str | None = None
    items: list[str] = []


class FoodVerifyResponse(BaseModel):
    status: str = "verified"
    food_groups: list[str]
    raw_text: str
    logged_at: datetime
