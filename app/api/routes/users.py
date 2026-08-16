from datetime import date, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.dependencies import get_current_user
from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.check_ins import CheckInRepository
from app.db.repositories.push_tokens import PushTokenRepository
from app.db.repositories.reminders import ReminderRepository
from app.db.repositories.supplements import SupplementRepository
from app.models.user import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
    PushTokenRegister,
    SupplementCreate,
    SupplementResponse,
    SupplementUpdate,
    SupplementVerifyRequest,
    SupplementVerifyResponse,
    UserProfile,
    UserSettingsUpdate,
)
from app.services.calendar import generate_google_calendar_url, generate_ical_content
from app.services.extraction import _supplement_display

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


@router.put("/me/settings", response_model=UserProfile)
@router.patch("/me/settings", response_model=UserProfile)
def update_user_settings(
    payload: UserSettingsUpdate,
    current_user: dict = Depends(get_current_user),
) -> UserProfile:
    """Unified settings endpoint to update appointments, supplements, and reminder times."""
    user_id = UUID(current_user["id"])
    app_repo = AppointmentRepository()
    supp_repo = SupplementRepository()

    if payload.appointment is not None:
        data = payload.appointment.model_dump(exclude_unset=True)
        if "appointment_date" in data and data["appointment_date"] is not None:
            data["appointment_date"] = data["appointment_date"].isoformat()
        if data:
            app_repo.upsert(user_id, data)

    if payload.supplements is not None:
        for s_item in payload.supplements:
            s_data = s_item.model_dump(exclude_unset=True)
            s_id = s_data.pop("id", None)
            if "reminder_time" in s_data and s_data["reminder_time"] is not None:
                s_data["reminder_time"] = s_data["reminder_time"].isoformat()
            if s_id:
                try:
                    supp_repo.update(user_id, s_id, s_data)
                except ValueError:
                    pass
            elif s_data and "name" in s_data:
                supp_repo.create(user_id, s_data)

    return get_me(current_user)


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


@router.delete("/me/supplements/{supplement_id}")
def delete_supplement(
    supplement_id: UUID,
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    deleted = SupplementRepository().delete(UUID(current_user["id"]), supplement_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Supplement not found")
    return {"status": "deleted"}


@router.post("/me/supplements/verify", response_model=SupplementVerifyResponse)
@router.post("/me/supplements/{supplement_id}/verify", response_model=SupplementVerifyResponse)
def verify_supplement_manually(
    payload: SupplementVerifyRequest = SupplementVerifyRequest(),
    supplement_id: UUID | None = None,
    current_user: dict = Depends(get_current_user),
) -> SupplementVerifyResponse:
    """Manually verify/log supplement intake today outside of voice checkin intake."""
    user_id = UUID(current_user["id"])
    target_id = supplement_id or payload.supplement_id

    all_supps = SupplementRepository().list_all(user_id)
    supp_name = payload.supplement_name or "iron"
    if target_id:
        match = next((s for s in all_supps if str(s["id"]) == str(target_id)), None)
        if match:
            supp_name = match.get("name", supp_name)
    elif all_supps:
        supp_name = all_supps[0].get("name", supp_name)

    disp_name = _supplement_display(supp_name)
    raw_text = payload.raw_text or (
        f"የ{disp_name} ወስጃለሁ" if payload.taken_today else f"የ{disp_name} አልወሰድኩም"
    )

    checkin_data = {
        "symptoms": [],
        "food_log": None,
        "supplement_check": {
            "supplement_name": supp_name,
            "taken_today": payload.taken_today,
            "raw_text": raw_text,
            "confirmed": True,
        },
        "closing_mentions": [],
        "danger_sign_triggered": False,
    }

    CheckInRepository().create(user_id, checkin_data)

    reminders = ReminderRepository().list_pending(user_id)
    for r in reminders:
        if r.get("type") == "supplement":
            ReminderRepository().dismiss(user_id, UUID(r["id"]))

    return SupplementVerifyResponse(
        status="verified",
        supplement_name=supp_name,
        taken_today=payload.taken_today,
        logged_at=datetime.utcnow(),
    )


@router.post("/me/appointment", response_model=AppointmentResponse)
@router.put("/me/appointment", response_model=AppointmentResponse)
def upsert_appointment(
    payload: AppointmentCreate,
    current_user: dict = Depends(get_current_user),
) -> AppointmentResponse:
    user_id = UUID(current_user["id"])
    data = payload.model_dump()
    data["appointment_date"] = payload.appointment_date.isoformat()
    appointment = AppointmentRepository().upsert(user_id, data)
    return AppointmentResponse(**appointment)


@router.delete("/me/appointment")
def delete_appointment(
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    deleted = AppointmentRepository().delete(UUID(current_user["id"]))
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return {"status": "deleted"}


@router.post("/me/push-tokens")
def register_push_token(
    payload: PushTokenRegister,
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    """Registers device FCM or Web Push token for offline notifications."""
    PushTokenRepository().register(UUID(current_user["id"]), payload.token, payload.platform)
    return {"status": "registered", "token": payload.token}


@router.get("/me/appointment/calendar-link")
def get_appointment_calendar_link(
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    """Returns 1-tap Google Calendar URL and iCal download URL for ANC appointment."""
    user_id = UUID(current_user["id"])
    appointment = AppointmentRepository().get_by_user(user_id)
    if not appointment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No appointment found")

    app_date = date.fromisoformat(appointment["appointment_date"])
    gcal_url = generate_google_calendar_url(app_date)

    return {
        "google_calendar_url": gcal_url,
        "ical_download_url": "/users/me/appointment/calendar.ics",
    }


@router.get("/me/appointment/calendar.ics")
def download_appointment_ical(
    current_user: dict = Depends(get_current_user),
) -> Response:
    """Returns standard .ics calendar file for Apple Calendar, Outlook, or Google Calendar."""
    user_id = UUID(current_user["id"])
    appointment = AppointmentRepository().get_by_user(user_id)
    if not appointment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No appointment found")

    app_date = date.fromisoformat(appointment["appointment_date"])
    ical_text = generate_ical_content(app_date)

    return Response(
        content=ical_text,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename=anc_appointment_{app_date}.ics"},
    )
