import json
import sys
from pathlib import Path

collection = {
    "info": {
        "_postman_id": "e9b2b4a6-enat-4444-8888-abcdef123456",
        "name": "EnatAI - Maternal Health Clinical Backend API",
        "description": "Comprehensive Postman API Collection for EnatAI Maternal Health Platform.\n\nIncludes Authentication, Maternal Onboarding, Gestational Calculator, WHO 8-Contact ANC Schedule, Voice & Text Check-in, Ethiopian Nutrition & Food Group Classification, Supplements, Appointments, Clinician Summaries & QR Sharing, Notifications, and Text-to-Speech (TTS).",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "variable": [
        {"key": "baseUrl", "value": "http://localhost:8000", "type": "string"},
        {"key": "token", "value": "", "type": "string"},
        {"key": "session_id", "value": "", "type": "string"},
        {"key": "item_id", "value": "", "type": "string"},
        {"key": "supplement_id", "value": "", "type": "string"},
        {"key": "notification_id", "value": "", "type": "string"},
        {"key": "share_link_slug", "value": "", "type": "string"},
        {"key": "checkin_id", "value": "", "type": "string"},
    ],
    "item": [
        {
            "name": "01. Health & System",
            "item": [
                {
                    "name": "Health Check",
                    "request": {
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/health",
                            "host": ["{{baseUrl}}"],
                            "path": ["health"],
                        },
                        "description": "Returns operational status of the FastAPI backend.",
                    },
                }
            ],
        },
        {
            "name": "02. Authentication",
            "item": [
                {
                    "name": "Register / Signup",
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "var jsonData = pm.response.json();",
                                    "if (jsonData.access_token) {",
                                    "    pm.collectionVariables.set('token', jsonData.access_token);",
                                    "}",
                                ],
                                "type": "text/javascript",
                            },
                        }
                    ],
                    "request": {
                        "auth": {"type": "noauth"},
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "email": "mother@example.com",
                                    "password": "StrongPassword123!",
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/auth/signup",
                            "host": ["{{baseUrl}}"],
                            "path": ["auth", "signup"],
                        },
                        "description": "Registers a new mother account with Supabase Auth and seeds user in PostgreSQL users table.",
                    },
                },
                {
                    "name": "Login",
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "var jsonData = pm.response.json();",
                                    "if (jsonData.access_token) {",
                                    "    pm.collectionVariables.set('token', jsonData.access_token);",
                                    "}",
                                ],
                                "type": "text/javascript",
                            },
                        }
                    ],
                    "request": {
                        "auth": {"type": "noauth"},
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "email": "mother@example.com",
                                    "password": "StrongPassword123!",
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/auth/login",
                            "host": ["{{baseUrl}}"],
                            "path": ["auth", "login"],
                        },
                        "description": "Authenticates user and returns JWT bearer access token.",
                    },
                },
                {
                    "name": "Forgot Password",
                    "request": {
                        "auth": {"type": "noauth"},
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {"email": "mother@example.com"}, indent=2
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/auth/forgot-password",
                            "host": ["{{baseUrl}}"],
                            "path": ["auth", "forgot-password"],
                        },
                        "description": "Sends password reset email link.",
                    },
                },
                {
                    "name": "Reset Password",
                    "request": {
                        "auth": {"type": "noauth"},
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "token_hash": "RECOVERY_TOKEN_HASH_FROM_EMAIL",
                                    "new_password": "NewStrongPassword123!",
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/auth/reset-password",
                            "host": ["{{baseUrl}}"],
                            "path": ["auth", "reset-password"],
                        },
                        "description": "Updates password with recovery token.",
                    },
                },
            ],
        },
        {
            "name": "03. Maternal Intake & Gestational Engine",
            "item": [
                {
                    "name": "Calculate Gestational Age (Instant Preview Calculator)",
                    "request": {
                        "auth": {"type": "noauth"},
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "method": "lnmp",
                                    "lnmp_date": "2026-05-15",
                                    "ultrasound_date": None,
                                    "ultrasound_gestational_weeks": None,
                                    "ultrasound_gestational_days": None,
                                    "calculation_date": None,
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/calculate-gestational-age",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "calculate-gestational-age"],
                        },
                        "description": "Instant public preview calculator without needing authentication. Computes gestational age in weeks & days, trimester, and EDD.",
                    },
                },
                {
                    "name": "Submit Onboarding (23 Maternal Questions)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "age": 26,
                                    "area": "urban",
                                    "pregnancy_counting_method": "lnmp",
                                    "lnmp_date": "2026-05-15",
                                    "ultrasound_date": None,
                                    "ultrasound_gestational_weeks": None,
                                    "ultrasound_gestational_days": None,
                                    "user_gestational_weeks": 14,
                                    "user_gestational_days": 3,
                                    "total_pregnancies": 2,
                                    "live_births": 1,
                                    "had_c_section": False,
                                    "child_passed_away": False,
                                    "past_pregnancy_complications": [
                                        "preterm_birth",
                                        "prom",
                                    ],
                                    "known_medical_conditions": [
                                        "hypertension",
                                        "other",
                                    ],
                                    "custom_medical_condition": "Mild seasonal asthma",
                                    "malaria_endemic_area": True,
                                    "current_medications": "Methyldopa 250mg",
                                    "supplements": ["iron & folic acid", "calcium"],
                                    "hospital": "St. Paul's Hospital Millennium Medical College",
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/onboarding",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "onboarding"],
                        },
                        "description": "Saves maternal clinical intake, seeds supplements table, and auto-schedules immediate next WHO ANC contact appointment.",
                    },
                },
                {
                    "name": "Get User Profile (Live Pregnancy Progress & Metrics)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/users/me",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me"],
                        },
                        "description": "Returns full user profile, live gestational progression (advancing automatically every day), supplements, active appointment, and notifications.",
                    },
                },
                {
                    "name": "Update Profile (Full Maternal Update)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "PUT",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "age": 27,
                                    "area": "urban",
                                    "pregnancy_counting_method": "lnmp",
                                    "lnmp_date": "2026-05-15",
                                    "user_gestational_weeks": 14,
                                    "user_gestational_days": 3,
                                    "hospital": "Tikur Anbessa Specialized Hospital (TASH)",
                                    "malaria_endemic_area": False,
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/profile",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "profile"],
                        },
                        "description": "Updates maternal details and recalculates gestational metrics.",
                    },
                },
                {
                    "name": "Patch Profile (Partial Update)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "PATCH",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "current_medications": "Methyldopa 250mg morning only"
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/profile",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "profile"],
                        },
                        "description": "Partially updates user profile fields.",
                    },
                },
                {
                    "name": "Update Preferred Hospital",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "PUT",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "hospital": "Tikur Anbessa Specialized Hospital (TASH)"
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/hospital",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "hospital"],
                        },
                        "description": "Dedicated endpoint to update the patient's delivery / ANC hospital.",
                    },
                },
                {
                    "name": "Update Settings (Unified Settings Update)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "PUT",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "hospital": "Gandhi Memorial Hospital",
                                    "language_preference": "am",
                                    "appointment_date": "2026-09-18",
                                    "reminder_lead_days": 2,
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/settings",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "settings"],
                        },
                        "description": "Unified settings endpoint to update language, hospital, appointment, and reminders in one call.",
                    },
                },
                {
                    "name": "Get WHO 8-Contact ANC Schedule & Timeline",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/users/me/anc-schedule",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "anc-schedule"],
                        },
                        "description": "Returns complete WHO 8-contact antenatal schedule calculated directly from gestational age, with target dates, trimesters, and immediate upcoming contact.",
                    },
                },
            ],
        },
        {
            "name": "04. Supplements Management",
            "item": [
                {
                    "name": "List User Supplements",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/users/me/supplements",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "supplements"],
                        },
                        "description": "Returns list of all active/inactive supplements for the mother.",
                    },
                },
                {
                    "name": "Create Supplement",
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "var jsonData = pm.response.json();",
                                    "if (jsonData.id) {",
                                    "    pm.collectionVariables.set('supplement_id', jsonData.id);",
                                    "    console.log('Saved supplement_id:', jsonData.id);",
                                    "}",
                                ],
                                "type": "text/javascript",
                            },
                        }
                    ],
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "name": "iron & folic acid",
                                    "dosage": "60mg elemental iron / 400µg folic acid",
                                    "frequency": "daily",
                                    "reminder_time": "08:00:00",
                                    "active": True,
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/supplements",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "supplements"],
                        },
                        "description": "Adds a new prescribed supplement.",
                    },
                },
                {
                    "name": "Update Supplement",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "PUT",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "name": "iron & folic acid",
                                    "dosage": "60mg / 400µg",
                                    "reminder_time": "09:00:00",
                                    "active": True,
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/supplements/{{supplement_id}}",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "supplements", "{{supplement_id}}"],
                        },
                        "description": "Updates an existing supplement.",
                    },
                },
                {
                    "name": "Verify Supplement Intake Today (Auto-skips Stage 3 in Voice Check-in)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "supplement_name": "iron & folic acid",
                                    "taken_today": True,
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/supplements/verify",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "supplements", "verify"],
                        },
                        "description": "Manual 1-tap UI toggle for taking daily supplement. Logging this today automatically skips Stage 3 (Supplements) during voice check-in!",
                    },
                },
                {
                    "name": "Delete Supplement",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "DELETE",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/users/me/supplements/{{supplement_id}}",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "supplements", "{{supplement_id}}"],
                        },
                        "description": "Deletes a supplement.",
                    },
                },
            ],
        },
        {
            "name": "05. Food Logging (Ethiopian 4-Food-Group Checkbox)",
            "item": [
                {
                    "name": "Manual 4-Food-Group Logging (Auto-skips Stage 2 in Voice Check-in)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "food_groups": [
                                        "grains",
                                        "proteins",
                                        "fruits_and_vegetables",
                                    ],
                                    "raw_text": "እንጀራ፣ ሽሮ እና ሰላጣ",
                                    "items": ["እንጀራ", "ሽሮ", "ሰላጣ"],
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/food/verify",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "food", "verify"],
                        },
                        "description": "Allows patient to select food groups eaten today directly from a 4-group checkbox UI ('grains', 'proteins', 'dairy', 'fruits_and_vegetables'). Automatically skips Stage 2 (Food) during daily voice check-in!",
                    },
                },
                {
                    "name": "Manual Food Log Alias",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "food_groups": ["grains", "dairy"],
                                    "raw_text": "ገንፎ በቅቤ እና እርጎ",
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/food-log",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "food-log"],
                        },
                        "description": "Alias endpoint for manual food group logging.",
                    },
                },
            ],
        },
        {
            "name": "06. Appointments & Calendar Integration",
            "item": [
                {
                    "name": "Set or Update ANC Appointment",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "appointment_date": "2026-09-18",
                                    "reminder_lead_days": 2,
                                    "anc_contact_number": 2,
                                    "anc_contact_title": "2nd ANC Contact (20 Weeks)",
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/appointment",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "appointment"],
                        },
                        "description": "Sets or edits ANC appointment date and reminder lead time.",
                    },
                },
                {
                    "name": "Get 1-Tap Google Calendar Link & iCal Export Link",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/users/me/appointment/calendar-link",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "appointment", "calendar-link"],
                        },
                        "description": "Generates 1-tap web URL to add ANC appointment to Google Calendar with device reminders, plus iCal download link.",
                    },
                },
                {
                    "name": "Download Apple/Outlook Calendar File (.ics)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/users/me/appointment/calendar.ics",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "appointment", "calendar.ics"],
                        },
                        "description": "Directly downloads standard iCalendar .ics file.",
                    },
                },
                {
                    "name": "Delete Appointment",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "DELETE",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/users/me/appointment",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "appointment"],
                        },
                        "description": "Deletes the scheduled appointment.",
                    },
                },
            ],
        },
        {
            "name": "07. Push Notifications & Devices",
            "item": [
                {
                    "name": "Register Push Device Token",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "token": "fcm_or_web_push_device_token_xyz",
                                    "platform": "web",
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/users/me/push-tokens",
                            "host": ["{{baseUrl}}"],
                            "path": ["users", "me", "push-tokens"],
                        },
                        "description": "Registers device push token for appointment and supplement alerts.",
                    },
                }
            ],
        },
        {
            "name": "08. Voice Check-in Intake Workflow",
            "item": [
                {
                    "name": "0. List Check-in Prompts & Metadata",
                    "request": {
                        "auth": {"type": "noauth"},
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/checkin/prompts",
                            "host": ["{{baseUrl}}"],
                            "path": ["checkin", "prompts"],
                        },
                        "description": "Returns all 4 standard check-in questions, localized Amharic/English categories, and audio playback URLs.",
                    },
                },
                {
                    "name": "0. Stream Stored Prompt Audio (Zero Redundant TTS)",
                    "request": {
                        "auth": {"type": "noauth"},
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/checkin/prompts/symptoms/audio",
                            "host": ["{{baseUrl}}"],
                            "path": ["checkin", "prompts", "symptoms", "audio"],
                        },
                        "description": "Streams pre-cached Amharic speech audio (MP3) for the question prompt without calling dynamic TTS repeatedly.",
                    },
                },
                {
                    "name": "1. Start Check-in Session",
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "var jsonData = pm.response.json();",
                                    "if (jsonData.session_id) {",
                                    "    pm.collectionVariables.set('session_id', jsonData.session_id);",
                                    "    console.log('Saved session_id:', jsonData.session_id);",
                                    "}",
                                ],
                                "type": "text/javascript",
                            },
                        }
                    ],
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/checkin/start",
                            "host": ["{{baseUrl}}"],
                            "path": ["checkin", "start"],
                        },
                        "description": "Starts daily check-in session. Returns first stage ('symptoms') and audio streaming URL.",
                    },
                },
                {
                    "name": "2. Respond with Audio (Multipart Upload)",
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "var jsonData = pm.response.json();",
                                    "if (jsonData.pending_items && jsonData.pending_items.length > 0) {",
                                    "    pm.collectionVariables.set('item_id', jsonData.pending_items[0].item_id);",
                                    "    console.log('Saved item_id:', jsonData.pending_items[0].item_id);",
                                    "}",
                                ],
                                "type": "text/javascript",
                            },
                        }
                    ],
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [],
                        "body": {
                            "mode": "formdata",
                            "formdata": [
                                {
                                    "key": "audio",
                                    "type": "file",
                                    "description": "Audio recording (.webm, .wav, .m4a, .mp3)",
                                }
                            ],
                        },
                        "url": {
                            "raw": "{{baseUrl}}/checkin/{{session_id}}/respond",
                            "host": ["{{baseUrl}}"],
                            "path": ["checkin", "{{session_id}}", "respond"],
                        },
                        "description": "Uploads recorded Amharic voice. Transcribes via Addis AI STT and extracts structured items.",
                    },
                },
                {
                    "name": "3A. Verify Item (Single Item Confirmation or Edit)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "item_id": "{{item_id}}",
                                    "confirmed": True,
                                    "corrected_value": {
                                        "raw_text": "ቀላል የድካም ስሜት ብቻ ነው"
                                    },
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/checkin/{{session_id}}/verify",
                            "host": ["{{baseUrl}}"],
                            "path": ["checkin", "{{session_id}}", "verify"],
                        },
                        "description": "Confirms or corrects an extracted item.",
                    },
                },
                {
                    "name": "3B. Bulk Verify Items (All Items in Stage at Once)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "items": [
                                        {"item_id": "{{item_id}}", "confirmed": True}
                                    ]
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/checkin/{{session_id}}/verify",
                            "host": ["{{baseUrl}}"],
                            "path": ["checkin", "{{session_id}}", "verify"],
                        },
                        "description": "Bulk confirms all pending items in one call.",
                    },
                },
                {
                    "name": "3C. Voice Correction for Single Item",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [],
                        "body": {
                            "mode": "formdata",
                            "formdata": [
                                {
                                    "key": "audio",
                                    "type": "file",
                                    "description": "Re-recorded audio correction",
                                }
                            ],
                        },
                        "url": {
                            "raw": "{{baseUrl}}/checkin/{{session_id}}/items/{{item_id}}/voice-correct",
                            "host": ["{{baseUrl}}"],
                            "path": [
                                "checkin",
                                "{{session_id}}",
                                "items",
                                "{{item_id}}",
                                "voice-correct",
                            ],
                        },
                        "description": "Re-records voice for a specific pending item.",
                    },
                },
                {
                    "name": "4. Complete Stage & Advance / Finish Check-in",
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "var jsonData = pm.response.json();",
                                    "if (jsonData.check_in_id) {",
                                    "    pm.collectionVariables.set('checkin_id', jsonData.check_in_id);",
                                    "    console.log('Saved checkin_id:', jsonData.check_in_id);",
                                    "}",
                                ],
                                "type": "text/javascript",
                            },
                        }
                    ],
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/checkin/{{session_id}}/complete",
                            "host": ["{{baseUrl}}"],
                            "path": ["checkin", "{{session_id}}", "complete"],
                        },
                        "description": "Advances to next stage. When finishing final stage ('closing'), saves check-in and returns localized Amharic summary text.",
                    },
                },
                {
                    "name": "Get User Check-in History",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/checkin/history",
                            "host": ["{{baseUrl}}"],
                            "path": ["checkin", "history"],
                        },
                        "description": "Returns list of past check-ins with localized Amharic summaries and danger sign flags.",
                    },
                },
                {
                    "name": "Get Single Check-in Detail",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/checkin/history/{{checkin_id}}",
                            "host": ["{{baseUrl}}"],
                            "path": ["checkin", "history", "{{checkin_id}}"],
                        },
                        "description": "Returns full details of a specific check-in session.",
                    },
                },
            ],
        },
        {
            "name": "09. Clinician Summaries & Doctor Sharing",
            "item": [
                {
                    "name": "Generate Clinician Summary Report (Manual)",
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "var jsonData = pm.response.json();",
                                    "if (jsonData.share_link_slug) {",
                                    "    pm.collectionVariables.set('share_link_slug', jsonData.share_link_slug);",
                                    "    console.log('Saved share_link_slug:', jsonData.share_link_slug);",
                                    "}",
                                ],
                                "type": "text/javascript",
                            },
                        }
                    ],
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/summary/generate",
                            "host": ["{{baseUrl}}"],
                            "path": ["summary", "generate"],
                        },
                        "description": "Generates immutable clinical summary with 2-tier symptoms ('danger_signs' vs 'recorded_symptoms'), 100% nutritional group distribution, ANC contact tags, and QR code URL.",
                    },
                },
                {
                    "name": "Check & Trigger Automatic Pre-Appointment Summary",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/summary/check-automatic",
                            "host": ["{{baseUrl}}"],
                            "path": ["summary", "check-automatic"],
                        },
                        "description": "Checks if appointment is 1 day away. If so, generates a deduplicated report without changing appointment attendance or contact number.",
                    },
                },
                {
                    "name": "Get Latest Summary",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/summary/latest",
                            "host": ["{{baseUrl}}"],
                            "path": ["summary", "latest"],
                        },
                        "description": "Returns most recent clinician report.",
                    },
                },
                {
                    "name": "Public Doctor Summary View (No Auth Required)",
                    "request": {
                        "auth": {"type": "noauth"},
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/summary/{{share_link_slug}}",
                            "host": ["{{baseUrl}}"],
                            "path": ["summary", "{{share_link_slug}}"],
                        },
                        "description": "Public doctor view for scanning patient QR code. Returns de-identified summary with 2-tier symptoms and nutritional variation.",
                    },
                },
            ],
        },
        {
            "name": "10. Notifications & Reminders",
            "item": [
                {
                    "name": "Get Active Notifications",
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "var jsonData = pm.response.json();",
                                    "if (jsonData && jsonData.length > 0) {",
                                    "    pm.collectionVariables.set('notification_id', jsonData[0].id);",
                                    "    console.log('Saved notification_id:', jsonData[0].id);",
                                    "}",
                                ],
                                "type": "text/javascript",
                            },
                        }
                    ],
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/notifications",
                            "host": ["{{baseUrl}}"],
                            "path": ["notifications"],
                        },
                        "description": "Retrieves active notification alerts for supplements, appointments, and generated reports.",
                    },
                },
                {
                    "name": "Dismiss Notification",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/notifications/{{notification_id}}/dismiss",
                            "host": ["{{baseUrl}}"],
                            "path": ["notifications", "{{notification_id}}", "dismiss"],
                        },
                        "description": "Dismisses a notification banner.",
                    },
                },
                {
                    "name": "List Reminders",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/reminders",
                            "host": ["{{baseUrl}}"],
                            "path": ["reminders"],
                        },
                        "description": "Returns pending reminder items.",
                    },
                },
                {
                    "name": "Retired Daily Reminder Trigger (410 in development)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}/reminders/run-daily",
                            "host": ["{{baseUrl}}"],
                            "path": ["reminders", "run-daily"],
                        },
                        "description": "Returns 410 when development routes are enabled; absent otherwise. Operators use PROCESS_ROLE=worker python -m app.jobs scheduler.",
                    },
                },
            ],
        },
        {
            "name": "11. Text-to-Speech (TTS)",
            "item": [
                {
                    "name": "Synthesize Speech (POST JSON Payload)",
                    "request": {
                        "auth": {
                            "type": "bearer",
                            "bearer": [
                                {"key": "token", "value": "{{token}}", "type": "string"}
                            ],
                        },
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps(
                                {
                                    "text": "እንደምን አደሩ፣ ዛሬ ጤናዎ እንዴት ነው?",
                                    "voice_id": None,
                                },
                                indent=2,
                            ),
                        },
                        "url": {
                            "raw": "{{baseUrl}}/tts",
                            "host": ["{{baseUrl}}"],
                            "path": ["tts"],
                        },
                        "description": "Synthesizes Amharic text via authenticated POST. Provider outages return 503 with code=provider_unavailable, draft_preserved=true, recovery=[retry,manual_input], and Retry-After.",
                    },
                }
            ],
        },
    ],
}

# Phase 1 contracts: signup never creates a client session; sharing is explicit.
for group in collection["item"]:
    for item in group["item"]:
        request = item.get("request", {})
        path = request.get("url", {}).get("path", [])
        if path == ["auth", "signup"]:
            item.pop("event", None)
            request["description"] = (
                "Returns 202 verification_required. Confirm email before login."
            )
        if path == ["summary", "generate"]:
            request["description"] = (
                "Create an owner-only snapshot. Sharing and QR delivery require explicit share creation."
            )
        if path == ["summary", "{{share_link_slug}}"]:
            request["description"] = (
                "Resolve a consented, expiring bearer share. Raw patient text is omitted. Not anonymous data."
            )


def security_request(name, method, path, body=None, authenticated=True):
    request = {
        "method": method,
        "header": [],
        "url": {
            "raw": "{{baseUrl}}/" + path,
            "host": ["{{baseUrl}}"],
            "path": path.split("/"),
        },
        "auth": {
            "type": "bearer",
            "bearer": [{"key": "token", "value": "{{token}}", "type": "string"}],
        }
        if authenticated
        else {"type": "noauth"},
    }
    if body is not None:
        request["header"] = [{"key": "Content-Type", "value": "application/json"}]
        request["body"] = {"mode": "raw", "raw": json.dumps(body, indent=2)}
    return {"name": name, "request": request}


collection["item"].append(
    {
        "name": "12. Secure identity and sharing lifecycle",
        "item": [
            security_request(
                "Exchange Telegram launch data",
                "POST",
                "auth/telegram",
                {"init_data": "{{telegram_init_data}}"},
                False,
            ),
            security_request(
                "Refresh Supabase session",
                "POST",
                "auth/refresh",
                {"refresh_token": "{{refresh_token}}"},
                False,
            ),
            security_request("Logout", "POST", "auth/logout"),
            security_request(
                "Link second verified identity",
                "POST",
                "auth/link",
                {"access_token": "{{second_identity_token}}"},
            ),
            security_request(
                "Consent and create expiring summary share",
                "POST",
                "summary/{{summary_id}}/shares",
                {"consent": True, "expires_in_hours": 24},
            ),
            security_request(
                "Revoke summary share", "DELETE", "summary/shares/{{share_id}}"
            ),
            security_request(
                "Retry private QR artifact",
                "POST",
                "summary/shares/{{share_id}}/qr",
                {"token": "{{share_link_slug}}"},
            ),
        ],
    }
)
for key in (
    "telegram_init_data",
    "refresh_token",
    "second_identity_token",
    "summary_id",
    "share_id",
):
    collection["variable"].append({"key": key, "value": "", "type": "string"})

# Phase 2: versioned sessions, explicit additions, exact windows and attendance.
collection["variable"].extend(
    [
        {"key": "session_version", "value": "0", "type": "string"},
        {
            "key": "idempotency_key",
            "value": "replace-for-each-new-mutation",
            "type": "string",
        },
    ]
)
collection["item"].append(
    {
        "name": "13. Workflow integrity",
        "item": [
            security_request("Resume session", "GET", "checkin/{{session_id}}/state"),
            security_request(
                "Explicit manual item addition",
                "POST",
                "checkin/{{session_id}}/verify",
                {
                    "items": [
                        {
                            "action": "add",
                            "confirmed": True,
                            "corrected_value": {"raw_text": "Patient-entered text"},
                        }
                    ]
                },
            ),
            security_request(
                "Mark appointment completed",
                "POST",
                "users/me/appointment/transition",
                {"action": "completed", "version": 0},
            ),
            security_request(
                "Reschedule appointment",
                "POST",
                "users/me/appointment/transition",
                {
                    "action": "rescheduled",
                    "version": 1,
                    "appointment_date": "2026-11-01",
                },
            ),
        ],
    }
)
for group in collection["item"]:
    for item in group["item"]:
        request = item.get("request", {})
        path = request.get("url", {}).get("path", [])
        method = request.get("method")
        joined = "/".join(path)
        mutation = method in ("POST", "PUT") and (
            (path and path[0] == "checkin")
            or joined == "summary/generate"
            or joined
            in (
                "users/me/food/verify",
                "users/me/food-log",
                "users/me/appointment",
                "users/me/appointment/transition",
            )
            or (
                joined.startswith("users/me/supplements/") and joined.endswith("verify")
            )
        )
        if mutation:
            request.setdefault("header", []).append(
                {"key": "Idempotency-Key", "value": "{{idempotency_key}}"}
            )
            request["description"] = (
                request.get("description", "")
                + " Use a new key per logical mutation; retain the exact key and body for retries."
            )
        if path and path[0] == "checkin" and len(path) > 2 and method == "POST":
            request["header"].append(
                {"key": "X-Session-Version", "value": "{{session_version}}"}
            )
        if path and path[0] == "checkin" and (method == "POST" or path[-1] == "state"):
            item.setdefault("event", []).append(
                {
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": [
                            "if (pm.response.code === 200) { const state = pm.response.json(); if (Number.isInteger(state.version)) pm.collectionVariables.set('session_version', String(state.version)); }"
                        ],
                    },
                }
            )
        if joined == "checkin/{{session_id}}/verify":
            body = json.loads(request["body"]["raw"])
            if "items" not in body:
                body = {"items": [body]}
            request["body"]["raw"] = json.dumps(body, indent=2, ensure_ascii=False)
        if joined in ("checkin/{{session_id}}/complete", "summary/generate"):
            request["body"] = {"mode": "raw", "raw": "{}"}
            if not any(h["key"].lower() == "content-type" for h in request["header"]):
                request["header"].append(
                    {"key": "Content-Type", "value": "application/json"}
                )
        if joined == "summary/check-automatic":
            request["description"] = (
                "Generate one snapshot per due appointment/date/contact or monthly period; attendance and contact number remain unchanged."
            )
        if method == "GET" and joined in {
            "checkin/history",
            "notifications",
            "reminders",
            "users/me/supplements",
        }:
            request["url"]["raw"] += "?limit=50"
            request["url"]["query"] = [
                {"key": "limit", "value": "50"},
                {"key": "cursor", "value": "{{page_cursor}}", "disabled": True},
            ]
            request["description"] = (
                "Returns an owned array page (default 50, maximum 100). Send X-Next-Cursor as cursor for the next page; absence means end. Enable cursor only when continuing the same list."
            )
            item.setdefault("event", []).append(
                {
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": [
                            "pm.collectionVariables.set('page_cursor', pm.response.headers.get('X-Next-Cursor') || '');"
                        ],
                    },
                }
            )
        if joined.startswith("users/me/supplements/") and joined.endswith("verify"):
            request["description"] = (
                "Confirm the explicitly selected supplement. Skip the voice supplement stage only after all active supplements have confirmed observations today. Requires a retry key."
            )

# Retired development-only triggers are absent from the production contract.
for group in collection["item"]:
    group["item"] = [
        item
        for item in group["item"]
        if item.get("request", {}).get("url", {}).get("path")
        != ["reminders", "run-daily"]
    ]

# Privacy routes remain disabled until the policy and support owner are configured.
privacy_examples = []
for title, method, path, body in (
    ("Personal data export manifest", "GET", "users/me/privacy/export", None),
    ("Export owned check-in page", "GET", "users/me/privacy/export/check_ins", None),
    ("Request deletion review", "POST", "users/me/privacy/requests", {"confirm": True}),
    (
        "Cancel deletion request",
        "POST",
        "users/me/privacy/requests/{{privacy_request_id}}/cancel",
        None,
    ),
):
    request = {
        "method": method,
        "auth": {
            "type": "bearer",
            "bearer": [{"key": "token", "value": "{{token}}", "type": "string"}],
        },
        "header": [],
        "url": {
            "raw": "{{baseUrl}}/" + path,
            "host": ["{{baseUrl}}"],
            "path": path.split("/"),
        },
        "description": "Requires configured privacy tools. Requests are reviewed, not automatically erased. Export pages are independently consistent; follow next_cursor using the after query parameter.",
    }
    if body is not None:
        request["body"] = {"mode": "raw", "raw": json.dumps(body)}
        request["header"] = [
            {"key": "Content-Type", "value": "application/json"},
            {"key": "Idempotency-Key", "value": "{{idempotency_key}}"},
        ]
    privacy_examples.append({"name": title, "request": request})
collection["item"].append(
    {"name": "Privacy and personal data", "item": privacy_examples}
)
collection["variable"].append(
    {"key": "privacy_request_id", "value": "", "type": "string"}
)

care_examples = []
for title, method, path, body, retry in (
    ("Portal account identity", "GET", "portal/me", None, False),
    (
        "Invite care recipient",
        "POST",
        "users/me/care-connections",
        {
            "recipient_id": "{{recipient_id}}",
            "relationship": "clinician",
            "consent": True,
        },
        False,
    ),
    ("List patient connections", "GET", "users/me/care-connections", None, False),
    (
        "Revoke care access",
        "DELETE",
        "users/me/care-connections/{{connection_id}}",
        None,
        False,
    ),
    (
        "Accept care invitation",
        "POST",
        "care-connections/accept",
        {"token": "{{invitation_token}}"},
        False,
    ),
    ("Connected patients", "GET", "portal/patients", None, False),
    (
        "Clinician patient overview",
        "GET",
        "portal/patients/{{patient_id}}",
        None,
        False,
    ),
    (
        "Confirmed patient history",
        "GET",
        "portal/patients/{{patient_id}}/check-ins",
        None,
        False,
    ),
    (
        "Patient latest summary",
        "GET",
        "portal/patients/{{patient_id}}/summary/latest",
        None,
        False,
    ),
    (
        "Upcoming patient appointment",
        "GET",
        "portal/patients/{{patient_id}}/appointment",
        None,
        False,
    ),
    (
        "Patient emergency alerts",
        "GET",
        "portal/patients/{{patient_id}}/alerts",
        None,
        False,
    ),
    (
        "Acknowledge alert",
        "POST",
        "portal/patients/{{patient_id}}/alerts/{{alert_id}}/acknowledge",
        None,
        True,
    ),
    (
        "Sync confirmed offline check-in",
        "POST",
        "checkin/offline-sync",
        {
            "schema_version": 1,
            "client_submission_id": "{{client_submission_id}}",
            "recorded_at": "2026-10-22T08:30:00+03:00",
            "client_confirmed_at": "2026-10-22T08:32:00+03:00",
            "confirmed": True,
            "symptoms": [
                {
                    "raw_text": "Synthetic symptom report",
                    "category": "high_fever",
                    "severity": "unspecified",
                }
            ],
            "food_log": [],
            "supplement_check": [],
            "closing_mentions": [],
        },
        True,
    ),
):
    request = {
        "method": method,
        "auth": {
            "type": "bearer",
            "bearer": [{"key": "token", "value": "{{token}}", "type": "string"}],
        },
        "header": [],
        "url": {
            "raw": "{{baseUrl}}/" + path,
            "host": ["{{baseUrl}}"],
            "path": path.split("/"),
        },
        "description": "Care/offline features default off. Use the signed-in actor's token. Patient consent and recipient acceptance are required for portal data. Preserve offline submission UUID and payload on retries. See docs/care-offline-mvp.md.",
    }
    if body is not None:
        request["body"] = {"mode": "raw", "raw": json.dumps(body)}
        request["header"].append({"key": "Content-Type", "value": "application/json"})
    if retry:
        request["header"].append(
            {
                "key": "Idempotency-Key",
                "value": "{{client_submission_id}}"
                if path == "checkin/offline-sync"
                else "{{idempotency_key}}",
            }
        )
    care_examples.append({"name": title, "request": request})
collection["item"].append(
    {"name": "Care portal and offline check-ins", "item": care_examples}
)
for variable in (
    "recipient_id",
    "patient_id",
    "connection_id",
    "invitation_token",
    "alert_id",
    "client_submission_id",
):
    collection["variable"].append({"key": variable, "value": "", "type": "string"})

output_path = Path(__file__).resolve().parents[1] / "EnatAI_Postman_Collection.json"
rendered = json.dumps(collection, ensure_ascii=False, indent=2) + "\n"
if "--check" in sys.argv:
    if not output_path.exists() or output_path.read_text() != rendered:
        raise SystemExit(
            "Postman collection is stale: run scripts/generate_postman_collection.py"
        )
    print("Postman collection is current")
else:
    output_path.write_text(rendered)
    print(f"Generated Postman collection: {output_path}")
