# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v170_v174_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:59:41 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 83 | 1 | 0 | 0 | 1 | **1.2%** | **98.8%** | 0.3% | 4.87s |
| **Deepgram** | 83 | 1 | 0 | 0 | 1 | **1.2%** | **98.8%** | 0.3% | 4.85s |
| **Gemini** | 83 | 4 | 3 | 0 | 1 | **4.8%** | **95.2%** | 2.9% | 4.15s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v170.wav`
> **Ground Truth Reference**:
> *It's not severe pain; it's just the normal pressure I feel when the baby pushes downward.*

#### Sahara
- **Latency**: 5.08s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   severe   pain   its   just   the   normal   pressure   i    feel   when   the   baby   pushes   downward  
HYP : its   not   severe   pain   its   just   the   normal   pressure   i    feel   when   the   baby   pushes   downward  
EVAL: ✓     ✓     ✓        ✓      ✓     ✓      ✓     ✓        ✓          ✓    ✓      ✓      ✓     ✓      ✓        ✓         
```

#### Deepgram
- **Latency**: 9.57s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   severe   pain   its   just   the   normal   pressure   i    feel   when   the   baby   pushes   downward  
HYP : its   not   severe   pain   its   just   the   normal   pressure   i    feel   when   the   baby   pushes   downward  
EVAL: ✓     ✓     ✓        ✓      ✓     ✓      ✓     ✓        ✓          ✓    ✓      ✓      ✓     ✓      ✓        ✓         
```

#### Gemini
- **Latency**: 4.67s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   severe   pain   its   just   the   normal   pressure   i    feel   when   the   baby   pushes   downward  
HYP : its   not   severe   pain   its   just   the   normal   pressure   i    feel   when   the   baby   pushes   downward  
EVAL: ✓     ✓     ✓        ✓      ✓     ✓      ✓     ✓        ✓          ✓    ✓      ✓      ✓     ✓      ✓        ✓         
```

---

### Voice: `v171.wav`
> **Ground Truth Reference**:
> *My stomach isn't cramping, but because I'm bloated with gas it feels a bit heavy.*

#### Sahara
- **Latency**: 4.75s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   stomach   isnt   cramping   but   because   im   bloated   with   gas   it   feels   a    bit   heavy  
HYP : my   stomach   isnt   cramping   but   because   im   bloated   with   gas   it   feels   a    bit   heavy  
EVAL: ✓    ✓         ✓      ✓          ✓     ✓         ✓    ✓         ✓      ✓     ✓    ✓       ✓    ✓     ✓      
```

#### Deepgram
- **Latency**: 3.43s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   stomach   isnt   cramping   but   because   im   bloated   with   gas   it   feels   a    bit   heavy  
HYP : my   stomach   isnt   cramping   but   because   im   bloated   with   gas   it   feels   a    bit   heavy  
EVAL: ✓    ✓         ✓      ✓          ✓     ✓         ✓    ✓         ✓      ✓     ✓    ✓       ✓    ✓     ✓      
```

#### Gemini
- **Latency**: 3.94s | **Ref Words**: 15 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 14.3%

```text
REF : my   stomach   isnt   cramping     but       because   im   bloated   with   gas   it   feels   a    bit   heavy  
HYP : my   stomach   is     encramping   perhaps   because   im   bloated   with   gas   it   feels   a    bit   heavy  
EVAL: ✓    ✓         SUB    SUB          SUB       ✓         ✓    ✓         ✓      ✓     ✓    ✓       ✓    ✓     ✓      
```

---

### Voice: `v172.wav`
> **Ground Truth Reference**:
> *When I woke up I was slightly nauseous, but now I ate and feel better; no more vomiting.*

#### Sahara
- **Latency**: 5.27s | **Ref Words**: 18 | **Errors**: 1 (S: 0, D: 0, I: 1)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 1.5%

```text
REF : when   i    woke   up   i    was   slightly   nauseous   but   now   i    ate   and   ---   feel   better   no   more   vomiting  
HYP : when   i    woke   up   i    was   slightly   nauseous   but   now   i    ate   and   i     feel   better   no   more   vomiting  
EVAL: ✓      ✓    ✓      ✓    ✓    ✓     ✓          ✓          ✓     ✓     ✓    ✓     ✓     INS   ✓      ✓        ✓    ✓      ✓         
```

#### Deepgram
- **Latency**: 4.2s | **Ref Words**: 18 | **Errors**: 1 (S: 0, D: 0, I: 1)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 1.5%

```text
REF : when   i    woke   up   i    was   slightly   nauseous   but   now   i    ate   and   ---   feel   better   no   more   vomiting  
HYP : when   i    woke   up   i    was   slightly   nauseous   but   now   i    ate   and   i     feel   better   no   more   vomiting  
EVAL: ✓      ✓    ✓      ✓    ✓    ✓     ✓          ✓          ✓     ✓     ✓    ✓     ✓     INS   ✓      ✓        ✓    ✓      ✓         
```

#### Gemini
- **Latency**: 3.99s | **Ref Words**: 18 | **Errors**: 1 (S: 0, D: 0, I: 1)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 1.5%

```text
REF : when   i    woke   up   i    was   slightly   nauseous   but   now   i    ate   and   ---   feel   better   no   more   vomiting  
HYP : when   i    woke   up   i    was   slightly   nauseous   but   now   i    ate   and   i     feel   better   no   more   vomiting  
EVAL: ✓      ✓    ✓      ✓    ✓    ✓     ✓          ✓          ✓     ✓     ✓    ✓     ✓     INS   ✓      ✓        ✓    ✓      ✓         
```

---

### Voice: `v173.wav`
> **Ground Truth Reference**:
> *My feet are slightly swollen; but I think it's because I've been standing all day, my hands and face are fine.*

#### Sahara
- **Latency**: 4.45s | **Ref Words**: 21 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   feet   are   slightly   swollen   but   i    think   its   because   ive   been   standing   all   day   my   hands   and   face   are   fine  
HYP : my   feet   are   slightly   swollen   but   i    think   its   because   ive   been   standing   all   day   my   hands   and   face   are   fine  
EVAL: ✓    ✓      ✓     ✓          ✓         ✓     ✓    ✓       ✓     ✓         ✓     ✓      ✓          ✓     ✓     ✓    ✓       ✓     ✓      ✓     ✓     
```

#### Deepgram
- **Latency**: 3.78s | **Ref Words**: 21 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   feet   are   slightly   swollen   but   i    think   its   because   ive   been   standing   all   day   my   hands   and   face   are   fine  
HYP : my   feet   are   slightly   swollen   but   i    think   its   because   ive   been   standing   all   day   my   hands   and   face   are   fine  
EVAL: ✓    ✓      ✓     ✓          ✓         ✓     ✓    ✓       ✓     ✓         ✓     ✓      ✓          ✓     ✓     ✓    ✓       ✓     ✓      ✓     ✓     
```

#### Gemini
- **Latency**: 4.41s | **Ref Words**: 21 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   feet   are   slightly   swollen   but   i    think   its   because   ive   been   standing   all   day   my   hands   and   face   are   fine  
HYP : my   feet   are   slightly   swollen   but   i    think   its   because   ive   been   standing   all   day   my   hands   and   face   are   fine  
EVAL: ✓    ✓      ✓     ✓          ✓         ✓     ✓    ✓       ✓     ✓         ✓     ✓      ✓          ✓     ✓     ✓    ✓       ✓     ✓      ✓     ✓     
```

---

### Voice: `v174.wav`
> **Ground Truth Reference**:
> *My back hurts occasionally, but it's not at the level of severe pain.*

#### Sahara
- **Latency**: 4.81s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   back   hurts   occasionally   but   its   not   at   the   level   of   severe   pain  
HYP : my   back   hurts   occasionally   but   its   not   at   the   level   of   severe   pain  
EVAL: ✓    ✓      ✓       ✓              ✓     ✓     ✓     ✓    ✓     ✓       ✓    ✓        ✓     
```

#### Deepgram
- **Latency**: 3.25s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   back   hurts   occasionally   but   its   not   at   the   level   of   severe   pain  
HYP : my   back   hurts   occasionally   but   its   not   at   the   level   of   severe   pain  
EVAL: ✓    ✓      ✓       ✓              ✓     ✓     ✓     ✓    ✓     ✓       ✓    ✓        ✓     
```

#### Gemini
- **Latency**: 3.75s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   back   hurts   occasionally   but   its   not   at   the   level   of   severe   pain  
HYP : my   back   hurts   occasionally   but   its   not   at   the   level   of   severe   pain  
EVAL: ✓    ✓      ✓       ✓              ✓     ✓     ✓     ✓    ✓     ✓       ✓    ✓        ✓     
```

---
