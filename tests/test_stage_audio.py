from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.constants import CHECKIN_STAGE_METADATA, STAGE_PROMPTS
from app.main import app
from app.services.checkin_session import CheckInSessionService
from app.services.stage_audio import (
    _STAGE_AUDIO_BYTE_CACHE,
    get_or_synthesize_stage_audio,
)


def test_stage_prompts_match_frontend_spec() -> None:
    assert (
        STAGE_PROMPTS["symptoms"]
        == "ዛሬ ጽኑ ራስ ምታት፣ የዓይን ብዥታ፣ ደም መፍሰስ፣ ፈሳሽ መፍሰስ ወይም ከፍተኛ የሆድ ህመም ተሰምቶዎታል?"
    )
    assert (
        STAGE_PROMPTS["food"]
        == "ዛሬ ምን ምን አይነት ምግቦችን ተመገቡ? ቢያንስ አንድ ተጨማሪ የተመጣጠነ ምግብ ወስደዋል?"
    )
    assert (
        STAGE_PROMPTS["supplement"]
        == "የዛሬውን የብረት እና ፎሊክ አሲድ (IFA) ወይም የካልሲየም እንክብል ወስደዋል?"
    )
    assert STAGE_PROMPTS["closing"] == "ሌላ የሚያስጨንቅዎት ማንኛውም የጤና ለውጥ፣ ህመም ወይም ጥያቄ አለዎት?"

    assert CHECKIN_STAGE_METADATA["symptoms"]["category_am"] == "የአደጋ ምልክቶች እና ህመም"
    assert (
        CHECKIN_STAGE_METADATA["symptoms"]["category_en"] == "DANGER SIGNS & SYMPTOMS"
    )


@pytest.mark.asyncio
async def test_stored_stage_audio_is_cached_without_provider_calls():
    _STAGE_AUDIO_BYTE_CACHE.clear()
    with (
        patch("app.services.stage_audio.get_supabase_client") as storage,
        patch(
            "app.services.stage_audio.AddisAIClient.synthesize_speech",
            new_callable=AsyncMock,
        ) as synth,
    ):
        storage.return_value.storage.from_.return_value.download.return_value = (
            b"ID3stored audio"
        )
        assert await get_or_synthesize_stage_audio("symptoms") == b"ID3stored audio"
        assert await get_or_synthesize_stage_audio("symptoms") == b"ID3stored audio"
        storage.return_value.storage.from_.return_value.download.assert_called_once()
        synth.assert_not_called()
    _STAGE_AUDIO_BYTE_CACHE.clear()


@pytest.mark.asyncio
async def test_missing_generic_audio_does_not_trigger_provider():
    _STAGE_AUDIO_BYTE_CACHE.clear()
    with (
        patch("app.services.stage_audio.get_supabase_client") as storage,
        patch(
            "app.services.stage_audio.AddisAIClient.synthesize_speech",
            new_callable=AsyncMock,
        ) as synth,
    ):
        storage.return_value.storage.from_.return_value.download.return_value = b""
        with pytest.raises(RuntimeError, match="not provisioned"):
            await get_or_synthesize_stage_audio("symptoms")
        synth.assert_not_called()


@pytest.mark.asyncio
async def test_storage_download_does_not_block_event_loop():
    import asyncio
    import threading

    from app.services.stage_audio import prompt_path

    _STAGE_AUDIO_BYTE_CACHE.clear()
    started, release = threading.Event(), threading.Event()

    def download(_):
        started.set()
        assert release.wait(2)
        return b"ID3stored"

    with patch("app.services.stage_audio.get_supabase_client") as storage:
        storage.return_value.storage.from_.return_value.download.side_effect = download
        task = asyncio.create_task(get_or_synthesize_stage_audio("symptoms"))
        for _ in range(100):
            if started.is_set():
                break
            await asyncio.sleep(0.005)
        assert started.is_set() and not task.done()
        release.set()
        assert await task == b"ID3stored"
    assert prompt_path("symptoms").count("/") == 2
    _STAGE_AUDIO_BYTE_CACHE.clear()


def test_checkin_prompts_endpoint() -> None:
    client = TestClient(app)
    resp = client.get("/checkin/prompts")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 4
    stages = [d["stage"] for d in data]
    assert stages == ["symptoms", "food", "supplement", "closing"]
    assert "symptoms" in data[0]["audio_url"]


@pytest.mark.asyncio
async def test_generic_cache_has_entry_bound_and_project_separation(monkeypatch):
    from app.config import get_settings
    from app.services import stage_audio

    _STAGE_AUDIO_BYTE_CACHE.clear()
    with patch("app.services.stage_audio.get_supabase_client") as storage:
        storage.return_value.storage.from_.return_value.download.return_value = (
            b"ID3stored"
        )
        for n in range(6):
            settings = get_settings().model_copy(
                update={"supabase_url": f"https://project-{n}.example.org"}
            )
            monkeypatch.setattr(
                stage_audio, "get_settings", lambda settings=settings: settings
            )
            await get_or_synthesize_stage_audio("symptoms")
        assert storage.return_value.storage.from_.return_value.download.call_count == 6
        assert len(_STAGE_AUDIO_BYTE_CACHE) == 4
    _STAGE_AUDIO_BYTE_CACHE.clear()


def test_checkin_prompt_audio_endpoint() -> None:
    client = TestClient(app)

    with patch(
        "app.api.routes.checkin.get_or_synthesize_stage_audio", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = b"MOCK_AUDIO_PAYLOAD"

        resp = client.get("/checkin/prompts/symptoms/audio")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "audio/mpeg"
        assert resp.content == b"MOCK_AUDIO_PAYLOAD"


def test_start_session_returns_static_stage_audio_url(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.db.idempotency.execute", lambda uid, op, key, payload, action: action()
    )
    service = CheckInSessionService()
    user_id = uuid4()

    with (
        patch.object(service.check_ins, "has_food_logged_today", return_value=False),
        patch.object(
            service.check_ins, "has_supplement_logged_today", return_value=False
        ),
        patch.object(service.supplements, "list_active", return_value=[]),
        patch.object(
            service.sessions,
            "create",
            return_value={
                "id": str(uuid4()),
                "version": 0,
                "stage_status": "awaiting_response",
            },
        ),
    ):
        res = service.start_session(user_id)
        assert res["stage"] == "symptoms"
        assert "symptoms" in res["question_audio_url"]
