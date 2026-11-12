from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, JsonValue

from app.models.care import Relationship


class PortalIdentity(BaseModel):
    id: UUID
    display_name: str
    is_clinician: bool


class PortalAppointment(BaseModel):
    appointment_date: date
    hospital: str | None
    anc_contact_title: str | None
    anc_contact_title_am: str | None
    status: Literal["scheduled"]
    version: int


class PatientCard(BaseModel):
    id: UUID
    display_name: str
    relationship: Relationship
    appointment: PortalAppointment | None
    unacknowledged_alert_count: int


class PortalPatient(BaseModel):
    id: UUID
    display_name: str
    hospital: str | None
    estimated_due_date: date | None
    gestational_age_weeks: int | None
    gestational_age_days: int | None
    pregnancy_as_of: datetime | None
    overview_retrieved_at: datetime
    latest_check_in_received_at: datetime | None


class PortalSummary(BaseModel):
    id: UUID
    period_start: date
    period_end: date
    generated_at: datetime
    content_json: dict[str, JsonValue]
