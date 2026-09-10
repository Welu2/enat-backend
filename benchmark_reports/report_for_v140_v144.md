# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v140_v144_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:58:01 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 46 | 0 | 0 | 0 | 0 | **0.0%** | **100.0%** | 0.0% | 4.98s |
| **Deepgram** | 46 | 1 | 1 | 0 | 0 | **2.2%** | **97.8%** | 1.6% | 3.14s |
| **Gemini** | 46 | 0 | 0 | 0 | 0 | **0.0%** | **100.0%** | 0.0% | 3.81s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v140.wav`
> **Ground Truth Reference**:
> *No, I haven't felt anything, I'm very well today, thank you.*

#### Sahara
- **Latency**: 5.55s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   i    havent   felt   anything   im   very   well   today   thank   you  
HYP : no   i    havent   felt   anything   im   very   well   today   thank   you  
EVAL: ✓    ✓    ✓        ✓      ✓          ✓    ✓      ✓      ✓       ✓       ✓    
```

#### Deepgram
- **Latency**: 3.25s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   i    havent   felt   anything   im   very   well   today   thank   you  
HYP : no   i    havent   felt   anything   im   very   well   today   thank   you  
EVAL: ✓    ✓    ✓        ✓      ✓          ✓    ✓      ✓      ✓       ✓       ✓    
```

#### Gemini
- **Latency**: 3.92s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   i    havent   felt   anything   im   very   well   today   thank   you  
HYP : no   i    havent   felt   anything   im   very   well   today   thank   you  
EVAL: ✓    ✓    ✓        ✓      ✓          ✓    ✓      ✓      ✓       ✓       ✓    
```

---

### Voice: `v141.wav`
> **Ground Truth Reference**:
> *Not at all. I haven't felt a headache or abdominal cramps, I'm fine.*

#### Sahara
- **Latency**: 5.06s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : not   at   all   i    havent   felt   a    headache   or   abdominal   cramps   im   fine  
HYP : not   at   all   i    havent   felt   a    headache   or   abdominal   cramps   im   fine  
EVAL: ✓     ✓    ✓     ✓    ✓        ✓      ✓    ✓          ✓    ✓           ✓        ✓    ✓     
```

#### Deepgram
- **Latency**: 3.28s | **Ref Words**: 13 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **7.7%** | **Word Accuracy**: **92.3%** | **CER**: 5.9%

```text
REF : not   at   all   i    havent   felt   a     headache   or   abdominal   cramps   im   fine  
HYP : not   at   all   i    havent   felt   the   headache   or   abdominal   cramps   im   fine  
EVAL: ✓     ✓    ✓     ✓    ✓        ✓      SUB   ✓          ✓    ✓           ✓        ✓    ✓     
```

#### Gemini
- **Latency**: 4.21s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : not   at   all   i    havent   felt   a    headache   or   abdominal   cramps   im   fine  
HYP : not   at   all   i    havent   felt   a    headache   or   abdominal   cramps   im   fine  
EVAL: ✓     ✓    ✓     ✓    ✓        ✓      ✓    ✓          ✓    ✓           ✓        ✓    ✓     
```

---

### Voice: `v142.wav`
> **Ground Truth Reference**:
> *No; in fact, I feel better today.*

#### Sahara
- **Latency**: 5.37s | **Ref Words**: 7 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   in   fact   i    feel   better   today  
HYP : no   in   fact   i    feel   better   today  
EVAL: ✓    ✓    ✓      ✓    ✓      ✓        ✓      
```

#### Deepgram
- **Latency**: 2.9s | **Ref Words**: 7 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   in   fact   i    feel   better   today  
HYP : no   in   fact   i    feel   better   today  
EVAL: ✓    ✓    ✓      ✓    ✓      ✓        ✓      
```

#### Gemini
- **Latency**: 3.93s | **Ref Words**: 7 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   in   fact   i    feel   better   today  
HYP : no   in   fact   i    feel   better   today  
EVAL: ✓    ✓    ✓      ✓    ✓      ✓        ✓      
```

---

### Voice: `v143.wav`
> **Ground Truth Reference**:
> *Nothing unusual, everything is normal.*

#### Sahara
- **Latency**: 3.85s | **Ref Words**: 5 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : nothing   unusual   everything   is   normal  
HYP : nothing   unusual   everything   is   normal  
EVAL: ✓         ✓         ✓            ✓    ✓       
```

#### Deepgram
- **Latency**: 2.98s | **Ref Words**: 5 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : nothing   unusual   everything   is   normal  
HYP : nothing   unusual   everything   is   normal  
EVAL: ✓         ✓         ✓            ✓    ✓       
```

#### Gemini
- **Latency**: 3.29s | **Ref Words**: 5 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : nothing   unusual   everything   is   normal  
HYP : nothing   unusual   everything   is   normal  
EVAL: ✓         ✓         ✓            ✓    ✓       
```

---

### Voice: `v144.wav`
> **Ground Truth Reference**:
> *No, none of the things you mentioned happened to me.*

#### Sahara
- **Latency**: 5.06s | **Ref Words**: 10 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   none   of   the   things   you   mentioned   happened   to   me  
HYP : no   none   of   the   things   you   mentioned   happened   to   me  
EVAL: ✓    ✓      ✓    ✓     ✓        ✓     ✓           ✓          ✓    ✓   
```

#### Deepgram
- **Latency**: 3.28s | **Ref Words**: 10 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   none   of   the   things   you   mentioned   happened   to   me  
HYP : no   none   of   the   things   you   mentioned   happened   to   me  
EVAL: ✓    ✓      ✓    ✓     ✓        ✓     ✓           ✓          ✓    ✓   
```

#### Gemini
- **Latency**: 3.68s | **Ref Words**: 10 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   none   of   the   things   you   mentioned   happened   to   me  
HYP : no   none   of   the   things   you   mentioned   happened   to   me  
EVAL: ✓    ✓      ✓    ✓     ✓        ✓     ✓           ✓          ✓    ✓   
```

---
