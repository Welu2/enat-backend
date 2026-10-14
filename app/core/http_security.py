import logging
from uuid import uuid4

from fastapi.exceptions import RequestValidationError
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.core.errors import (
    ApplicationError,
    ArtifactUnavailable,
    Conflict,
    ConsentRequired,
    FeatureUnavailable,
    InvalidAudio,
    InvalidMutation,
    NotFound,
    PayloadTooLarge,
    ProviderUnavailable,
    RateLimited,
)
from app.core.limits import take_rate

PRIVATE_HEADERS = {
    "Cache-Control": "no-store",
    "Referrer-Policy": "no-referrer",
    "X-Robots-Tag": "noindex, nofollow",
}


class AccessLogFilter(logging.Filter):
    def filter(self, record):
        # Uvicorn access records contain the full request target including query.
        # Replace the entire target; request IDs provide application correlation.
        if isinstance(record.args, tuple) and len(record.args) == 5:
            args = list(record.args)
            args[2] = "[redacted]"
            record.args = tuple(args)
        return True


def error_response(exc):
    if isinstance(exc, StarletteHTTPException):
        return JSONResponse(
            {"detail": exc.detail if isinstance(exc.detail, str) else "Request failed"},
            exc.status_code,
            headers={**(exc.headers or {}), **PRIVATE_HEADERS},
        )
    if isinstance(exc, RequestValidationError):
        return JSONResponse({"detail": "Invalid request"}, 422, headers=PRIVATE_HEADERS)
    if isinstance(exc, ProviderUnavailable):
        return JSONResponse(
            {
                "detail": "Speech service unavailable; retry or use manual input",
                "code": "provider_unavailable",
                "draft_preserved": True,
                "recovery": ["retry", "manual_input"],
            },
            503,
            headers={"Retry-After": "30", **PRIVATE_HEADERS},
        )
    for error, code, message in (
        (Conflict, 409, "State changed or retry key conflicts; reload and retry"),
        (NotFound, 404, "Resource not found"),
        (InvalidMutation, 422, "Invalid mutation"),
        (ConsentRequired, 400, "Explicit consent is required"),
        (InvalidAudio, 415, "Unsupported or invalid audio"),
        (PayloadTooLarge, 413, "Audio exceeds upload or duration limit"),
        (ArtifactUnavailable, 503, "Artifact temporarily unavailable"),
        (FeatureUnavailable, 503, "Feature unavailable pending review"),
    ):
        if isinstance(exc, error):
            return JSONResponse({"detail": message}, code, headers=PRIVATE_HEADERS)
    if isinstance(exc, RateLimited):
        return JSONResponse(
            {"detail": "Request limit exceeded"},
            429,
            headers={"Retry-After": "60", **PRIVATE_HEADERS},
        )
    return JSONResponse(
        {"detail": "Service temporarily unavailable"}, 503, headers=PRIVATE_HEADERS
    )


async def validation_error(request, exc):
    # Pydantic errors otherwise echo patient input and credentials.
    return error_response(exc)


async def http_error(request, exc):
    return error_response(exc)


class SecurityMiddleware:
    def __init__(self, app, settings):
        self.app = app
        self.settings = settings

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        request_id = scope.get("enat.request_id") or str(uuid4())
        headers = dict(scope.get("headers", []))
        path = scope["path"]
        maximum = (
            self.settings.max_request_bytes
            if headers.get(b"content-type", b"").startswith(b"multipart/form-data")
            else min(self.settings.max_request_bytes, 65536)
        )
        try:
            declared = int(headers.get(b"content-length", b"0"))
            if declared < 0:
                raise ValueError()
        except ValueError:
            return await JSONResponse(
                {"detail": "Invalid Content-Length"}, 400, headers=PRIVATE_HEADERS
            )(scope, receive, send)
        if declared > maximum:
            return await JSONResponse(
                {"detail": "Request body too large"}, 413, headers=PRIVATE_HEADERS
            )(scope, receive, send)
        try:
            if self.settings.enable_request_limits and path not in {
                "/health",
                "/ready",
            }:
                # Trust only ASGI peer address. Proxy headers are configured at
                # the server with an explicit trusted proxy IP list, never '*'.
                peer = (scope.get("client") or ("unknown",))[0]
                category = (
                    "auth"
                    if path.startswith("/auth/")
                    else "public"
                    if path.startswith("/summary/")
                    else "api"
                )
                await run_in_threadpool(
                    take_rate, peer, category, 10 if category == "auth" else 60
                )
        except ApplicationError as exc:
            return await error_response(exc)(scope, receive, send)
        # Count chunks even when Content-Length is missing or forged. No provider
        # or downstream parser sees a partial body before this bound is checked.
        chunks = []
        size = 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            size += len(message.get("body", b""))
            if size > maximum:
                return await JSONResponse(
                    {"detail": "Request body too large"}, 413, headers=PRIVATE_HEADERS
                )(scope, receive, send)
            chunks.append(message.get("body", b""))
            if not message.get("more_body", False):
                break
        body = b"".join(chunks)
        delivered = False

        async def replay():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": body, "more_body": False}
            return await receive()

        started = False

        async def private_send(message):
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
                additions = [
                    (k.lower().encode(), v.encode()) for k, v in PRIVATE_HEADERS.items()
                ]
                original = [
                    (k, v)
                    for k, v in message.get("headers", [])
                    if k.lower() not in {a[0] for a in additions}
                ]
                message = {
                    **message,
                    "headers": original
                    + additions
                    + [(b"x-request-id", request_id.encode())],
                }
            await send(message)

        try:
            await self.app(scope, replay, private_send)
        except ApplicationError as exc:
            if started:
                raise RuntimeError("Response failed after headers") from None
            await error_response(exc)(scope, replay, private_send)
        except Exception:
            if started:
                raise RuntimeError("Response failed after headers") from None
            logging.getLogger("enat.security").error(
                "request_failed request_id=%s", request_id
            )
            await JSONResponse(
                {"detail": "Internal server error"}, 500, headers=PRIVATE_HEADERS
            )(scope, replay, private_send)
