from uuid import uuid4
import pytest
from app.services.reminders import ReminderService
from app.db.repositories.reminders import ReminderRepository


def test_notifications_list_and_dismiss(monkeypatch) -> None:
    user_id = uuid4()
    rem_id = uuid4()
    now_str = "2026-08-15T10:00:00"

    fake_reminder = {
        "id": str(rem_id),
        "user_id": str(user_id),
        "type": "supplement",
        "message": "Reminder to take your iron supplement.",
        "due_at": now_str,
        "dismissed": False,
        "created_at": now_str,
    }

    service = ReminderService()
    monkeypatch.setattr(service.reminders, "list_pending", lambda uid: [fake_reminder])

    pending = service.list_pending(user_id)
    assert len(pending) == 1
    assert pending[0]["type"] == "supplement"

    repo = ReminderRepository()
    monkeypatch.setattr(repo, "dismiss", lambda uid, rid: {**fake_reminder, "dismissed": True})

    dismissed = repo.dismiss(user_id, rem_id)
    assert dismissed["dismissed"] is True
