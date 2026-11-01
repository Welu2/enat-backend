"""Script to execute standalone API requests against the FastAPI backend for the Calendar feature."""

import os

os.environ["ENVIRONMENT"] = "test"
os.environ["ENABLE_REQUEST_LIMITS"] = "false"
os.environ["RATE_LIMIT_SECRET"] = "test-limit-secret-at-least-32-characters"
os.environ["SUPABASE_URL"] = "https://example.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "test-service-role-key"
os.environ["SUPABASE_JWT_SECRET"] = "test-jwt-secret"

import json
from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.dependencies import get_current_user
from app.main import app

# In-memory storage to simulate real database state transitions
DATABASE = {}


class MockCalendarRepository:
    def create(self, user_id, data):
        item_id = str(uuid4())
        now = datetime.now(timezone.utc).isoformat()
        item = {
            "id": item_id,
            "user_id": str(user_id),
            "created_at": now,
            "updated_at": now,
            **data,
        }
        DATABASE[item_id] = item
        return item

    def list_by_user(self, user_id, from_date=None, to_date=None, item_type=None):
        items = [i for i in DATABASE.values() if i["user_id"] == str(user_id)]
        if from_date:
            items = [i for i in items if i["date"] >= str(from_date)]
        if to_date:
            items = [i for i in items if i["date"] <= str(to_date)]
        if item_type:
            items = [i for i in items if i["type"] == item_type]
        items.sort(key=lambda r: (r.get("date") or "", r.get("time") or ""))
        return items

    def get_by_id(self, user_id, item_id):
        item = DATABASE.get(str(item_id))
        if item and item["user_id"] == str(user_id):
            return item
        return None

    def update(self, user_id, item_id, data):
        item = self.get_by_id(user_id, item_id)
        if not item:
            return None
        now = datetime.now(timezone.utc).isoformat()
        item.update(data)
        item["updated_at"] = now
        DATABASE[str(item_id)] = item
        return item

    def delete(self, user_id, item_id):
        item = self.get_by_id(user_id, item_id)
        if not item:
            return False
        del DATABASE[str(item_id)]
        return True


def print_section(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_exchange(method: str, path: str, status_code: int, req_body=None, res_body=None):
    print(f"\n--> {method} {path}")
    if req_body:
        print(f"    Request Payload:  {json.dumps(req_body, ensure_ascii=False)}")
    print(f"<-- Status Code:     {status_code}")
    if res_body is not None:
        print(f"    Response Body:    {json.dumps(res_body, indent=2, ensure_ascii=False)}")


def main():
    test_user_id = str(uuid4())
    test_user = {"id": test_user_id, "email": "mother@example.com"}

    # Patch repository to use the in-memory state engine
    import app.api.routes.calendar as calendar_module
    calendar_module.CalendarItemRepository = MockCalendarRepository

    print_section("1. Security: Unauthenticated Request Test")
    client_unauth = TestClient(app)
    res = client_unauth.get("/users/me/calendar/items")
    print_exchange("GET", "/users/me/calendar/items", res.status_code, res_body=res.json())
    assert res.status_code == 401, f"Expected 401, got {res.status_code}"

    # Setup authenticated client
    app.dependency_overrides[get_current_user] = lambda: test_user
    client = TestClient(app)

    print_section("2. Input Validation: Invalid Payload Rejections")
    # Invalid type
    bad_type_payload = {"title": "Team sync", "type": "meeting", "date": "2026-11-05"}
    res = client.post("/users/me/calendar/items", json=bad_type_payload)
    print_exchange("POST", "/users/me/calendar/items (Invalid Type: 'meeting')", res.status_code, req_body=bad_type_payload, res_body=res.json())
    assert res.status_code == 422

    # Bad date format
    bad_date_payload = {"title": "Doctor visit", "type": "event", "date": "05/11/2026"}
    res = client.post("/users/me/calendar/items", json=bad_date_payload)
    print_exchange("POST", "/users/me/calendar/items (Invalid Date Format)", res.status_code, req_body=bad_date_payload, res_body=res.json())
    assert res.status_code == 422

    print_section("3. POST: Create Calendar Events and Tasks")
    # 3.1 Create Event
    event_payload = {
        "title": "Hospital Ultrasound Scan",
        "title_am": "የሆስፒታል አልትራሳውንድ ምርመራ",
        "type": "event",
        "date": "2026-11-10",
        "time": "10:30:00",
        "completed": False,
    }
    res_event = client.post("/users/me/calendar/items", json=event_payload)
    print_exchange("POST", "/users/me/calendar/items", res_event.status_code, req_body=event_payload, res_body=res_event.json())
    assert res_event.status_code == 201
    event_id = res_event.json()["id"]

    # 3.2 Create Task 1
    task1_payload = {
        "title": "Take Iron & Folic Acid Pills",
        "title_am": "የብረት እና ፎሊክ አሲድ እንክብል መውሰድ",
        "type": "task",
        "date": "2026-11-02",
        "time": "08:00:00",
        "completed": False,
    }
    res_task1 = client.post("/users/me/calendar/items", json=task1_payload)
    print_exchange("POST", "/users/me/calendar/items", res_task1.status_code, req_body=task1_payload, res_body=res_task1.json())
    assert res_task1.status_code == 201
    task1_id = res_task1.json()["id"]

    # 3.3 Create Task 2
    task2_payload = {
        "title": "Drink 2L Water",
        "title_am": "2 ሊትር ውሃ መጠጣት",
        "type": "task",
        "date": "2026-11-03",
        "time": "09:00:00",
        "completed": False,
    }
    res_task2 = client.post("/users/me/calendar/items", json=task2_payload)
    print_exchange("POST", "/users/me/calendar/items", res_task2.status_code, req_body=task2_payload, res_body=res_task2.json())
    assert res_task2.status_code == 201
    task2_id = res_task2.json()["id"]

    print_section("4. GET: List All Calendar Items")
    res_all = client.get("/users/me/calendar/items")
    print_exchange("GET", "/users/me/calendar/items", res_all.status_code, res_body=res_all.json())
    assert res_all.status_code == 200
    assert len(res_all.json()) == 3

    print_section("5. GET: Filter by Type (Events Only vs Tasks Only)")
    # Filter type=event
    res_events = client.get("/users/me/calendar/items?type=event")
    print_exchange("GET", "/users/me/calendar/items?type=event", res_events.status_code, res_body=res_events.json())
    assert res_events.status_code == 200
    assert len(res_events.json()) == 1
    assert res_events.json()[0]["id"] == event_id

    # Filter type=task
    res_tasks = client.get("/users/me/calendar/items?type=task")
    print_exchange("GET", "/users/me/calendar/items?type=task", res_tasks.status_code, res_body=res_tasks.json())
    assert res_tasks.status_code == 200
    assert len(res_tasks.json()) == 2

    print_section("6. GET: Filter by Date Range")
    res_date = client.get("/users/me/calendar/items?from_date=2026-11-01&to_date=2026-11-05")
    print_exchange("GET", "/users/me/calendar/items?from_date=2026-11-01&to_date=2026-11-05", res_date.status_code, res_body=res_date.json())
    assert res_date.status_code == 200
    assert len(res_date.json()) == 2  # Only the two tasks in early November

    print_section("7. PUT: Update Task (Mark as Completed & Change Time)")
    update_payload = {"completed": True, "time": "08:30:00"}
    res_update = client.put(f"/users/me/calendar/items/{task1_id}", json=update_payload)
    print_exchange("PUT", f"/users/me/calendar/items/{task1_id}", res_update.status_code, req_body=update_payload, res_body=res_update.json())
    assert res_update.status_code == 200
    assert res_update.json()["completed"] is True
    assert res_update.json()["time"] == "08:30:00"

    print_section("8. GET: Retrieve Single Item by ID")
    res_single = client.get(f"/users/me/calendar/items/{task1_id}")
    print_exchange("GET", f"/users/me/calendar/items/{task1_id}", res_single.status_code, res_body=res_single.json())
    assert res_single.status_code == 200
    assert res_single.json()["id"] == task1_id
    assert res_single.json()["completed"] is True

    print_section("9. DELETE: Remove Calendar Item")
    res_delete = client.delete(f"/users/me/calendar/items/{task2_id}")
    print_exchange("DELETE", f"/users/me/calendar/items/{task2_id}", res_delete.status_code, res_body=res_delete.json())
    assert res_delete.status_code == 200
    assert res_delete.json() == {"status": "deleted"}

    print_section("10. 404 Verification: Fetching Deleted or Missing Item")
    res_deleted_get = client.get(f"/users/me/calendar/items/{task2_id}")
    print_exchange("GET (Deleted Item)", f"/users/me/calendar/items/{task2_id}", res_deleted_get.status_code, res_body=res_deleted_get.json())
    assert res_deleted_get.status_code == 404

    print_section("ALL API REQUEST TESTS COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
