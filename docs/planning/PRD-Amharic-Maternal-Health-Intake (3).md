# Product Requirements Document
## Voice-Based Amharic Clinical Intake for Maternal Health (ANC Support)

**Status:** Draft for UniPods AI Programme application
**Team:** [Add names]
**Last updated:** August 2026

---

## 1. Problem Statement

In Ethiopia, maternal health outcomes are significantly affected by two related gaps:

- **Delayed care-seeking**: A 2025 systematic review found approximately 44.7% of women experienced delays in deciding to seek care, with lack of ANC (antenatal care) follow-up associated with those delays.
- **Low danger-sign awareness**: Another review found women's knowledge of obstetric danger signs was only about 48% during pregnancy.
- Ethiopia's national ANC guideline specifically emphasizes nutrition counseling, since inadequate dietary intake and maternal undernutrition remain significant problems.

Between scheduled ANC visits, there is no structured way for a pregnant woman to record symptoms, danger signs, or general wellbeing — and no structured record for her clinician to review when she does come in. Existing pregnancy/health apps assume typing, literacy, and often a non-Ethiopian context (language, diet, and health system).

## 2. Target Users

**Primary: Pregnant women in Ethiopia**
- Amharic speakers, may not be comfortable typing
- Attending (or should be attending) periodic ANC visits
- Managing pregnancy largely on their own between appointments

**Secondary: Health workers / clinicians**
- See patients briefly and infrequently
- Currently rely on the patient's memory for what happened between visits
- Need a fast, trustworthy way to review interim symptoms and flags at the point of care

## 3. Solution Summary

A voice-first Amharic intake app that lets a pregnant woman describe her symptoms and wellbeing naturally, converts her speech into structured clinical information via AI extraction, verifies each extracted item with her directly, checks the verified data against Ethiopian ANC protocol thresholds, and produces a clinician-ready summary for her next visit.

The AI's role is specifically **structured information extraction from natural speech**, not diagnosis and not free-form conversation — extracted data is verified by the patient and evaluated by a deterministic, auditable rules layer, not left to model judgment.

## 4. Core User Flow

1. Woman opens app, taps to start a check-in session (voice, hands-free where possible).
2. App asks a fixed sequence of prompts in Amharic:
   a. Symptoms / danger signs
   b. What did you eat today? (recorded, not scored or advised on)
   c. Supplement check — only asked if a supplement is on record (e.g., "did you take your iron today?"); skipped entirely otherwise
   d. "Anything else you'd like to mention?" — open-ended closing question where things like breastfeeding intent or therapeutic food mentions are picked up if she raises them, rather than being asked as fixed daily prompts
3. She responds to each prompt somewhat naturally — she may mention multiple things in one answer (e.g., "my feet have been swelling for three days and I have a bad headache").
4. Speech is transcribed (Amharic ASR).
5. AI extraction layer pulls structured fields from the transcription (symptom type, duration, severity, category).
6. App reads back each extracted item individually for confirmation ("swelling, 3 days — is that correct?").
7. If incorrect, she can correct that single item via text/selection (no need to redo the whole entry).
8. Once confirmed, structured data is checked against the deterministic ANC protocol rules engine.
9. If a danger sign is flagged, she is told directly to seek care now.
10. Data accumulates over time; before her next scheduled ANC visit (or on demand), a one-page clinician summary is generated.

## 5. Feature List

### Core (MVP)
- Voice check-in flow with fixed prompt set (Amharic)
- Amharic speech-to-text
- Multi-entity structured extraction from transcribed response
- Per-item verification (confirm/correct each extracted item individually)
- Typed correction fallback
- Deterministic rules engine checking structured data against Ethiopian ANC protocol danger-sign thresholds
- Patient-facing danger-sign alert (direct instruction to seek care)
- Clinician summary generation (on demand / pre-visit), delivered via a shareable link + QR code

### Supporting (if time allows)
- Basic nutrition topic tracking (no causal claims about fasting or specific practices)
- Medication/supplement (e.g., iron/folic acid) adherence tracking

### Explicitly out of scope
- Multiple languages (Amharic only for MVP)
- AI-generated diagnosis or treatment recommendations
- Real-time doctor-in-the-loop messaging or remote triage
- Full EMR integration
- Open-ended/unstructured chatbot conversation
- Doctor accounts, patient search/matching, or a multi-patient doctor dashboard (deferred to v2 roadmap — see §7.1)

## 6. Data Requirements

### 6.1 ANC Protocol Danger Signs

Sourced from Ethiopian maternal health guidelines and associated studies. Presence of any of these indicates a critical danger sign requiring immediate care-seeking. The rules engine (not the LLM) makes the final determination based on the extraction layer's category mapping:

| Category (schema value) | Description |
|---|---|
| `vaginal_bleeding` | Any severe vaginal bleeding during pregnancy |
| `swelling_hands_face` | Swollen hands or swollen face |
| `blurred_vision` | Blurred vision |
| `severe_abdominal_pain` | Severe abdominal pain, cramping, or sudden pelvic pressure |
| `fluid_leakage` | Leaking of fluid from the vagina, or water breaking without contractions |
| `severe_headache` | Severe or persistent headache |
| `persistent_nausea_vomiting` | Persistent nausea and vomiting |
| `high_fever` | High fever |
| `convulsions_loss_of_consciousness` | Convulsions or loss of consciousness |
| `difficulty_breathing` | Difficulty breathing |
| `severe_weakness_or_backache` | Severe weakness or persistent backache |
| `abnormal_fetal_movement` | Accelerated or reduced fetal movement |

### 6.2 Antenatal Nutrition Guidance (record-only tracking, no advice given)

Ethiopia's ANC guidelines emphasize nutrition due to the prevalence of maternal undernutrition. The app **records** conversational mentions of these topics for the clinician to review — it does not evaluate, score, or advise on nutritional adequacy. Just as danger-sign judgment stays in the deterministic rules layer rather than the LLM, nutritional adequacy judgment stays with the clinician, not the AI — Ethiopian food nutrition scoring is not a reliable or safe thing for the app to attempt in this MVP.

| Topic (schema value) | What's recorded |
|---|---|
| `dietary_intake` | Free-text/tagged log of what she ate that day — no scoring or advice |
| `supplement_taken` | Only asked if she has a supplement on record (see below); specific ("did you take your iron today?"), not generic |
| `therapeutic_food` | Mentions of BEP supplements or ready-to-use therapeutic foods, if raised |
| `breastfeeding_intent` | Captured only if she raises it, via the open-ended closing question (see §4) — not asked as a daily prompt |

**Supplement tracking design**: two-tier, to avoid a counterintuitive daily "no" for women not on any supplement:
- **Setup** (once, editable anytime / re-askable periodically e.g. every couple weeks): "Are you currently taking any supplements (iron, folic acid, etc.)?" If yes, record which.
- **Daily check-in**: only included in the fixed prompt sequence if a supplement is on record, and phrased specifically ("did you take your iron today?"), not as a generic yes/no.

**Note on MUAC**: MUAC (<23cm indicates acute malnutrition) is a *physically measured* value, not something a woman can reliably self-report via voice. It is not a voice-extraction field in this MVP. Instead, the clinician summary includes a standing reminder line ("MUAC screening due — check at visit") rather than attempting to capture a number through the intake flow. This could be added later as a manual number-entry field if needed.

### 6.3 Extraction Schema

Structured JSON the AI extraction layer outputs per check-in turn:

```json
{
  "symptoms": [
    {
      "raw_text": "እግሬ እያበጠ ነው",
      "category": "swelling_hands_face",
      "duration": "3 days",
      "severity": "mild | moderate | severe | unspecified",
      "danger_sign": true,
      "confirmed": null
    }
  ],
  "food_log": {
    "raw_text": "...",
    "confirmed": null
  },
  "supplement_check": {
    "supplement_name": "iron | folic_acid | other | null",
    "taken_today": true,
    "confirmed": null
  },
  "closing_mentions": [
    {
      "raw_text": "...",
      "topic": "breastfeeding_intent | therapeutic_food | other",
      "confirmed": null
    }
  ],
  "session_flags": {
    "any_danger_sign": false,
    "requires_immediate_alert": false
  }
}
```

- `category` must be one of the 12 danger-sign values in §6.1, or `null`/other for non-danger symptoms not on the protocol list.
- `confirmed` is set by the per-item verification step (true/false), not by the extraction step — nothing is finalized into the summary until confirmed.
- `danger_sign` is set deterministically (true only if `category` matches the protocol list) — this is a lookup, not an LLM judgment call.
- `food_log` is recorded as-is with no scoring or nutritional evaluation.
- `supplement_check` is only present in a session if a supplement is on record for the user (see §6.2); otherwise this step is skipped entirely, not asked and answered "no."
- `closing_mentions` captures whatever comes up in response to the open-ended "anything else?" prompt — this is where `breastfeeding_intent` and unprompted `therapeutic_food` mentions are picked up, rather than being asked as fixed daily questions.

### 6.4 Deterministic Rules Engine Logic

```
IF any symptom.category is in DANGER_SIGN_LIST AND symptom.confirmed == true:
    session_flags.any_danger_sign = true
    session_flags.requires_immediate_alert = true
    → trigger patient-facing "seek care now" message
ELSE:
    → log normally for clinician summary, no alert
```

### 6.5 Provenance Tagging

Each summary item indicates self-reported vs. any device-measured data (e.g., a future BP cuff reading or manually entered MUAC value), so the clinician can weight the information appropriately.

## 7. Technical Architecture

```
Voice input (Amharic)
      ↓
Speech-to-text (ASR)
      ↓
Structured extraction (LLM, few-shot prompted)
      ↓
Per-item verification (patient confirms/corrects)
      ↓
Deterministic rules engine (Ethiopian ANC protocol thresholds)
      ↓
Patient alert (if flagged)  +  Clinician summary (accumulated over time)
```

**Confirmed technical decisions:**
- ASR/TTS + LLM extraction: **Addis AI** (used previously by the team, no fine-tuning planned for MVP — few-shot prompting for extraction)
- Client platform: **Web app (Next.js)**
- Backend: **FastAPI**
- Database/storage: **Supabase**
- Team split: one person owns frontend (Next.js), one owns backend (FastAPI + Supabase + extraction/rules pipeline)

**Delivery mechanism**: no doctor accounts, search, or matching are built for MVP (see note below). Instead, each generated summary produces a **shareable link + QR code**:
- The link opens a read-only, snapshotted view of that summary (frozen to the data available at generation time — later check-ins don't alter it).
- The QR code encodes the same link, for quick scan-and-view at the appointment (e.g., clinic staff scans it on her phone).
- No login is required to view a summary link — access is via possession of the link/QR code, consistent with keeping the MVP patient-auth-only.

**Note on doctor accounts/dashboard**: a full doctor-facing flow (registration, patient search/matching, multi-patient dashboard, automatic pre-appointment delivery to a doctor's account) was considered but deliberately deferred — it would effectively require building a second product surface within the same 10-day window as the core voice pipeline, which is the primary technical differentiator for this application. This is documented as a **v2 roadmap item** rather than an MVP feature.

## 7.1 Clinician Summary: Aggregation & Trigger Mechanism

**Trigger mechanism**: the woman enters/edits her next known ANC appointment date in-app (a simple date field — no doctor-facing login required for MVP). This date drives when a pre-visit summary is generated. In addition, a "View my summary" option lets her generate a summary on demand at any time, independent of the appointment date.

**Generation timing**:
- **Pre-appointment (automatic)**: N days before the stored appointment date (e.g., 1–2 days), the app auto-generates the summary so it's ready to show at the visit. No delivery/messaging to the doctor is built — she (or clinic staff) opens the summary in-app at the appointment.
- **On-demand (manual)**: available any time via a button, useful if the appointment date isn't set yet or she wants an earlier check.

**Aggregation logic**:
- Pull all *confirmed* check-in entries between the last generated summary's end date (or account creation, if no prior summary) and today.
- Group by category:
  - **Danger signs**: listed individually with dates (e.g., "swelling reported on days 3, 7, 12"), not averaged or reduced to yes/no — clinicians need the pattern, not just occurrence.
  - **Food log**: recorded as a simple daily log table (date + what was eaten) — no scoring, no advice, for the clinician to review.
  - **Supplement adherence**: if applicable, a simple adherence count/pattern (e.g., "iron taken 5 of 7 days").
  - **Closing mentions**: anything raised in the open-ended "anything else?" prompt (e.g., breastfeeding intent, therapeutic food) listed with dates.
  - **General wellbeing trend**: brief rollup of non-danger-sign symptoms mentioned.
- Include the provenance line: all data in MVP is self-reported (no device-measured data yet).

**Data model (Supabase):**
```
check_ins (id, user_id, timestamp, symptoms[], food_log, supplement_check, closing_mentions[], danger_sign_triggered)
appointments (id, user_id, appointment_date, last_summary_generated_at)
summaries (id, user_id, period_start, period_end, generated_at, content_json, share_link_slug, qr_code_url)
```

## 8. Success Criteria (for demo / application)

- End-to-end flow works live: voice input → extraction → verification → flagged/unflagged result → summary output
- At least one realistic multi-symptom Amharic utterance is correctly extracted into multiple structured fields
- Danger-sign flagging correctly triggers off the rules engine, not the LLM
- A clinician summary can be generated and shown as a concrete artifact
- Team can clearly articulate what's real (working) vs. simulated in the demo

## 9. Key Risks

- **Amharic ASR/extraction reliability**: the single biggest technical risk. Ethiopian languages are recognized as low-resource in NLP research (e.g., EthioLLM). Mitigation: day-1/2 spike testing real Amharic speech through the chosen ASR before committing further; per-item verification and typed fallback exist specifically to absorb extraction errors.
- **Protocol data sourcing**: danger-sign thresholds and nutrition guidance must be pulled from an authoritative source (Ethiopian ANC/MNCH guideline), not assumed.
- **Differentiation**: prior Ethiopian work exists on Amharic maternal-health Q&A and ML-based maternal risk prediction. This product's claim to novelty rests specifically on the structured multi-entity extraction + per-item verification workflow, not on "Amharic + maternal health + AI" alone — this framing should stay consistent across the application and demo.
- **Safety/liability**: AI must never appear to diagnose or prescribe. All clinical thresholds must route through the deterministic rules layer, not model discretion.

## 10. Open Items Before Build Starts

- [x] Compile the specific ANC protocol danger-sign list and nutrition guidance from the Ethiopian MOH guideline (see §6.1, §6.2)
- [x] Finalize the extraction schema (exact fields/format) (see §6.3)
- [x] Choose ASR/TTS and LLM providers (Addis AI) — run day-1/2 spike test before further build
- [x] Decide client platform and backend stack (Next.js + FastAPI + Supabase)
- [x] Assign ownership of each pipeline stage between team members (frontend / backend split)
- [x] MUAC decision: out of MVP scope, clinician-facing reminder only (see §6.2 note)
- [ ] Run the Addis AI day-1/2 spike test on realistic Amharic maternal-health sentences
- [ ] Decide exact pre-appointment lead time (N days) for auto-generating the summary
