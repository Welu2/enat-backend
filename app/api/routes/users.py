from datetime import date, datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.dependencies import get_current_user
from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.check_ins import CheckInRepository
from app.db.repositories.push_tokens import PushTokenRepository
from app.db.repositories.reminders import ReminderRepository
from app.db.repositories.supplements import SupplementRepository
from app.db.repositories.users import UserRepository
from app.models.user import (
    ANCScheduleResponse,
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
    FoodVerifyRequest,
    FoodVerifyResponse,
    GestationalAgeCalculateRequest,
    GestationalAgeCalculateResponse,
    HospitalUpdateRequest,
    MaternalProfileUpdate,
    OnboardingSubmitRequest,
    PushTokenRegister,
    SupplementCreate,
    SupplementResponse,
    SupplementUpdate,
    SupplementVerifyRequest,
    SupplementVerifyResponse,
    UserProfile,
    UserSettingsUpdate,
)
from app.services.anc_schedule import calculate_all_anc_dates, get_next_anc_contact
from app.services.calendar import generate_google_calendar_url, generate_ical_content
from app.services.extraction import _supplement_display
from app.services.gestational_age import (
    calculate_gestational_age_and_edd,
    get_current_pregnancy_status,
)
from app.services.nutrition import classify_ethiopian_food

router = APIRouter(prefix="/users", tags=["users"])


def _build_user_profile(user: dict[str, Any]) -> UserProfile:
    """Helper to assemble a complete UserProfile with real-time calculated gestational metrics."""
    user_id = UUID(user["id"])
    supplements = SupplementRepository().list_all(user_id)
    appointment = AppointmentRepository().get_by_user(user_id)
    reminders = ReminderRepository().list_pending(user_id)

    live_pregnancy = get_current_pregnancy_status(user)
    live_pregnancy_model = (
        GestationalAgeCalculateResponse(**live_pregnancy) if live_pregnancy else None
    )

    return UserProfile(
        id=user_id,
        email=user.get("email"),
        created_at=user["created_at"],
        age=user.get("age"),
        area=user.get("area"),
        pregnancy_counting_method=user.get("pregnancy_counting_method"),
        lnmp_date=user.get("lnmp_date"),
        ultrasound_date=user.get("ultrasound_date"),
        ultrasound_weeks=user.get("ultrasound_weeks"),
        gestational_age_weeks=user.get("gestational_age_weeks"),
        gestational_age_days=user.get("gestational_age_days"),
        is_gestational_age_manual=bool(user.get("is_gestational_age_manual")),
        effective_lnmp_date=user.get("effective_lnmp_date"),
        estimated_due_date=user.get("estimated_due_date"),
        trimester=user.get("trimester"),
        total_pregnancies=user.get("total_pregnancies"),
        live_births=user.get("live_births"),
        had_c_section=user.get("had_c_section"),
        child_passed_away=user.get("child_passed_away"),
        past_pregnancy_complications=user.get("past_pregnancy_complications") or [],
        known_medical_conditions=user.get("known_medical_conditions") or [],
        custom_medical_condition=user.get("custom_medical_condition"),
        malaria_endemic_area=user.get("malaria_endemic_area"),
        current_medications=user.get("current_medications"),
        hospital=user.get("hospital"),
        onboarding_completed=bool(user.get("onboarding_completed")),
        current_pregnancy_status=live_pregnancy_model,
        supplements=supplements,
        appointment=appointment,
        pending_reminders=reminders,
    )


@router.post("/calculate-gestational-age", response_model=GestationalAgeCalculateResponse)
def calculate_gestational_age(
    payload: GestationalAgeCalculateRequest,
) -> GestationalAgeCalculateResponse:
    """Public calculation endpoint for instant frontend pregnancy age, EDD, and trimester preview."""
    manual_w = (
        payload.manual_gestational_weeks
        if payload.manual_gestational_weeks is not None
        else (
            payload.ultrasound_weeks
            if payload.pregnancy_counting_method == "manual"
            else None
        )
    )
    result = calculate_gestational_age_and_edd(
        pregnancy_counting_method=payload.pregnancy_counting_method,
        lnmp_date=payload.lnmp_date,
        ultrasound_date=payload.ultrasound_date,
        ultrasound_weeks=payload.ultrasound_weeks,
        ultrasound_days=payload.ultrasound_days,
        manual_gestational_weeks=manual_w,
        manual_gestational_days=payload.manual_gestational_days,
        as_of_date=payload.as_of_date,
    )
    return GestationalAgeCalculateResponse(**result)


@router.get("/me", response_model=UserProfile)
def get_me(current_user: dict = Depends(get_current_user)) -> UserProfile:
    """Fetch current user profile, onboarding data, live pregnancy metrics, supplements, and reminders."""
    user_id = UUID(current_user["id"])
    fresh_user = UserRepository().get_by_id(user_id) or current_user
    return _build_user_profile(fresh_user)


@router.post("/me/onboarding", response_model=UserProfile)
def submit_onboarding(
    payload: OnboardingSubmitRequest,
    current_user: dict = Depends(get_current_user),
) -> UserProfile:
    """Submit full initial onboarding intake questions, calculate and save pregnancy metrics & seed supplements."""
    user_id = UUID(current_user["id"])
    user_repo = UserRepository()
    supp_repo = SupplementRepository()
    app_repo = AppointmentRepository()

    # 1. Resolve manual vs calculated gestational age
    manual_w = payload.manual_gestational_weeks or payload.gestational_age_weeks
    manual_d = payload.manual_gestational_days or payload.gestational_age_days

    calc_res = calculate_gestational_age_and_edd(
        pregnancy_counting_method=payload.pregnancy_counting_method,
        lnmp_date=payload.lnmp_date,
        ultrasound_date=payload.ultrasound_date,
        ultrasound_weeks=payload.ultrasound_weeks,
        ultrasound_days=payload.ultrasound_days,
        manual_gestational_weeks=manual_w,
        manual_gestational_days=manual_d,
    )

    update_data: dict[str, Any] = {
        "age": payload.age,
        "area": payload.area,
        "pregnancy_counting_method": payload.pregnancy_counting_method,
        "lnmp_date": payload.lnmp_date.isoformat() if payload.lnmp_date else None,
        "ultrasound_date": payload.ultrasound_date.isoformat() if payload.ultrasound_date else None,
        "ultrasound_weeks": payload.ultrasound_weeks,
        "gestational_age_weeks": calc_res["gestational_age_weeks"],
        "gestational_age_days": calc_res["gestational_age_days"],
        "is_gestational_age_manual": calc_res["is_gestational_age_manual"],
        "effective_lnmp_date": (
            calc_res["effective_lnmp_date"].isoformat()
            if calc_res["effective_lnmp_date"]
            else None
        ),
        "estimated_due_date": (
            calc_res["estimated_due_date"].isoformat()
            if calc_res["estimated_due_date"]
            else None
        ),
        "trimester": calc_res["trimester"],
        "total_pregnancies": payload.total_pregnancies,
        "live_births": payload.live_births,
        "had_c_section": payload.had_c_section,
        "child_passed_away": payload.child_passed_away,
        "past_pregnancy_complications": payload.past_pregnancy_complications,
        "known_medical_conditions": payload.known_medical_conditions,
        "custom_medical_condition": payload.custom_medical_condition,
        "malaria_endemic_area": payload.malaria_endemic_area,
        "current_medications": payload.current_medications,
        "hospital": payload.hospital,
        "onboarding_completed": True,
    }

    # Clean out None values where appropriate
    cleaned_update = {k: v for k, v in update_data.items() if v is not None or k in ("custom_medical_condition", "current_medications", "hospital")}
    user_repo.update_profile(user_id, cleaned_update)

    # 2. Seed supplements into the supplements table if provided
    if payload.supplements:
        existing_supps = {s["name"].lower() for s in supp_repo.list_all(user_id)}
        for supp in payload.supplements:
            name: str = ""
            if isinstance(supp, str):
                name = supp.strip()
            elif isinstance(supp, dict) and supp.get("name"):
                name = str(supp["name"]).strip()

            if name and name.lower() not in existing_supps:
                supp_repo.create(
                    user_id,
                    {
                        "name": name,
                        "active": True,
                        "reminder_enabled": True,
                        "reminder_time": "09:00:00",
                    },
                )
                existing_supps.add(name.lower())

    # 3. Auto-schedule first upcoming WHO ANC contact if user has no appointment yet
    existing_apt = app_repo.get_by_user(user_id)
    if not existing_apt:
        eff_lnmp_str = update_data.get("effective_lnmp_date") or update_data.get("lnmp_date")
        if eff_lnmp_str:
            eff_lnmp_date = date.fromisoformat(eff_lnmp_str) if isinstance(eff_lnmp_str, str) else eff_lnmp_str
            next_anc = get_next_anc_contact(eff_lnmp_date)
            app_repo.create(
                user_id,
                {
                    "appointment_date": next_anc["target_date"],
                    "anc_contact_number": next_anc["contact_number"],
                    "anc_contact_title": next_anc["title_en"],
                    "anc_contact_title_am": next_anc["title_am"],
                    "target_gestational_weeks": next_anc["gestational_weeks"],
                    "reminder_lead_days": 2,
                },
            )

    fresh_user = user_repo.get_by_id(user_id) or current_user
    return _build_user_profile(fresh_user)


@router.put("/me/profile", response_model=UserProfile)
@router.patch("/me/profile", response_model=UserProfile)
def update_user_profile(
    payload: MaternalProfileUpdate,
    current_user: dict = Depends(get_current_user),
) -> UserProfile:
    """Update maternal profile information, medical history, or gestational age metrics."""
    user_id = UUID(current_user["id"])
    user_repo = UserRepository()
    data = payload.model_dump(exclude_unset=True)

    # If date or calculation fields are modified, recompute pregnancy status
    date_fields_changed = any(
        k in data for k in ("lnmp_date", "ultrasound_date", "ultrasound_weeks", "gestational_age_weeks", "pregnancy_counting_method")
    )
    if date_fields_changed:
        existing = user_repo.get_by_id(user_id) or current_user
        method = data.get("pregnancy_counting_method") or existing.get("pregnancy_counting_method") or "lnmp"
        lnmp_d = data.get("lnmp_date") or (
            date.fromisoformat(existing["lnmp_date"]) if existing.get("lnmp_date") else None
        )
        us_d = data.get("ultrasound_date") or (
            date.fromisoformat(existing["ultrasound_date"]) if existing.get("ultrasound_date") else None
        )
        us_w = data.get("ultrasound_weeks", existing.get("ultrasound_weeks"))
        manual_w = data.get("gestational_age_weeks")

        calc_res = calculate_gestational_age_and_edd(
            pregnancy_counting_method=method,
            lnmp_date=lnmp_d,
            ultrasound_date=us_d,
            ultrasound_weeks=us_w,
            manual_gestational_weeks=manual_w,
        )
        if calc_res.get("gestational_age_weeks") is not None:
            data["gestational_age_weeks"] = calc_res["gestational_age_weeks"]
            data["gestational_age_days"] = calc_res["gestational_age_days"]
            data["is_gestational_age_manual"] = calc_res["is_gestational_age_manual"]
            data["effective_lnmp_date"] = (
                calc_res["effective_lnmp_date"].isoformat()
                if calc_res["effective_lnmp_date"]
                else None
            )
            data["estimated_due_date"] = (
                calc_res["estimated_due_date"].isoformat()
                if calc_res["estimated_due_date"]
                else None
            )
            data["trimester"] = calc_res["trimester"]

    # Convert dates to iso strings
    for k in ("lnmp_date", "ultrasound_date", "estimated_due_date", "effective_lnmp_date"):
        if k in data and isinstance(data[k], date):
            data[k] = data[k].isoformat()

    if data:
        user_repo.update_profile(user_id, data)

    fresh_user = user_repo.get_by_id(user_id) or current_user
    return _build_user_profile(fresh_user)


@router.put("/me/hospital", response_model=UserProfile)
@router.patch("/me/hospital", response_model=UserProfile)
def update_hospital(
    payload: HospitalUpdateRequest,
    current_user: dict = Depends(get_current_user),
) -> UserProfile:
    """Quick update endpoint for mother's preferred hospital / health center."""
    user_id = UUID(current_user["id"])
    UserRepository().update_hospital(user_id, payload.hospital)
    fresh_user = UserRepository().get_by_id(user_id) or current_user
    return _build_user_profile(fresh_user)


@router.put("/me/settings", response_model=UserProfile)
@router.patch("/me/settings", response_model=UserProfile)
def update_user_settings(
    payload: UserSettingsUpdate,
    current_user: dict = Depends(get_current_user),
) -> UserProfile:
    """Unified settings endpoint to update hospital, appointments, supplements, and maternal details."""
    user_id = UUID(current_user["id"])
    user_repo = UserRepository()
    app_repo = AppointmentRepository()
    supp_repo = SupplementRepository()

    if payload.hospital is not None:
        user_repo.update_hospital(user_id, payload.hospital)

    if payload.maternal_profile is not None:
        update_user_profile(payload.maternal_profile, current_user)

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

    fresh_user = user_repo.get_by_id(user_id) or current_user
    return _build_user_profile(fresh_user)


@router.get("/me/supplements", response_model=list[SupplementResponse])
def list_supplements(
    current_user: dict = Depends(get_current_user),
) -> list[SupplementResponse]:
    supplements = SupplementRepository().list_all(UUID(current_user["id"]))
    return [SupplementResponse(**s) for s in supplements]


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


@router.post("/me/food/verify", response_model=FoodVerifyResponse)
@router.post("/me/food-log", response_model=FoodVerifyResponse)
def verify_food_manually(
    payload: FoodVerifyRequest,
    current_user: dict = Depends(get_current_user),
) -> FoodVerifyResponse:
    """Manually verify/log food intake from the 4-food-group checkbox UI outside of voice intake.
    
    Logging food for today automatically causes the voice check-in session (POST /checkin/start)
    to skip Stage 2 (food)!
    """
    user_id = UUID(current_user["id"])
    raw_text = payload.raw_text or (
        ", ".join(payload.items) if payload.items else ", ".join(payload.food_groups)
    ) or "የዕለቱ ምግብ"

    # If food_groups is empty but raw_text/items are provided, classify automatically
    groups = payload.food_groups
    if not groups:
        groups = classify_ethiopian_food(raw_text)

    checkin_data = {
        "symptoms": [],
        "food_log": {
            "raw_text": raw_text,
            "food_groups": groups,
            "items": payload.items,
            "confirmed": True,
        },
        "supplement_check": None,
        "closing_mentions": [],
        "danger_sign_triggered": False,
    }

    CheckInRepository().create(user_id, checkin_data)

    return FoodVerifyResponse(
        status="verified",
        food_groups=groups,
        raw_text=raw_text,
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


@router.get("/me/anc-schedule", response_model=ANCScheduleResponse)
def get_user_anc_schedule(
    current_user: dict = Depends(get_current_user),
) -> ANCScheduleResponse:
    """Returns the full 8-contact WHO ANC schedule, next upcoming appointment, and calculated dates."""
    user_id = UUID(current_user["id"])
    user = UserRepository().get_by_id(user_id) or current_user
    status_info = get_current_pregnancy_status(user)

    eff_lnmp_str = user.get("effective_lnmp_date") or user.get("lnmp_date")
    if eff_lnmp_str:
        eff_lnmp_date = date.fromisoformat(eff_lnmp_str[:10])
    else:
        eff_lnmp_date = date.today()

    all_contacts = calculate_all_anc_dates(eff_lnmp_date)
    next_anc = get_next_anc_contact(eff_lnmp_date)

    return ANCScheduleResponse(
        current_gestational_age_weeks=status_info.get("gestational_age_weeks", 0) if status_info else 0,
        current_gestational_age_days=status_info.get("gestational_age_days", 0) if status_info else 0,
        effective_lnmp_date=eff_lnmp_date if eff_lnmp_str else None,
        estimated_due_date=date.fromisoformat(user["estimated_due_date"][:10]) if user.get("estimated_due_date") else None,
        next_anc_contact=next_anc,
        all_contacts=all_contacts,
    )
