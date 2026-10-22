import json

# Fixed decoder commands, no shell, bounded input/time/output.
import subprocess  # nosec B404
import tempfile
from pathlib import Path

from fastapi import UploadFile
from starlette.concurrency import run_in_threadpool

from app.config import get_settings
from app.core.errors import ArtifactUnavailable, InvalidAudio, PayloadTooLarge

FORMATS = {
    "audio/wav": {"wav"},
    "audio/x-wav": {"wav"},
    "audio/webm": {"matroska", "webm"},
    "audio/ogg": {"ogg"},
    "audio/mp4": {"mov", "mp4", "m4a", "3gp", "3g2", "mj2"},
    "audio/mpeg": {"mp3"},
}


def inspect_audio(data: bytes, content_type: str, max_seconds: int):
    demuxer = {
        "audio/wav": "wav",
        "audio/x-wav": "wav",
        "audio/webm": "matroska",
        "audio/ogg": "ogg",
        "audio/mp4": "mov",
        "audio/mpeg": "mp3",
    }[content_type]
    try:
        with tempfile.TemporaryDirectory(prefix="enat-audio-") as directory:
            path = Path(directory) / "upload"
            path.write_bytes(data)
            input_args = [
                "-f",
                demuxer,
                "-protocol_whitelist",
                "file,pipe",
                "-i",
                str(path),
            ]
            # Fixed executable/arguments; upload is a private temporary file.
            probe = subprocess.run(  # nosec B603, B607
                [
                    "ffprobe",
                    "-v",
                    "error",
                    *input_args,
                    "-show_entries",
                    "format=format_name:stream=codec_type",
                    "-of",
                    "json",
                ],
                capture_output=True,
                timeout=5,
                check=True,
            )
            payload = json.loads(probe.stdout)
            formats = set(payload["format"]["format_name"].split(","))
            streams = payload.get("streams", [])
            if (
                not formats.intersection(FORMATS[content_type])
                or not streams
                or any(s.get("codec_type") != "audio" for s in streams)
            ):
                raise ValueError()
            # Decode at most max+1 seconds to bounded mono PCM. Browser WebM
            # commonly lacks duration metadata; metadata alone can also lie.
            # Fixed decoder; protocols and decode duration are bounded.
            decoded = subprocess.run(  # nosec B603, B607
                [
                    "ffmpeg",
                    "-nostdin",
                    "-v",
                    "error",
                    *input_args,
                    "-t",
                    str(max_seconds + 1),
                    "-ac",
                    "1",
                    "-ar",
                    "16000",
                    "-f",
                    "s16le",
                    "pipe:1",
                ],
                capture_output=True,
                timeout=10,
                check=True,
            )
            duration = len(decoded.stdout) / 32000
            if duration <= 0:
                raise ValueError()
            if duration > max_seconds:
                raise PayloadTooLarge("Audio duration exceeds limit")
    except FileNotFoundError as exc:
        raise ArtifactUnavailable("Audio validation unavailable") from exc
    except (ValueError, KeyError, subprocess.SubprocessError) as exc:
        raise InvalidAudio("Unsupported or invalid audio") from exc


async def read_audio(upload: UploadFile):
    settings = get_settings()
    content_type = (upload.content_type or "").split(";")[0].lower()
    if content_type not in FORMATS:
        raise InvalidAudio("Unsupported audio format")
    chunks = []
    count = 0
    while data := await upload.read(65536):
        count += len(data)
        if count > settings.max_audio_bytes:
            raise PayloadTooLarge("Audio upload too large")
        chunks.append(data)
    data = b"".join(chunks)
    await run_in_threadpool(
        inspect_audio, data, content_type, settings.max_audio_seconds
    )
    return data
