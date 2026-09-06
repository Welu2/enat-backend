import io
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.addis_ai import AddisAIClient
from app.services.checkin_session import CheckInSessionService
from app.services.deepgram import DeepgramClient
from app.services.speech import (
    get_asr_client,
    get_tts_client,
    normalize_voice_model,
)


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


# 1. Voice Model Normalization Tests
def test_normalize_voice_model_deepgram() -> None:
    assert normalize_voice_model("deepgram") == "deepgram"
    assert normalize_voice_model("deep_gram") == "deepgram"
    assert normalize_voice_model("DEEPGRAM") == "deepgram"
    assert normalize_voice_model("deepgram_voice") == "deepgram"


# 2. Speech Service Routing Tests
def test_get_asr_client_deepgram() -> None:
    client = get_asr_client("deepgram")
    assert isinstance(client, DeepgramClient)

    client_alias = get_asr_client("deep_gram")
    assert isinstance(client_alias, DeepgramClient)


def test_get_tts_client_deepgram_routing() -> None:
    # When language is English, returns DeepgramClient
    client_en = get_tts_client("deepgram", language="en")
    assert isinstance(client_en, DeepgramClient)

    # When language is Amharic, Deepgram does not support Amharic -> routes to AddisAIClient
    client_am = get_tts_client("deepgram", language="am")
    assert isinstance(client_am, AddisAIClient)


# 3. DeepgramClient TTS Synthesis Tests
@pytest.mark.asyncio
async def test_deepgram_synthesize_speech_english_success() -> None:
    client = DeepgramClient()
    client.settings.deepgram_api_key = "test_dg_key"
    client.settings.deepgram_api_base_url = "https://api.deepgram.com"
    client.settings.deepgram_tts_model = "aura-asteria-en"

    mock_audio_bytes = b"DEEPGRAM_AURA_TTS_MP3_STREAM"

    def mock_post(url, headers=None, json=None):
        assert "v1/speak?model=aura-asteria-en" in str(url)
        assert headers.get("Authorization") == "Token test_dg_key"
        assert json.get("text") == "Please describe your symptoms"
        return httpx.Response(200, content=mock_audio_bytes, request=httpx.Request("POST", str(url)))

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(side_effect=mock_post)):
        result = await client.synthesize_speech("Please describe your symptoms", language="en")

    assert result == mock_audio_bytes


@pytest.mark.asyncio
async def test_deepgram_synthesize_speech_fallback_on_missing_key() -> None:
    client = DeepgramClient()
    client.settings.deepgram_api_key = ""  # No key configured

    result = await client.synthesize_speech("Hello mother", language="en")
    assert isinstance(result, bytes)
    assert len(result) > 0  # Fallback to gTTS succeeded


@pytest.mark.asyncio
async def test_deepgram_synthesize_speech_fallback_on_http_error() -> None:
    client = DeepgramClient()
    client.settings.deepgram_api_key = "test_dg_key"

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(side_effect=httpx.ConnectError("Connection refused"))):
        result = await client.synthesize_speech("Hello there", language="en")

    assert isinstance(result, bytes)
    assert len(result) > 0  # Fallback to gTTS succeeded


@pytest.mark.asyncio
async def test_deepgram_synthesize_speech_amharic_safeguard() -> None:
    client = DeepgramClient()
    mock_addis_audio = b"ADDIS_AI_AMHARIC_AUDIO"

    with patch.object(client.addis_client, "synthesize_speech", new=AsyncMock(return_value=mock_addis_audio)) as mock_addis:
        result = await client.synthesize_speech("ጤና ይስጥልኝ", language="am")

    mock_addis.assert_called_once_with("ጤና ይስጥልኝ", voice_id=None, language="am")
    assert result == mock_addis_audio


# 4. DeepgramClient STT Listen Transcription Tests
@pytest.mark.asyncio
async def test_deepgram_transcribe_english_success() -> None:
    client = DeepgramClient()
    client.settings.deepgram_api_key = "test_dg_key"
    client.settings.deepgram_api_base_url = "https://api.deepgram.com"
    client.settings.deepgram_stt_model = "nova-2"

    def mock_post(url, headers=None, content=None):
        assert "v1/listen" in str(url)
        assert "model=nova-2" in str(url)
        assert headers.get("Authorization") == "Token test_dg_key"
        assert content == b"fake_voice"
        return httpx.Response(
            200,
            json={
                "results": {
                    "channels": [
                        {
                            "alternatives": [
                                {
                                    "transcript": "I feel dizzy today",
                                    "confidence": 0.98,
                                }
                            ]
                        }
                    ]
                }
            },
            request=httpx.Request("POST", str(url)),
        )

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(side_effect=mock_post)):
        transcript = await client.transcribe(
            audio_bytes=b"fake_voice",
            filename="voice.wav",
            content_type="audio/wav",
            language="en",
        )

    assert transcript == "I feel dizzy today"


@pytest.mark.asyncio
async def test_deepgram_transcribe_missing_key_raises() -> None:
    client = DeepgramClient()
    client.settings.deepgram_api_key = ""

    with pytest.raises(RuntimeError, match="DEEPGRAM_API_KEY is not configured"):
        await client.transcribe(b"fake_voice", language="en")


@pytest.mark.asyncio
async def test_deepgram_transcribe_amharic_safeguard() -> None:
    client = DeepgramClient()

    with patch.object(client.addis_client, "transcribe", new=AsyncMock(return_value="ራስ ምታት አለኝ")) as mock_addis:
        res = await client.transcribe(b"audio", filename="test.wav", content_type="audio/wav", language="am")

    mock_addis.assert_called_once_with(b"audio", "test.wav", "audio/wav", language="am")
    assert res == "ራስ ምታት አለኝ"


# 5. CheckInSessionService Integration with Deepgram
@pytest.mark.asyncio
async def test_checkin_respond_deepgram_english() -> None:
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
         patch.object(DeepgramClient, "transcribe", new=AsyncMock(return_value="I feel tired today")) as mock_transcribe, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])) as mock_extract, \
         patch.object(service.sessions, "update"):

        await service.respond(
            user_id=session_id,
            session_id=session_id,
            audio_bytes=b"fake_audio",
            filename="voice.wav",
            content_type="audio/wav",
            model="deepgram",
        )

        mock_transcribe.assert_called_once_with(b"fake_audio", "voice.wav", "audio/wav", language="en")
        mock_extract.assert_called_once_with("I feel tired today", "symptoms", language="en")


@pytest.mark.asyncio
async def test_checkin_respond_deepgram_amharic_safeguard() -> None:
    service = CheckInSessionService()
    session_id = uuid4()
    session = {
        "id": session_id,
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "closing"],
        "draft_data": {"symptoms": [], "language": "am"},
        "pending_items": [],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session), \
         patch.object(AddisAIClient, "transcribe", new=AsyncMock(return_value="ደህና ነኝ")) as mock_addis, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])) as mock_extract, \
         patch.object(service.sessions, "update"):

        await service.respond(
            user_id=session_id,
            session_id=session_id,
            audio_bytes=b"fake_audio",
            filename="voice.wav",
            content_type="audio/wav",
            model="deepgram",
        )

        # In Amharic sessions, Deepgram is safeguarded to Addis AI ASR
        mock_addis.assert_called_once_with(b"fake_audio", "voice.wav", "audio/wav", language="am")
        mock_extract.assert_called_once_with("ደህና ነኝ", "symptoms", language="am")


# 6. HTTP API Endpoint Tests
def test_api_tts_deepgram_get(test_client: TestClient) -> None:
    fake_audio = b"DEEPGRAM_GET_AUDIO"

    with patch.object(DeepgramClient, "synthesize_speech", new=AsyncMock(return_value=fake_audio)):
        res = test_client.get("/tts?text=Did%20you%20take%20iron&model=deepgram&language=en")
        assert res.status_code == 200
        assert res.content == fake_audio


def test_api_tts_deepgram_post(test_client: TestClient) -> None:
    fake_audio = b"DEEPGRAM_POST_AUDIO"

    with patch.object(DeepgramClient, "synthesize_speech", new=AsyncMock(return_value=fake_audio)):
        res = test_client.post(
            "/tts",
            json={
                "text": "Did you take iron today?",
                "model": "deepgram",
                "language": "en",
            },
        )
        assert res.status_code == 200
        assert res.content == fake_audio
