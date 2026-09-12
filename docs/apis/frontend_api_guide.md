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

### Forgot Password (Send Reset Email)
- **Endpoint**: `POST /auth/forgot-password`
- **Request Body**:
```json
{
  "email": "mother@example.com"
}
```
- **Response** `(200 OK)`:
```json
{
  "status": "success",
  "message": "If an account with that email exists, a password reset link has been sent to your email."
}
```

### Reset Password (Update Password with Recovery Token)
- **Endpoint**: `POST /auth/reset-password`
- **Request Body**:
```json
{
  "access_token": "recovery_access_token_from_email_link",
  "new_password": "newsecurepassword123"
}
```
- **Response** `(200 OK)`:
```json
{
  "status": "success",
  "message": "Password updated successfully. You can now log in with your new password."
}
```

> [!NOTE]
> The backend handles Supabase ES256 and HS256 JWT decoding seamlessly. Save the `access_token` securely on device storage.

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
- **Request Body**:
```json
{
  "appointment": {
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
Allows the patient to manually confirm supplement intake (e.g. from home screen checklist button). Logging supplement intake for today automatically dismisses pending reminders and **skips Stage 3 (Supplement)** during voice check-in!
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

### Step 0: Check-in Stage Prompts & Stored Voice Audio
Frontend can query all 4 standard check-in prompts or play the stored Amharic voice for each stage directly (zero dynamic TTS latency!):
- **Get All Stage Prompts**: `GET /checkin/prompts`
- **Stream Stored Audio for Stage**: `GET /checkin/prompts/{stage}/audio` (e.g. `/checkin/prompts/symptoms/audio`)

### Step 1: Start Session
- **Endpoint**: `POST /checkin/start`
- **Response** `(200 OK)`:
```json
{
  "session_id": "93b761d2-42ba-4270-9bb2-dffd19256ab1",
  "stage": "symptoms",
  "question_prompt": "ዛሬ ጽኑ ራስ ምታት፣ የዓይን ብዥታ፣ ደም መፍሰስ፣ ፈሳሽ መፍሰስ ወይም ከፍተኛ የሆድ ህመም ተሰምቶዎታል?",
  "question_audio_url": "/checkin/prompts/symptoms/audio"
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
- **Request Body (Single Item Verification)**:
```json
{
  "item_id": "2e166c60-7461-41fb-86d6-ff99c886c950",
  "confirmed": true,
  "corrected_value": {
    "raw_text": "ቀላል የድካም ስሜት ብቻ ነው"
  }
}
```

- **Request Body (Bulk Verification for All Items at Once)**:
```json
{
  "items": [
    {
      "item_id": "2e166c60-7461-41fb-86d6-ff99c886c950",
      "confirmed": true
    },
    {
      "item_id": "889bb790-ce6d-4008-8254-9435f3d8642c",
      "confirmed": true,
      "corrected_value": {
        "severity": "mild"
      }
    }
  ]
}
```
- **Response** `(200 OK)`:
```json
{
  "session_id": "93b761d2-42ba-4270-9bb2-dffd19256ab1",
  "stage": "symptoms",
  "pending_items": [],
  "confirmed_count": 2
}
```

> [!TIP]
> **Bulk Verification**: When multiple symptoms, foods, or closing questions are returned in `pending_items`, the frontend can present all items at once and confirm them all in a single bulk `POST /verify` call!
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
  "summary_text_am": "ምንም የአደጋ ምልክት አልተገኘም፣ ነገር ግን ቀላል የድካም ስሜት ምልክት ተመዝግቧል",
  "summary_text_en": "No danger signs detected, but mild fatigue symptom recorded.",
  "check_in_id": "f589c311-2090-482f-b441-11883c5112ab"
}
```

> [!NOTE]
> **Daily Check-in Summary Rules (in Amharic & English)**:
> - **Danger Signs Detected**: `"{x} የአደጋ ምልክት ተገኝቷል፣ በአስቸቋይ የህክምና እርዳታ ያግኙ"`
> - **Non-Danger Symptoms**: `"ምንም የአደጋ ምልክት አልተገኘም፣ ነገር ግን {x} ምልክት ተመዝግቧል"`
> - **No Symptoms Reported**: `"ምንም የአደጋ ምልክት አልተገኘም"`

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
    "danger_sign_triggered": false,
    "summary_text_am": "ምንም የአደጋ ምልክት አልተገኘም፣ ነገር ግን ቀላል የድካም ስሜት ምልክት ተመዝግቧል",
    "summary_text_en": "No danger signs detected, but mild fatigue symptom recorded."
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
        "category": "no_danger_sign_detected",
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
      "percentage": 86
    },
    "closing_mentions": [],
    "muac_reminder": "MUAC screening due — check at visit",
    "provenance_note": "All data in this summary is self-reported by the patient (no device-measured data)."
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
| `400 Bad Request` | `"All pending items must be verified before completing the stage"` | Patient hasn't verified `pending_items`; call `/verify` first. |
| `404 Not Found` | `"Check-in record not found"` | Resource ID doesn't exist or belongs to another user. |
| `409 Conflict` | `"Appointment already exists"` | Use `PUT /users/me/appointment` to update an existing appointment. |

### Frontend UI Checklist
1. **Always display `verification_phrase`** returned by backend directly on screen.
2. **Audio File Formats**: Send `.webm` or `.wav` recorded at 16kHz for Addis AI ASR accuracy.
3. **Empty Stage Handling**: When user says "No / nothing", `pending_items` is `[]`. Directly call `/complete` to move forward.

---

## 9. Text-to-Speech (TTS) Voice Synthesis

The backend includes native **Text-to-Speech (TTS)** via Addis AI so the AI can speak stage prompts and read-back verification phrases in Amharic voice.

### 1. Automatic Audio URLs in Check-in Responses
All check-in endpoints automatically attach `question_audio_url` and `verification_audio_url`:

- **Start / Advance Stage Response**:
```json
{
  "session_id": "93b761d2-42ba-4270-9bb2-dffd19256ab1",
  "stage": "symptoms",
  "question_prompt": "ዛሬ ወይም በቅርቡ ምንም አይነት ያልተለመደ የጤና እክል ወይም ህመም ተሰምቶዎታል?",
  "question_audio_url": "/tts?text=%E1%8B%AE%E1%88%A5..."
}
```

- **Respond / Verify Pending Items Response**:
```json
{
  "item_id": "2e166c60-7461-41fb-86d6-ff99c886c950",
  "raw_text": "ቀላል የድካም ስሜት",
  "verification_phrase": "ቀላል የድካም ስሜት — ትክክል ነው?",
  "verification_audio_url": "/tts?text=%E1%88%A8%E1%8B%AE..."
}
```

### 2. Direct TTS Endpoints
- **Stream Audio via GET (HTML `<audio src="...">` / Mobile Audio Player)**:  
  `GET /tts?text=ከፍተኛ+ትኩሳት+—+ትክክል+ነው%3F` -> Returns `audio/mpeg` MP3 stream.
- **Synthesize Audio via POST**:  
  `POST /tts`  
  `{"text": "ከፍተኛ ትኩሳት — ትክክል ነው?"}` -> Returns `audio/mpeg` MP3 stream.
