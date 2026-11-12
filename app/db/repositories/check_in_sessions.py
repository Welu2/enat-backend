from copy import deepcopy
from datetime import timedelta
from uuid import uuid4

from psycopg import sql
from psycopg.types.json import Jsonb

from app.core.clock import utc_now
from app.core.errors import Conflict, NotFound
from app.db.data import get_data_client, normalize, transaction


class CheckInSessionRepository:
    def __init__(self, clock=utc_now):
        self.clock = clock

    def create(self, user_id, data):
        now = self.clock()
        draft_data = deepcopy(data.get("draft_data") or {})
        draft_data["_version"] = 0
        draft_data["_stage_status"] = data.get("stage_status", "awaiting_response")
        clean_data = {k: v for k, v in data.items() if k not in ("version", "stage_status")}
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "status": "in_progress",
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(hours=2)).isoformat(),
            **clean_data,
            "draft_data": draft_data,
        }
        row = (
            get_data_client()
            .table("check_in_sessions")
            .insert(payload)
            .execute()
            .data[0]
        )
        return {
            **row,
            "version": 0,
            "stage_status": data.get("stage_status", "awaiting_response"),
        }

    def get(self, session_id, user_id, *, lock=False):
        try:
            with transaction() as conn:
                query = "SELECT * FROM check_in_sessions WHERE id=%s AND user_id=%s"
                if lock:
                    query += " FOR UPDATE"
                row = normalize(conn.execute(query, (session_id, user_id)).fetchone())
                if row:
                    draft = row.get("draft_data") or {}
                    row["version"] = row.get("version") if row.get("version") is not None else draft.get("_version", 0)
                    row["stage_status"] = row.get("stage_status") or draft.get("_stage_status", "awaiting_response")
                return row
        except Exception:
            client = get_data_client()
            res = (
                client.table("check_in_sessions")
                .select("*")
                .eq("id", str(session_id))
                .eq("user_id", str(user_id))
                .maybe_single()
                .execute()
            )
            if not res or not res.data:
                return None
            row = normalize(res.data)
            draft = row.get("draft_data") or {}
            row["version"] = row.get("version") if row.get("version") is not None else draft.get("_version", 0)
            row["stage_status"] = row.get("stage_status") or draft.get("_stage_status", "awaiting_response")
            return row

    def update(self, session_id, user_id, data, *, expected_version):
        try:
            with transaction() as conn:
                assignments = sql.SQL(", ").join(
                    sql.SQL("{}=%s").format(sql.Identifier(k)) for k in data
                )
                values = [
                    Jsonb(v) if isinstance(v, (dict, list)) else v for v in data.values()
                ]
                row = conn.execute(
                    sql.SQL(
                        "UPDATE check_in_sessions SET {}, version=version+1 WHERE id=%s AND user_id=%s AND version=%s AND status='in_progress' AND expires_at>%s RETURNING *"
                    ).format(assignments),
                    [*values, session_id, user_id, expected_version, self.clock()],
                ).fetchone()
                if not row:
                    if not self.get(session_id, user_id):
                        raise NotFound("Session not found")
                    raise Conflict("Session changed or expired")
                return normalize(row)
        except (NotFound, Conflict):
            raise
        except Exception:
            client = get_data_client()
            now_iso = self.clock().isoformat()
            existing = self.get(session_id, user_id)
            if not existing:
                raise NotFound("Session not found")
            if existing.get("version", 0) != expected_version:
                raise Conflict("Session changed or expired")
            if existing.get("status") != "in_progress" or existing.get("expires_at", "") <= now_iso:
                raise Conflict("Session changed or expired")

            draft = deepcopy(data.get("draft_data") or existing.get("draft_data") or {})
            draft["_version"] = expected_version + 1
            stage_status = data.get("stage_status") or draft.get("_stage_status", "awaiting_response")
            draft["_stage_status"] = stage_status

            ALLOWED = {"current_stage", "stage_order", "draft_data", "pending_items", "status", "expires_at"}
            payload = {k: v for k, v in data.items() if k in ALLOWED}
            payload["draft_data"] = draft

            res = (
                client.table("check_in_sessions")
                .update(payload)
                .eq("id", str(session_id))
                .eq("user_id", str(user_id))
                .execute()
            )
            if not res or not res.data:
                raise Conflict("Session changed or expired")
            row = normalize(res.data[0])
            row["version"] = expected_version + 1
            row["stage_status"] = stage_status
            return row
