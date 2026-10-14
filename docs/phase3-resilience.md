# Phase 3 background work and provider resilience

Local implementation record, 13 October 2026. Migration 008 follows migrations
001–007. No deployed database, provider account, or storage bucket was changed.

## Processes and credentials

The API no longer starts a scheduler. `ENABLE_EMBEDDED_SCHEDULER=true` is rejected
in every environment; the development-only `/reminders/run-daily` returns 410.
APScheduler and its unused timezone dependency were removed from both lockfiles.

Deploy the same application revision as separate processes:

```bash
# API environment: PROCESS_ROLE=api, DATABASE_URL using enat_app, API secrets.
python -m uvicorn app.main:app

# Separate worker environment: PROCESS_ROLE=worker, WORKER_DATABASE_URL using enat_worker.
python -m app.jobs scheduler
python -m app.jobs worker
python -m app.jobs status
```

Worker mode requires no Supabase/Auth/Storage/provider credentials or API database
credential. Set `ENVIRONMENT`, `PROCESS_ROLE=worker`, `WORKER_DATABASE_URL`, and
optionally `REMINDER_CRON_HOUR`. Provision login/password/TLS through the existing
secret-management process: migrations deliberately leave both database roles
NOLOGIN. Neither process may connect as owner, superuser, or BYPASSRLS. Do not
grant privileged role memberships. Keep the worker credential out of API instances.
The API rejects worker configuration. Workers cannot change check-ins, appointments,
or immutable snapshots, or read authentication identities, push tokens, or shares.
Their patient reads and snapshot/reminder writes use transaction-local owner RLS.

## Scheduling, delivery, and recovery

The scheduler uses the Addis Ababa calendar and the configured daily hour (06:00
by default). Each transaction enqueues at most 100 users, ordered by UUID, and
commits its cursor with the jobs. The scheduler row has a 30-second renewable
lease and a row lock; a replacement resumes the saved cursor after expiry.
Unique user/date job keys make repeated pages harmless. The first deployment
starts with the current local date. Users joining after a day's cursor passes
them enter the next day's scan. Disabled accounts are excluded.

Missed days remain represented by durable jobs. Workers consume old daily jobs
without issuing stale supplement prompts or manufacturing historical reports from
today's profile. Current-day work follows through the same cursor. Already created
reminders keep their original due times. Historical unkeyed reminders remain
unchanged; review same-day reminders when replacing a previously active legacy
scheduler. Pause that scheduler before enabling these workers.

Workers claim one due job using `FOR UPDATE SKIP LOCKED`, with a random lease
token, 60-second expiry, and 15-second heartbeat. A killed worker's lease becomes
claimable. Completion, heartbeat, and failure updates require the current token
and an unexpired lease. Handler effects are independently idempotent: supplement
keys include the supplement ID, appointment keys include appointment/date, and
automatic summaries retain Phase 2 generation keys. A crash after an effect but
before acknowledgement may repeat the handler without duplicating the effect.

Ordinary failures receive exponential backoff with jitter, five attempts by
default, and a terminal `failed` state. An expired final attempt also becomes
failed. A failed user does not stop another job. Exception bodies and patient text
are never saved as job errors. SIGTERM/SIGINT stop polling after the current job;
forced termination is recovered through its lease.

The scheduler also converts committed outbox rows into uniquely keyed delivery
jobs in bounded pages. `checkin.completed` and `summary.created` produce generic
in-app notifications exposed by the existing notification/reminder APIs. The
notification and outbox delivery timestamp commit together. Delivery does not
mean push, SMS, or email; none of those external transports is configured here.
Unsupported events fail visibly and require a handler before replay. A disabled
account's event is consumed without a new notification.

### Failed-job procedure

1. Run `python -m app.jobs status`. Inspect pending/failed counts and oldest due
   age; scheduler lag measures the saved occurrence relative to its due hour.
   Alert on failed jobs or lag over five minutes in the deployment monitoring.
2. With the worker database credential, list bounded metadata only:

   ```sql
   SELECT id, kind, attempts, last_error, finished_at
   FROM background_jobs WHERE status='failed'
   ORDER BY finished_at, id LIMIT 100;
   ```

3. Repair the failed dependency or handler, then replay a specific job:

   ```bash
   python -m app.jobs replay --job-id JOB_UUID
   ```

4. Replay only changes failed jobs to pending, increments `replay_count`, resets
   the attempt budget, and preserves job/domain deduplication keys. Verify a
   subsequent successful status and decreasing backlog. Never delete the queue
   row or invent a new deduplication key to force an already-applied domain effect.

## Provider behavior and client recovery

Each API event loop owns one HTTPX client closed at shutdown, bounded to
`PROVIDER_CONCURRENCY` connections. Connect/read/write/pool timeouts are 3/15/10/2
seconds. Each request has a 20-second wall-clock limit; an ASR-plus-extraction
turn shares one 45-second deadline, including retries and capacity waits. These
limits are configurable within validated bounds. Lease cleanup may add bounded
database cleanup time after cancellation (connection/statement limits are five
seconds). No database transaction spans provider work.

Only connection failures and HTTP 429/503 get one automatic HTTP retry. Long or
date-form `Retry-After` values return a recoverable error rather than being ignored.
Read/write timeouts are not automatically repeated because a provider may have
already charged. Extraction permits two schema attempts; the whole operation
permits at most four HTTP attempts. Every attempt consumes the existing daily
user/global budgets and distributed concurrency lease. Retries can still incur
charges; production currency budgets and actual billing need vendor verification.

Three failed requests open a local circuit for 30 seconds; one probe can restore
it. Circuits are per API process; concurrency/budget admission remains distributed.
JSON shapes/text sizes, streamed response sizes, base64, and audio signatures are
validated. JSON errors cannot be returned as successful audio. Provider failures
return private 503 responses with `code=provider_unavailable`, `draft_preserved`,
`recovery=[retry,manual_input]`, and `Retry-After`. Existing drafts and retry keys
remain usable. The frontend must offer resume/retry/manual input.

Database operations in async check-in/provider paths use the bounded thread pool;
generic storage downloads are now offloaded too. `IO_THREAD_LIMIT` defaults to 16.
Synchronous routes already use FastAPI's thread pool. Production capacity and
event-loop latency still require Phase 5 measurement.

## Versioned generic prompt provisioning

Generic prompt URLs now include a hash of the checked-in Amharic prompt and voice
version. `stage_audio_prompts` is retained for legacy data; current metadata comes
from the versioned code constants. Provision before deploying the new URLs:

```bash
# Separate API/provisioning credentials and an approved operator account/budget.
python -m app.provision_prompts --operator-user-id OPERATOR_UUID --output /tmp/enat-prompts
```

This explicit command writes four MP3 files and a manifest locally. Have the
approved reviewer check the audio, then upload the manifest's exact paths to the
public `audio-prompts` bucket using a privileged provisioning credential. Use
immutable cache headers for those versioned objects. Check each manifest URL in
staging and retain previous versions through the client rollout. No patient text
is accepted by this command. No synthesis or upload occurs during API requests
or startup. Storage cache entries use project plus versioned path, expire after
one hour, and share a 16MB byte cap. A missing or invalid stored asset fails
without calling the speech provider. Patient TTS is never cached here.

## Verification and release gates

The unit and isolated PostgreSQL suites cover transport failures, 429/503/500,
malformed payloads/audio, operation deadlines, retry multiplication, pool reuse,
draft preservation, nonblocking storage reads, more than 1,000 scheduled users,
two schedulers, concurrent claims, lease fencing/heartbeat/replay, separate worker
grants, outbox rollback, two simultaneous supplements, automatic-summary retries,
and actual process death after a domain effect followed by CLI worker restart.
Results: **182 unit tests**, **49 fresh-install PostgreSQL tests** (two upgrade-only
skips), and **51 legacy-upgrade PostgreSQL tests** passed. Lint, dependency
consistency, whitespace checks, and the secret-pattern scan passed. Existing
test/dependency deprecation warnings remain; hosted CI was not run locally.

Release still requires staging credential/grant audit, process supervision and
alerts, prompt generation/review/upload and CDN checks, provider latency/billing
verification, frontend recovery behavior, and the earlier clinical/privacy gates.
The migration and application rollout must be rehearsed. Roll back by stopping
new schedulers/workers and restoring the prior API image without dropping queue
or occurrence data; keep old embedded scheduling disabled. Phase 5 owns backups,
retention, monitored capacity, and restore/rollback exercises.
