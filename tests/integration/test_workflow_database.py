"""Integrity acceptance tests using the restricted app role and real transactions."""

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from unittest.mock import AsyncMock
from uuid import uuid4

import psycopg
import pytest
from psycopg.types.json import Jsonb

from app.core.clock import LOCAL_ZONE, utc_now
from app.core.errors import (
    Conflict,
    DataUnavailable,
    InvalidMutation,
    ProviderUnavailable,
)
from app.db import data, idempotency
from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.check_in_sessions import CheckInSessionRepository
from app.db.repositories.check_ins import CheckInRepository
from app.services.checkin_session import CheckInSessionService, _empty_draft_data
from app.services.clinical_policy import normalize_item
from app.services.summary import SummaryService
from tests.integration.test_security_database import acting, db, pytestmark  # noqa: F401


def session(uid, stage="closing", draft=None, pending=None):
    return CheckInSessionRepository().create(
        uid,
        {
            "current_stage": stage,
            "stage_order": [stage],
            "stage_status": "awaiting_confirmation" if pending else "ready",
            "pending_items": pending or [],
            "draft_data": draft or _empty_draft_data(),
        },
    )


def counts(admin, uid):
    # Fresh statement snapshots see commits made by the application connection.
    return [
        admin.execute(
            f"SELECT count(*) AS n FROM {table} WHERE user_id=%s", (uid,)
        ).fetchone()["n"]
        for table in ("check_ins", "domain_outbox", "mutation_results")
    ]


def test_concurrent_completion_is_one_atomic_result_even_with_different_retry_keys(db):
    admin, a, _ = db
    with acting(a["id"]):
        record = session(a["id"])
    gate = Barrier(8)

    def finish(n):
        with acting(a["id"]):
            gate.wait()
            return CheckInSessionService().complete_stage(
                a["id"], record["id"], expected_version=0, key=f"finish-{n}"
            )

    with ThreadPoolExecutor(max_workers=8) as workers:
        results = list(workers.map(finish, range(8)))
    assert all(result == results[0] for result in results)
    assert counts(admin, a["id"])[:2] == [1, 1]
    with acting(a["id"]):
        assert (
            CheckInSessionService().complete_stage(
                a["id"], record["id"], expected_version=0
            )
            == results[0]
        )
        stored = CheckInSessionRepository().get(record["id"], a["id"])
        assert stored["version"] == 1 and stored["terminal_result"] == results[0]
        with pytest.raises(DataUnavailable):
            data.get_data_client().table("check_ins").insert(
                {"user_id": a["id"], "session_id": record["id"]}
            ).execute()


@pytest.mark.parametrize("failure_point", ["outbox", "session"])
def test_completion_rolls_back_every_write_on_failure(db, monkeypatch, failure_point):
    admin, a, _ = db
    service = CheckInSessionService()
    with acting(a["id"]):
        record = session(a["id"])

        def fail(*args, **kwargs):
            raise RuntimeError("injected crash")

        with monkeypatch.context() as m:
            m.setattr(
                idempotency if failure_point == "outbox" else service.sessions,
                "emit" if failure_point == "outbox" else "update",
                fail,
            )
            with pytest.raises(RuntimeError):
                service.complete_stage(
                    a["id"], record["id"], expected_version=0, key="rollback-retry"
                )
        assert counts(admin, a["id"]) == [0, 0, 0]
        assert service.get_state(a["id"], record["id"])["status"] == "in_progress"
        assert service.complete_stage(
            a["id"], record["id"], expected_version=0, key="rollback-retry"
        )["session_completed"]


def test_concurrent_verifications_cannot_overwrite_each_other(db):
    _, a, _ = db
    item = normalize_item(
        "symptoms", {"raw_text": "bleeding", "category": "vaginal_bleeding"}
    )
    with acting(a["id"]):
        record = session(a["id"], "symptoms", pending=[item])
    gate = Barrier(2)

    def verify(n):
        with acting(a["id"]):
            gate.wait()
            try:
                return CheckInSessionService().verify_item(
                    a["id"],
                    record["id"],
                    item["item_id"],
                    expected_version=0,
                    key=f"verify-{n}",
                )
            except Conflict:
                return "conflict"

    with ThreadPoolExecutor(max_workers=2) as workers:
        results = list(workers.map(verify, range(2)))
    assert results.count("conflict") == 1
    with acting(a["id"]):
        stored = CheckInSessionRepository().get(record["id"], a["id"])
        assert len(stored["draft_data"]["symptoms"]) == 1
        assert stored["draft_data"]["symptoms"][0]["confirmed_at"]


@pytest.mark.asyncio
async def test_slow_provider_response_is_rejected_after_stage_transition(
    db, monkeypatch
):
    _, a, _ = db
    service = CheckInSessionService()
    entered, resume = asyncio.Event(), asyncio.Event()

    async def delayed(*args):
        assert data._active_transaction.get() is None
        entered.set()
        await resume.wait()
        return "test transcript"

    monkeypatch.setattr(service.asr, "transcribe", delayed)
    monkeypatch.setattr(service.extraction, "extract", AsyncMock(return_value=[]))
    with acting(a["id"]):
        record = session(a["id"])
        task = asyncio.create_task(
            service.respond(
                a["id"],
                record["id"],
                b"audio",
                "a.wav",
                "audio/wav",
                expected_version=0,
                key="slow-provider",
            )
        )
        await entered.wait()
        result = await asyncio.to_thread(
            service.complete_stage,
            a["id"],
            record["id"],
            expected_version=0,
            key="complete-first",
        )
        resume.set()
        with pytest.raises(Conflict):
            await task
        assert service.get_state(a["id"], record["id"])["terminal_result"] == result


@pytest.mark.asyncio
async def test_failed_provider_preserves_draft_and_retry_key(db, monkeypatch):
    _, a, _ = db
    service = CheckInSessionService()
    monkeypatch.setattr(service.asr, "transcribe", AsyncMock(side_effect=TimeoutError))
    with acting(a["id"]):
        record = session(a["id"])
        with pytest.raises(ProviderUnavailable):
            await service.respond(
                a["id"],
                record["id"],
                b"audio",
                "a.wav",
                "audio/wav",
                expected_version=0,
                key="outage-retry",
            )
        assert service.get_state(a["id"], record["id"])["version"] == 0
        assert (
            idempotency.lookup(
                a["id"], f"checkin:{record['id']}:respond", "outage-retry", {}
            )
            is None
        )


def test_retry_key_scopes_conflicts_and_atomic_bulk_validation(db):
    _, a, b = db
    with acting(a["id"]):
        record = session(a["id"], "food")
        service = CheckInSessionService()
        inputs = [
            {"action": "add", "corrected_value": {"raw_text": "injera"}},
            {"action": "add", "corrected_value": {"raw_text": "milk"}},
        ]
        result = service.verify_item(
            a["id"],
            record["id"],
            items_payload=inputs,
            expected_version=0,
            key="same-key",
        )
        assert (
            service.verify_item(
                a["id"],
                record["id"],
                items_payload=inputs,
                expected_version=0,
                key="same-key",
            )
            == result
        )
        with pytest.raises(Conflict):
            service.verify_item(
                a["id"],
                record["id"],
                items_payload=inputs[:1],
                expected_version=0,
                key="same-key",
            )
        assert idempotency.execute(
            a["id"], "other-operation", "same-key", {}, lambda: {"other": True}
        ) == {"other": True}
        with pytest.raises(InvalidMutation):
            service.verify_item(
                a["id"],
                record["id"],
                items_payload=inputs + [{"item_id": "missing"}],
                expected_version=1,
                key="bad-bulk",
            )
        final = service.complete_stage(a["id"], record["id"], expected_version=1)
        foods = CheckInRepository().get_by_id(a["id"], final["check_in_id"])["food_log"]
        assert [f["raw_text"] for f in foods] == ["injera", "milk"]
    with acting(b["id"]):
        assert idempotency.execute(
            b["id"], "other-operation", "same-key", {}, lambda: {"other": False}
        ) == {"other": False}
        assert data.transaction
        with data.transaction() as conn:
            assert (
                conn.execute(
                    "SELECT count(*) AS n FROM mutation_results WHERE user_id=%s",
                    (a["id"],),
                ).fetchone()["n"]
                == 0
            )


def test_unknown_items_and_unconfirmed_persistence_are_rejected(db):
    _, a, _ = db
    with acting(a["id"]):
        service = CheckInSessionService()
        item = normalize_item("closing", {"raw_text": "question"})
        record = session(a["id"], pending=[item])
        with pytest.raises(InvalidMutation):
            service.verify_item(a["id"], record["id"], "wrong-id", expected_version=0)
        with pytest.raises(InvalidMutation):
            service.complete_stage(a["id"], record["id"], expected_version=0, skip=True)
        with pytest.raises(InvalidMutation):
            CheckInRepository().create(a["id"], {"food_log": [{"raw_text": "milk"}]})
        with pytest.raises(DataUnavailable):
            data.get_data_client().table("check_ins").insert(
                {
                    "user_id": a["id"],
                    "food_log": [{"raw_text": "milk", "confirmed": True}],
                }
            ).execute()


def test_multiple_supplements_preserved_and_not_inferred(db):
    _, a, _ = db
    with acting(a["id"]):
        service = CheckInSessionService()
        record = session(a["id"], "supplement")
        inputs = [
            {
                "action": "add",
                "corrected_value": {
                    "raw_text": name,
                    "supplement_name": name,
                    "taken_today": taken,
                },
            }
            for name, taken in [("iron", True), ("calcium", False), ("unknown", None)]
        ]
        service.verify_item(
            a["id"], record["id"], items_payload=inputs, expected_version=0
        )
        final = service.complete_stage(a["id"], record["id"], expected_version=1)
        saved = CheckInRepository().get_by_id(a["id"], final["check_in_id"])
        assert [i["supplement_name"] for i in saved["supplement_check"]] == [
            "iron",
            "calcium",
            "unknown",
        ]
        assert (
            SummaryService._aggregate([saved])["supplement_adherence"]["percentage"]
            == 50
        )


def test_report_exact_window_all_rows_immutable_outbox_and_appointment_unchanged(db):
    admin, a, _ = db
    start = utc_now() - timedelta(days=2)
    end = start + timedelta(days=1)
    item = normalize_item("food", {"raw_text": "milk"}, confirm=True)
    # More than the former API's 1000-row limit, plus rows on both boundaries.
    admin.execute(
        "INSERT INTO check_ins(user_id,timestamp,food_log) SELECT %s,%s + n*interval '1 second',%s FROM generate_series(0,1004) n",
        (a["id"], start, Jsonb([item])),
    )
    admin.execute(
        "INSERT INTO check_ins(user_id,timestamp,food_log) VALUES(%s,%s,%s),(%s,%s,%s)",
        (
            a["id"],
            end,
            Jsonb([item]),
            a["id"],
            start - timedelta(microseconds=1),
            Jsonb([item]),
        ),
    )
    admin.commit()
    with acting(a["id"]):
        appointment = AppointmentRepository().create(
            a["id"], {"appointment_date": end.date().isoformat()}
        )
        service = SummaryService()
        report = service.generate(
            a["id"], period_start=start, period_end=end, key="report-window"
        )
        assert len(report["content_json"]["food_logs"]) == 1005
        assert (
            report["window_start"] == start.isoformat()
            and report["window_end"] == end.isoformat()
        )
        assert AppointmentRepository().get_by_user(a["id"]) == appointment
        assert (
            service.generate(
                a["id"], period_start=start, period_end=end, key="report-window"
            )
            == report
        )
        empty = service.generate(
            a["id"],
            period_start=end + timedelta(seconds=1),
            period_end=end + timedelta(hours=1),
        )
        assert empty["content_json"]["food_logs"] == []
        with pytest.raises(DataUnavailable):
            data.get_data_client().table("summaries").update({"content_json": {}}).eq(
                "id", report["id"]
            ).execute()
    with pytest.raises(psycopg.errors.CheckViolation):
        admin.execute(
            "UPDATE summaries SET content_json='{}' WHERE id=%s", (report["id"],)
        )
    admin.rollback()
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM domain_outbox WHERE user_id=%s AND event_type='summary.created'",
            (a["id"],),
        ).fetchone()["n"]
        == 2
    )


def test_summary_outbox_failure_rolls_back_snapshot(db, monkeypatch):
    admin, a, _ = db
    with acting(a["id"]):
        monkeypatch.setattr(
            idempotency,
            "emit",
            lambda *args: (_ for _ in ()).throw(RuntimeError("outbox crash")),
        )
        with pytest.raises(RuntimeError):
            SummaryService().generate(a["id"], key="summary-crash")
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM summaries WHERE user_id=%s", (a["id"],)
        ).fetchone()["n"]
        == 0
    )


def test_concurrent_auto_reports_do_not_consume_appointment(db):
    _, a, _ = db
    with acting(a["id"]):
        appointment = AppointmentRepository().create(
            a["id"],
            {"appointment_date": utc_now().astimezone(LOCAL_ZONE).date().isoformat()},
        )
    gate = Barrier(4)

    def generate(_):
        with acting(a["id"]):
            gate.wait()
            return SummaryService().check_and_generate_auto_summary(a["id"])

    with ThreadPoolExecutor(max_workers=4) as workers:
        results = list(workers.map(generate, range(4)))
    assert len({r["id"] for r in results}) == 1
    with acting(a["id"]):
        assert AppointmentRepository().get_by_user(a["id"]) == appointment


def test_appointment_attendance_and_reschedule_require_explicit_version(db):
    admin, a, _ = db
    with acting(a["id"]):
        repo = AppointmentRepository()
        old = repo.upsert(
            a["id"], {"appointment_date": "2026-01-01", "anc_contact_number": 1}
        )
        missed = repo.transition(a["id"], "missed", 0)
        assert missed["status"] == "missed" and missed["anc_contact_number"] == 1
        with pytest.raises(Conflict):
            repo.transition(a["id"], "completed", 0)
        moved = repo.transition(
            a["id"], "rescheduled", 1, appointment_date="2026-02-01"
        )
        assert moved["status"] == "scheduled" and moved["anc_contact_number"] == 1
        completed = repo.transition(a["id"], "completed", 2)
        assert completed["previous_appointment_date"] == "2026-02-01"
        assert completed["anc_contact_number"] == 1 and completed["id"] == old["id"]
        with pytest.raises(Conflict):
            repo.upsert(a["id"], {"appointment_date": "2026-03-01"})
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM appointment_events WHERE user_id=%s", (a["id"],)
        ).fetchone()["n"]
        == 3
    )


@pytest.mark.skipif(
    os.environ.get("ENAT_TEST_HAS_LEGACY") != "1", reason="Upgrade-only fixture"
)
def test_upgrade_wraps_singletons_without_manufacturing_confirmation(db):
    admin, _, _ = db
    rows = admin.execute(
        "SELECT * FROM check_ins WHERE user_id='00000000-0000-4000-8000-000000000001'"
    ).fetchall()
    assert len(rows) == 1
    assert rows[0]["food_log"][0]["raw_text"] == "legacy food"
    assert rows[0]["food_log"][0].get("confirmed") is not True
    assert SummaryService._aggregate(data.normalize(rows))["food_logs"] == []


def test_http_checkin_confirmation_summary_share_and_revoke(db, monkeypatch):
    from fastapi.testclient import TestClient

    from app import dependencies
    from app.main import app

    admin, a, b = db
    claims = {
        "sub": a["id"],
        "email": a["email"],
        "session_id": str(uuid4()),
        "iat": utc_now().timestamp(),
    }
    monkeypatch.setattr(dependencies, "decode_access_token", lambda token: claims)
    client = TestClient(app)
    auth = {"Authorization": "Bearer synthetic-token"}
    assert client.post("/checkin/start", headers=auth).status_code == 422
    response = client.post(
        "/checkin/start", headers={**auth, "Idempotency-Key": "http-start"}
    )
    assert response.status_code == 200, response.text
    sid = response.json()["session_id"]
    version = 0

    def headers(key):
        return {**auth, "Idempotency-Key": key, "X-Session-Version": str(version)}

    assert (
        client.post(
            f"/checkin/{sid}/verify",
            headers=headers("bad-flag"),
            json={
                "items": [
                    {
                        "action": "add",
                        "corrected_value": {"raw_text": "test", "danger_sign": False},
                    }
                ]
            },
        ).status_code
        == 422
    )
    assert (
        client.post(
            f"/checkin/{sid}/verify",
            headers=headers("unknown-item"),
            json={"items": [{"item_id": "not-an-item"}]},
        ).status_code
        == 422
    )
    add = client.post(
        f"/checkin/{sid}/verify",
        headers=headers("http-symptom"),
        json={
            "items": [
                {
                    "action": "add",
                    "corrected_value": {
                        "raw_text": "synthetic bleeding",
                        "category": "vaginal_bleeding",
                        "severity": "mild",
                    },
                }
            ]
        },
    )
    assert add.status_code == 200, add.text
    assert (
        add.json()["danger_sign_triggered"] is True
    )  # Warning before other stages finish.
    version = add.json()["version"]
    complete = client.post(
        f"/checkin/{sid}/complete", headers=headers("http-stage1"), json={}
    )
    assert complete.status_code == 200, complete.text
    version = complete.json()["version"]
    state = client.get(f"/checkin/{sid}/state", headers=auth).json()
    assert state["version"] == version and state["current_stage"] == "food"
    add = client.post(
        f"/checkin/{sid}/verify",
        headers=headers("http-food"),
        json={
            "items": [
                {"action": "add", "corrected_value": {"raw_text": "injera"}},
                {"action": "add", "corrected_value": {"raw_text": "milk"}},
            ]
        },
    )
    assert add.status_code == 200, add.text
    # An older version gets a conflict rather than overwriting the food list.
    stale = client.post(
        f"/checkin/{sid}/complete", headers=headers("stale-complete"), json={}
    )
    assert stale.status_code == 409
    version = add.json()["version"]
    complete = client.post(
        f"/checkin/{sid}/complete", headers=headers("http-stage2"), json={}
    )
    version = complete.json()["version"]
    final = client.post(
        f"/checkin/{sid}/complete", headers=headers("http-stage3"), json={"skip": True}
    )
    assert final.status_code == 200, final.text
    assert final.json()["session_completed"] is True
    assert (
        client.post(
            f"/checkin/{sid}/complete",
            headers=headers("retry-new-key"),
            json={"skip": True},
        ).json()
        == final.json()
    )
    history = client.get("/checkin/history", headers=auth).json()
    assert len(history) == 1 and len(history[0]["food_log"]) == 2
    report = client.post(
        "/summary/generate", headers={**auth, "Idempotency-Key": "http-report"}, json={}
    )
    assert report.status_code == 200, report.text
    assert len(report.json()["content_json"]["danger_signs"]) == 1
    assert len(report.json()["content_json"]["food_logs"]) == 2
    share = client.post(
        f"/summary/{report.json()['id']}/shares", headers=auth, json={"consent": True}
    )
    assert share.status_code == 201, share.text
    token = share.json()["share_url"].rsplit("/", 1)[-1]
    public = client.get("/summary/" + token)
    assert public.status_code == 200 and "synthetic bleeding" not in public.text
    assert (
        client.delete("/summary/shares/" + share.json()["id"], headers=auth).status_code
        == 204
    )
    assert client.get("/summary/" + token).status_code == 404


def test_qr_failure_can_be_retried_without_another_snapshot_or_share(db, monkeypatch):
    from app.core.errors import ArtifactUnavailable, NotFound
    from app.services import sharing

    admin, a, b = db
    with acting(a["id"]):
        snapshot = SummaryService().generate(a["id"])
        with monkeypatch.context() as m:
            m.setattr(
                sharing,
                "generate_qr_png",
                lambda *args: (_ for _ in ()).throw(
                    ArtifactUnavailable("render failure")
                ),
            )
            share = sharing.create_share(
                a["id"], snapshot["id"], sharing.ShareRequest(consent=True)
            )
        assert (
            share["qr_status"] == "retry_required" and share["qr_code_base64"] is None
        )
        token = share["share_url"].rsplit("/", 1)[-1]
        assert sharing.render_share_qr(a["id"], share["id"], token).startswith(
            b"\x89PNG"
        )
        sharing.revoke_share(a["id"], share["id"])
        with pytest.raises(NotFound):
            sharing.render_share_qr(a["id"], share["id"], token)
    with acting(b["id"]), pytest.raises(NotFound):
        sharing.render_share_qr(b["id"], share["id"], token)
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM summaries WHERE user_id=%s", (a["id"],)
        ).fetchone()["n"]
        == 1
    )
    assert (
        admin.execute(
            "SELECT count(*) AS n FROM summary_shares WHERE user_id=%s", (a["id"],)
        ).fetchone()["n"]
        == 1
    )


@pytest.mark.asyncio
async def test_slow_voice_correction_cannot_overwrite_confirmed_item(db, monkeypatch):
    _, a, _ = db
    service = CheckInSessionService()
    entered, resume = asyncio.Event(), asyncio.Event()

    async def delayed(*args):
        assert data._active_transaction.get() is None
        entered.set()
        await resume.wait()
        return "a correction"

    monkeypatch.setattr(service.asr, "transcribe", delayed)
    monkeypatch.setattr(
        service.extraction,
        "extract",
        AsyncMock(return_value=[{"raw_text": "different text", "category": None}]),
    )
    with acting(a["id"]):
        item = normalize_item(
            "symptoms", {"raw_text": "bleeding", "category": "vaginal_bleeding"}
        )
        record = session(a["id"], "symptoms", pending=[item])
        with pytest.raises(InvalidMutation):
            await service.voice_correct_item(
                a["id"],
                record["id"],
                "unknown",
                b"audio",
                "a.wav",
                "audio/wav",
                expected_version=0,
            )
        assert not entered.is_set()
        task = asyncio.create_task(
            service.voice_correct_item(
                a["id"],
                record["id"],
                item["item_id"],
                b"audio",
                "a.wav",
                "audio/wav",
                expected_version=0,
                key="slow-correction",
            )
        )
        await entered.wait()
        await asyncio.to_thread(
            service.verify_item,
            a["id"],
            record["id"],
            item["item_id"],
            expected_version=0,
            key="confirm-first",
        )
        resume.set()
        with pytest.raises(Conflict):
            await task
        stored = service.get_state(a["id"], record["id"])
        assert stored["pending_items"] == []
        assert stored["draft_data"]["symptoms"][0]["category"] == "vaginal_bleeding"
        assert stored["draft_data"]["symptoms"][0]["confirmed"] is True


def test_manual_supplements_require_selection_and_cover_each_active_supplement(db):
    from app.db.repositories.supplements import SupplementRepository
    from app.models.user import SupplementVerifyRequest
    from app.services.manual_intake import log_supplement

    admin, a, _ = db
    with acting(a["id"]):
        iron = SupplementRepository().create(a["id"], {"name": "iron"})
        calcium = SupplementRepository().create(a["id"], {"name": "calcium"})
        with pytest.raises(InvalidMutation):
            log_supplement(
                a["id"], SupplementVerifyRequest(taken_today=True), None, "no-selection"
            )
        no = SupplementVerifyRequest(taken_today=False)
        result = log_supplement(a["id"], no, iron["id"], "manual-iron")
        assert log_supplement(a["id"], no, iron["id"], "manual-iron") == result
        assert not CheckInRepository().has_supplement_logged_today(a["id"])
        log_supplement(
            a["id"],
            SupplementVerifyRequest(taken_today=True),
            calcium["id"],
            "manual-calcium",
        )
        assert CheckInRepository().has_supplement_logged_today(a["id"])
    assert counts(admin, a["id"]) == [2, 2, 2]


def test_http_appointment_default_contact_and_versioned_reschedule(db, monkeypatch):
    from fastapi.testclient import TestClient

    from app import dependencies
    from app.main import app

    _, a, _ = db
    monkeypatch.setattr(
        dependencies,
        "decode_access_token",
        lambda token: {
            "sub": a["id"],
            "email": a["email"],
            "session_id": str(uuid4()),
            "iat": utc_now().timestamp(),
        },
    )
    client = TestClient(app)
    headers = {
        "Authorization": "Bearer synthetic",
        "Idempotency-Key": "appointment-new",
    }
    created = client.post(
        "/users/me/appointment",
        headers=headers,
        json={"appointment_date": "2026-11-01"},
    )
    assert created.status_code == 200, created.text
    assert created.json()["anc_contact_number"] == 1 and created.json()["version"] == 0
    headers["Idempotency-Key"] = "appointment-move"
    moved = client.put(
        "/users/me/appointment",
        headers=headers,
        json={"appointment_date": "2026-11-03", "version": 0},
    )
    assert moved.status_code == 200, moved.text
    assert moved.json()["version"] == 1 and moved.json()["status"] == "scheduled"
    assert (
        client.put(
            "/users/me/appointment",
            headers=headers,
            json={"appointment_date": "2026-11-03", "version": 0},
        ).json()
        == moved.json()
    )
