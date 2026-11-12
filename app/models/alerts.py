from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

AlertStatus = Literal["unacknowledged", "acknowledged"]


class CategoryLabel(BaseModel):
    category: str
    en: str
    am: str


class EmergencyAlert(BaseModel):
    id: UUID
    categories: list[str]
    category_labels: list[CategoryLabel]
    recorded_at: datetime
    received_at: datetime
    created_at: datetime
    status: AlertStatus
    acknowledged_at: datetime | None
