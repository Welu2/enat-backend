# Care portal and offline check-in backend

The backend supports patient-approved clinician and trusted-person access, emergency alerts from finalized confirmed check-ins, and idempotent offline structured submissions. The product frontend is a separate dependency: this repository does not contain the six portal/patient screens or the IndexedDB queue described in the [implementation plan](clinician-offline-mvp-plan.md). Backend verification does not establish a finished product MVP or approval for real patient use.

## Enable the backend

Apply migrations through `012_offline_checkins.sql` with the migration owner. Existing environments must first deploy the compatible fallback described below. Configure the candidate API with:

```dotenv
ENABLE_CARE_PORTAL=true
ENABLE_OFFLINE_CHECKINS=true
```

Both flags default to false. Disabled functionality returns 503; retain pending offline work and retry later. Connection listing and patient revocation remain available even when new portal access is disabled. Alert insertion continues for check-ins finalized by the candidate while the portal flag is off. Historical check-ins are not converted into new alerts.

The app uses its existing restricted `enat_app` credential. Do not supply care operator, migration owner, or Supabase service-role credentials to portal queries. Existing patient row-level security is unchanged. Cross-patient projections and acknowledgements use static, permission-checking database functions; actor identity is never replaced with the URL's patient ID.

## Provision a clinician

The clinician signs in through the existing authentication flow. Use their own `/portal/me` account ID; no patient onboarding is required. A database administrator provisions a separate restricted login with membership in the migration-created `enat_care_operator` role. Keep that login's credentials outside API/worker environment files. The operator role can manage clinician profiles and cannot read patient clinical tables.

Set `CARE_OPERATOR_DATABASE_URL` securely in the operator's environment, then run:

```bash
python scripts/manage_clinician.py ACCOUNT_UUID --enable --display-name "Clinician name"
python scripts/manage_clinician.py ACCOUNT_UUID --disable
```

Disabling a clinician profile prevents subsequent portal reads and acknowledgements even with an existing login token. Re-enabling restores eligibility for still-active patient connections; revoke the connections if that access should end permanently.

## Patient approval and recipient access

1. The intended recipient supplies their authenticated account ID to the patient.
2. The patient calls `POST /users/me/care-connections` with `recipient_id`, `relationship` (`clinician` or `trusted_person`), and strict `consent: true`.
3. The response includes an invitation token once. Share it manually with the intended recipient. The database stores only its hash; token values never belong in URLs, logs, or analytics.
4. The recipient signs in and calls `POST /care-connections/accept` with `{ "token": "..." }`.
5. The patient can list connections or revoke one with `DELETE /users/me/care-connections/{connection_id}`.

Invitations expire after 48 hours and bind to the specified account. Active access lasts until revoked or an account/profile is disabled. One pending/active trusted-person connection is allowed per patient. A lost invitation-creation response requires listing, revoking the pending invitation, and creating another; raw tokens are not retained in a replay cache. Repeating acceptance never reactivates revoked access.

Clinicians receive existing confirmed history and summaries after explicit patient consent. Trusted people receive only patient name, the upcoming scheduled appointment, and alerts created since their current connection was accepted. Acknowledgement belongs to clinicians and means seen, not treated or resolved. Both relationships may exist for an account; the active clinician relationship provides the broader authorized projection. A disabled clinician profile does not erase a separately approved trusted-person connection.

Read calls and actual lifecycle transitions create immutable access events. Audit failures fail the operation. Portal responses use `Cache-Control: no-store`. Revocation blocks requests begun after it commits; previously displayed data cannot be recalled and must be cleared by the client when access fails.

## Portal contracts

The generated [OpenAPI](openapi.json), [operation inventory](api-operations.md), and the Postman folder **Care portal and offline check-ins** contain all request/response schemas and examples.

Lists default to 50 and cap at 100. Continue using `X-Next-Cursor` as the `cursor` query parameter. Patient and connection lists sort by ascending UUID; alerts sort by descending `(created_at, id)` and history by descending `(timestamp, id)`. Reauthorize every page. Alert filtering accepts `status=unacknowledged` or `status=acknowledged`.

Appointment reads return the current scheduled appointment on/after today in `Africa/Addis_Ababa`, or JSON `null`. They expose no fabricated time of day. Portal users cannot reschedule appointments.

Stored pregnancy fields lack an authoritative observation date in the existing schema. The overview therefore returns `pregnancy_as_of: null` with a separate server `overview_retrieved_at`; clients must not label retrieved gestational age as a newly measured value. Missing latest summaries return 404. Summary responses exclude public bearer links and QR URLs. Older immutable snapshots can lack the new timestamp and late-observation fields.

`POST /portal/patients/{patient_id}/alerts/{alert_id}/acknowledge` requires `Idempotency-Key`. Current access is checked before replay. The first acknowledgement's actor/time is preserved; reusing a key for a different alert returns 409 and rolls back any tentative change.

## Offline sync contract

The patient sends one frozen, explicitly confirmed structured submission to `POST /checkin/offline-sync`, using their normal login and an `Idempotency-Key` equal to the body `client_submission_id` UUID. No voice-session ID or session version is needed. There are no provider calls on this path.

The body requires `schema_version: 1`, `recorded_at`, `client_confirmed_at`, strict `confirmed: true`, and all four arrays: `symptoms`, `food_log`, `supplement_check`, `closing_mentions`. Use the existing editable clinical field schemas. Each array is limited to 50 entries, the total to 100, and the body to 64 KiB. At least one observation is required; an empty form never means healthy. Unknown symptom categories remain unclassified rather than being treated as a negative clinical assessment.

All times must include timezone offsets. Require `recorded_at <= client_confirmed_at`; confirmation can be at most five minutes ahead of the server. Old submissions are accepted and marked with their original recording time. Client times are self-reported. The server supplies receipt time, item/source IDs, normalization policy, and danger classification; attempts to submit those server-owned fields are rejected.

First acceptance and identical retries return 200 with the same submission/check-in IDs, `status: synced`, recorded/received times, danger flag, and alert ID when applicable. A changed payload under the same submission ID returns 409. Permanent uniqueness and a canonical payload hash protect against duplicate insertion after temporary retry results have been cleared. UTC-equivalent timestamp representations are the same input.

Final check-in, alert, outbox event, and retry result are atomic. A failed write never creates a partial success. Existing voice and manual intake use the same final alert-creation path. Portal alerts begin when the check-in is finalized; the existing immediate danger indication during voice verification remains available to the patient.

## Time and reporting

`recorded_at` is the reported observation time. `received_at` and the backward-compatible `timestamp` are the server receipt time. For offline items, the legacy `confirmed_at` is acceptance time; `client_confirmed_at` and the `offline_patient_report_accepted_at_server` provenance distinguish the reported confirmation event.

History and summary selection use receipt time. New summaries declare `window.basis: received_at` and display observation dates from `recorded_at`. Arrivals with observation times outside the interval appear under `late_observations`, excluded from that interval's nutrition/adherence statistics. Their confirmed content and source IDs remain visible. Older snapshots are never rewritten. Daily food/supplement completeness uses observation time so an old upload cannot suppress today's stage.

## Required frontend integration

Implement the six screens and local queue in the actual patient frontend repository. Do not interpret these backend endpoints as an implemented website. Required client behavior includes:

- Patient sharing settings, invitation acceptance, clinician dashboard/detail, trusted-person dashboard, and offline structured check-in.
- A versioned static form cache and an account-specific IndexedDB queue that survives restart. No offline voice processing or portal-response caching.
- Frozen confirmed payloads with stable UUIDs, cross-tab sync leases, bounded retry/backoff, manual retry, and recovery after a lost response.
- Pause on expired login; resume only as the same account. A 422 needs correction and reconfirmation under a new ID; a 409 needs reconciliation. Never change the UUID after an uncertain network result.
- Retain pending submissions on service unavailability, including 404 from an older rollback image whose offline endpoint is absent. Never report such submissions as delivered.
- A visible choice to remain and sync or discard pending local work on explicit logout. Storage/quota failures must not be reported as saved data.
- Clear distinction between pending sync and delivery. Offline check-ins have reached neither portal. Preserve existing reviewed emergency guidance without waiting for sync or acknowledgement.
- Loading, empty, stale, disconnected, revoked, and authentication-expired states; last successful portal refresh; support for `late_observations` and older summary shapes.

## Privacy and retention

The existing privacy-tool flag/policy still controls exports. The manifest now includes patient-owned `care_connections`, `emergency_alerts`, and `care_audit`, plus offline timestamps in check-in exports. Fields are explicitly allowlisted. Invitation tokens/hashes and submission hashes remain excluded. Audit exports do not recursively add access events.

No new retention period or automatic deletion is introduced. Reviewed deletion/restore procedures must account for care connections, clinician/recipient references, alerts, permanent submission identities, and immutable care audit events. Foreign keys and audit immutability intentionally prevent unreviewed erasure. A patient's deletion-review request retains its existing non-destructive behavior.

## Migration and fallback

The candidate requires all 12 applied migrations. Migration 012 backfills time metadata while retaining legacy unverified observations. Its confirmation trigger still protects every insert and every clinical-content update; metadata backfill does not invent confirmation. New SQL inserts from the fallback image receive compatible timestamp defaults through a trigger.

CI builds a new compatibility bridge from pinned pre-feature source `027e62011a78642fab3de4140b22ced8fd3a564b`, replacing `app/core/readiness.py` with [the reviewed readiness overlay](../deploy/care_bridge_readiness.py) and using the candidate runtime lockfile for the audited certifi/Pillow fixes. The bridge requires applied migrations 001–010 and tolerates only ordered attempts of 011/012, including a running/failed final attempt. Unknown migrations and an incomplete earlier migration fail readiness. The previously documented schema-009 bridge is not a fallback for this candidate.

Build and verify this bridge before applying 011/012 to an existing environment. Roll back by changing the application image while retaining the additive schema. The bridge serves existing patient flows; new portal/offline routes are absent. During fallback, no new portal access is served and offline clients retain queued work. Alert-feed coverage excludes check-ins finalized by that older image. Return to the candidate to restore new functionality; do not delete schema/data to roll back.

The container rehearsal uses two distinct image tags in `ENAT_REHEARSAL_IMAGES=previous,current`, injects a failed/running 012 ledger entry in a disposable database, and checks candidate → bridge → candidate readiness and persisted owned history. The overlay's ordered 011/012 cases also have unit coverage. Preserve immutable image digests as release evidence before a live rollout.

## Verification and demonstration

Run the normal repository formatting, lint, type, contract, unit, database, secret, and release checks from `README.md`. Additional demo command:

```bash
python scripts/test_database.py --fresh --demo
```

This creates only synthetic accounts in the runner's disposable PostgreSQL cluster, provisions a clinician, accepts patient invitations, submits/retries a dangerous offline check-in, acknowledges its alert, and verifies trusted-person revocation. It writes `artifacts/operations/care-offline-demo.json`; no usable tokens are printed and the cluster is removed afterward. The demo intentionally reports `frontend_verified: false`.

The feature tests cover database privileges, trusted-person projections, account/profile deactivation, connection expiry/slots, pagination authorization, acknowledgement races, permanent deduplication, clock validation, receipt/observation separation, transaction failure, privacy export exclusion, and HTTP authentication/body limits. Complete the browser scenarios from the implementation plan after the frontend repository is connected.


## Local verification on 22 October 2026

- Unit/API suite: 276 passed; database tests run separately.
- Fresh database: 87 passed, 2 legacy-only cases skipped; synthetic care/offline demo passed.
- Legacy upgrade and final container rehearsal: 89 database tests passed.
- Formatting, lint, type checking (22 modules), dependency consistency, 71 Postman examples, OpenAPI, and secret scanning passed.
- Runtime/development dependency and source security gates passed after updating only certifi to 2026.10.19 and Pillow to 13.0.0.
- Candidate container smoke test and image scan passed, with zero high/critical image findings. Candidate → bridge → candidate preserved schema readiness and the owned patient row. One concurrent scan/rehearsal run timed out on readiness; the isolated rerun passed.

Reports are generated under `artifacts/security/` and `artifacts/operations/`. The final scan and rollback evidence reference the same locally built candidate image. No live deployment or browser verification was performed. The remaining product milestone is frontend implementation in the patient application repository.
