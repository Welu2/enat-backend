# Phase 2 workflow integrity — 13 October 2026

The local implementation covers transactional check-ins, explicit confirmation,
retry keys, exact report windows, preserved collections, and explicit appointment
attendance. It is not clinical approval or a production deployment.

## Contracts and persistence

- Check-in mutations require `Idempotency-Key`; all session mutations after start
  also require `X-Session-Version`. Responses include version and stage status.
  `GET /checkin/{id}/state` supports reconnect/resume. Stale mutations return 409.
- Verification accepts a bounded `items` list with `verify`, `add`, and `discard`
  operations. Unknown IDs are rejected, including for a single pending item.
  Typed stage fields reject server metadata, unknown categories, malformed
  durations, nonboolean confirmation, and fields belonging to another stage.
- Each provider operation reads state before calling the provider, holds no
  database transaction during that call, and compares the version when saving.
  Database operations in these async paths run in the framework thread pool.
  Failed or stale calls leave the draft untouched.
- Finalization locks the owned session, validates confirmation/provenance,
  creates one check-in under a unique `session_id`, marks the session completed,
  records its terminal response, and writes an outbox event in one transaction.
  Completion retries return the original result even with a new or missing key
  at the service boundary. The HTTP contract requires the key.
- Retry records are scoped by owner and operation, with a canonical request hash
  and committed JSON result. Changed requests using the same key return 409.
  Start, verify, audio mutations, completion, manual intake, manual reports, and
  dedicated appointment creation/rescheduling/attendance requests use this mechanism. Automatic reports use a server key
  per appointment/date/contact or calendar month, backed by a unique index.
- Snapshot insertion, outbox insertion, and the retry result share a transaction.
  Summary UPDATE is rejected by a database trigger even for the migration owner;
  the application has only SELECT/INSERT privileges. Shares remain separate.
- Outbox events are durable but not consumed yet. Phase 3 implements workers,
  leases, retries, and delivery. No notification delivery is implied by an event.
- Duplicate simultaneous provider requests can still incur duplicate provider
  calls before one domain result commits; shared quotas remain active. A provider
  reservation/lease workflow belongs to Phase 3.

## Clinical information and uncertainty

`clinical-conservative-v1` is the shared normalization rule. Recognized danger
categories are preserved regardless of the severity label. Null/unclassified
observations and missing assessments remain uncertain, rather than producing
"No danger signs detected." Verification exposes a confirmed warning before
unrelated stages finish. The existing danger-warning wording is retained.

Only exact JSON `confirmed:true` observations enter new permanent check-ins or
reports. Server-owned provenance includes source item, confirmation instant,
policy version, and available prompt/model versions. `intake-v2` identifies the
extraction prompt; model version remains null because the current provider
response does not expose a stable identifier. A null legacy confirmation time
is labeled unknown, never fabricated.

Food and supplement values are arrays in session drafts, final records, and
history responses. Multiple verified items are retained. The manual meal form
preserves all supplied food names and explicit food-group selections together
as one meal observation. Unknown supplements stay unknown; manual supplement
logging requires an explicit selected ID or name. The supplement voice stage is
skipped only when every active named supplement has a confirmed boolean report
on the local day. Logging one supplement does not dismiss unrelated reminders.

Report queries use `[window_start, window_end)` and return all matching PostgreSQL
rows without a PostgREST response cap. Empty results stay empty; database errors
propagate as retriable 503 responses. Default reports cover at most 30 days, from
the latest of account creation, 30 days ago, and a recorded previous attended
appointment. Explicit aware bounds may span up to 366 days and cannot end in the
future. Output date labels use the supported local calendar.

Adherence is calculated per named supplement and local day. Conflicting reports,
unknown values, and absent reports are unknown. Percentages use known observations
only; the response states that denominator and includes per-supplement counts.
They do not estimate adherence over unobserved days.

Reports never change appointment attendance or contact number. Explicit
`completed`, `missed`, and `rescheduled` transitions check a version and append an
attendance event. Rescheduling requires a date; selecting another ANC contact is
explicit. Future visits cannot be marked completed/missed. Completed attendance
records the previous appointment date; neither missed attendance nor report
creation advances it.

UTC-aware timestamps are used for persistence and database sessions. Local dates
and 09:00 appointment calendar exports use `Africa/Addis_Ababa`. Services and
repositories accept an injected clock; gestational calculations also accept an
explicit `as_of_date`.

## Migration and client rollout

1. Rehearse migrations 001–007 using the fresh and synthetic-upgrade harness.
   Inspect actual grants, data shape, row counts and locks in staging before
   applying migration 007 to a deployed database. It backfills existing JSON and
   needs a planned maintenance window appropriate to the data volume.
2. Coordinate the API and frontend release. Old single-item verification bodies,
   omitted retry/version headers, singleton history consumers, and automatic
   appointment-advancement assumptions are incompatible. The
   [frontend guide](../frontend_api_guide.md) and regenerated
   [Postman collection](../EnatAI_Postman_Collection.json) describe the contract.
3. Migration 007 wraps legacy singleton JSON without manufacturing confirmation.
   Missing/invalid confirmation is marked `legacy_unverified` and excluded from
   reports. Historical confirmed observations remain readable; unavailable
   provenance stays null. Historical snapshots remain unchanged.
4. Pre-migration in-progress sessions are expired, retaining their drafts for
   inspection. Clients must start a new session and confirm again. Their old
   content cannot be silently finalized under the new provenance rules.
5. Do not roll back to an older binary against this schema: it can write neither
   the required collections nor confirmation provenance. Roll back to a tested
   compatible image or forward-fix. Do not drop uniqueness/RLS/triggers to make an
   old client appear compatible. No deployed migration has been performed here.

QR rendering occurs after share creation commits. If it fails, share creation
returns its usable URL with `qr_status:"retry_required"` and null PNG. An owner
can retry `POST /summary/shares/{id}/qr` with the retained token; no new snapshot
or share is created. Revoked, expired, or another owner's shares cannot be rendered.
Tokens remain hashed in the database; the retry body and response are private.
Sharing still defaults off pending the Phase 1 privacy review.

Mutation results contain sensitive response data. They are retained with the
account and are not silently expired, which would weaken retry guarantees.
Retention/deletion policy and any future bounded idempotency horizon require
review before release. Existing account foreign-key cascades cover these records.

## Verification and remaining release gates

Run from the Python 3.12 virtual environment:

```sh
.venv/bin/ruff check app tests scripts
.venv/bin/python -m pytest -q
.venv/bin/python scripts/test_database.py --fresh
.venv/bin/python scripts/test_database.py
.venv/bin/python scripts/scan_secrets.py
.venv/bin/python -m pip check
```

Local result: **157 unit tests passed**; isolated PostgreSQL **37 fresh-install
and 39 upgrade tests passed**. The fresh run skips two upgrade-only cases. Lint,
dependency consistency and `git diff --check` passed; the tracked/history secret
pattern scan reported zero findings. The test client dependency emits a known
deprecation warning. Hosted CI was not observed.

The suite exercises concurrent finalization and verification, delayed voice and
transcription races, failure injection before session commit and during outbox
writes, retry-key scoping/conflicts, multiple foods/supplements, malformed and
forged corrections, missing confirmation, exact boundaries with over 1,000 rows,
immutable snapshots, automatic-report deduplication, local midnight, migration
compatibility, and an authenticated confirm → complete → report → share → revoke
flow. The database role/RLS tests from Phase 1 also run against migration 007.

Clinical acceptance remains open. A qualified reviewer must approve the policy,
localized warning/uncertainty wording, attendance semantics, and expected outcomes
for Amharic negation, ambiguous categories, code switching, noisy recordings,
severe versus mild descriptions, and corrections that change a warning. Existing
provider examples and deterministic tests are engineering evidence, not a
clinician-labeled evaluation corpus. Live ASR/extraction quality has not been
measured. No reviewer approval is recorded or implied.

Frontend/staging migration rehearsal, live Supabase checks, privacy approvals,
worker delivery, hosted CI, load testing, and operational release gates remain
open. No production data, credentials, or live services were changed.
