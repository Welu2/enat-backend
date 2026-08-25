from unittest.mock import AsyncMock, patch
import pytest
from app.services.addis_ai import AddisAIClient


@pytest.mark.asyncio
async def test_addis_ai_synthesize_speech_success() -> None:
    client = AddisAIClient()
    dummy_audio = b"dummy_mp3_bytes"

    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "audio/mpeg"}
    mock_response.content = dummy_audio
    mock_response.raise_for_status = lambda: None

    with patch("httpx.AsyncClient.post", return_value=mock_response):
        audio = await client.synthesize_speech("ሰላም")

    assert audio == dummy_audio
