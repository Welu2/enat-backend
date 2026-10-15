# Phase 5 operations: implementation and verification evidence

Evidence dates: 14–15 October 2026. All database records, artifacts and users in these
rehearsals are synthetic. No live Supabase project or staging/production service
was accessed. Current release dependencies are in the
[readiness plan](../production_readiness_plan.md) and
[operations runbook](operations-runbook.md).

## Delivered

- A patched Python 3.12/Alpine 3.24 container with non-root execution, hash-locked
  binary wheels, real FFmpeg validation and graceful shutdown. The
  [Compose template](../deploy/compose.yaml) separates two APIs, worker, scheduler
  and migration credentials and sets explicit CPU, memory, PID and tmpfs limits.
- A serialized, checksum-verified migration runner and additive migration 009.
  Applied status commits with schema changes; failed attempts retain a safe
  SQLSTATE. Fresh, legacy, concurrent-run, rollback and checksum-drift cases pass.
- Async liveness and bounded readiness, independent of provider health. Readiness
  has a dedicated execution lane, a 1.25-second HTTP deadline and a nonblocking
  guard preventing abandoned database probes from accumulating.
- Structured redacted request/job logs, server-generated correlation IDs even on
  early rejections, sampled OTLP traces and W3C context through providers/outbox.
  Protected API and worker metrics cover latency/errors, loop lag, pools, queue
  state/age, provider attempts/errors, confirmation failures and share operations.
  No patient identifiers or text are metric labels or captured span payloads.
- Stable cursor pagination with default 50/max 100 on history, notifications,
  reminders and supplements. Array response bodies remain compatible; clients
  must follow X-Next-Cursor. Reports explicitly page beyond 1,000 rows. A
  production-shaped history query uses checkin_history_cursor and reads 51 rows
  from a 10,000-row owned history without a full-table sort.
- AES-256-GCM backups of a consistent PostgreSQL snapshot plus a separately
  provided immutable object snapshot. Restore authenticates before mutation,
  verifies database/object hashes and references, preserves grants, and rejects
  occupied targets. Temporary plaintext requires a private encrypted scratch
  volume. Managed PITR and remote backup storage still need actual infrastructure.
- Bounded cleanup of expired security state and expiration of stale drafts
  without erasing clinical content. Medical retention/deletion policy is an
  unresolved approval dependency, not an arbitrary hard-coded purge period.
- A [Grafana dashboard](../deploy/grafana-dashboard.json), private Prometheus
  scrape configuration, nine alert rules and alert firing tests, plus concrete
  deployment, provider, queue, slow-DB, rotation, correction, share compromise,
  rollback, restore and incident procedures.

## Verification

| Gate | Local result |
|---|---|
| Unit/HTTP tests | 208 passed, outbound network blocked |
| Fresh PostgreSQL 16 | 60 passed; 2 legacy-only cases skipped |
| Synthetic legacy upgrade | 62 passed, migrations 001–009 |
| Types/style/contracts | Strict mypy on 12 boundary files; Ruff; 54 Postman examples and deterministic OpenAPI |
| Dependency/source/secrets | Both locked graphs clean; Bandit covers application and backup tool; source/history secret patterns clean |
| Container | Non-root/read-only/no-network smoke, real audio decoding, unauthorized access, unavailable readiness and graceful stop pass |
| Container security | Zero HIGH/CRITICAL findings on the refreshed 14 October advisory database; no vulnerability exceptions |
| Deployment/monitoring | Real Compose services and migration container pass; four authenticated scrapes, 13 dashboard queries, local outage notification and resource-limit assertions pass; missing-target/outage/job alert tests pass |
| Capacity under deployment limits | 90,000 scheduled requests/30 minutes; 2 CPUs per API; p95 25 ms, p99 48 ms; 13 transport failures (0.0144%); 150-second outage and recovery pass |
| Encrypted restore | Corruption rejected before mutation; database rows, schema ledger, object bytes and restricted grants verified |
| Image compatibility | Candidate forward/rollback/forward passes on unchanged schema 009 and the same owned record |

Final image:
`sha256:94a8556cadc7f1b0b5cdc4baebdb7ceae537c6eec2b46a2fa43fdc83f114d1e4`.

Retained previous candidate:
`sha256:878b31ec70c3b7f64d209cebb5871c33840457611b165be0bc5858a3312c50f9`.

Both scan clean at HIGH/CRITICAL. The previous candidate predates the final
early-error request-ID fix. These are two candidates from this session, not an
approved historical production release. Each image startup/readiness/history/
shutdown step took about 6.2–6.4 seconds. Schema and saved row identity remained
unchanged. An initial rehearsal could not find an older untagged build; retaining
explicit candidate tags resolved the local artifact-retention issue. Production
must retain immutable registry digests, not rely on Docker's untagged cache.

## Capacity evidence and limits

Two 30-minute runs each scheduled 90,000 requests at 50 requests/second against two
Uvicorn processes and real PostgreSQL. Each workload adds 1,000 synthetic users and
100,000 history records alongside the retained integration fixtures. The mix is
80% paginated history, 10% profile reads and
10% notification-dismiss writes. Authentication uses real opaque sessions and the
restricted application role; rate limits remain enabled. Synthetic proxy addresses
represent distinct clients. One API is killed and restarted; the harness polls
readiness and routes to available instances.

| Measurement | Initial run | Diagnostic repeat |
|---|---:|---:|
| End-to-end p95, including scheduler delay | 137 ms | 21 ms |
| End-to-end p99, including scheduler delay | 7.236 s — failed | 32 ms — passed |
| HTTP request p99 excluding scheduler delay | Not captured | 30 ms |
| Load-generator scheduling p99 | Not captured | 2.4 ms |
| Transport errors | 6 / 90,000 | 3 / 90,000 |
| Both instances recovered | Yes | Yes |

The first failure is retained in artifacts/operations/load-previous-*.json and
is not rewritten as a pass. Its cause was not isolated. The repeat added separate
client-scheduling and request measurements and captured server metrics; it passed
the 500-ms p95 and 1-second p99 thresholds. Three transport errors during forced
failure are included (0.0033%); zero-error service is not claimed.

Those host-process runs used a local 8-logical-CPU Linux host, Python 3.12.3 and
two API pools of ten connections. They did not enforce Compose CPU/memory limits
and are not multi-host availability or live provider tests. The later readiness/
early-error correlation changes do not alter the tested authenticated read/write
queries; their targeted unit, integration and image checks pass. Repeat on actual
staging hardware/limits. No voice latency, medical ASR accuracy, currency spend,
99.9% availability, 15-minute RPO or 60-minute production RTO is claimed.

## Compose deployment rehearsal

The follow-up rehearsal starts deploy/compose.yaml with staging configuration
validation, synthetic credentials and a disposable migrated PostgreSQL database.
The API pair, worker and scheduler run as UID 10001 with read-only roots, dropped
capabilities, no privilege escalation, 128-PID and 512-MiB limits. The migration
container verifies the same nine-migration ledger. An internal Docker network
prevents external provider/Auth traffic; the local Linux harness uses private
bridge addresses. The application image is the same scanned digest listed above.

The first full Compose run used one CPU per API, scheduled 90,000 requests over
30 minutes and held one API down for 150 seconds. It **failed** the p99 gate:
275-ms p95 and 1.708-second p99. There were 142 transport failures, 117 HTTP 503s
and 397 requests with no ready backend (656/90,000, 0.729%). Errors accumulated
during failure/recovery and did not increase afterward. This failed evidence is
retained; the template now assigns two CPUs to each API, with one each for worker
and scheduler. Pool sizes and memory limits are unchanged. The harness now probes
replicas independently with a 250-ms connect timeout and 1.5-second probe deadline.

The full repeat **passed** with the same image, workload, duration, outage and
acceptance thresholds:

| Measurement | One CPU per API | Two CPUs per API + independent probes |
|---|---:|---:|
| Scheduled requests / duration | 90,000 / 1,800 s | 90,000 / 1,800 s |
| End-to-end p95 | 275 ms | 25 ms |
| End-to-end p99 | 1,708 ms — failed | 48 ms — passed |
| Request p99 excluding generator delay | 1,706 ms | 46 ms |
| Load-generator scheduling p99 | 3.7 ms | 3.1 ms |
| Transport / HTTP 503 / no-ready-backend failures | 142 / 117 / 397 | 13 / 0 / 0 |
| Overall error rate | 0.729% | 0.0144% |
| All services recovered; local alert received | Yes | Yes |

The resource and probe changes were validated together; their individual effects
were not isolated. Worker and scheduler retain one CPU each, and all four services
retain 512 MiB and their original database pools. The report's `python` field is
the host load-generator version; the service runtime is identified by the image
digest. This remains a single-host Linux rehearsal with a local database, not
remote staging, multi-host failure tolerance or live voice-provider evidence.

Prometheus successfully scraped all four protected exporters. The real outage
rule fired and reached a local Alertmanager-compatible test sink; all four
targets recovered afterward. The scheduler and worker delivered a committed
outbox event exactly once. All 13 Grafana panel queries execute against the live
synthetic metrics; job delay and scheduler delay are separate series. The missing-
API-target alert case is covered by an additional promtool regression test.
No Grafana UI or human notification channel was tested. Ingress monitoring must
also cover errors rejected before ASGI, including Uvicorn concurrency-limit 503s.
The successful repeat had no HTTP 503s or no-ready-backend failures; its 13
transport failures occurred around the forced kill and remain in the gate's
denominator. Rehearsal containers, network and database were removed afterward.

The initial short Compose check passed 1,000 requests with no errors (434-ms p95,
577-ms p99). Short checks validate wiring only and do not satisfy the capacity gate.
Reports use artifacts/operations/load-compose.json, with previous runs archived as
load-compose-previous-*.json; service logs and dashboard query evidence are separate.

## Reproduce and maintain

Run normal gates from README. PostgreSQL 16 and FFmpeg are required locally.
Use these additional commands in the locked development environment:

```bash
python scripts/test_database.py --fresh
python scripts/test_database.py
ENAT_LOAD_SECONDS=120 python scripts/test_database.py --fresh --load
python scripts/test_database.py --fresh --load
ENAT_REHEARSAL_IMAGES=enat:phase5-previous,enat:phase5 python scripts/test_database.py --containers
ENAT_LOAD_COMPOSE=1 ENAT_LOAD_IMAGE=enat:phase5 ENAT_LOAD_SECONDS=120 python scripts/test_database.py --fresh --load
ENAT_LOAD_COMPOSE=1 ENAT_LOAD_IMAGE=enat:phase5 python scripts/test_database.py --fresh --load
```

The default load duration is 1,800 seconds; the short run only checks the harness.
The test runner creates/removes isolated databases and refuses live-cluster DSNs
for load/image rehearsals. Container rehearsals require Docker and the two retained
images. Restore tests create empty isolated databases and private temporary files.

CI runs the unit/integration, contract, source/dependency, image, configuration
and short host/Compose rehearsal gates. A workflow_dispatch run adds the full
Compose capacity job against its built and scanned image, including the sustained
outage and local alert-notification assertion.
The first [hosted run](https://github.com/Welu2/enat-backend/actions/runs/38621523163)
failed on commit f4bc3aa. Unit collection collided on the two test_operations.py
modules; pytest now uses importlib mode and package-qualified shared fixtures.
The container job passed image/security/alert checks and 60 fresh-database tests,
then failed the 20-second load gate: 10 forced-crash transport failures out of
1,000 requests (1%), p95 341 ms and p99 3.002 seconds. All services recovered.
CI wiring checks now run for 120 seconds (6,000 requests), retaining the same
forced outage, 50 requests/second, p95/p99 limits and <1% error threshold. This
gives the fixed failure-detection window a larger sample; no errors are excluded
and the full 30-minute capacity requirement remains unchanged.
A local 120-second run then failed latency (p95 1.638 s, p99 2.017 s,
41/6,000 errors) around restart. The generator awaited Docker commands inside
its scheduling loop, creating catch-up bursts. Fault injection now runs in a
separate task, joined before cleanup, so command latency does not pause traffic.
The failed measurements remain archived; this harness change does not alter
service limits or discard errors.
The corrected local run passed all 6,000 requests through the harness: p95 68 ms,
p99 121 ms and 10 transport errors (0.1667%), with both APIs recovered, four
authenticated scrapes and exactly-once outbox delivery. Generator scheduling p99
was 7.5 ms. This two-minute check supplements the earlier full capacity evidence.
The local host-process repeat also passed: p95 38 ms, p99 92 ms and one transport
error out of 6,000 requests, alongside all 62 legacy-upgrade tests.

The corrected [hosted run](https://github.com/Welu2/enat-backend/actions/runs/38764968793)
passed on commit a59e999 on 15 October. Both `test` and `container` passed every
gate. Each two-minute rehearsal attempted 6,000 requests on a four-logical-CPU
Ubuntu runner: host p95/p99 10/11 ms with seven transport errors (0.1167%);
Compose p95/p99 14/17 ms with 12 transport errors (0.2%). Recovery, all four
scrapes and exactly-once outbox delivery passed. The built/scanned Compose image
was sha256:5cac46ac4b3bb340bac21941cc5bfdc2f586700e8dd6190625eb21b981e2c196.
The manual 30-minute capacity job was skipped for this push; the earlier full
local results remain the capacity evidence. Hosted reports were downloaded to
artifacts/hosted/38764968793.

GitHub branch protection on `master` now requires up-to-date `test` and
`container` checks from GitHub Actions (app 15368), including for administrators.
Force pushes and branch deletion are disabled. The saved configuration was read
back and verified. This protects merges; it does not approve a patient release.
Reports are under ignored artifacts/operations and artifacts/security; CI retains
them for 30 days. Archive release evidence and images for the approved retention
period. The dependency manifest records lock hashes and tool versions; container
reports record exact image/scanner digests.

## Still required before patient release

Supply the staging project and deployment/monitoring/backup access; run real
Supabase Auth/Storage/grant tests, staged migration/rollback/failure drills, alert
delivery and managed-PITR/object recovery. Validate frontend pagination and retry
contracts, real-provider Amharic quality and 20-concurrent-voice latency, and
approved monetary budgets. Obtain clinical and privacy decisions, retention/
deletion/export policy, named primary/backup responders and an accountable
supervised-pilot release decision. These dependencies keep
full phase/release acceptance open despite the completed local implementation.
