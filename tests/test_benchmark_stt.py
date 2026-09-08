import io
from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.addis_ai import AddisAIClient
from app.services.deepgram import DeepgramClient
from app.services.gemini import GeminiTranscribeClient
from app.services.sahara import SaharaVoiceClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_benchmark_stt_amharic_batch(client: TestClient) -> None:
    """Test Amharic batch executes Sahara, Addis AI, and Gemini sequentially with correct results."""
    mock_sahara = AsyncMock(return_value="ሰሃራ ጽሑፍ")
    mock_addis = AsyncMock(return_value="አዲስ አይ ጽሑፍ")
    mock_gemini = AsyncMock(return_value="ጀሚናይ ጽሑፍ")

    files = [
        ("files", ("audio1.wav", io.BytesIO(b"dummy audio 1"), "audio/wav")),
        ("files", ("audio2.wav", io.BytesIO(b"dummy audio 2"), "audio/wav")),
    ]

    with patch.object(SaharaVoiceClient, "transcribe", mock_sahara), \
         patch.object(AddisAIClient, "transcribe", mock_addis), \
         patch.object(GeminiTranscribeClient, "transcribe", mock_gemini):
        
        response = client.post(
            "/dev/benchmark-stt",
            files=files,
            data={"language_code": "am", "stage_label": "symptoms"},
        )

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2

    # Check first file
    res1 = data["results"][0]
    assert res1["filename"] == "audio1.wav"
    assert res1["stage_label"] == "symptoms"
    models1 = res1["models"]
    assert "sahara" in models1
    assert "addis_ai" in models1
    assert "gemini" in models1
    assert "deepgram" not in models1

    assert models1["sahara"]["hypothesis_text"] == "ሰሃራ ጽሑፍ"
    assert isinstance(models1["sahara"]["latency_seconds"], float)
    assert models1["addis_ai"]["hypothesis_text"] == "አዲስ አይ ጽሑፍ"
    assert isinstance(models1["addis_ai"]["latency_seconds"], float)
    assert models1["gemini"]["hypothesis_text"] == "ጀሚናይ ጽሑፍ"
    assert isinstance(models1["gemini"]["latency_seconds"], float)

    # Check second file
    res2 = data["results"][1]
    assert res2["filename"] == "audio2.wav"
    assert res2["stage_label"] == "symptoms"
    assert res2["models"]["sahara"]["hypothesis_text"] == "ሰሃራ ጽሑፍ"

    assert mock_sahara.call_count == 2
    assert mock_addis.call_count == 2
    assert mock_gemini.call_count == 2


def test_benchmark_stt_english_batch(client: TestClient) -> None:
    """Test English batch executes Sahara, Deepgram, and Gemini (swapping Addis AI for Deepgram)."""
    mock_sahara = AsyncMock(return_value="Sahara English transcript")
    mock_deepgram = AsyncMock(return_value="Deepgram English transcript")
    mock_gemini = AsyncMock(return_value="Gemini English transcript")

    files = [
        ("files", ("en_voice_01.wav", io.BytesIO(b"english audio bytes"), "audio/wav")),
    ]

    with patch.object(SaharaVoiceClient, "transcribe", mock_sahara), \
         patch.object(DeepgramClient, "transcribe", mock_deepgram), \
         patch.object(GeminiTranscribeClient, "transcribe", mock_gemini):
        
        response = client.post(
            "/dev/benchmark-stt",
            files=files,
            data={"language_code": "en", "stage_label": "supplement"},
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1

    item = data["results"][0]
    assert item["filename"] == "en_voice_01.wav"
    assert item["stage_label"] == "supplement"
    models = item["models"]
    assert "sahara" in models
    assert "deepgram" in models
    assert "gemini" in models
    assert "addis_ai" not in models

    assert models["sahara"]["hypothesis_text"] == "Sahara English transcript"
    assert models["deepgram"]["hypothesis_text"] == "Deepgram English transcript"
    assert models["gemini"]["hypothesis_text"] == "Gemini English transcript"


def test_benchmark_stt_defaults_stage_label_to_symptoms(client: TestClient) -> None:
    """When stage_label is omitted, it defaults to 'symptoms'."""
    mock_sahara = AsyncMock(return_value="text")
    mock_addis = AsyncMock(return_value="text")
    mock_gemini = AsyncMock(return_value="text")

    files = [
        ("files", ("test.wav", io.BytesIO(b"audio"), "audio/wav")),
    ]

    with patch.object(SaharaVoiceClient, "transcribe", mock_sahara), \
         patch.object(AddisAIClient, "transcribe", mock_addis), \
         patch.object(GeminiTranscribeClient, "transcribe", mock_gemini):
        
        response = client.post(
            "/dev/benchmark-stt",
            files=files,
        )

    assert response.status_code == 200
    data = response.json()
    assert data["results"][0]["stage_label"] == "symptoms"


def test_benchmark_stt_query_params_support(client: TestClient) -> None:
    """Supports language_code and stage_label passed as query parameters."""
    mock_sahara = AsyncMock(return_value="Sahara text")
    mock_deepgram = AsyncMock(return_value="Deepgram text")
    mock_gemini = AsyncMock(return_value="Gemini text")

    files = [
        ("files", ("test.wav", io.BytesIO(b"audio"), "audio/wav")),
    ]

    with patch.object(SaharaVoiceClient, "transcribe", mock_sahara), \
         patch.object(DeepgramClient, "transcribe", mock_deepgram), \
         patch.object(GeminiTranscribeClient, "transcribe", mock_gemini):
        
        response = client.post(
            "/dev/benchmark-stt?language_code=en&stage_label=food",
            files=files,
        )

    assert response.status_code == 200
    data = response.json()
    assert data["results"][0]["stage_label"] == "food"
    assert "deepgram" in data["results"][0]["models"]


def test_benchmark_stt_error_resilience_preserves_latency(client: TestClient) -> None:
    """If one model fails (e.g. rate limit / network error), record error and latency, and don't fail batch."""
    mock_sahara = AsyncMock(return_value="Sahara succeeded")
    mock_addis = AsyncMock(side_effect=RuntimeError("Addis AI API rate limited 429"))
    mock_gemini = AsyncMock(return_value="Gemini succeeded")

    files = [
        ("files", ("voice.wav", io.BytesIO(b"audio"), "audio/wav")),
    ]

    with patch.object(SaharaVoiceClient, "transcribe", mock_sahara), \
         patch.object(AddisAIClient, "transcribe", mock_addis), \
         patch.object(GeminiTranscribeClient, "transcribe", mock_gemini):
        
        response = client.post(
            "/dev/benchmark-stt",
            files=files,
            data={"language_code": "am"},
        )

    assert response.status_code == 200
    data = response.json()
    models = data["results"][0]["models"]

    # Sahara succeeded
    assert models["sahara"]["hypothesis_text"] == "Sahara succeeded"
    assert "error" not in models["sahara"]

    # Addis AI failed with recorded error and latency
    assert "error" in models["addis_ai"]
    assert "Addis AI API rate limited 429" in models["addis_ai"]["error"]
    assert "latency_seconds" in models["addis_ai"]
    assert isinstance(models["addis_ai"]["latency_seconds"], float)

    # Gemini still ran and succeeded
    assert models["gemini"]["hypothesis_text"] == "Gemini succeeded"
    assert "error" not in models["gemini"]


def test_benchmark_stt_filter_models(client: TestClient) -> None:
    """When models='gemini' is passed, only Gemini is called; Sahara and Addis AI are skipped."""
    mock_sahara = AsyncMock(return_value="Sahara")
    mock_addis = AsyncMock(return_value="Addis")
    mock_gemini = AsyncMock(return_value="Gemini only")

    files = [
        ("files", ("voice.wav", io.BytesIO(b"audio"), "audio/wav")),
    ]

    with patch.object(SaharaVoiceClient, "transcribe", mock_sahara), \
         patch.object(AddisAIClient, "transcribe", mock_addis), \
         patch.object(GeminiTranscribeClient, "transcribe", mock_gemini):
        
        response = client.post(
            "/dev/benchmark-stt",
            files=files,
            data={"language_code": "am", "models": "gemini"},
        )

    assert response.status_code == 200
    data = response.json()
    models = data["results"][0]["models"]

    assert "gemini" in models
    assert models["gemini"]["hypothesis_text"] == "Gemini only"
    assert "sahara" not in models
    assert "addis_ai" not in models
    assert mock_sahara.call_count == 0
    assert mock_addis.call_count == 0
    assert mock_gemini.call_count == 1
