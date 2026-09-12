# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v175_v179_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:59:49 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 84 | 1 | 1 | 0 | 0 | **1.2%** | **98.8%** | 0.9% | 5.21s |
| **Deepgram** | 84 | 4 | 4 | 0 | 0 | **4.8%** | **95.2%** | 3.0% | 3.40s |
| **Gemini** | 84 | 2 | 2 | 0 | 0 | **2.4%** | **97.6%** | 1.2% | 3.81s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v175.wav`
> **Ground Truth Reference**:
> *Since last night the baby's kicks have decreased a lot; and today it hasn't moved even once.*

#### Sahara
- **Latency**: 5.71s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : since   last   night   the   babys   kicks   have   decreased   a    lot   and   today   it   hasnt   moved   even   once  
HYP : since   last   night   the   babys   kicks   have   decreased   a    lot   and   today   it   hasnt   moved   even   once  
EVAL: ✓       ✓      ✓       ✓     ✓       ✓       ✓      ✓           ✓    ✓     ✓     ✓       ✓    ✓       ✓       ✓      ✓     
```

#### Deepgram
- **Latency**: 3.68s | **Ref Words**: 17 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.9%** | **Word Accuracy**: **94.1%** | **CER**: 4.2%

```text
REF : since   last   night   the   babys   kicks   have   decreased   a    lot   and   today   it   hasnt   moved   even   once  
HYP : since   last   night   the   babys   hips    have   decreased   a    lot   and   today   it   hasnt   moved   even   once  
EVAL: ✓       ✓      ✓       ✓     ✓       SUB     ✓      ✓           ✓    ✓     ✓     ✓       ✓    ✓       ✓       ✓      ✓     
```

#### Gemini
- **Latency**: 4.19s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : since   last   night   the   babys   kicks   have   decreased   a    lot   and   today   it   hasnt   moved   even   once  
HYP : since   last   night   the   babys   kicks   have   decreased   a    lot   and   today   it   hasnt   moved   even   once  
EVAL: ✓       ✓      ✓       ✓     ✓       ✓       ✓      ✓           ✓    ✓     ✓     ✓       ✓    ✓       ✓       ✓      ✓     
```

---

### Voice: `v176.wav`
> **Ground Truth Reference**:
> *I can't breathe; I can't draw air in, and my heart is beating so fast.*

#### Sahara
- **Latency**: 5.21s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    cant   breathe   i    cant   draw   air   in   and   my   heart   is   beating   so   fast  
HYP : i    cant   breathe   i    cant   draw   air   in   and   my   heart   is   beating   so   fast  
EVAL: ✓    ✓      ✓         ✓    ✓      ✓      ✓     ✓    ✓     ✓    ✓       ✓    ✓         ✓    ✓     
```

#### Deepgram
- **Latency**: 3.56s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    cant   breathe   i    cant   draw   air   in   and   my   heart   is   beating   so   fast  
HYP : i    cant   breathe   i    cant   draw   air   in   and   my   heart   is   beating   so   fast  
EVAL: ✓    ✓      ✓         ✓    ✓      ✓      ✓     ✓    ✓     ✓    ✓       ✓    ✓         ✓    ✓     
```

#### Gemini
- **Latency**: 3.28s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    cant   breathe   i    cant   draw   air   in   and   my   heart   is   beating   so   fast  
HYP : i    cant   breathe   i    cant   draw   air   in   and   my   heart   is   beating   so   fast  
EVAL: ✓    ✓      ✓         ✓    ✓      ✓      ✓     ✓    ✓     ✓    ✓       ✓    ✓         ✓    ✓     
```

---

### Voice: `v177.wav`
> **Ground Truth Reference**:
> *Even if I drink water it comes back up; today alone I've thrown up over ten times, I'm utterly exhausted.*

#### Sahara
- **Latency**: 5.83s | **Ref Words**: 20 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.0%** | **Word Accuracy**: **95.0%** | **CER**: 3.7%

```text
REF : even   if   i    drink   water   it   comes   back   up   today   alone   ive   thrown   up   over   ten   times   im   utterly   exhausted  
HYP : even   if   i    drink   water   it   comes   back   up   today   alone   ive   thrown   up   over   10    times   im   utterly   exhausted  
EVAL: ✓      ✓    ✓    ✓       ✓       ✓    ✓       ✓      ✓    ✓       ✓       ✓     ✓        ✓    ✓      SUB   ✓       ✓    ✓         ✓          
```

#### Deepgram
- **Latency**: 3.49s | **Ref Words**: 20 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.0%** | **Word Accuracy**: **95.0%** | **CER**: 3.7%

```text
REF : even   if   i    drink   water   it   comes   back   up   today   alone   ive   thrown   up   over   ten   times   im   utterly   exhausted  
HYP : even   if   i    drink   water   it   comes   back   up   today   alone   ive   thrown   up   over   10    times   im   utterly   exhausted  
EVAL: ✓      ✓    ✓    ✓       ✓       ✓    ✓       ✓      ✓    ✓       ✓       ✓     ✓        ✓    ✓      SUB   ✓       ✓    ✓         ✓          
```

#### Gemini
- **Latency**: 4.3s | **Ref Words**: 20 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.0%** | **Word Accuracy**: **95.0%** | **CER**: 3.7%

```text
REF : even   if   i    drink   water   it   comes   back   up   today   alone   ive   thrown   up   over   ten   times   im   utterly   exhausted  
HYP : even   if   i    drink   water   it   comes   back   up   today   alone   ive   thrown   up   over   10    times   im   utterly   exhausted  
EVAL: ✓      ✓    ✓    ✓       ✓       ✓    ✓       ✓      ✓    ✓       ✓       ✓     ✓        ✓    ✓      SUB   ✓       ✓    ✓         ✓          
```

---

### Voice: `v178.wav`
> **Ground Truth Reference**:
> *My body is burning like fire; it's shaking me with chills and soaking my clothes.*

#### Sahara
- **Latency**: 5.01s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   body   is   burning   like   fire   its   shaking   me   with   chills   and   soaking   my   clothes  
HYP : my   body   is   burning   like   fire   its   shaking   me   with   chills   and   soaking   my   clothes  
EVAL: ✓    ✓      ✓    ✓         ✓      ✓      ✓     ✓         ✓    ✓      ✓        ✓     ✓         ✓    ✓        
```

#### Deepgram
- **Latency**: 3.4s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   body   is   burning   like   fire   its   shaking   me   with   chills   and   soaking   my   clothes  
HYP : my   body   is   burning   like   fire   its   shaking   me   with   chills   and   soaking   my   clothes  
EVAL: ✓    ✓      ✓    ✓         ✓      ✓      ✓     ✓         ✓    ✓      ✓        ✓     ✓         ✓    ✓        
```

#### Gemini
- **Latency**: 3.76s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   body   is   burning   like   fire   its   shaking   me   with   chills   and   soaking   my   clothes  
HYP : my   body   is   burning   like   fire   its   shaking   me   with   chills   and   soaking   my   clothes  
EVAL: ✓    ✓      ✓    ✓         ✓      ✓      ✓     ✓         ✓    ✓      ✓        ✓     ✓         ✓    ✓        
```

---

### Voice: `v179.wav`
> **Ground Truth Reference**:
> *My back feels like it's snapping deep inside the bone; I can't even turn around in bed.*

#### Sahara
- **Latency**: 4.31s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   back   feels   like   its   snapping   deep   inside   the   bone   i    cant   even   turn   around   in   bed  
HYP : my   back   feels   like   its   snapping   deep   inside   the   bone   i    cant   even   turn   around   in   bed  
EVAL: ✓    ✓      ✓       ✓      ✓     ✓          ✓      ✓        ✓     ✓      ✓    ✓      ✓      ✓      ✓        ✓    ✓    
```

#### Deepgram
- **Latency**: 2.85s | **Ref Words**: 17 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **11.8%** | **Word Accuracy**: **88.2%** | **CER**: 6.0%

```text
REF : my   back   feels   like   its   snapping   deep   inside   the   bone   i    cant   even   turn   around   in    bed  
HYP : my   back   feels   like   its   snapping   deep   inside   the   bone   i    cant   even   turn   around   a     bit  
EVAL: ✓    ✓      ✓       ✓      ✓     ✓          ✓      ✓        ✓     ✓      ✓    ✓      ✓      ✓      ✓        SUB   SUB  
```

#### Gemini
- **Latency**: 3.5s | **Ref Words**: 17 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.9%** | **Word Accuracy**: **94.1%** | **CER**: 1.5%

```text
REF : my   back   feels   like   its   snapping   deep   inside   the   bone   i    cant   even   turn   around   in   bed  
HYP : my   back   feels   like   its   napping    deep   inside   the   bone   i    cant   even   turn   around   in   bed  
EVAL: ✓    ✓      ✓       ✓      ✓     SUB        ✓      ✓        ✓     ✓      ✓    ✓      ✓      ✓      ✓        ✓    ✓    
```

---
