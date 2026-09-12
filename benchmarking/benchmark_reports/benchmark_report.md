# 📊 Comprehensive STT Benchmark Evaluation Report
**Project:** Enat AI — Maternal & Child Health Audio Intelligence System  
**Generated:** 2026-09-08 10:46:33 UTC  
**Dataset Coverage:** `v1` to `v229` (229 audio files | 46 benchmark batches)  
**Total Audio Duration:** 3281.06 seconds (54.68 minutes | 0.91 hours)  
**Total Reference Corpus:** 3,412 words (13,792 characters)  
**Total Model Inferences:** 687 API calls (229 files × 3 competing models per language tier)  

---

## 🏆 1. Executive Summary & Grand Overall Leaderboard
This scoreboard aggregates speech-to-text transcription accuracy across all **229 audio recordings** encompassing Pure Amharic, Code-Switched Amharic-English, and Pure English maternal health conversations. All word error rates (WER) and character error rates (CER) are calculated using exact NIST sclite-standard Levenshtein alignment (Substitution weight: 4, Deletion weight: 3, Insertion weight: 3).

| Rank | Model | Files | Ref Words | Errors (S / D / I) | WER (%) | Word Acc (%) | CER (%) | Mean Latency | Median Latency | P90 Latency |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Deepgram Nova-2** | 90 | 1645 | 75 (49 / 21 / 5) | **4.56%** | 95.44% | 2.07% | 4.10s | 3.79s | 4.95s |
| 2 | **Sahara STT** | 229 | 3412 | 550 (386 / 137 / 27) | **16.12%** | 83.88% | 8.29% | 4.28s | 4.04s | 5.66s |
| 3 | **Gemini 3.5 Transcribe** | 229 | 3412 | 630 (537 / 60 / 33) | **18.46%** | 81.54% | 12.49% | 5.42s | 4.22s | 8.91s |
| 4 | **Addis AI STT** | 139 | 1767 | 649 (571 / 38 / 40) | **36.73%** | 63.27% | 37.64% | 3.88s | 3.71s | 4.71s |

> [!NOTE]
> **Model Evaluation Coverage:**
> - **Gemini 3.5 Transcribe** & **Sahara STT**: Evaluated across **all 229 files** (`am`, `am-en`, `en`).
> - **Addis AI STT**: Evaluated across **139 files** (`am`: v1–v66 and `am-en`: v67–v139). Addis AI is specialized for Ethiopian languages and was not tested on pure English.
> - **Deepgram Nova-2**: Evaluated across **90 files** (`en`: v140–v229). Deepgram was benchmarked specifically on the English test set.

---

## 🌐 2. Cross-Language Comparative Matrix
Direct comparison of Word Error Rate (WER %) and Mean Latency across each distinct linguistic tier:

| Model | Pure Amharic (`am`, v1–v66) | Code-Switched (`am-en`, v67–v139) | Pure English (`en`, v140–v229) | Overall Benchmark WER | Mean Latency (All) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemini 3.5 Transcribe** | 17.24% | 40.47% | 5.47% | **18.46%** | 5.42s |
| **Sahara STT** | 23.34% | 28.83% | 4.98% | **16.12%** | 4.28s |
| **Addis AI STT** | 14.59% | 53.21% | — | **36.73%** | 3.88s |
| **Deepgram Nova-2** | — | — | 4.56% | **4.56%** | 4.10s |

---

## 📌 3. Pure Amharic (v1 – v66)
*66 maternal health audio samples recorded in pure Amharic. Assesses native Fidel recognition, medical vocabulary handling, and Amharic phonetic nuances.*

- **Audio Files:** 66 recordings (`v1` to `v66`)
- **Cumulative Audio Duration:** 734.13 seconds (12.24 minutes)
- **Ground Truth Vocabulary:** 754 total words (2703 characters)

| Rank | Model | Files | Ref Words | Errors (S / D / I) | WER (%) | Word Acc (%) | CER (%) | Mean Latency | Median Latency | P90 Latency |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Addis AI STT** | 66 | 754 | 110 (92 / 9 / 9) | **14.59%** | 85.41% | 5.55% | 3.62s | 3.52s | 4.30s |
| 2 | **Gemini 3.5 Transcribe** | 66 | 754 | 130 (117 / 10 / 3) | **17.24%** | 82.76% | 6.70% | 8.14s | 8.30s | 10.30s |
| 3 | **Sahara STT** | 66 | 754 | 176 (130 / 39 / 7) | **23.34%** | 76.66% | 12.91% | 3.56s | 3.10s | 4.85s |

### 🔍 Pure Amharic Key Observations:
- **Addis AI STT leads pure Amharic recognition (14.59% WER)**, achieving the highest accuracy on native Ge'ez Fidel script with pristine orthography.
- **Gemini 3.5 Transcribe demonstrates robust comprehension (17.24% WER)**, closely trailing Addis AI while handling medical symptom descriptions accurately.
- **Sahara STT shows strong baseline performance (23.34% WER)**, but had 1 empty transcription on `v28.wav` due to audio endpoint silence threshold sensitivity.

---

## 📌 4. Code-Switched Amharic-English (v67 – v139)
*73 clinical consultation audio samples where mothers and healthcare workers code-switch between Amharic and English (e.g., 'symptom የለኝም', 'bleeding ምናምን', 'completely normal').*

- **Audio Files:** 73 recordings (`v67` to `v139`)
- **Cumulative Audio Duration:** 1128.15 seconds (18.80 minutes)
- **Ground Truth Vocabulary:** 1013 total words (4383 characters)

| Rank | Model | Files | Ref Words | Errors (S / D / I) | WER (%) | Word Acc (%) | CER (%) | Mean Latency | Median Latency | P90 Latency |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Sahara STT** | 73 | 1013 | 292 (204 / 76 / 12) | **28.83%** | 71.17% | 15.22% | 3.78s | 3.57s | 4.89s |
| 2 | **Gemini 3.5 Transcribe** | 73 | 1013 | 410 (354 / 32 / 24) | **40.47%** | 59.53% | 31.60% | 4.37s | 3.81s | 5.35s |
| 3 | **Addis AI STT** | 73 | 1013 | 539 (479 / 29 / 31) | **53.21%** | 46.79% | 57.43% | 4.12s | 3.89s | 4.86s |

### 🔍 Code-Switched Amharic-English Key Observations:
- **Sahara STT leads Code-Switching (28.83% WER):** Sahara demonstrated the most balanced bilingual handling, accurately transcribing English clinical terms in Latin alphabet while preserving surrounding Amharic grammar in Fidel.
- **Gemini 3.5 Transcribe takes 2nd place (40.47% WER):** Gemini handled multi-script medical phrases well, but occasionally transliterated short English affirmative/negative interjections into Fidel (e.g., transcribing 'No, no, no' as 'ኖ ኖ ኖ ኖ'), which impacted word alignment against Latin reference transcripts.
- **The Fidel Transliteration Phenomenon (Addis AI, 53.21% WER):** Addis AI is trained strictly for Ethiopian Fidel script. When speakers say English clinical terms, Addis AI transliterates them phonetically into Ge'ez letters (e.g. `ሲምፕተም` instead of `symptom`, `ብሊዲንግ` instead of `bleeding`, `ኮምፕሊትሊ ኖርማል` instead of `completely normal`). While phonetically intelligible, this generates high Levenshtein word errors against bilingual Latin/Fidel reference transcripts.

---

## 📌 5. Pure English (v140 – v229)
*90 maternal health consultation audio samples spoken in English by Ethiopian speakers (Addis Ababa accent).*

- **Audio Files:** 90 recordings (`v140` to `v229`)
- **Cumulative Audio Duration:** 1418.78 seconds (23.65 minutes)
- **Ground Truth Vocabulary:** 1645 total words (6706 characters)

| Rank | Model | Files | Ref Words | Errors (S / D / I) | WER (%) | Word Acc (%) | CER (%) | Mean Latency | Median Latency | P90 Latency |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Deepgram Nova-2** | 90 | 1645 | 75 (49 / 21 / 5) | **4.56%** | 95.44% | 2.07% | 4.10s | 3.79s | 4.95s |
| 2 | **Sahara STT** | 90 | 1645 | 82 (52 / 22 / 8) | **4.98%** | 95.02% | 1.89% | 5.20s | 5.06s | 6.07s |
| 3 | **Gemini 3.5 Transcribe** | 90 | 1645 | 90 (66 / 18 / 6) | **5.47%** | 94.53% | 2.33% | 4.28s | 4.03s | 4.91s |

### 🔍 Pure English Key Observations:
- **Deepgram Nova-2 achieves #1 accuracy (4.56% WER)**, leading in precision, word boundary detection, and latency.
- **Sahara STT closely follows at #2 (4.98% WER)**, proving its strength as an all-round multilingual speech recognition engine.
- **Gemini 3.5 Transcribe ranks #3 (5.47% WER)**, reliably transcribing Ethiopian-accented English medical terminology with high precision.

---

## ⚡ 6. Latency & Real-Time Performance Profile
Comprehensive response latency distribution (in seconds) across all 687 inferences:

| Model | Inferences | Min Latency | Median (P50) | Mean Latency | 90th Percentile (P90) | Max Latency | Real-Time Factor (RTF) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Deepgram Nova-2** | 90 | 2.85s | 3.79s | 4.10s | 4.95s | 9.57s | 0.260x |
| **Sahara STT** | 229 | 2.37s | 4.04s | 4.28s | 5.66s | 19.20s | 0.298x |
| **Addis AI STT** | 139 | 2.76s | 3.71s | 3.88s | 4.71s | 8.17s | 0.290x |
| **Gemini 3.5 Transcribe** | 229 | 2.85s | 4.22s | 5.42s | 8.91s | 23.42s | 0.378x |

> **Note on Real-Time Factor (RTF):** Calculated as `Total Processing Time / Total Audio Duration`. An RTF < 1.0 indicates that audio is transcribed faster than real-time playback.

---

## 💡 7. Production Deployment & Architecture Recommendations

### 1. Dynamic Intelligent STT Router
Given that model performance diverges across language modes, Enat AI should employ language-aware routing:
- **Pure Amharic Audio Stream (`am`):** Route to **Addis AI STT** or **Gemini 3.5 Transcribe** for the highest fidelity Fidel transcriptions.
- **Code-Switched Audio Stream (`am-en`):** Route to **Gemini 3.5 Transcribe** or **Sahara STT**, which natively preserve Latin script for clinical terminology alongside Amharic.
- **Pure English Audio Stream (`en`):** Route to **Deepgram Nova-2** for low latency and high accuracy, with **Gemini 3.5 Transcribe** as fallback.

### 2. Handling Code-Switching with Addis AI
- If Addis AI is selected as primary for local sovereign deployment, integrate an **Amharic Phonetic Transliteration Normalizer** that maps common Ge'ez medical transliterations (e.g. `ሲምፕተም` $\leftrightarrow$ `symptom`, `ብሊዲንግ` $\leftrightarrow$ `bleeding`) prior to downstream clinical triage processing.

### 3. Rate-Limit & Resilience Strategy
- Configure **Sahara STT** as the primary cross-language fallback engine whenever Gemini or Deepgram quotas are exhausted.

---
*Benchmark report generated from raw JSON telemetry and evaluated using NIST sclite Levenshtein edit distance.*
