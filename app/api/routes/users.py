from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.reminders import ReminderRepository
from app.db.repositories.supplements import SupplementRepository
from app.models.user import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
    SupplementCreate,
    SupplementResponse,
    SupplementUpdate,
    UserProfile,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserProfile)
def get_me(current_user: dict = Depends(get_current_user)) -> UserProfile:
    user_id = UUID(current_user["id"])
    supplements = SupplementRepository().list_all(user_id)
    appointment = AppointmentRepository().get_by_user(user_id)
    reminders = ReminderRepository().list_pending(user_id)

    return UserProfile(
        id=user_id,
        email=current_user.get("email"),
        created_at=current_user["created_at"],
        supplements=supplements,
        appointment=appointment,
        pending_reminders=reminders,
    )


@router.post("/me/supplements", response_model=SupplementResponse)
def create_supplement(
    payload: SupplementCreate,
    current_user: dict = Depends(get_current_user),
) -> SupplementResponse:
    data = payload.model_dump()
    if data.get("reminder_time") is not None:
        data["reminder_time"] = data["reminder_time"].isoformat()
    supplement = SupplementRepository().create(UUID(current_user["id"]), data)
    return SupplementResponse(**supplement)


@router.put("/me/supplements/{supplement_id}", response_model=SupplementResponse)
def update_supplement(
    supplement_id: UUID,
    payload: SupplementUpdate,
    current_user: dict = Depends(get_current_user),
) -> SupplementResponse:
    data = payload.model_dump(exclude_unset=True)
    if "reminder_time" in data and data["reminder_time"] is not None:
        data["reminder_time"] = data["reminder_time"].isoformat()
    try:
        supplement = SupplementRepository().update(UUID(current_user["id"]), supplement_id, data)
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return SupplementResponse(**supplement)


@router.post("/me/appointment", response_model=AppointmentResponse)
def create_appointment(
    payload: AppointmentCreate,
    current_user: dict = Depends(get_current_user),
) -> AppointmentResponse:
    user_id = UUID(current_user["id"])
    repo = AppointmentRepository()
    if repo.get_by_user(user_id):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Appointment already exists")
    appointment = repo.create(
        user_id,
        {
            "appointment_date": payload.appointment_date.isoformat(),
            "reminder_lead_days": payload.reminder_lead_days,
        },
    )
    return AppointmentResponse(**appointment)


@router.put("/me/appointment", response_model=AppointmentResponse)
def update_appointment(
    payload: AppointmentUpdate,
    current_user: dict = Depends(get_current_user),
) -> AppointmentResponse:
    user_id = UUID(current_user["id"])
    data = payload.model_dump(exclude_unset=True)
    if "appointment_date" in data and data["appointment_date"] is not None:
        data["appointment_date"] = data["appointment_date"].isoformat()
    try:
        appointment = AppointmentRepository().update(user_id, data)
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return AppointmentResponse(**appointment)
