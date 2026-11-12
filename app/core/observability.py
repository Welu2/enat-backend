"""Low-cardinality metrics and manually allowlisted traces/logs; no payload capture."""

import asyncio
import json
import logging
import secrets
from contextlib import contextmanager
from contextvars import ContextVar
from time import monotonic
from uuid import uuid4

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from starlette.responses import JSONResponse, Response

REQUESTS = Histogram(
    "enat_http_seconds",
    "HTTP duration",
    ["method", "route", "status"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5, 15, 45, 60),
)
PROVIDERS = Histogram(
    "enat_provider_seconds",
    "Provider operation duration including retries",
    ["operation", "outcome"],
    buckets=(0.1, 1, 5, 10, 20, 45, 60),
)
CALLS = Counter(
    "enat_provider_attempts",
    "Billable attempt upper bound, including retry attempts",
    ["operation"],
)
LAG = Gauge("enat_event_loop_lag_seconds", "Latest event loop scheduling delay")
POOL = Gauge("enat_db_pool", "Database pool statistics", ["stat"])
JOBS = Gauge("enat_jobs", "Durable queue counts", ["status"])
JOB_AGE = Gauge(
    "enat_oldest_due_job_seconds", "Age of oldest pending or expired-running job"
)
PROVIDER_USED = Gauge(
    "enat_provider_daily_calls", "Distributed global daily admitted provider attempts"
)
CONFIRMATIONS = Counter(
    "enat_confirmation_failures", "Rejected confirmation mutations", ["status"]
)
SHARES = Counter(
    "enat_share_requests", "Share create, lookup, revoke outcomes", ["route", "status"]
)
request_id = ContextVar("request_id", default="")
_tracer_provider = None


class SafeFormatter(logging.Formatter):
    def format(self, record):
        # Messages must be static event names. Never serialize arbitrary extras,
        # exception objects, SQL, URLs, headers, or provider/request bodies.
        result = {
            "event": record.getMessage(),
            "level": record.levelname,
            "request_id": request_id.get(),
        }
        for key in ("job_id", "route", "status", "duration_ms"):
            if hasattr(record, key):
                result[key] = getattr(record, key)
        ctx = trace.get_current_span().get_span_context()
        if ctx.is_valid:
            result["trace_id"] = format(ctx.trace_id, "032x")
        return json.dumps(result)


def configure(settings):
    global _tracer_provider
    logger = logging.getLogger("enat")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(SafeFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    if settings.otlp_endpoint and _tracer_provider is None:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )

        _tracer_provider = TracerProvider(
            resource=Resource.create({"service.name": "enat-" + settings.process_role}),
            sampler=TraceIdRatioBased(0.1),
        )
        _tracer_provider.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporter(endpoint=settings.otlp_endpoint, timeout=2),
                max_queue_size=1024,
            )
        )
        trace.set_tracer_provider(_tracer_provider)


def shutdown():
    if _tracer_provider:
        _tracer_provider.force_flush(timeout_millis=2000)


def trace_headers() -> dict[str, str]:
    carrier: dict[str, str] = {}
    TraceContextTextMapPropagator().inject(carrier)
    return {key: value for key, value in carrier.items() if key == "traceparent"}


@contextmanager
def span(name, parent=None, **attributes):
    context = (
        TraceContextTextMapPropagator().extract({"traceparent": parent})
        if parent
        else None
    )
    with trace.get_tracer("enat").start_as_current_span(
        name,
        context=context,
        attributes=attributes,
        record_exception=False,
        set_status_on_exception=False,
    ) as current:
        yield current


@contextmanager
def provider_span(path):
    operation = {
        "/api/v2/stt": "asr",
        "/api/v1/chat_generate": "extract",
        "/api/v1/tts": "tts",
    }.get(path, "other")
    start, outcome = monotonic(), "error"
    with span("provider." + operation):
        try:
            yield operation
            outcome = "ok"
        finally:
            PROVIDERS.labels(operation, outcome).observe(monotonic() - start)


async def loop_monitor():
    while True:
        start = monotonic()
        await asyncio.sleep(1)
        LAG.set(max(0, monotonic() - start - 1))


class TelemetryMiddleware:
    def __init__(self, app, settings):
        self.app, self.settings = app, settings

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        if scope["path"] == "/metrics":
            headers = dict(scope.get("headers", []))
            supplied = headers.get(b"authorization", b"").decode("latin1")
            if not self.settings.metrics_token or not secrets.compare_digest(
                supplied, "Bearer " + self.settings.metrics_token
            ):
                return await JSONResponse({"detail": "Not found"}, 404)(
                    scope, receive, send
                )
            from app.db.data import get_pool

            if get_pool.cache_info().currsize:
                for name, value in get_pool().get_stats().items():
                    POOL.labels(name).set(value)
            return await Response(
                generate_latest(),
                media_type="text/plain; version=0.0.4",
                headers={"Cache-Control": "no-store"},
            )(scope, receive, send)
        token = request_id.set(str(uuid4()))
        scope["enat.request_id"] = request_id.get()
        start, status = monotonic(), 500
        # Propagate only W3C traceparent; never baggage or tenant-supplied labels.
        headers = dict(scope.get("headers", []))
        carrier = {
            "traceparent": headers.get(b"traceparent", b"").decode("latin1")[:128]
        }
        parent = TraceContextTextMapPropagator().extract(carrier)
        with trace.get_tracer("enat").start_as_current_span(
            "http.request",
            context=parent,
            record_exception=False,
            set_status_on_exception=False,
        ) as current:

            async def observe(message):
                nonlocal status
                if message["type"] == "http.response.start":
                    status = message["status"]
                    # Include correlation on early host/body/rate-limit failures
                    # as well as responses that reach the router.
                    headers = list(message.get("headers", []))
                    if not any(key.lower() == b"x-request-id" for key, _ in headers):
                        headers.append((b"x-request-id", request_id.get().encode()))
                    message = {**message, "headers": headers}
                await send(message)

            try:
                await self.app(scope, receive, observe)
            finally:
                route = getattr(scope.get("route"), "path", "unmatched")
                method = (
                    scope["method"]
                    if scope["method"]
                    in {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}
                    else "OTHER"
                )
                elapsed = monotonic() - start
                current.update_name(method + " " + route)
                current.set_attribute("http.route", route)
                current.set_attribute("http.response.status_code", status)
                REQUESTS.labels(method, route, str(status)).observe(elapsed)
                if route.endswith("/verify") and status >= 400:
                    CONFIRMATIONS.labels(str(status)).inc()
                if route.startswith("/summary/"):
                    SHARES.labels(route, str(status)).inc()
                logging.getLogger("enat.http").info(
                    "request_completed",
                    extra={
                        "route": route,
                        "status": status,
                        "duration_ms": round(elapsed * 1000, 2),
                    },
                )
                request_id.reset(token)
