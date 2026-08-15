import json
from unittest.mock import AsyncMock, patch

import pytest

from app.services.extraction import ExtractionService, _parse_json_response


def test_parse_json_response_strips_markdown_fence() -> None:
    raw = '```json\n{"symptoms":[]}\n```'
    assert _parse_json_response(raw) == {"symptoms": []}


@pytest.mark.asyncio
async def test_extraction_validates_symptoms_and_sets_danger_sign() -> None:
    service = ExtractionService()
    llm_payload = {
        "symptoms": [
            {
                "raw_text": "ከባድ ራስ ምታት",
                "category": "severe_headache",
                "duration": {"value": 1, "unit": "day"},
                "severity": "severe",
            }
        ]
    }

    with patch.object(
        service.client,
        "generate_json",
        new=AsyncMock(return_value=json.dumps(llm_payload)),
    ):
        items = await service.extract("ከባድ ራስ ምታት", "symptoms")

    assert len(items) == 1
    assert items[0]["danger_sign"] is True
    assert items[0]["confirmed"] is False
    assert "item_id" in items[0]
    assert "verification_phrase" in items[0]
    assert "ከባድ ራስ ምታት" in items[0]["verification_phrase"]
    assert "1 ቀን" in items[0]["verification_phrase"]


@pytest.mark.asyncio
async def test_extraction_retries_on_invalid_json() -> None:
    service = ExtractionService()
    mock = AsyncMock(side_effect=["not-json", '{"symptoms":[]}'])
    with patch.object(service.client, "generate_json", new=mock):
        items = await service.extract("ምንም", "symptoms")
    assert items == []
    assert mock.await_count == 2


@pytest.mark.asyncio
async def test_extraction_raises_after_max_retries() -> None:
    service = ExtractionService()
    with patch.object(
        service.client,
        "generate_json",
        new=AsyncMock(return_value="not-json"),
    ):
        with pytest.raises(ValueError):
            await service.extract("test", "symptoms")
