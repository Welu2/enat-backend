# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v150_v154_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:58:29 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 77 | 2 | 2 | 0 | 0 | **2.6%** | **97.4%** | 1.9% | 5.17s |
| **Deepgram** | 77 | 2 | 2 | 0 | 0 | **2.6%** | **97.4%** | 2.2% | 4.04s |
| **Gemini** | 77 | 2 | 2 | 0 | 0 | **2.6%** | **97.4%** | 1.9% | 4.38s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v150.wav`
> **Ground Truth Reference**:
> *My head doesn't hurt, but since the afternoon my eyes are very blurry, I can't see things clearly.*

#### Sahara
- **Latency**: 5.17s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   head   doesnt   hurt   but   since   the   afternoon   my   eyes   are   very   blurry   i    cant   see   things   clearly  
HYP : my   head   doesnt   hurt   but   since   the   afternoon   my   eyes   are   very   blurry   i    cant   see   things   clearly  
EVAL: ✓    ✓      ✓        ✓      ✓     ✓       ✓     ✓           ✓    ✓      ✓     ✓      ✓        ✓    ✓      ✓     ✓        ✓        
```

#### Deepgram
- **Latency**: 4.06s | **Ref Words**: 18 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 5.3%

```text
REF : my   head   doesnt   hurt   but   since   the   afternoon   my   eyes   are   very     blurry   i    cant   see   things   clearly  
HYP : my   head   doesnt   hurt   but   since   the   afternoon   my   eyes   are   really   blurry   i    cant   see   things   clearly  
EVAL: ✓    ✓      ✓        ✓      ✓     ✓       ✓     ✓           ✓    ✓      ✓     SUB      ✓        ✓    ✓      ✓     ✓        ✓        
```

#### Gemini
- **Latency**: 4.59s | **Ref Words**: 18 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 7.9%

```text
REF : my   head   doesnt   hurt   but   since   the   afternoon   my   eyes   are   very     blurry   i    cant   see   things   clearly  
HYP : my   head   doesnt   hurt   bad   since   the   afternoon   my   eyes   are   really   blurry   i    cant   see   things   clearly  
EVAL: ✓    ✓      ✓        ✓      SUB   ✓       ✓     ✓           ✓    ✓      ✓     SUB      ✓        ✓    ✓      ✓     ✓        ✓        
```

---

### Voice: `v151.wav`
> **Ground Truth Reference**:
> *Yes; when I went to the bathroom I saw some blood, it has really scared me.*

#### Sahara
- **Latency**: 4.3s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   when   i    went   to   the   bathroom   i    saw   some   blood   it   has   really   scared   me  
HYP : yes   when   i    went   to   the   bathroom   i    saw   some   blood   it   has   really   scared   me  
EVAL: ✓     ✓      ✓    ✓      ✓    ✓     ✓          ✓    ✓     ✓      ✓       ✓    ✓     ✓        ✓        ✓   
```

#### Deepgram
- **Latency**: 4.3s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   when   i    went   to   the   bathroom   i    saw   some   blood   it   has   really   scared   me  
HYP : yes   when   i    went   to   the   bathroom   i    saw   some   blood   it   has   really   scared   me  
EVAL: ✓     ✓      ✓    ✓      ✓    ✓     ✓          ✓    ✓     ✓      ✓       ✓    ✓     ✓        ✓        ✓   
```

#### Gemini
- **Latency**: 3.89s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   when   i    went   to   the   bathroom   i    saw   some   blood   it   has   really   scared   me  
HYP : yes   when   i    went   to   the   bathroom   i    saw   some   blood   it   has   really   scared   me  
EVAL: ✓     ✓      ✓    ✓      ✓    ✓     ✓          ✓    ✓     ✓      ✓       ✓    ✓     ✓        ✓        ✓   
```

---

### Voice: `v152.wav`
> **Ground Truth Reference**:
> *It's not urine, a watery clear fluid is leaking continuously, all my clothes are soaked.*

#### Sahara
- **Latency**: 6.09s | **Ref Words**: 15 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **6.7%** | **Word Accuracy**: **93.3%** | **CER**: 4.3%

```text
REF : its   not   urine   a    watery   clear   fluid   is   leaking   continuously   all   my   clothes   are   soaked  
HYP : its   not   urine   a    watery   clear   fluid   is   leaking   continuously   oh    my   clothes   are   soaked  
EVAL: ✓     ✓     ✓       ✓    ✓        ✓       ✓       ✓    ✓         ✓              SUB   ✓    ✓         ✓     ✓       
```

#### Deepgram
- **Latency**: 3.99s | **Ref Words**: 15 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **6.7%** | **Word Accuracy**: **93.3%** | **CER**: 4.3%

```text
REF : its   not   urine   a    watery   clear   fluid   is   leaking   continuously   all   my   clothes   are   soaked  
HYP : its   not   rain    a    watery   clear   fluid   is   leaking   continuously   all   my   clothes   are   soaked  
EVAL: ✓     ✓     SUB     ✓    ✓        ✓       ✓       ✓    ✓         ✓              ✓     ✓    ✓         ✓     ✓       
```

#### Gemini
- **Latency**: 5.43s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   urine   a    watery   clear   fluid   is   leaking   continuously   all   my   clothes   are   soaked  
HYP : its   not   urine   a    watery   clear   fluid   is   leaking   continuously   all   my   clothes   are   soaked  
EVAL: ✓     ✓     ✓       ✓    ✓        ✓       ✓       ✓    ✓         ✓              ✓     ✓    ✓         ✓     ✓       
```

---

### Voice: `v153.wav`
> **Ground Truth Reference**:
> *My abdomen is cramping severely; I can neither stand nor sit.*

#### Sahara
- **Latency**: 5.07s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   abdomen   is   cramping   severely   i    can   neither   stand   nor   sit  
HYP : my   abdomen   is   cramping   severely   i    can   neither   stand   nor   sit  
EVAL: ✓    ✓         ✓    ✓          ✓          ✓    ✓     ✓         ✓       ✓     ✓    
```

#### Deepgram
- **Latency**: 3.83s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   abdomen   is   cramping   severely   i    can   neither   stand   nor   sit  
HYP : my   abdomen   is   cramping   severely   i    can   neither   stand   nor   sit  
EVAL: ✓    ✓         ✓    ✓          ✓          ✓    ✓     ✓         ✓       ✓     ✓    
```

#### Gemini
- **Latency**: 3.96s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   abdomen   is   cramping   severely   i    can   neither   stand   nor   sit  
HYP : my   abdomen   is   cramping   severely   i    can   neither   stand   nor   sit  
EVAL: ✓    ✓         ✓    ✓          ✓          ✓    ✓     ✓         ✓       ✓     ✓    
```

---

### Voice: `v154.wav`
> **Ground Truth Reference**:
> *My hands and face are very swollen; my ring won't come off, and my eyes are puffy.*

#### Sahara
- **Latency**: 5.2s | **Ref Words**: 17 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.9%** | **Word Accuracy**: **94.1%** | **CER**: 4.8%

```text
REF : my   hands   and   face   are   very   swollen   my   ring   wont     come   off   and   my   eyes   are   puffy  
HYP : my   hands   and   face   are   very   swollen   my   ring   doesnt   come   off   and   my   eyes   are   puffy  
EVAL: ✓    ✓       ✓     ✓      ✓     ✓      ✓         ✓    ✓      SUB      ✓      ✓     ✓     ✓    ✓      ✓     ✓      
```

#### Deepgram
- **Latency**: 4.01s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   hands   and   face   are   very   swollen   my   ring   wont   come   off   and   my   eyes   are   puffy  
HYP : my   hands   and   face   are   very   swollen   my   ring   wont   come   off   and   my   eyes   are   puffy  
EVAL: ✓    ✓       ✓     ✓      ✓     ✓      ✓         ✓    ✓      ✓      ✓      ✓     ✓     ✓    ✓      ✓     ✓      
```

#### Gemini
- **Latency**: 4.03s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   hands   and   face   are   very   swollen   my   ring   wont   come   off   and   my   eyes   are   puffy  
HYP : my   hands   and   face   are   very   swollen   my   ring   wont   come   off   and   my   eyes   are   puffy  
EVAL: ✓    ✓       ✓     ✓      ✓     ✓      ✓         ✓    ✓      ✓      ✓      ✓     ✓     ✓    ✓      ✓     ✓      
```

---
