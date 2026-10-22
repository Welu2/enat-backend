"""Generate/check OpenAPI and validate every Postman example against live routes."""

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def application():
    # Schema generation never needs live credentials, network calls, or .env contents.
    os.environ.update(
        {
            "ENVIRONMENT": "test",
            "PROCESS_ROLE": "api",
            "ENABLE_DEV_ROUTES": "false",
            "ENABLE_EMBEDDED_SCHEDULER": "false",
            "DATABASE_URL": "",
            "WORKER_DATABASE_URL": "",
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "contract-placeholder",
            "SUPABASE_PUBLISHABLE_KEY": "contract-placeholder",
            "SUPABASE_JWT_SECRET": "contract-placeholder",
            "ADDIS_API_KEY": "contract-placeholder",
            "ADDIS_API_BASE_URL": "https://provider.invalid",
            "ENABLE_REQUEST_LIMITS": "false",
            "ENABLE_SUMMARY_SHARING": "false",
            "ENABLE_PRIVACY_TOOLS": "false",
            "ENABLE_CARE_PORTAL": "false",
            "ENABLE_OFFLINE_CHECKINS": "false",
            "PRIVACY_POLICY_VERSION": "",
            "PRIVACY_SUPPORT_URL": "",
            "TELEGRAM_BOT_TOKEN": "",
            "LEGACY_HS256_UNTIL": "",
            "PUBLIC_BASE_URL": "http://localhost:3000",
            "CORS_ORIGINS": "http://localhost:3000",
            "TRUSTED_HOSTS": "testserver,localhost",
            "RATE_LIMIT_SECRET": "contract-placeholder-at-least-32-characters",
        }
    )
    from app.config import get_settings

    get_settings.cache_clear()
    from app.main import create_app

    return create_app()


def requests(items):
    for item in items:
        if "request" in item:
            yield item["name"], item["request"]
        yield from requests(item.get("item", []))


def check_examples(schema):
    from jsonschema import Draft202012Validator, FormatChecker

    collection = json.loads((ROOT / "EnatAI_Postman_Collection.json").read_text())
    count = 0
    failures = []
    for name, request in requests(collection["item"]):
        path = "/" + "/".join(request["url"]["path"])
        concrete = re.sub(
            r"\{\{[^}]+\}\}", "00000000-0000-4000-8000-000000000001", path
        )
        method = request["method"]
        matches = [
            p
            for p, methods in schema["paths"].items()
            if method.lower() in methods
            and re.fullmatch(re.sub(r"\{[^}]+\}", "[^/]+", p), concrete)
        ]
        if not matches:
            failures.append(f"{name}: unknown operation {method} {path}")
            continue
        route = sorted(matches, key=lambda p: p.count("{"))[0]
        operation = schema["paths"][route][method.lower()]
        headers = {
            h["key"].lower() for h in request.get("header", []) if not h.get("disabled")
        }
        if request.get("auth", collection.get("auth", {})).get("type") == "bearer":
            headers.add("authorization")
        required = {
            p["name"].lower()
            for p in operation.get("parameters", [])
            if p["in"] == "header" and p.get("required")
        }
        if missing := required - headers:
            failures.append(f"{name}: missing headers {sorted(missing)}")
        body = request.get("body", {})
        request_schema = (
            operation.get("requestBody", {})
            .get("content", {})
            .get("application/json", {})
            .get("schema")
        )
        if body.get("mode") == "raw" and request_schema is not None:
            raw = re.sub(
                r"\{\{([^}]+)\}\}",
                lambda m: (
                    "A" * 43
                    if m[1] in ("share_token", "share_link_slug", "invitation_token")
                    else "00000000-0000-4000-8000-000000000001"
                ),
                body["raw"],
            )
            validator = Draft202012Validator(
                {**request_schema, "components": schema["components"]},
                format_checker=FormatChecker(),
            )
            errors = list(validator.iter_errors(json.loads(raw)))
            if errors:
                failures.append(
                    f"{name}: invalid JSON body: "
                    + "; ".join(e.message for e in errors)
                )
        elif body.get("mode") == "formdata":
            multipart = (
                operation.get("requestBody", {})
                .get("content", {})
                .get("multipart/form-data", {})
                .get("schema", {})
            )
            if "$ref" in multipart:
                multipart = schema["components"]["schemas"][
                    multipart["$ref"].rsplit("/", 1)[-1]
                ]
            fields = {
                field["key"]: field
                for field in body.get("formdata", [])
                if not field.get("disabled")
            }
            if missing := set(multipart.get("required", [])) - fields.keys():
                failures.append(f"{name}: missing multipart fields {sorted(missing)}")
            for key, field in fields.items():
                expected = multipart.get("properties", {}).get(key)
                if expected is None or (
                    expected.get("format") == "binary" and field.get("type") != "file"
                ):
                    failures.append(f"{name}: invalid multipart field {key}")
        elif operation.get("requestBody", {}).get("required"):
            failures.append(f"{name}: required body missing")
        if (
            operation.get("security")
            and request.get("auth", collection.get("auth", {})).get("type") != "bearer"
        ):
            failures.append(f"{name}: bearer auth missing")
        count += 1
    if failures:
        raise SystemExit("\n".join(failures))
    print(
        f"{count} Postman examples match current routes, bodies, required headers and authentication"
    )


def invariants(schema):
    for path in (
        "/checkin/history",
        "/notifications",
        "/reminders",
        "/users/me/supplements",
    ):
        operation = schema["paths"][path]["get"]
        parameters = {
            p["name"]: p["schema"]
            for p in operation["parameters"]
            if p["in"] == "query"
        }
        if (
            parameters["limit"].get("default") != 50
            or parameters["limit"].get("maximum") != 100
            or "cursor" not in parameters
        ):
            raise SystemExit("Pagination contract drift: " + path)
        if "X-Next-Cursor" not in operation["responses"]["200"].get("headers", {}):
            raise SystemExit("Missing continuation header: " + path)
    for method, path, expected in (
        ("post", "/tts", {"audio/mpeg", "audio/wav"}),
        ("get", "/checkin/prompts/{stage}/audio", {"audio/mpeg", "audio/wav"}),
        ("post", "/summary/shares/{share_id}/qr", {"image/png"}),
        ("get", "/users/me/appointment/calendar.ics", {"text/calendar"}),
    ):
        if (
            set(schema["paths"][path][method]["responses"]["200"]["content"])
            != expected
        ):
            raise SystemExit(f"Binary/text response contract drift: {path}")
    public = {
        ("get", "/health"),
        ("get", "/tts"),
        ("get", "/checkin/prompts"),
        ("get", "/checkin/prompts/{stage}/audio"),
        ("get", "/summary/{share_link_slug}"),
        ("post", "/users/calculate-gestational-age"),
        *[
            ("post", "/auth/" + p)
            for p in (
                "signup",
                "login",
                "refresh",
                "forgot-password",
                "reset-password",
                "telegram",
            )
        ],
    }
    for path, methods in schema["paths"].items():
        if path.startswith("/dev/"):
            raise SystemExit("Development endpoint leaked into default OpenAPI")
        for method, operation in methods.items():
            if (method, path) not in public and not operation.get("security"):
                raise SystemExit(f"Missing bearer contract: {method} {path}")
            for code in ("401", "409", "422", "429", "503"):
                if (
                    operation["responses"][code]["content"]["application/json"][
                        "schema"
                    ].get("$ref")
                    != "#/components/schemas/ErrorResponse"
                ):
                    raise SystemExit(f"Error envelope drift: {method} {path} {code}")
            if path.startswith("/checkin/{session_id}/") and method == "post":
                required = {
                    p["name"]
                    for p in operation.get("parameters", [])
                    if p.get("required")
                }
                if not {"Idempotency-Key", "X-Session-Version"} <= required:
                    raise SystemExit(f"Missing mutation concurrency contract: {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    app = application()
    schema = app.openapi()
    invariants(schema)
    check_examples(schema)
    artifacts = {
        "docs/openapi.json": json.dumps(
            schema, ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n"
    }
    lines = [
        "# Generated API operations",
        "",
        "Generated by `python scripts/check_contracts.py --write`. Do not edit by hand.",
        "",
        "Bodies and response schemas: [OpenAPI](openapi.json). Behavior: [frontend guide](../frontend_api_guide.md).",
        "",
        "| Method | Path | Bearer required | Required headers |",
        "|---|---|---|---|",
    ]
    for path, methods in sorted(schema["paths"].items()):
        for method, operation in sorted(methods.items()):
            headers = ", ".join(
                p["name"]
                for p in operation.get("parameters", [])
                if p["in"] == "header" and p.get("required")
            )
            lines.append(
                f"| {method.upper()} | `{path}` | {'yes' if operation.get('security') else 'no'} | {headers or '—'} |"
            )
    artifacts["docs/api-operations.md"] = "\n".join(lines) + "\n"
    stale = []
    for name, content in artifacts.items():
        path = ROOT / name
        if args.write:
            path.write_text(content)
        elif not path.exists() or path.read_text() != content:
            stale.append(name)
    if stale:
        raise SystemExit(
            f"Contract artifacts are stale: {', '.join(stale)}. Run scripts/check_contracts.py --write"
        )
    print("OpenAPI and operation inventory are current")


if __name__ == "__main__":
    main()
