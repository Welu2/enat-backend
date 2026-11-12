from uuid import uuid4

from app.db.repositories.reminders import ReminderRepository
from app.services.reminders import ReminderService


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
    monkeypatch.setattr(
        repo, "dismiss", lambda uid, rid: {**fake_reminder, "dismissed": True}
    )

    dismissed = repo.dismiss(user_id, rem_id)
    assert dismissed["dismissed"] is True


def test_notifications_include_dismissed(monkeypatch) -> None:
    from fastapi import Response
    from app.api.routes import notifications as notif_route

    user_id = uuid4()
    item_active = {
        "id": str(uuid4()),
        "user_id": str(user_id),
        "type": "checkin",
        "message": "Daily checkin reminder",
        "due_at": "2026-08-15T08:00:00",
        "dismissed": False,
        "created_at": "2026-08-15T08:00:00",
    }
    item_dismissed = {
        "id": str(uuid4()),
        "user_id": str(user_id),
        "type": "supplement",
        "message": "Supplement reminder from yesterday",
        "due_at": "2026-08-14T08:00:00",
        "dismissed": True,
        "created_at": "2026-08-14T08:00:00",
    }

    monkeypatch.setattr(
        notif_route,
        "list_reminders",
        lambda resp, uid, lim, cur, include_dismissed=False: (
            [item_active, item_dismissed] if include_dismissed else [item_active]
        ),
    )

    resp = Response()
    res = notif_route.get_notifications(resp, user_id=user_id, include_dismissed=True)
    assert len(res) == 2
    assert res[0].dismissed is False
    assert res[1].dismissed is True

    res_only_active = notif_route.get_notifications(resp, user_id=user_id, include_dismissed=False)
    assert len(res_only_active) == 1
    assert res_only_active[0].dismissed is False
