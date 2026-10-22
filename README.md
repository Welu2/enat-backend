# EnatAI (እናት AI) — Voice-Based Amharic Clinical Intake System for Maternal Health

EnatAI is a voice-first clinical intake and monitoring platform designed for pregnant women in Ethiopia. Using natural Amharic speech, pregnant mothers perform daily check-ins on their mobile or web devices. The platform transcribes speech into text, extracts structured clinical data, presents localized Amharic verification read-backs, checks symptoms against standard Ethiopian Antenatal Care (ANC) danger-sign protocols, and generates immutable clinician summaries accessible via shareable links and QR codes.


**Security migration:** Phase 1 changes authentication, patient-table credentials,
summary sharing, and speech playback. Read [the deployment and client migration
notes](docs/phase1-security.md) before upgrading. Sharing remains disabled pending
privacy review; the service is not yet approved for production patient use.

The [care portal and offline check-in backend](docs/care-offline-mvp.md) adds
patient-approved clinician/trusted-person access, alerts, and duplicate-safe offline
ingestion. Features default off. Frontend screens and the local queue remain a
separate integration step in the [MVP implementation plan](docs/clinician-offline-mvp-plan.md).

The patched container now passes the [security gate](docs/security-remediation.md).
Local Phase 5 implementation and load/restore evidence are recorded in
[operations verification](docs/phase5-operations.md). Live staging, clinical/privacy
approval and operational ownership remain release requirements.

Release candidate publication, digest promotion/rollback, guarded live staging
checks, Auth capacity tests and voice evaluation are documented in
[release delivery](docs/release-delivery.md). These tools keep clinical/privacy
and live operational acceptance explicit.

Migration 010 adds [personal-data export, deletion-review requests and privacy/share
audit events](docs/privacy-operations.md). Enable these only after configuring the
approved policy, support channel and request owner. Existing deployments need the
documented schema-compatibility bridge before this migration.

---

## 🛡️ Core Clinical & Safety Principles

1. **Strict Separation of AI & Medical Judgment**:  
   The LLM (via Addis AI) is used **EXCLUSIVELY** for:
   - Speech-to-text transcription (ASR)
   - Converting Amharic speech transcripts into structured JSON schemas
   The application builds Amharic confirmation phrases deterministically from
   the extracted fields; speech synthesis only renders those phrases as audio.
   
   **The LLM is NEVER allowed to make clinical decisions or diagnose danger signs.** Danger-sign classification is strictly computed by a deterministic server-side rules engine comparing extracted categories against fixed Ethiopian ANC protocols.

2. **Mandatory Patient Verification Loop**:  
   Nothing enters the permanent `check_ins` record or clinician `summaries` until it has been explicitly confirmed by the patient (`confirmed: true`).

3. **Deterministic Danger Sign Flagging**:  
   One versioned policy preserves recognized danger categories regardless of the severity label. Unclassified or missing observations remain uncertain. Clinical review of the categories, extraction examples, and localized wording is required before patient use.

4. **Immutable Clinician Summaries**:  
   Once a clinician summary is generated, its JSON content is an immutable snapshot of patient health history for doctor visits.

---

## 🚀 Key Features

- **Multi-Stage Voice Intake Session**: Guided 4-stage check-in (`symptoms`, `food`, `supplement`, `closing`).
- **Flexible Item-Level Correction**:
  - Manual text/value edits (`raw_text`, `severity`, `duration`, etc.)
  - Single-item voice re-recording (`POST /checkin/{id}/items/{item_id}/voice-correct`)
  - Additional stage recordings after pending items are resolved (`POST /checkin/{id}/respond`)
- **Automated Clinician Summary Generation**:
  - Automatically generated **1 day before scheduled ANC appointment**.
  - Monthly fallback generation (**every 30 days**) if no appointment date is set.
  - On-demand generation; explicit, expiring patient-controlled links and private QR responses when sharing is enabled.
- **In-App Notifications & Reminders**:
  - Daily supplement intake reminders.
  - Approaching ANC appointment alerts.
  - Summary report readiness notifications.
- **Full Amharic Localization**: All read-back verification phrases, prompts, duration formatting (hours, days, weeks, months), and supplement names are rendered in Amharic.

---

## 🛠️ Tech Stack & Architecture

- **Backend Framework**: Python 3.12, FastAPI, Pydantic v2, Uvicorn, PostgreSQL workers.
- **AI & Speech Services**: [Addis AI](https://addis.ai) API:
  - Custom Amharic Speech-to-Text (ASR)
  - `chat_generate` endpoint for structured JSON extraction
- **Database & Authentication**: Supabase (PostgreSQL) with Row-Level Security and online JWT verification. ES256/RS256 are accepted; legacy HS256 requires an explicit expiry setting.
- **QR Code Generation**: `qrcode` Python library (generates PNG QR codes encoding public summary URLs).
- **Testing**: `pytest`, `pytest-asyncio`, `unittest.mock`.

---

## 📊 Database Schema (Supabase / Postgres)

The authoritative schema is the ordered [migrations](migrations/). Migration 007
adds session versions and terminal results, unique check-in session references,
confirmation enforcement, canonical food/supplement arrays, mutation results,
outbox events, immutable report windows, and explicit appointment attendance.
Patient-table access uses the restricted `enat_app` role and owner RLS policies.
Migration 008 adds durable jobs, scheduler checkpoints/leases, reminder occurrence
keys, and restricted `enat_worker` grants. See the [Phase 3 worker runbook](docs/phase3-resilience.md).
See [Phase 2 rollout and verification](docs/phase2-integrity.md) before upgrading;
the old client request format is incompatible with the new workflow contract.


---

## 📋 Ethiopian ANC Danger Sign Reference Categories

The deterministic rules engine flags symptoms against the following 12 protocol categories defined in the Ethiopian ANC Guidelines:

1. `vaginal_bleeding` — የማህፀን ደም መፍሰስ
2. `swelling_hands_face` — የእጅ ወይም የፊት እብጠት
3. `blurred_vision` — የእይታ ብዥታ
4. `severe_abdominal_pain` — ከባድ የሆድ ህመም
5. `fluid_leakage` — የፈሳሽ መፍሰስ
6. `severe_headache` — ከባድ ራስ ምታት
7. `persistent_nausea_vomiting` — የማይቋረጥ ማስታወክ
8. `high_fever` — ከፍተኛ ትኩሳት
9. `convulsions_loss_of_consciousness` — መንቀጥቀጥ ወይም ራስን መሳት
10. `difficulty_breathing` — የመተንፈስ ችግር
11. `severe_weakness_or_backache` — ከባድ ድካም ወይም የጀርባ ህመም
12. `abnormal_fetal_movement` — የፅንስ እንቅስቃሴ መለወጥ

---

## ⚡ Installation & Local Setup

### 1. Prerequisites
- Python 3.12 on Linux (the supported build and CI environment)
- Supabase Account & Project
- Addis AI API Key

### 2. Environment Configuration
Copy [`.env.example`](.env.example) to `.env` and supply development credentials.
The actual settings are `ADDIS_API_KEY`, `SUPABASE_URL`,
`SUPABASE_SERVICE_ROLE_KEY` (Storage), `SUPABASE_PUBLISHABLE_KEY` (Auth),
`DATABASE_URL` (the constrained `enat_app` role), `PUBLIC_BASE_URL`, and
`CORS_ORIGINS`; the remaining options are documented in the template.
`PUBLIC_BASE_URL` points at the frontend. CORS accepts only the configured origins.

`ENVIRONMENT` accepts `development`, `test`, `staging`, or `production`.
Development routes default off. Staging/production reject development routes,
embedded scheduling, non-HTTPS service URLs, and empty/wildcard/localhost CORS
origins. These configuration checks do not close the other production blockers
in [the readiness plan](production_readiness_plan.md).

### 3. Install Dependencies
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements-dev.lock
python -m pip check
```

Use `requirements.lock` for runtime-only installations. The `.txt` files are
resolver inputs; committed `.lock` files pin transitive versions and artifact
hashes. Regenerate both on Python 3.12/Linux, then run the full checks:

```bash
python -m piptools compile --generate-hashes --output-file=requirements.lock requirements.txt
python -m piptools compile --generate-hashes --constraint=requirements.lock --output-file=requirements-dev.lock requirements-dev.txt
```

### 4. Database Configuration
Apply migrations `001` through `012` with `MIGRATION_DATABASE_URL` and
`python -m app.migrate`, using a separate migration owner. The runner serializes
execution, verifies checksums and records failures. Rehearse existing untracked
databases before baselining; see [the runbook](docs/operations-runbook.md).
Provision the `enat_app` login and use it for `DATABASE_URL`; install ffmpeg/ffprobe.
See [Phase 1 deployment notes](docs/phase1-security.md) for grants, storage, and rollback requirements.
Generic prompt assets use the `audio-prompts` bucket. QR PNGs are generated privately
in memory; the legacy `summary-qr-codes` bucket is made private by migration 005.
The [Phase 0 inventory](docs/production-baseline.md) is historical. Migration 005
repairs the recorded schema gaps and introduces isolation; deployed Supabase
verification and the remaining production-readiness phases are still required.

### 5. Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Access interactive OpenAPI docs at `http://localhost:8000/docs`.
`/health` reports process liveness only.

For local debugging only, `ENABLE_DEV_ROUTES=true` adds `/dev/asr-test` and
`/reminders/run-daily`. Both routes are absent by default, including from OpenAPI.
`/reminders/run-daily` now returns 410. Embedded scheduling is removed and
`ENABLE_EMBEDDED_SCHEDULER=true` is rejected in every environment. Deploy separate
processes with restricted `WORKER_DATABASE_URL` credentials:

```bash
PROCESS_ROLE=worker python -m app.jobs scheduler
PROCESS_ROLE=worker python -m app.jobs worker
PROCESS_ROLE=worker python -m app.jobs status
```

The scheduler uses `REMINDER_CRON_HOUR` in `Africa/Addis_Ababa`; multiple instances
coordinate through a database lease. Jobs and outbox deliveries survive restarts.
Follow the [worker, failed-job replay, and prompt provisioning runbook](docs/phase3-resilience.md)
for credentials, catch-up behavior, versioned audio, and staging gates.

### 6. Run Automated Checks
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
python scripts/security_audit.py
docker build --pull -t enat:release .
python scripts/smoke_container.py
python scripts/scan_container.py
```

Tests override inherited settings with dummy values before application imports
and block outbound TCP/UDP connections. No live credentials or providers are
required. Database tests require local PostgreSQL 16 binaries and create isolated
temporary clusters with synthetic data. Security scans need advisory/registry
network access. Reports and CycloneDX SBOMs are written to `artifacts/security/`
and uploaded by CI, including on failed scans.

To rehearse the actual Compose deployment on Linux with Docker and synthetic data:

```bash
ENAT_LOAD_COMPOSE=1 ENAT_LOAD_IMAGE=enat:release ENAT_LOAD_SECONDS=120 python scripts/test_database.py --fresh --load
ENAT_LOAD_COMPOSE=1 ENAT_LOAD_IMAGE=enat:release python scripts/test_database.py --fresh --load
```

The first command checks the harness; the second runs the 30-minute capacity gate
with a 150-second API outage. Both use the deployment template's CPU/memory/PID
limits, separate API/worker roles and a disposable database. An internal Docker
network prevents provider calls; the Linux host reaches private bridge addresses.
Prometheus scrapes all four services, and the full run requires an outage alert
to reach a local test receiver. This does not test human paging or managed PITR.
Results are written to `artifacts/operations/load-compose.json`. No deployment
secrets are loaded. See [operations evidence](docs/phase5-operations.md) for limits.

See [Phase 4 evidence and gate policy](docs/phase4-verification.md) for the strict
type-check scope, patient journey, and security remediation. The default production
contract is committed as [OpenAPI](docs/openapi.json) and a generated
[operation inventory](docs/api-operations.md). After intentional contract edits,
regenerate Postman first, then run `python scripts/check_contracts.py --write`;
review the resulting diffs. CI checks never rewrite these artifacts.

---

## 🌐 API Overview

The complete generated method/path list is in [API operations](docs/api-operations.md).

### Authentication
- `POST /auth/signup` — Register new user account.
- `POST /auth/login` — Authenticate and receive Bearer Access Token.

### User Profile & Settings
- `GET /users/me` — Fetch complete user profile, supplements, appointment settings, and pending notifications.
- `POST /users/me/supplements` — Add a supplement (e.g. Iron, Folic Acid).
- `PUT /users/me/supplements/{id}` — Update supplement reminder settings.
- `POST /users/me/appointment` — Set ANC appointment date & reminder lead days.
- `PUT /users/me/appointment` — Reschedule using the current appointment version.
- `POST /users/me/appointment/transition` — Explicitly record completed, missed, or rescheduled attendance.

### Voice Intake Workflow
- `GET /checkin/{session_id}/state` — Resume from the current version, draft and terminal result.
- `POST /checkin/start` — Start a new 4-stage intake session.
- `POST /checkin/{session_id}/respond` — Upload voice recording (`audio`) for current stage.
- `POST /checkin/{session_id}/verify` — Confirm or manually edit an extracted item (`raw_text`, `severity`, `duration`).
- `POST /checkin/{session_id}/items/{item_id}/voice-correct` — Re-record voice specifically for a single pending item.
- `POST /checkin/{session_id}/complete` — Complete current stage or finalize check-in session.

### History & Summaries
- `GET /checkin/history` — List owned history, default 50/max 100. Continue using `X-Next-Cursor` as the `cursor` query parameter.
- `GET /checkin/history/{checkin_id}` — Get full detailed record of a single past check-in.
- `POST /summary/generate` — Manually generate a clinician summary snapshot.
- `POST /summary/check-automatic` — Trigger pre-appointment / monthly auto-summary check.
- `GET /summary/latest` — Fetch latest summary snapshot for the user.
- `POST /summary/{summary_id}/shares` — Explicit consent and expiring share creation (disabled pending review).
- `GET /summary/{token}` — Resolve a scoped, unexpired bearer share.
- `DELETE /summary/shares/{share_id}` — Revoke an owned share.

### Notifications & Reminders
- `GET /notifications` — List active, un-dismissed notifications (supplement reminders, appointment alerts, report generated alerts).
- `POST /notifications/{notification_id}/dismiss` — Mark a notification as dismissed.

---

## 📁 Repository Structure

```
EnatAI/
├── app/
│   ├── api/
│   │   └── routes/         # FastAPI endpoint route handlers (auth, checkin, notifications, summary, users)
│   ├── core/               # App constants & configuration settings
│   ├── db/
│   │   ├── client.py       # Supabase client singleton
│   │   └── repositories/   # Database repositories (appointments, check_ins, reminders, summaries, supplements, users)
│   ├── models/             # Pydantic schema models for requests & responses
│   └── services/           # Business logic (ASR, Addis AI LLM extraction, checkin sessions, danger signs, summary, reminders)
├── tests/                  # Pytest automated test suite
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependency requirements
└── README.md               # Project documentation
```
