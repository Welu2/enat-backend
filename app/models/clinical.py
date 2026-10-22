"""Patient-editable clinical fields. Metadata is added exclusively by the server."""

from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    field_validator,
    model_validator,
)

from app.core.constants import DANGER_SIGN_CATEGORIES

Text = Annotated[str, Field(min_length=1, max_length=8000)]
Severity = Literal["mild", "moderate", "severe", "unspecified"]
FoodGroup = Literal["grains", "proteins", "dairy", "fruits_and_vegetables"]


class Editable(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    raw_text: Text


class Duration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: (
        Annotated[float, Field(ge=0, le=100000, allow_inf_nan=False, strict=True)]
        | None
    ) = None
    unit: Literal["minute", "hour", "day", "week", "month", "unspecified"] = (
        "unspecified"
    )

    @model_validator(mode="after")
    def coherent(self) -> Self:
        if (self.value is None) != (self.unit == "unspecified"):
            raise ValueError("Duration needs both a value and a unit")
        return self


class SymptomFields(Editable):
    category: str | None = None
    duration: Duration | None = None
    severity: Severity = "unspecified"

    @field_validator("category")
    @classmethod
    def category_allowed(cls, value: str | None) -> str | None:
        if value is not None and value not in DANGER_SIGN_CATEGORIES:
            raise ValueError("Unknown symptom category")
        return value


class FoodFields(Editable):
    food_groups: list[FoodGroup] = Field(default_factory=list, max_length=4)
    items: list[Text] = Field(default_factory=list, max_length=50)


class SupplementFields(Editable):
    supplement_name: Annotated[str, Field(min_length=1, max_length=200)] = "unknown"
    taken_today: StrictBool | None = None


class ClosingFields(Editable):
    topic: Literal[
        "dietary_intake",
        "supplement_taken",
        "therapeutic_food",
        "breastfeeding_intent",
        "other",
        "general_closing",
    ] = "other"


STAGE_FIELDS = {
    "symptoms": SymptomFields,
    "food": FoodFields,
    "supplement": SupplementFields,
    "closing": ClosingFields,
}
STAGE_KEYS = {
    "symptoms": "symptoms",
    "food": "food_log",
    "supplement": "supplement_check",
    "closing": "closing_mentions",
}


class SymptomCorrection(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    raw_text: Text | None = None
    category: str | None = None
    duration: Duration | None = None
    severity: Severity | None = None

    @field_validator("category")
    @classmethod
    def category_allowed(cls, value: str | None) -> str | None:
        return SymptomFields.category_allowed(value)


class FoodCorrection(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    raw_text: Text | None = None
    food_groups: list[FoodGroup] | None = Field(default=None, max_length=4)
    items: list[Text] | None = Field(default=None, max_length=50)


class SupplementCorrection(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    raw_text: Text | None = None
    supplement_name: Annotated[str, Field(min_length=1, max_length=200)] | None = None
    taken_today: StrictBool | None = None


class ClosingCorrection(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    raw_text: Text | None = None
    topic: (
        Literal[
            "dietary_intake",
            "supplement_taken",
            "therapeutic_food",
            "breastfeeding_intent",
            "other",
            "general_closing",
        ]
        | None
    ) = None
