# Clinician portal and offline check-in MVP implementation plan

Build a clinician portal for approved patients, a limited portal for one trusted person per patient, and offline structured check-ins that sync without duplicates. Reuse the existing FastAPI, PostgreSQL, authentication, clinical validation, appointments, summaries, and transaction infrastructure.

This is an implementation specification for a coding agent. The work includes backend changes in this repository and frontend integration in the patient application. Backend completion alone does not complete the product MVP. This checkout currently contains no frontend application; obtain its repository before beginning the frontend milestone. Continue the backend milestones independently.

## MVP decisions

| Area | Required behavior |
|---|---|
| Clinician provisioning | An operator enables an existing authenticated account as a clinician. No public clinician signup or self-assigned role. |
| Patient connection | The patient invites a specific account; that account accepts while signed in. Clinician access also requires an active clinician profile. |
| Trusted person | At most one pending or active trusted-person connection per patient. A trusted person can support several patients. |
| Clinician permissions | Read linked patient identity, pregnancy overview, confirmed check-ins, latest summary, appointments, and emergency alerts; acknowledge alerts. |
| Trusted-person permissions | Read linked patient display name, upcoming appointment, and alerts created since that connection became active. No clinical history or summaries. |
| Patient control | View pending/active connections and revoke either immediately. Clinician consent explicitly includes existing confirmed history and summaries. |
| Emergency definition | A completed, patient-confirmed check-in containing a danger category recognized by the existing server policy. This is an alert, not a new diagnosis. |
| Alert lifecycle | `unacknowledged` to `acknowledged`, by a linked clinician. Acknowledgement means seen, not treated or resolved. |
| Offline check-in | A cached structured form, explicitly reviewed and confirmed by the patient. Voice remains online. |
| Offline delivery | Foreground sync on app open, connectivity recovery, and manual retry. Background delivery while the app is closed is not an MVP guarantee. |
| Appointments | Reuse patient appointment management. Portal users have read-only access. |
| Exclusions | Clinician scheduling, chat, prescriptions, SMS/calls, push escalation, emergency dispatch, organization administration, offline voice processing, and medical-record integrations. |

Preserve existing clinical rules and release requirements. Do not enable disabled summary-sharing features as a shortcut for portal access. Synthetic-data demonstration readiness and approval for real patient use are separate outcomes already documented in the repository.

## Existing implementation to reuse

| Files | Implementation relevance |
|---|---|
| `app/dependencies.py`, `app/core/security.py` | Authentication and verified actor identity. Accounts are shared identities; a trusted-person relationship is not a global account role. |
| `app/db/data.py`, migration `005` | Restricted `enat_app` connection, transaction-local actor identity, and owner row-level security. |
| `app/models/clinical.py`, `app/services/clinical_policy.py` | Strict editable clinical fields, normalization, confirmation provenance, and deterministic danger classification. |
| `app/services/checkin_session.py`, `app/db/repositories/check_in_sessions.py` | Existing voice workflow with version checks and two-hour sessions. Offline forms must not replay expired voice sessions. |
| `app/db/repositories/check_ins.py`, `app/services/manual_intake.py` | Central persistence and existing structured manual intake examples. |
| `app/db/idempotency.py`, migration `007` | Transactional retry results and deduplicated outbox events. |
| `app/db/repositories/appointments.py` | Existing appointment state and version rules. |
| `app/services/summary.py` | Immutable snapshots, receipt-time report windows, and aggregation that currently uses check-in `timestamp` as the observation date. |
| `app/services/privacy.py`, migration `010` | Allowlisted exports and immutable audit patterns. |
| `app/core/readiness.py`, `.github/workflows/ci.yml` | Exact schema readiness and a pinned rollback bridge that must be updated for new migrations. |

Do not modify previously applied migrations. Proposed new migration names below assume `010` remains the latest migration; use the next available numbers if the repository changes.

## Database changes

### Migration 011 for care access and alerts

Create these tables with foreign keys, indexes, explicit grants, and row-level security. Use `timestamptz` for instants and existing UUID identifiers.

| Table | Required fields and constraints |
|---|---|
| `clinician_profiles` | `user_id` primary key referencing `users`, `display_name`, `active`, `created_at`, `updated_at`. Only the controlled provisioning operator can enable/disable profiles. |
| `care_connections` | `id`, `patient_id`, `recipient_id`, `relationship` (`clinician` or `trusted_person`), `status` (`pending`, `active`, `revoked`, `expired`), `consent_version`, `consented_at`, `created_at`, `accepted_at`, `revoked_at`, `expires_at`, `invite_token_hash`. Reject self-connections. Token hash is unique. |
| `emergency_alerts` | `id`, `patient_id`, `check_in_id` unique, recognized category codes, `recorded_at`, `received_at`, `created_at`, `policy_version`, `status`, nullable `acknowledged_at`, nullable `acknowledged_by`. Enforce coherent acknowledgement fields and check-in ownership. |
| `care_access_events` | Immutable `id`, `patient_id`, authenticated `actor_id`, `connection_id` when applicable, action, resource type/ID when applicable, row count for list reads, and server timestamp. No raw clinical text, credentials, tokens, or request bodies. |

Use a partial unique index for one pending/active trusted-person connection per patient and another for one pending/active connection per patient/recipient/relationship. Expire elapsed pending invitations under the same per-patient lock before checking these constraints. Pending invitations expire after 48 hours; active connections last until revoked or an account/profile is disabled.

Prevent alteration of connection ownership, relationship, consent, and token binding through arbitrary updates. Implement lifecycle changes through narrowly scoped database functions. Enforce alert ownership with a composite check-in foreign key or an equivalent database constraint, not only application code. Index active connections by recipient and patient, and alerts by patient plus creation time/ID.

### Migration 012 for offline submissions

Add the following to `check_ins`:

- `recorded_at`: observation/capture time; backfill existing rows from `timestamp`.
- `received_at`: server acceptance time; backfill from `timestamp`.
- `client_confirmed_at`: nullable, client-reported confirmation time.
- `capture_source`: `online` or `offline_form`; existing rows are `online`.
- `client_submission_id`: nullable UUID, unique together with `user_id` when present.
- `submission_hash`: nullable canonical hash of the submitted offline payload.

Backfill timestamps without manufacturing new patient-confirmation evidence. Set both times explicitly for every new online submission. Keep existing `timestamp` equal to server receipt time for API compatibility and existing report selection. Add an index on `(user_id, recorded_at, id)` for daily observation queries.

Migration 007 retains some legacy unverified rows while enforcing confirmation on subsequent updates. A timestamp-only backfill must not fail on those rows or turn them into confirmed history. Narrow the confirmation trigger's update coverage to clinical fields if necessary, retaining enforcement for every insert and every clinical-content update. Rehearse this with synthetic legacy unverified data; do not disable confirmation protection for normal application writes.

The permanent submission ID and hash provide duplicate protection even if old `mutation_results` entries are later removed. Do not impose one check-in per patient per day: separate legitimate submissions can happen on the same day.

## Authorization and connection lifecycle

Keep `current_user_id` as the authenticated actor. Never impersonate a patient by switching it to a patient ID from a URL. Do not use a service-role connection for portal queries or widen existing patient-table policies to every clinician.

Use narrowly scoped PostgreSQL functions for cross-patient portal projections and alert acknowledgement. Each function derives the actor from `enat_user_id()`, checks active accounts and the active connection, checks clinician activation where required, and returns only the explicitly permitted fields. Use a fixed `search_path`, bound inputs, no arbitrary SQL/table arguments, and no public execution grants. Grant only the required functions to `enat_app`; revoke execution from Supabase client roles. Existing patient-owned reads and writes remain protected by owner RLS.

Record successful portal reads and connection/acknowledgement transitions in `care_access_events` within the same transaction. Audit failure fails the operation. The app and worker must not directly rewrite or delete audit events. All portal responses use `Cache-Control: no-store`; portal clinical responses are never service-worker cached.

Connection flow:

1. Recipient signs in and obtains their account ID from `GET /portal/me`. For this pilot, they share that ID with the patient; do not build an account-search directory.
2. Patient selects relationship, supplies recipient ID, reviews permissions, and submits explicit consent. A clinician invitation requires an already-enabled clinician profile. Invalid recipients return a generic unavailable response without revealing account details.
3. Server generates a cryptographically random invitation token, stores only its hash, and returns the token once. The UI lets the patient copy/share it manually. No email/SMS delivery integration is required.
4. Recipient signs in and accepts using the token in the request body. It must match the bound recipient, be unexpired, and still be pending. Acceptance and audit are atomic.
5. Patient can revoke pending or active access. Requests started after revocation commits must be denied. Data already displayed cannot be recalled; clear portal state on the next refresh/access failure and on logout.

Invitation creation is intentionally not replayed through a result store containing the raw token. If its response is lost, the patient lists connections, revokes the pending invitation, and creates another. Repeating acceptance of the same token by its bound recipient may return the existing active connection; it must never reactivate revoked/expired access or change the recipient. Concurrent acceptance has one state transition and one audit event.

Use the existing login/signup flow for all users. Add a controlled operator command or documented parameterized SQL for enabling/disabling clinician profiles by existing user ID. Keep operator credentials out of the API/worker configuration. Deactivation must block clinician access and acknowledgement immediately, including existing authenticated sessions.

## API contracts

Implement strict Pydantic request and response models; reject unknown mutation fields. These are new endpoints. Preserve existing patient endpoints and conventions.

| Method and path | Contract |
|---|---|
| `GET /portal/me` | Own account ID, display name, enabled clinician capability. Does not require patient onboarding. |
| `POST /users/me/care-connections` | `{recipient_id, relationship, consent: true}`. Returns 201 with connection metadata, expiry, and one-time token. Consent version is server-owned. |
| `GET /users/me/care-connections` | Patient-owned connection metadata and recipient display name; never token/hash. |
| `DELETE /users/me/care-connections/{id}` | Revoke an owned connection; repeated revocation returns 204. Another patient's ID returns 404. |
| `POST /care-connections/accept` | `{token}` under recipient authentication. Returns active connection ID and relationship, without patient clinical data. |
| `GET /portal/patients` | Connected patient cards: patient ID/display name, relationship, next appointment, unacknowledged alert count within permitted visibility. |
| `GET /portal/patients/{patient_id}` | Clinician only: ID/display name, stored pregnancy overview with an as-of date, hospital, latest check-in receipt time. Explicitly exclude credentials and unrelated profile fields. |
| `GET /portal/patients/{patient_id}/check-ins` | Clinician only: paginated confirmed history with both timestamps. No session drafts or pending extracted items. |
| `GET /portal/patients/{patient_id}/summary/latest` | Clinician only: latest immutable structured summary; return 404 if none. Never return bearer sharing links. |
| `GET /portal/patients/{patient_id}/appointment` | Both relationships: current scheduled appointment on/after today in `Africa/Addis_Ababa`, or `null`. Return date, hospital, ANC contact title, status, and version; do not fabricate appointment times. |
| `GET /portal/patients/{patient_id}/alerts` | Both relationships: bounded alert list, optional status filter. Clinicians see available alert history; trusted people only alerts created at/after connection acceptance. |
| `POST /portal/patients/{patient_id}/alerts/{alert_id}/acknowledge` | Clinician only; requires `Idempotency-Key`. First acknowledgement wins; repeats return current acknowledgement without overwriting the first actor/time. |
| `POST /checkin/offline-sync` | Submit one confirmed structured check-in. Requires `Idempotency-Key` equal to `client_submission_id`. Returns 200 for first acceptance and identical retries. |

List endpoints default to 50 and cap at 100, using stable keyset cursors and `X-Next-Cursor`. Choose/document a deterministic ordering per endpoint; alert/history lists use descending receipt/creation time plus UUID, patient/connection lists can use UUID ordering. Recheck permissions on every page. A forged cursor never expands authorization.

Return 401 for missing/expired authentication, 404 for inaccessible resources/relationships, 409 for conflicting duplicate payloads or connection slots, 422 for invalid submissions, and existing 429/503 responses for retryable limits/dependencies. Reuse the repository's error envelope and request IDs. Return only curated alert fields to trusted people: alert ID, recognized category labels, recorded/received times, status, and acknowledged time. Exclude raw check-in text, full profile, clinician identity, supplements, food logs, and summary content.

## Offline submission contract and processing

Example request body, using the patient's own authentication:

```json
{
  "schema_version": 1,
  "client_submission_id": "eb211034-f516-4aa1-baa9-cf352f93c8bc",
  "recorded_at": "2026-10-22T08:30:00+03:00",
  "client_confirmed_at": "2026-10-22T08:32:00+03:00",
  "confirmed": true,
  "symptoms": [
    {
      "raw_text": "Patient-entered symptom text",
      "category": "severe_headache",
      "severity": "unspecified"
    }
  ],
  "food_log": [],
  "supplement_check": [],
  "closing_mentions": []
}
```

Use existing editable field schemas for each collection. Require all four arrays, with no more than 50 entries each and 100 total; cap the request body at 64 KiB. Require at least one observation. An explicit no-symptoms answer can be a symptom entry with patient-visible text and `category: null`; an empty submission must not imply the patient is well. Never classify arbitrary free text as safe.

Require strict `confirmed: true`, schema version 1, timezone-aware times, and `recorded_at <= client_confirmed_at <= received_at + 5 minutes`. Reject larger future clock skew with a correctable validation error. Accept older submissions without silently dropping them. Client timestamps are patient-device reports, not trusted server evidence.

Processing must follow this order:

1. Authenticate, enforce body limits, and validate the versioned request shape. Derive patient ID solely from the authenticated actor.
2. Compute a canonical hash of all submitted semantic fields, normalizing timestamps to UTC. Lock the patient/submission pair and check permanent duplicate identity before time-relative checks. An accepted retry remains valid later even if policy or time has changed.
3. For an existing ID with the same hash, return the original check-in ID and stored result fields. A changed payload under that ID returns 409. Do not insert another outbox event or alert.
4. For a new ID, validate timestamps and normalize each observation through the shared clinical policy. Reject submitted server metadata such as `danger_sign`, `policy_version`, `received_at`, source IDs, or patient IDs. Preserve unclassified observations.
5. Set server-owned `received_at` and existing `timestamp` from one clock reading. Store `client_confirmed_at` separately. For compatibility, normalized item `confirmed_at` is the server acceptance time; set source to `offline_form` and expose the client confirmation time and provenance in history/summaries so this is not presented as an online verification event.
6. Recompute the aggregate danger flag from normalized, confirmed symptoms. Within one transaction, insert the check-in, any emergency alert, the existing `checkin.completed` outbox event, and retry result. Roll back all writes on any failure.
7. Return `{client_submission_id, check_in_id, status: "synced", recorded_at, received_at, danger_sign_triggered, alert_id}`. Every field comes from persisted data; identical retries return the same values.

Use permanent uniqueness in addition to `app/db/idempotency.py`; an expired cache or a changed request header must not allow a second record. Do not attach offline submissions to a voice session or invoke ASR/LLM providers.

## Alert creation and time semantics

Put final check-in persistence and alert creation behind one shared transactional service/repository path used by voice completion, offline sync, and manual intake. Recompute the aggregate danger flag on this path rather than trusting caller flags. Create exactly one alert per dangerous completed check-in; repeated categories are deduplicated in its category list. Keep the existing immediate patient-facing danger indication during voice verification. Portal alerts in this MVP begin at final check-in persistence.

Acknowledgement is a conditional update scoped to patient, alert, active connection, and active clinician profile. A second clinician cannot overwrite the first acknowledgement. Audit only the actual state transition. Check current authorization before returning any idempotency replay to avoid leaking an old result after revocation.

Do not backfill historical alerts automatically. Existing confirmed records remain visible to clinicians through history; the pilot runbook must state that the alert feed starts with check-ins finalized by this release. No alert implies neither an assessment of safety nor that someone is monitoring continuously.

Keep history pagination and report selection based on existing receipt-time `timestamp`. Add both times to new history responses and summary provenance. Update summary rendering to display observation dates from `recorded_at` while declaring `window.basis = "received_at"` on new snapshots. A delayed observation is included in later snapshots whose receipt window contains its arrival, without modifying previous snapshots.

Update food/supplement daily checks to query observation time, not arrival time: yesterday's meal synced today must not suppress today's food stage. For summary adherence and nutrition calculations, exclude observations whose recorded date falls outside the selected report interval from interval statistics, but retain them in a clearly marked `late_observations` section with source IDs and both timestamps. Do not count the same observation in both interval statistics and that section. Existing snapshots remain unchanged, and readers must support snapshots that lack the new fields.

## Frontend implementation

Use the established frontend framework once its repository is available. Do not create a separate disconnected portal or assume this Python repository contains a working patient UI.

Required screens:

| Screen | Required behavior |
|---|---|
| Patient access settings | Explain permissions, enter recipient account ID, create/copy invitation, list connection status, revoke access. |
| Invitation acceptance | Require login, submit token in a body, show accepted/expired/wrong-account states without clinical data in URLs. |
| Clinician dashboard | Connected patient cards with next appointment and unacknowledged alert count. Refresh on focus and manually; show last successful refresh. |
| Clinician patient detail | Pregnancy overview, confirmed history, latest summary, appointment, alerts, acknowledgement button. |
| Trusted-person dashboard | Patient name, upcoming appointment, permitted alerts and acknowledgement status. |
| Patient offline check-in | Cached structured fields, explicit review/confirmation, and visible queue status. |

The frontend must expose the signed-in user's account ID for pilot invitations and support users without maternal onboarding when opening recipient screens. Represent loading, empty, authentication-expired, disconnected, and revoked states. A failed fetch must not render as an empty alert list. Clear stale patient content when changing accounts or losing access.

Implement the patient queue in IndexedDB, partitioned by authenticated account ID. Cache only static app/form assets and reviewed generic help content; do not cache portal clinical responses or tokens with submissions. Cache clinical category/form definitions with a schema version and refresh them online. Never store recorded audio for this MVP.

Queue state machine:

```text
draft -> pending_sync -> syncing -> synced
                          |
                          +-> pending_sync     network error, 429, or 5xx
                          +-> needs_attention  invalid payload or changed-ID conflict
                          +-> auth_required    login expired
```

Create the submission UUID and freeze the payload at confirmation. Sync items individually so one bad item does not block the queue. Use a per-account sync lock/lease across tabs; server uniqueness remains authoritative. Recover abandoned `syncing` leases after app termination. Retry with bounded exponential backoff and jitter, honor `Retry-After`, and offer manual retry. Browser connectivity events trigger attempts; successful HTTP responses establish delivery.

Persist the server acknowledgement locally before removing the clinical payload. On reload after a lost response, replay the unchanged UUID/payload. Retain a minimal receipt (submission ID, check-in ID, times) after success. Only allow edits after a definitive 422 rejection; re-confirm those edits under a new submission ID. Network-uncertain submissions stay frozen and are retried first. A 409 needs reconciliation, not automatic resubmission under a new ID.

Do not upload account A's queue using account B's credentials. Pause on session expiry and resume only after the same account signs in. Preserve pending items through automatic auth expiry. On explicit logout with pending items, show a choice to stay and sync or discard local pending data and sign out; never silently lose pending work. Clear synced local clinical payloads and portal state at logout. Handle storage quota failures visibly before claiming a check-in is saved; explain that clearing browser storage removes unsynced entries. Do not claim browser-local storage is encrypted unless the application actually implements and tests that protection.

Display recorded time, sync status, and delayed receipt clearly. Pending check-ins have not reached either portal. Keep existing reviewed emergency guidance available offline and state that users must not wait for sync or portal acknowledgement to seek help. Use existing Amharic labels and arrange review of new patient-facing wording; do not invent clinical guidance or emergency contact numbers.

## Implementation milestones

Complete these in order. Each milestone must include meaningful tests and updated contracts for its changes. Keep completed work reviewable in small commits if the coding session requests commits.

| Milestone | Files and work | Completion evidence |
|---|---|---|
| 1 Access foundation | Migration 011; new `app/models/care.py`, `app/services/care_access.py`, `app/db/repositories/care_connections.py`, `app/api/routes/care.py`; extend `app/dependencies.py`; operator provisioning; register routes in `app/main.py`. | Invite, accept, expire, revoke, clinician deactivation, concurrency, and database privilege tests pass. |
| 2 Portal and alerts | New `app/models/portal.py`, `app/models/alerts.py`, `app/services/portal.py`, `app/services/alerts.py`, corresponding routes/repositories; shared final-check-in alert insertion; narrow database projection functions. | Two patients, two clinicians, and a trusted person demonstrate permitted reads, forbidden reads, and one alert/acknowledgement per transition. |
| 3 Offline ingestion | Migration 012; new `app/models/offline_checkin.py`, `app/services/offline_checkin.py`; add route before generic session routes; update check-in repository/history models. | Offline request succeeds without provider calls; concurrent/lost-response retries create exactly one record, alert, and outbox event. |
| 4 Time and compatibility | Update `app/services/summary.py`, daily observation queries, privacy export models/service, schema readiness, generated API contracts, migration/rollback rehearsal. | Delayed observations preserve original dates; old snapshots remain readable; fresh and upgrade database tests pass. |
| 5 Frontend | Implement the six screens, permission-aware navigation, IndexedDB queue, static caching, same-account resume, and translated states in the actual frontend repository. | Browser end-to-end tests cover invitation, portal visibility, offline restart/reconnect, token expiry, and logout behavior. |
| 6 Pilot verification | Seed synthetic demo accounts/data, deployment instructions, feature settings, API examples, evidence from checks, and a walkthrough. | Backend and frontend acceptance checks pass together; any existing real-patient release requirements remain explicit. |

Use proposed filenames as module boundaries, adapting to actual repository conventions. Keep clinical logic in shared services and authorization in both the API path and database functions. Do not introduce a general permissions framework, message broker, or new AI provider.

## Verification matrix

Add unit/API coverage under `tests/` and real PostgreSQL coverage under `tests/integration/`, following the existing fixtures and restricted connection roles.

| Area | Required cases |
|---|---|
| Actor isolation | Unassigned clinician denied; trusted person denied history/summary; guessed patient/alert IDs denied; forged cursor denied; no patient impersonation through request fields. |
| Database enforcement | Direct `enat_app` queries cannot read another patient's base rows; portal functions enforce relationship/projection; anon/authenticated/service-role clients cannot execute privileged functions; provisioning privileges unavailable to API/worker. |
| Invitations | Consent false rejected; token expired/revoked/wrong recipient rejected; self-invite rejected; concurrent creation respects one trusted-person slot; concurrent acceptance produces one transition; raw token absent from logs/audit/retry storage. |
| Revocation | Reads and acknowledgement after committed revocation fail, including cached retry keys; disabled clinician/patient/recipient blocked; revoked token cannot reactivate access. |
| Alerts | Confirmed danger creates one alert; unconfirmed drafts create none; client danger metadata rejected; unknown symptom remains unclassified; concurrent acknowledgement preserves first actor/time. |
| Offline integrity | Missing confirmation rejected; same ID/same content returns original result; same ID/changed content returns 409; same ID from two concurrent tabs produces one insert; retry after simulated commit/response loss succeeds; permanent dedup survives retry-result deletion. |
| Atomicity | Inject failure at alert, audit, and outbox persistence; assert no partial final check-in or false success. Existing voice completion still behaves correctly. |
| Time | Naive/future times rejected; UTC offsets normalized; Addis Ababa midnight boundary correct; old submission accepted; delayed receipt does not become today's meal; snapshots retain original content. |
| Summary compatibility | Late observations outside interval statistics appear separately; no double counting; old snapshots render without new metadata; newer receipt windows can include delayed arrivals. |
| Client queue | Offline capture and restart; interrupted sync and lease recovery; partial queue failures; same-account relogin; account switch; lost acknowledgement; quota exhaustion; no portal response cached. |
| Privacy | New owned connections/alerts/audit fields export through explicit allowlists; exclude invitation tokens/hashes and submission hashes; another patient's audit is inaccessible. |
| Migration | Fresh installation, upgrade with synthetic existing data, coherent backfill, unknown schema detection, candidate/compatible-fallback/candidate rehearsal. |

At completion run the repository checks using its Python 3.12 environment:

```bash
ruff format --check app tests scripts
ruff check app tests scripts
mypy
python scripts/generate_postman_collection.py --check
python scripts/check_contracts.py
python -m pytest
python scripts/test_database.py --fresh
python scripts/test_database.py
python scripts/scan_secrets.py
```

After intentional API edits, regenerate Postman using `scripts/generate_postman_collection.py`, then run `python scripts/check_contracts.py --write` and review the OpenAPI/operation diffs. Include new modules in applicable type-check scope. Run existing container/security/release checks when building the pilot image, as described in `README.md`; document environmental blockers instead of marking unrun checks as passed. Run the frontend repository's lint, build, and browser tests once integrated.

## Rollout and completion criteria

Add `ENABLE_CARE_PORTAL` and `ENABLE_OFFLINE_CHECKINS`, both default false, with settings validation, `.env.example` documentation, and tests. Gate new public functionality with these settings; the shared alert persistence path operates whenever the new backend finalizes a check-in, so temporarily hiding portal access does not lose newly recorded alerts. Patient revocation must remain available for existing connections even if new portal access/invitations are disabled. Disabled offline sync returns a retryable unavailable response so clients retain their queues.

New migrations change the exact schema readiness requirement. Update `SCHEMA_VERSION`/`SCHEMA_COUNT`, tests, and the reviewed compatible rollback image/CI rehearsal. Do not assume the currently pinned schema-009/010 bridge accepts schemas 011/012. Rehearse the additive migration path on synthetic data before deployment; never roll back by deleting patient records or rewriting applied migration checksums.

Extend privacy exports with owned connection metadata, alerts, and access events using explicit allowlists. Update the export manifest/types and retention runbook for these records. Do not add automatic deletion or new retention periods as part of this MVP.

The backend is complete when migrations, authorization, portal APIs, alerts, offline ingestion, contract artifacts, and backend/database checks pass. The product MVP is complete only when the frontend screens and queue pass this demonstration:

1. Patient approves a provisioned clinician and one trusted person; each accepts using their own login.
2. Clinician sees only linked patients, confirmed history, summary, and appointments. Trusted person sees only permitted alerts and upcoming appointments.
3. Patient confirms a structured check-in offline, closes/reopens the app, reconnects, and gets exactly one synced record.
4. A dangerous completed check-in creates one visible alert with original recorded time and server receipt time. Clinician acknowledgement appears without implying resolution.
5. A lost server response and repeated retries produce no duplicates; failed items remain visible and recoverable.
6. Revocation immediately blocks subsequent server access. Patient appointment and online voice workflows still pass regression checks.

## Coding agent handoff

Use this instruction to start implementation:

> Implement `docs/clinician-offline-mvp-plan.md` milestone by milestone. Inspect repository instructions and current code first. Preserve existing patient isolation, confirmation requirements, immutable summaries, and voice APIs. Begin with migrations and access-control tests, then portal/alerts, offline ingestion, and timestamp/report compatibility. Reuse the existing database transactions, idempotency, and clinical policy. Implement the frontend milestone in the actual frontend repository; if it is unavailable, complete independent backend work and report the missing frontend as an explicit remaining dependency. Update generated contracts and run the specified checks. Report completed milestones, test results, and remaining gaps accurately; do not call backend-only work a finished product MVP.
