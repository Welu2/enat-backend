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
        payload = {
            "id": str(uuid4()),
            "user_id": str(user_id),
            "status": "in_progress",
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(hours=2)).isoformat(),
            **data,
        }
        return (
            get_data_client()
            .table("check_in_sessions")
            .insert(payload)
            .execute()
            .data[0]
        )

    def get(self, session_id, user_id, *, lock=False):
        with transaction() as conn:
            query = "SELECT * FROM check_in_sessions WHERE id=%s AND user_id=%s"
            if lock:
                query += " FOR UPDATE"
            return normalize(conn.execute(query, (session_id, user_id)).fetchone())

    def update(self, session_id, user_id, data, *, expected_version):
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
