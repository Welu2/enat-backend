# EnatAI Backend — Frontend Integration & API Guide

> **Base URL**: `http://localhost:8000` (or your deployed backend host)  
> **Target Audience**: Mobile & Web Frontend Developers  
> **Primary Language**: Amharic (speech-to-text, verification read-back phrases, clinical prompt messages)  

---

## Table of Contents

1. [Authentication Flow](#1-authentication-flow)
2. [User Settings & Profile Management](#2-user-settings--profile-management)
3. [Voice Check-in Intake Workflow](#3-voice-check-in-intake-workflow)
   - [Stage 1: Symptoms](#stage-1-symptoms)
   - [Stage 2: Food Log](#stage-2-food-log)
   - [Stage 3: Supplement Tracking](#stage-3-supplement-tracking)
   - [Stage 4: Closing Questions](#stage-4-closing-questions)
4. [Verification & Correction Flows](#4-verification--correction-flows)
   - [Manual Text Verification & Edits](#a-manual-text-verification--edits)
   - [Single-Item Voice Correction](#b-single-item-voice-correction)
   - [Full-Stage Voice Re-recording](#c-full-stage-voice-re-recording)
5. [Check-in History & Details](#5-check-in-history--details)
6. [Clinician Summaries & QR Sharing](#6-clinician-summaries--qr-sharing)
7. [Notifications & Reminders System](#7-notifications--reminders-system)
8. [Error Handling & Best Practices](#8-error-handling--best-practices)

---

## 1. Authentication Flow

The generated [OpenAPI schema](docs/openapi.json) and
[operation inventory](docs/api-operations.md) define current paths, bearer
requirements, request bodies, and mutation headers. CI validates the Postman
examples against this schema.

Authenticated patient endpoints use `Authorization: Bearer <access_token>`.
Health and generic prompts are public; public summary resolution requires an
explicitly created, unexpired bearer share. `/auth/link` and `/auth/logout`
require authentication.

| Endpoint | Request / behavior |
| --- | --- |
| `POST /auth/signup` | `{"email":"mother@example.com","password":"securepassword123"}` → **202**, `status=verification_required`; no session. Confirm email before login. |
| `POST /auth/login` | Email/password → access token, refresh token, expiry, internal user ID and email. Failures return generic 401. |
| `POST /auth/refresh` | `{"refresh_token":"..."}` → rotated session. Replace both tokens atomically. |
| `POST /auth/forgot-password` | Email → generic **202**, whether an eligible account exists or not. |
| `POST /auth/reset-password` | `{"token_hash":"recovery hash from email","new_password":"newsecurepassword123"}` → consumes a recovery OTP, changes password, invalidates previous Supabase sessions. Ordinary access tokens are not accepted as recovery proof. |
| `POST /auth/telegram` | `{"init_data":"Telegram.WebApp.initData"}` → short-lived application bearer token. Launch data must be fresh and can be exchanged only once. Direct `tma` authentication is retired. |
| `POST /auth/link` | Current bearer token plus either `{"access_token":"second verified Supabase token"}` or `{"init_data":"fresh Telegram data"}`. Existing separate accounts return 409; no automatic data merge. |
| `POST /auth/logout` | Current bearer token → **204**; revoke its session and remove the account's device push registrations. |

ES256/RS256 tokens are verified through Supabase Auth on each request. HS256 is
rejected unless an operator sets a short, explicit migration deadline. Auth
outages return 503 and never enable weaker verification. Never log credentials,
recovery hashes, launch data, or bearer shares. Configure the Supabase recovery
email template and frontend callback as described in
[the Phase 1 deployment notes](docs/phase1-security.md).

---

## 2. Maternal Onboarding, Gestational Age Calculation & Profile Management

### 2.1 Calculate Gestational Age & EDD (Instant Live Preview)
Allows the frontend to instantly compute fetal age, trimester classification, and estimated due date (EDD) without storing, as the mother enters or edits her LNMP or ultrasound date.
- **Endpoint**: `POST /users/calculate-gestational-age`
- **Request Body**:
```json
{
  "pregnancy_counting_method": "lnmp",
  "lnmp_date": "2026-05-01"
}
```
*Alternatively, for manual override or ultrasound:*
```json
{
  "pregnancy_counting_method": "manual",
  "manual_gestational_weeks": 16,
  "manual_gestational_days": 3
}
```
- **Response** `(200 OK)`:
```json
{
  "gestational_age_weeks": 16,
  "gestational_age_days": 4,
  "gestational_age_total_days": 116,
  "formatted_age_am": "16 ሳምንት ከ 4 ቀን",
  "formatted_age_en": "16 weeks, 4 days",
  "trimester": "second_trimester",
  "trimester_info": {
    "number": 2,
    "key": "second_trimester",
    "name_en": "2nd Trimester",
    "name_am": "2ኛ ትሪሚስተር (14-27 ሳምንት)",
    "week_range": "14 - 27 weeks"
  },
  "estimated_due_date": "2027-02-05",
  "effective_lnmp_date": "2026-05-01",
  "is_gestational_age_manual": false,
  "days_until_edd": 164
}
```

### 2.2 Submit Initial Onboarding Questions
When a mother registers for the first time, she completes the baseline onboarding questionnaire. Submitting this endpoint calculates and saves her baseline pregnancy metrics, medical history, preferred hospital, and **automatically seeds her supplements** into the supplements database table.
- **Endpoint**: `POST /users/me/onboarding`
- Profile, initial supplements, and first appointment commit in one transaction.
  Supplements accept at most 50 nonempty names or objects containing only
  `{"name":"iron"}`; malformed values return 422 before writes.
- **Request Body**:
```json
{
  "age": 26,
  "area": "urban",
  "pregnancy_counting_method": "lnmp",
  "lnmp_date": "2026-05-01",
  "manual_gestational_weeks": 16,
  "manual_gestational_days": 4,
  "total_pregnancies": 2,
  "live_births": 1,
  "had_c_section": false,
  "child_passed_away": false,
  "past_pregnancy_complications": [
    "preterm_birth",
    "pre_eclampsia"
  ],
  "known_medical_conditions": [
    "hypertension",
    "other"
  ],
  "custom_medical_condition": "Mild seasonal asthma",
  "malaria_endemic_area": true,
  "current_medications": "Methyldopa 250mg daily",
  "supplements": [
    "iron & folic acid",
    "calcium"
  ],
  "hospital": "St. Paul's Hospital Millennium Medical College"
}
```
- **Response** `(200 OK)`: Returns complete `UserProfile` with `onboarding_completed: true` and live calculated `current_pregnancy_status`.

### 2.3 Set or Update Preferred Hospital
Mothers can set or change their preferred delivery / ANC hospital anytime.
- **Endpoint**: `PUT /users/me/hospital` or `PATCH /users/me/hospital`
- **Request Body**:
```json
{
  "hospital": "Tikur Anbessa Specialized Hospital"
}
```
- **Response** `(200 OK)`: Returns updated `UserProfile`.

### 2.4 Get Full User Profile & Settings
Frontend apps can query `GET /users/me` at launch to load all user configuration states, onboarding data, live gestational age progression, supplements, appointment date, and active notifications.
- **Endpoint**: `GET /users/me`
- **Response** `(200 OK)`:
```json
{
  "id": "e81acbf1-5f43-4afc-90be-b2d86c9a6802",
  "email": "mother@example.com",
  "created_at": "2026-08-15T10:00:00Z",
  "age": 26,
  "area": "urban",
  "pregnancy_counting_method": "lnmp",
  "lnmp_date": "2026-05-01",
  "ultrasound_date": null,
  "ultrasound_weeks": null,
  "gestational_age_weeks": 16,
  "gestational_age_days": 4,
  "is_gestational_age_manual": false,
  "effective_lnmp_date": "2026-05-01",
  "estimated_due_date": "2027-02-05",
  "trimester": "second_trimester",
  "total_pregnancies": 2,
  "live_births": 1,
  "had_c_section": false,
  "child_passed_away": false,
  "past_pregnancy_complications": ["preterm_birth"],
  "known_medical_conditions": ["hypertension"],
  "custom_medical_condition": null,
  "malaria_endemic_area": true,
  "current_medications": "Methyldopa",
  "hospital": "St. Paul's Hospital",
  "onboarding_completed": true,
  "current_pregnancy_status": {
    "gestational_age_weeks": 16,
    "gestational_age_days": 4,
    "gestational_age_total_days": 116,
    "formatted_age_am": "16 ሳምንት ከ 4 ቀን",
    "formatted_age_en": "16 weeks, 4 days",
    "trimester": "second_trimester",
    "trimester_info": {
      "number": 2,
      "key": "second_trimester",
      "name_en": "2nd Trimester",
      "name_am": "2ኛ ትሪሚስተር (14-27 ሳምንት)",
      "week_range": "14 - 27 weeks"
    },
    "estimated_due_date": "2027-02-05",
    "effective_lnmp_date": "2026-05-01",
    "is_gestational_age_manual": false,
    "days_until_edd": 164
  },
  "supplements": [
    {
      "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
      "user_id": "e81acbf1-5f43-4afc-90be-b2d86c9a6802",
      "name": "iron & folic acid",
      "active": true,
      "reminder_enabled": true,
      "reminder_time": "09:00:00",
      "created_at": "2026-08-15T10:00:00Z"
    }
  ],
  "appointment": {
    "id": "3a1103c8-8889-4d22-b5e1-77114b001199",
    "user_id": "e81acbf1-5f43-4afc-90be-b2d86c9a6802",
    "appointment_date": "2026-08-20",
    "reminder_lead_days": 2,
    "last_summary_generated_at": null
  },
  "pending_reminders": []
}
```

### Unified Settings Update (Bulk Update All Settings)
- **Endpoint**: `PUT /users/me/settings` or `PATCH /users/me/settings`
- All changes commit together. An unknown or another patient's supplement ID
  returns 404 and rolls back preceding changes. Updating an existing appointment
  requires its current `version`; stale versions return 409.
- **Request Body**:
```json
{
  "appointment": {
    "version": 0,
    "appointment_date": "2026-08-25",
    "reminder_lead_days": 3
  },
  "supplements": [
    {
      "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
      "reminder_enabled": true,
      "reminder_time": "08:30:00"
    }
  ]
}
```
- **Response** `(200 OK)`: Returns updated `UserProfile`.

### Add or Update Supplement
- **Endpoint**: `POST /users/me/supplements` or `PUT /users/me/supplements/{supplement_id}`
- **Request Body**:
```json
{
  "name": "iron",
  "active": true,
  "reminder_enabled": true,
  "reminder_time": "09:00:00"
}
```

### Delete Supplement
- **Endpoint**: `DELETE /users/me/supplements/{supplement_id}`
- **Response** `(200 OK)`: `{"status": "deleted"}`

### Manual Supplement Intake Verification (Skip Stage 3 in Voice Check-in)
Allows the patient to manually confirm supplement intake (e.g. from home screen checklist button). The supplement stage is skipped only when every active named supplement has a confirmed boolean observation today. Unrelated reminders remain pending. Choose a supplement ID or explicit name; no default supplement is inferred. This endpoint requires an `Idempotency-Key` header.
- **Endpoint**: `POST /users/me/supplements/verify` or `POST /users/me/supplements/{supplement_id}/verify`
- **Request Body**:
```json
{
  "supplement_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "supplement_name": "iron",
  "taken_today": true
}
```
- **Response** `(200 OK)`:
```json
{
  "status": "verified",
  "supplement_name": "iron",
  "taken_today": true,
  "logged_at": "2026-08-16T13:00:00Z"
}
```

### Manual 4-Food-Group Logging (Skip Stage 2 in Voice Check-in)
This endpoint requires `Idempotency-Key`; retries return the original logged result.
Allows the patient to select the food groups she ate today directly via a 4-group checkbox UI (`grains`, `proteins`, `dairy`, `fruits_and_vegetables`). Logging food for today automatically **skips Stage 2 (Food)** during the voice check-in session!
- **Endpoint**: `POST /users/me/food/verify` or `POST /users/me/food-log`
- **Request Body**:
```json
{
  "food_groups": [
    "grains",
    "proteins",
    "fruits_and_vegetables"
  ],
  "raw_text": "እንጀራ፣ ሽሮ እና ሰላጣ",
  "items": [
    "እንጀራ",
    "ሽሮ",
    "ሰላጣ"
  ]
}
```
- **Response** `(200 OK)`:
```json
{
  "status": "verified",
  "food_groups": [
    "grains",
    "proteins",
    "fruits_and_vegetables"
  ],
  "raw_text": "እንጀራ፣ ሽሮ እና ሰላጣ",
  "logged_at": "2026-08-25T12:00:00Z"
}
```

### Set or Update ANC Appointment
Send `Idempotency-Key`. Initial creation omits `version`; updates must include
`version` from the current appointment response. A date update is an explicit
reschedule and records an event. Reports never change attendance or contact number.

`POST /users/me/appointment/transition` accepts, for example,
`{"action":"completed","version":0}` or `{"action":"missed","version":0}`.
A new date uses `{"action":"rescheduled","version":1,"appointment_date":"2026-11-01"}`;
optional `anc_contact_number` explicitly selects the next contact. No contact
advancement happens automatically. Future visits cannot be marked completed/missed.
The appointment response includes `status` and `version`.

- **Endpoint**: `POST /users/me/appointment` or `PUT /users/me/appointment`
- **Request Body**:
```json
{
  "appointment_date": "2026-08-20",
  "reminder_lead_days": 2,
  "anc_contact_number": 2,
  "anc_contact_title": "2nd ANC Contact (20 Weeks)"
}
```

### Delete ANC Appointment
- **Endpoint**: `DELETE /users/me/appointment`
- **Response** `(200 OK)`: `{"status": "deleted"}`

### WHO 8-Contact ANC Schedule & Timeline
Returns the complete WHO 8-contact antenatal schedule calculated directly from the mother's gestational age / LNMP:
- **Endpoint**: `GET /users/me/anc-schedule`
- **Response** `(200 OK)`:
```json
{
  "current_gestational_age_weeks": 16,
  "current_gestational_age_days": 4,
  "effective_lnmp_date": "2026-05-01",
  "estimated_due_date": "2027-02-05",
  "next_anc_contact": {
    "contact_number": 2,
    "trimester": "second_trimester",
    "trimester_en": "Second Trimester",
    "trimester_am": "2ኛ ትሪሚስተር",
    "gestational_weeks": 20,
    "gestational_label_en": "20 weeks",
    "gestational_label_am": "20 ሳምንት",
    "schedule_next_weeks": 6,
    "title_en": "2nd ANC Contact (20 Weeks)",
    "title_am": "2ኛ የቅድመ ወሊድ ክትትል (20 ሳምንት)",
    "target_date": "2026-09-18",
    "current_gestational_weeks": 16
  },
  "all_contacts": [
    {
      "contact_number": 1,
      "trimester": "first_trimester",
      "gestational_weeks": 12,
      "title_en": "1st ANC Contact (Up to 12 Weeks)",
      "title_am": "1ኛ የቅድመ ወሊድ ክትትል (እስከ 12 ሳምንት)",
      "target_date": "2026-07-24",
      "schedule_next_weeks": 8
    },
    {
      "contact_number": 2,
      "trimester": "second_trimester",
      "gestational_weeks": 20,
      "title_en": "2nd ANC Contact (20 Weeks)",
      "title_am": "2ኛ የቅድመ ወሊድ ክትትል (20 ሳምንት)",
      "target_date": "2026-09-18",
      "schedule_next_weeks": 6
    },
    {
      "contact_number": 3,
      "trimester": "second_trimester",
      "gestational_weeks": 26,
      "title_en": "3rd ANC Contact (26 Weeks)",
      "title_am": "3ኛ የቅድመ ወሊድ ክትትል (26 ሳምንት)",
      "target_date": "2026-10-30",
      "schedule_next_weeks": 4
    },
    {
      "contact_number": 4,
      "trimester": "third_trimester",
      "gestational_weeks": 30,
      "title_en": "4th ANC Contact (30 Weeks)",
      "title_am": "4ኛ የቅድመ ወሊድ ክትትል (30 ሳምንት)",
      "target_date": "2026-11-27",
      "schedule_next_weeks": 4
    },
    {
      "contact_number": 5,
      "trimester": "third_trimester",
      "gestational_weeks": 34,
      "title_en": "5th ANC Contact (34 Weeks)",
      "title_am": "5ኛ የቅድመ ወሊድ ክትትል (34 ሳምንት)",
      "target_date": "2026-12-25",
      "schedule_next_weeks": 2
    },
    {
      "contact_number": 6,
      "trimester": "third_trimester",
      "gestational_weeks": 36,
      "title_en": "6th ANC Contact (36 Weeks)",
      "title_am": "6ኛ የቅድመ ወሊድ ክትትል (36 ሳምንት)",
      "target_date": "2027-01-08",
      "schedule_next_weeks": 2
    },
    {
      "contact_number": 7,
      "trimester": "third_trimester",
      "gestational_weeks": 38,
      "title_en": "7th ANC Contact (38 Weeks)",
      "title_am": "7ኛ የቅድመ ወሊድ ክትትል (38 ሳምንት)",
      "target_date": "2027-01-22",
      "schedule_next_weeks": 2
    },
    {
      "contact_number": 8,
      "trimester": "third_trimester",
      "gestational_weeks": 40,
      "title_en": "8th ANC Contact (40 Weeks - Delivery)",
      "title_am": "8ኛ የቅድመ ወሊድ ክትትል (40 ሳምንት - የመውለጃ ጊዜ)",
      "target_date": "2027-02-05",
      "schedule_next_weeks": null
    }
  ]
}
```

---

## 3. Voice Check-in Intake Workflow

The session runs `symptoms` → `food` → `supplement` → `closing`, with food or
supplement stages omitted when confirmed observations already cover that local day.
All local days use `Africa/Addis_Ababa`; persisted instants use UTC.

Every check-in POST requires `Idempotency-Key` (8–128 characters from
`A-Z a-z 0-9 _ . : -`). Generate a new key for each logical mutation, retain it
across network retries, and resend the exact same payload. Reusing a key for a
different payload returns `409`. Start accepts no body and returns version `0`.

Every subsequent session mutation also requires `X-Session-Version` containing
the most recent version returned by the server. Successful mutations increment
it. A stale version returns `409`; load `GET /checkin/{session_id}/state` before
retrying with a new key. A committed retry returns its original result, which can
have an older version than current state; reload state after reconnecting.

| Operation | Request | Response/state |
|---|---|---|
| `POST /checkin/start` | Retry key | `session_id`, `version`, `stage`, `stage_status`, prompt/audio URL |
| `POST /checkin/{id}/respond` | Version, retry key; multipart `audio` | Transcript and every extracted `pending_items`; no confirmation yet |
| `POST /checkin/{id}/items/{item_id}/voice-correct` | Version, retry key; multipart `audio` | Exactly one corrected pending item; requires confirmation again |
| `POST /checkin/{id}/verify` | Version, retry key; JSON `items` operations below | Pending list, confirmed count, version, immediate `danger_sign_triggered` |
| `POST /checkin/{id}/complete` | Version, retry key; `{}` | Next stage, or one durable terminal result and `check_in_id` |
| `GET /checkin/{id}/state` | Authentication | Current stage/status/version, pending items, draft, completed stages, expiry, terminal result |

Stage status is `awaiting_response`, `awaiting_confirmation`, `ready`, or
`completed`. An unanswered stage requires an explicit `{"skip":true}` completion.
Pending items must first be verified, corrected, or explicitly discarded. Skipped
and empty stages are not evidence that symptoms are absent. Provider failures
preserve the previous draft; offer retry or manual input.

Generic prompts: `GET /checkin/prompts` and
`GET /checkin/prompts/{stage}/audio`. Patient-specific read-backs use authenticated
`POST /tts`; `verification_audio_url` is null.

Phase 3 provider failures return **503** with `code: "provider_unavailable"`,
`draft_preserved: true`, `recovery: ["retry", "manual_input"]`, and `Retry-After`.
Resume the stored session, retain the retry key for the same audio/version, and
offer explicit manual correction/addition. Never interpret an outage as an empty
or reassuring clinical result. Provider work has a shared 45-second deadline.
Generic prompt URLs now contain a content version; missing assets require
operator provisioning and never trigger public synthesis.

## 4. Verification & Correction Flows

The only request shape is an `items` list (1–50 operations), including for one
item. Confirmation must be a JSON boolean. IDs, provenance, confirmation time,
policy/prompt/model versions, danger flags, and read-back phrases are server-owned.
Unknown IDs and fields return `422`; no single-item ID fallback exists.

```json
{
  "items": [
    {
      "action": "verify",
      "item_id": "2e166c60-7461-41fb-86d6-ff99c886c950",
      "confirmed": true,
      "corrected_value": {"duration": {"value": 2, "unit": "day"}}
    }
  ]
}
```

Omit `corrected_value` to confirm unchanged. Use `confirmed:false` to retain a
corrected item pending confirmation. Use `{"action":"discard","item_id":"..."}`
to explicitly remove a pending item. Manual addition is a separate action and
must omit `item_id`:

```json
{"items":[{"action":"add","confirmed":true,"corrected_value":{"raw_text":"እንጀራ በሽሮ"}}]}
```

Corrections are validated against the session stage:

| Stage | Editable fields |
|---|---|
| symptoms | `raw_text`, nullable recognized `category`, nullable `duration`, `severity` |
| food | `raw_text`, canonical `food_groups`, `items` |
| supplement | `raw_text`, `supplement_name`, `taken_today` (boolean or null for unknown) |
| closing | `raw_text`, recognized `topic` |

Severity is `mild`, `moderate`, `severe`, or `unspecified`. Duration has a finite
nonnegative numeric value and `minute`, `hour`, `day`, `week`, or `month`; unknown
is null or `{"value":null,"unit":"unspecified"}`. Text and collection limits are
published in OpenAPI. Each stage holds at most 100 confirmed and pending items.

Recognized danger categories are preserved even when severity is mild. Show the
warning immediately when verification returns `danger_sign_triggered:true`;
do not wait for food, supplement, or closing completion. An unknown classification
is not a reassuring assessment. Clinical review of the policy and wording remains
required before release.

Final completion atomically stores explicitly confirmed items, terminal session
state, and an outbox event. Repeated completion returns the original check-in.
Food and supplement collections retain every confirmed item. Unknown supplement
names are never silently replaced with the first configured supplement.

---

## 5. Check-in History & Details

### List User Check-in History
- **Endpoint**: `GET /checkin/history`
- Returns an owned array page, newest first (timestamp and ID break ties).
  `limit` defaults to 50 and accepts 1–100. Send the `X-Next-Cursor` response
  header as the next request's `cursor`; its absence means the final page.
  Keep the same endpoint and filters while continuing. Newer inserts appear
  on a fresh first-page request, not in an existing continuation.
  The same limit/cursor/header contract applies to `GET /notifications`,
  `GET /reminders`, and `GET /users/me/supplements`. Notifications are ordered
  by due time and ID, supplements by creation time and ID, both ascending.
  Responses remain arrays; clients must follow the header to retrieve all rows.
  `/users/me` embeds at most 50 pending reminders; use the paginated list for more.
- **Response** `(200 OK)`:
```json
[
  {
    "id": "f589c311-2090-482f-b441-11883c5112ab",
    "timestamp": "2026-08-15T12:00:00Z",
    "symptoms": [{"raw_text": "ቀላል የድካም ስሜት", "danger_sign": false, "confirmed": true}],
    "food_log": [{"raw_text": "እንጀራ በሽሮ", "confirmed": true}],
    "supplement_check": [{"supplement_name": "iron", "taken_today": true, "confirmed": true}],
    "closing_mentions": [],
    "danger_sign_triggered": false,
    "summary_text_am": "ቀላል የድካም ስሜት ምልክት ተመዝግቧል",
    "summary_text_en": "Reported symptom: mild fatigue. Classification is uncertain."
  }
]
```

### Get Single Check-in Detail
- **Endpoint**: `GET /checkin/history/{checkin_id}`
- **Response** `(200 OK)`: Returns full breakdown for that specific intake session.

---

## 6. Clinician Summaries & QR Sharing

Summaries aggregate all confirmed check-ins over the ANC window, formatted specifically for fast doctor skimming (distinct **Danger Signs** vs **Recorded General Symptoms** and **Nutritional Variation Share %**).

### Generate Manual Summary
- **Endpoint**: `POST /summary/generate`
- Requires `Idempotency-Key` and a JSON body: `{}` for the default window, or
  `{"period_start":"2026-09-01T00:00:00+03:00","period_end":"2026-09-18T00:00:00+03:00"}`.
  Both bounds must be timezone-aware, start < end, end no later than now, at most
  366 days. The window is start-inclusive and end-exclusive. Default start is
  the latest of account creation, 30 days ago, and the recorded previous attended
  appointment. Responses include exact `window_start`/`window_end`; date labels use
  the local calendar. An empty period remains empty; database failures return 503.
- Every included item has source/check-in references and confirmation provenance.
  Legacy missing confirmation is excluded; unknown legacy timestamps stay null.
  Missing or conflicting supplement-day observations are unknown, not missed doses.
  Percentages use only known observations; `by_supplement` provides separate counts.
- **Response** `(200 OK)`:
```json
{
  "id": "c138861d-91b4-4b51-bdf1-897711200119",
  "period_start": "2026-07-24",
  "period_end": "2026-09-18",
  "generated_at": "2026-09-17T13:00:00Z",
  "anc_contact_number": 2,
  "anc_contact_title": "2nd ANC Contact (20 Weeks)",
  "anc_contact_title_am": "2ኛ የቅድመ ወሊድ ክትትል (20 ሳምንት)",
  "target_gestational_weeks": 20,
  "content_json": {
    "anc_contact": {
      "contact_number": 2,
      "title_en": "2nd ANC Contact (20 Weeks)",
      "title_am": "2ኛ የቅድመ ወሊድ ክትትል (20 ሳምንት)",
      "target_gestational_weeks": 20,
      "trimester": "second_trimester",
      "schedule_next_weeks": 6
    },
    "danger_signs": [
      {
        "date": "2026-09-10",
        "category": "severe_headache",
        "category_display": "ከባድ ራስ ምታት",
        "category_display_en": "Severe headache",
        "raw_text": "ከባድ ራስ ምታት ለ 1 ቀን",
        "duration": {"value": 1, "unit": "day"},
        "severity": "severe"
      }
    ],
    "recorded_symptoms": [
      {
        "date": "2026-09-12",
        "category": null,
        "assessment": "unclassified",
        "category_display": "ቀላል የድካም ስሜት",
        "raw_text": "ቀላል የድካም ስሜት",
        "severity": "mild"
      }
    ],
    "food_logs": [
      {"date": "2026-09-12", "raw_text": "እንጀራ በሽሮ", "food_groups": ["grains", "proteins"]}
    ],
    "nutritional_variation": {
      "total_items_classified": 14,
      "tracked_days": 10,
      "percentages": {
        "grains": 40,
        "proteins": 30,
        "dairy": 10,
        "fruits_and_vegetables": 20
      }
    },
    "supplement_adherence": {
      "taken_days": 18,
      "tracked_days": 20,
      "total_days_in_period": 21,
      "percentage": 90
    },
    "closing_mentions": [],
    "muac_reminder": "MUAC screening due — check at visit",
    "provenance_note": "All data in this summary is self-reported by the patient (no device-measured data)."
  },
  "share_link_slug": null,
  "qr_code_url": null
}
```

### Check & Trigger Automatic Summary
- **Endpoint**: `POST /summary/check-automatic`
- **Rules**:
  - Generates when a scheduled appointment is today or tomorrow; repeated calls return the same snapshot for that appointment/date/contact. Attendance is unchanged.
  - If no scheduled appointment exists, checks the 30-day fallback; one automatic snapshot per calendar month. Background execution requires the separate scheduler and worker in `docs/phase3-resilience.md`.

### Get Latest Summary
- **Endpoint**: `GET /summary/latest`

### Consented summary sharing
Sharing defaults off pending privacy review. When enabled:

- `POST /summary/{summary_id}/shares` with `{"consent":true,"expires_in_hours":24}` returns **201** with share `id`, `expires_at`, `scope`, `share_url`, and private `qr_code_base64`.
- QR rendering failure returns `qr_status:"retry_required"` and null `qr_code_base64` alongside the usable URL. Retry `POST /summary/shares/{share_id}/qr` with `{"token":"<token from share_url>"}` and authentication to receive PNG bytes. This creates no new snapshot or share.
- Expiry is 24 hours by default, at most seven days. Keep the returned token in memory and show it only to the consenting patient; it cannot be retrieved later.
- `GET /summary/{token}` resolves the bearer link. It returns a structured allowlist, never the original `content_json` or raw patient text. This is sensitive health data, not anonymized data.
- `DELETE /summary/shares/{share_id}` revokes the owner's share. Expired, revoked and unknown tokens return 404.
- Set `no-store`, `no-referrer`, and `noindex` on the frontend share page. Remove analytics and redact proxy/CDN request paths and queries. Legacy links and public QR URLs are invalidated by migration 005.

---

## 7. Notifications & Reminders System

### Get Active Notifications
- **Endpoint**: `GET /notifications`
- **Response** `(200 OK)`:
```json
[
  {
    "id": "4b911200-7c22-411a-8800-9a8b77665511",
    "user_id": "e81acbf1-5f43-4afc-90be-b2d86c9a6802",
    "type": "supplement",
    "message": "Reminder to take your iron supplement.",
    "due_at": "2026-08-15T09:00:00Z",
    "dismissed": false,
    "created_at": "2026-08-15T09:00:00Z"
  },
  {
    "id": "9a112233-4455-6677-8899-aabbccddeeff",
    "user_id": "e81acbf1-5f43-4afc-90be-b2d86c9a6802",
    "type": "report_generated",
    "message": "Your clinician summary report for your ANC appointment has been generated.",
    "due_at": "2026-08-15T12:00:00Z",
    "dismissed": false,
    "created_at": "2026-08-15T12:00:00Z"
  }
]
```

### Dismiss Notification
- **Endpoint**: `POST /notifications/{notification_id}/dismiss`

### 1-Tap Google Calendar Link & iCal Export (.ics)
Add ANC appointment directly to Google Calendar or Apple Calendar with automated device reminders (1 day & 2 hours before):
- **Get Calendar Links**: `GET /users/me/appointment/calendar-link`
  - **Response** `(200 OK)`:
  ```json
  {
    "google_calendar_url": "https://calendar.google.com/calendar/render?action=TEMPLATE&text=...",
    "ical_download_url": "/users/me/appointment/calendar.ics"
  }
  ```
- **Download iCal File**: `GET /users/me/appointment/calendar.ics`
  - Returns downloadable `.ics` calendar file with built-in device notification alarms.

### Register Device Push Notification Tokens (FCM / Web Push)
Register device token for lockscreen push notifications when the app or browser is closed:
- **Endpoint**: `POST /users/me/push-tokens`
- **Request Body**:
```json
{
  "token": "fcm_device_token_or_web_push_subscription_string",
  "platform": "web"
}
```
- **Response** `(200 OK)`: `{"status": "registered", "token": "..."}`

---

## 8. Error Handling & Best Practices

| HTTP Status | Detail Example | Cause / Action |
|---|---|---|
| `401 Unauthorized` | `"Invalid or expired token"` | Access token missing or expired; redirect user to login. |
| `422 Unprocessable Entity` | `"Invalid mutation"` | Invalid fields/IDs or unresolved pending items; correct the request. |
| `404 Not Found` | `"Check-in record not found"` | Resource ID doesn't exist or belongs to another user. |
| `409 Conflict` | `"State changed or retry key conflicts; reload and retry"` | Reload current state. Retain keys for identical retries; use a new key for a new mutation. |

### Frontend UI Checklist
1. **Always display `verification_phrase`** returned by backend directly on screen.
2. **Audio File Formats**: Send `.webm` or `.wav` recorded at 16kHz for Addis AI ASR accuracy.
3. **Empty Stage Handling**: Confirm explicit negative statements like other observations. Skipping an unanswered stage requires `{"skip":true}` and must not display a reassuring assessment.

---

## 9. Text-to-Speech (TTS) Voice Synthesis

Generic `question_audio_url` values refer to pre-provisioned public prompt
assets. A missing generic asset does not trigger paid synthesis.
`verification_audio_url` is now `null`. To play a patient-specific verification
phrase, send authenticated `POST /tts` with `{"text":"...","voice_id":null}`,
then play the response blob. Revoke the local object URL after playback.
Never place health text in a URL. `GET /tts` returns **410**.

TTS accepts at most 2,000 characters. Uploads accept WAV, WebM, Ogg, MP4 audio,
and MP3 with matching MIME types; default limits are 6 MB and 120 seconds.
Oversized bodies/audio return **413**, unsupported or undecodable audio **415**,
and quota exhaustion **429** with `Retry-After`. Preserve drafts on errors.


## Privacy tools (migration 010)

The authenticated privacy routes are described in [privacy operations](docs/privacy-operations.md).
They return 503 while `ENABLE_PRIVACY_TOOLS` is false. Show the configured support
channel and accurately distinguish a deletion request from completed erasure.
Use `POST /users/me/privacy/requests` with `{"confirm":true}` and a stable
`Idempotency-Key`. The 202 response includes a request ID and `requested` status.
Cancellation uses `POST /users/me/privacy/requests/{id}/cancel`; current requests
are available in `GET /users/me/privacy/export/requests`.

For personal-data pages, get `/users/me/privacy/export`, then fetch each listed
section via `/users/me/privacy/export/{section}?limit=50`. Follow the response's
`next_cursor` as `after` until null. Pagination is per-page consistent; do not
claim the result is a point-in-time snapshot or includes external processor data.
Do not store these responses in a shared cache or log clinical contents.


## Care portal and offline check-ins

The [care and offline integration guide](docs/care-offline-mvp.md) specifies the new authenticated portal, patient consent, invitation, alert acknowledgement, and offline submission APIs. Both features default off. Portal users use their own login and require an active patient-approved relationship; never reuse a patient token for a clinician or trusted person.

Offline submissions use `POST /checkin/offline-sync` with a frozen payload and an `Idempotency-Key` equal to its `client_submission_id`. Receipt and observation times are separate. The existing voice sessions are not an offline queue. Implement the account-specific local queue and all recovery states in the patient frontend before claiming offline support to users. Portal clinical responses must never be service-worker cached.

Schemas and request examples are generated in [OpenAPI](docs/openapi.json) and the Postman **Care portal and offline check-ins** folder. The frontend implementation remains pending in its own repository.
