import pytest
from unittest.mock import patch, MagicMock
import httpx

from app.services.speech import normalize_voice_model, get_asr_client, get_tts_client
from app.services.gemini import GeminiTranscribeClient
from app.services.addis_ai import AddisAIClient


def test_normalize_voice_model_gemini():
    assert normalize_voice_model("gemini") == "gemini"
    assert normalize_voice_model("google") == "gemini"
    assert normalize_voice_model("gemini-3.5-transcribe") == "gemini"
    assert normalize_voice_model("gemini_transcribe") == "gemini"
    assert normalize_voice_model("GEMINI") == "gemini"


def test_get_asr_client_gemini():
    client = get_asr_client("gemini")
    assert isinstance(client, GeminiTranscribeClient)


def test_get_tts_client_gemini_fallback():
    client = get_tts_client("gemini")
    assert isinstance(client, AddisAIClient)


@pytest.mark.asyncio
async def test_gemini_transcribe_missing_api_key():
    client = GeminiTranscribeClient()
    with patch.object(client.settings, "gemini_api_key", ""):
        with pytest.raises(RuntimeError, match="GEMINI_API_KEY is not configured"):
            await client.transcribe(b"dummy audio", "audio.wav", "audio/wav")


@pytest.mark.asyncio
async def test_gemini_transcribe_primary_interactions_flow():
    client = GeminiTranscribeClient()

    async def mock_handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        if "/upload/v1beta/files" in url_str:
            return httpx.Response(
                200,
                headers={"x-goog-upload-url": "https://upload.test/session-123"},
                json={"file": {}},
            )
        elif "https://upload.test/session-123" in url_str:
            return httpx.Response(
                200,
                json={
                    "file": {
                        "name": "files/sample123",
                        "uri": "https://generativelanguage.googleapis.com/v1beta/files/sample123",
                    }
                },
            )
        elif "/v1beta/interactions" in url_str:
            return httpx.Response(
                200,
                json={
                    "status": "completed",
                    "steps": [
                        {
                            "id": "step_001",
                            "type": "model_output",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "ከፍተኛ ራስ ምታት አለብኝ",
                                }
                            ],
                        }
                    ],
                },
            )
        elif "/v1beta/files/sample123" in url_str:
            return httpx.Response(200, json={"status": "deleted"})
        return httpx.Response(404)

    transport = httpx.MockTransport(mock_handler)

    with patch.object(client.settings, "gemini_api_key", "test_gemini_key"):
        with patch("httpx.AsyncClient", return_value=httpx.AsyncClient(transport=transport)):
            result = await client.transcribe(b"audio-bytes-123", "sample.wav", "audio/wav")
            assert result == "ከፍተኛ ራስ ምታት አለብኝ"


@pytest.mark.asyncio
async def test_gemini_transcribe_output_text_field():
    client = GeminiTranscribeClient()

    async def mock_handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        if "/upload/v1beta/files" in url_str:
            return httpx.Response(
                200,
                headers={"x-goog-upload-url": "https://upload.test/session-456"},
                json={"file": {}},
            )
        elif "https://upload.test/session-456" in url_str:
            return httpx.Response(
                200,
                json={
                    "file": {
                        "name": "files/sample456",
                        "uri": "https://generativelanguage.googleapis.com/v1beta/files/sample456",
                    }
                },
            )
        elif "/v1beta/interactions" in url_str:
            return httpx.Response(
                200,
                json={
                    "status": "completed",
                    "output_text": "ደህና ነኝ ምንም ህመም የለም",
                },
            )
        elif "/v1beta/files/sample456" in url_str:
            return httpx.Response(200, json={"status": "deleted"})
        return httpx.Response(404)

    transport = httpx.MockTransport(mock_handler)

    with patch.object(client.settings, "gemini_api_key", "test_gemini_key"):
        with patch("httpx.AsyncClient", return_value=httpx.AsyncClient(transport=transport)):
            result = await client.transcribe(b"audio-bytes-456", "sample.wav", "audio/wav")
            assert result == "ደህና ነኝ ምንም ህመም የለም"


@pytest.mark.asyncio
async def test_gemini_transcribe_fallback_to_generate_content():
    client = GeminiTranscribeClient()

    async def mock_handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        if "/upload/v1beta/files" in url_str:
            # Files API fails
            return httpx.Response(500, text="Internal Files API error")
        elif "generateContent" in url_str:
            return httpx.Response(
                200,
                json={
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {"text": "የደም መፍሰስ አጋጥሞኛል"}
                                ]
                            }
                        }
                    ]
                },
            )
        return httpx.Response(404)

    transport = httpx.MockTransport(mock_handler)

    with patch.object(client.settings, "gemini_api_key", "test_gemini_key"):
        with patch("httpx.AsyncClient", return_value=httpx.AsyncClient(transport=transport)):
            result = await client.transcribe(b"audio-bytes-fallback", "sample.wav", "audio/wav")
            assert result == "የደም መፍሰስ አጋጥሞኛል"
