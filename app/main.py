import asyncio
import logging
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api.routes import (
    auth,
    checkin,
    notifications,
    privacy,
    reminders,
    summary,
    tts,
    users,
)
from app.config import Settings, get_settings
from app.core import observability
from app.core.http_security import (
    AccessLogFilter,
    SecurityMiddleware,
    http_error,
    validation_error,
)
from app.models.errors import ErrorResponse
from app.services.addis_ai import AddisAIClient
from app.services.provider_runtime import lifespan as provider_lifespan


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    if settings.process_role != "api":
        raise ValueError("Worker configuration cannot start the API")

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        import anyio

        anyio.to_thread.current_default_thread_limiter().total_tokens = (
            settings.io_thread_limit
        )
        observability.configure(settings)
        monitor = asyncio.create_task(observability.loop_monitor())
        try:
            async with provider_lifespan(settings):
                yield
        finally:
            monitor.cancel()
            with suppress(asyncio.CancelledError):
                await monitor
            await anyio.to_thread.run_sync(observability.shutdown)
            from app.db.data import close_pool

            await anyio.to_thread.run_sync(close_pool)

    app = FastAPI(
        title="EnatAI Clinical Intake Backend",
        version="0.1.0",
        lifespan=lifespan,
        responses={
            code: {"model": ErrorResponse, "description": description}
            for code, description in (
                (400, "Invalid request"),
                (401, "Invalid credentials"),
                (404, "Resource not found"),
                (409, "Version or retry-key conflict"),
                (413, "Request too large"),
                (415, "Invalid audio"),
                (422, "Invalid mutation"),
                (429, "Rate limited"),
                (500, "Internal error"),
                (503, "Dependency unavailable; retry or manual input"),
            )
        },
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Next-Cursor", "X-Request-ID"],
    )
    app.add_exception_handler(RequestValidationError, validation_error)
    app.add_exception_handler(HTTPException, http_error)
    app.add_middleware(SecurityMiddleware, settings=settings)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            h.strip() for h in settings.trusted_hosts.split(",") if h.strip()
        ],
    )
    app.add_middleware(observability.TelemetryMiddleware, settings=settings)
    logging.getLogger("uvicorn.access").addFilter(AccessLogFilter())
    for router in (
        auth.router,
        users.router,
        privacy.router,
        checkin.router,
        summary.router,
        reminders.router,
        notifications.router,
        tts.router,
    ):
        app.include_router(router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        """Process liveness only; never probes external services."""
        return {"status": "ok"}

    import anyio

    readiness_limiter = anyio.CapacityLimiter(1)

    @app.get("/ready", include_in_schema=False)
    async def ready():
        from starlette.responses import JSONResponse

        from app.core.readiness import database_ready

        ok = False
        # A dedicated bounded lane keeps readiness independent of the main
        # repository thread pool. Cancellation never spawns unbounded probes.
        with anyio.move_on_after(1.25):
            ok = await anyio.to_thread.run_sync(
                database_ready, limiter=readiness_limiter, abandon_on_cancel=True
            )
        return JSONResponse(
            {"status": "ready" if ok else "unavailable"}, 200 if ok else 503
        )

    if settings.enable_dev_routes:
        app.include_router(reminders.dev_router)

        @app.post("/dev/asr-test")
        async def dev_asr_test(audio: UploadFile = File(...)) -> dict[str, str]:
            from app.services.audio_upload import read_audio

            audio_bytes = await read_audio(audio)
            transcript = await AddisAIClient().transcribe(
                audio_bytes,
                audio.filename or "audio.wav",
                audio.content_type or "audio/wav",
            )
            return {"transcript": transcript}

    return app


app = create_app()
