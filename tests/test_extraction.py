import json
from unittest.mock import AsyncMock, patch

import pytest

from app.services.addis_ai import AddisAIClient
from app.services.danger_signs import check_danger_sign
from app.services.extraction import (
    FEW_SHOT_PROMPTS,
    STAGE_TOOLS,
    _SYSTEM_PROMPT_BASE,
    ExtractionService,
    _parse_json_response,
)


def test_parse_json_response_strips_markdown_fence() -> None:
    raw = '```json\n{"symptoms":[]}\n```'
    assert _parse_json_response(raw) == {"symptoms": []}


def test_stage_tools_do_not_contain_danger_sign_parameter() -> None:
    """Critical safety test: verify NO tool schema contains a 'danger_sign' parameter."""
    for stage, tool in STAGE_TOOLS.items():
        props = tool["function"]["parameters"]["properties"]
        assert "danger_sign" not in props, f"Tool for stage '{stage}' must never include danger_sign parameter!"


def test_addis_ai_client_extracts_openai_and_native_tool_calls() -> None:
    """Verify AddisAIClient._extract_tool_calls handles choices[0].message.tool_calls and native data formats."""
    # 1. OpenAI choices format with JSON string arguments
    openai_payload = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": "call_1",
                            "type": "function",
                            "function": {
                                "name": "log_symptom",
                                "arguments": '{"raw_text": "ከባድ ራስ ምታት", "category": "severe_headache"}',
                            },
                        }
                    ],
                }
            }
        ]
    }
    extracted = AddisAIClient._extract_tool_calls(openai_payload)
    assert len(extracted) == 1
    assert extracted[0][0] == "log_symptom"
    assert extracted[0][1]["category"] == "severe_headache"

    # 2. Native envelope format (data.tool_calls with dict arguments)
    native_payload = {
        "status": "success",
        "data": {
            "tool_calls": [
                {
                    "name": "log_food_entry",
                    "arguments": {"raw_text": "ጤፍ እና ስንዴ"},
                }
            ]
        },
    }
    extracted_native = AddisAIClient._extract_tool_calls(native_payload)
    assert len(extracted_native) == 1
    assert extracted_native[0][0] == "log_food_entry"
    assert extracted_native[0][1]["raw_text"] == "ጤፍ እና ስንዴ"

    # 3. Empty / zero tool calls
    empty_payload = {"choices": [{"message": {"role": "assistant", "content": ""}}]}
    assert AddisAIClient._extract_tool_calls(empty_payload) == []


@pytest.mark.asyncio
async def test_extraction_validates_single_symptom_and_sets_danger_sign() -> None:
    service = ExtractionService()
    mock_calls = [
        (
            "log_symptom",
            {
                "raw_text": "ከባድ ራስ ምታት",
                "category": "severe_headache",
                "duration": {"value": 1, "unit": "day"},
                "severity": "severe",
            },
        )
    ]

    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ከባድ ራስ ምታት", "symptoms")

    assert len(items) == 1
    assert items[0]["raw_text"] == "ከባድ ራስ ምታት"
    assert items[0]["category"] == "severe_headache"
    assert items[0]["danger_sign"] is True
    assert items[0]["confirmed"] is False
    assert "item_id" in items[0]
    assert "verification_phrase" in items[0]
    assert "ከባድ ራስ ምታት" in items[0]["verification_phrase"]
    assert "1 ቀን" in items[0]["verification_phrase"]


@pytest.mark.asyncio
async def test_extraction_multi_symptom_separate_tool_calls() -> None:
    """Multi-item mandate: multiple tool calls in one utterance produce multiple separate items."""
    service = ExtractionService()
    mock_calls = [
        (
            "log_symptom",
            {
                "raw_text": "እግሮቼ ለሶስት ቀናት እያበጡ ነው",
                "category": "swelling_hands_face",
                "duration": {"value": 3, "unit": "day"},
                "severity": "moderate",
            },
        ),
        (
            "log_symptom",
            {
                "raw_text": "ከባድ ራስ ምታት አለኝ",
                "category": "severe_headache",
                "duration": {"value": None, "unit": "unspecified"},
                "severity": "severe",
            },
        ),
    ]

    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("እግሮቼ ለሶስት ቀናት እያበጡ ነው እና ከባድ ራስ ምታት አለኝ", "symptoms")

    assert len(items) == 2
    assert items[0]["category"] == "swelling_hands_face"
    assert items[0]["danger_sign"] is True
    assert items[1]["category"] == "severe_headache"
    assert items[1]["danger_sign"] is True
    assert items[0]["item_id"] != items[1]["item_id"]


@pytest.mark.asyncio
async def test_extraction_negative_response_with_tool_call() -> None:
    """A negative response called via tool produces an item with category: null, danger_sign: False."""
    service = ExtractionService()
    mock_calls = [
        (
            "log_symptom",
            {
                "raw_text": "ምንም ምልክት የለም ደህና ነኝ",
                "category": None,
                "duration": {"value": None, "unit": "unspecified"},
                "severity": "unspecified",
            },
        )
    ]

    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ምንም ምልክት የለም ደህና ነኝ", "symptoms")

    assert len(items) == 1
    assert items[0]["raw_text"] == "ምንም ምልክት የለም ደህና ነኝ"
    assert items[0]["category"] is None
    assert items[0]["danger_sign"] is False
    assert items[0]["verification_phrase"] == "ምንም ምልክት የለም ደህና ነኝ — ትክክል ነው?"


@pytest.mark.asyncio
async def test_extraction_zero_tool_calls_fallback_captures_utterance() -> None:
    """When the model makes 0 tool calls, the patient utterance is still captured without data loss."""
    service = ExtractionService()
    # Zero tool calls returned by model
    mock_calls = []

    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ምንም አልተሰማኝም ደህና ነኝ", "symptoms")

    assert len(items) == 1
    assert items[0]["raw_text"] == "ምንም አልተሰማኝም ደህና ነኝ"
    assert items[0]["category"] is None
    assert items[0]["danger_sign"] is False
    assert items[0]["verification_phrase"] == "ምንም አልተሰማኝም ደህና ነኝ — ትክክል ነው?"


@pytest.mark.asyncio
async def test_extraction_code_switching_preserves_english_and_infers_supplement() -> None:
    """Code-switched input preserves English words in raw_text and extracts correct supplement name."""
    service = ExtractionService()
    mock_calls = [
        (
            "log_supplement_check",
            {
                "raw_text": "የብረት tablet ዛሬ ወስጄያለሁ",
                "supplement_name": "iron",
                "taken_today": True,
            },
        )
    ]

    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("የብረት tablet ዛሬ ወስጄያለሁ", "supplement")

    assert len(items) == 1
    assert "tablet" in items[0]["raw_text"]
    assert items[0]["supplement_name"] == "iron"
    assert items[0]["taken_today"] is True
    assert items[0]["verification_phrase"] == "የብረት ተጨማሪ ምግብ ዛሬ ወስደዋል — ትክክል ነው?"


@pytest.mark.asyncio
async def test_danger_sign_is_determined_strictly_by_python_lookup() -> None:
    """Verify danger_sign is NEVER set by tool args and strictly determined by check_danger_sign(category)."""
    service = ExtractionService()
    # Even if hostile / invalid tool call args include danger_sign=True with a fake category
    mock_calls = [
        (
            "log_symptom",
            {
                "raw_text": "ቀላል ህመም",
                "category": "not_a_danger_sign",
                "danger_sign": True,  # should be ignored/overridden
                "severity": "moderate",
            },
        )
    ]

    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ቀላል ህመም", "symptoms")

    assert len(items) == 1
    assert items[0]["danger_sign"] is False
    assert items[0]["category"] is None


@pytest.mark.asyncio
async def test_extraction_mild_symptom_overrides_danger_sign_to_false() -> None:
    service = ExtractionService()
    mock_calls = [
        (
            "log_symptom",
            {
                "raw_text": "ቀላል የድካም ስሜት",
                "category": "severe_weakness_or_backache",
                "duration": {"value": None, "unit": "unspecified"},
                "severity": "mild",
            },
        )
    ]

    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ቀላል የድካም ስሜት", "symptoms")

    assert len(items) == 1
    assert items[0]["category"] is None
    assert items[0]["danger_sign"] is False
    assert items[0]["verification_phrase"] == "ቀላል የድካም ስሜት — ትክክል ነው?"


@pytest.mark.asyncio
async def test_extraction_food_multiple_calls() -> None:
    service = ExtractionService()
    mock_calls = [
        ("log_food_entry", {"raw_text": "ጤፍ እና ስንዴ"}),
        ("log_food_entry", {"raw_text": "ወተት"}),
    ]

    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ዛሬ ጤፍ፣ ስንዴ እና ወተት ጠጣሁ", "food")

    assert len(items) == 2
    assert items[0]["raw_text"] == "ጤፍ እና ስንዴ"
    assert items[1]["raw_text"] == "ወተት"
    assert "grains" in items[0]["food_groups"]
    assert "dairy" in items[1]["food_groups"]


@pytest.mark.asyncio
async def test_extraction_closing_mentions() -> None:
    service = ExtractionService()
    mock_calls = [
        ("log_closing_mention", {"raw_text": "በወራት ላይ ጡት መክተት እፈልጋለሁ", "topic": "breastfeeding_intent"}),
        ("log_closing_mention", {"raw_text": "ስለ አመጋገብ ማወቅ እፈልጋለሁ", "topic": "dietary_intake"}),
    ]

    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("በወራት ላይ ጡት መክተት እፈልጋለሁ እና ስለ አመጋገብ ማወቅ እፈልጋለሁ", "closing")

    assert len(items) == 2
    assert items[0]["topic"] == "breastfeeding_intent"
    assert items[1]["topic"] == "dietary_intake"


def test_system_prompt_has_codeswitching_awareness_instruction() -> None:
    """Requirement 1: System prompt must explicitly include CODE-SWITCHING AWARENESS instruction."""
    assert "CODE-SWITCHING AWARENESS:" in _SYSTEM_PROMPT_BASE
    assert "Patients frequently mix Amharic and English" in _SYSTEM_PROMPT_BASE
    assert "tablet" in _SYSTEM_PROMPT_BASE
    assert "BP" in _SYSTEM_PROMPT_BASE
    assert "ultrasound" in _SYSTEM_PROMPT_BASE
    assert "ANC card" in _SYSTEM_PROMPT_BASE
    assert "HIV" in _SYSTEM_PROMPT_BASE
    assert "not a transcription error to fix" in _SYSTEM_PROMPT_BASE
    assert "preserve the exact mixed-language wording in raw_text" in _SYSTEM_PROMPT_BASE


def test_few_shot_prompts_have_codeswitching_across_all_stages() -> None:
    """Requirement 2: Few-shot examples must have code-switching examples in all four stages."""
    # Symptoms
    assert "ትንሽ dizziness ይሰማኛል ግን ደህና ነኝ" in FEW_SHOT_PROMPTS["symptoms"]
    assert "Severe headache አለብኝ" in FEW_SHOT_PROMPTS["symptoms"]
    # Food
    assert "ዛሬ bread እና ሻይ ጠጣሁ" in FEW_SHOT_PROMPTS["food"]
    # Supplement
    assert "የብረት tablet ዛሬ ወስጄያለሁ" in FEW_SHOT_PROMPTS["supplement"]
    # Closing
    assert "ስለ ultrasound appointment ማወቅ እፈልጋለሁ" in FEW_SHOT_PROMPTS["closing"]


@pytest.mark.asyncio
async def test_extraction_symptoms_codeswitching_mild_non_danger() -> None:
    """Checklist: Symptom-stage code-switched input keeps English intact and resolves category to null."""
    service = ExtractionService()
    mock_calls = [
        (
            "log_symptom",
            {
                "raw_text": "ትንሽ dizziness ይሰማኛል ግን ደህና ነኝ",
                "category": None,
                "duration": {"value": None, "unit": "unspecified"},
                "severity": "mild",
            },
        )
    ]
    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ትንሽ dizziness ይሰማኛል ግን ደህና ነኝ", "symptoms")

    assert len(items) == 1
    assert items[0]["raw_text"] == "ትንሽ dizziness ይሰማኛል ግን ደህና ነኝ"
    assert "dizziness" in items[0]["raw_text"]
    assert items[0]["category"] is None
    assert items[0]["danger_sign"] is False
    assert items[0]["severity"] == "mild"
    assert "dizziness" in items[0]["verification_phrase"]


@pytest.mark.asyncio
async def test_extraction_symptoms_codeswitching_danger_sign_intact() -> None:
    """Checklist: Symptom-stage code-switched danger sign resolves category and computes danger_sign True."""
    service = ExtractionService()
    mock_calls = [
        (
            "log_symptom",
            {
                "raw_text": "Severe headache አለብኝ",
                "category": "severe_headache",
                "duration": {"value": None, "unit": "unspecified"},
                "severity": "severe",
            },
        )
    ]
    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("Severe headache አለብኝ", "symptoms")

    assert len(items) == 1
    assert items[0]["raw_text"] == "Severe headache አለብኝ"
    assert "Severe headache" in items[0]["raw_text"]
    assert items[0]["category"] == "severe_headache"
    assert items[0]["danger_sign"] is True
    assert "ከባድ ራስ ምታት" in items[0]["verification_phrase"]


@pytest.mark.asyncio
async def test_extraction_food_codeswitching_bread() -> None:
    """Checklist: Food-stage code-switched input keeps English 'bread' intact and maps to food groups."""
    service = ExtractionService()
    mock_calls = [
        ("log_food_entry", {"raw_text": "ዛሬ bread እና ሻይ ጠጣሁ"}),
    ]
    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ዛሬ bread እና ሻይ ጠጣሁ", "food")

    assert len(items) == 1
    assert items[0]["raw_text"] == "ዛሬ bread እና ሻይ ጠጣሁ"
    assert "bread" in items[0]["raw_text"]
    assert "grains" in items[0]["food_groups"]


@pytest.mark.asyncio
async def test_extraction_closing_codeswitching_ultrasound() -> None:
    """Checklist: Closing-stage code-switched input keeps English intact and classifies topic."""
    service = ExtractionService()
    mock_calls = [
        (
            "log_closing_mention",
            {
                "raw_text": "ስለ ultrasound appointment ማወቅ እፈልጋለሁ",
                "topic": "general_closing",
            },
        ),
    ]
    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ስለ ultrasound appointment ማወቅ እፈልጋለሁ", "closing")

    assert len(items) == 1
    assert items[0]["raw_text"] == "ስለ ultrasound appointment ማወቅ እፈልጋለሁ"
    assert "ultrasound appointment" in items[0]["raw_text"]
    assert items[0]["topic"] == "general_closing"


@pytest.mark.asyncio
async def test_extraction_codeswitching_generalization_unseen_terms() -> None:
    """Checklist: Sanity-check generalizing behavior on code-switched inputs not in few-shot examples."""
    service = ExtractionService()
    mock_calls = [
        (
            "log_symptom",
            {
                "raw_text": "ከፍተኛ fever አለብኝ እና BP ተመርምሬያለሁ",
                "category": "high_fever",
                "duration": {"value": None, "unit": "unspecified"},
                "severity": "severe",
            },
        )
    ]
    with patch.object(service.client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)):
        items = await service.extract("ከፍተኛ fever አለብኝ እና BP ተመርምሬያለሁ", "symptoms")

    assert len(items) == 1
    assert items[0]["raw_text"] == "ከፍተኛ fever አለብኝ እና BP ተመርምሬያለሁ"
    assert "fever" in items[0]["raw_text"]
    assert "BP" in items[0]["raw_text"]
    assert items[0]["category"] == "high_fever"
    assert items[0]["danger_sign"] is True

