# Phase 1: identity and health-data controls

Implemented locally on 13 October 2026. This document records the implemented
security model, client migration, and outstanding deployment/reviewer gates.
It is not a production release approval. Phase 2 clinical/persistence defects
remain open, including confirmation rules, report windows, and atomic completion.

## Identity and authentication

The internal `users.id` remains the ownership key. `user_identities` maps a
unique `(provider, subject)` to it. Migration 005 preserves existing email user
UUIDs and Telegram mappings where legacy Telegram columns already exist; login
no longer overwrites `created_at`. Provisioning is serialized by provider/subject.
Linking requires an authenticated current account and proof of the added identity.
An identity already attached to another account returns 409; no automatic merge
or patient-data transfer occurs.

Email signup uses the public Supabase signup endpoint, returns generic 202, and
never auto-confirms or returns a session. Enable **Confirm email** in Supabase;
an unexpectedly issued signup session makes the backend fail closed with 503.
Login and every authenticated Supabase request require a confirmed email.
Disabled local users are denied by identity resolution, sessions, shares, and RLS.
Supabase account bans are checked through the online user response.

One token policy is used: validate algorithm, issuer, audience, finite expiry and
issued-at, UUID subject and session ID, then submit the identical token to
Supabase Auth for signature/account verification. ES256/RS256 are accepted;
HS256 requires an explicit `LEGACY_HS256_UNTIL` UTC deadline within 30 days.
There is no local shared-secret fallback, including on outages. Key rotation is
delegated to Auth; unavailability is 503, invalid credentials 401. The old
`SUPABASE_JWT_SECRET` setting is deprecated and unused.

`POST /auth/refresh` delegates single-use refresh rotation to Supabase. Replace
both client tokens together. Logout locally revokes the session family before
revoking its Supabase refresh session. This prevents the remaining JWT lifetime
from permitting backend access. Logout also deletes the account's push-token
registrations; devices must register again after login. Revoked Supabase session
IDs are retained because the remote refresh-session lifetime is not locally known.

Recovery uses `POST /auth/reset-password` with a `token_hash`, not an access
token. The backend consumes it through Supabase's **recovery** verification
endpoint, updates the password with the returned user bearer session, records
an account cutoff for old Supabase JWTs, and requests global Supabase logout.
Configure the recovery email template to deliver the recovery TokenHash to the
frontend callback (prefer a fragment, removed immediately by the frontend),
then POST it in the body. Do not pre-consume that OTP in the frontend. If the
update fails after OTP consumption, request a new recovery email. Validate this
exact flow, email confirmation, disabled-account behavior, and signing-key
rotation against the staging Supabase project before release. Local tests use
provider doubles; they do not prove live Auth configuration or SMTP delivery.

Telegram uses one HMAC validator with duplicate/malformed-parameter rejection,
a five-minute freshness bound, 30-second future skew, and empty-token rejection.
`POST /auth/telegram` exchanges launch data exactly once. Only token hashes and
a canonical launch digest are persisted. The opaque application token expires
15 minutes after the original `auth_date`; replay cannot extend it. Reopen the
Mini App for fresh signed launch data when a session expires. The previous
`Authorization: tma ...` path is retired. Account linking requires fresh launch
data too; linking an already provisioned separate account needs an explicit
future merge workflow.

## Database and storage authorization

Patient repositories now use PostgreSQL through a bounded connection pool.
They no longer use Supabase service-role requests. `DATABASE_URL` must authenticate
as `enat_app`: not a superuser, not BYPASSRLS, and not a table owner. Each
transaction sets `app.user_id` locally from the server's verified identity;
request parameters never choose this context. It is reset with the transaction
and tested across pooled connections and simultaneous HTTP requests.

Migration 005 adds missing Telegram and push-token schema, identity/session/share
records, RLS policies, and client-grant revocation. A user cannot read or mutate
another user's rows even if a repository ownership filter is omitted. The worker
role has only reminder access and explicit cleanup permissions in this phase;
production scheduling stays disabled until Phase 3 supplies its complete worker
contract. Security-definer identity/share/rate functions have a fixed search path,
backend-only EXECUTE grants, and no client RPC access.

Supabase Auth uses `SUPABASE_PUBLISHABLE_KEY`. The service-role key is retained
only for the Storage adapter. Supabase `anon`, `authenticated`, and `service_role`
lose direct patient-table and privileged-function grants. Generic prompt metadata
is backend-readable; mutations require administrative provisioning. Migration 005
makes the old QR bucket private and installs restrictive Storage policies denying
client access to patient QR objects and client modification of generic audio.
The local suite tests this against a Storage table/policy stand-in; real Supabase
Storage APIs, deployed policies, object caches/CDNs, role memberships, and grants
must still be audited in staging.

Apply migrations 001–006 with a separate migration-owner credential. Provision
`enat_app` LOGIN/password through secret management, grant no other roles to it,
and set the backend DSN with verified TLS (`sslmode=verify-full` and the correct
CA/hostname). Do not make `enat_app` the migration owner. Rehearse against a copy
of the actual legacy schema: duplicate Telegram IDs, duplicate identity mappings,
or unexpectedly pre-existing new tables should fail for review rather than
silently merge owners. The upgrade suite includes legacy email identities and
public summary credentials; it cannot model unknown live schema drift.

The new app requires migration 005 before accepting patient traffic. Its grant
changes intentionally prevent rolling back to the old service-role data path.
Deploy in a coordinated maintenance window after backup and staging rehearsal;
rollback to a build that retains the new authorization boundary. Do not undo
revocations or re-enable legacy public links as a routine rollback.

## Patient-controlled shares and speech

Sharing defaults **disabled** (`ENABLE_SUMMARY_SHARING=false`) pending privacy
review. The implemented candidate model is an explicitly consented bearer share,
24 hours by default and at most seven days, with immediate revocation. Tokens
have 256 bits of randomness; only hashes are stored. Scope `structured-v1`
includes approved-category symptom dates/severity and integer adherence counts.
Raw text, closing notes, user metadata, arbitrary nested fields, and old QR URLs
are never forwarded. It remains sensitive, potentially identifying health data;
it is not anonymization and does not require clinician authentication. Review
whether this scope and bearer-access model meet the product's intended use.

Generate an owner-only snapshot, then explicitly POST to
`/summary/{summary_id}/shares` with `consent: true`. The private response supplies
the URL, share ID/expiry, and QR PNG as base64. Nothing is uploaded to a public
bucket. A token/QR is returned only at creation; generate a new consented share
if lost. DELETE `/summary/shares/{share_id}` revokes it. Migration 005 invalidates
all old slug credentials and removes old QR URLs from snapshots. Existing files
are made private; deletion and downstream CDN/cache purge remain deployment work.

API responses carry `Cache-Control: no-store`, `Referrer-Policy: no-referrer`,
and `X-Robots-Tag: noindex, nofollow`. The frontend share page needs equivalent
headers, no analytics, and careful handling of browser history and third-party
requests. Backend Uvicorn access logging redacts request targets; configure the
edge/CDN to redact paths/queries and never capture bodies or authorization headers.

Patient-specific speech is authenticated `POST /tts` only, capped at 2,000
characters, with no shared patient-audio cache. `GET /tts` returns 410 and new
verification responses contain `verification_audio_url: null`. Clients POST the
verification phrase and play the returned blob. Automatic gTTS fallback and its
dependency are removed; only the configured Addis endpoint receives speech data.
Approve that processor, its contract, permitted purposes, retention, location,
and operational access before patient use. No processor approval is inferred from
this implementation. Public generic audio must be provisioned in advance; a
cache miss cannot trigger a synthesis call. The generic byte cache holds at most
four 4 MB objects, each for at most one hour.

## Resource controls and operations

A middleware counts actual body chunks, including requests without a trustworthy
Content-Length. JSON bodies are capped at 64 KB; multipart bodies default to
8 MB. Audio files are read in chunks with a 6 MB cap and checked before provider
calls. Restricted-format ffprobe/ffmpeg inspect and decode at most 121 seconds
into bounded mono PCM; the default maximum is 120 seconds. This supports browser
WebM without trusting duration metadata. Supported types are WAV, WebM, Ogg,
MP4 audio, and MP3. Deploy both **ffmpeg and ffprobe**. Errors are 413 (size/time),
415 (format/decode), or 503 (validator unavailable). Existing Amharic recording
compatibility still needs client/device validation.

PostgreSQL-backed counters are shared across API replicas: 10 auth attempts per
peer/minute, 60 other non-health requests per peer/minute, and 120 requests per
verified user/minute. All provider attempts, including extraction retries, count
against per-user and global rolling 24-hour call budgets (defaults 100 and 10,000).
Provider work also needs a global lease (default 20 concurrent calls), expires
abandoned leases after 90 seconds, and has a 65-second operation deadline.
429 includes Retry-After. Database/limiter failure denies work; limits cannot be
disabled in staging/production. Adjust these pilot defaults with observed quotas,
latency, abuse patterns, and user counts. Request/audio/token bounds constrain
usage, but **currency-denominated spending limits and vendor billing alerts are
not validated**; provider pricing and account quotas remain release inputs.

Run through `bash scripts/run_api.sh`; configure `TRUSTED_HOSTS` and explicit
`TRUSTED_PROXY_IPS`, never a wildcard. The command bounds server concurrency and
keepalive. Configure edge upload timeouts and body/concurrency limits as well.
Request validation and provider exceptions do not echo input; unexpected error
logs contain a generated request ID. API schema/startup validation hides setting
values in exceptions. Detailed observability and outage runbooks remain Phase 5.

Schedule `SELECT enat_cleanup_security_state()` using the worker credential in
the Phase 3 scheduler. It removes expired launch/session and rate-limit data;
summary retention and clinical-data deletion are separate decisions. Before
release, assign owners and approved policies for consent records, patient
export/deletion, retention of records/backups/logs/shares, processor deletion,
incident response, and access reviews. These are open reviewer/operational gates,
not policies silently decided by the implementation.

## Verification and remaining gates

Final local results on Python 3.12.3 / PostgreSQL 16:

- Unit/default suite: **133 passed**, with the 20 database tests intentionally
  skipped unless the disposable-cluster harness is used.
- Fresh database: **19 passed**, one upgrade-only fixture skipped.
- Legacy-row upgrade: **20 passed**, including the actual HTTP identity/logout
  path, RLS/role checks, Storage-policy stand-in, and repository JSON/time round trips.
- Ruff undefined-name gate, dependency consistency, and `git diff --check`: passed.
- Working-tree and available-history secret-pattern scan: **zero findings**.
- Existing UTC and dependency deprecation warnings remain visible.


The repository includes network-blocked unit tests and a disposable PostgreSQL 16
suite (`python scripts/test_database.py`, plus `--fresh`). It covers exact roles,
missing application filters, ownership on writes, disabled accounts, stable
identities, replay concurrency, linking conflicts, pool context isolation,
concurrent HTTP requests, logout/password cutoff, device-token ownership,
share expiry/revocation, legacy credential invalidation, storage restrictions,
and atomic distributed limits. The harness never connects to deployed services.

`python scripts/scan_secrets.py` checks the working tree and available Git history
for high-signal credential/private-key patterns and reports locations only. Zero
matches does not prove no secrets exist. It does not inspect untracked deployment
artifacts outside this checkout, hosting secrets, or remote logs. Any subsequently
confirmed exposed credential must be rotated through secret management.

Release gates still open: actual Supabase Auth/Storage verification and grant
audit, client rollout and recording compatibility, privacy/security sign-off on
sharing and processors, retention/export/deletion/incident ownership, vendor cost
limits, deployed proxy/CDN redaction, and the Phase 2–5 acceptance criteria. No
live migration, hosted CI run, secret rotation, external publication, or production
deployment was performed.

References used for implementation: [Supabase signup](https://supabase.com/docs/reference/python/auth-signup),
[JWT verification](https://supabase.com/docs/guides/auth/jwts),
[session lifecycle](https://supabase.com/docs/guides/auth/sessions), and
[Telegram launch validation](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app).
