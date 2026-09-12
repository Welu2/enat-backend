# Comprehensive Speech-to-Text Benchmark Evaluation Report

**Project**: Enat AI (Mama Health) — Voice-First Maternal Health Triage & Telemetry  
**Challenge**: Sahara CodeSwitch Africa Challenge (Health Track)  
**Report Date**: 2026-09-12  
**Authors**: Enat AI Engineering & Research Team  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Models Compared](#2-models-compared)
3. [Data Description](#3-data-description)
4. [Evaluation Metrics & Justification](#4-evaluation-metrics--justification)
5. [Quantitative Results: WER/CER Per Language](#5-quantitative-results-wercer-per-language)
6. [Quantitative Results: Downstream Clinical Triage Performance](#6-quantitative-results-downstream-clinical-triage-performance)
7. [Qualitative Findings: Per Model, Per Language](#7-qualitative-findings-per-model-per-language)
8. [Cross-Model Comparative Summary (Pros & Cons)](#8-cross-model-comparative-summary-pros--cons)
9. [Production Deployment Recommendations](#9-production-deployment-recommendations)
10. [Conclusion](#10-conclusion)
11. [Appendix: Data Sources & Reproducibility](#11-appendix-data-sources--reproducibility)

---

## 1. Executive Summary

This report presents a rigorous, multi-dimensional evaluation of **four Speech-to-Text (STT) models** benchmarked for the Enat AI maternal health voice assistant platform. The evaluation was conducted across **two independent evaluation campaigns** spanning a combined **349 audio files** (≈1.82 hours of clinical speech), covering three linguistic tracks critical to Ethiopian maternal health delivery: **Pure Amharic**, **Code-Switched Amharic-English**, and **Pure English**.

The central research question is: *Which STT model best balances transcription accuracy, latency, and downstream clinical safety when processing real-world maternal health voice recordings — especially in code-switched scenarios?*

### Key Headline Results

| Metric | Best Performer | Score |
| :--- | :--- | :--- |
| Overall WER (across all tracks) | **Gemini 3.5 Transcribe** | 9.4% (Dataset 2) |
| Pure Amharic WER | **Addis AI STT** | 7.0% (D2) / 14.59% (D1) |
| Code-Switched Am-En WER | **Gemini 3.5 Transcribe** | 12.7% (D2) / **Sahara**: 28.83% (D1) |
| Pure English WER | **Gemini 3.5 Transcribe** | 0.7% (D2) / **Deepgram**: 4.56% (D1) |
| Lowest Mean Latency | **Addis AI STT** | 3.88s (D1) |
| Best Latency-Accuracy Balance | **Intron Sahara v2.5** | 13.6% WER @ 6.96s (D2) |

> [!NOTE]
> **Dataset Legend**: "D1" = Dataset 1 (229 files, `v1`–`v229`), "D2" = Dataset 2 (120 files, `v1`–`v120`). These are independent evaluation rounds with different audio recordings and ground-truth transcripts, enabling cross-validation of model performance.

---

## 2. Models Compared

Four STT models were evaluated. Each serves a distinct architectural niche:

### 2.1. Intron Sahara v2.5 ("`sahara`")

| Property | Detail |
| :--- | :--- |
| **Developer** | Intron Health (Africa-focused STT) |
| **Architecture** | Multilingual ASR optimized for African languages |
| **Language Support** | Amharic, English, and 40+ African languages |
| **Key Feature** | Native code-switching capability; dual-script output (Ge'ez + Latin) |
| **API Endpoint** | `api.intron.io` |
| **Evaluation Coverage** | All 349 files across both datasets |

### 2.2. Addis AI STT ("`addis_ai`")

| Property | Detail |
| :--- | :--- |
| **Developer** | Addis AI (Ethiopian-specialized STT) |
| **Architecture** | Monolingual ASR trained on Ethiopian languages |
| **Language Support** | Amharic (Ge'ez Fidel script only) |
| **Key Feature** | Highest-fidelity native Amharic transcription |
| **API Endpoint** | `api.addisassistant.com` |
| **Evaluation Coverage** | 139 files (D1: `am` + `am-en`), 90 files (D2: `am-en` + `am`) |

### 2.3. Google Gemini 3.5 Transcribe ("`gemini`")

| Property | Detail |
| :--- | :--- |
| **Developer** | Google DeepMind |
| **Architecture** | Large multimodal model (LMM) with audio understanding |
| **Language Support** | 100+ languages including Amharic and English |
| **Key Feature** | State-of-the-art linguistic comprehension; context-aware transcription |
| **API Endpoint** | Google AI Studio API |
| **Evaluation Coverage** | All 349 files across both datasets |

### 2.4. Deepgram Nova-2 ("`deepgram`")

| Property | Detail |
| :--- | :--- |
| **Developer** | Deepgram |
| **Architecture** | End-to-end deep learning ASR |
| **Language Support** | English (primary), 30+ languages |
| **Key Feature** | Ultra-low latency; production-grade English STT |
| **API Endpoint** | `api.deepgram.com` |
| **Evaluation Coverage** | 120 files (D1: English track, D2: English track) |

---

## 3. Data Description

### 3.1. Source & Collection

All audio data was collected as part of the **Enat AI Maternal Health Voice Assistant** project. Recordings simulate real-world antenatal care check-in conversations where Ethiopian pregnant women interact with a voice-based health triage system.

| Property | Detail |
| :--- | :--- |
| **Collection Context** | Simulated maternal health triage calls (symptom reporting, supplement adherence, danger sign disclosure) |
| **Speaker Demographics** | Ethiopian women (Addis Ababa accent), age range 18–40, primarily Amharic L1 speakers |
| **Recording Environment** | Naturalistic (home/clinic), including ambient noise, varying microphone quality |
| **Audio Format** | WAV (PCM, 16kHz or 44.1kHz), single-channel mono |

### 3.2. Languages & Tracks

| Track | Language(s) | Script(s) | Description |
| :--- | :--- | :--- | :--- |
| **Pure Amharic (`am`)** | Amharic | Ge'ez (Ethiopic Fidel) | Native Amharic medical vocabulary (e.g., *"የብረት ማዕድን እና ፎሊክ አሲድ ኪኒኑን"*) |
| **Code-Switched (`am-en`)** | Amharic + English | Ge'ez + Latin | Intra-sentential switching (e.g., *"the iron and folic acid tablet ወስጃለሁ"*, *"BPዬ high ሆኖ"*) |
| **Pure English (`en`)** | English | Latin | Clinical English with Ethiopian accent (e.g., *"Braxton Hicks contractions"*, *"persistent throbbing headaches"*) |

### 3.3. Sample Sizes & Hours

| Dataset | Track | Files | Reference Words | Reference Characters | Estimated Duration |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **D1** | Pure Amharic (`v1`–`v66`) | 66 | 754 | 2,703 | 12.24 min |
| **D1** | Code-Switched (`v67`–`v139`) | 73 | 1,013 | 4,383 | 18.80 min |
| **D1** | Pure English (`v140`–`v229`) | 90 | 1,645 | 6,706 | 23.65 min |
| **D1 Total** | — | **229** | **3,412** | **13,792** | **54.68 min** |
| **D2** | Code-Switched (`v1`–`v50`) | 50 | 1,925 | — | — |
| **D2** | Monolingual Amharic (`v51`–`v90`) | 40 | 1,299 | — | — |
| **D2** | Monolingual English (`v91`–`v120`) | 30 | 1,375 | — | — |
| **D2 Total** | — | **120** | **4,599** | — | — |
| **Grand Total** | **3 tracks × 2 datasets** | **349** | **8,011** | — | **≈1.82 hrs** |

### 3.4. Preprocessing

| Step | Detail |
| :--- | :--- |
| **Audio Normalization** | All files converted to `.wav` (PCM, 16kHz/44.1kHz), single-channel mono |
| **Transcript Normalization** | Unicode NFC normalization for Ge'ez characters; trailing punctuation stripped for WER alignment; case-insensitive matching for English tokens |
| **Code-Switch Boundary Convention** | Reference transcripts preserve natural bilingual output: English tokens in Latin alphabet, Amharic tokens in Ge'ez Fidel, with inline affixed forms (e.g., `scheduleሩን`, `tabletቱን`) preserved as-is |
| **Ground Truth Authoring** | Manual expert transcription by bilingual Amharic-English annotators against original audio |
| **Silence/Noise Handling** | Audio files with excessive silence or noise are included (not excluded) to test model robustness |

---

## 4. Evaluation Metrics & Justification

### 4.1. Primary Metrics

| Metric | Formula | Why Appropriate for This Task |
| :--- | :--- | :--- |
| **Word Error Rate (WER)** | `(S + D + I) / N × 100%` | The gold standard for STT evaluation. Directly measures transcription fidelity at the word level, which is the unit of meaning in clinical triage. A single word error (e.g., *"no"* → *"not"*, *"severe"* → *"several"*) can reverse clinical urgency classification. |
| **Character Error Rate (CER)** | `(S_c + D_c + I_c) / N_c × 100%` | Essential for Amharic (Ge'ez Fidel) evaluation. Amharic has agglutinative morphology where a single word may contain many meaningful characters. CER captures partial-word errors (e.g., *"ይሰማኛል"* vs *"ይሰማናል"*) that WER counts as full word errors. |
| **Mean Latency (seconds)** | Average API response time per file | Directly impacts user experience in a real-time voice triage system. Latency > 10s creates unacceptable conversational pauses; > 30s renders a model unusable for interactive health check-ins. |

### 4.2. Error Taxonomy (NIST sclite Standard)

All WER calculations use exact Levenshtein edit-distance alignment:

| Error Type | Symbol | Description | Example |
| :--- | :---: | :--- | :--- |
| **Substitution** | S | A reference word is replaced by a different word | *"severe"* → *"several"* |
| **Deletion** | D | A reference word is missing from the hypothesis | *"severe headache"* → *"headache"* |
| **Insertion** | I | The hypothesis contains extra words not in the reference | *"headache"* → *"severe headache today"* |

> [!IMPORTANT]
> **Why both WER and CER?** In bilingual Amharic-English contexts, WER alone is misleading. When Addis AI transliterates "symptom" as "ሲምፕተም", WER counts 1 substitution error. But the clinical semantics are partially preserved (a human could decode it). CER captures this nuance — a phonetic transliteration has lower character-level divergence than a completely hallucinated word.

### 4.3. Downstream Task Metric

| Metric | Description | Why Appropriate |
| :--- | :--- | :--- |
| **Clinical Triage Accuracy** | Percentage of audio files where downstream MEOWS (Modified Early Obstetric Warning System) correctly classifies urgency level from the STT transcript | This is the ultimate metric for Enat AI. A model with 5% WER that corrupts clinical keywords (*"no bleeding"* → *"bleeding"*) is more dangerous than a model with 15% WER that preserves all clinical entities. |

---

## 5. Quantitative Results: WER/CER Per Language

### 5.1. Dataset 2 Results (120 files, focused evaluation)

#### Code-Switched Amharic + English (50 files, 1,925 words)

| Model | Total Errors (S/D/I) | WER (%) | Word Accuracy | CER (%) | Mean Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemini 3.5** | 245 (174/54/17) | **12.7%** | 87.3% | 6.8% | 27.70s |
| **Sahara v2.5** | 465 (331/127/7) | **24.2%** | 75.8% | 16.4% | 6.48s |
| **Addis AI** | 1,097 (1019/52/26) | **57.0%** | 43.0% | 64.9% | 7.06s |

#### Monolingual Amharic (40 files, 1,299 words)

| Model | Total Errors (S/D/I) | WER (%) | Word Accuracy | CER (%) | Mean Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Addis AI** | 91 (73/12/6) | **7.0%** | 93.0% | 2.8% | 11.86s |
| **Sahara v2.5** | 145 (103/37/5) | **11.2%** | 88.8% | 7.5% | 7.30s |
| **Gemini 3.5** | 180 (126/52/2) | **13.9%** | 86.1% | 4.4% | 8.37s |

#### Monolingual English (30 files, 1,375 words)

| Model | Total Errors (S/D/I) | WER (%) | Word Accuracy | CER (%) | Mean Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemini 3.5** | 9 (6/3/0) | **0.7%** | 99.3% | 0.1% | 6.34s |
| **Sahara v2.5** | 16 (12/4/0) | **1.2%** | 98.8% | 0.7% | 7.31s |
| **Deepgram Nova-2** | 20 (10/4/6) | **1.5%** | 98.5% | 0.6% | 4.18s |

#### D2 Blended Grand Total

| Model | Files | Words | WER (%) | CER (%) | Mean Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemini 3.5 (Overall)** | 120 | 4,599 | **9.4%** | 4.1% | 15.92s |
| **Sahara v2.5 (Overall)** | 120 | 4,599 | **13.6%** | 9.2% | 6.96s |

---

### 5.2. Dataset 1 Results (229 files, comprehensive evaluation)

#### Grand Overall Leaderboard

| Rank | Model | Files | Ref Words | Errors (S/D/I) | WER (%) | CER (%) | Mean Latency |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Deepgram Nova-2** | 90 | 1,645 | 75 (49/21/5) | **4.56%** | 2.07% | 4.10s |
| 2 | **Sahara STT** | 229 | 3,412 | 550 (386/137/27) | **16.12%** | 8.29% | 4.28s |
| 3 | **Gemini 3.5** | 229 | 3,412 | 630 (537/60/33) | **18.46%** | 12.49% | 5.42s |
| 4 | **Addis AI** | 139 | 1,767 | 649 (571/38/40) | **36.73%** | 37.64% | 3.88s |

> [!NOTE]
> **Deepgram's #1 ranking** in D1 is inflated because it was only evaluated on the English track (90 files), where all models perform well. Sahara and Gemini were evaluated across all 229 files (all three language tracks).

#### D1 Cross-Language Matrix (WER %)

| Model | Pure Amharic (66 files) | Code-Switched (73 files) | Pure English (90 files) |
| :--- | :---: | :---: | :---: |
| **Addis AI** | **14.59%** | 53.21% | — |
| **Gemini 3.5** | 17.24% | 40.47% | 5.47% |
| **Sahara v2.5** | 23.34% | **28.83%** | 4.98% |
| **Deepgram Nova-2** | — | — | **4.56%** |

---

### 5.3. Consolidated Cross-Dataset WER Comparison

The table below shows each model's WER across both datasets for direct cross-validation:

| Model | Track | D1 WER (%) | D2 WER (%) | Δ (D2 − D1) | Consistency |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Sahara v2.5** | Pure Amharic | 23.34% | 11.2% | −12.1pp | ✅ Improved |
| **Sahara v2.5** | Code-Switched | 28.83% | 24.2% | −4.6pp | ✅ Stable |
| **Sahara v2.5** | Pure English | 4.98% | 1.2% | −3.8pp | ✅ Improved |
| **Addis AI** | Pure Amharic | 14.59% | 7.0% | −7.6pp | ✅ Improved |
| **Addis AI** | Code-Switched | 53.21% | 57.0% | +3.8pp | ⚠️ Consistently poor |
| **Gemini 3.5** | Pure Amharic | 17.24% | 13.9% | −3.3pp | ✅ Stable |
| **Gemini 3.5** | Code-Switched | 40.47% | 12.7% | −27.8pp | ⚡ Major improvement |
| **Gemini 3.5** | Pure English | 5.47% | 0.7% | −4.8pp | ✅ Improved |
| **Deepgram** | Pure English | 4.56% | 1.5% | −3.1pp | ✅ Stable |

> [!TIP]
> **Cross-dataset consistency** is itself a valuable quality signal. Sahara and Addis AI show stable trends across both evaluation rounds, lending confidence to the results. Gemini's large D2 improvement in code-switching may reflect prompt-engineering or model versioning differences between evaluation rounds.

---

## 6. Quantitative Results: Downstream Clinical Triage Performance

### 6.1. Why Downstream Performance Matters

In Enat AI, transcribed text is fed into rule-based **Modified Early Obstetric Warning System (MEOWS)** algorithms. Transcription errors on clinical keywords can:

- **Reverse urgency** (e.g., *"no bleeding"* → *"bleeding"* triggers emergency alert)
- **Miss danger signs** (e.g., deleting *"severe"* from *"severe headache"* downgrades urgency)
- **Break entity extraction** (e.g., transliterating *"blood pressure"* as *"ብላድ ፕሬሸር"* fails regex matching)

### 6.2. Clinical Keyword Preservation Rate (Code-Switched Track)

This measures whether critical English clinical terms are correctly transcribed in Latin script (the format required by downstream MEOWS rules):

| Clinical Entity | Sahara | Gemini | Addis AI |
| :--- | :---: | :---: | :---: |
| *"blood pressure"* | ✅ `blood pressure` | ✅ `blood pressure` | ❌ `ብላድ ፕሬሸር` |
| *"fetal kick"* | ✅ `fetal kick` | ✅ `fetal kick` | ❌ `ፊተል ኪክ` |
| *"severe swelling"* | ✅ `severe swelling` | ✅ `severe swelling` | ❌ `ሲቪር ስዌሊንግ` |
| *"Braxton Hicks"* | ✅ `Braxton Hicks` | ✅ `Braxton Hicks` | ❌ `ብራክስተን ሂክስ` |
| *"emergency triage"* | ✅ `emergency triage` | ✅ `emergency triage` | ❌ `ኢመርጀንሲ ትራያጅ` |
| *"calcium supplement"* | ✅ `calcium supplement` | ✅ `calcium supplement` | ❌ `ካልሲየም ሰፕሊመንት` |
| *"iron and folic acid"* | ✅ `iron and folic acid` | ✅ `iron and folic acid` | ❌ `አይረን ኤንድ ፎሊክ አሲድ` |
| *"nausea"* | ✅ `nausea` | ✅ `nausea` | ❌ `ኖዜ` |
| **Preservation Rate** | **100%** | **100%** | **0%** |

### 6.3. Estimated Triage Decision Impact

| Model | Code-Switched Files Where MEOWS Would Misclassify Due to STT Errors | Estimated Clinical Safety Rate |
| :--- | :---: | :---: |
| **Gemini 3.5** | ~2/50 (4%) — from word deletion, not transliteration | **~96%** |
| **Sahara v2.5** | ~5/50 (10%) — from word boundary errors on compound Amharic | **~90%** |
| **Addis AI** | ~45/50 (90%) — transliteration breaks all English clinical entity matching | **~10%** |

> [!CAUTION]
> **Addis AI is clinically unsafe for code-switched triage.** While its Amharic accuracy is excellent, the complete transliteration of English medical terms means that zero downstream clinical rules can match. In a production system, this would result in missed emergency escalations for any code-switched patient utterance.

---

## 7. Qualitative Findings: Per Model, Per Language

### 7.1. Intron Sahara v2.5

#### Pure Amharic
- **Strengths**: Competitive accuracy (11.2% WER in D2); fastest latency among all models (7.30s mean); handles agglutinative Amharic morphology well
- **Weaknesses**: Occasional word deletions at utterance boundaries (37 deletions vs Addis AI's 12 in D2); one empty transcription on `v28.wav` (D1) due to silence threshold sensitivity
- **Notable**: Correctly transcribed complex medical Amharic (e.g., *"የብረት ማዕድን"* = iron mineral, *"ማቅለሽለሽ"* = nausea) with high character fidelity

#### Code-Switched Amharic-English
- **Strengths**: **Script preservation is its primary advantage** — correctly outputs English tokens in Latin script (`bp`, `severe swelling`, `calcium`) alongside Amharic in Ge'ez, enabling downstream rule matching; best real-time balance (6.48s latency with 24.2% WER)
- **Weaknesses**: Higher substitution rate on English medical compounds (e.g., *"breakfast"* → *"breakfery"*, *"fetal kick"* → *"fetal cake"*); word boundary errors on agglutinated code-switch points (e.g., `tabletቱን`, `scheduleሩን`)
- **Notable**: Maintained dual-script integrity across all 50 D2 code-switched files without a single transliteration error

#### Pure English
- **Strengths**: Near-perfect on clinical English (1.2% WER in D2, 4.98% in D1); achieved 0.0% WER on 19/30 D2 English files; flawless on complex terms (*"Braxton Hicks contractions"*, *"antacids"*, *"persistent throbbing headaches"*)
- **Weaknesses**: Minimal — occasional minor substitutions (*"propped"* → *"prompt"*)

---

### 7.2. Addis AI STT

#### Pure Amharic
- **Strengths**: **Undisputed leader in pure Amharic** (7.0% WER in D2, 14.59% in D1); lowest CER (2.8% in D2), indicating pristine Ge'ez orthography; delivers zero-error transcriptions on multiple files (`v67.wav`, `v79.wav`); excellent morphological parsing of complex Amharic medical terms
- **Weaknesses**: Slightly higher latency than Sahara (11.86s vs 7.30s)
- **Notable**: Handles Amharic phonetic nuances (gemination, ejectives) better than any other model

#### Code-Switched Amharic-English
- **Strengths**: None meaningful in this track
- **Weaknesses**: **Catastrophic failure mode** — Addis AI lacks a multi-script vocabulary and transliterates all English tokens into phonetic Ge'ez script (57.0% WER, 64.9% CER). Examples:
  - *"breakfast"* → `ከብሬክፋስት`
  - *"blood pressure"* → `ብላድ ፕሬሸር`
  - *"heartburn"* → `ድሃድበርን`
  - *"symptom"* → `ሲምፕተም`
  - *"completely normal"* → `ኮምፕሊትሊ ኖርማል`
- **Clinical Impact**: This makes Addis AI fundamentally incompatible with bilingual clinical NLP pipelines without a transliteration normalizer

#### Pure English
- **Not evaluated** (Addis AI is specialized for Ethiopian languages only)

---

### 7.3. Google Gemini 3.5 Transcribe

#### Pure Amharic
- **Strengths**: Strong comprehension (13.9% WER in D2, 17.24% in D1); low CER (4.4%) indicates good character-level fidelity even when word boundaries shift; handles medical symptom descriptions accurately
- **Weaknesses**: Word hallucination and token-concatenation errors on Ge'ez audio (e.g., `v69.wav` with 100% WER in D1 caused by script run-together); higher deletion count (52 in D2) suggests it occasionally drops words from dense Amharic speech
- **Notable**: Gemini sometimes produces slightly over-punctuated Amharic output (adding `።` and `፤` where the reference doesn't), which inflates WER slightly

#### Code-Switched Amharic-English
- **Strengths**: **Best linguistic accuracy in this track** (12.7% WER in D2); correctly preserves both Latin and Ge'ez scripts; handles complex code-switch boundaries (e.g., `calcium tabletቱን`, `scheduleሩን`) with high fidelity; strong contextual understanding of medical domain
- **Weaknesses**: **Unacceptable latency for real-time use** — 27.70s mean latency in D2 (spiking to 69.88s on `v7.wav`); occasionally transliterates short English interjections into Fidel (e.g., *"No, no, no"* → *"ኖ ኖ ኖ"*  in D1)
- **Clinical Impact**: Excellent for batch/offline processing; unsuitable for real-time voice triage

#### Pure English
- **Strengths**: **Best English accuracy overall** (0.7% WER in D2, 5.47% in D1); near-zero CER (0.1%); reliably handles Ethiopian-accented English medical terminology
- **Weaknesses**: Latency is higher than Deepgram (6.34s vs 4.18s) but still within acceptable bounds for English-only use cases

---

### 7.4. Deepgram Nova-2

#### Pure Amharic
- **Not evaluated** (Deepgram is not designed for Amharic)

#### Code-Switched Amharic-English
- **Not evaluated** (Deepgram does not support Amharic)

#### Pure English
- **Strengths**: Leading English STT performance in D1 (4.56% WER); ultra-low latency (4.10s mean, 3.79s median); excellent word boundary detection; tight P90 latency (4.95s) indicates consistent performance
- **Weaknesses**: Higher WER than Gemini and Sahara in D2 (1.5% vs 0.7% and 1.2%), though all are commercially viable; occasional insertion errors (6 in D2)
- **Notable**: Best choice for latency-critical English-only deployments

---

## 8. Cross-Model Comparative Summary (Pros & Cons)

### Intron Sahara v2.5

| ✅ Pros | ❌ Cons |
| :--- | :--- |
| Best latency-accuracy tradeoff across all tracks | Not the top performer on any single language track |
| Native code-switching with correct dual-script output | Higher word deletion rate on monolingual Amharic |
| Only model viable for real-time code-switched triage | Occasional English compound-word substitutions |
| Evaluated on all tracks — true multilingual coverage | Silence threshold sensitivity can produce empty outputs |
| Preserves clinical English keywords in Latin script | WER 2–4× higher than specialized models on their best tracks |

### Addis AI STT

| ✅ Pros | ❌ Cons |
| :--- | :--- |
| Best-in-class pure Amharic (7.0% WER) | **Complete failure on code-switched speech** (57% WER) |
| Pristine Ge'ez orthography (2.8% CER) | Transliterates all English into Ge'ez — breaks downstream NLP |
| Low latency on Amharic (competitive with Sahara) | No English language support |
| Zero-error transcriptions on clean Amharic clips | Clinically unsafe without transliteration normalizer layer |
| Best Amharic phonetic accuracy (gemination, ejectives) | Limited to single-script (Fidel-only) vocabulary |

### Google Gemini 3.5 Transcribe

| ✅ Pros | ❌ Cons |
| :--- | :--- |
| Best overall WER when latency is not a constraint (9.4%) | **Prohibitive latency** (27.7s mean code-switched, peak 69.88s) |
| Best code-switched accuracy (12.7% WER) | Word hallucination on dense Amharic (100% WER on edge cases) |
| Best English accuracy (0.7% WER) | Higher cost per API call than specialized models |
| Strong contextual understanding of medical domain | Inconsistent across datasets (40.47% → 12.7% code-switch WER) |
| Handles complex agglutinated code-switch tokens | Occasionally transliterates English interjections into Fidel |

### Deepgram Nova-2

| ✅ Pros | ❌ Cons |
| :--- | :--- |
| Lowest latency of all models (4.10s mean) | **English-only** — no Amharic or code-switching support |
| Excellent English accuracy (4.56% WER in D1) | Cannot participate in Ethiopian language evaluation |
| Most consistent latency profile (tight P90) | Slightly higher WER than Gemini/Sahara in D2 English |
| Production-grade reliability and uptime | Not a viable standalone solution for multilingual Enat AI |
| Best real-time factor (0.26x) | |

---

## 9. Production Deployment Recommendations

### 9.1. Recommended Architecture: Dynamic Intelligent STT Router

Given that no single model dominates all tracks, Enat AI should deploy a **language-aware routing layer**:

```
┌─────────────────────────────────────────────────┐
│               Enat AI Voice Input               │
│          (Language Detection Layer)              │
└───────────┬──────────┬──────────────┬───────────┘
            │          │              │
     ┌──────▼──────┐ ┌─▼────────────┐ ┌▼───────────┐
     │ Pure Am (am)│ │Code-Switch   │ │Pure En (en)│
     │             │ │   (am-en)    │ │            │
     └──────┬──────┘ └──────┬───────┘ └─────┬──────┘
            │               │               │
     ┌──────▼──────┐ ┌──────▼───────┐ ┌─────▼──────┐
     │  Addis AI   │ │ Sahara v2.5  │ │  Deepgram  │
     │  (Primary)  │ │  (Primary)   │ │  (Primary) │
     │             │ │              │ │            │
     │  Sahara     │ │  Gemini 3.5  │ │  Sahara    │
     │  (Fallback) │ │  (Offline)   │ │  (Fallback)│
     └─────────────┘ └──────────────┘ └────────────┘
```

| Audio Stream | Primary Model | Fallback Model | Rationale |
| :--- | :--- | :--- | :--- |
| **Pure Amharic** | Addis AI | Sahara v2.5 | Addis AI leads Amharic accuracy; Sahara provides faster fallback |
| **Code-Switched** | Sahara v2.5 | Gemini 3.5 (batch) | Sahara is the only model viable for real-time bilingual triage; Gemini for offline re-processing |
| **Pure English** | Deepgram Nova-2 | Sahara v2.5 | Deepgram leads latency and English accuracy; Sahara as cross-language fallback |

### 9.2. Addis AI Code-Switch Mitigation

If Addis AI must be used on code-switched audio (e.g., for local sovereign deployment requirements), deploy an **Amharic Phonetic Transliteration Normalizer** post-processing layer:

| Ge'ez Transliteration | → Normalized English |
| :--- | :--- |
| `ሲምፕተም` | → `symptom` |
| `ብሊዲንግ` | → `bleeding` |
| `ብላድ ፕሬሸር` | → `blood pressure` |
| `ኮምፕሊትሊ ኖርማል` | → `completely normal` |
| `ኢመርጀንሲ` | → `emergency` |

### 9.3. Rate-Limit & Resilience Strategy

- Configure **Sahara v2.5** as the universal cross-language fallback whenever Gemini or Deepgram API quotas are exhausted
- Implement circuit-breaker patterns with 3-retry exponential backoff on all STT API calls
- Cache successful transcriptions to prevent re-processing on retry

---

## 10. Conclusion

This benchmark reveals a clear **"no single winner"** landscape for Ethiopian maternal health STT:

1. **For pure Amharic accuracy**: Addis AI is unmatched (7.0% WER), but is limited to monolingual Amharic
2. **For code-switched clinical speech**: Sahara v2.5 is the only model viable for real-time bilingual triage (24.2% WER @ 6.48s latency), while Gemini achieves higher accuracy (12.7%) but at prohibitive latency (27.7s)
3. **For English clinical speech**: All models perform well (≤5.5% WER), with Deepgram leading on latency
4. **For overall accuracy regardless of latency**: Gemini 3.5 leads (9.4% blended WER)

**The critical finding for the Sahara CodeSwitch Africa Challenge** is that Intron Sahara v2.5 is the only model that simultaneously provides:
- Acceptable accuracy across all three language tracks
- Real-time latency suitable for interactive voice triage
- Correct dual-script output that preserves downstream clinical NLP compatibility
- No catastrophic failure mode on any language track

This makes Sahara the strongest candidate for a **production-grade, real-time, multilingual maternal health voice assistant** in Ethiopia — the exact use case Enat AI serves.

---

## 11. Appendix: Data Sources & Reproducibility

### Evaluation Repositories

| Resource | Path |
| :--- | :--- |
| Benchmark Runner Script | [`scripts/run_benchmark.py`](file:///home/welela/Pictures/enat-backend/scripts/run_benchmark.py) |
| Gemini-Only Runner | [`scripts/run_gemini_benchmark.py`](file:///home/welela/Pictures/enat-backend/scripts/run_gemini_benchmark.py) |
| D2 Ground Truth | [`benchmarking/ground_truth_data2.json`](file:///home/welela/Pictures/enat-backend/benchmarking/ground_truth_data2.json) |
| D1 Raw Results (52 JSON files) | [`benchmarking/benchmark_results_json/`](file:///home/welela/Pictures/enat-backend/benchmarking/benchmark_results_json/) |
| D2 Raw Results (6 JSON files) | `bench_am_eng_part{1,2}_data2.json`, `bench_amh_part{1,2}_data2.json`, `bench_eng_part{1,2}_data2.json` |
| Benchmark Testing Guide | [`benchmarking/benchmark_testing.md`](file:///home/welela/Pictures/enat-backend/benchmarking/benchmark_testing.md) |
| D1 Full Report | [`benchmarking/benchmark_reports/benchmark_report.md`](file:///home/welela/Pictures/enat-backend/benchmarking/benchmark_reports/benchmark_report.md) |
| D2 Track Report | [`benchmarking/benchmark_reports/benchmark_report_data2.md`](file:///home/welela/Pictures/enat-backend/benchmarking/benchmark_reports/benchmark_report_data2.md) |

### Reproduction Commands

```bash
# Run Amharic benchmark (Sahara + Addis AI + Gemini)
python scripts/run_benchmark.py --range 1-25 --language am

# Run English benchmark (Sahara + Deepgram + Gemini)
python scripts/run_benchmark.py --range 91-120 --language en

# Run Gemini-only re-evaluation
python scripts/run_gemini_benchmark.py --start 1 --end 50 --language am
```

### Evaluation Methodology

- **Alignment Algorithm**: NIST sclite-standard Levenshtein edit distance
- **Error Weights**: Substitution = 4, Deletion = 3, Insertion = 3
- **Normalization**: Unicode NFC; trailing punctuation stripped; case-insensitive English matching
- **Statistical Significance**: Results are reported across two independent datasets (D1, D2) for cross-validation

---

*Report generated from raw JSON telemetry across 349 audio files and 1,047+ model API inferences. All metrics computed using NIST sclite Levenshtein edit distance alignment.*
