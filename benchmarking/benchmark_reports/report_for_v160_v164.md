# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v160_v164_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:59:07 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 97 | 5 | 2 | 3 | 0 | **5.2%** | **94.8%** | 1.1% | 5.02s |
| **Deepgram** | 97 | 8 | 4 | 3 | 1 | **8.2%** | **91.8%** | 2.8% | 5.21s |
| **Gemini** | 97 | 4 | 2 | 2 | 0 | **4.1%** | **95.9%** | 0.6% | 4.43s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v160.wav`
> **Ground Truth Reference**:
> *I am throwing up everything I eat, I can't keep water down; I feel a weakness where I can't even stand up.*

#### Sahara
- **Latency**: 5.62s | **Ref Words**: 22 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 1.2%

```text
REF : i     am    throwing   up   everything   i    eat   i    cant   keep   water   down   i    feel   a    weakness   where   i    cant   even   stand   up  
HYP : ---   im    throwing   up   everything   i    eat   i    cant   keep   water   down   i    feel   a    weakness   where   i    cant   even   stand   up  
EVAL: DEL   SUB   ✓          ✓    ✓            ✓    ✓     ✓    ✓      ✓      ✓       ✓      ✓    ✓      ✓    ✓          ✓       ✓    ✓      ✓      ✓       ✓   
```

#### Deepgram
- **Latency**: 4.79s | **Ref Words**: 22 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 1.2%

```text
REF : i     am    throwing   up   everything   i    eat   i    cant   keep   water   down   i    feel   a    weakness   where   i    cant   even   stand   up  
HYP : ---   im    throwing   up   everything   i    eat   i    cant   keep   water   down   i    feel   a    weakness   where   i    cant   even   stand   up  
EVAL: DEL   SUB   ✓          ✓    ✓            ✓    ✓     ✓    ✓      ✓      ✓       ✓      ✓    ✓      ✓    ✓          ✓       ✓    ✓      ✓      ✓       ✓   
```

#### Gemini
- **Latency**: 4.57s | **Ref Words**: 22 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 1.2%

```text
REF : i     am    throwing   up   everything   i    eat   i    cant   keep   water   down   i    feel   a    weakness   where   i    cant   even   stand   up  
HYP : ---   im    throwing   up   everything   i    eat   i    cant   keep   water   down   i    feel   a    weakness   where   i    cant   even   stand   up  
EVAL: DEL   SUB   ✓          ✓    ✓            ✓    ✓     ✓    ✓      ✓      ✓       ✓      ✓    ✓      ✓    ✓          ✓       ✓    ✓      ✓      ✓       ✓   
```

---

### Voice: `v161.wav`
> **Ground Truth Reference**:
> *Oh I don't know! My stomach hurts a bit, but I can't tell if it's the usual fetal pressure or something else.*

#### Sahara
- **Latency**: 5.02s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : oh   i    dont   know   my   stomach   hurts   a    bit   but   i    cant   tell   if   its   the   usual   fetal   pressure   or   something   else  
HYP : oh   i    dont   know   my   stomach   hurts   a    bit   but   i    cant   tell   if   its   the   usual   fetal   pressure   or   something   else  
EVAL: ✓    ✓    ✓      ✓      ✓    ✓         ✓       ✓    ✓     ✓     ✓    ✓      ✓      ✓    ✓     ✓     ✓       ✓       ✓          ✓    ✓           ✓     
```

#### Deepgram
- **Latency**: 8.09s | **Ref Words**: 22 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.5%** | **Word Accuracy**: **95.5%** | **CER**: 1.2%

```text
REF : oh   i    dont   know   my   stomach   hurts   a    bit   but   i    cant   tell   if   its   the   usual   fetal   pressure   or   something   else  
HYP : oh   i    dont   know   my   stomach   hurts   a    bit   but   i    cant   tell   if   its   the   usual   fatal   pressure   or   something   else  
EVAL: ✓    ✓    ✓      ✓      ✓    ✓         ✓       ✓    ✓     ✓     ✓    ✓      ✓      ✓    ✓     ✓     ✓       SUB     ✓          ✓    ✓           ✓     
```

#### Gemini
- **Latency**: 4.2s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : oh   i    dont   know   my   stomach   hurts   a    bit   but   i    cant   tell   if   its   the   usual   fetal   pressure   or   something   else  
HYP : oh   i    dont   know   my   stomach   hurts   a    bit   but   i    cant   tell   if   its   the   usual   fetal   pressure   or   something   else  
EVAL: ✓    ✓    ✓      ✓      ✓    ✓         ✓       ✓    ✓     ✓     ✓    ✓      ✓      ✓    ✓     ✓     ✓       ✓       ✓          ✓    ✓           ✓     
```

---

### Voice: `v162.wav`
> **Ground Truth Reference**:
> *There is fluid, but I don't know if I leaked urine or my water broke, what should I do?*

#### Sahara
- **Latency**: 4.79s | **Ref Words**: 19 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : there   is   fluid   but   i    dont   know   if   i    leaked   urine   or   my   water   broke   what   should   i    do  
HYP : there   is   fluid   but   i    dont   know   if   i    leaked   urine   or   my   water   broke   what   should   i    do  
EVAL: ✓       ✓    ✓       ✓     ✓    ✓      ✓      ✓    ✓    ✓        ✓       ✓    ✓    ✓       ✓       ✓      ✓        ✓    ✓   
```

#### Deepgram
- **Latency**: 3.34s | **Ref Words**: 19 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **10.5%** | **Word Accuracy**: **89.5%** | **CER**: 7.7%

```text
REF : there   is   fluid   but   i    dont   know   if   i    leaked   ---   urine   or   my   water   broke   what   should   i    do  
HYP : there   is   fluid   but   i    dont   know   if   i    leaked   the   rain    or   my   water   broke   what   should   i    do  
EVAL: ✓       ✓    ✓       ✓     ✓    ✓      ✓      ✓    ✓    ✓        INS   SUB     ✓    ✓    ✓       ✓       ✓      ✓        ✓    ✓   
```

#### Gemini
- **Latency**: 5.19s | **Ref Words**: 19 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : there   is   fluid   but   i    dont   know   if   i    leaked   urine   or   my   water   broke   what   should   i    do  
HYP : there   is   fluid   but   i    dont   know   if   i    leaked   urine   or   my   water   broke   what   should   i    do  
EVAL: ✓       ✓    ✓       ✓     ✓    ✓      ✓      ✓    ✓    ✓        ✓       ✓    ✓    ✓       ✓       ✓      ✓        ✓    ✓   
```

---

### Voice: `v163.wav`
> **Ground Truth Reference**:
> *It's not blood, but I see a bit of brownish discharge, does that count as a danger sign?*

#### Sahara
- **Latency**: 4.79s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   blood   but   i    see   a    bit   of   brownish   discharge   does   that   count   as   a    danger   sign  
HYP : its   not   blood   but   i    see   a    bit   of   brownish   discharge   does   that   count   as   a    danger   sign  
EVAL: ✓     ✓     ✓       ✓     ✓    ✓     ✓    ✓     ✓    ✓          ✓           ✓      ✓      ✓       ✓    ✓    ✓        ✓     
```

#### Deepgram
- **Latency**: 5.84s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   blood   but   i    see   a    bit   of   brownish   discharge   does   that   count   as   a    danger   sign  
HYP : its   not   blood   but   i    see   a    bit   of   brownish   discharge   does   that   count   as   a    danger   sign  
EVAL: ✓     ✓     ✓       ✓     ✓    ✓     ✓    ✓     ✓    ✓          ✓           ✓      ✓      ✓       ✓    ✓    ✓        ✓     
```

#### Gemini
- **Latency**: 4.2s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   blood   but   i    see   a    bit   of   brownish   discharge   does   that   count   as   a    danger   sign  
HYP : its   not   blood   but   i    see   a    bit   of   brownish   discharge   does   that   count   as   a    danger   sign  
EVAL: ✓     ✓     ✓       ✓     ✓    ✓     ✓    ✓     ✓    ✓          ✓           ✓      ✓      ✓       ✓    ✓    ✓        ✓     
```

---

### Voice: `v164.wav`
> **Ground Truth Reference**:
> *Um... the headache is there, my vision is also slightly dim, but there is no bleeding.*

#### Sahara
- **Latency**: 4.86s | **Ref Words**: 16 | **Errors**: 3 (S: 1, D: 2, I: 0)
- **WER**: **18.8%** | **Word Accuracy**: **81.2%** | **CER**: 4.6%

```text
REF : um    the   headache   is   there   my   vision   is   also   slightly   dim   but   there   is       no   bleeding  
HYP : ---   the   headache   is   there   my   vision   is   also   slightly   dim   but   ---     theres   no   bleeding  
EVAL: DEL   ✓     ✓          ✓    ✓       ✓    ✓        ✓    ✓      ✓          ✓     ✓     DEL     SUB      ✓    ✓         
```

#### Deepgram
- **Latency**: 3.99s | **Ref Words**: 16 | **Errors**: 3 (S: 1, D: 2, I: 0)
- **WER**: **18.8%** | **Word Accuracy**: **81.2%** | **CER**: 4.6%

```text
REF : um    the   headache   is   there   my   vision   is   also   slightly   dim   but   there   is       no   bleeding  
HYP : ---   the   headache   is   there   my   vision   is   also   slightly   dim   but   ---     theres   no   bleeding  
EVAL: DEL   ✓     ✓          ✓    ✓       ✓    ✓        ✓    ✓      ✓          ✓     ✓     DEL     SUB      ✓    ✓         
```

#### Gemini
- **Latency**: 3.99s | **Ref Words**: 16 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 1.5%

```text
REF : um   the   headache   is   there   my   vision   is   also   slightly   dim   but   there   is       no   bleeding  
HYP : um   the   headache   is   there   my   vision   is   also   slightly   dim   but   ---     theres   no   bleeding  
EVAL: ✓    ✓     ✓          ✓    ✓       ✓    ✓        ✓    ✓      ✓          ✓     ✓     DEL     SUB      ✓    ✓         
```

---
