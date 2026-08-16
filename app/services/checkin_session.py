from datetime import datetime
from typing import Any
from uuid import UUID

from app.core.constants import CHECKIN_STAGES, STAGE_PROMPTS
from app.db.repositories.check_in_sessions import CheckInSessionRepository
from app.db.repositories.check_ins import CheckInRepository
from app.db.repositories.supplements import SupplementRepository
from app.models.checkin import CheckInStage
from app.services.addis_ai import AddisAIClient
from app.services.danger_signs import check_danger_sign
from app.services.extraction import ExtractionService, build_verification_phrase


def _empty_draft_data() -> dict[str, Any]:
    return {
        "symptoms": [],
        "food_log": None,
        "supplement_check": None,
        "closing_mentions": [],
    }


from datetime import timezone

def _parse_datetime(val: str | datetime) -> datetime:
    if isinstance(val, datetime):
        dt = val
    else:
        dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


class CheckInSessionService:
    def __init__(self) -> None:
        self.sessions = CheckInSessionRepository()
        self.check_ins = CheckInRepository()
        self.supplements = SupplementRepository()
        self.asr = AddisAIClient()
        self.extraction = ExtractionService()

    def _build_stage_order(self, user_id: UUID) -> list[CheckInStage]:
        stages: list[CheckInStage] = ["symptoms", "food"]
        if self.supplements.list_active(user_id) and not self.check_ins.has_supplement_logged_today(user_id):
            stages.append("supplement")
        stages.append("closing")
        return stages

    def start_session(self, user_id: UUID) -> dict[str, Any]:
        stage_order = self._build_stage_order(user_id)
        session = self.sessions.create(
            user_id,
            {
                "current_stage": stage_order[0],
                "stage_order": stage_order,
                "draft_data": _empty_draft_data(),
                "pending_items": [],
            },
        )
        return {
            "session_id": session["id"],
            "stage": stage_order[0],
            "question_prompt": STAGE_PROMPTS[stage_order[0]],
        }

    async def respond(
        self,
        user_id: UUID,
        session_id: UUID,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> dict[str, Any]:
        session = self._get_active_session(user_id, session_id)
        stage = session["current_stage"]
        transcript = await self.asr.transcribe(audio_bytes, filename, content_type)
        pending_items = await self.extraction.extract(transcript, stage)

        if stage == "supplement" and pending_items:
            active_supplements = self.supplements.list_active(user_id)
            for item in pending_items:
                raw_name = str(item.get("supplement_name") or "").lower().strip()
                if raw_name in ("unknown", "other", "none", "") and active_supplements:
                    item["supplement_name"] = active_supplements[0]["name"]
                    item["verification_phrase"] = build_verification_phrase(item, stage)

        self.sessions.update(
            session_id,
            user_id,
            {"pending_items": pending_items},
        )

        return {
            "session_id": session_id,
            "stage": stage,
            "transcript": transcript,
            "pending_items": pending_items,
        }

    def verify_item(
        self,
        user_id: UUID,
        session_id: UUID,
        item_id: str | None = None,
        confirmed: bool = True,
        corrected_value: dict[str, Any] | None = None,
        items_payload: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        session = self._get_active_session(user_id, session_id)
        pending_items = list(session.get("pending_items") or [])
        draft_data = dict(session.get("draft_data") or _empty_draft_data())
        stage = session["current_stage"]

        verifications: list[dict[str, Any]] = []
        if items_payload:
            verifications = items_payload
        elif item_id:
            verifications = [{"item_id": item_id, "confirmed": confirmed, "corrected_value": corrected_value}]
        elif corrected_value:
            verifications = [{"item_id": str(uuid4()), "confirmed": confirmed, "corrected_value": corrected_value}]

        updated_pending: list[dict[str, Any]] = list(pending_items)
        confirmed_count = 0

        for verif in verifications:
            v_item_id = verif.get("item_id")
            v_confirmed = verif.get("confirmed", True)
            v_corrected = verif.get("corrected_value")

            target_id = v_item_id
            matching = [i for i in updated_pending if i.get("item_id") == v_item_id]
            if not matching and len(updated_pending) == 1 and v_item_id:
                target_id = updated_pending[0].get("item_id")

            matched_item = None
            for idx, item in enumerate(updated_pending):
                if item.get("item_id") == target_id:
                    matched_item = dict(item)
                    updated_pending.pop(idx)
                    break

            if not matched_item and v_corrected:
                matched_item = {
                    "item_id": target_id or str(uuid4()),
                    "raw_text": v_corrected.get("raw_text", ""),
                }

            if matched_item:
                if v_corrected:
                    matched_item.update(v_corrected)
                    if stage == "symptoms":
                        severity = str(matched_item.get("severity") or "").lower()
                        if severity == "mild":
                            matched_item["category"] = None
                            matched_item["danger_sign"] = False
                        else:
                            matched_item["danger_sign"] = check_danger_sign(matched_item.get("category"))
                    if "verification_phrase" not in v_corrected:
                        matched_item["verification_phrase"] = build_verification_phrase(matched_item, stage)

                matched_item["confirmed"] = v_confirmed
                if v_confirmed:
                    confirmed_count += 1
                    self._store_confirmed_item(draft_data, stage, matched_item)
                else:
                    updated_pending.append(matched_item)

        self.sessions.update(
            session_id,
            user_id,
            {"pending_items": updated_pending, "draft_data": draft_data},
        )

        return {
            "session_id": session_id,
            "stage": stage,
            "pending_items": updated_pending,
            "confirmed_count": confirmed_count,
        }

    async def voice_correct_item(
        self,
        user_id: UUID,
        session_id: UUID,
        item_id: str,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> dict[str, Any]:
        """Record voice again specifically to correct a single pending item."""
        session = self._get_active_session(user_id, session_id)
        stage = session["current_stage"]
        pending_items = list(session.get("pending_items") or [])

        # Support fallback when user passes session_id instead of item_id on single-item stages
        target_item_id = item_id
        matching_items = [i for i in pending_items if i.get("item_id") == item_id]
        if not matching_items and len(pending_items) == 1:
            target_item_id = pending_items[0].get("item_id", item_id)

        correction_transcript = await self.asr.transcribe(audio_bytes, filename, content_type)
        extracted_corrections = await self.extraction.extract(correction_transcript, stage)

        item_updated = False
        if extracted_corrections:
            new_data = extracted_corrections[0]
            for item in pending_items:
                if item.get("item_id") == target_item_id:
                    for field in ("category", "duration", "severity", "raw_text", "supplement_name", "taken_today", "topic"):
                        if field in new_data and new_data[field] is not None:
                            item[field] = new_data[field]
                    if stage == "symptoms":
                        severity = str(item.get("severity") or "").lower()
                        if severity == "mild":
                            item["category"] = None
                            item["danger_sign"] = False
                        else:
                            item["danger_sign"] = check_danger_sign(item.get("category"))
                    item["verification_phrase"] = build_verification_phrase(item, stage)
                    item["correction_transcript"] = correction_transcript
                    item_updated = True
                    break

        self.sessions.update(
            session_id,
            user_id,
            {"pending_items": pending_items},
        )

        return {
            "session_id": session_id,
            "stage": stage,
            "correction_transcript": correction_transcript,
            "item_updated": item_updated,
            "pending_items": pending_items,
        }

    def complete_stage(self, user_id: UUID, session_id: UUID) -> dict[str, Any]:
        session = self._get_active_session(user_id, session_id)
        stage_order: list[str] = session["stage_order"]
        current_stage = session["current_stage"]
        pending_items = session.get("pending_items") or []

        if pending_items:
            raise ValueError("All pending items must be verified before completing the stage")

        current_index = stage_order.index(current_stage)
        is_last_stage = current_index == len(stage_order) - 1

        if is_last_stage:
            draft_data = session.get("draft_data") or _empty_draft_data()
            danger_sign_triggered = any(
                item.get("confirmed") and item.get("danger_sign")
                for item in draft_data.get("symptoms", [])
            )
            check_in = self.check_ins.create(
                user_id,
                {
                    "symptoms": draft_data.get("symptoms"),
                    "food_log": draft_data.get("food_log"),
                    "supplement_check": draft_data.get("supplement_check"),
                    "closing_mentions": draft_data.get("closing_mentions"),
                    "danger_sign_triggered": danger_sign_triggered,
                },
            )
            self.sessions.update(
                session_id,
                user_id,
                {"status": "completed"},
            )
            return {
                "session_id": session_id,
                "stage_completed": current_stage,
                "danger_sign_triggered": danger_sign_triggered,
                "next_stage": None,
                "question_prompt": None,
                "session_completed": True,
                "check_in_id": check_in["id"],
            }

        next_stage = stage_order[current_index + 1]
        self.sessions.update(
            session_id,
            user_id,
            {"current_stage": next_stage, "pending_items": []},
        )
        return {
            "session_id": session_id,
            "stage_completed": current_stage,
            "danger_sign_triggered": False,
            "next_stage": next_stage,
            "question_prompt": STAGE_PROMPTS[next_stage],
            "session_completed": False,
            "check_in_id": None,
        }

    def _get_active_session(self, user_id: UUID, session_id: UUID) -> dict[str, Any]:
        session = self.sessions.get(session_id, user_id)
        if not session:
            raise ValueError("Session not found")
        if session.get("status") != "in_progress":
            raise ValueError("Session is not active")
        expires_at = session.get("expires_at")
        if expires_at and _parse_datetime(expires_at) < datetime.utcnow():
            raise ValueError("Session has expired")
        return session

    @staticmethod
    def _store_confirmed_item(
        draft_data: dict[str, Any],
        stage: CheckInStage,
        item: dict[str, Any],
    ) -> None:
        if stage == "symptoms":
            if item.get("category"):
                item["danger_sign"] = check_danger_sign(item["category"])
            draft_data.setdefault("symptoms", []).append(item)
        elif stage == "food":
            draft_data["food_log"] = item
        elif stage == "supplement":
            draft_data["supplement_check"] = item
        elif stage == "closing":
            draft_data.setdefault("closing_mentions", []).append(item)
