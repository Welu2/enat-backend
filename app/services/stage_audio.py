"""Only versioned, approved generic prompts enter this fixed-size public cache."""

import hashlib
from time import monotonic

import httpx
from starlette.concurrency import run_in_threadpool
from storage3.exceptions import StorageApiError

from app.config import get_settings
from app.core.constants import CHECKIN_STAGE_METADATA, CHECKIN_STAGES, STAGE_PROMPTS
from app.core.errors import ArtifactUnavailable, NotFound
from app.db.client import get_supabase_client
from app.services.addis_ai import AddisAIClient

_STAGE_AUDIO_BYTE_CACHE = {}
_STAGE_AUDIO_EXPIRES = {}


def prompt_path(stage):
    stage = stage.lower().strip()
    if stage not in STAGE_PROMPTS:
        raise NotFound("Invalid stage")
    version = hashlib.sha256(
        ("am-default-v1:" + STAGE_PROMPTS[stage]).encode()
    ).hexdigest()[:16]
    return f"prompts/{version}/{stage}.mp3"


def get_default_supabase_audio_url(stage):
    return (
        get_settings().supabase_url.rstrip("/")
        + "/storage/v1/object/public/audio-prompts/"
        + prompt_path(stage)
    )


def get_stage_audio_url(stage):
    return get_default_supabase_audio_url(stage)


async def get_or_synthesize_stage_audio(stage):
    # Compatibility function name; runtime cache misses never synthesize.
    stage = stage.lower().strip()
    path = prompt_path(stage)
    key = (get_settings().supabase_url, path)
    if (
        key in _STAGE_AUDIO_BYTE_CACHE
        and _STAGE_AUDIO_EXPIRES.get(key, 0) > monotonic()
    ):
        return _STAGE_AUDIO_BYTE_CACHE[key]

    def download():
        return get_supabase_client().storage.from_("audio-prompts").download(path)

    try:
        audio = AddisAIClient._validated_audio(await run_in_threadpool(download))
    except (StorageApiError, httpx.HTTPError, ValueError) as exc:
        raise ArtifactUnavailable("Generic prompt audio is not provisioned") from exc
    # At most four 4MB assets across all configured projects/versions; expired
    # entries are evicted before admission. No patient text or patient audio.
    now = monotonic()
    for old in list(_STAGE_AUDIO_BYTE_CACHE):
        if _STAGE_AUDIO_EXPIRES.get(old, 0) <= now:
            _STAGE_AUDIO_BYTE_CACHE.pop(old, None)
            _STAGE_AUDIO_EXPIRES.pop(old, None)
    while _STAGE_AUDIO_BYTE_CACHE and (
        len(_STAGE_AUDIO_BYTE_CACHE) >= len(CHECKIN_STAGES)
        or sum(map(len, _STAGE_AUDIO_BYTE_CACHE.values())) + len(audio) > 16_000_000
    ):
        old = next(iter(_STAGE_AUDIO_BYTE_CACHE))
        _STAGE_AUDIO_BYTE_CACHE.pop(old)
        _STAGE_AUDIO_EXPIRES.pop(old, None)
    _STAGE_AUDIO_BYTE_CACHE[key] = audio
    _STAGE_AUDIO_EXPIRES[key] = now + 3600
    return audio


def get_all_stage_prompts_metadata():
    return [
        {
            "stage": stage,
            **CHECKIN_STAGE_METADATA[stage],
            "audio_url": get_stage_audio_url(stage),
        }
        for stage in CHECKIN_STAGES
    ]
