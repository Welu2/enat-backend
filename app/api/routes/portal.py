from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Response

from app.db.pagination import PAGE_RESPONSE
from app.dependencies import get_current_user_id
from app.models.alerts import AlertStatus, EmergencyAlert
from app.models.checkin import CheckInHistoryItem
from app.models.portal import (
    PatientCard,
    PortalAppointment,
    PortalIdentity,
    PortalPatient,
    PortalSummary,
)
from app.services import portal

router = APIRouter(
    prefix="/portal", tags=["portal"], dependencies=[Depends(get_current_user_id)]
)
PageLimit = Annotated[int, Query(ge=1, le=100)]
Cursor = Annotated[str | None, Query(max_length=256)]


@router.get("/me", response_model=PortalIdentity)
def identity():
    return portal.identity()


@router.get("/patients", response_model=list[PatientCard], responses=PAGE_RESPONSE)
def patients(response: Response, limit: PageLimit = 50, cursor: Cursor = None):
    rows, next_cursor = portal.patients(limit, cursor)
    if next_cursor:
        response.headers["X-Next-Cursor"] = next_cursor
    return rows


@router.get("/patients/{patient_id}", response_model=PortalPatient)
def patient(patient_id: UUID):
    return portal.read(patient_id, "patient")


@router.get(
    "/patients/{patient_id}/appointment", response_model=PortalAppointment | None
)
def appointment(patient_id: UUID):
    return portal.read(patient_id, "appointment")


@router.get("/patients/{patient_id}/summary/latest", response_model=PortalSummary)
def summary(patient_id: UUID):
    return portal.read(patient_id, "summary")


@router.get(
    "/patients/{patient_id}/check-ins",
    response_model=list[CheckInHistoryItem],
    responses=PAGE_RESPONSE,
)
def history(
    patient_id: UUID, response: Response, limit: PageLimit = 50, cursor: Cursor = None
):
    rows, next_cursor = portal.history(patient_id, "check_ins", limit, cursor)
    if next_cursor:
        response.headers["X-Next-Cursor"] = next_cursor
    return rows


@router.get(
    "/patients/{patient_id}/alerts",
    response_model=list[EmergencyAlert],
    responses=PAGE_RESPONSE,
)
def alerts(
    patient_id: UUID,
    response: Response,
    limit: PageLimit = 50,
    cursor: Cursor = None,
    status: AlertStatus | None = None,
):
    rows, next_cursor = portal.history(patient_id, "alerts", limit, cursor, status)
    if next_cursor:
        response.headers["X-Next-Cursor"] = next_cursor
    return rows


@router.post(
    "/patients/{patient_id}/alerts/{alert_id}/acknowledge",
    response_model=EmergencyAlert,
)
def acknowledge(
    patient_id: UUID,
    alert_id: UUID,
    key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=128)],
):
    return portal.acknowledge(patient_id, alert_id, key)
