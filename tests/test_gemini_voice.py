import json
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
async def test_gemini_transcribe_amharic_success():
    client = GeminiTranscribeClient()

    async def mock_handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        assert "models/gemini-3.5-transcribe:generateContent" in url_str
        assert "key=test_gemini_key" in url_str
        body = json.loads(request.content)
        parts = body["contents"][0]["parts"]
        assert "Amharic" in parts[0]["text"]
        assert parts[1]["inline_data"]["mime_type"] == "audio/wav"
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {"text": "ከፍተኛ ራስ ምታት አለብኝ"}
                            ]
                        }
                    }
                ]
            },
        )

    transport = httpx.MockTransport(mock_handler)

    with patch.object(client.settings, "gemini_api_key", "test_gemini_key"):
        with patch("httpx.AsyncClient", return_value=httpx.AsyncClient(transport=transport)):
            result = await client.transcribe(
                b"audio-bytes-123", "sample.wav", "audio/wav", language="am", model="gemini-3.5-transcribe"
            )
            assert result == "ከፍተኛ ራስ ምታት አለብኝ"


@pytest.mark.asyncio
async def test_gemini_transcribe_english_success():
    client = GeminiTranscribeClient()

    async def mock_handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        assert ":generateContent" in url_str
        body = json.loads(request.content)
        parts = body["contents"][0]["parts"]
        assert "English" in parts[0]["text"]
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {"text": "I have severe headache"}
                            ]
                        }
                    }
                ]
            },
        )

    transport = httpx.MockTransport(mock_handler)

    with patch.object(client.settings, "gemini_api_key", "test_gemini_key"):
        with patch("httpx.AsyncClient", return_value=httpx.AsyncClient(transport=transport)):
            result = await client.transcribe(b"audio-bytes-english", "sample.wav", "audio/wav", language="en")
            assert result == "I have severe headache"


@pytest.mark.asyncio
async def test_gemini_transcribe_error_handling():
    client = GeminiTranscribeClient()

    async def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, text='{"error": {"code": 429, "message": "Resource exhausted"}}')

    transport = httpx.MockTransport(mock_handler)

    with patch.object(client.settings, "gemini_api_key", "test_gemini_key"):
        with patch("httpx.AsyncClient", return_value=httpx.AsyncClient(transport=transport)):
            with pytest.raises(RuntimeError, match="Gemini Transcribe request failed"):
                await client.transcribe(b"audio-bytes", "sample.wav", "audio/wav")

