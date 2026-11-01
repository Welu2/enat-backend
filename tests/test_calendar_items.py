from datetime import date, datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_current_user
from app.main import app


@pytest.fixture
def test_user():
    return {"id": str(uuid4()), "email": "mother@example.com"}


@pytest.fixture
def auth_client(test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user
    client = TestClient(app)
    yield client, test_user
    app.dependency_overrides.clear()


@pytest.mark.enable_socket
def test_create_and_list_calendar_items(auth_client, monkeypatch):
    client, user = auth_client
    user_id = user["id"]
    item_id = str(uuid4())
    now = datetime.now(timezone.utc).isoformat()

    fake_item = {
        "id": item_id,
        "user_id": user_id,
        "title": "Prenatal yoga",
        "title_am": "የቅድመ ወሊድ ዮጋ",
        "type": "event",
        "date": "2026-11-05",
        "time": "18:00:00",
        "reminder_at": None,
        "completed": False,
        "created_at": now,
        "updated_at": now,
    }

    mock_repo = Mock()
    mock_repo.create.return_value = fake_item
    mock_repo.list_by_user.return_value = [fake_item]

    monkeypatch.setattr(
        "app.api.routes.calendar.CalendarItemRepository", lambda: mock_repo
    )

    # 1. Test POST /users/me/calendar/items
    create_payload = {
        "title": "Prenatal yoga",
        "title_am": "የቅድመ ወሊድ ዮጋ",
        "type": "event",
        "date": "2026-11-05",
        "time": "18:00:00",
        "completed": False,
    }
    res = client.post("/users/me/calendar/items", json=create_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["id"] == item_id
    assert data["title"] == "Prenatal yoga"
    assert data["type"] == "event"
    assert data["completed"] is False

    # 2. Test GET /users/me/calendar/items
    res = client.get("/users/me/calendar/items?from_date=2026-11-01&type=event")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["title"] == "Prenatal yoga"


@pytest.mark.enable_socket
def test_get_and_update_calendar_item(auth_client, monkeypatch):
    client, user = auth_client
    user_id = user["id"]
    item_id = str(uuid4())
    now = datetime.now(timezone.utc).isoformat()

    fake_item = {
        "id": item_id,
        "user_id": user_id,
        "title": "Take iron pills",
        "title_am": "የብረት እንክብል መውሰድ",
        "type": "task",
        "date": "2026-11-02",
        "time": "08:00:00",
        "reminder_at": None,
        "completed": False,
        "created_at": now,
        "updated_at": now,
    }

    mock_repo = Mock()
    mock_repo.get_by_id.return_value = fake_item
    mock_repo.update.return_value = {**fake_item, "completed": True}

    monkeypatch.setattr(
        "app.api.routes.calendar.CalendarItemRepository", lambda: mock_repo
    )

    # Test GET /users/me/calendar/items/{id}
    res = client.get(f"/users/me/calendar/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["completed"] is False

    # Test PUT /users/me/calendar/items/{id}
    res = client.put(
        f"/users/me/calendar/items/{item_id}",
        json={"completed": True},
    )
    assert res.status_code == 200
    assert res.json()["completed"] is True


@pytest.mark.enable_socket
def test_delete_calendar_item(auth_client, monkeypatch):
    client, user = auth_client
    item_id = str(uuid4())

    mock_repo = Mock()
    mock_repo.delete.side_effect = lambda uid, iid: True if str(iid) == item_id else False

    monkeypatch.setattr(
        "app.api.routes.calendar.CalendarItemRepository", lambda: mock_repo
    )

    # Existing item
    res = client.delete(f"/users/me/calendar/items/{item_id}")
    assert res.status_code == 200
    assert res.json() == {"status": "deleted"}

    # Non-existent item (404)
    missing_id = str(uuid4())
    res = client.delete(f"/users/me/calendar/items/{missing_id}")
    assert res.status_code == 404


@pytest.mark.enable_socket
def test_unauthenticated_request_rejected():
    client = TestClient(app)
    res = client.get("/users/me/calendar/items")
    assert res.status_code == 401


@pytest.mark.enable_socket
def test_validation_errors_rejected(auth_client):
    client, _ = auth_client

    # Invalid type
    res = client.post(
        "/users/me/calendar/items",
        json={"title": "Invalid Type", "type": "meeting", "date": "2026-11-05"},
    )
    assert res.status_code == 422

    # Missing title
    res = client.post(
        "/users/me/calendar/items",
        json={"type": "event", "date": "2026-11-05"},
    )
    assert res.status_code == 422

    # Invalid date format
    res = client.post(
        "/users/me/calendar/items",
        json={"title": "Bad Date", "type": "task", "date": "not-a-date"},
    )
    assert res.status_code == 422


@pytest.mark.enable_socket
def test_get_not_found_item(auth_client, monkeypatch):
    client, _ = auth_client
    mock_repo = Mock()
    mock_repo.get_by_id.return_value = None
    mock_repo.update.return_value = None
    monkeypatch.setattr(
        "app.api.routes.calendar.CalendarItemRepository", lambda: mock_repo
    )

    missing_id = str(uuid4())
    res = client.get(f"/users/me/calendar/items/{missing_id}")
    assert res.status_code == 404

    res = client.put(f"/users/me/calendar/items/{missing_id}", json={"completed": True})
    assert res.status_code == 404

