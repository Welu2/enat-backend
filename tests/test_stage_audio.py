from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.constants import CHECKIN_STAGE_METADATA, STAGE_PROMPTS
from app.main import app
from app.services.checkin_session import CheckInSessionService
from app.services.stage_audio import _STAGE_AUDIO_BYTE_CACHE, get_or_synthesize_stage_audio


def test_stage_prompts_match_frontend_spec() -> None:
    assert STAGE_PROMPTS["symptoms"] == "ዛሬ ጽኑ ራስ ምታት፣ የዓይን ብዥታ፣ ደም መፍሰስ፣ ፈሳሽ መፍሰስ ወይም ከፍተኛ የሆድ ህመም ተሰምቶዎታል?"
    assert STAGE_PROMPTS["food"] == "ዛሬ ምን ምን አይነት ምግቦችን ተመገቡ? ቢያንስ አንድ ተጨማሪ የተመጣጠነ ምግብ ወስደዋል?"
    assert STAGE_PROMPTS["supplement"] == "የዛሬውን የብረት እና ፎሊክ አሲድ (IFA) ወይም የካልሲየም እንክብል ወስደዋል?"
    assert STAGE_PROMPTS["closing"] == "ሌላ የሚያስጨንቅዎት ማንኛውም የጤና ለውጥ፣ ህመም ወይም ጥያቄ አለዎት?"

    assert CHECKIN_STAGE_METADATA["symptoms"]["category_am"] == "የአደጋ ምልክቶች እና ህመም"
    assert CHECKIN_STAGE_METADATA["symptoms"]["category_en"] == "DANGER SIGNS & SYMPTOMS"


@pytest.mark.asyncio
async def test_get_or_synthesize_stage_audio_caches_result() -> None:
    _STAGE_AUDIO_BYTE_CACHE.clear()

    fake_mp3 = b"FAKE_MP3_AUDIO_STREAM_BYTES"

    with patch("app.services.stage_audio.AddisAIClient.synthesize_speech", new_callable=AsyncMock) as mock_synth, \
         patch("app.services.stage_audio.get_supabase_client") as mock_db:
        mock_synth.return_value = fake_mp3
        mock_db.return_value.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = None

        # First call: calls synthesize
        audio_1 = await get_or_synthesize_stage_audio("symptoms")
        assert audio_1 == fake_mp3
        assert mock_synth.call_count == 1

        # Second call: uses cache, does not call synthesize again
        audio_2 = await get_or_synthesize_stage_audio("symptoms")
        assert audio_2 == fake_mp3
        assert mock_synth.call_count == 1  # Still 1, 0 redundant TTS calls!


def test_checkin_prompts_endpoint() -> None:
    client = TestClient(app)
    resp = client.get("/checkin/prompts")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 4
    stages = [d["stage"] for d in data]
    assert stages == ["symptoms", "food", "supplement", "closing"]
    assert "symptoms" in data[0]["audio_url"]


def test_checkin_prompt_audio_endpoint() -> None:
    client = TestClient(app)

    with patch("app.api.routes.checkin.get_or_synthesize_stage_audio", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = b"MOCK_AUDIO_PAYLOAD"

        resp = client.get("/checkin/prompts/symptoms/audio")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "audio/mpeg"
        assert resp.content == b"MOCK_AUDIO_PAYLOAD"


def test_start_session_returns_static_stage_audio_url() -> None:
    service = CheckInSessionService()
    user_id = uuid4()

    with patch.object(service.check_ins, "has_food_logged_today", return_value=False), \
         patch.object(service.check_ins, "has_supplement_logged_today", return_value=False), \
         patch.object(service.supplements, "list_active", return_value=[]), \
         patch.object(service.sessions, "create", return_value={"id": str(uuid4())}):

        res = service.start_session(user_id)
        assert res["stage"] == "symptoms"
        assert "symptoms" in res["question_audio_url"]
