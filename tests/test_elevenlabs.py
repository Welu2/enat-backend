import io
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.addis_ai import AddisAIClient
from app.services.checkin_session import CheckInSessionService
from app.services.elevenlabs import ElevenLabsClient
from app.services.speech import (
    get_asr_client,
    get_tts_client,
    normalize_voice_model,
)


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


# 1. Voice Model Normalization Tests
def test_normalize_voice_model_elevenlabs() -> None:
    assert normalize_voice_model("elevenlabs") == "elevenlabs"
    assert normalize_voice_model("eleven_labs") == "elevenlabs"
    assert normalize_voice_model("ELEVENLABS") == "elevenlabs"
    assert normalize_voice_model("eleven") == "elevenlabs"
    assert normalize_voice_model("11labs") == "elevenlabs"


# 2. Speech Service Routing Tests
def test_get_asr_client_elevenlabs() -> None:
    client = get_asr_client("elevenlabs")
    assert isinstance(client, ElevenLabsClient)

    client_alias = get_asr_client("eleven_labs")
    assert isinstance(client_alias, ElevenLabsClient)


def test_get_tts_client_elevenlabs_routing() -> None:
    # When language is English, returns ElevenLabsClient
    client_en = get_tts_client("elevenlabs", language="en")
    assert isinstance(client_en, ElevenLabsClient)

    # When language is Amharic, ElevenLabs does not support Amharic -> routes to AddisAIClient
    client_am = get_tts_client("elevenlabs", language="am")
    assert isinstance(client_am, AddisAIClient)


# 3. ElevenLabsClient TTS Synthesis Tests
@pytest.mark.asyncio
async def test_elevenlabs_synthesize_speech_english_success() -> None:
    client = ElevenLabsClient()
    client.settings.elevenlabs_api_key = "test_xi_key"
    client.settings.elevenlabs_api_base_url = "https://api.elevenlabs.io"
    client.settings.elevenlabs_voice_id = "21m00Tcm4TlvDq8ikWAM"
    client.settings.elevenlabs_model_id = "eleven_multilingual_v2"

    mock_audio_bytes = b"ELEVENLABS_TTS_MP3_STREAM"

    def mock_post(url, headers=None, json=None):
        assert "v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" in str(url)
        assert headers.get("xi-api-key") == "test_xi_key"
        assert headers.get("Accept") == "audio/mpeg"
        assert json.get("text") == "Please describe your symptoms"
        assert json.get("model_id") == "eleven_multilingual_v2"
        return httpx.Response(200, content=mock_audio_bytes, request=httpx.Request("POST", str(url)))

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(side_effect=mock_post)):
        result = await client.synthesize_speech("Please describe your symptoms", language="en")

    assert result == mock_audio_bytes


@pytest.mark.asyncio
async def test_elevenlabs_synthesize_speech_fallback_on_missing_key() -> None:
    client = ElevenLabsClient()
    client.settings.elevenlabs_api_key = ""  # No key configured

    result = await client.synthesize_speech("Hello pregnant mother", language="en")
    assert isinstance(result, bytes)
    assert len(result) > 0  # Generated via gTTS fallback


@pytest.mark.asyncio
async def test_elevenlabs_synthesize_speech_fallback_on_http_error() -> None:
    client = ElevenLabsClient()
    client.settings.elevenlabs_api_key = "test_xi_key"

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(side_effect=httpx.ConnectError("Connection refused"))):
        result = await client.synthesize_speech("Hello there", language="en")

    assert isinstance(result, bytes)
    assert len(result) > 0  # Fallback to gTTS succeeded


@pytest.mark.asyncio
async def test_elevenlabs_synthesize_speech_amharic_safeguard() -> None:
    client = ElevenLabsClient()
    mock_addis_audio = b"ADDIS_AI_AMHARIC_AUDIO"

    with patch.object(client.addis_client, "synthesize_speech", new=AsyncMock(return_value=mock_addis_audio)) as mock_addis:
        result = await client.synthesize_speech("ጤና ይስጥልኝ", language="am")

    mock_addis.assert_called_once_with("ጤና ይስጥልኝ", voice_id=None, language="am")
    assert result == mock_addis_audio


# 4. ElevenLabsClient Scribe STT Transcription Tests
@pytest.mark.asyncio
async def test_elevenlabs_transcribe_english_success() -> None:
    client = ElevenLabsClient()
    client.settings.elevenlabs_api_key = "test_xi_key"
    client.settings.elevenlabs_api_base_url = "https://api.elevenlabs.io"
    client.settings.elevenlabs_stt_model_id = "scribe_v1"

    def mock_post(url, headers=None, files=None, data=None):
        assert "v1/speech-to-text" in str(url)
        assert headers.get("xi-api-key") == "test_xi_key"
        assert data.get("model_id") == "scribe_v1"
        assert data.get("language_code") == "en"
        assert "file" in files
        return httpx.Response(
            200,
            json={"text": "I have a mild headache", "language_code": "en"},
            request=httpx.Request("POST", str(url)),
        )

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(side_effect=mock_post)):
        transcript = await client.transcribe(
            audio_bytes=b"fake_voice",
            filename="voice.wav",
            content_type="audio/wav",
            language="en",
        )

    assert transcript == "I have a mild headache"


@pytest.mark.asyncio
async def test_elevenlabs_transcribe_missing_key_raises() -> None:
    client = ElevenLabsClient()
    client.settings.elevenlabs_api_key = ""

    with pytest.raises(RuntimeError, match="ELEVENLABS_API_KEY is not configured"):
        await client.transcribe(b"fake_voice", language="en")


@pytest.mark.asyncio
async def test_elevenlabs_transcribe_amharic_safeguard() -> None:
    client = ElevenLabsClient()

    with patch.object(client.addis_client, "transcribe", new=AsyncMock(return_value="ራስ ምታት አለኝ")) as mock_addis:
        res = await client.transcribe(b"audio", filename="test.wav", content_type="audio/wav", language="am")

    mock_addis.assert_called_once_with(b"audio", "test.wav", "audio/wav", language="am")
    assert res == "ራስ ምታት አለኝ"


# 5. CheckInSessionService Integration with ElevenLabs
@pytest.mark.asyncio
async def test_checkin_respond_elevenlabs_english() -> None:
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
         patch.object(ElevenLabsClient, "transcribe", new=AsyncMock(return_value="I feel tired today")) as mock_transcribe, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])) as mock_extract, \
         patch.object(service.sessions, "update"):

        await service.respond(
            user_id=session_id,
            session_id=session_id,
            audio_bytes=b"fake_audio",
            filename="voice.wav",
            content_type="audio/wav",
            model="elevenlabs",
        )

        mock_transcribe.assert_called_once_with(b"fake_audio", "voice.wav", "audio/wav", language="en")
        mock_extract.assert_called_once_with("I feel tired today", "symptoms", language="en")


@pytest.mark.asyncio
async def test_checkin_respond_elevenlabs_amharic_safeguard() -> None:
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
            model="elevenlabs",
        )

        # In Amharic sessions, ElevenLabs is safeguarded to Addis AI ASR
        mock_addis.assert_called_once_with(b"fake_audio", "voice.wav", "audio/wav", language="am")
        mock_extract.assert_called_once_with("ደህና ነኝ", "symptoms", language="am")


# 6. HTTP API Endpoint Tests
def test_api_tts_elevenlabs_get(test_client: TestClient) -> None:
    fake_audio = b"ELEVENLABS_GET_AUDIO"

    with patch.object(ElevenLabsClient, "synthesize_speech", new=AsyncMock(return_value=fake_audio)):
        res = test_client.get("/tts?text=Did%20you%20take%20iron&model=elevenlabs&language=en")
        assert res.status_code == 200
        assert res.content == fake_audio


def test_api_tts_elevenlabs_post(test_client: TestClient) -> None:
    fake_audio = b"ELEVENLABS_POST_AUDIO"

    with patch.object(ElevenLabsClient, "synthesize_speech", new=AsyncMock(return_value=fake_audio)):
        res = test_client.post(
            "/tts",
            json={
                "text": "Did you take iron today?",
                "model": "elevenlabs",
                "language": "en",
            },
        )
        assert res.status_code == 200
        assert res.content == fake_audio
