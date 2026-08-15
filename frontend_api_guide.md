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

All endpoints (except `/auth/*` and `/summary/public/*`) require a Bearer Access Token in the HTTP Request Header:

```http
Authorization: Bearer <access_token>
```

### Sign Up
- **Endpoint**: `POST /auth/signup`
- **Request Body**:
```json
{
  "email": "mother@example.com",
  "password": "securepassword123"
}
```
- **Response** `(200 OK)`:
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user_id": "e81acbf1-5f43-4afc-90be-b2d86c9a6802",
  "email": "mother@example.com"
}
```

### Log In
- **Endpoint**: `POST /auth/login`
- **Request Body**:
```json
{
  "email": "mother@example.com",
  "password": "securepassword123"
}
```
- **Response** `(200 OK)`: Returns `access_token`, `user_id`, and `email`.

> [!NOTE]
> The backend handles Supabase ES256 and HS256 JWT decoding seamlessly. Save the `access_token` securely on device storage.

---

## 2. User Settings & Profile Management

Frontend apps can query `GET /users/me` at launch to load all user configuration states (supplements, appointment date, reminder lead days, active notifications).

### Get Full User Profile & Settings
- **Endpoint**: `GET /users/me`
- **Response** `(200 OK)`:
```json
{
  "id": "e81acbf1-5f43-4afc-90be-b2d86c9a6802",
  "email": "mother@example.com",
  "created_at": "2026-08-15T10:00:00Z",
  "supplements": [
    {
      "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
      "user_id": "e81acbf1-5f43-4afc-90be-b2d86c9a6802",
      "name": "iron",
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

### Add Supplement
- **Endpoint**: `POST /users/me/supplements`
- **Request Body**:
```json
{
  "name": "iron",
  "active": true,
  "reminder_enabled": true,
  "reminder_time": "09:00:00"
}
```

### Update Supplement
- **Endpoint**: `PUT /users/me/supplements/{supplement_id}`
- **Request Body**:
```json
{
  "active": false
}
```

### Set ANC Appointment
- **Endpoint**: `POST /users/me/appointment`
- **Request Body**:
```json
{
  "appointment_date": "2026-08-20",
  "reminder_lead_days": 2
}
```

### Update ANC Appointment
- **Endpoint**: `PUT /users/me/appointment`
- **Request Body**:
```json
{
  "appointment_date": "2026-08-25"
}
```

---

## 3. Voice Check-in Intake Workflow

The intake session is a multi-stage conversational state machine:
`symptoms` → `food` → `supplement` (if active supplement exists) → `closing`.

```mermaid
graph TD
    Start[POST /checkin/start] --> Stage1[Stage: symptoms]
    Stage1 --> Voice1[POST /checkin/{id}/respond audio]
    Voice1 --> Verify1[POST /checkin/{id}/verify]
    Verify1 --> Complete1[POST /checkin/{id}/complete]
    Complete1 --> Stage2[Stage: food]
    Stage2 --> Voice2[POST /checkin/{id}/respond audio]
    Voice2 --> Verify2[POST /checkin/{id}/verify]
    Verify2 --> Complete2[POST /checkin/{id}/complete]
    Complete2 --> Stage3{Supplement Active?}
    Stage3 -- Yes --> Stage3Supp[Stage: supplement]
    Stage3Supp --> Complete3[POST /checkin/{id}/complete]
    Stage3 -- No --> Stage4[Stage: closing]
    Complete3 --> Stage4
    Stage4 --> Finish[Intake Complete status: completed]
```

### Step 1: Start Session
- **Endpoint**: `POST /checkin/start`
- **Response** `(200 OK)`:
```json
{
  "session_id": "93b761d2-42ba-4270-9bb2-dffd19256ab1",
  "stage": "symptoms",
  "question_prompt": "ዛሬ ወይም በቅርቡ ምንም አይነት ያልተለመደ የጤና እክል ወይም ህመም ተሰምቶዎታል?"
}
```

### Step 2: Send Voice Response (Audio Upload)
- **Endpoint**: `POST /checkin/{session_id}/respond`
- **Content-Type**: `multipart/form-data`
- **Form Field**: `audio` (file upload: `.webm`, `.wav`, `.m4a`, `.mp3`)
- **Response** `(200 OK)`:
```json
{
  "session_id": "93b761d2-42ba-4270-9bb2-dffd19256ab1",
  "stage": "symptoms",
  "transcript": "ቀላል የድካም ስሜት አለኝ",
  "pending_items": [
    {
      "item_id": "2e166c60-7461-41fb-86d6-ff99c886c950",
      "raw_text": "ቀላል የድካም ስሜት አለኝ",
      "category": null,
      "duration": {"value": null, "unit": "unspecified"},
      "severity": "mild",
      "danger_sign": false,
      "confirmed": false,
      "verification_phrase": "ቀላል የድካም ስሜት አለኝ — ትክክል ነው?"
    }
  ]
}
```

> [!IMPORTANT]
> **Danger Signs Rule**: If `severity` is `"mild"`, `category` is automatically set to `null` and `danger_sign` is `false`. Danger signs are strictly reserved for severe/persistent protocol conditions.

---

## 4. Verification & Correction Flows

Each stage presents `pending_items` for patient read-back confirmation.

### A. Manual Text Verification & Edits
When the patient confirms or manually edits an item:

- **Endpoint**: `POST /checkin/{session_id}/verify`
- **Request Body**:
```json
{
  "item_id": "2e166c60-7461-41fb-86d6-ff99c886c950",
  "confirmed": true,
  "corrected_value": {
    "raw_text": "ቀላል የድካም ስሜት ብቻ ነው"
  }
}
```
- **Response** `(200 OK)`:
```json
{
  "session_id": "93b761d2-42ba-4270-9bb2-dffd19256ab1",
  "stage": "symptoms",
  "pending_items": [],
  "confirmed_count": 1
}
```

> [!TIP]
> **Single-Item Fallback**: On single-item stages (`food`, `supplement`), if the client accidentally sends the `session_id` in `item_id`, the backend automatically targets the single pending item.

### B. Single-Item Voice Correction
If the patient taps "Re-record voice for this item":

- **Endpoint**: `POST /checkin/{session_id}/items/{item_id}/voice-correct`
- **Content-Type**: `multipart/form-data`
- **Form Field**: `audio` (file upload)
- **Response** `(200 OK)`:
```json
{
  "session_id": "93b761d2-42ba-4270-9bb2-dffd19256ab1",
  "stage": "symptoms",
  "correction_transcript": "ከባድ ራስ ምታት ለሁለት ቀን",
  "item_updated": true,
  "pending_items": [
    {
      "item_id": "2e166c60-7461-41fb-86d6-ff99c886c950",
      "raw_text": "ከባድ ራስ ምታት ለሁለት ቀን",
      "category": "severe_headache",
      "duration": {"value": 2, "unit": "day"},
      "severity": "severe",
      "danger_sign": true,
      "confirmed": false,
      "verification_phrase": "ከባድ ራስ ምታት፣ 2 ቀን — ትክክል ነው?"
    }
  ]
}
```

### C. Complete Stage & Advance
Once all pending items in a stage are verified (or if `pending_items` is `[]` because "Nothing" was reported):

- **Endpoint**: `POST /checkin/{session_id}/complete`
- **Response (Intermediate Stage)** `(200 OK)`:
```json
{
  "session_id": "93b761d2-42ba-4270-9bb2-dffd19256ab1",
  "stage_completed": "symptoms",
  "next_stage": "food",
  "question_prompt": "ዛሬ ምን አይነት ምግቦች ተመገቡ?",
  "session_completed": false,
  "danger_sign_triggered": false
}
```

- **Response (Final Stage Completed)** `(200 OK)`:
```json
{
  "session_id": "93b761d2-42ba-4270-9bb2-dffd19256ab1",
  "stage_completed": "closing",
  "next_stage": null,
  "question_prompt": null,
  "session_completed": true,
  "danger_sign_triggered": false,
  "check_in_id": "f589c311-2090-482f-b441-11883c5112ab"
}
```

---

## 5. Check-in History & Details

### List User Check-in History
- **Endpoint**: `GET /checkin/history`
- **Response** `(200 OK)`:
```json
[
  {
    "id": "f589c311-2090-482f-b441-11883c5112ab",
    "timestamp": "2026-08-15T12:00:00Z",
    "symptoms": [{"raw_text": "ቀላል የድካም ስሜት", "danger_sign": false, "confirmed": true}],
    "food_log": {"raw_text": "እንጀራ በሽሮ", "confirmed": true},
    "supplement_check": {"supplement_name": "iron", "taken_today": true, "confirmed": true},
    "closing_mentions": [],
    "danger_sign_triggered": false
  }
]
```

### Get Single Check-in Detail
- **Endpoint**: `GET /checkin/history/{checkin_id}`
- **Response** `(200 OK)`: Returns full breakdown for that specific intake session.

---

## 6. Clinician Summaries & QR Sharing

Summaries aggregate all confirmed check-ins over a period for ANC doctor visits.

### Generate Manual Summary
- **Endpoint**: `POST /summary/generate`
- **Response** `(200 OK)`:
```json
{
  "id": "c138861d-91b4-4b51-bdf1-897711200119",
  "period_start": "2026-08-01",
  "period_end": "2026-08-15",
  "generated_at": "2026-08-15T13:00:00Z",
  "content_json": {
    "danger_signs": [],
    "symptoms_summary": [...],
    "food_logs": [{"raw_text": "እንጀራ በሽሮ"}],
    "supplement_adherence": {"taken_days": 5, "total_reported": 6, "percentage": 83.3},
    "patient_questions": []
  },
  "share_link_slug": "ab89ef12",
  "qr_code_url": "https://.../qr/ab89ef12.png"
}
```

### Check & Trigger Automatic Summary
- **Endpoint**: `POST /summary/check-automatic`
- **Rules**:
  - Automatically generates **1 day before appointment date**.
  - If no appointment is set, automatically generates **every 30 days**.

### Get Latest Summary
- **Endpoint**: `GET /summary/latest`

### Public Doctor View (No Auth Required)
- **Endpoint**: `GET /summary/public/{share_link_slug}`
- Returns de-identified summary for clinical review.

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

---

## 8. Error Handling & Best Practices

| HTTP Status | Detail Example | Cause / Action |
|---|---|---|
| `401 Unauthorized` | `"Invalid or expired token"` | Access token missing or expired; redirect user to login. |
| `400 Bad Request` | `"All pending items must be verified before completing the stage"` | Patient hasn't verified `pending_items`; call `/verify` first. |
| `404 Not Found` | `"Check-in record not found"` | Resource ID doesn't exist or belongs to another user. |
| `409 Conflict` | `"Appointment already exists"` | Use `PUT /users/me/appointment` to update an existing appointment. |

### Frontend UI Checklist
1. **Always display `verification_phrase`** returned by backend directly on screen.
2. **Audio File Formats**: Send `.webm` or `.wav` recorded at 16kHz for Addis AI ASR accuracy.
3. **Empty Stage Handling**: When user says "No / nothing", `pending_items` is `[]`. Directly call `/complete` to move forward.
