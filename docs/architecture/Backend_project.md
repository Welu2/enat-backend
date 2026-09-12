# Voice-Based Amharic Clinical Intake App for Maternal Health
## Project Overview

Build the backend for a voice-first web app that helps pregnant women in Ethiopia do daily voice check-ins in Amharic. The app transcribes her speech, extracts structured clinical data (symptoms, food log, supplement adherence), has her confirm each extracted item, checks confirmed data against a fixed Ethiopian ANC danger-sign protocol, and periodically generates a clinician-readable summary accessible via a shareable link + QR code.

**Stack**: FastAPI (Python) backend, Supabase (Postgres) for database + auth, Addis AI for both ASR/TTS and LLM-based extraction.

**Core design principle**: the LLM is used ONLY for (a) transcription, (b) structured extraction from natural speech, and (c) light natural-language phrasing of confirmations. It is NEVER used to make clinical judgment calls — danger-sign detection is a deterministic lookup against a fixed list, not an LLM decision. Keep this separation strict and auditable throughout the codebase.

---

## Data Models (Supabase / Postgres)

```sql
users (
  id uuid primary key,
  email text,
  created_at timestamp
)

supplements (
  id uuid primary key,
  user_id uuid references users(id),
  name text, -- e.g. "iron", "folic_acid", "other"
  active boolean default true,
  reminder_enabled boolean default true,
  reminder_time time,
  created_at timestamp
)

appointments (
  id uuid primary key,
  user_id uuid references users(id),
  appointment_date date,
  last_summary_generated_at timestamp,
  reminder_lead_days int default 2
)

check_ins (
  id uuid primary key,
  user_id uuid references users(id),
  timestamp timestamp,
  symptoms jsonb, -- array of {raw_text, category, duration, severity, danger_sign, confirmed}
  food_log jsonb, -- {raw_text, confirmed}
  supplement_check jsonb, -- {supplement_name, taken_today, confirmed} or null
  closing_mentions jsonb, -- array of {raw_text, topic, confirmed}
  danger_sign_triggered boolean default false
)

summaries (
  id uuid primary key,
  user_id uuid references users(id),
  period_start date,
  period_end date,
  generated_at timestamp,
  content_json jsonb,
  share_link_slug text unique,
  qr_code_url text
)
```

---

## Fixed Reference Data (hardcode as constants, not DB-editable for MVP)

### Danger sign categories (deterministic lookup list):
```python
DANGER_SIGN_CATEGORIES = [
    "vaginal_bleeding",
    "swelling_hands_face",
    "blurred_vision",
    "severe_abdominal_pain",
    "fluid_leakage",
    "severe_headache",
    "persistent_nausea_vomiting",
    "high_fever",
    "convulsions_loss_of_consciousness",
    "difficulty_breathing",
    "severe_weakness_or_backache",
    "abnormal_fetal_movement",
]
```

### Nutrition/closing topics (informational, no danger logic attached):
```python
NUTRITION_TOPICS = ["dietary_intake", "therapeutic_food", "breastfeeding_intent"]
```

---

## Core Pipeline (implement as a sequence of clearly separated functions/services — don't collapse into one big handler)

### 1. Audio ingestion endpoint
`POST /checkin/{session_id}/respond`
- Accepts an audio blob (from browser mic) for the current question in the sequence.
- Passes audio to Addis AI ASR → returns Amharic transcript.

### 2. Extraction service
- Takes the transcript + the current question stage (symptoms / food / supplement / closing) as context.
- Calls Addis AI LLM with a few-shot extraction prompt (see "Extraction Prompt Spec" below) constrained to return structured JSON matching the check_ins schema fields for that stage.
- Validates the JSON response against a schema (use Pydantic models) before proceeding — reject/retry on malformed output, never pass unvalidated LLM output downstream.

### 3. Danger-sign lookup (deterministic — no LLM involved)
```python
def check_danger_sign(category: str) -> bool:
    return category in DANGER_SIGN_CATEGORIES
```
This function is the ONLY thing allowed to set `danger_sign: true`. The LLM extraction step should not be trusted to self-report this flag — recompute it server-side from the extracted `category` value every time.

### 4. Verification flow
- For each extracted item, return it to the frontend for confirmation.
- `POST /checkin/{session_id}/verify` — accepts item id + confirmed (true/false) + optional corrected value.
- Only items with `confirmed: true` are eligible to be written into the final `check_ins` record.

### 5. Session completion
- `POST /checkin/{session_id}/complete` — writes the finalized, confirmed check_ins row to Supabase.
- If any confirmed symptom has `danger_sign: true`, set `danger_sign_triggered: true` on the row and return a flag to the frontend to show the alert screen.

### 6. Summary generation
`POST /summary/generate` (also callable by a scheduled job — see Reminders below)
- Pulls all confirmed check_ins between `last_summary_generated_at` (or account creation) and now, for the user.
- Aggregation logic:
  - Danger signs: list individually with dates, not deduplicated/averaged.
  - Food log: simple list by date, no scoring.
  - Supplement adherence: count of "taken" days vs. total days tracked.
  - Closing mentions: list with dates and topic.
- Writes a new `summaries` row with `content_json` = the aggregated structure, generates a unique `share_link_slug`, and generates a QR code image (encode the share link URL) — store the QR image (e.g., in Supabase storage) and save its URL to `qr_code_url`.
- This summary is a **snapshot** — once generated, its `content_json` does not change even if new check-ins occur afterward.

### 7. Public summary view (read-only, no auth)
`GET /summary/public/{share_link_slug}`
- Returns the snapshotted `content_json` for display. No login required — access is via possession of the link/slug. Do not expose any other user data via this endpoint.

### 8. Reminders (scheduled job, e.g. via a cron/background task)
- Daily job checks each user:
  - No appointment on record → queue "set your appointment" reminder.
  - Active supplement on record → queue reminder at their configured `reminder_time`.
  - Appointment date within `reminder_lead_days` → queue "appointment approaching" reminder, AND trigger summary auto-generation (§6) ahead of the appointment.
- For MVP, reminders are in-app/web push only — no SMS/telephony (deliberately, to avoid carrier/regulatory dependencies).

---

## Extraction Prompt Spec (for the LLM extraction step)

Build this as a few-shot prompt with:
- Clear instruction that output must be valid JSON matching the schema for the current stage only (don't ask it to extract everything at once — one stage's schema per call).
- 3-5 example Amharic input/output pairs per stage (symptoms, food log, supplement check, closing) covering both single-item and multi-item extraction from one utterance.
- Explicit instruction: if nothing relevant is mentioned, return an empty result for that field rather than guessing/inventing content.
- Instruction to preserve `raw_text` verbatim (the original transcript segment) alongside the structured fields, so nothing is silently paraphrased away before human verification.

---

## API Endpoint Summary

```
POST /auth/signup
POST /auth/login
GET  /users/me
POST /users/me/supplements
PUT  /users/me/supplements/{id}
POST /users/me/appointment
PUT  /users/me/appointment

POST /checkin/start                     -> creates session, returns first question stage
POST /checkin/{session_id}/respond      -> audio in, transcript + extraction out
POST /checkin/{session_id}/verify       -> confirm/correct an extracted item
POST /checkin/{session_id}/complete     -> finalize session, write check_ins row
GET  /checkin/history                   -> list past check_ins for the user

POST /summary/generate                  -> generate a new summary snapshot
GET  /summary/latest                    -> most recent summary for the user
GET  /summary/public/{share_link_slug}  -> public read-only summary view

GET  /reminders                         -> current pending reminders for the user
```

---

## Non-negotiable Implementation Rules

1. Danger-sign flags are ALWAYS recomputed server-side from a fixed category list — never trust an LLM-provided boolean directly.
2. Nothing enters a `check_ins` row or a `summaries` row until it has passed through user confirmation (`confirmed: true`).
3. No nutritional scoring, advice, or diagnosis logic anywhere in the backend — food log and nutrition mentions are recorded as-is, never evaluated.
4. Supplement check-in questions are only generated/asked if an active supplement record exists for the user — do not hardcode a daily yes/no for users with none.
5. Summaries are immutable snapshots once generated — do not recompute `content_json` for an existing summary row when new check-ins arrive.
6. Public summary access is link/slug-based only — no doctor accounts, login, or patient search/matching in this MVP.

---

## What NOT to build in this pass

- Doctor accounts, authentication, or a multi-patient dashboard
- SMS or phone-call/IVR delivery of anything
- Any nutrition scoring/recommendation logic
- MUAC as a voice-extractable field
- Multi-language support beyond Amharic for the check-in flow itself (UI language toggle for static text is a separate, frontend-only concern — not a backend/database concern)

---

## Suggested Build Order (for a working demo, not necessarily production-ready)

1. Auth + user setup (supplement/appointment initial config)
2. Audio ingestion → ASR → raw transcript round-trip working end-to-end (validate Addis AI integration first, before extraction logic)
3. Extraction service for the symptoms stage only, with the danger-sign lookup wired in
4. Verification + session completion for symptoms stage
5. Extend to food log, supplement check, closing question stages
6. Summary generation + aggregation logic
7. Share link + QR code generation, public summary view
8. Reminders (can be simplified/mocked for demo if time is short — this is the lowest-risk piece to cut if behind schedule)
