# Comprehensive STT Benchmark Evaluation Report: Mama Health (Enat AI)

- **Challenge**: Sahara CodeSwitch Africa Challenge (Health Track)
- **Application**: Mama Health (Enat AI) — Voice-First Maternal Health Triage & Telemetry
- **Evaluation Date**: 2026-09-09[cite: 1, 2, 3, 4, 5, 6]
- **Total Audio Files Evaluated**: 120 files (`v1.wav` – `v120.wav`)[cite: 1, 2, 3, 4, 5, 6]
- **Total Evaluated Reference Words**: 4,599 words[cite: 1, 2, 3, 4, 5, 6]
- **Models Benchmarked**: Intron Sahara v2.5, Addis AI, Google Gemini, and Deepgram[cite: 1, 2, 3, 4, 5, 6]
- **Evaluation Repositories**: `benchmarking/benchmark_results.json`

---

## 1. Executive Summary & Aggregate Performance

| Corpus Track | Total Files | Total Words | Model | Total Errors (S/D/I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Mean Latency |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Code-Switched Amharic + English** | 50[cite: 1, 4] | 1,925[cite: 1, 4] | **Sahara**[cite: 1, 4]<br>**Addis AI**[cite: 1, 4]<br>**Gemini**[cite: 1, 4] | 465 (331 / 127 / 7)[cite: 1, 4]<br>1,097 (1019 / 52 / 26)[cite: 1, 4]<br>245 (174 / 54 / 17)[cite: 1, 4] | **24.2%**[cite: 1, 4]<br>**57.0%**[cite: 1, 4]<br>**12.7%**[cite: 1, 4] | 75.8%[cite: 1, 4]<br>43.0%[cite: 1, 4]<br>87.3%[cite: 1, 4] | 16.4%[cite: 1, 4]<br>64.9%[cite: 1, 4]<br>6.8%[cite: 1, 4] | 6.48s[cite: 1, 4]<br>7.06s[cite: 1, 4]<br>27.70s[cite: 1, 4] |
| **Monolingual Amharic** | 40[cite: 2, 6] | 1,299[cite: 2, 6] | **Sahara**[cite: 2, 6]<br>**Addis AI**[cite: 2, 6]<br>**Gemini**[cite: 2, 6] | 145 (103 / 37 / 5)[cite: 2, 6]<br>91 (73 / 12 / 6)[cite: 2, 6]<br>180 (126 / 52 / 2)[cite: 2, 6] | **11.2%**[cite: 2, 6]<br>**7.0%**[cite: 2, 6]<br>**13.9%**[cite: 2, 6] | 88.8%[cite: 2, 6]<br>93.0%[cite: 2, 6]<br>86.1%[cite: 2, 6] | 7.5%[cite: 2, 6]<br>2.8%[cite: 2, 6]<br>4.4%[cite: 2, 6] | 7.30s[cite: 2, 6]<br>11.86s[cite: 2, 6]<br>8.37s[cite: 2, 6] |
| **Monolingual English** | 30[cite: 3, 5] | 1,375[cite: 3, 5] | **Sahara**[cite: 3, 5]<br>**Deepgram**[cite: 3, 5]<br>**Gemini**[cite: 3, 5] | 16 (12 / 4 / 0)[cite: 3, 5]<br>20 (10 / 4 / 6)[cite: 3, 5]<br>9 (6 / 3 / 0)[cite: 3, 5] | **1.2%**[cite: 3, 5]<br>**1.5%**[cite: 3, 5]<br>**0.7%**[cite: 3, 5] | 98.8%[cite: 3, 5]<br>98.5%[cite: 3, 5]<br>99.3%[cite: 3, 5] | 0.7%[cite: 3, 5]<br>0.6%[cite: 3, 5]<br>0.1%[cite: 3, 5] | 7.31s[cite: 3, 5]<br>4.18s[cite: 3, 5]<br>6.34s[cite: 3, 5] |
| **Blended Grand Total** | **120**[cite: 1, 2, 3, 4, 5, 6] | **4,599**[cite: 1, 2, 3, 4, 5, 6] | **Sahara (Overall)**[cite: 1, 2, 3, 4, 5, 6]<br>**Gemini (Overall)**[cite: 1, 2, 3, 4, 5, 6] | 626 (446 / 168 / 12)[cite: 1, 2, 3, 4, 5, 6]<br>434 (306 / 109 / 19)[cite: 1, 2, 3, 4, 5, 6] | **13.6%**[cite: 1, 2, 3, 4, 5, 6]<br>**9.4%**[cite: 1, 2, 3, 4, 5, 6] | 86.4%[cite: 1, 2, 3, 4, 5, 6]<br>90.6%[cite: 1, 2, 3, 4, 5, 6] | 9.2%[cite: 1, 2, 3, 4, 5, 6]<br>4.1%[cite: 1, 2, 3, 4, 5, 6] | **6.96s**[cite: 1, 2, 3, 4, 5, 6]<br>**15.92s**[cite: 1, 2, 3, 4, 5, 6] |

---

## 2. Track-by-Track Benchmark Analysis

### 2.1. Code-Switched Amharic + English (`v1.wav` – `v50.wav`)
The code-switched corpus models authentic tele-intake where expectant mothers and health extension workers freely mix Amharic with English medical terminology (e.g., *"the iron and folic acid tablet ወስጃለሁ"*, *"BPዬ high ሆኖ እንዳይሆን ፈርቻለሁ"*).

* **Part 1 (`v1`–`v25`, 966 Words)**[cite: 1]:
  * **Sahara**: 209 errors (S: 156, D: 51, I: 2) | WER: **21.6%** | CER: 15.5% | Avg Latency: 6.97s[cite: 1].
  * **Addis AI**: 544 errors (S: 509, D: 24, I: 11) | WER: **56.3%** | CER: 64.6% | Avg Latency: 8.12s[cite: 1].
  * **Gemini**: 119 errors (S: 89, D: 28, I: 2) | WER: **12.3%** | CER: 7.1% | Avg Latency: 34.31s[cite: 1].
* **Part 2 (`v26`–`v50`, 959 Words)**[cite: 4]:
  * **Sahara**: 256 errors (S: 175, D: 76, I: 5) | WER: **26.7%** | CER: 17.3% | Avg Latency: 5.99s[cite: 4].
  * **Addis AI**: 553 errors (S: 510, D: 28, I: 15) | WER: **57.7%** | CER: 65.2% | Avg Latency: 6.00s[cite: 4].
  * **Gemini**: 126 errors (S: 85, D: 26, I: 15) | WER: **13.1%** | CER: 6.4% | Avg Latency: 21.09s[cite: 4].

**Key Findings:**
* **The Addis AI Transliteration Barrier**: Addis AI suffers a severe performance penalty on code-switched speech (**57.0% WER**, **64.9% CER**)[cite: 1, 4]. Because it lacks a multi-script vocabulary, it transliterates all English words into phonetic Ge'ez (e.g., *"breakfast"* $\rightarrow$ *ከብሬክፋስት*, *"blood pressure"* $\rightarrow$ *ብላድ ፕሬሸር*, and *"heartburn"* $\rightarrow$ *ድሃድበርን*)[cite: 1, 4]. This breaks downstream medical parsing rules.
* **Sahara Script Preservation**: Sahara correctly isolates and outputs Latin tokens for critical clinical keywords (*"bp"*, *"severe swelling"*, *"calcium"*, *"nausea"*), sustaining a workable **24.2% WER**[cite: 1, 4].
* **Gemini Latency Latency Penalty**: Gemini achieves strong linguistic accuracy (**12.7% WER**) but exhibits an unviable average latency of **27.70 seconds** (spiking to **69.88s** on `v7.wav`), making it unsuited for real-time triage[cite: 1, 4].

---

### 2.2. Monolingual Amharic Track (`v51.wav` – `v90.wav`)
This track tests pure native Ge'ez input (e.g., *"የብረት ማዕድን እና ፎሊክ አሲድ ኪኒኑን"*, *"የፅንሱ እንቅስቃሴ በጣም ቀንሷል"*).

* **Part 1 (`v51`–`v70`, 652 Words)**[cite: 2]:
  * **Sahara**: 78 errors (S: 55, D: 21, I: 2) | WER: **12.0%** | CER: 8.0% | Avg Latency: 7.37s[cite: 2].
  * **Addis AI**: 52 errors (S: 41, D: 8, I: 3) | WER: **8.0%** | CER: 3.3% | Avg Latency: 11.59s[cite: 2].
  * **Gemini**: 113 errors (S: 67, D: 44, I: 2) | WER: **17.3%** | CER: 4.9% | Avg Latency: 7.69s[cite: 2].
* **Part 2 (`v71`–`v90`, 647 Words)**[cite: 6]:
  * **Sahara**: 67 errors (S: 48, D: 16, I: 3) | WER: **10.4%** | CER: 7.0% | Avg Latency: 7.22s[cite: 6].
  * **Addis AI**: 39 errors (S: 32, D: 4, I: 3) | WER: **6.0%** | CER: 2.2% | Avg Latency: 12.12s[cite: 6].
  * **Gemini**: 67 errors (S: 59, D: 8, I: 0) | WER: **10.4%** | CER: 3.8% | Avg Latency: 9.05s[cite: 6].

**Key Findings:**
* **Addis AI Monolingual Superiority**: When language switching is absent, Addis AI achieves the lowest WER (**7.0%**) and CER (**2.8%**)[cite: 2, 6], delivering zero-error transcriptions on clips like `v67.wav` and `v79.wav`[cite: 2, 6].
* **Sahara Native Robustness**: Sahara delivers competitive accuracy (**11.2% WER**, **7.5% CER**) while completing transcriptions substantially faster than Addis AI (**7.30s** vs. **11.86s**)[cite: 2, 6].
* **Gemini Failure Modes**: Gemini suffers from word hallucination and token-concatenation errors on Ge'ez audio (e.g., `v69.wav` with a 100% WER caused by script run-together)[cite: 2].

---

### 2.3. Monolingual English Track (`v91.wav` – `v120.wav`)
This track evaluates clinical reporting and intake in English.

* **Part 1 (`v91`–`v105`, 696 Words)**[cite: 3]:
  * **Sahara**: 13 errors (S: 9, D: 4, I: 0) | WER: **1.9%** | CER: 1.1% | Avg Latency: 6.72s[cite: 3].
  * **Deepgram**: 12 errors (S: 7, D: 1, I: 4) | WER: **1.7%** | CER: 0.6% | Avg Latency: 4.14s[cite: 3].
  * **Gemini**: 6 errors (S: 4, D: 2, I: 0) | WER: **0.9%** | CER: 0.1% | Avg Latency: 5.86s[cite: 3].
* **Part 2 (`v106`–`v120`, 679 Words)**[cite: 5]:
  * **Sahara**: 3 errors (S: 3, D: 0, I: 0) | WER: **0.4%** | CER: 0.3% | Avg Latency: 7.90s[cite: 5].
  * **Deepgram**: 8 errors (S: 3, D: 3, I: 2) | WER: **1.2%** | CER: 0.6% | Avg Latency: 4.22s[cite: 5].
  * **Gemini**: 3 errors (S: 2, D: 1, I: 0) | WER: **0.4%** | CER: 0.1% | Avg Latency: 6.81s[cite: 5].

**Key Findings:**
* All models proved commercially viable on English maternal speech, maintaining word accuracies $\ge 98.5\%$[cite: 3, 5].
* Sahara maintained **0.0% WER** across 19 of the 30 English test files[cite: 3, 5], flawlessly transcribing complex clinical tokens like *"Braxton Hicks contractions"*, *"throbbing headaches"*, and *"antacids"*[cite: 3, 5].

---

## 3. Impact on the Downstream Clinical Triage Task (Agentic Validation)

In maternal health triage, transcription errors directly degrade clinical decision accuracy. When transcribed text is fed into rule-based Modified Early Obstetric Warning System (MEOWS) algorithms, transcription fidelity dictates whether life-threatening conditions are caught or missed.