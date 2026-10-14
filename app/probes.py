"""Container-local health probes; no provider requests or patient data."""

import os
import sys
from time import time
from urllib.request import Request, urlopen


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "live"
    if mode not in {"live", "ready", "worker"}:
        raise SystemExit("Unknown probe")
    target = (
        "http://127.0.0.1:9000/metrics"
        if mode == "worker"
        else "http://127.0.0.1:8000/" + ("health" if mode == "live" else "ready")
    )
    headers = (
        {"Authorization": "Bearer " + os.environ.get("METRICS_TOKEN", "")}
        if mode == "worker"
        else {}
    )
    try:
        with urlopen(Request(target, headers=headers), timeout=2) as response:  # nosec B310: fixed loopback HTTP targets
            body = response.read(512000).decode()
        if mode == "worker":
            value = next(
                line.split()[1]
                for line in body.splitlines()
                if line.startswith("enat_worker_heartbeat_timestamp_seconds ")
            )
            if time() - float(value) > 90:
                raise ValueError("Stale worker heartbeat")
    except Exception:
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
