# Operations and release runbook

These commands are prepared for the separately provisioned staging and production
environments. No hosting project, deployment credentials, approved previous release,
clinical/privacy owners, or on-call responders have been supplied in this session.
Do not interpret local rehearsals as a production authorization.

## Deploy and migrate

Use separate Supabase projects, object buckets, database logins, rate-limit secrets,
metrics secrets and provider accounts for development, staging and production.
Store environment files in a secret manager or private files outside the repository.
API configuration receives only enat_app and required Auth/Storage/provider credentials;
workers receive enat_worker, METRICS_TOKEN and the private OTLP_ENDPOINT. Never give
API/worker processes the migration owner login. Require verified TLS for remote DB
connections and the actual HTTPS frontend/CORS/host allowlist.

Build, smoke-test and scan the image, then promote that exact digest:
`docker build --pull -t enat:release .`,
`python scripts/smoke_container.py enat:release`,
`python scripts/scan_container.py --image enat:release`.
Archive the image digest, both lock hashes, source revision/working-tree patch and
security/operations artifacts. Base and Python wheels are pinned; APK security
updates are refreshed during build. A rebuild is a new candidate, not the same release.

Set DEPLOYMENT_ENV, ENAT_IMAGE (repository@sha256 digest), API_ENV_FILE,
WORKER_ENV_FILE and MIGRATION_ENV_FILE for deploy/compose.yaml. The templates
provide two independently restartable APIs, a scheduler and worker, each with
CPU/memory/PID limits, a read-only root, bounded tmpfs and no Linux capabilities.
They are one-host templates, not multi-host availability proof. API ports bind
only to loopback. API_A_PORT and API_B_PORT optionally override the default local
ports 8001/8002. Connect an approved TLS ingress/load balancer that checks /ready;
probe /health for liveness. Configure explicit proxy IPs and include loopback in
TRUSTED_HOSTS for probes. Do not expose worker port 9000 or /metrics publicly.

Run the migration service once before replacing API containers:
`docker compose -f deploy/compose.yaml --profile tools run --rm migrate`.
The owner DSN belongs only in its private environment file. Alternatively run
`python -m app.migrate` with MIGRATION_DATABASE_URL supplied securely.
The session advisory lock serializes deployers. Each migration and its applied
ledger row commit together. Failures record a safe SQLSTATE; interrupted running
attempts are retried transactionally. Edited checksums and unknown future
migrations are rejected. Readiness requires all nine known migrations applied.

Existing manually migrated databases must first be cloned and compared with the
synthetic legacy rehearsal. Do not invent ledger records or automatically mark
unknown changes applied: an owner must review and record a one-time baseline,
including exact migration hashes and schema/grant comparison. Local rehearsals
cover fresh and synthetic legacy data, not arbitrary deployed drift.

Migration 009 is additive. Its index builds use a five-second lock timeout and
120-second statement timeout. Measure table sizes in staging; if these bounds
cannot be met, stop and prepare a reviewed concurrent-index expansion before
rollout. Never raise lock timeouts blindly on a busy patient database.

## Rollback and instance failure

Record a clean previously reviewed image digest and its supported schema before
each deployment. Drain one API, replace it, await /ready, then replace the second.
If readiness or error/latency gates fail, drain the new instance and restore the
previous compatible image. Retain additive schema changes; do not run destructive
down migrations. Repeat history/ownership checks and confirm durable jobs/outbox
counts. Do not roll back to the rejected Debian candidate with known vulnerabilities.

A killed worker's lease becomes eligible after 60 seconds. Allow the replacement
to claim it; handler effects are idempotent and lease updates fenced. Do not edit
lease tokens or manufacture successful status. A failed job is replayed explicitly:
`python -m app.jobs status`, then after diagnosis
`python -m app.jobs replay --job-id <failed-job-uuid>` in the restricted worker
environment. Recheck domain effects and retry counts. The scheduler resumes its
committed cursor; old occurrences advance without sending stale dose prompts.

## Readiness, monitoring and provider outage

/health is liveness. /ready checks restricted database access and the migration
ledger with bounded pool acquisition and statement timeouts. Speech-provider
degradation never removes history-only APIs from rotation. /metrics requires
METRICS_TOKEN as a bearer credential; workers serve the same protected exporter
on their private port 9000. No user IDs, share tokens, request bodies, raw URLs
or health text are metric labels. Request and job IDs belong in redacted logs.

Integrate deploy/prometheus.yml, alerts.yml and grafana-dashboard.json into the
private monitoring stack. Configure a receiver and assign/test primary and backup
routing; alert files alone do not deliver pages. Set OTLP_ENDPOINT to the private
collector's /v1/traces endpoint. Manual spans carry route templates and statuses;
W3C traceparent follows provider calls and outbox jobs. Baggage, exception text,
credentials and patient payloads are excluded; sampling is 10%, not caller-forced.

For provider errors, inspect per-operation latency/error/attempt metrics and
provider status without opening patient payloads. Preserve drafts, use manual
input, and respect circuit/backoff limits. Do not enable another processor without
approval. The 24-hour attempt counter is an upper-bound call estimate, not money:
reconcile actual vendor invoices and set approved currency budgets separately.

For slow SQL, inspect pool availability/waiting and the measured history query
plan; identify blocking transactions with restricted DBA tooling. Do not log bind
values. Reduce admission or worker concurrency before enlarging pools. The
template's maximum configured pool demand is 28 connections (10+10+4+4), plus
migration/monitoring overhead; reserve capacity below the actual database limit.
The first local rehearsal failed p99 with one CPU per API during replica loss.
APIs now receive two CPUs each; worker and scheduler retain one CPU each. All four
retain 512 MiB. The full repeat passed 90,000 requests with p95 25 ms/p99 48 ms and
13 transport errors during forced failure; independent readiness probes were
also introduced in that repeat. Repeat the measured envelope on the intended staging host before
approving its capacity, including the resources needed by monitoring and the DB.

### Isolated deployment rehearsal

On a Linux Docker host, build/scan the candidate and set ENAT_LOAD_IMAGE to that
local image. Run `ENAT_LOAD_COMPOSE=1 python scripts/test_database.py --fresh --load`.
The runner creates a disposable PostgreSQL cluster, applies/tests all migrations,
then starts the actual Compose API pair, scheduler and worker with staging
configuration validation and separate synthetic role configuration. It verifies
the running containers' CPU, 512-MiB, 128-PID, read-only and non-root settings.
The migration container rechecks the ledger before services start.

The no-egress network isolates fake Auth/provider endpoints. Prometheus uses the
real bearer-authenticated scrape targets and alert rules, with a two-second
scrape/evaluation interval for the rehearsal. Alert `for` durations are unchanged.
A local Alertmanager-compatible sink records alert names; it has no external
notification route and is not a substitute for testing the real on-call receiver.
The 30-minute workload holds one API down for 150 seconds, then requires all four
scrape targets to recover and the outage alert to have reached the sink. It also
checks that a committed outbox event produced exactly one durable notification.
Temporary services, network and database are removed automatically. Only synthetic
metrics, redacted service logs and measurement reports remain in artifacts.

Use ENAT_LOAD_SECONDS=20 for a short wiring check (three-second outage and no
alert-duration assertion). CI runs this check on the built image; its manual
capacity job runs the full workload. External staging, ingress, real Auth/Storage,
human alert delivery and managed recovery still require environment-specific drills.

## Backup and restore

Enable encrypted managed database backups and PITR with an approved recovery
window and verified restore credentials. A logical dump is not 15-minute PITR.
Version and back up object bytes independently: database backups include storage
metadata, not object contents. The operator must produce a stable object snapshot
directory using bucket/key paths and a protected 32-random-byte key file (0600).
Keys live separately in the secret manager, never beside uploaded backups.

`python scripts/backup_restore.py backup --archive <new-encrypted-archive> --objects <immutable-object-snapshot> --key-file <private-key-file> --work-dir <private-encrypted-scratch>`
uses BACKUP_DATABASE_URL. It exports one PostgreSQL snapshot, checks every
database-referenced artifact, records hashes and encrypts the bundle using
AES-256-GCM. The scratch volume must be encrypted: temporary dump/tar files are
plaintext inside private temporary directories. Upload the encrypted output to
a separately protected versioned destination; record its checksum and timestamp.

To rehearse, provision an empty isolated database with the required restricted
roles (enat_app/enat_worker) and dump owner, plus an empty object directory.
Set RESTORE_DATABASE_URL, then run the same command with `restore`.
Authentication and hashes are checked before database mutation; pg_restore uses
one transaction. Existing databases/object destinations are refused. Verify
migration status, RLS/grants, session/share revocation, history/snapshots, and all
object references before traffic. Record elapsed time and newest recovered event
to establish RTO/RPO. A local synthetic 0.3–0.5-second restore is not a production
recovery guarantee. Copy verified objects to a new isolated bucket and validate
its access policies before any cutover.

## Credentials, retention and compromised links

Rotate one environment at a time: create a new restricted DB login/credential,
update its secret, restart one process, check readiness and ownership, roll the
remainder, then revoke the old credential. Rotate API/provider/Storage/metrics
secrets independently. For Supabase signing keys, verify online key rotation and
recovery in staging. Never restore auto-confirmation or a JWT verification bypass.

For a compromised share, use the owned revoke endpoint immediately. For account
compromise, revoke application sessions and Supabase sessions through approved
incident procedures; confirm old credentials fail. Patient text must not appear
in incident tickets or chat. Capture only opaque request/job IDs and protected
audit references. Sharing stays disabled until the privacy review is approved.

The scheduler runs bounded security cleanup every minute: expired rate buckets,
provider leases, old app sessions/revocations and shares expired for over 30 days.
Expired drafts are marked expired; content, immutable summaries, completion and
idempotency evidence are retained. Clinical retention/deletion/export needs an
approved jurisdiction-specific policy and audited implementation; this session
cannot choose a medical retention period. Storage deletion must follow references
and backup retention, never an unreviewed bucket wipe.

For data correction, use confirmed, versioned application flows. Preserve an
immutable issued summary; correct source records through an audited procedure
and issue a new snapshot. Never directly rewrite shared clinical history to hide
an incident. Stop affected flows if integrity or cross-user isolation fails.

For suspected exposure, isolate the affected public endpoint, revoke relevant
shares/sessions, preserve protected evidence, and notify the assigned incident
and privacy leads via their established process. They decide obligations and
communications. This repository supplies no invented notification deadline.

## Required release record

Before admitting patients, attach named primary and backup responders, clinical
and privacy approval, real Supabase Auth/Storage/grant checks, frontend pagination
and mutation rollout, provider corpus/billing results, a clean hosted CI run,
required branch checks, approved image/rollback digest, measured staging load
under deployment limits, alert delivery, live migration/rollback/failure rehearsal,
and a timed managed-PITR plus object restore. These are still pending external
evidence; no production deployment was performed.
