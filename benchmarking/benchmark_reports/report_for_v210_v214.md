# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v210_v214_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 10:02:26 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 108 | 11 | 8 | 1 | 2 | **10.2%** | **89.8%** | 5.2% | 5.47s |
| **Deepgram** | 108 | 8 | 6 | 2 | 0 | **7.4%** | **92.6%** | 4.1% | 3.83s |
| **Gemini** | 108 | 13 | 11 | 0 | 2 | **12.0%** | **88.0%** | 6.1% | 3.95s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v210.wav`
> **Ground Truth Reference**:
> *In the morning I drank oat with milk, for lunch I had doro wot, and in the afternoon I took roasted kolo and peanuts with extra milk.*

#### Sahara
- **Latency**: 5.63s | **Ref Words**: 27 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **7.4%** | **Word Accuracy**: **92.6%** | **CER**: 2.9%

```text
REF : in   the   morning   i    drank   oat   with   milk   for   lunch   i    had   doro   wot      and   in   the   afternoon   i    took   roasted   kolo   and   peanuts   with   extra   milk  
HYP : in   the   morning   i    drank   oat   with   milk   for   lunch   i    had   ---    doroid   and   in   the   afternoon   i    took   roasted   kolo   and   peanuts   with   extra   milk  
EVAL: ✓    ✓     ✓         ✓    ✓       ✓     ✓      ✓      ✓     ✓       ✓    ✓     DEL    SUB      ✓     ✓    ✓     ✓           ✓    ✓      ✓         ✓      ✓     ✓         ✓      ✓       ✓     
```

#### Deepgram
- **Latency**: 4.17s | **Ref Words**: 27 | **Errors**: 4 (S: 2, D: 2, I: 0)
- **WER**: **14.8%** | **Word Accuracy**: **85.2%** | **CER**: 8.6%

```text
REF : in   the   morning   i    drank   oat    with   milk   for   lunch   i    had   doro   wot   and   in   the   afternoon   i    took   roasted   kolo   and   peanuts   with   extra   milk  
HYP : in   the   morning   i    drank   oats   with   milk   for   lunch   i    had   ---    ---   and   in   the   afternoon   i    took   roasted   colo   and   peanuts   with   extra   milk  
EVAL: ✓    ✓     ✓         ✓    ✓       SUB    ✓      ✓      ✓     ✓       ✓    ✓     DEL    DEL   ✓     ✓    ✓     ✓           ✓    ✓      ✓         SUB    ✓     ✓         ✓      ✓       ✓     
```

#### Gemini
- **Latency**: 4.12s | **Ref Words**: 27 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 2.9%

```text
REF : in   the   morning   i    drank   oat    with   milk   for   lunch   i    had   doro   wot   and   in   the   afternoon   i    took   roasted   kolo   and   peanuts   with   extra   milk  
HYP : in   the   morning   i    drank   oats   with   milk   for   lunch   i    had   doro   wat   and   in   the   afternoon   i    took   roasted   colo   and   peanuts   with   extra   milk  
EVAL: ✓    ✓     ✓         ✓    ✓       SUB    ✓      ✓      ✓     ✓       ✓    ✓     ✓      SUB   ✓     ✓    ✓     ✓           ✓    ✓      ✓         SUB    ✓     ✓         ✓      ✓       ✓     
```

---

### Voice: `v211.wav`
> **Ground Truth Reference**:
> *Yes; I ate four times. Injera with shiro and greens, and in between I added fruit juice and yoghurt.*

#### Sahara
- **Latency**: 5.06s | **Ref Words**: 19 | **Errors**: 5 (S: 4, D: 0, I: 1)
- **WER**: **26.3%** | **Word Accuracy**: **73.7%** | **CER**: 12.8%

```text
REF : yes   i    ate   four   times   ---   injera    with   shiro   and   greens   and   in   between   i    added   fruit   juice   and   yoghurt  
HYP : yes   i    ate   4      times   in    general   with   shito   and   greens   and   in   between   i    added   fruit   juice   and   yogurt   
EVAL: ✓     ✓    ✓     SUB    ✓       INS   SUB       ✓      SUB     ✓     ✓        ✓     ✓    ✓         ✓    ✓       ✓       ✓       ✓     SUB      
```

#### Deepgram
- **Latency**: 3.67s | **Ref Words**: 19 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **10.5%** | **Word Accuracy**: **89.5%** | **CER**: 6.4%

```text
REF : yes   i    ate   four   times   injera   with   shiro     and   greens   and   in   between   i    added   fruit   juice   and   yoghurt  
HYP : yes   i    ate   four   times   injera   with   chorizo   and   greens   and   in   between   i    added   fruit   juice   and   yogurt   
EVAL: ✓     ✓    ✓     ✓      ✓       ✓        ✓      SUB       ✓     ✓        ✓     ✓    ✓         ✓    ✓       ✓       ✓       ✓     SUB      
```

#### Gemini
- **Latency**: 4.12s | **Ref Words**: 19 | **Errors**: 4 (S: 3, D: 0, I: 1)
- **WER**: **21.1%** | **Word Accuracy**: **79.0%** | **CER**: 12.8%

```text
REF : yes   i    ate   four   times   ---   injera   with   shiro      and   greens   and   in   between   i    added   fruit   juice   and   yoghurt  
HYP : yes   i    ate   four   times   and   jaro     with   shiitake   and   greens   and   in   between   i    added   fruit   juice   and   yogurt   
EVAL: ✓     ✓    ✓     ✓      ✓       INS   SUB      ✓      SUB        ✓     ✓        ✓     ✓    ✓         ✓    ✓       ✓       ✓       ✓     SUB      
```

---

### Voice: `v212.wav`
> **Ground Truth Reference**:
> *I didn't take an extra meal; for morning and lunch I just ate the usual injera with shiro, nothing different.*

#### Sahara
- **Latency**: 4.86s | **Ref Words**: 20 | **Errors**: 3 (S: 2, D: 0, I: 1)
- **WER**: **15.0%** | **Word Accuracy**: **85.0%** | **CER**: 8.1%

```text
REF : i    didnt   take   an   extra   meal   for   morning   and   lunch   i    just   ate   the   usual   ---   injera    with   shiro   nothing   different  
HYP : i    didnt   take   an   extra   meal   for   morning   and   lunch   i    just   ate   the   usual   in    general   with   sure    nothing   different  
EVAL: ✓    ✓       ✓      ✓    ✓       ✓      ✓     ✓         ✓     ✓       ✓    ✓      ✓     ✓     ✓       INS   SUB       ✓      SUB     ✓         ✓          
```

#### Deepgram
- **Latency**: 3.76s | **Ref Words**: 20 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.0%** | **Word Accuracy**: **95.0%** | **CER**: 3.5%

```text
REF : i    didnt   take   an   extra   meal   for   morning   and   lunch   i    just   ate   the   usual   injera   with   shiro   nothing   different  
HYP : i    didnt   take   an   extra   meal   for   morning   and   lunch   i    just   ate   the   usual   injera   with   shawl   nothing   different  
EVAL: ✓    ✓       ✓      ✓    ✓       ✓      ✓     ✓         ✓     ✓       ✓    ✓      ✓     ✓     ✓       ✓        ✓      SUB     ✓         ✓          
```

#### Gemini
- **Latency**: 3.41s | **Ref Words**: 20 | **Errors**: 4 (S: 3, D: 0, I: 1)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 10.5%

```text
REF : i    didnt   take   an   extra   meal   for   morning   and   lunch   i    just   ate   the   usual   ---   injera    with    shiro   nothing   different  
HYP : i    didnt   take   an   extra   meal   for   morning   and   lunch   i    just   ate   the   usual   in    general   which   sure    nothing   different  
EVAL: ✓    ✓       ✓      ✓    ✓       ✓      ✓     ✓         ✓     ✓       ✓    ✓      ✓     ✓     ✓       INS   SUB       SUB     SUB     ✓         ✓          
```

---

### Voice: `v213.wav`
> **Ground Truth Reference**:
> *No, nothing extra; today I only had bread with tea for breakfast, and I haven't eaten lunch yet.*

#### Sahara
- **Latency**: 5.27s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   nothing   extra   today   i    only   had   bread   with   tea   for   breakfast   and   i    havent   eaten   lunch   yet  
HYP : no   nothing   extra   today   i    only   had   bread   with   tea   for   breakfast   and   i    havent   eaten   lunch   yet  
EVAL: ✓    ✓         ✓       ✓       ✓    ✓      ✓     ✓       ✓      ✓     ✓     ✓           ✓     ✓    ✓        ✓       ✓       ✓    
```

#### Deepgram
- **Latency**: 3.52s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   nothing   extra   today   i    only   had   bread   with   tea   for   breakfast   and   i    havent   eaten   lunch   yet  
HYP : no   nothing   extra   today   i    only   had   bread   with   tea   for   breakfast   and   i    havent   eaten   lunch   yet  
EVAL: ✓    ✓         ✓       ✓       ✓    ✓      ✓     ✓       ✓      ✓     ✓     ✓           ✓     ✓    ✓        ✓       ✓       ✓    
```

#### Gemini
- **Latency**: 3.96s | **Ref Words**: 18 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 2.7%

```text
REF : no   nothing   extra   today   i    only   had   bread   with   tea   for   breakfast   and   i    havent   eaten   lunch   yet  
HYP : no   nothing   extra   today   i    only   had   bread   with   tea   for   breakfast   and   i    hasnt    eaten   lunch   yet  
EVAL: ✓    ✓         ✓       ✓       ✓    ✓      ✓     ✓       ✓      ✓     ✓     ✓           ✓     ✓    SUB      ✓       ✓       ✓    
```

---

### Voice: `v214.wav`
> **Ground Truth Reference**:
> *I didn't get anything nutritious; I only ate whatever split-pea stew was in the house with injera, there was no fruit or meat.*

#### Sahara
- **Latency**: 6.55s | **Ref Words**: 24 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.2%** | **Word Accuracy**: **95.8%** | **CER**: 3.0%

```text
REF : i    didnt   get   anything   nutritious   i    only   ate   whatever   split   pea   stew   was   in   the   house   with   injera   there   was   no   fruit   or   meat  
HYP : i    didnt   get   anything   nutritious   i    only   ate   whatever   split   pea   stew   was   in   the   house   with   njar     there   was   no   fruit   or   meat  
EVAL: ✓    ✓       ✓     ✓          ✓            ✓    ✓      ✓     ✓          ✓       ✓     ✓      ✓     ✓    ✓     ✓       ✓      SUB      ✓       ✓     ✓    ✓       ✓    ✓     
```

#### Deepgram
- **Latency**: 4.04s | **Ref Words**: 24 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.2%** | **Word Accuracy**: **95.8%** | **CER**: 1.0%

```text
REF : i    didnt   get   anything   nutritious   i    only   ate   whatever   split   pea   stew   was   in   the   house   with   injera   there   was   no   fruit   or   meat   
HYP : i    didnt   get   anything   nutritious   i    only   ate   whatever   split   pea   stew   was   in   the   house   with   injera   there   was   no   fruit   or   meats  
EVAL: ✓    ✓       ✓     ✓          ✓            ✓    ✓      ✓     ✓          ✓       ✓     ✓      ✓     ✓    ✓     ✓       ✓      ✓        ✓       ✓     ✓    ✓       ✓    SUB    
```

#### Gemini
- **Latency**: 4.12s | **Ref Words**: 24 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.2%** | **Word Accuracy**: **95.8%** | **CER**: 3.0%

```text
REF : i    didnt   get   anything   nutritious   i    only   ate   whatever   split   pea   stew   was   in   the   house   with   injera   there   was   no   fruit   or   meat  
HYP : i    didnt   get   anything   nutritious   i    only   ate   whatever   split   pea   stew   was   in   the   house   with   ginger   there   was   no   fruit   or   meat  
EVAL: ✓    ✓       ✓     ✓          ✓            ✓    ✓      ✓     ✓          ✓       ✓     ✓      ✓     ✓    ✓     ✓       ✓      SUB      ✓       ✓     ✓    ✓       ✓    ✓     
```

---
