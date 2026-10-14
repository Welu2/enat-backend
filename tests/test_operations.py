import json
import logging

from fastapi.testclient import TestClient

from app.config import get_settings
from app.core.observability import SafeFormatter
from app.main import create_app


def test_metrics_require_bearer_and_do_not_label_paths_or_patient_inputs():
    client = TestClient(create_app())
    assert client.get("/metrics").status_code == 404
    assert (
        client.get("/metrics", headers={"Authorization": "Bearer wrong"}).status_code
        == 404
    )
    client.get("/unknown/private-patient-token?text=private-health-text")
    result = client.get(
        "/metrics", headers={"Authorization": "Bearer " + get_settings().metrics_token}
    )
    assert result.status_code == 200
    assert "enat_http_seconds" in result.text
    assert "private-patient-token" not in result.text
    assert "private-health-text" not in result.text


def test_early_request_failures_also_receive_server_correlation_ids():
    from uuid import UUID

    client = TestClient(create_app())
    response = client.post(
        "/auth/login",
        content=b"x",
        headers={"Content-Length": "99999999", "X-Request-ID": "untrusted"},
    )
    assert response.status_code == 413
    assert UUID(response.headers["x-request-id"])
    response = client.get("/health", headers={"Host": "untrusted.invalid"})
    assert response.status_code == 400
    assert UUID(response.headers["x-request-id"])


def test_structured_logs_drop_unreviewed_extras_and_exceptions():
    record = logging.LogRecord(
        "enat", logging.ERROR, "", 0, "request_completed", (), None
    )
    record.health_text = "secret patient text"
    record.authorization = "Bearer secret"
    record.route = "/summary/{share_link_slug}"
    value = json.loads(SafeFormatter().format(record))
    assert value["route"] == "/summary/{share_link_slug}"
    assert "secret" not in str(value)


def test_trace_propagation_retains_parent_without_payloads(monkeypatch):
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    from app.core import observability

    provider = TracerProvider()
    exporter = InMemorySpanExporter()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("test")
    monkeypatch.setattr(observability.trace, "get_tracer", lambda *_: tracer)
    with observability.span("request") as parent:
        headers = observability.trace_headers()
        parent_context = parent.get_span_context()
    assert set(headers) == {"traceparent"}
    with observability.span(
        "job.outbox.deliver", parent=headers["traceparent"]
    ) as child:
        assert child.get_span_context().trace_id == parent_context.trace_id
    with TestClient(create_app()) as client:
        client.get("/unknown/private-token?health=private-text")
    spans = exporter.get_finished_spans()
    assert spans[1].parent.span_id == parent_context.span_id
    assert all(
        "private-" not in str((s.name, dict(s.attributes), s.events)) for s in spans
    )
    provider.shutdown()


def test_timed_out_readiness_does_not_accumulate_database_probes(monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    from app.core import readiness

    entered, release = Event(), Event()

    def unavailable_pool():
        entered.set()
        release.wait(5)
        raise TimeoutError()

    monkeypatch.setattr(readiness, "get_pool", unavailable_pool)
    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(readiness.database_ready)
        assert entered.wait(2)
        try:
            # A second probe returns immediately rather than queueing a second
            # DB operation behind a possibly stuck network connection.
            assert executor.submit(readiness.database_ready).result(timeout=1) is False
            assert TestClient(create_app()).get("/health").status_code == 200
        finally:
            release.set()
        assert first.result(timeout=2) is False
