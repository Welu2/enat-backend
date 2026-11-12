"""Conservative, versioned normalization; clinical release review remains required."""

from uuid import uuid4

from pydantic import ValidationError

from app.core.clock import utc_now
from app.core.errors import InvalidMutation
from app.models.clinical import STAGE_FIELDS, STAGE_KEYS
from app.services.danger_signs import check_danger_sign
from app.services.nutrition import classify_ethiopian_food

POLICY_VERSION = "clinical-conservative-v1"
PROMPT_VERSION = "intake-v2"


def collection(value):
    if isinstance(value, dict):
        return [value]
    return value if isinstance(value, list) else []


def confirmed_items(value):
    return [
        i
        for i in collection(value)
        if isinstance(i, dict) and i.get("confirmed") is True
    ]


def danger(item):
    # Severity alone never clears a recognized danger category.
    return check_danger_sign(item.get("category"))


def normalize_item(
    stage, item, correction=None, *, source="manual", now=None, confirm=False
):
    schema = STAGE_FIELDS[stage]
    fields = {k: v for k, v in item.items() if k in schema.model_fields}
    if correction is not None:
        if set(correction) - set(schema.model_fields):
            raise InvalidMutation("Server-owned or unknown correction field")
        fields.update(correction)
    try:
        fields = schema.model_validate(fields).model_dump(mode="json")
    except ValidationError as exc:
        raise InvalidMutation("Invalid clinical fields") from exc
    item_id = item.get("item_id") or str(uuid4())
    result = {
        **fields,
        "item_id": item_id,
        "source_item_id": item.get("source_item_id") or item_id,
        "source": item.get("source") or source,
        "confirmed": confirm is True,
        "confirmed_at": (now or utc_now()).isoformat() if confirm is True else None,
        "policy_version": POLICY_VERSION,
        "prompt_version": item.get("prompt_version"),
        "model_version": item.get("model_version"),
    }
    if stage == "symptoms":
        result["danger_sign"] = danger(result)
        result["assessment"] = (
            "recognized_danger_category" if result["danger_sign"] else "unclassified"
        )
    elif stage == "food" and not fields["food_groups"]:
        result["food_groups"] = classify_ethiopian_food(fields["raw_text"])
    return result


def validated_draft(draft):
    result = {}
    for stage, key in STAGE_KEYS.items():
        result[key] = []
        for item in collection(draft.get(key)):
            if not isinstance(item, dict) or item.get("confirmed") is not True:
                raise InvalidMutation("Unconfirmed content cannot be persisted")
            normalized = normalize_item(stage, item, confirm=True)
            # Never manufacture legacy confirmation provenance.
            normalized["confirmed_at"] = item.get("confirmed_at")
            result[key].append(normalized)
    return result
