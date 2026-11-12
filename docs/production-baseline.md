# Production baseline — 13 October 2026

Scope: Phase 0 of `production_readiness_plan.md`, starting from revision
`14975c2`. This baseline does not authorize patient production use or close
Phases 1–5. No production services, credentials, grants, or data were accessed.

## Runtime and verification

Supported runtime: Python 3.12 on Linux. Runtime and development dependencies have separate
hashed lockfiles; development resolution is constrained to the runtime lock.
APScheduler is constrained below version 4 because the current adapter uses its
version 3 API. CI installs from the development lock, runs dependency consistency
and undefined-name checks, and runs tests with dummy configuration and sockets
blocked. The import test visits every application module; lifecycle tests run
startup/shutdown repeatedly and verify scheduler cleanup after an exception.

Initial system-Python command: `python3 -m pytest tests -q` failed before collection
with `ModuleNotFoundError: pytest_asyncio`. No initial pass rate was inferred.
After installing the locked dependencies, an untouched snapshot of `14975c2`
still failed collection with four errors caused by undefined `settings` in
`app/dependencies.py`. The snapshot was tested separately; the working tree was
not reverted.

Final local results:

- Hash-checked install from `requirements-dev.lock`: succeeded (72 packages).
- `python -m pip check`: no broken requirements.
- `ruff check app tests scripts`: passed.
- `python -m pytest -q`: 98 passed. Existing UTC/dependency deprecations and
  blocked network-attempt warnings remain visible; no test failed or skipped.
- Migrations 001–004: all applied to a fresh PostgreSQL 16 cluster. Eight tables
  found; seven with RLS, zero policies, no Telegram columns, no `push_tokens`.
- `git diff --check`: passed.

CI workflow is added; a hosted GitHub Actions run has not been observed.
No vulnerability scan, live Supabase isolation test, load test, or restore drill
is claimed by these results.

The undefined `settings`, `Depends`, and `uuid4` references are repaired. The
stage-audio URL guard now checks for a string instead of referencing an undefined
test-mock class. Authentication semantics and clinical rules are otherwise
unchanged in this milestone and remain release blockers.

## Configuration and operating behavior

`.env.example` lists all Settings fields. `ENVIRONMENT` selects development,
test, staging, or production. Development endpoints and embedded scheduling
default off. Staging and production reject either flag; they require HTTPS
service/frontend URLs and an explicit HTTPS CORS allowlist. No frontend or
Telegram origin is implicitly allowed. Configure each client origin explicitly.

Automatic reminders do not run by default. The existing scheduler is available
only by explicit opt-in outside staging/production and uses Africa/Addis_Ababa.
A durable worker is required before enabling production reminders. `/health`
is process liveness, not database/provider readiness.

## Schema inventory

Migrations 001–004 are the repository schema baseline. Their contents were
compared against repository reads and writes. Fresh-install verification uses
an isolated PostgreSQL 16 cluster with no TCP listener or application credentials;
it does not establish Supabase Auth/Storage behavior or production grants.

| Resource | Schema gap / next work |
| --- | --- |
| `users` | `telegram_id`, `first_name`, `username` referenced by UserRepository are absent. Preserve existing identity IDs in the forward migration. |
| `push_tokens` | Entire table absent. Define ownership and durable registration before enabling this feature. |
| `stage_audio_prompts` | Table exists without RLS. Define public-read/backend-write grants for generic prompts. |
| Seven patient/workflow tables | RLS enabled but no policies supplied. Backend uses a service-role client, which bypasses RLS. Phase 1 must establish and test the actual data role. |
| `check_in_sessions`, `check_ins` | No session version or unique finalization linkage; Phase 2 requires transactional finalization and stale-write detection. |
| `summaries` | Legacy public slug stored on snapshot; no expiry, revocation, or separate share lifecycle. |
| Jobs/outbox | No durable job, lease, or deduplication tables; Phase 3 work remains. |

Upgrade/backfill rehearsals, role-isolation tests, and live grants audits remain
open. This milestone intentionally adds no schema migration before those identity,
sharing, and transaction designs are implemented together.

## External services, storage, and consumers

| Boundary | Current repository behavior / configuration |
| --- | --- |
| Supabase Auth | `SUPABASE_URL`, service-role key and JWT secret; signup/login/recovery and server-side JWT validation. Verified signup and strict token policy remain Phase 1 blockers. |
| Supabase data API | Same service-role client used by repositories; no direct PostgreSQL application role yet. |
| Addis AI | `ADDIS_API_KEY`, `ADDIS_API_BASE_URL`; STT, extraction and TTS send voice/text externally. |
| Google TTS | Automatic gTTS fallback still exists. Approval/disablement is part of Phase 1. |
| Telegram | `TELEGRAM_BOT_TOKEN`; signed launch data supported, but freshness and empty-token rejection remain Phase 1 work. |
| `summary-qr-codes` | Legacy public QR upload; private artifacts and expiring shares remain required. |
| `audio-prompts` | Generic stage audio, public URLs and generated MP3 uploads. Project-specific fallback URL remains F17 work. |
| Calendar links | Google Calendar URLs and downloadable iCalendar content, created by the backend. |
| Web and Telegram Mini App clients | Inferred from auth routes, frontend API guide, and old CORS entries. Actual deployed client versions/owners were not verified. |
| Postman | Tracked collection and generator exist; full contract synchronization remains Phase 4. |

Legacy `FRONTEND_URL` handling in QR creation and the hardcoded prompt storage
fallback still require consolidation in F17. The new template documents the
canonical Settings names without claiming these older code paths are removed.

## Remaining release decisions

Identity linking and trusted database role, consent/share scope and expiry,
clinical rule approval, processor approval/retention, and durable-job delivery
semantics still need their planned implementation and review. Capacity and
recovery targets in the plan remain proposals without measured evidence.
