import json
import re
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ValidationError

from app.core.constants import DANGER_SIGN_CATEGORIES, NUTRITION_TOPICS
from app.models.checkin import CheckInStage
from app.services.addis_ai import AddisAIClient
from app.services.danger_signs import check_danger_sign
from app.services.gemini import GeminiTranscribeClient
from app.services.nutrition import classify_ethiopian_food


class SymptomItem(BaseModel):
    raw_text: str
    category: str | None = None
    duration: dict[str, Any] | None = None
    severity: str = "unspecified"


class FoodItem(BaseModel):
    raw_text: str


class SupplementItem(BaseModel):
    raw_text: str
    supplement_name: str = "unknown"
    taken_today: bool = False


class ClosingItem(BaseModel):
    raw_text: str
    topic: str = "general_closing"


# Stage to per-item Pydantic schema mapping
STAGE_SCHEMAS: dict[CheckInStage, type[BaseModel]] = {
    "symptoms": SymptomItem,
    "food": FoodItem,
    "supplement": SupplementItem,
    "closing": ClosingItem,
}

# Canonical danger-sign category values the LLM must choose from.
_CATEGORY_LIST = ", ".join(sorted(DANGER_SIGN_CATEGORIES))

# Explicit JSON tool definitions per check-in stage
# NOTE: danger_sign is strictly omitted from tool schemas — it is computed in Python via check_danger_sign()
STAGE_TOOLS: dict[CheckInStage, dict[str, Any]] = {
    "symptoms": {
        "type": "function",
        "function": {
            "name": "log_symptom",
            "description": "Log an extracted maternal symptom. Call this tool once for each distinct symptom reported by the patient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "raw_text": {
                        "type": "string",
                        "description": "The exact patient words describing the symptom, preserved without translation or paraphrasing.",
                    },
                    "category": {
                        "type": ["string", "null"],
                        "enum": [*sorted(DANGER_SIGN_CATEGORIES), None],
                        "description": (
                            "One of the 12 danger sign categories if the patient reports a severe, persistent, "
                            "or alarming danger sign, or null if this is a mild, non-danger, or general pregnancy symptom."
                        ),
                    },
                    "duration": {
                        "type": "object",
                        "description": "Duration of the symptom.",
                        "properties": {
                            "value": {
                                "type": ["integer", "null"],
                                "description": "Numeric duration value or null if unspecified.",
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["hour", "day", "week", "month", "unspecified"],
                                "description": "Time unit for the duration.",
                            },
                        },
                        "required": ["unit"],
                        "additionalProperties": False,
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["mild", "moderate", "severe", "unspecified"],
                        "description": "Symptom severity level.",
                    },
                },
                "required": ["raw_text"],
                "additionalProperties": False,
            },
        },
    },
    "food": {
        "type": "function",
        "function": {
            "name": "log_food_entry",
            "description": "Log an extracted food or beverage item consumed by the patient. Call this tool once per distinct food item or combination.",
            "parameters": {
                "type": "object",
                "properties": {
                    "raw_text": {
                        "type": "string",
                        "description": "The exact patient words describing the food or drink consumed.",
                    },
                },
                "required": ["raw_text"],
                "additionalProperties": False,
            },
        },
    },
    "supplement": {
        "type": "function",
        "function": {
            "name": "log_supplement_check",
            "description": "Log whether the patient took their prescribed daily prenatal supplements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "raw_text": {
                        "type": "string",
                        "description": "The exact patient words regarding supplement intake.",
                    },
                    "supplement_name": {
                        "type": "string",
                        "description": "Name of the supplement (e.g. iron, folic_acid, calcium, multivitamin, or unknown).",
                    },
                    "taken_today": {
                        "type": "boolean",
                        "description": "True if the patient took the supplement today, False if not taken or skipped.",
                    },
                },
                "required": ["raw_text", "supplement_name", "taken_today"],
                "additionalProperties": False,
            },
        },
    },
    "closing": {
        "type": "function",
        "function": {
            "name": "log_closing_mention",
            "description": "Log a question, concern, or general closing remark from the patient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "raw_text": {
                        "type": "string",
                        "description": "The exact patient words describing questions, concerns, or closing statement.",
                    },
                    "topic": {
                        "type": "string",
                        "enum": [*NUTRITION_TOPICS, "general_closing"],
                        "description": "Topic category of the question/statement or general_closing.",
                    },
                },
                "required": ["raw_text"],
                "additionalProperties": False,
            },
        },
    },
}

FEW_SHOT_PROMPTS: dict[CheckInStage, str] = {
    "symptoms": """\
Examples:

Input: "ሁለት ቀን ከባድ ራስ ምታት እያለኝ ነው"
Tool Call: log_symptom(raw_text="ሁለት ቀን ከባድ ራስ ምታት እያለኝ ነው", category="severe_headache", duration={"value":2,"unit":"day"}, severity="severe")

Input: "ቀላል የድካም ስሜት እና የጀርባ ህመም አለኝ"
Tool Call: log_symptom(raw_text="ቀላል የድካም ስሜት እና የጀርባ ህመም አለኝ", category=null, duration={"value":null,"unit":"unspecified"}, severity="mild")

Input: "ማቅለሽለሽ ማስታወክ እና ትኩሳት አለብኝ"
Tool Calls:
log_symptom(raw_text="ማቅለሽለሽ እና ማስታወክ", category="persistent_nausea_vomiting", duration={"value":null,"unit":"unspecified"}, severity="unspecified")
log_symptom(raw_text="ትኩሳት", category="high_fever", duration={"value":null,"unit":"unspecified"}, severity="unspecified")

Input: "እግሮቼ ለሶስት ቀናት እያበጡ ነው እና ከባድ ራስ ምታት አለኝ"
Tool Calls:
log_symptom(raw_text="ከባድ ራስ ምታት አለኝ", category="severe_headache", duration={"value":null,"unit":"unspecified"}, severity="severe")

Input: "Severe headache አለብኝ"
Tool Call: log_symptom(raw_text="Severe headache አለብኝ", category="severe_headache", duration={"value":null,"unit":"unspecified"}, severity="severe")

Input: "ትንሽ dizziness ይሰማኛል ግን ደህና ነኝ"
Tool Call: log_symptom(raw_text="ትንሽ dizziness ይሰማኛል ግን ደህና ነኝ", category=null, duration={"value":null,"unit":"unspecified"}, severity="mild")

Input: "I have had a severe headache and high fever for 2 days"
Tool Calls:
log_symptom(raw_text="severe headache", category="severe_headache", duration={"value":2,"unit":"day"}, severity="severe")
log_symptom(raw_text="high fever", category="high_fever", duration={"value":2,"unit":"day"}, severity="severe")

Input: "I feel completely fine, no symptoms today"
Tool Call: log_symptom(raw_text="I feel completely fine, no symptoms today", category=null, duration={"value":null,"unit":"unspecified"}, severity="unspecified")
""",
    "food": """\
Examples:

Input: "ዛሬ ጤፍ እና ስንዴ በላሁ"
Tool Call: log_food_entry(raw_text="ዛሬ ጤፍ እና ስንዴ በላሁ")

Input: "ዛሬ ጤፍ፣ ስንዴ እና ወተት ጠጣሁ"
Tool Calls:
log_food_entry(raw_text="ጤፍ እና ስንዴ")
log_food_entry(raw_text="ወተት")

Input: "ዛሬ bread እና ሻይ ጠጣሁ"
Tool Call: log_food_entry(raw_text="ዛሬ bread እና ሻይ ጠጣሁ")

Input: "ምንም አልበላሁም"
Tool Call: log_food_entry(raw_text="ምንም አልበላሁም")

Input: "Today I ate eggs, bread and drank milk"
Tool Calls:
log_food_entry(raw_text="eggs and bread")
log_food_entry(raw_text="milk")

Input: "I haven't eaten anything today"
Tool Call: log_food_entry(raw_text="I haven't eaten anything today")
""",
    "supplement": """\
Examples:

Input: "የብረት tablet ዛሬ ወስጄያለሁ"
Tool Call: log_supplement_check(raw_text="የብረት tablet ዛሬ ወስጄያለሁ", supplement_name="iron", taken_today=true)

Input: "ዛሬ አልወስድኩም"
Tool Call: log_supplement_check(raw_text="ዛሬ አልወስድኩም", supplement_name="unknown", taken_today=false)

Input: "አይ ምንም አልወሰድኩም"
Tool Call: log_supplement_check(raw_text="አይ ምንም አልወሰድኩም", supplement_name="unknown", taken_today=false)

Input: "Yes, I took my iron tablet today"
Tool Call: log_supplement_check(raw_text="iron tablet", supplement_name="iron", taken_today=true)

Input: "No, I missed my supplement today"
Tool Call: log_supplement_check(raw_text="missed my supplement today", supplement_name="unknown", taken_today=false)
""",
    "closing": """\
Examples:

Input: "በወራት ላይ ጡት መክተት እፈልጋለሁ"
Tool Call: log_closing_mention(raw_text="በወራት ላይ ጡት መክተት እፈልጋለሁ", topic="breastfeeding_intent")

Input: "በወራት ላይ ጡት መክተት እፈልጋለሁ እና ስለ አመጋገብ ማወቅ እፈልጋለሁ"
Tool Calls:
log_closing_mention(raw_text="በወራት ላይ ጡት መክተት እፈልጋለሁ", topic="breastfeeding_intent")
log_closing_mention(raw_text="ስለ አመጋገብ ማወቅ እፈልጋለሁ", topic="dietary_intake")

Input: "ስለ ultrasound appointment ማወቅ እፈልጋለሁ"
Tool Call: log_closing_mention(raw_text="ስለ ultrasound appointment ማወቅ እፈልጋለሁ", topic="general_closing")

Input: "ምንም ጥያቄ የለኝም"
Tool Call: log_closing_mention(raw_text="ምንም ጥያቄ የለኝም", topic="general_closing")

Input: "ሌላ ነገር የለም"
Tool Call: log_closing_mention(raw_text="ሌላ ነገር የለም", topic="general_closing")

Input: "When should I come for my next ultrasound check?"
Tool Call: log_closing_mention(raw_text="When should I come for my next ultrasound check?", topic="general_closing")

Input: "I have no other questions, thank you"
Tool Call: log_closing_mention(raw_text="I have no other questions, thank you", topic="general_closing")
""",
}

# Base system prompt shared across all stages.
_SYSTEM_PROMPT_BASE = (
    "You are a structured clinical data extractor for a maternal health intake system. "
    "Your ONLY job is to extract structured items from patient speech transcripts (which may be in Amharic, English, or mixed code-switching) by invoking the provided tools. "
    "You must NEVER give medical advice, diagnosis, or any clinical opinion. "
    "CRITICAL MULTI-ITEM MANDATE: If the transcript contains multiple distinct symptoms, multiple food items, "
    "or multiple questions/topics, YOU MUST CALL THE RELEVANT TOOL SEPARATELY FOR EVERY SINGLE ITEM! "
    "For example, if the transcript mentions nausea, vomiting, AND fever, call log_symptom for 'nausea and vomiting' "
    "AND call log_symptom for 'fever'. NEVER drop items or extract only one item when multiple items are spoken. "
    "CRITICAL MANDATORY TRANSCRIPTION CAPTURE: Every spoken utterance from the patient is valuable clinical information. "
    "If the patient states they feel fine, have no symptoms, ate nothing, or have no questions (e.g. 'አይ ምንም ይለኛል', "
    "'ምንም ምልክት የለም', 'ደህና ነኝ', 'ምንም አልበላሁም', 'ምንም የለም', 'I feel fine', 'no symptoms'), YOU MUST STILL CALL THE TOOL with raw_text set to "
    "their exact words, category set to null, duration set to null, and severity set to 'unspecified'. "
    "NEVER return without calling the tool if the patient gave a spoken response. "
    "Preserve the raw_text field exactly as it appears in the transcript — do not translate or paraphrase. "
    "CODE-SWITCHING AWARENESS: Patients frequently mix Amharic and English within a single sentence, "
    "especially for medical/clinical terms (e.g., 'tablet', 'BP', 'ultrasound', 'ANC card', 'HIV', drug names, numbers). "
    "This is normal, natural Ethiopian speech, not a transcription error to fix. When it occurs: preserve the exact "
    "mixed-language wording in raw_text without translating the English portion into Amharic or vice versa. "
    "Use the English term as a meaningful signal for classification (e.g., 'tablet' near 'የብረት' signals an iron "
    "supplement), but never alter how the words actually appeared in speech. "
    "Never attempt to output or set the danger_sign field — that is computed deterministically by the rules engine, not by you. "
    "duration must be an object: {\"value\": <integer or null>, \"unit\": \"hour|day|week|month|unspecified\"}. "
    "If no duration is mentioned, use {\"value\": null, \"unit\": \"unspecified\"}. "
    "severity must be exactly one of: mild, moderate, severe, unspecified. "
    "CRITICAL CATEGORY RULE: Most common pregnancy symptoms (such as mild weakness/fatigue, mild back pain, "
    "mild nausea, normal leg swelling, or mild headache) are NON-DANGER symptoms and MUST have category set to null. "
    "Do NOT force mild or non-critical symptoms into danger categories. Only set category to one of the 12 danger sign "
    "keys if the transcript explicitly describes a severe, persistent, or alarming danger sign: "
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
    "no_danger_sign_detected": {"am": "ምንም የአደጋ ምልክት አልተገኘም (መደበኛ)", "en": "no danger sign detected (normal)"},
    "normal_or_expected": {"am": "የተለመደ የእርግዝና ስሜት", "en": "expected pregnancy symptom"},
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
    """Look up a category's display label in the given language.

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


_SUPPLEMENT_NAME_AMHARIC: dict[str, str] = {
    "iron": "የብረት ተጨማሪ ምግብ",
    "folic_acid": "ፎሊክ አሲድ",
    "calcium": "ካልሲየም",
    "multivitamin": "መልቲቪታሚን",
}


def _supplement_display(name: str | None) -> str:
    if not name or str(name).lower().strip() in ("unknown", "other", "none", "null"):
        return "ተጨማሪ ምግብ"
    clean_name = str(name).lower().strip()
    return _SUPPLEMENT_NAME_AMHARIC.get(clean_name, str(name))


def build_verification_phrase(item: dict[str, Any], stage: CheckInStage, lang: str = "am") -> str:
    """Build the human-readable read-back string shown to the patient for confirmation in Amharic or English."""
    clean_lang = "en" if str(lang).lower().startswith("en") else "am"

    if clean_lang == "en":
        if stage == "symptoms":
            raw_text = (item.get("raw_text") or "").strip()
            category = item.get("category")
            severity = str(item.get("severity") or "").lower()
            duration_str = _format_duration(item.get("duration"), lang="en")

            if category and category not in ("no_danger_sign_detected", "normal_or_expected", "none", "null") and severity != "mild" and item.get("danger_sign", True):
                display = _category_display(category, lang="en")
            else:
                display = raw_text if raw_text else "symptom"

            parts: list[str] = [display]
            if duration_str and duration_str not in display:
                parts.append(duration_str)
            return f"{', '.join(parts)} — is that correct?"

        if stage == "food":
            raw = (item.get("raw_text") or "").strip()
            return f"Food eaten: {raw} — is that correct?"

        if stage == "supplement":
            raw_name = item.get("supplement_name") or "supplement"
            display_name = raw_name.replace("_", " ").title()
            taken = "taken today" if item.get("taken_today") else "not taken today"
            return f"{display_name} {taken} — is that correct?"

        # closing
        raw = (item.get("raw_text") or "").strip()
        return f"Mentioned: {raw} — is that correct?"

    # Default Amharic
    if stage == "symptoms":
        raw_text = (item.get("raw_text") or "").strip()
        category = item.get("category")
        severity = str(item.get("severity") or "").lower()
        duration_str = _format_duration(item.get("duration"), lang="am")

        # For active danger sign categories, use the localized danger sign display label.
        # For non-danger symptoms (category is "no_danger_sign_detected" or severity is mild), use the patient's actual reported text (raw_text).
        if category and category not in ("no_danger_sign_detected", "normal_or_expected", "none", "null") and severity != "mild" and item.get("danger_sign", True):
            display = _category_display(category, lang="am")
        else:
            display = raw_text if raw_text else "ምልክት"

        parts: list[str] = [display]
        if duration_str and duration_str not in display:
            parts.append(duration_str)
        return f"{'፣ '.join(parts)} — ትክክል ነው?"

    if stage == "food":
        raw = (item.get("raw_text") or "").strip()
        return f"የበሉት: {raw} — ትክክል ነው?"

    if stage == "supplement":
        raw_name = item.get("supplement_name")
        display_name = _supplement_display(raw_name)
        taken = "ዛሬ ወስደዋል" if item.get("taken_today") else "ዛሬ አልወሰዱም"
        return f"{display_name} {taken} — ትክክል ነው?"

    # closing
    raw = (item.get("raw_text") or "").strip()
    return f"የጠቀሱት: {raw} — ትክክል ነው?"


_build_verification_phrase = build_verification_phrase


from urllib.parse import quote


def build_tts_url(text: str, language: str = "am") -> str:
    encoded = quote(text)
    clean_lang = str(language).lower().strip()
    is_en = clean_lang.startswith("en") or (not any("\u1200" <= c <= "\u137F" for c in text))
    if is_en:
        return f"/tts?text={encoded}&language=en"
    return f"/tts?text={encoded}"


def _detect_symptom_category_from_text(text: str) -> tuple[str | None, str]:
    """Heuristic fallback for emergency danger sign recognition if LLM fails completely."""
    low = text.lower()
    if any(k in low for k in ["headache", "ራስ ምታት"]):
        if any(k in low for k in ["severe", "bad", "terrible", "ከባድ", "ጽኑ", "ከፍተኛ"]):
            return "severe_headache", "severe"
        return "severe_headache", "moderate"
    if any(k in low for k in ["bleeding", "bleed", "ደም መፍሰስ", "ደም"]):
        return "vaginal_bleeding", "severe"
    if any(k in low for k in ["blurred vision", "blurry vision", "blurry", "ብዥታ", "የእይታ ብዥታ"]):
        return "blurred_vision", "severe"
    if any(k in low for k in ["abdominal pain", "belly pain", "stomach pain", "የሆድ ህመም"]):
        return "severe_abdominal_pain", "severe"
    if any(k in low for k in ["fluid leak", "water break", "fluid leakage", "ፈሳሽ መፍሰስ"]):
        return "fluid_leakage", "severe"
    if any(k in low for k in ["high fever", "ከፍተኛ ትኩሳት", "ትኩሳት"]):
        return "high_fever", "severe"
    if any(k in low for k in ["swelling", "swollen", "እብጠት"]):
        return "swelling_hands_face", "severe"
    if any(k in low for k in ["difficulty breathing", "shortness of breath", "የመተንፈስ ችግር"]):
        return "difficulty_breathing", "severe"
    if any(k in low for k in ["convulsion", "seizure", "መንቀጥቀጥ"]):
        return "convulsions_loss_of_consciousness", "severe"
    if any(k in low for k in ["vomiting", "nausea", "ማስታወክ", "ማቅለሽለሽ"]):
        return "persistent_nausea_vomiting", "moderate"
    if any(k in low for k in ["fetal movement", "baby moving", "የፅንስ እንቅስቃሴ"]):
        return "abnormal_fetal_movement", "severe"
    return None, "unspecified"


def _attach_item_ids(
    stage: CheckInStage,
    data: dict[str, Any],
    transcript: str = "",
    language: str = "am",
) -> list[dict[str, Any]]:
    clean_transcript = transcript.strip()
    is_english = str(language).lower().startswith("en") or (clean_transcript and not any("\u1200" <= c <= "\u137F" for c in clean_transcript))

    if stage == "symptoms":
        items = []
        for item in data.get("symptoms", []):
            item = dict(item)
            item["item_id"] = str(uuid4())
            item["confirmed"] = False

            severity = str(item.get("severity") or "").lower()
            category = item.get("category")
            if severity == "mild" or not category or category in ("none", "null", "no_danger_sign_detected"):
                item["category"] = None
                item["danger_sign"] = False
            else:
                item["danger_sign"] = check_danger_sign(category)
                if not item["danger_sign"]:
                    item["category"] = None

            item["category_display"] = _category_display(item["category"], lang="am")
            item["category_display_en"] = _category_display(item["category"], lang="en")
            phrase_am = build_verification_phrase(item, stage, lang="am")
            phrase_en = build_verification_phrase(item, stage, lang="en")
            item["verification_phrase_am"] = phrase_am
            item["verification_phrase_en"] = phrase_en
            phrase = phrase_en if is_english else phrase_am
            item["verification_phrase"] = phrase
            item["verification_audio_url"] = build_tts_url(phrase, language="en" if is_english else "am")
            items.append(item)

        if not items and clean_transcript and "symptoms" not in data:
            fallback_category, fallback_severity = _detect_symptom_category_from_text(clean_transcript)
            is_danger = check_danger_sign(fallback_category) if fallback_category else False
            fallback = {
                "item_id": str(uuid4()),
                "raw_text": clean_transcript,
                "category": fallback_category,
                "category_display": _category_display(fallback_category, lang="am"),
                "category_display_en": _category_display(fallback_category, lang="en"),
                "duration": {"value": None, "unit": "unspecified"},
                "severity": fallback_severity,
                "danger_sign": is_danger,
                "confirmed": False,
            }
            phrase_am = build_verification_phrase(fallback, stage, lang="am")
            phrase_en = build_verification_phrase(fallback, stage, lang="en")
            fallback["verification_phrase_am"] = phrase_am
            fallback["verification_phrase_en"] = phrase_en
            phrase = phrase_en if is_english else phrase_am
            fallback["verification_phrase"] = phrase
            fallback["verification_audio_url"] = build_tts_url(phrase, language="en" if is_english else "am")
            items.append(fallback)

        return items

    if stage == "food":
        food = data.get("food_log")
        items = []
        if food:
            food_list = food if isinstance(food, list) else [food]
            for f in food_list:
                if not isinstance(f, dict):
                    continue
                item = dict(f)
                item["item_id"] = str(uuid4())
                item["confirmed"] = False
                raw = item.get("raw_text") or ""
                item["food_groups"] = classify_ethiopian_food(raw)
                phrase_am = build_verification_phrase(item, stage, lang="am")
                phrase_en = build_verification_phrase(item, stage, lang="en")
                item["verification_phrase_am"] = phrase_am
                item["verification_phrase_en"] = phrase_en
                phrase = phrase_en if is_english else phrase_am
                item["verification_phrase"] = phrase
                item["verification_audio_url"] = build_tts_url(phrase)
                items.append(item)

        if not items and clean_transcript and "food_log" not in data:
            fallback = {
                "item_id": str(uuid4()),
                "raw_text": clean_transcript,
                "food_groups": classify_ethiopian_food(clean_transcript),
                "confirmed": False,
            }
            phrase_am = build_verification_phrase(fallback, stage, lang="am")
            phrase_en = build_verification_phrase(fallback, stage, lang="en")
            fallback["verification_phrase_am"] = phrase_am
            fallback["verification_phrase_en"] = phrase_en
            phrase = phrase_en if is_english else phrase_am
            fallback["verification_phrase"] = phrase
            fallback["verification_audio_url"] = build_tts_url(phrase)
            items.append(fallback)

        return items

    if stage == "supplement":
        supplement = data.get("supplement_check")
        items = []
        if supplement and isinstance(supplement, dict):
            item = dict(supplement)
            item["item_id"] = str(uuid4())
            item["confirmed"] = False
            phrase_am = build_verification_phrase(item, stage, lang="am")
            phrase_en = build_verification_phrase(item, stage, lang="en")
            item["verification_phrase_am"] = phrase_am
            item["verification_phrase_en"] = phrase_en
            phrase = phrase_en if is_english else phrase_am
            item["verification_phrase"] = phrase
            item["verification_audio_url"] = build_tts_url(phrase)
            items.append(item)

        if not items and clean_transcript and "supplement_check" not in data:
            low = clean_transcript.lower()
            taken = (
                "አዎ" in clean_transcript
                or ("ወሰድ" in clean_transcript and "አልወሰድ" not in clean_transcript)
                or "yes" in low
                or ("took" in low and "not" not in low and "didn't" not in low and "miss" not in low)
            )
            fallback = {
                "item_id": str(uuid4()),
                "supplement_name": "unknown",
                "taken_today": taken,
                "raw_text": clean_transcript,
                "confirmed": False,
            }
            phrase_am = build_verification_phrase(fallback, stage, lang="am")
            phrase_en = build_verification_phrase(fallback, stage, lang="en")
            fallback["verification_phrase_am"] = phrase_am
            fallback["verification_phrase_en"] = phrase_en
            phrase = phrase_en if is_english else phrase_am
            fallback["verification_phrase"] = phrase
            fallback["verification_audio_url"] = build_tts_url(phrase)
            items.append(fallback)

        return items

    # closing
    items = []
    for mention in data.get("closing_mentions", []):
        item = dict(mention)
        item["item_id"] = str(uuid4())
        item["confirmed"] = False
        phrase_am = build_verification_phrase(item, stage, lang="am")
        phrase_en = build_verification_phrase(item, stage, lang="en")
        item["verification_phrase_am"] = phrase_am
        item["verification_phrase_en"] = phrase_en
        phrase = phrase_en if is_english else phrase_am
        item["verification_phrase"] = phrase
        item["verification_audio_url"] = build_tts_url(phrase)
        items.append(item)

    if not items and clean_transcript and "closing_mentions" not in data:
        fallback = {
            "item_id": str(uuid4()),
            "raw_text": clean_transcript,
            "topic": "general_closing",
            "confirmed": False,
        }
        phrase_am = build_verification_phrase(fallback, stage, lang="am")
        phrase_en = build_verification_phrase(fallback, stage, lang="en")
        fallback["verification_phrase_am"] = phrase_am
        fallback["verification_phrase_en"] = phrase_en
        phrase = phrase_en if is_english else phrase_am
        fallback["verification_phrase"] = phrase
        fallback["verification_audio_url"] = build_tts_url(phrase)
        items.append(fallback)

    return items


class ExtractionService:
    def __init__(self) -> None:
        self.addis_client = AddisAIClient()
        self.gemini_client = GeminiTranscribeClient()
        self.client = self.addis_client

    async def extract(
        self,
        transcript: str,
        stage: CheckInStage,
        language: str = "am",
    ) -> list[dict[str, Any]]:
        tool_def = STAGE_TOOLS[stage]
        expected_tool_name = tool_def["function"]["name"]
        item_schema = STAGE_SCHEMAS[stage]

        system_prompt = _build_system_prompt(stage)
        user_prompt = f"Stage: {stage}\nPatient Transcript:\n{transcript}"

        has_geez = any("\u1200" <= c <= "\u137F" for c in transcript)
        is_english = str(language).lower().startswith("en") or (not has_geez and bool(transcript.strip()))
        primary_client = self.gemini_client if is_english else self.addis_client
        fallback_client = self.addis_client if is_english else self.gemini_client

        last_error: Exception | None = None
        for attempt in range(3):
            current_client = primary_client if attempt < 2 else fallback_client
            try:
                raw_tool_calls = await current_client.generate_with_tools(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    tools=[tool_def],
                    tool_choice="auto",
                )

                validated_items: list[dict[str, Any]] = []
                for tool_name, args in raw_tool_calls:
                    if tool_name == expected_tool_name:
                        item = item_schema.model_validate(args).model_dump()
                        validated_items.append(item)

                if not validated_items and transcript.strip() and attempt < 2:
                    # Current client returned no structured tool calls for a non-empty patient transcript;
                    # failover to fallback client on next attempt.
                    continue

                # Assemble into stage data dict matching _attach_item_ids expectations
                stage_data: dict[str, Any] = {}
                if stage == "symptoms":
                    stage_data = {"symptoms": validated_items} if validated_items else {}
                elif stage == "food":
                    stage_data = {"food_log": validated_items} if validated_items else {}
                elif stage == "supplement":
                    stage_data = {"supplement_check": validated_items[0]} if validated_items else {}
                elif stage == "closing":
                    stage_data = {"closing_mentions": validated_items} if validated_items else {}

                return _attach_item_ids(stage, stage_data, transcript=transcript, language="en" if is_english else "am")
            except (ValidationError, ValueError, RuntimeError, Exception) as exc:
                last_error = exc
                continue

        # If all attempts failed or returned no tools, safely fall back to attached raw item with heuristic detection
        return _attach_item_ids(stage, {}, transcript=transcript, language="en" if is_english else "am")

