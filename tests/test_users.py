from uuid import uuid4
import pytest
from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.supplements import SupplementRepository


def test_appointment_upsert_and_delete(monkeypatch) -> None:
    user_id = uuid4()
    repo = AppointmentRepository()

    monkeypatch.setattr(repo, "get_by_user", lambda uid: None)
    monkeypatch.setattr(repo, "create", lambda uid, data: {"id": str(uuid4()), "user_id": str(uid), **data})

    created = repo.upsert(user_id, {"appointment_date": "2026-08-20", "reminder_lead_days": 2})
    assert created["appointment_date"] == "2026-08-20"

    monkeypatch.setattr(repo, "get_by_user", lambda uid: created)
    monkeypatch.setattr(repo, "update", lambda uid, data: {**created, **data})

    updated = repo.upsert(user_id, {"appointment_date": "2026-08-25"})
    assert updated["appointment_date"] == "2026-08-25"


def test_supplement_delete(monkeypatch) -> None:
    user_id = uuid4()
    supp_id = uuid4()
    repo = SupplementRepository()

    monkeypatch.setattr(repo, "delete", lambda uid, sid: True)
    assert repo.delete(user_id, supp_id) is True


def test_calendar_link_and_ical_generation() -> None:
    from datetime import date
    from app.services.calendar import generate_google_calendar_url, generate_ical_content

    app_date = date(2026, 8, 25)
    gcal_url = generate_google_calendar_url(app_date)
    assert "https://calendar.google.com/calendar/render" in gcal_url
    assert "20260825T090000Z" in gcal_url

    ical_content = generate_ical_content(app_date)
    assert "BEGIN:VCALENDAR" in ical_content
    assert "DTSTART:20260825T090000Z" in ical_content
    assert "VALARM" in ical_content
