import hashlib
from copy import deepcopy
from uuid import uuid4

from starlette.concurrency import run_in_threadpool

from app.core.clock import as_utc, utc_now
from app.core.constants import STAGE_PROMPTS
from app.core.errors import Conflict, InvalidMutation, NotFound
from app.db import idempotency
from app.db.repositories.check_in_sessions import CheckInSessionRepository
from app.db.repositories.check_ins import CheckInRepository
from app.db.repositories.supplements import SupplementRepository
from app.models.clinical import STAGE_FIELDS, STAGE_KEYS
from app.services.addis_ai import AddisAIClient
from app.services.anc_schedule import generate_checkin_summary_text
from app.services.clinical_policy import (
    collection,
    danger,
    normalize_item,
    validated_draft,
)
from app.services.extraction import ExtractionService, build_verification_phrase
from app.services.provider_runtime import operation as provider_operation


def _empty_draft_data():
    return {key: [] for key in STAGE_KEYS.values()}


def _audio_url(stage):
    # Stable generic asset endpoint: no external calls inside a transaction.
    return f"/checkin/prompts/{stage}/audio"


class CheckInSessionService:
    def __init__(self, clock=utc_now):
        self.clock = clock
        self.sessions = CheckInSessionRepository(clock)
        self.check_ins = CheckInRepository(clock)
        self.supplements = SupplementRepository(clock)
        self.asr = AddisAIClient()
        self.extraction = ExtractionService()

    def _build_stage_order(self, user_id):
        stages = ["symptoms"]
        if not self.check_ins.has_food_logged_today(user_id):
            stages.append("food")
        if self.supplements.list_active(
            user_id
        ) and not self.check_ins.has_supplement_logged_today(user_id):
            stages.append("supplement")
        return stages + ["closing"]

    def start_session(self, user_id, *, key=None):
        def action():
            stages = self._build_stage_order(user_id)
            session = self.sessions.create(
                user_id,
                {
                    "current_stage": stages[0],
                    "stage_order": stages,
                    "draft_data": _empty_draft_data(),
                    "pending_items": [],
                },
            )
            return {
                "session_id": session["id"],
                "stage": stages[0],
                "version": session["version"],
                "stage_status": session["stage_status"],
                "question_prompt": STAGE_PROMPTS[stages[0]],
                "question_audio_url": _audio_url(stages[0]),
            }

        return idempotency.execute(user_id, "checkin:start", key, {}, action)

    def get_state(self, user_id, session_id):
        session = self.sessions.get(session_id, user_id)
        if not session:
            raise NotFound("Session not found")
        return session

    def _get_active_session(self, user_id, session_id, expected_version, *, lock=False):
        session = (
            self.get_state(user_id, session_id)
            if not lock
            else self.sessions.get(session_id, user_id, lock=True)
        )
        if not session:
            raise NotFound("Session not found")
        if session["version"] != expected_version or session["status"] != "in_progress":
            raise Conflict("Session changed")
        if as_utc(session["expires_at"]) <= self.clock():
            raise Conflict("Session expired")
        return session

    async def respond(
        self,
        user_id,
        session_id,
        audio_bytes,
        filename,
        content_type,
        *,
        expected_version,
        key=None,
    ):
        operation = f"checkin:{session_id}:respond"
        payload = {
            "version": expected_version,
            "audio": hashlib.sha256(audio_bytes).hexdigest(),
            "content_type": content_type,
        }
        previous = await run_in_threadpool(
            idempotency.lookup, user_id, operation, key, payload
        )
        if previous is not None:
            return previous
        session = await run_in_threadpool(
            self._get_active_session, user_id, session_id, expected_version
        )
        if session.get("pending_items"):
            raise InvalidMutation("Verify or correct existing items first")
        stage = session["current_stage"]
        async with provider_operation():
            transcript = await self.asr.transcribe(audio_bytes, filename, content_type)
            pending = await self.extraction.extract(transcript, stage)

        # Provider failure never changes state; saving compares the version read above.
        def action():
            updated = self.sessions.update(
                session_id,
                user_id,
                {
                    "pending_items": pending,
                    "stage_status": "awaiting_confirmation" if pending else "ready",
                },
                expected_version=expected_version,
            )
            return {
                "session_id": session_id,
                "version": updated["version"],
                "stage_status": updated["stage_status"],
                "stage": stage,
                "transcript": transcript,
                "pending_items": pending,
            }

        return await run_in_threadpool(
            idempotency.execute, user_id, operation, key, payload, action
        )

    def verify_item(
        self,
        user_id,
        session_id,
        item_id=None,
        confirmed=True,
        corrected_value=None,
        items_payload=None,
        *,
        expected_version,
        key=None,
        action="verify",
    ):
        entries = (
            items_payload
            if items_payload is not None
            else [
                {
                    "item_id": item_id,
                    "confirmed": confirmed,
                    "corrected_value": corrected_value,
                    "action": action,
                }
            ]
        )
        payload = {"version": expected_version, "items": entries}

        def mutate():
            session = self._get_active_session(user_id, session_id, expected_version)
            pending = deepcopy(session.get("pending_items") or [])
            draft = deepcopy(session.get("draft_data") or _empty_draft_data())
            stage = session["current_stage"]
            seen = set()
            count = 0
            if not entries or len(entries) > 50:
                raise InvalidMutation("Expected 1 to 50 verification items")
            for entry in entries:
                entry_action = entry.get("action", "verify")
                target = entry.get("item_id")
                if type(entry.get("confirmed", True)) is not bool:
                    raise InvalidMutation("Confirmation must be boolean")
                if entry_action == "add":
                    if target is not None or not entry.get("corrected_value"):
                        raise InvalidMutation(
                            "Manual addition needs fields and no item ID"
                        )
                    item = {"item_id": str(uuid4())}
                else:
                    if not target or target in seen:
                        raise InvalidMutation("Missing or duplicate item ID")
                    seen.add(target)
                    item = next((i for i in pending if i["item_id"] == target), None)
                    if item is None:
                        raise InvalidMutation("Unknown item ID")
                    pending.remove(item)
                    if entry_action == "discard":
                        continue
                    if entry_action != "verify":
                        raise InvalidMutation("Unknown verification operation")
                item = normalize_item(
                    stage,
                    item,
                    entry.get("corrected_value"),
                    now=self.clock(),
                    confirm=entry.get("confirmed", True),
                )
                item["verification_phrase"] = build_verification_phrase(item, stage)
                item["verification_audio_url"] = None
                if item["confirmed"] is True:
                    values = collection(draft.get(STAGE_KEYS[stage]))
                    if len(values) >= 100:
                        raise InvalidMutation("Stage item limit reached")
                    draft[STAGE_KEYS[stage]] = values + [item]
                    count += 1
                else:
                    pending.append(item)
            if len(pending) + len(collection(draft.get(STAGE_KEYS[stage]))) > 100:
                raise InvalidMutation("Stage item limit reached")
            updated = self.sessions.update(
                session_id,
                user_id,
                {
                    "pending_items": pending,
                    "draft_data": draft,
                    "stage_status": "awaiting_confirmation" if pending else "ready",
                },
                expected_version=expected_version,
            )
            return {
                "session_id": session_id,
                "version": updated["version"],
                "stage_status": updated["stage_status"],
                "stage": stage,
                "pending_items": pending,
                "confirmed_count": count,
                "danger_sign_triggered": any(
                    danger(i)
                    for i in draft.get("symptoms", [])
                    if i.get("confirmed") is True
                ),
            }

        return idempotency.execute(
            user_id, f"checkin:{session_id}:verify", key, payload, mutate
        )

    async def voice_correct_item(
        self,
        user_id,
        session_id,
        item_id,
        audio_bytes,
        filename,
        content_type,
        *,
        expected_version,
        key=None,
    ):
        operation = f"checkin:{session_id}:voice-correct"
        payload = {
            "version": expected_version,
            "item_id": item_id,
            "audio": hashlib.sha256(audio_bytes).hexdigest(),
            "content_type": content_type,
        }
        previous = await run_in_threadpool(
            idempotency.lookup, user_id, operation, key, payload
        )
        if previous is not None:
            return previous
        session = await run_in_threadpool(
            self._get_active_session, user_id, session_id, expected_version
        )
        stage = session["current_stage"]
        pending = deepcopy(session.get("pending_items") or [])
        index = next(
            (n for n, i in enumerate(pending) if i["item_id"] == item_id), None
        )
        if index is None:
            raise InvalidMutation("Unknown item ID")
        async with provider_operation():
            transcript = await self.asr.transcribe(audio_bytes, filename, content_type)
            corrections = await self.extraction.extract(transcript, stage)
        if len(corrections) != 1:
            raise InvalidMutation(
                "A correction must identify exactly one item; use manual editing"
            )
        fields = {
            k: v
            for k, v in corrections[0].items()
            if k in STAGE_FIELDS[stage].model_fields
        }
        item = normalize_item(stage, pending[index], fields, now=self.clock())
        item["source"] = "voice_correction"
        item["prompt_version"] = corrections[0].get("prompt_version")
        item["model_version"] = corrections[0].get("model_version")
        item["verification_phrase"] = build_verification_phrase(item, stage)
        item["verification_audio_url"] = None
        pending[index] = item

        def mutate():
            updated = self.sessions.update(
                session_id,
                user_id,
                {"pending_items": pending, "stage_status": "awaiting_confirmation"},
                expected_version=expected_version,
            )
            return {
                "session_id": session_id,
                "version": updated["version"],
                "stage_status": updated["stage_status"],
                "stage": stage,
                "correction_transcript": transcript,
                "item_updated": True,
                "pending_items": pending,
            }

        return await run_in_threadpool(
            idempotency.execute, user_id, operation, key, payload, mutate
        )

    def complete_stage(
        self, user_id, session_id, *, expected_version, key=None, skip=False
    ):
        def mutate():
            # Independent session lock/uniqueness protects retries even without a key.
            session = self.sessions.get(session_id, user_id, lock=True)
            if not session:
                raise NotFound("Session not found")
            if session["status"] == "completed" and session.get("terminal_result"):
                return session["terminal_result"]
            if (
                session["version"] != expected_version
                or session["status"] != "in_progress"
                or as_utc(session["expires_at"]) <= self.clock()
            ):
                raise Conflict("Session changed or expired")
            if session.get("pending_items") or (
                session["stage_status"] != "ready" and not skip
            ):
                raise InvalidMutation(
                    "Confirm pending items or explicitly skip an unanswered stage"
                )
            if skip and session["stage_status"] != "awaiting_response":
                raise InvalidMutation("Only an unanswered stage can be skipped")
            stages = session["stage_order"]
            stage = session["current_stage"]
            index = stages.index(stage)
            completed = {
                **session.get("completed_stages", {}),
                stage: "skipped" if skip else "completed",
            }
            draft = validated_draft(session["draft_data"])
            summary = generate_checkin_summary_text(draft["symptoms"])
            result = {
                "session_id": session_id,
                "version": expected_version + 1,
                "stage_completed": stage,
                **summary,
                "next_stage": None,
                "question_prompt": None,
                "question_audio_url": None,
                "session_completed": index == len(stages) - 1,
                "check_in_id": None,
            }
            update = {"completed_stages": completed, "pending_items": []}
            if result["session_completed"]:
                record = self.check_ins.create(
                    user_id, {**draft, **summary, "session_id": str(session_id)}
                )
                result["check_in_id"] = record["id"]
                result["stage_status"] = "completed"
                update.update(
                    status="completed",
                    stage_status="completed",
                    terminal_result=idempotency.normalize(result),
                )
                idempotency.emit(
                    user_id,
                    "checkin.completed",
                    record["id"],
                    {"session_id": str(session_id)},
                )
            else:
                next_stage = stages[index + 1]
                result.update(
                    next_stage=next_stage,
                    stage_status="awaiting_response",
                    question_prompt=STAGE_PROMPTS[next_stage],
                    question_audio_url=_audio_url(next_stage),
                )
                update.update(
                    current_stage=next_stage, stage_status="awaiting_response"
                )
            self.sessions.update(
                session_id, user_id, update, expected_version=expected_version
            )
            return result

        return idempotency.execute(
            user_id,
            f"checkin:{session_id}:complete",
            key,
            {"version": expected_version, "skip": skip},
            mutate,
        )
