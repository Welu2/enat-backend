import json
import re
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ValidationError

from app.core.constants import DANGER_SIGN_CATEGORIES, NUTRITION_TOPICS
from app.models.checkin import CheckInStage
from app.services.addis_ai import AddisAIClient
from app.services.danger_signs import check_danger_sign


class SymptomsExtraction(BaseModel):
    symptoms: list[dict[str, Any]]


class FoodExtraction(BaseModel):
    food_log: dict[str, Any] | None = None


class SupplementExtraction(BaseModel):
    supplement_check: dict[str, Any] | None = None


class ClosingExtraction(BaseModel):
    closing_mentions: list[dict[str, Any]]


STAGE_SCHEMAS: dict[CheckInStage, type[BaseModel]] = {
    "symptoms": SymptomsExtraction,
    "food": FoodExtraction,
    "supplement": SupplementExtraction,
    "closing": ClosingExtraction,
}

# Canonical danger-sign category values the LLM must choose from.
# Injected verbatim into every stage's system prompt so the model cannot
# hallucinate a non-existent category that would silently bypass the rules engine.
_CATEGORY_LIST = ", ".join(sorted(DANGER_SIGN_CATEGORIES))

# Human-readable display labels for the per-item verification read-back phrase.
_CATEGORY_DISPLAY: dict[str, str] = {
    "vaginal_bleeding": "vaginal bleeding",
    "swelling_hands_face": "swelling of hands or face",
    "blurred_vision": "blurred vision",
    "severe_abdominal_pain": "severe abdominal pain",
    "fluid_leakage": "fluid leakage",
    "severe_headache": "severe headache",
    "persistent_nausea_vomiting": "persistent nausea or vomiting",
    "high_fever": "high fever",
    "convulsions_loss_of_consciousness": "convulsions or loss of consciousness",
    "difficulty_breathing": "difficulty breathing",
    "severe_weakness_or_backache": "severe weakness or backache",
    "abnormal_fetal_movement": "abnormal fetal movement",
}

FEW_SHOT_PROMPTS: dict[CheckInStage, str] = {
    "symptoms": f"""\
Examples:

Input: "ሁለት ቀን ከባድ ራስ ምታት እያለኝ ነው"
Output: {{"symptoms":[{{"raw_text":"ሁለት ቀን ከባድ ራስ ምታት እያለኝ ነው","category":"severe_headache","duration":{{"value":2,"unit":"day"}},"severity":"severe"}}]}}

Input: "እግሮቼ ለሶስት ቀናት እያበጡ ነው እና ከባድ ራስ ምታት አለኝ"
Output: {{"symptoms":[
  {{"raw_text":"እግሮቼ ለሶስት ቀናት እያበጡ ነው","category":"swelling_hands_face","duration":{{"value":3,"unit":"day"}},"severity":"moderate"}},
  {{"raw_text":"ከባድ ራስ ምታት አለኝ","category":"severe_headache","duration":{{"value":null,"unit":"unspecified"}},"severity":"severe"}}
]}}

Input: "ምንም ምልክት የለም"
Output: {{"symptoms":[]}}
""",
    "food": """\
Examples:

Input: "ዛሬ ጤፍ እና ስንዴ በላሁ"
Output: {"food_log":{"raw_text":"ዛሬ ጤፍ እና ስንዴ በላሁ"}}

Input: "ምንም አልበልኩም"
Output: {"food_log":null}
""",
    "supplement": """\
Examples:

Input: "የብረት tablet ዛሬ ወስጄያለሁ"
Output: {"supplement_check":{"raw_text":"የብረት tablet ዛሬ ወስጄያለሁ","supplement_name":"iron","taken_today":true}}

Input: "ዛሬ አልወስድኩም"
Output: {"supplement_check":{"raw_text":"ዛሬ አልወስድኩም","supplement_name":"unknown","taken_today":false}}
""",
    "closing": """\
Examples:

Input: "በወራት ላይ ጡት መክተት እፈልጋለሁ"
Output: {"closing_mentions":[{"raw_text":"በወራት ላይ ጡት መክተት እፈልጋለሁ","topic":"breastfeeding_intent"}]}

Input: "ሌላ ነገር የለም"
Output: {"closing_mentions":[]}
""",
}

# Base system prompt shared across all stages.
_SYSTEM_PROMPT_BASE = (
    "You are a structured data extractor for a maternal health intake system in Ethiopia. "
    "Your ONLY job is to convert Amharic speech transcripts into the requested JSON schema — "
    "you must NEVER give medical advice, diagnosis, or any clinical opinion. "
    "Return ONLY valid JSON with no markdown fences, no explanation, no commentary outside the JSON. "
    "If nothing relevant is mentioned, return empty lists or null values rather than guessing. "
    "Preserve the raw_text field exactly as it appears in the transcript — do not translate or paraphrase. "
    "Never set the danger_sign field — that is computed deterministically by the rules engine, not by you. "
    "duration must be an object: {\"value\": <integer or null>, \"unit\": \"hour|day|week|month|unspecified\"}. "
    "This keeps duration language-neutral so it can be displayed in any language at render time — "
    "never return duration as a free-text string in English or Amharic. "
    "If no duration is mentioned, use {\"value\": null, \"unit\": \"unspecified\"}. "
    "severity must be exactly one of: mild, moderate, severe, unspecified. "
    f"For symptom category, you MUST use one of these exact values (or null for non-danger symptoms): "
    f"{_CATEGORY_LIST}."
)


def _build_system_prompt(stage: CheckInStage) -> str:
    topic_hint = ""
    if stage == "closing":
        topic_hint = f" Valid topic values: {', '.join(NUTRITION_TOPICS)}."

    return f"{_SYSTEM_PROMPT_BASE}{topic_hint}\n\n{FEW_SHOT_PROMPTS[stage]}"


def _parse_json_response(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)
    return json.loads(cleaned)


# Danger-sign category display labels per language. One entry per category,
# both languages together, so the 12-item list can never drift out of sync
# between languages (the old two-separate-dicts setup could silently lose
# a category from one language and not the other).
_CATEGORY_DISPLAY: dict[str, dict[str, str]] = {
    "vaginal_bleeding": {"am": "የማህፀን ደም መፍሰስ", "en": "vaginal bleeding"},
    "swelling_hands_face": {"am": "የእጅ ወይም የፊት እብጠት", "en": "swelling of hands or face"},
    "blurred_vision": {"am": "የእይታ ብዥታ", "en": "blurred vision"},
    "severe_abdominal_pain": {"am": "ከባድ የሆድ ህመም", "en": "severe abdominal pain"},
    "fluid_leakage": {"am": "የፈሳሽ መፍሰስ", "en": "fluid leakage"},
    "severe_headache": {"am": "ከባድ ራስ ምታት", "en": "severe headache"},
    "persistent_nausea_vomiting": {"am": "የማይቋረጥ ማስታወክ", "en": "persistent nausea or vomiting"},
    "high_fever": {"am": "ከፍተኛ ትኩሳት", "en": "high fever"},
    "convulsions_loss_of_consciousness": {"am": "መንቀጥቀጥ ወይም ራስን መሳት", "en": "convulsions or loss of consciousness"},
    "difficulty_breathing": {"am": "የመተንፈስ ችግር", "en": "difficulty breathing"},
    "severe_weakness_or_backache": {"am": "ከባድ ድካም ወይም የጀርባ ህመም", "en": "severe weakness or backache"},
    "abnormal_fetal_movement": {"am": "የፅንስ እንቅስቃሴ መለወጥ", "en": "abnormal fetal movement"},
}


def _category_display(category: str, lang: str = "am") -> str:
    """Look up a danger-sign category's display label in the given language.

    Used for both the patient-facing Amharic verification phrase and the
    clinician-facing summary (which may render in English) — one lookup
    table, two consumers, so the label sets can't diverge.
    """
    labels = _CATEGORY_DISPLAY.get(category)
    if not labels:
        return category.replace("_", " ") if category else "ምልክት" if lang == "am" else "symptom"
    return labels.get(lang, labels.get("am", category))

# Duration unit display labels per language. Add a new top-level key here
# (e.g. "om" for Afaan Oromo) to support another language without touching
# the extraction schema, prompts, or database — duration stays a
# language-neutral {value, unit} object everywhere upstream of this dict.
_DURATION_UNIT_DISPLAY: dict[str, dict[str, str]] = {
    "am": {
        "hour": "ሰዓት",
        "day": "ቀን",
        "week": "ሳምንት",
        "month": "ወር",
    },
    "en": {
        "hour": "hour(s)",
        "day": "day(s)",
        "week": "week(s)",
        "month": "month(s)",
    },
}


def _format_duration(duration: dict[str, Any] | str | None, lang: str = "am") -> str:
    """Render a duration object {value, unit} or string as display text.

    Returns "" when there's nothing to show (no duration mentioned), so
    callers can safely skip it rather than showing an empty/placeholder value.
    """
    if not duration:
        return ""
    if isinstance(duration, str):
        return duration
    unit = duration.get("unit")
    value = duration.get("value")
    if not unit or unit == "unspecified" or value is None:
        return ""
    unit_labels = _DURATION_UNIT_DISPLAY.get(lang, _DURATION_UNIT_DISPLAY["am"])
    unit_label = unit_labels.get(unit, unit)
    return f"{value} {unit_label}"


def build_verification_phrase(item: dict[str, Any], stage: CheckInStage) -> str:
    """Build the human-readable Amharic read-back string shown to the patient for confirmation.

    PRD §4 step 6: "App reads back each extracted item individually for
    confirmation ('swelling, 3 days — is that correct?')."
    """
    if stage == "symptoms":
        category = item.get("category") or ""
        display = _category_display(category, lang="am")
        duration_str = _format_duration(item.get("duration"), lang="am")
        parts: list[str] = [display]
        if duration_str:
            parts.append(duration_str)
        return f"{'፣ '.join(parts)} — ትክክል ነው?"

    if stage == "food":
        raw = item.get("raw_text") or ""
        return f"የበሉት: {raw} — ትክክል ነው?"

    if stage == "supplement":
        name = item.get("supplement_name") or "ተጨማሪ ምግብ"
        taken = "ዛሬ ወስደዋል" if item.get("taken_today") else "ዛሬ አልወሰዱም"
        return f"{name} {taken} — ትክክል ነው?"

    # closing
    raw = item.get("raw_text") or ""
    return f"የጠቀሱት: {raw} — ትክክል ነው?"


_build_verification_phrase = build_verification_phrase


def _attach_item_ids(stage: CheckInStage, data: dict[str, Any]) -> list[dict[str, Any]]:
    if stage == "symptoms":
        items = []
        for item in data.get("symptoms", []):
            item = dict(item)
            item["item_id"] = str(uuid4())
            item["confirmed"] = False
            item["danger_sign"] = check_danger_sign(item.get("category", ""))
            item["verification_phrase"] = _build_verification_phrase(item, stage)
            items.append(item)
        return items

    if stage == "food":
        food = data.get("food_log")
        if not food:
            return []
        item = dict(food)
        item["item_id"] = str(uuid4())
        item["confirmed"] = False
        item["verification_phrase"] = _build_verification_phrase(item, stage)
        return [item]

    if stage == "supplement":
        supplement = data.get("supplement_check")
        if not supplement:
            return []
        item = dict(supplement)
        item["item_id"] = str(uuid4())
        item["confirmed"] = False
        item["verification_phrase"] = _build_verification_phrase(item, stage)
        return [item]

    # closing
    items = []
    for mention in data.get("closing_mentions", []):
        item = dict(mention)
        item["item_id"] = str(uuid4())
        item["confirmed"] = False
        item["verification_phrase"] = _build_verification_phrase(item, stage)
        items.append(item)
    return items


class ExtractionService:
    def __init__(self) -> None:
        self.client = AddisAIClient()

    async def extract(self, transcript: str, stage: CheckInStage) -> list[dict[str, Any]]:
        schema = STAGE_SCHEMAS[stage]
        system_prompt = _build_system_prompt(stage)
        user_prompt = f"Stage: {stage}\nTranscript:\n{transcript}"

        last_error: Exception | None = None
        for _ in range(3):
            try:
                raw = await self.client.generate_json(system_prompt, user_prompt)
                parsed = _parse_json_response(raw)
                validated = schema.model_validate(parsed)
                return _attach_item_ids(stage, validated.model_dump())
            except (json.JSONDecodeError, ValidationError, ValueError) as exc:
                last_error = exc
                continue

        raise ValueError(f"Failed to extract valid JSON for stage {stage}") from last_error
