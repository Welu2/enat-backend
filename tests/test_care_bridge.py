from unittest.mock import MagicMock

import pytest

from deploy import care_bridge_readiness as bridge


@pytest.mark.parametrize(
    "extra,statuses,expected",
    [
        ((), (), True),
        (("011_care_portal.sql",), ("running",), True),
        (("011_care_portal.sql",), ("failed",), True),
        (bridge.ADDITIVE_MIGRATIONS, ("applied", "running"), True),
        (bridge.ADDITIVE_MIGRATIONS, ("applied", "failed"), True),
        (bridge.ADDITIVE_MIGRATIONS, ("applied", "applied"), True),
        (bridge.ADDITIVE_MIGRATIONS, ("failed", "applied"), False),
        (("012_offline_checkins.sql",), ("applied",), False),
        (("013_unknown.sql",), ("applied",), False),
    ],
)
def test_bridge_accepts_only_ordered_reviewed_schema_attempts(
    monkeypatch, extra, statuses, expected
):
    rows = [{"name": n, "status": "applied"} for n in bridge.BASE_MIGRATIONS]
    rows += [{"name": n, "status": s} for n, s in zip(extra, statuses, strict=True)]
    pool = MagicMock()
    conn = pool.connection.return_value.__enter__.return_value
    conn.execute.return_value.fetchall.return_value = rows
    monkeypatch.setattr(bridge, "get_pool", lambda: pool)
    assert bridge.database_ready() is expected
    rows[0]["status"] = "failed"
    assert not bridge.database_ready()
