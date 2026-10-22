"""One bounded HTTP pool per application event loop; one budget per voice turn."""

import asyncio
import random
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from time import monotonic

import httpx
from pydantic import JsonValue

from app.config import Settings, get_settings
from app.core.errors import ProviderUnavailable
from app.core.limits import provider_budget
from app.core.observability import CALLS, provider_span, trace_headers


@dataclass
class Operation:
    calls: int = 0


_operation: ContextVar[Operation | None] = ContextVar(
    "provider_operation", default=None
)
_runtimes: dict[asyncio.AbstractEventLoop, "ProviderRuntime"] = {}


@asynccontextmanager
async def operation() -> AsyncIterator[None]:
    if _operation.get() is not None:
        yield
        return
    token = _operation.set(Operation())
    try:
        async with asyncio.timeout(get_settings().provider_operation_seconds):
            yield
    except TimeoutError as exc:
        raise ProviderUnavailable("Provider operation timed out") from exc
    finally:
        _operation.reset(token)


class ProviderRuntime:
    def __init__(
        self,
        settings: Settings | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(connect=3, read=15, write=10, pool=2),
            limits=httpx.Limits(
                max_connections=self.settings.provider_concurrency,
                max_keepalive_connections=self.settings.provider_concurrency,
            ),
            transport=transport,
            follow_redirects=False,
        )
        self.slots = asyncio.Semaphore(self.settings.provider_concurrency)
        self.failures = 0
        self.open_until = 0.0
        self.probing = False

    async def close(self) -> None:
        await self.client.aclose()

    async def request(
        self,
        path: str,
        *,
        max_bytes: int = 128_000,
        json: Mapping[str, JsonValue] | None = None,
        files: Mapping[str, tuple[str, bytes, str]] | None = None,
        data: Mapping[str, str] | None = None,
    ) -> httpx.Response:
        with provider_span(path):
            return await self._request(
                path, max_bytes=max_bytes, json=json, files=files, data=data
            )

    async def _request(
        self,
        path: str,
        *,
        max_bytes: int = 128_000,
        json: Mapping[str, JsonValue] | None = None,
        files: Mapping[str, tuple[str, bytes, str]] | None = None,
        data: Mapping[str, str] | None = None,
    ) -> httpx.Response:
        async with operation():
            if monotonic() < self.open_until or self.probing:
                raise ProviderUnavailable("Provider circuit open")
            probe = self.failures >= 3
            if probe:
                self.probing = True
            try:
                async with self.slots:
                    for attempt in range(2):
                        budget = _operation.get()
                        if budget is None:
                            raise RuntimeError("Missing provider operation scope")
                        if budget.calls >= 4:
                            raise ProviderUnavailable(
                                "Provider attempt budget exhausted"
                            )
                        budget.calls += 1
                        CALLS.labels(
                            {
                                "/api/v2/stt": "asr",
                                "/api/v1/chat_generate": "extract",
                                "/api/v1/tts": "tts",
                            }.get(path, "other")
                        ).inc()
                        retry = False
                        # Scheduling jitter, never a credential.
                        retry_delay = random.uniform(0.1, 0.3)  # nosec B311
                        try:
                            async with (
                                provider_budget(),
                                asyncio.timeout(self.settings.provider_request_seconds),
                            ):
                                async with self.client.stream(
                                    "POST",
                                    self.settings.addis_api_base_url.rstrip("/") + path,
                                    headers={
                                        "x-api-key": self.settings.addis_api_key,
                                        **trace_headers(),
                                    },
                                    json=json,
                                    files=files,
                                    data=data,
                                ) as response:
                                    if response.status_code in (429, 503):
                                        retry = True
                                        retry_after = response.headers.get(
                                            "retry-after"
                                        )
                                        if retry_after:
                                            # Long/date-form server backoffs are returned
                                            # to the caller instead of holding a voice turn.
                                            try:
                                                retry_delay = max(
                                                    retry_delay, float(retry_after)
                                                )
                                            except ValueError as exc:
                                                raise ProviderUnavailable(
                                                    "Provider requested later retry"
                                                ) from exc
                                            if not 0 <= retry_delay <= 1:
                                                raise ProviderUnavailable(
                                                    "Provider requested later retry"
                                                )
                                    elif response.status_code != 200:
                                        raise ProviderUnavailable(
                                            "Provider rejected request"
                                        )
                                    else:
                                        chunks, size = [], 0
                                        async for chunk in response.aiter_bytes():
                                            size += len(chunk)
                                            if size > max_bytes:
                                                raise ProviderUnavailable(
                                                    "Provider response exceeds bound"
                                                )
                                            chunks.append(chunk)
                                        result = httpx.Response(
                                            200,
                                            # aiter_bytes has already decoded content.
                                            headers={
                                                "content-type": response.headers.get(
                                                    "content-type", ""
                                                )
                                            },
                                            content=b"".join(chunks),
                                        )
                                        self.failures, self.open_until = 0, 0.0
                                        return result
                        except (httpx.ConnectError, httpx.ConnectTimeout):
                            retry = True
                        except (httpx.HTTPError, TimeoutError) as exc:
                            # Read/write failures may already have incurred a charge.
                            raise ProviderUnavailable(
                                "Provider transport unavailable"
                            ) from exc
                        if not retry or attempt == 1:
                            raise ProviderUnavailable("Provider unavailable")
                        await asyncio.sleep(retry_delay)
            except ProviderUnavailable:
                self.failures += 1
                if self.failures >= 3:
                    self.open_until = monotonic() + 30
                raise
            finally:
                if probe:
                    self.probing = False
        raise ProviderUnavailable("Provider attempts exhausted")


@asynccontextmanager
async def lifespan(settings: Settings) -> AsyncIterator[ProviderRuntime]:
    loop = asyncio.get_running_loop()
    runtime = ProviderRuntime(settings)
    _runtimes[loop] = runtime
    try:
        yield runtime
    finally:
        _runtimes.pop(loop, None)
        await runtime.close()


@asynccontextmanager
async def runtime_client() -> AsyncIterator[ProviderRuntime]:
    runtime = _runtimes.get(asyncio.get_running_loop())
    if runtime is not None:
        yield runtime
    else:
        # Standalone provisioning/test use has explicit cleanup too.
        runtime = ProviderRuntime()
        try:
            yield runtime
        finally:
            await runtime.close()
