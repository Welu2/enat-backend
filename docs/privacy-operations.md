# Privacy requests, personal-data export and audit

Migration 010 adds owned privacy requests, immutable audit events, restricted
operator access and queue telemetry. It does not choose a medical retention
period or erase clinical records. Export and request endpoints default off until
an operating policy and support channel have been configured.

## Enable and operate

Apply migrations through `010_privacy_workflows.sql`, assign a primary and backup
privacy queue owner, test alert delivery, and configure:

```dotenv
ENABLE_PRIVACY_TOOLS=true
PRIVACY_POLICY_VERSION=YOUR_APPROVED_POLICY_VERSION
PRIVACY_SUPPORT_URL=https://YOUR_SUPPORT_HOST/privacy
```

A nonempty policy version and an HTTPS support URL are required. These settings
identify the operating policy; they do not themselves prove clinical/legal
approval. Keep tools disabled until the assigned team can handle requests.

Provision a separate controlled operator login that inherits `enat_privacy_operator`.
Do not grant that role to the API, worker, Supabase clients or end users. This role
can read the request/audit queue but cannot read patient clinical tables, forge
requests, rewrite events or delete records. The migration creates it as NOLOGIN;
login credentials and access review belong to infrastructure provisioning.

The worker and scheduler publish aggregate `enat_privacy_requests_pending` and
`enat_privacy_oldest_request_seconds`, with no user labels. The
`EnatPrivacyRequestPending` warning fires when a request remains queued for one
minute. This is an operational notification, not a statutory response deadline.
Route it to the assigned privacy owner. Actual alert delivery must be tested.

## Patient API

All paths require the patient's normal authentication and return `Cache-Control:
no-store`. The server uses the authenticated identity, not a submitted user ID.

| Method and path | Behavior |
|---|---|
| `GET /users/me/privacy/export` | Returns versioned section inventory, policy/support information and exclusions. |
| `GET /users/me/privacy/export/{section}?limit=50&after=<UUID>` | Returns up to 100 owned records and `next_cursor`; continue with that UUID as `after` until null. |
| `POST /users/me/privacy/requests` | Body `{"confirm":true}` plus `Idempotency-Key`; returns 202 with a pending deletion-review request. |
| `POST /users/me/privacy/requests/{id}/cancel` | Cancels an owned request; repeated cancellation is safe. Unknown/other-user IDs return 404. |

Only one pending request exists per patient, even with concurrent different retry
keys. A replay of the same key returns its original response; fetch the `requests`
export section for current status after cancellation. A submitted request does
not disable the account or delete data. The support team must verify scope and
identity, determine any preservation requirements under the approved policy, and
use its reviewed resolution process. Automated erasure and operator resolution
transitions remain pending that policy; do not label this endpoint a completed
erasure service. A patient can cancel and submit a new request.

Export sections include profile, supplements, appointments/attendance events,
confirmed check-ins, drafts, summaries, reminders, share metadata, privacy
requests and audit events. Fields are explicitly allowlisted. Bearer credentials,
push delivery tokens, internal retry/job payloads, object bytes, backups and
external processor records are excluded and listed in the manifest. Such records
need the separately approved disclosure process; this API does not claim a
complete legal-access response across all processors.

Pages are individually transactionally consistent, not a database snapshot across
multiple requests. Concurrent edits/inserts can change what appears across pages.
For a fixed full snapshot, the privacy team must use its approved controlled
export process. UUID keyset pagination reads beyond 1,000 records without an
offset or total-result cap; use all returned pages. Clients must retain the
section and cursor together and must not log exported clinical contents.

## Audit guarantees and limits

Each exported data page records section, row count, patient identity and time in
the same transaction. An audit failure fails the read instead of delivering an
unaudited page. Reading the audit section does not append another export event,
so that export terminates. Request creation/cancellation and share creation,
revocation and successful public reads append database-triggered/function events.
Retries and repeated revocation do not fabricate duplicate state transitions.
Public reads record `share_recipient`, not a claimed clinician identity.

Events contain no raw health text, bearer/share tokens, hashes of those tokens,
IP addresses or request bodies. Patient RLS limits reads to the owner. App,
worker and client roles cannot update/delete the audit; a database trigger also
rejects rewriting by normal owner DML. This is not proof against a database
administrator deliberately disabling controls. Historical access before migration
010 is not backfilled or invented. This audit covers these privacy/share actions,
not every clinical read in the product.

Audit/request references intentionally prevent an unreviewed cascade from user
deletion. The approved retention/erasure implementation must explicitly address
these records, immutable clinical snapshots, processors, object references,
backups and suppression after restore. Do not bypass triggers or foreign keys to
make a pending request appear completed.

## Migration and rollback

The previous schema-009 image rejected newer ledgers in readiness. Commit
`d147cbd` is a bridge that requires completed schema 009 and tolerates only the reviewed additive 010
entry, including a running or transactionally rolled-back attempt. It leaves
application behavior unchanged. Deploy and verify a reviewed bridge image before
applying 010 to an existing environment, retaining that exact image as fallback.
The new privacy candidate requires completed schema 010. Application rollback
keeps the additive schema and can return to the bridge image. Do not use the
older unmodified schema-009 image as fallback. New installations still need a
reviewed compatible fallback image before pilot bootstrap.

Indexes use the existing migration lock/statement timeouts; rehearse them at
actual volume. Migration 010 performs no patient-data backfill or deletion.

CI pins the bridge source revision and rehearses bridge readiness with running
and failed migration ledger entries, then candidate → bridge → candidate with
completed schema 010 and preserved synthetic patient data. Update that reviewed
fallback explicitly when introducing future schema changes.
