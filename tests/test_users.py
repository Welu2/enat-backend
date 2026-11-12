from uuid import uuid4

from app.db.repositories.supplements import SupplementRepository


def test_supplement_delete(monkeypatch) -> None:
    user_id = uuid4()
    supp_id = uuid4()
    repo = SupplementRepository()

    monkeypatch.setattr(repo, "delete", lambda uid, sid: True)
    assert repo.delete(user_id, supp_id) is True


def test_calendar_link_and_ical_generation() -> None:
    from datetime import date

    from app.services.calendar import (
        generate_google_calendar_url,
        generate_ical_content,
    )

    app_date = date(2026, 8, 25)
    gcal_url = generate_google_calendar_url(app_date)
    assert "https://calendar.google.com/calendar/render" in gcal_url
    assert "20260825T060000Z" in gcal_url

    ical_content = generate_ical_content(app_date)
    assert "BEGIN:VCALENDAR" in ical_content
    assert "DTSTART:20260825T060000Z" in ical_content
    assert "VALARM" in ical_content
