"""UTC persistence and the supported population's explicit calendar timezone."""

from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

LOCAL_ZONE = ZoneInfo("Africa/Addis_Ababa")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def as_utc(value: datetime | str) -> datetime:
    if not isinstance(value, datetime):
        value = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    # Legacy naive instants were written with utcnow().
    return (
        value.replace(tzinfo=timezone.utc)
        if value.tzinfo is None
        else value.astimezone(timezone.utc)
    )


def local_day_bounds(now: datetime | str) -> tuple[datetime, datetime]:
    start = datetime.combine(
        as_utc(now).astimezone(LOCAL_ZONE).date(), time.min, LOCAL_ZONE
    )
    return start.astimezone(timezone.utc), (start + timedelta(days=1)).astimezone(
        timezone.utc
    )
