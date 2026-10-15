"""HTTP acceptance with real migrations/RLS and a mocked provider HTTP transport."""

import asyncio
import io
import json
import wave
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Event
from uuid import uuid4

import httpx
from fastapi.testclient import TestClient

from app import dependencies
from app.core.clock import LOCAL_ZONE, utc_now
from app.main import app
from app.services import provider_runtime
from tests.integration.test_security_database import db, pytestmark  # noqa: F401


def identity(monkeypatch, user):
    monkeypatch.setattr(
        dependencies,
        "decode_access_token",
        lambda token: {
            "sub": user["id"],
            "email": user["email"],
            "session_id": str(uuid4()),
            "iat": utc_now().timestamp(),
        },
    )
    return {"Authorization": "Bearer synthetic-journey"}


def wav():
    stream = io.BytesIO()
    with wave.open(stream, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(b"\x00\x00" * 1600)
    return stream.getvalue()


def provider(monkeypatch, entered=None, release=None):
    calls = []

    async def handle(request):
        calls.append(request.url.path)
        if request.url.path.endswith("/stt"):
            if entered is not None:
                entered.set()
                # Yield while waiting so other requests can resume/read the session.
                async with asyncio.timeout(10):
                    while not release.is_set():
                        await asyncio.sleep(0.01)
            return httpx.Response(200, json={"text": "synthetic patient transcript"})
        return httpx.Response(
            200,
            json={
                "text": json.dumps(
                    {
                        "symptoms": [
                            {
                                "raw_text": "synthetic patient transcript",
                                "category": None,
                            }
                        ]
                    }
                )
            },
        )

    original = provider_runtime.ProviderRuntime.__init__

    def init(self, settings=None, transport=None):
        original(self, settings, httpx.MockTransport(handle))

    monkeypatch.setattr(provider_runtime.ProviderRuntime, "__init__", init)
    return calls


def ok(response, code=200):
    assert response.status_code == code, response.text
    return response.json() if response.content else None


def test_onboarding_voice_correction_warning_completion_summary_share_revoke(
    db, monkeypatch
):
    _, user, other = db
    auth = identity(monkeypatch, user)
    calls = provider(monkeypatch)
    with TestClient(app) as client:
        profile = ok(
            client.post(
                "/users/me/onboarding",
                headers=auth,
                json={
                    "age": 26,
                    "pregnancy_counting_method": "lnmp",
                    "lnmp_date": (
                        utc_now().astimezone(LOCAL_ZONE).date() - timedelta(days=70)
                    ).isoformat(),
                    "supplements": ["iron", {"name": "calcium"}],
                    "hospital": "Synthetic health centre",
                },
            )
        )
        assert profile["onboarding_completed"] and len(profile["supplements"]) == 2
        appointment = profile["appointment"]
        start = ok(
            client.post(
                "/checkin/start", headers={**auth, "Idempotency-Key": "journey-start"}
            )
        )
        sid, version = start["session_id"], start["version"]

        def headers(key):
            return {**auth, "Idempotency-Key": key, "X-Session-Version": str(version)}

        result = ok(
            client.post(
                f"/checkin/{sid}/respond",
                headers=headers("journey-audio"),
                files={"audio": ("synthetic.wav", wav(), "audio/wav")},
            )
        )
        assert len(calls) == 2 and len(result["pending_items"]) == 1
        version = result["version"]
        pending = result["pending_items"][0]
        state = ok(client.get(f"/checkin/{sid}/state", headers=auth))
        assert not state["draft_data"]["symptoms"]
        assert (
            client.post(
                f"/checkin/{sid}/complete",
                headers=headers("unconfirmed-finish"),
                json={},
            ).status_code
            == 422
        )
        verified = ok(
            client.post(
                f"/checkin/{sid}/verify",
                headers=headers("journey-correction"),
                json={
                    "items": [
                        {
                            "item_id": pending["item_id"],
                            "confirmed": True,
                            "corrected_value": {
                                "raw_text": "synthetic bleeding",
                                "category": "vaginal_bleeding",
                                "severity": "mild",
                            },
                        }
                    ]
                },
            )
        )
        assert verified["danger_sign_triggered"] is True
        version = verified["version"]
        state = ok(client.get(f"/checkin/{sid}/state", headers=auth))
        assert state["status"] == "in_progress" and state["current_stage"] == "symptoms"
        assert state["draft_data"]["symptoms"][0]["confirmed_at"]
        for stage in ("symptoms", "food", "supplement", "closing"):
            state = ok(client.get(f"/checkin/{sid}/state", headers=auth))
            assert state["current_stage"] == stage
            if stage in ("food", "supplement"):
                value = (
                    {"raw_text": "synthetic meal"}
                    if stage == "food"
                    else {
                        "raw_text": "iron taken",
                        "supplement_name": "iron",
                        "taken_today": True,
                    }
                )
                added = ok(
                    client.post(
                        f"/checkin/{sid}/verify",
                        headers=headers(f"journey-{stage}"),
                        json={"items": [{"action": "add", "corrected_value": value}]},
                    )
                )
                version = added["version"]
            final = ok(
                client.post(
                    f"/checkin/{sid}/complete",
                    headers=headers(f"finish-{stage}"),
                    json={"skip": stage == "closing"},
                )
            )
            version = final["version"]
        assert final["session_completed"]
        history = ok(client.get("/checkin/history", headers=auth))
        assert len(history) == 1 and history[0]["symptoms"][0]["confirmed"] is True
        report = ok(
            client.post(
                "/summary/generate",
                headers={**auth, "Idempotency-Key": "journey-report"},
                json={},
            )
        )
        assert len(report["content_json"]["danger_signs"]) == 1
        assert ok(client.get("/users/me", headers=auth))["appointment"] == appointment
        shared = ok(
            client.post(
                f"/summary/{report['id']}/shares", headers=auth, json={"consent": True}
            ),
            201,
        )
        share_path = "/summary/" + shared["share_url"].rsplit("/", 1)[-1]
        public = client.get(share_path)
        assert public.status_code == 200 and "synthetic bleeding" not in public.text
        assert public.headers["cache-control"] == "no-store"
        other_auth = identity(monkeypatch, other)
        assert (
            client.get(f"/checkin/{sid}/state", headers=other_auth).status_code == 404
        )
        assert (
            client.delete(
                "/summary/shares/" + shared["id"], headers=other_auth
            ).status_code
            == 404
        )
        identity(monkeypatch, user)
        ok(client.delete("/summary/shares/" + shared["id"], headers=auth), 204)
        assert client.get(share_path).status_code == 404


def test_slow_response_lost_by_client_reconnects_and_replays_without_provider_charge(
    db, monkeypatch
):
    admin, user, _ = db
    auth = identity(monkeypatch, user)
    entered, release = Event(), Event()
    calls = provider(monkeypatch, entered, release)
    with TestClient(app) as client:
        start = ok(
            client.post(
                "/checkin/start", headers={**auth, "Idempotency-Key": "slow-start"}
            )
        )
        sid = start["session_id"]
        headers = {
            **auth,
            "Idempotency-Key": "slow-audio-retry",
            "X-Session-Version": "0",
        }

        def submit():
            return client.post(
                f"/checkin/{sid}/respond",
                headers=headers,
                files={"audio": ("synthetic.wav", wav(), "audio/wav")},
            )

        with ThreadPoolExecutor(max_workers=1) as pool:
            pending = pool.submit(submit)
            try:
                assert entered.wait(5)
                state = ok(client.get(f"/checkin/{sid}/state", headers=auth))
                assert state["version"] == 0 and state["pending_items"] == []
            finally:
                release.set()
            # The server commits; model a client that loses/discards the response.
            assert pending.result(timeout=15).status_code == 200
    with TestClient(app) as reconnected:
        state = ok(reconnected.get(f"/checkin/{sid}/state", headers=auth))
        assert state["version"] == 1 and len(state["pending_items"]) == 1
        replay = ok(
            reconnected.post(
                f"/checkin/{sid}/respond",
                headers=headers,
                files={"audio": ("synthetic.wav", wav(), "audio/wav")},
            )
        )
        assert (
            replay["version"] == 1 and replay["pending_items"] == state["pending_items"]
        )
        assert len(calls) == 2
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM mutation_results WHERE user_id=%s", (user["id"],)
        ).fetchone()["n"]
        == 2
    )


def test_settings_missing_owned_supplement_rolls_back_prior_hospital_write(
    db, monkeypatch
):
    admin, user, _ = db
    auth = identity(monkeypatch, user)
    with TestClient(app) as client:
        response = client.patch(
            "/users/me/settings",
            headers=auth,
            json={
                "hospital": "Must roll back",
                "supplements": [{"id": str(uuid4()), "name": "missing"}],
            },
        )
        assert response.status_code == 404
        assert ok(client.get("/users/me", headers=auth))["hospital"] is None
    assert (
        admin.execute(
            "SELECT hospital FROM users WHERE id=%s", (user["id"],)
        ).fetchone()["hospital"]
        is None
    )


def test_onboarding_late_write_failure_rolls_back_profile_and_supplements(
    db, monkeypatch
):
    from app.core.errors import DataUnavailable
    from app.db.repositories.appointments import AppointmentRepository

    _, user, _ = db
    auth = identity(monkeypatch, user)

    def fail(*args, **kwargs):
        raise DataUnavailable("synthetic internal detail")

    monkeypatch.setattr(AppointmentRepository, "create", fail)
    with TestClient(app) as client:
        response = client.post(
            "/users/me/onboarding",
            headers=auth,
            json={
                "lnmp_date": (
                    utc_now().astimezone(LOCAL_ZONE).date() - timedelta(days=70)
                ).isoformat(),
                "hospital": "Must roll back",
                "supplements": ["iron"],
            },
        )
        assert (
            response.status_code == 503
            and "synthetic internal detail" not in response.text
        )
        profile = ok(client.get("/users/me", headers=auth))
        assert not profile["onboarding_completed"] and not profile["supplements"]
        assert profile["hospital"] is None
