from uuid import UUID

from app.core.errors import Conflict
from app.db.data import normalize, transaction


class PushTokenRepository:
    def register(self, user_id: UUID, token: str, platform: str = "web") -> dict:
        # Uniqueness is global; a conflict never transfers another user's token.
        with transaction() as conn:
            row = conn.execute(
                """INSERT INTO push_tokens(user_id,token,platform) VALUES(%s,%s,%s)
            ON CONFLICT(token) DO UPDATE SET platform=excluded.platform,updated_at=now()
            WHERE push_tokens.user_id=excluded.user_id RETURNING *""",
                (user_id, token, platform),
            ).fetchone()
        if not row:
            raise Conflict("Device registration conflict")
        return normalize(row)

    def list_for_user(self, user_id: UUID) -> list[dict]:
        with transaction() as conn:
            return normalize(
                conn.execute(
                    "SELECT * FROM push_tokens WHERE user_id=%s", (user_id,)
                ).fetchall()
            )
