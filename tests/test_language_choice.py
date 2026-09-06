import io
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.routes.checkin import get_current_user_id
from app.core.constants import (
    CHECKIN_STAGES,
    STAGE_PROMPTS,
    STAGE_PROMPTS_EN,
    get_stage_category,
    get_stage_prompt,
)
from app.main import app
from app.services.addis_ai import AddisAIClient
from app.services.checkin_session import CheckInSessionService
from app.services.extraction import (
    ExtractionService,
    build_tts_url,
    build_verification_phrase,
)
from app.services.gemini import GeminiTranscribeClient, to_gemini_parameter_schema
from app.services.sahara import SaharaVoiceClient
from app.services.speech import get_tts_client, normalize_language


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_user_id() -> str:
    return str(uuid4())


# 1. Constants Tests
def test_stage_prompts_and_categories_localization() -> None:
    # Amharic prompts
    for stage in CHECKIN_STAGES:
        am_prompt = get_stage_prompt(stage, language="am")
        assert am_prompt == STAGE_PROMPTS[stage]
        assert len(am_prompt) > 0

    # English prompts
    for stage in CHECKIN_STAGES:
        en_prompt = get_stage_prompt(stage, language="en")
        assert en_prompt == STAGE_PROMPTS_EN[stage]
        assert "Did you" in en_prompt or "What foods" in en_prompt or "Do you have" in en_prompt

    # Categories
    assert get_stage_category("symptoms", language="am") == "የአደጋ ምልክቶች እና ህመም"
    assert get_stage_category("symptoms", language="en") == "DANGER SIGNS & SYMPTOMS"
    assert get_stage_category("food", language="en") == "NUTRITION & DIET"


# 2. Speech Normalization & TTS Client Routing
def test_normalize_language() -> None:
    assert normalize_language("am") == "am"
    assert normalize_language("en") == "en"
    assert normalize_language("english") == "en"
    assert normalize_language("en-US") == "en"
    assert normalize_language("amharic") == "am"
    assert normalize_language(None) == "am"
    assert normalize_language("") == "am"


def test_get_tts_client_english_routing() -> None:
    # When language is "en", even if model="addisai" requested, route to Sahara (gTTS fallback supported)
    client_en = get_tts_client("addisai", language="en")
    assert isinstance(client_en, SaharaVoiceClient)

    # When language is "am" and model="addisai", routes to AddisAIClient
    client_am = get_tts_client("addisai", language="am")
    assert isinstance(client_am, AddisAIClient)

    # Sahara with English
    client_sahara = get_tts_client("sahara", language="en")
    assert isinstance(client_sahara, SaharaVoiceClient)


# 3. Extraction Verification Phrases Localization
def test_build_verification_phrase_localization() -> None:
    symptom_item = {
        "raw_text": "severe headache",
        "category": "severe_headache",
        "category_display": "ከባድ ራስ ምታት",
        "category_display_en": "Severe headache",
        "duration": {"value": 2, "unit": "day"},
        "severity": "severe",
    }
    phrase_am = build_verification_phrase(symptom_item, "symptoms", lang="am")
    phrase_en = build_verification_phrase(symptom_item, "symptoms", lang="en")

    assert "ትክክል ነው?" in phrase_am
    assert "is that correct?" in phrase_en
    assert "2 day(s)" in phrase_en

    supplement_item = {
        "supplement_name": "iron",
        "taken_today": True,
        "raw_text": "I took iron",
    }
    phrase_supp_am = build_verification_phrase(supplement_item, "supplement", lang="am")
    phrase_supp_en = build_verification_phrase(supplement_item, "supplement", lang="en")

    assert "ትክክል ነው?" in phrase_supp_am
    assert "Iron taken today" in phrase_supp_en
    assert "is that correct?" in phrase_supp_en


def test_build_tts_url_localization() -> None:
    am_url = build_tts_url("ዛሬ ራስ ምታት አለኝ", language="am")
    assert "language=en" not in am_url

    en_url = build_tts_url("Severe headache — is that correct?", language="en")
    assert "language=en" in en_url


# 4. CheckInSessionService Start Session in English
def test_checkin_session_start_english() -> None:
    service = CheckInSessionService()
    user_id = uuid4()

    with patch.object(service.check_ins, "has_food_logged_today", return_value=False), \
         patch.object(service.supplements, "list_active", return_value=[]), \
         patch.object(service.sessions, "create") as mock_create:
        mock_create.return_value = {"id": uuid4()}

        res = service.start_session(user_id, language="en")
        assert res["language"] == "en"
        assert res["question_prompt"] == STAGE_PROMPTS_EN["symptoms"]
        assert "_en.mp3" in res["question_audio_url"]
        # Verify draft_data stored language="en"
        create_call_args = mock_create.call_args[0][1]
        assert create_call_args["draft_data"]["language"] == "en"


# 5. CheckInSessionService Respond Language & ASR Routing
@pytest.mark.asyncio
async def test_checkin_respond_addisai_locks_asr_to_amharic_even_if_english() -> None:
    service = CheckInSessionService()
    session_id = uuid4()
    session = {
        "id": session_id,
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "closing"],
        "draft_data": {"symptoms": [], "language": "en"},
        "pending_items": [],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session), \
         patch.object(AddisAIClient, "transcribe", new=AsyncMock(return_value="I have severe headache")) as mock_addis, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])) as mock_extract, \
         patch.object(service.sessions, "update"):

        await service.respond(
            user_id=session_id,
            session_id=session_id,
            audio_bytes=b"fake_audio",
            filename="voice.wav",
            content_type="audio/wav",
            model="addisai",
        )

        # Addis AI ASR must receive language="am"
        mock_addis.assert_called_once_with(b"fake_audio", "voice.wav", "audio/wav", language="am")
        # Extraction should receive the session language ("en")
        mock_extract.assert_called_once_with("I have severe headache", "symptoms", language="en")


@pytest.mark.asyncio
async def test_checkin_respond_sahara_passes_english_language() -> None:
    service = CheckInSessionService()
    session_id = uuid4()
    session = {
        "id": session_id,
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "closing"],
        "draft_data": {"symptoms": [], "language": "en"},
        "pending_items": [],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session), \
         patch.object(SaharaVoiceClient, "transcribe", new=AsyncMock(return_value="I have headache")) as mock_sahara, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])) as mock_extract, \
         patch.object(service.sessions, "update"):

        await service.respond(
            user_id=session_id,
            session_id=session_id,
            audio_bytes=b"fake_audio",
            filename="voice.wav",
            content_type="audio/wav",
            model="sahara",
            language="en",
        )

        # Sahara ASR receives language="en"
        mock_sahara.assert_called_once_with(b"fake_audio", "voice.wav", "audio/wav", language="en")
        mock_extract.assert_called_once_with("I have headache", "symptoms", language="en")


@pytest.mark.asyncio
async def test_checkin_respond_gemini_passes_english_language() -> None:
    service = CheckInSessionService()
    session_id = uuid4()
    session = {
        "id": session_id,
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "closing"],
        "draft_data": {"symptoms": [], "language": "en"},
        "pending_items": [],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session), \
         patch.object(GeminiTranscribeClient, "transcribe", new=AsyncMock(return_value="I have fever")) as mock_gemini, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])) as mock_extract, \
         patch.object(service.sessions, "update"):

        await service.respond(
            user_id=session_id,
            session_id=session_id,
            audio_bytes=b"fake_audio",
            filename="voice.wav",
            content_type="audio/wav",
            model="gemini",
        )

        # Gemini receives language="en" (which maps internally to en-US)
        mock_gemini.assert_called_once_with(b"fake_audio", "voice.wav", "audio/wav", language="en")
        mock_extract.assert_called_once_with("I have fever", "symptoms", language="en")


# 6. HTTP API Endpoint Tests
def test_api_start_checkin_english(test_client: TestClient, mock_user_id: str) -> None:
    app.dependency_overrides[get_current_user_id] = lambda: uuid4()
    try:
        with patch.object(CheckInSessionService, "start_session") as mock_start:
            mock_start.return_value = {
                "session_id": uuid4(),
                "stage": "symptoms",
                "question_prompt": STAGE_PROMPTS_EN["symptoms"],
                "question_audio_url": "https://example.com/prompts/symptoms_en.mp3",
                "language": "en",
            }
            res = test_client.post("/checkin/start?language=en")
            assert res.status_code == 200
            data = res.json()
            assert data["language"] == "en"
            assert data["question_prompt"] == STAGE_PROMPTS_EN["symptoms"]
    finally:
        app.dependency_overrides.clear()


def test_api_tts_english_endpoint(test_client: TestClient) -> None:
    fake_audio = b"ENGLISH_TTS_AUDIO_BYTES"

    with patch.object(SaharaVoiceClient, "synthesize_speech", new=AsyncMock(return_value=fake_audio)):
        # Test GET with language=en
        res_get = test_client.get("/tts?text=Did%20you%20experience%20any%20symptoms&model=sahara&language=en")
        assert res_get.status_code == 200
        assert res_get.content == fake_audio

        # Test POST with language=en and model=addisai (routes to Sahara / gTTS)
        res_post = test_client.post(
            "/tts",
            json={
                "text": "Did you take your daily supplements today?",
                "model": "addisai",
                "language": "en",
            },
        )
        assert res_post.status_code == 200
        assert res_post.content == fake_audio


# 7. Gemini Parameter Schema Converter
def test_gemini_parameter_schema_conversion() -> None:
    schema = {
        "type": "object",
        "properties": {
            "symptom": {"type": "string", "description": "The symptom"},
            "severity": {"type": ["string", "null"], "enum": ["mild", "severe", None]},
            "nested": {
                "type": "object",
                "properties": {
                    "count": {"type": "integer"}
                }
            }
        },
        "required": ["symptom"]
    }

    converted = to_gemini_parameter_schema(schema)
    assert converted["type"] == "OBJECT"
    assert converted["properties"]["symptom"]["type"] == "STRING"
    assert converted["properties"]["severity"]["type"] == "STRING"
    assert converted["properties"]["severity"]["nullable"] is True
    assert converted["properties"]["severity"]["enum"] == ["mild", "severe"]
    assert converted["properties"]["nested"]["type"] == "OBJECT"
    assert converted["properties"]["nested"]["properties"]["count"]["type"] == "INTEGER"
    assert converted["required"] == ["symptom"]


# 8. Extraction Tool Calling Language Routing Tests
@pytest.mark.asyncio
async def test_extraction_service_routes_to_gemini_for_english() -> None:
    service = ExtractionService()
    mock_calls = [
        (
            "log_symptom",
            {
                "raw_text": "I have severe headache",
                "category": "severe_headache",
                "duration": {"value": 1, "unit": "day"},
                "severity": "severe",
            },
        )
    ]

    with patch.object(service.gemini_client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)) as mock_gemini, \
         patch.object(service.addis_client, "generate_with_tools", new=AsyncMock()) as mock_addis:

        items = await service.extract("I have severe headache", "symptoms", language="en")

        mock_gemini.assert_called_once()
        mock_addis.assert_not_called()
        assert len(items) == 1
        assert items[0]["raw_text"] == "I have severe headache"
        assert items[0]["category"] == "severe_headache"
        assert items[0]["danger_sign"] is True
        assert "is that correct?" in items[0]["verification_phrase"]
        assert "1 day(s)" in items[0]["verification_phrase"]


@pytest.mark.asyncio
async def test_extraction_service_routes_to_addisai_for_amharic() -> None:
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

    with patch.object(service.addis_client, "generate_with_tools", new=AsyncMock(return_value=mock_calls)) as mock_addis, \
         patch.object(service.gemini_client, "generate_with_tools", new=AsyncMock()) as mock_gemini:

        items = await service.extract("ከባድ ራስ ምታት", "symptoms", language="am")

        mock_addis.assert_called_once()
        mock_gemini.assert_not_called()
        assert len(items) == 1
        assert items[0]["raw_text"] == "ከባድ ራስ ምታት"
        assert items[0]["category"] == "severe_headache"
        assert items[0]["danger_sign"] is True
        assert "ትክክል ነው?" in items[0]["verification_phrase"]


@pytest.mark.asyncio
async def test_extraction_service_fallback_to_gemini_on_amharic_failure() -> None:
    service = ExtractionService()
    fallback_calls = [
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

    with patch.object(service.addis_client, "generate_with_tools", new=AsyncMock(side_effect=RuntimeError("Addis AI timeout"))) as mock_addis, \
         patch.object(service.gemini_client, "generate_with_tools", new=AsyncMock(return_value=fallback_calls)) as mock_gemini:

        items = await service.extract("ከባድ ራስ ምታት", "symptoms", language="am")

        # 2 attempts on addis_client, then 3rd attempt falls back to gemini_client
        assert mock_addis.call_count == 2
        mock_gemini.assert_called_once()
        assert len(items) == 1
        assert items[0]["category"] == "severe_headache"


@pytest.mark.asyncio
async def test_extraction_service_fallback_to_addisai_on_english_failure() -> None:
    service = ExtractionService()
    fallback_calls = [
        (
            "log_symptom",
            {
                "raw_text": "severe headache",
                "category": "severe_headache",
                "duration": {"value": 1, "unit": "day"},
                "severity": "severe",
            },
        )
    ]

    with patch.object(service.gemini_client, "generate_with_tools", new=AsyncMock(side_effect=RuntimeError("Gemini error"))) as mock_gemini, \
         patch.object(service.addis_client, "generate_with_tools", new=AsyncMock(return_value=fallback_calls)) as mock_addis:

        items = await service.extract("severe headache", "symptoms", language="en")

        assert mock_gemini.call_count == 2
        mock_addis.assert_called_once()
        assert len(items) == 1
        assert items[0]["category"] == "severe_headache"

