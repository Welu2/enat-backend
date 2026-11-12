"""Isolated Compose backend for load_rehearsal; never reads deployment secrets."""

import getpass
import json
import os
import socket
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from uuid import uuid4

import httpx
import psycopg

PROMETHEUS = "prom/prometheus:v3.15.0@sha256:efd719c99d83b060d9daefdcf00360461adf279f45ef5391f8d111892118753e"


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class ComposeStack:
    def __init__(self, env, directory):
        self.directory = Path(directory)
        self.project = "enat-rehearsal-" + uuid4().hex[:12]
        self.network = self.project + "-private"
        self.ports = [free_port(), free_port()]
        self.prometheus_port = free_port()
        self.urls = []
        self.prometheus_url = ""
        self.env = env
        self.command = []
        self.receiver = None
        self.received = set()
        self.evidence = {}
        self.network_created = False
        self.outbox_id = uuid4()

    def run(self, *args, timeout=120):
        result = subprocess.run(
            list(args), env=self.env, capture_output=True, text=True, timeout=timeout
        )
        if result.returncode:
            # Only synthetic configuration is passed, but keep logs private anyway.
            (self.directory / "compose-error.log").write_text(result.stderr)
            raise RuntimeError(
                "Compose rehearsal command failed: "
                + " ".join(args[:3])
                + "\n"
                + result.stderr[-2000:]
            )
        return result.stdout.strip()

    def compose(self, *args, **kwargs):
        return self.run(*self.command, *args, **kwargs)

    def start(self):
        dsn = psycopg.conninfo.conninfo_to_dict(self.env["ENAT_TEST_ADMIN_DSN"])
        database_directory = dsn.get("host", "")
        if not database_directory.startswith("/tmp/enat-security-"):
            raise ValueError(
                "Compose rehearsal requires the disposable database runner"
            )
        os.chmod(database_directory, 0o755)
        os.chmod(self.directory, 0o755)
        image = self.run(
            "docker",
            "image",
            "inspect",
            "--format",
            "{{.Id}}",
            os.environ.get("ENAT_LOAD_IMAGE", "enat:phase5"),
        )
        self.run("docker", "network", "create", "--internal", self.network)
        self.network_created = True
        gateway = json.loads(self.run("docker", "network", "inspect", self.network))[0][
            "IPAM"
        ]["Config"][0]["Gateway"]
        common = {
            "METRICS_TOKEN": self.env["METRICS_TOKEN"],
            "OTLP_ENDPOINT": "",
            "ENABLE_DEV_ROUTES": "false",
        }
        api = dict(
            common,
            DATABASE_URL=self.env["ENAT_TEST_APP_DSN"],
            SUPABASE_URL="https://example.supabase.co",
            SUPABASE_SERVICE_ROLE_KEY="synthetic-placeholder",
            SUPABASE_PUBLISHABLE_KEY="synthetic-placeholder",
            ADDIS_API_KEY="synthetic-placeholder",
            ADDIS_API_BASE_URL="https://provider.example.invalid",
            PUBLIC_BASE_URL="https://frontend.example.invalid",
            CORS_ORIGINS="https://frontend.example.invalid",
            TRUSTED_HOSTS="127.0.0.1,localhost,api-a,api-b",
            TRUSTED_PROXY_IPS=gateway,
            ENABLE_REQUEST_LIMITS="true",
            RATE_LIMIT_SECRET=self.env["RATE_LIMIT_SECRET"],
        )
        worker = dict(common, WORKER_DATABASE_URL=self.env["ENAT_TEST_WORKER_DSN"])
        dsn.setdefault("user", getpass.getuser())
        migration = {"MIGRATION_DATABASE_URL": psycopg.conninfo.make_conninfo(**dsn)}
        for name, values in (
            ("api", api),
            ("worker", worker),
            ("migration", migration),
        ):
            path = self.directory / (name + ".env")
            path.write_text(
                "".join(f"{key}={value}\n" for key, value in values.items())
            )
            path.chmod(0o600)

        received = self.received

        class Receiver(BaseHTTPRequestHandler):
            def do_POST(self):
                length = int(self.headers.get("Content-Length", "0"))
                if self.path != "/api/v2/alerts" or not 0 < length <= 65536:
                    self.send_error(400)
                    return
                alerts = json.loads(self.rfile.read(length))
                received.update(a["labels"]["alertname"] for a in alerts)
                self.send_response(200)
                self.end_headers()

            def log_message(self, *_):
                pass

        # Local Alertmanager-compatible sink, with no external notification route.
        self.receiver = ThreadingHTTPServer((gateway, 0), Receiver)
        threading.Thread(target=self.receiver.serve_forever, daemon=True).start()
        token_file = self.directory / "metrics-token"
        token_file.write_text(common["METRICS_TOKEN"])
        token_file.chmod(0o644)  # Synthetic-only token readable by the Prometheus UID.
        config = Path("deploy/prometheus.yml").read_text().replace("15s", "2s")
        config += (
            "\nalerting:\n  alertmanagers:\n    - static_configs:\n"
            f"        - targets: ['{gateway}:{self.receiver.server_port}']\n"
        )
        (self.directory / "prometheus.yml").write_text(config)
        services = {
            name: {"volumes": [f"{database_directory}:{database_directory}:ro"]}
            for name in ("api-a", "api-b", "worker", "scheduler", "migrate")
        }
        services["prometheus"] = {
            "image": PROMETHEUS,
            "read_only": True,
            "cap_drop": ["ALL"],
            "security_opt": ["no-new-privileges:true"],
            "mem_limit": "256m",
            "cpus": 0.5,
            "pids_limit": 64,
            "tmpfs": ["/prometheus:rw,noexec,nosuid,size=128m,uid=65534,gid=65534"],
            "ports": [f"127.0.0.1:{self.prometheus_port}:9090"],
            "volumes": [
                f"{self.directory}/prometheus.yml:/etc/prometheus/prometheus.yml:ro",
                f"{Path('deploy/alerts.yml').resolve()}:/etc/prometheus/alerts.yml:ro",
                f"{token_file}:/run/secrets/enat_metrics_token:ro",
            ],
            "command": [
                "--config.file=/etc/prometheus/prometheus.yml",
                "--storage.tsdb.path=/prometheus",
                "--storage.tsdb.retention.time=2h",
            ],
        }
        override = self.directory / "compose.json"
        override.write_text(
            json.dumps(
                {
                    "services": services,
                    "networks": {"default": {"external": True, "name": self.network}},
                }
            )
        )
        self.env = dict(
            self.env,
            DEPLOYMENT_ENV="staging",
            ENAT_IMAGE=image,
            API_ENV_FILE=str(self.directory / "api.env"),
            WORKER_ENV_FILE=str(self.directory / "worker.env"),
            MIGRATION_ENV_FILE=str(self.directory / "migration.env"),
            API_A_PORT=str(self.ports[0]),
            API_B_PORT=str(self.ports[1]),
        )
        self.command = [
            "docker",
            "compose",
            "--project-name",
            self.project,
            "-f",
            str(Path("deploy/compose.yaml").resolve()),
            "-f",
            str(override),
        ]
        with psycopg.connect(self.env["ENAT_TEST_ADMIN_DSN"]) as conn:
            user = uuid4()
            conn.execute("INSERT INTO users(id) VALUES(%s)", (user,))
            conn.execute(
                "INSERT INTO domain_outbox(id,user_id,event_type,aggregate_id,created_at) "
                "VALUES(%s,%s,'checkin.completed',%s,now()-interval '1 day')",
                (self.outbox_id, user, uuid4()),
            )
        self.compose("--profile", "tools", "run", "--rm", "migrate")
        self.compose("up", "-d", "--wait", "--wait-timeout", "100")
        # Docker internal networks intentionally omit published host ports. The
        # local harness reaches private bridge IPs; containers still have no egress.
        for service in ("api-a", "api-b", "prometheus"):
            identifier = self.compose("ps", "-q", service)
            inspect = json.loads(self.run("docker", "inspect", identifier))[0]
            address = inspect["NetworkSettings"]["Networks"][self.network]["IPAddress"]
            if service == "prometheus":
                self.prometheus_url = f"http://{address}:9090"
            else:
                self.urls.append(f"http://{address}:8000")
        runtime = {}
        for service in ("api-a", "api-b", "worker", "scheduler"):
            identifier = self.compose("ps", "-q", service)
            inspect = json.loads(self.run("docker", "inspect", identifier))[0]
            host = inspect["HostConfig"]
            cpus = 2 if service.startswith("api-") else 1
            assert host["NanoCpus"] == cpus * 1_000_000_000
            assert host["Memory"] == 512 * 1024 * 1024
            assert host["PidsLimit"] == 128 and host["ReadonlyRootfs"]
            assert inspect["Config"]["User"] == "10001:10001"
            assert "ALL" in host["CapDrop"]
            assert "no-new-privileges:true" in host["SecurityOpt"]
            runtime[service] = {
                "cpus": cpus,
                "memory_mib": 512,
                "pids": 128,
                "read_only": True,
            }
        self.evidence = {
            "image": image,
            "runtime_limits": runtime,
            "staging_config_validation": True,
            "migration_container_passed": True,
            "external_network": False,
        }
        self.wait_for_scrapes()
        print(
            "Compose: two APIs, worker, scheduler and authenticated Prometheus scrapes ready",
            flush=True,
        )

    def query(self, expression):
        response = httpx.get(
            self.prometheus_url + "/api/v1/query",
            params={"query": expression},
            timeout=3,
            trust_env=False,
        )
        response.raise_for_status()
        return response.json()["data"]["result"]

    def wait_for_scrapes(self):
        for _ in range(30):
            try:
                rows = self.query('up{job=~"enat-api|enat-worker"}')
            except httpx.HTTPError:
                rows = []
            if len(rows) == 4 and all(row["value"][1] == "1" for row in rows):
                return
            time.sleep(1)
        raise RuntimeError("All four authenticated metrics targets must be scraped")

    def kill(self):
        self.compose("kill", "-s", "SIGKILL", "api-a")

    def restart(self):
        self.compose("up", "-d", "api-a")

    def finish(self, require_alert):
        self.compose("up", "-d", "--wait", "--wait-timeout", "100")
        self.wait_for_scrapes()
        self.evidence["all_four_scrapes_recovered"] = True
        self.evidence["local_alert_notifications"] = sorted(self.received)
        self.evidence["human_notification_tested"] = False
        dashboard_queries = []
        for panel in json.loads(Path("deploy/grafana-dashboard.json").read_text())[
            "panels"
        ]:
            for target in panel["targets"]:
                rows = self.query(target["expr"])
                dashboard_queries.append(
                    {
                        "panel": panel["title"],
                        "target": target["refId"],
                        "series": len(rows),
                    }
                )
        self.evidence["dashboard_queries"] = dashboard_queries
        self.evidence["grafana_ui_tested"] = False
        if require_alert and "EnatApiUnavailable" not in self.received:
            raise RuntimeError("API outage did not reach the local alert sink")
        with psycopg.connect(self.env["ENAT_TEST_ADMIN_DSN"]) as conn:
            delivered = conn.execute(
                "SELECT delivered_at IS NOT NULL FROM domain_outbox WHERE id=%s",
                (self.outbox_id,),
            ).fetchone()[0]
            notifications = conn.execute(
                "SELECT count(*) FROM reminders WHERE occurrence_key=%s",
                ("outbox:" + str(self.outbox_id),),
            ).fetchone()[0]
            assert delivered and notifications == 1
            self.evidence["scheduler_worker_outbox_delivered_once"] = True
        for service in ("api-a", "api-b", "worker", "scheduler"):
            identifier = self.compose("ps", "-q", service)
            inspect = json.loads(self.run("docker", "inspect", identifier))[0]
            assert not inspect["State"]["OOMKilled"]
            assert inspect["State"]["Health"]["Status"] == "healthy"
        return self.evidence

    def close(self):
        try:
            if self.command:
                try:
                    destination = Path("artifacts/operations")
                    destination.mkdir(parents=True, exist_ok=True)
                    (destination / "compose-service-logs.txt").write_text(
                        self.compose("logs", "--no-color", "--tail", "40")
                    )
                finally:
                    self.compose("down", "--volumes", "--remove-orphans", timeout=120)
        finally:
            if self.receiver:
                self.receiver.shutdown()
                self.receiver.server_close()
            if self.network_created:
                self.run("docker", "network", "rm", self.network)
