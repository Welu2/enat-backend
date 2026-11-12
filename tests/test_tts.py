from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.core.errors import ProviderUnavailable
from app.services.addis_ai import AddisAIClient


@pytest.mark.asyncio
async def test_addis_ai_synthesize_speech_success():
    response = httpx.Response(
        200, headers={"content-type": "audio/mpeg"}, content=b"ID3dummy_mp3_bytes"
    )
    with patch(
        "app.services.provider_runtime.ProviderRuntime.request",
        new=AsyncMock(return_value=response),
    ):
        assert await AddisAIClient().synthesize_speech("ሰላም") == b"ID3dummy_mp3_bytes"


@pytest.mark.asyncio
async def test_tts_rejects_json_success_and_never_falls_back():
    response = httpx.Response(200, json={"error": "private patient text"})
    with patch(
        "app.services.provider_runtime.ProviderRuntime.request",
        new=AsyncMock(return_value=response),
    ) as request:
        with pytest.raises(ProviderUnavailable, match="Invalid provider audio"):
            await AddisAIClient().synthesize_speech("private patient text")
        assert request.await_count == 1
