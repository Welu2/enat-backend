"""Explicit operator command; never invoked by API startup or cache misses.

python -m app.provision_prompts --operator-user-id UUID --output /tmp/enat-prompts
Review generated files before uploading their manifest paths to audio-prompts.
"""

import argparse
import asyncio
import json
from pathlib import Path
from uuid import UUID

from app.config import get_settings
from app.core.constants import STAGE_PROMPTS
from app.db.data import close_pool, current_user_id
from app.services.addis_ai import AddisAIClient
from app.services.provider_runtime import lifespan
from app.services.stage_audio import prompt_path


async def generate(output, operator):
    token = current_user_id.set(str(operator))
    try:
        async with lifespan(get_settings()):
            client = AddisAIClient()
            manifest = []
            for stage, text in STAGE_PROMPTS.items():
                audio = await client.synthesize_speech(text)
                if audio.startswith(b"RIFF"):
                    raise ValueError(
                        "Provisioning requires MP3 output for .mp3 object paths"
                    )
                path = output / prompt_path(stage)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(audio)
                manifest.append(
                    {"stage": stage, "path": prompt_path(stage), "bytes": len(audio)}
                )
            (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    finally:
        current_user_id.reset(token)
        close_pool()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operator-user-id", type=UUID, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    asyncio.run(generate(args.output, args.operator_user_id))


if __name__ == "__main__":
    main()
