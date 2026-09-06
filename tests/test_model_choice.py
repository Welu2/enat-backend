import io
from unittest.mock import AsyncMock, patch
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient

from app.api.routes.checkin import get_current_user_id
from app.main import app
from app.services.addis_ai import AddisAIClient
from app.services.checkin_session import CheckInSessionService
from app.services.gemini import GeminiTranscribeClient
from app.services.sahara import SaharaVoiceClient


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_user_id() -> str:
    return str(uuid4())


@pytest.mark.asyncio
async def test_checkin_service_respond_defaults_to_addisai() -> None:
    service = CheckInSessionService()
    session = {
        "id": uuid4(),
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "food", "closing"],
        "draft_data": {"symptoms": []},
        "pending_items": [],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session), \
         patch.object(AddisAIClient, "transcribe", new=AsyncMock(return_value="addisai transcript")) as mock_addis, \
         patch.object(SaharaVoiceClient, "transcribe", new=AsyncMock(return_value="sahara transcript")) as mock_sahara, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])), \
         patch.object(service.sessions, "update"):
        res = await service.respond(session["id"], session["id"], b"audio", "file.wav", "audio/wav")
        assert mock_addis.called
        assert not mock_sahara.called
        assert res["transcript"] == "addisai transcript"


@pytest.mark.asyncio
async def test_checkin_service_respond_routes_to_sahara_when_specified() -> None:
    service = CheckInSessionService()
    session = {
        "id": uuid4(),
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "food", "closing"],
        "draft_data": {"symptoms": []},
        "pending_items": [],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session), \
         patch.object(AddisAIClient, "transcribe", new=AsyncMock(return_value="addisai transcript")) as mock_addis, \
         patch.object(SaharaVoiceClient, "transcribe", new=AsyncMock(return_value="sahara transcript")) as mock_sahara, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])), \
         patch.object(service.sessions, "update"):
        res = await service.respond(session["id"], session["id"], b"audio", "file.wav", "audio/wav", model="sahara")
        assert not mock_addis.called
        assert mock_sahara.called
        assert res["transcript"] == "sahara transcript"


@pytest.mark.asyncio
async def test_checkin_service_voice_correct_routes_to_sahara() -> None:
    service = CheckInSessionService()
    item_id = str(uuid4())
    session = {
        "id": uuid4(),
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "food", "closing"],
        "draft_data": {"symptoms": []},
        "pending_items": [{"item_id": item_id, "raw_text": "old", "category": None}],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session), \
         patch.object(SaharaVoiceClient, "transcribe", new=AsyncMock(return_value="sahara corrected")) as mock_sahara, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])), \
         patch.object(service.sessions, "update"):
        res = await service.voice_correct_item(session["id"], session["id"], item_id, b"audio", "file.wav", "audio/wav", model="sahara")
        assert mock_sahara.called
        assert res["correction_transcript"] == "sahara corrected"


def test_api_checkin_respond_passes_model_form_data(test_client: TestClient, mock_user_id: str) -> None:
    app.dependency_overrides[get_current_user_id] = lambda: uuid4()
    session_id = uuid4()
    audio_file = io.BytesIO(b"fake audio data")

    with patch("app.api.routes.checkin.CheckInSessionService.respond", new=AsyncMock(return_value={
        "session_id": session_id,
        "stage": "symptoms",
        "transcript": "mock transcript",
        "pending_items": [],
    })) as mock_respond:
        response = test_client.post(
            f"/checkin/{session_id}/respond",
            files={"audio": ("sample.wav", audio_file, "audio/wav")},
            data={"model": "sahara"},
        )
        assert response.status_code == 200
        assert mock_respond.called
        assert mock_respond.call_args.kwargs["model"] == "sahara"

    app.dependency_overrides.clear()


def test_api_checkin_respond_passes_model_query_param(test_client: TestClient) -> None:
    app.dependency_overrides[get_current_user_id] = lambda: uuid4()
    session_id = uuid4()
    audio_file = io.BytesIO(b"fake audio data")

    with patch("app.api.routes.checkin.CheckInSessionService.respond", new=AsyncMock(return_value={
        "session_id": session_id,
        "stage": "symptoms",
        "transcript": "mock transcript",
        "pending_items": [],
    })) as mock_respond:
        response = test_client.post(
            f"/checkin/{session_id}/respond?model=sahara",
            files={"audio": ("sample.wav", audio_file, "audio/wav")},
        )
        assert response.status_code == 200
        assert mock_respond.called
        assert mock_respond.call_args.kwargs["model"] == "sahara"

    app.dependency_overrides.clear()


def test_api_tts_routes_to_sahara_on_get(test_client: TestClient) -> None:
    with patch.object(SaharaVoiceClient, "synthesize_speech", new=AsyncMock(return_value=b"sahara_audio")) as mock_synth:
        response = test_client.get("/tts?text=ሰላም&model=sahara")
        assert response.status_code == 200
        assert response.content == b"sahara_audio"
        assert mock_synth.called


def test_api_tts_routes_to_sahara_on_post(test_client: TestClient) -> None:
    with patch.object(SaharaVoiceClient, "synthesize_speech", new=AsyncMock(return_value=b"sahara_post_audio")) as mock_synth:
        response = test_client.post("/tts", json={"text": "ሰላም", "model": "sahara"})
        assert response.status_code == 200
        assert response.content == b"sahara_post_audio"
        assert mock_synth.called


def test_api_dev_asr_test_routes_to_sahara(test_client: TestClient) -> None:
    audio_file = io.BytesIO(b"fake dev audio")
    with patch.object(SaharaVoiceClient, "transcribe", new=AsyncMock(return_value="dev sahara ok")) as mock_transcribe:
        response = test_client.post(
            "/dev/asr-test",
            files={"audio": ("dev.wav", audio_file, "audio/wav")},
            data={"model": "sahara"},
        )
        assert response.status_code == 200
        assert response.json()["transcript"] == "dev sahara ok"
        assert response.json()["model"] == "sahara"
        assert mock_transcribe.called


@pytest.mark.asyncio
async def test_checkin_service_respond_routes_to_gemini() -> None:
    service = CheckInSessionService()
    session = {
        "id": uuid4(),
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "food", "closing"],
        "draft_data": {"symptoms": []},
        "pending_items": [],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session), \
         patch.object(AddisAIClient, "transcribe", new=AsyncMock(return_value="addisai transcript")) as mock_addis, \
         patch.object(GeminiTranscribeClient, "transcribe", new=AsyncMock(return_value="gemini transcript")) as mock_gemini, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])), \
         patch.object(service.sessions, "update"):
        res = await service.respond(session["id"], session["id"], b"audio", "file.wav", "audio/wav", model="gemini")
        assert not mock_addis.called
        assert mock_gemini.called
        assert res["transcript"] == "gemini transcript"


@pytest.mark.asyncio
async def test_checkin_service_voice_correct_routes_to_gemini() -> None:
    service = CheckInSessionService()
    item_id = str(uuid4())
    session = {
        "id": uuid4(),
        "current_stage": "symptoms",
        "stage_order": ["symptoms", "food", "closing"],
        "draft_data": {"symptoms": []},
        "pending_items": [{"item_id": item_id, "raw_text": "old", "category": None}],
        "status": "in_progress",
        "expires_at": "2099-01-01T00:00:00",
    }

    with patch.object(service, "_get_active_session", return_value=session), \
         patch.object(GeminiTranscribeClient, "transcribe", new=AsyncMock(return_value="gemini corrected")) as mock_gemini, \
         patch.object(service.extraction, "extract", new=AsyncMock(return_value=[])), \
         patch.object(service.sessions, "update"):
        res = await service.voice_correct_item(session["id"], session["id"], item_id, b"audio", "file.wav", "audio/wav", model="gemini")
        assert mock_gemini.called
        assert res["correction_transcript"] == "gemini corrected"


def test_api_dev_asr_test_routes_to_gemini(test_client: TestClient) -> None:
    audio_file = io.BytesIO(b"fake dev audio")
    with patch.object(GeminiTranscribeClient, "transcribe", new=AsyncMock(return_value="dev gemini ok")) as mock_transcribe:
        response = test_client.post(
            "/dev/asr-test",
            files={"audio": ("dev.wav", audio_file, "audio/wav")},
            data={"model": "gemini"},
        )
        assert response.status_code == 200
        assert response.json()["transcript"] == "dev gemini ok"
        assert response.json()["model"] == "gemini"
        assert mock_transcribe.called


@pytest.mark.asyncio
async def test_addisai_transcribe_accepts_language_parameter() -> None:
    import httpx
    client = AddisAIClient()
    client.settings.addis_api_key = "test_key"
    client.settings.addis_api_base_url = "https://api.addisassistant.com"

    def mock_post(url, headers=None, files=None, data=None):
        import json
        assert "api/v2/stt" in str(url)
        assert headers.get("x-api-key") == "test_key"
        req_data = json.loads(data["request_data"])
        assert req_data["language_code"] == "am"
        return httpx.Response(200, json={"data": {"transcription": "ደህና ነኝ"}}, request=httpx.Request("POST", str(url)))

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(side_effect=mock_post)):
        res = await client.transcribe(
            audio_bytes=b"fake_bytes",
            filename="voice.wav",
            content_type="audio/wav",
            language="am",
        )
    assert res == "ደህና ነኝ"


