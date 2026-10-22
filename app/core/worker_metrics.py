"""Internal worker exporter. Configure a bearer secret and never publish port 9000."""

import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from time import time

from prometheus_client import Gauge, generate_latest

from app.core.observability import JOB_AGE, JOBS
from app.db import jobs

HEARTBEAT = Gauge(
    "enat_worker_heartbeat_timestamp_seconds", "Time of last successful worker loop"
)
PRIVACY_PENDING = Gauge(
    "enat_privacy_requests_pending", "Requests awaiting privacy review"
)
PRIVACY_AGE = Gauge(
    "enat_privacy_oldest_request_seconds", "Age of oldest pending privacy request"
)
SCHEDULER_LAG = Gauge("enat_scheduler_lag_seconds", "Scheduler cursor delay")


def update():
    stats = jobs.stats()
    for status in ("pending", "running", "failed"):
        JOBS.labels(status).set(stats[status])
    JOB_AGE.set(float(stats["oldest_due_seconds"]))
    SCHEDULER_LAG.set(float(stats["scheduler_lag_seconds"]))
    PRIVACY_PENDING.set(stats["privacy_queue"]["pending"])
    PRIVACY_AGE.set(float(stats["privacy_queue"]["oldest_seconds"]))
    HEARTBEAT.set(time())


def start(token):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if (
                self.path != "/metrics"
                or not token
                or not secrets.compare_digest(
                    self.headers.get("Authorization", ""), "Bearer " + token
                )
            ):
                self.send_error(404)
                return
            body = generate_latest()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_):
            pass

        def setup(self):
            super().setup()
            self.connection.settimeout(2)

    server = ThreadingHTTPServer(("0.0.0.0", 9000), Handler)  # nosec B104: internal container network, bearer protected
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
