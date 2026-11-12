"""Exercise the runtime entrypoint as non-root with no outbound network or real settings."""

import subprocess
import sys

SMOKE = r"""
import io
import os
import signal
import subprocess
import time
import urllib.error
import urllib.request
import wave

assert os.getuid() == 10001
from app.services.audio_upload import inspect_audio
audio = io.BytesIO()
with wave.open(audio, "wb") as sample:
    sample.setnchannels(1)
    sample.setsampwidth(2)
    sample.setframerate(16000)
    sample.writeframes(b"\x00\x00" * 1600)
inspect_audio(audio.getvalue(), "audio/wav", 1)
server = subprocess.Popen(["bash", "scripts/run_api.sh"], stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True)
try:
    for attempt in range(50):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=1) as response:
                assert response.status == 200 and response.read() == b'{"status":"ok"}'
            break
        except urllib.error.URLError:
            time.sleep(0.1)
    else:
        raise RuntimeError("API did not become live")
    for path, status in (("/checkin/history", 401), ("/dev/asr-test", 404), ('/ready',503)):
        try:
            urllib.request.urlopen("http://127.0.0.1:8000" + path, timeout=2)
        except urllib.error.HTTPError as exc:
            assert exc.code == status and exc.headers["cache-control"] == "no-store"
        else:
            raise AssertionError(path)
finally:
    server.terminate()
    code = server.wait(timeout=10)
    output = server.stdout.read()
    print(output)
    # Uvicorn restores and re-raises the original signal after lifespan shutdown.
    assert "Application shutdown complete." in output
    assert code in (0, -signal.SIGTERM)
print("Non-root container: audio validation, API startup/authentication and graceful stop passed")
"""


def main():
    image = sys.argv[1] if len(sys.argv) > 1 else "enat:release"
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--network=none",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=32m",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges",
            "-e",
            "ENVIRONMENT=test",
            "-e",
            "ENABLE_REQUEST_LIMITS=false",
            "-e",
            "SUPABASE_URL=https://example.supabase.co",
            "-e",
            "SUPABASE_SERVICE_ROLE_KEY=smoke-placeholder",
            "-e",
            "ADDIS_API_KEY=smoke-placeholder",
            image,
            "python",
            "-c",
            SMOKE,
        ],
        check=True,
        timeout=45,
    )


if __name__ == "__main__":
    main()
