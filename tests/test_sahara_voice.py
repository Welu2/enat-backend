from unittest.mock import AsyncMock, patch
import httpx
import pytest

from app.services.addis_ai import AddisAIClient
from app.services.sahara import SaharaVoiceClient
from app.services.speech import (
    get_asr_client,
    get_tts_client,
    normalize_voice_model,
)


def test_normalize_voice_model() -> None:
    assert normalize_voice_model("addisai") == "addisai"
    assert normalize_voice_model("ADDISAI") == "addisai"
    assert normalize_voice_model(None) == "addisai"
    assert normalize_voice_model("") == "addisai"
    assert normalize_voice_model("sahara") == "sahara"
    assert normalize_voice_model("intron") == "sahara"
    assert normalize_voice_model("SAHARA_VOICE") == "sahara"


def test_speech_dispatcher_factories() -> None:
    assert isinstance(get_asr_client("addisai"), AddisAIClient)
    assert isinstance(get_asr_client("sahara"), SaharaVoiceClient)
    assert isinstance(get_asr_client("intron"), SaharaVoiceClient)

    assert isinstance(get_tts_client("addisai"), AddisAIClient)
    assert isinstance(get_tts_client("sahara"), SaharaVoiceClient)
    assert isinstance(get_tts_client("intron"), SaharaVoiceClient)


@pytest.mark.asyncio
async def test_sahara_asr_transcribe_success() -> None:
    client = SaharaVoiceClient()
    mock_resp = httpx.Response(
        200,
        json={
            "status": "Ok",
            "message": "file status found",
            "data": {
                "file_id": "test-123",
                "processing_status": "FILE_TRANSCRIBED",
                "audio_file_name": "sample.wav",
                "audio_transcript": "ከባድ ራስ ምታት አለኝ",
                "processed_audio_duration_in_seconds": 5,
            },
        },
        request=httpx.Request("POST", "https://infer.voice.intron.io/file/v1/upload/sync"),
    )

    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_resp)) as mock_post:
        transcript = await client.transcribe(b"dummy_wav_data", "sample.wav", "audio/wav")
        assert transcript == "ከባድ ራስ ምታት አለኝ"
        assert mock_post.called
        call_kwargs = mock_post.call_args.kwargs
        assert call_kwargs["data"]["use_language_asr_input"] == "am"
        assert call_kwargs["data"]["audio_file_name"] == "sample.wav"


@pytest.mark.asyncio
async def test_sahara_asr_transcribe_http_error() -> None:
    client = SaharaVoiceClient()
    mock_resp = httpx.Response(
        401,
        text="Unauthorized API key",
        request=httpx.Request("POST", "https://infer.voice.intron.io/file/v1/upload/sync"),
    )

    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_resp)):
        with pytest.raises(RuntimeError, match="Sahara ASR request failed"):
            await client.transcribe(b"dummy", "sample.wav")


@pytest.mark.asyncio
async def test_sahara_tts_synthesize_success() -> None:
    client = SaharaVoiceClient()
    mock_gen_resp = httpx.Response(
        200,
        json={
            "status": "Ok",
            "data": {
                "audio_path": "https://infer.voice.intron.io/storage/speech_123.wav",
                "audio_duration_in_seconds": 3,
                "processing_status": "TTS_TEXT_AUDIO_GENERATED",
            },
        },
        request=httpx.Request("POST", "https://infer.voice.intron.io/tts/v1/generate"),
    )
    mock_audio_resp = httpx.Response(
        200,
        content=b"RIFFdummywavbytes",
        request=httpx.Request("GET", "https://infer.voice.intron.io/storage/speech_123.wav"),
    )

    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_gen_resp)) as mock_post, \
         patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_audio_resp)) as mock_get:
        audio_bytes = await client.synthesize_speech("ሰላም እንደምን አላችሁ")
        assert audio_bytes == b"RIFFdummywavbytes"
        assert mock_post.called
        assert mock_get.called
        post_json = mock_post.call_args.kwargs["json"]
        assert post_json["voice_language"] == "am"
        assert post_json["voice_accent"] == "amharic"
        assert post_json["text"] == "ሰላም እንደምን አላችሁ"


@pytest.mark.asyncio
async def test_sahara_tts_synthesize_error_status() -> None:
    client = SaharaVoiceClient()
    mock_gen_resp = httpx.Response(
        200,
        json={
            "status": "Error",
            "message": "invalid text voice language",
            "data": {},
        },
        request=httpx.Request("POST", "https://infer.voice.intron.io/tts/v1/generate"),
    )

    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_gen_resp)):
        with pytest.raises(RuntimeError, match="Sahara TTS generation rejected"):
            await client.synthesize_speech("invalid")
