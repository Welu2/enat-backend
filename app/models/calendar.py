from __future__ import annotations

import datetime as dt
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

CalendarItemType = Literal["event", "task"]


class CalendarItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    title_am: str | None = Field(default=None, max_length=200)
    type: CalendarItemType
    date: dt.date
    time: dt.time | None = None
    reminder_at: dt.datetime | None = None
    completed: bool = False


class CalendarItemUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=200)
    title_am: str | None = Field(default=None, max_length=200)
    type: CalendarItemType | None = None
    date: dt.date | None = None
    time: dt.time | None = None
    reminder_at: dt.datetime | None = None
    completed: bool | None = None


class CalendarItemResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    title_am: str | None = None
    type: CalendarItemType
    date: dt.date
    time: dt.time | None = None
    reminder_at: dt.datetime | None = None
    completed: bool
    created_at: dt.datetime
    updated_at: dt.datetime

