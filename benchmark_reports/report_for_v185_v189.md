# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v185_v189_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 10:00:07 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 105 | 6 | 2 | 4 | 0 | **5.7%** | **94.3%** | 3.1% | 5.24s |
| **Deepgram** | 105 | 4 | 2 | 2 | 0 | **3.8%** | **96.2%** | 3.3% | 3.96s |
| **Gemini** | 105 | 2 | 1 | 1 | 0 | **1.9%** | **98.1%** | 0.3% | 3.96s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v185.wav`
> **Ground Truth Reference**:
> *My breath is cut short, I can't breathe while sitting; my face and neck are also swollen.*

#### Sahara
- **Latency**: 6.07s | **Ref Words**: 17 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **11.8%** | **Word Accuracy**: **88.2%** | **CER**: 8.7%

```text
REF : my   breath   is   cut   short    i    cant   breathe   while   sitting   my   face   and   neck   are   also   swollen  
HYP : my   breath   is   ---   cattle   i    cant   breathe   while   sitting   my   face   and   neck   are   also   swollen  
EVAL: ✓    ✓        ✓    DEL   SUB      ✓    ✓      ✓         ✓       ✓         ✓    ✓      ✓     ✓      ✓     ✓      ✓        
```

#### Deepgram
- **Latency**: 5.25s | **Ref Words**: 17 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **11.8%** | **Word Accuracy**: **88.2%** | **CER**: 10.1%

```text
REF : my   breath   is   cut   short       i    cant   breathe   while   sitting   my   face   and   neck   are   also   swollen  
HYP : my   breath   is   ---   scattered   i    cant   breathe   while   sitting   my   face   and   neck   are   also   swollen  
EVAL: ✓    ✓        ✓    DEL   SUB         ✓    ✓      ✓         ✓       ✓         ✓    ✓      ✓     ✓      ✓     ✓      ✓        
```

#### Gemini
- **Latency**: 4.1s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   breath   is   cut   short   i    cant   breathe   while   sitting   my   face   and   neck   are   also   swollen  
HYP : my   breath   is   cut   short   i    cant   breathe   while   sitting   my   face   and   neck   are   also   swollen  
EVAL: ✓    ✓        ✓    ✓     ✓       ✓    ✓      ✓         ✓       ✓         ✓    ✓      ✓     ✓      ✓     ✓      ✓        
```

---

### Voice: `v186.wav`
> **Ground Truth Reference**:
> *Um... how do I tell you... it's not blood, but I saw a pinkish fluid this morning; is that a problem?*

#### Sahara
- **Latency**: 5.18s | **Ref Words**: 21 | **Errors**: 1 (S: 0, D: 1, I: 0)
- **WER**: **4.8%** | **Word Accuracy**: **95.2%** | **CER**: 2.8%

```text
REF : um    how   do   i    tell   you   its   not   blood   but   i    saw   a    pinkish   fluid   this   morning   is   that   a    problem  
HYP : ---   how   do   i    tell   you   its   not   blood   but   i    saw   a    pinkish   fluid   this   morning   is   that   a    problem  
EVAL: DEL   ✓     ✓    ✓    ✓      ✓     ✓     ✓     ✓       ✓     ✓    ✓     ✓    ✓         ✓       ✓      ✓         ✓    ✓      ✓    ✓        
```

#### Deepgram
- **Latency**: 3.37s | **Ref Words**: 21 | **Errors**: 1 (S: 0, D: 1, I: 0)
- **WER**: **4.8%** | **Word Accuracy**: **95.2%** | **CER**: 2.8%

```text
REF : um    how   do   i    tell   you   its   not   blood   but   i    saw   a    pinkish   fluid   this   morning   is   that   a    problem  
HYP : ---   how   do   i    tell   you   its   not   blood   but   i    saw   a    pinkish   fluid   this   morning   is   that   a    problem  
EVAL: DEL   ✓     ✓    ✓    ✓      ✓     ✓     ✓     ✓       ✓     ✓    ✓     ✓    ✓         ✓       ✓      ✓         ✓    ✓      ✓    ✓        
```

#### Gemini
- **Latency**: 4.29s | **Ref Words**: 21 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : um   how   do   i    tell   you   its   not   blood   but   i    saw   a    pinkish   fluid   this   morning   is   that   a    problem  
HYP : um   how   do   i    tell   you   its   not   blood   but   i    saw   a    pinkish   fluid   this   morning   is   that   a    problem  
EVAL: ✓    ✓     ✓    ✓    ✓      ✓     ✓     ✓     ✓       ✓     ✓    ✓     ✓    ✓         ✓       ✓      ✓         ✓    ✓      ✓    ✓        
```

---

### Voice: `v187.wav`
> **Ground Truth Reference**:
> *Oh please! My head hurts, but there is no bleeding or anything like that; I was thinking maybe if I drink tea it will pass.*

#### Sahara
- **Latency**: 5.13s | **Ref Words**: 25 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **8.0%** | **Word Accuracy**: **92.0%** | **CER**: 1.1%

```text
REF : oh   please   my   head   hurts   but   there   is       no   bleeding   or   anything   like   that   i    was   thinking   maybe   if   i    drink   tea   it   will   pass  
HYP : oh   please   my   head   hurts   but   ---     theres   no   bleeding   or   anything   like   that   i    was   thinking   maybe   if   i    drink   tea   it   will   pass  
EVAL: ✓    ✓        ✓    ✓      ✓       ✓     DEL     SUB      ✓    ✓          ✓    ✓          ✓      ✓      ✓    ✓     ✓          ✓       ✓    ✓    ✓       ✓     ✓    ✓      ✓     
```

#### Deepgram
- **Latency**: 3.82s | **Ref Words**: 25 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.0%** | **Word Accuracy**: **96.0%** | **CER**: 4.2%

```text
REF : oh   please   my   head   hurts   but   there   is   no   bleeding    or   anything   like   that   i    was   thinking   maybe   if   i    drink   tea   it   will   pass  
HYP : oh   please   my   head   hurts   but   there   is   no   breathing   or   anything   like   that   i    was   thinking   maybe   if   i    drink   tea   it   will   pass  
EVAL: ✓    ✓        ✓    ✓      ✓       ✓     ✓       ✓    ✓    SUB         ✓    ✓          ✓      ✓      ✓    ✓     ✓          ✓       ✓    ✓    ✓       ✓     ✓    ✓      ✓     
```

#### Gemini
- **Latency**: 4.17s | **Ref Words**: 25 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **8.0%** | **Word Accuracy**: **92.0%** | **CER**: 1.1%

```text
REF : oh   please   my   head   hurts   but   there   is       no   bleeding   or   anything   like   that   i    was   thinking   maybe   if   i    drink   tea   it   will   pass  
HYP : oh   please   my   head   hurts   but   ---     theres   no   bleeding   or   anything   like   that   i    was   thinking   maybe   if   i    drink   tea   it   will   pass  
EVAL: ✓    ✓        ✓    ✓      ✓       ✓     DEL     SUB      ✓    ✓          ✓    ✓          ✓      ✓      ✓    ✓     ✓          ✓       ✓    ✓    ✓       ✓     ✓    ✓      ✓     
```

---

### Voice: `v188.wav`
> **Ground Truth Reference**:
> *I don't know if my eyes are blurry because of the medication or the illness; but my head hurts.*

#### Sahara
- **Latency**: 4.64s | **Ref Words**: 19 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    dont   know   if   my   eyes   are   blurry   because   of   the   medication   or   the   illness   but   my   head   hurts  
HYP : i    dont   know   if   my   eyes   are   blurry   because   of   the   medication   or   the   illness   but   my   head   hurts  
EVAL: ✓    ✓      ✓      ✓    ✓    ✓      ✓     ✓        ✓         ✓    ✓     ✓            ✓    ✓     ✓         ✓     ✓    ✓      ✓      
```

#### Deepgram
- **Latency**: 3.64s | **Ref Words**: 19 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    dont   know   if   my   eyes   are   blurry   because   of   the   medication   or   the   illness   but   my   head   hurts  
HYP : i    dont   know   if   my   eyes   are   blurry   because   of   the   medication   or   the   illness   but   my   head   hurts  
EVAL: ✓    ✓      ✓      ✓    ✓    ✓      ✓     ✓        ✓         ✓    ✓     ✓            ✓    ✓     ✓         ✓     ✓    ✓      ✓      
```

#### Gemini
- **Latency**: 3.76s | **Ref Words**: 19 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    dont   know   if   my   eyes   are   blurry   because   of   the   medication   or   the   illness   but   my   head   hurts  
HYP : i    dont   know   if   my   eyes   are   blurry   because   of   the   medication   or   the   illness   but   my   head   hurts  
EVAL: ✓    ✓      ✓      ✓    ✓    ✓      ✓     ✓        ✓         ✓    ✓     ✓            ✓    ✓     ✓         ✓     ✓    ✓      ✓      
```

---

### Voice: `v189.wav`
> **Ground Truth Reference**:
> *My stomach is gassy, it has cramps but wait, its....is this kind of pain normal or should I go to the clinic?*

#### Sahara
- **Latency**: 5.2s | **Ref Words**: 23 | **Errors**: 1 (S: 0, D: 1, I: 0)
- **WER**: **4.3%** | **Word Accuracy**: **95.7%** | **CER**: 3.7%

```text
REF : my   stomach   is   gassy   it   has   cramps   but   wait   its   is   this   kind   of   pain   normal   or   should   i    go   to   the   clinic  
HYP : my   stomach   is   gassy   it   has   cramps   but   wait   ---   is   this   kind   of   pain   normal   or   should   i    go   to   the   clinic  
EVAL: ✓    ✓         ✓    ✓       ✓    ✓     ✓        ✓     ✓      DEL   ✓    ✓      ✓      ✓    ✓      ✓        ✓    ✓        ✓    ✓    ✓    ✓     ✓       
```

#### Deepgram
- **Latency**: 3.7s | **Ref Words**: 23 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   stomach   is   gassy   it   has   cramps   but   wait   its   is   this   kind   of   pain   normal   or   should   i    go   to   the   clinic  
HYP : my   stomach   is   gassy   it   has   cramps   but   wait   its   is   this   kind   of   pain   normal   or   should   i    go   to   the   clinic  
EVAL: ✓    ✓         ✓    ✓       ✓    ✓     ✓        ✓     ✓      ✓     ✓    ✓      ✓      ✓    ✓      ✓        ✓    ✓        ✓    ✓    ✓    ✓     ✓       
```

#### Gemini
- **Latency**: 3.5s | **Ref Words**: 23 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   stomach   is   gassy   it   has   cramps   but   wait   its   is   this   kind   of   pain   normal   or   should   i    go   to   the   clinic  
HYP : my   stomach   is   gassy   it   has   cramps   but   wait   its   is   this   kind   of   pain   normal   or   should   i    go   to   the   clinic  
EVAL: ✓    ✓         ✓    ✓       ✓    ✓     ✓        ✓     ✓      ✓     ✓    ✓      ✓      ✓    ✓      ✓        ✓    ✓        ✓    ✓    ✓    ✓     ✓       
```

---
