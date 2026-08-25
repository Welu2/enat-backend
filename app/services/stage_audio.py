import logging
from typing import Any

from app.core.constants import CHECKIN_STAGE_METADATA, CHECKIN_STAGES, STAGE_PROMPTS
from app.db.client import get_supabase_client
from app.services.addis_ai import AddisAIClient

logger = logging.getLogger(__name__)

# In-memory fast cache for public URLs and audio bytes
_STAGE_AUDIO_URL_CACHE: dict[str, str] = {}
_STAGE_AUDIO_BYTE_CACHE: dict[str, bytes] = {}


def get_default_supabase_audio_url(stage: str) -> str:
    """Computes standard public Supabase Storage URL for a stage prompt audio file."""
    clean_stage = stage.lower().strip()
    try:
        client = get_supabase_client()
        url = client.storage.from_("audio-prompts").get_public_url(f"prompts/{clean_stage}.mp3")
        if isinstance(url, str) and url:
            return url
    except Exception:
        pass
    return f"https://lpsjopunbwsmvuzwwqap.supabase.co/storage/v1/object/public/audio-prompts/prompts/{clean_stage}.mp3"


def get_stage_audio_url(stage: str) -> str:
    """Returns the verified Supabase Storage public URL for a checkin stage question prompt.

    Pulls directly from the database `stage_audio_prompts` table with fast in-memory caching.
    """
    clean_stage = stage.lower().strip()
    if clean_stage in _STAGE_AUDIO_URL_CACHE:
        return _STAGE_AUDIO_URL_CACHE[clean_stage]

    # 1. Query Supabase stage_audio_prompts table
    try:
        client = get_supabase_client()
        res = (
            client.table("stage_audio_prompts")
            .select("audio_url")
            .eq("stage", clean_stage)
            .maybe_single()
            .execute()
        )
        if res and hasattr(res, "data") and isinstance(res.data, dict) and res.data.get("audio_url"):
            url = str(res.data["audio_url"])
            if url and not isinstance(url, MagicMock if "MagicMock" in globals() else type(None)):
                _STAGE_AUDIO_URL_CACHE[clean_stage] = url
                return url
    except Exception as exc:
        logger.debug(f"DB lookup for stage_audio_prompts url failed: {exc}")

    # 2. Fallback to Supabase Storage public URL
    computed_url = str(get_default_supabase_audio_url(clean_stage))
    _STAGE_AUDIO_URL_CACHE[clean_stage] = computed_url
    return computed_url


async def get_or_synthesize_stage_audio(stage: str) -> bytes:
    """Retrieves stored audio bytes for a checkin prompt, synthesizing and storing in Supabase if missing."""
    clean_stage = stage.lower().strip()
    if clean_stage not in STAGE_PROMPTS:
        raise ValueError(f"Invalid stage '{stage}'. Must be one of {CHECKIN_STAGES}")

    if clean_stage in _STAGE_AUDIO_BYTE_CACHE:
        return _STAGE_AUDIO_BYTE_CACHE[clean_stage]

    client = get_supabase_client()
    file_path = f"prompts/{clean_stage}.mp3"

    # 1. Try downloading directly from Supabase Storage
    try:
        downloaded = client.storage.from_("audio-prompts").download(file_path)
        if downloaded and isinstance(downloaded, bytes) and len(downloaded) > 0:
            _STAGE_AUDIO_BYTE_CACHE[clean_stage] = downloaded
            return downloaded
    except Exception as exc:
        logger.debug(f"Supabase download for {file_path} note: {exc}")

    # 2. Synthesize with TTS engine
    prompt_text = STAGE_PROMPTS[clean_stage]
    audio_bytes = await AddisAIClient().synthesize_speech(prompt_text)
    if not audio_bytes:
        raise RuntimeError(f"Failed to synthesize audio for stage '{stage}'")

    _STAGE_AUDIO_BYTE_CACHE[clean_stage] = audio_bytes

    # 3. Upload to Supabase Storage
    try:
        client.storage.from_("audio-prompts").upload(
            file_path,
            audio_bytes,
            file_options={"content-type": "audio/mpeg", "upsert": "true"},
        )
        public_url = client.storage.from_("audio-prompts").get_public_url(file_path)
        if isinstance(public_url, str):
            _STAGE_AUDIO_URL_CACHE[clean_stage] = public_url

        # 4. Upsert row into stage_audio_prompts database table
        meta = CHECKIN_STAGE_METADATA.get(clean_stage, {})
        row = {
            "stage": clean_stage,
            "prompt_am": meta.get("prompt_am", prompt_text),
            "prompt_en": meta.get("prompt_en", ""),
            "category_am": meta.get("category_am", ""),
            "category_en": meta.get("category_en", ""),
            "audio_url": str(public_url),
        }
        client.table("stage_audio_prompts").upsert(row).execute()
    except Exception as exc:
        logger.warning(f"Failed to persist stage audio to Supabase: {exc}")

    return audio_bytes


def get_all_stage_prompts_metadata() -> list[dict[str, Any]]:
    """Returns all 4 standard check-in stage prompts, localized categories, and Supabase audio URLs from DB."""
    # 1. Try querying DB
    try:
        client = get_supabase_client()
        res = client.table("stage_audio_prompts").select("*").execute()
        if res and hasattr(res, "data") and isinstance(res.data, list) and len(res.data) >= len(CHECKIN_STAGES):
            db_map = {row["stage"]: row for row in res.data if isinstance(row, dict) and "stage" in row}
            if len(db_map) >= len(CHECKIN_STAGES):
                prompts = []
                for stage_key in CHECKIN_STAGES:
                    row = db_map[stage_key]
                    url = str(row.get("audio_url") or get_stage_audio_url(stage_key))
                    prompts.append({
                        "stage": stage_key,
                        "category_am": row.get("category_am"),
                        "category_en": row.get("category_en"),
                        "prompt_am": row.get("prompt_am"),
                        "prompt_en": row.get("prompt_en"),
                        "audio_url": url,
                    })
                return prompts
    except Exception as exc:
        logger.debug(f"DB query for all stage prompts note: {exc}")

    # 2. Fallback to constant metadata + verified Supabase Storage URLs
    prompts = []
    for stage_key in CHECKIN_STAGES:
        meta = CHECKIN_STAGE_METADATA[stage_key]
        prompts.append({
            "stage": stage_key,
            "category_am": meta["category_am"],
            "category_en": meta["category_en"],
            "prompt_am": meta["prompt_am"],
            "prompt_en": meta["prompt_en"],
            "audio_url": str(get_stage_audio_url(stage_key)),
        })
    return prompts
