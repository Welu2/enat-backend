# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v205_v209_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 10:00:56 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 124 | 7 | 4 | 2 | 1 | **5.6%** | **94.4%** | 2.0% | 5.26s |
| **Deepgram** | 124 | 7 | 5 | 1 | 1 | **5.6%** | **94.4%** | 2.4% | 5.04s |
| **Gemini** | 124 | 7 | 6 | 1 | 0 | **5.6%** | **94.4%** | 3.0% | 4.31s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v205.wav`
> **Ground Truth Reference**:
> *I don't feel anything alarming; other than the pressure when the baby kicks now and then, I am fine.*

#### Sahara
- **Latency**: 4.57s | **Ref Words**: 19 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **10.5%** | **Word Accuracy**: **89.5%** | **CER**: 1.3%

```text
REF : i    dont   feel   anything   alarming   other   than   the   pressure   when   the   baby   kicks   now   and   then   i     am    fine  
HYP : i    dont   feel   anything   alarming   other   than   the   pressure   when   the   baby   kicks   now   and   then   ---   im    fine  
EVAL: ✓    ✓      ✓      ✓          ✓          ✓       ✓      ✓     ✓          ✓      ✓     ✓      ✓       ✓     ✓     ✓      DEL   SUB   ✓     
```

#### Deepgram
- **Latency**: 5.13s | **Ref Words**: 19 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **10.5%** | **Word Accuracy**: **89.5%** | **CER**: 1.3%

```text
REF : i    dont   feel   anything   alarming   other   than   the   pressure   when   the   baby   kicks   now   and   then   i     am    fine  
HYP : i    dont   feel   anything   alarming   other   than   the   pressure   when   the   baby   kicks   now   and   then   ---   im    fine  
EVAL: ✓    ✓      ✓      ✓          ✓          ✓       ✓      ✓     ✓          ✓      ✓     ✓      ✓       ✓     ✓     ✓      DEL   SUB   ✓     
```

#### Gemini
- **Latency**: 3.78s | **Ref Words**: 19 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **10.5%** | **Word Accuracy**: **89.5%** | **CER**: 1.3%

```text
REF : i    dont   feel   anything   alarming   other   than   the   pressure   when   the   baby   kicks   now   and   then   i     am    fine  
HYP : i    dont   feel   anything   alarming   other   than   the   pressure   when   the   baby   kicks   now   and   then   ---   im    fine  
EVAL: ✓    ✓      ✓      ✓          ✓          ✓       ✓      ✓     ✓          ✓      ✓     ✓      ✓       ✓     ✓     ✓      DEL   SUB   ✓     
```

---

### Voice: `v206.wav`
> **Ground Truth Reference**:
> *None of the symptoms you mentioned are there; just a bit of tiredness and reduced appetite today.*

#### Sahara
- **Latency**: 5.47s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : none   of   the   symptoms   you   mentioned   are   there   just   a    bit   of   tiredness   and   reduced   appetite   today  
HYP : none   of   the   symptoms   you   mentioned   are   there   just   a    bit   of   tiredness   and   reduced   appetite   today  
EVAL: ✓      ✓    ✓     ✓          ✓     ✓           ✓     ✓       ✓      ✓    ✓     ✓    ✓           ✓     ✓         ✓          ✓      
```

#### Deepgram
- **Latency**: 8.2s | **Ref Words**: 17 | **Errors**: 1 (S: 0, D: 0, I: 1)
- **WER**: **5.9%** | **Word Accuracy**: **94.1%** | **CER**: 3.8%

```text
REF : none   of   the   symptoms   you   mentioned   are   there   just   a    bit   of   tiredness   and   reduced   ---   appetite   today  
HYP : none   of   the   symptoms   you   mentioned   are   there   just   a    bit   of   tiredness   and   reduced   the   appetite   today  
EVAL: ✓      ✓    ✓     ✓          ✓     ✓           ✓     ✓       ✓      ✓    ✓     ✓    ✓           ✓     ✓         INS   ✓          ✓      
```

#### Gemini
- **Latency**: 3.66s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : none   of   the   symptoms   you   mentioned   are   there   just   a    bit   of   tiredness   and   reduced   appetite   today  
HYP : none   of   the   symptoms   you   mentioned   are   there   just   a    bit   of   tiredness   and   reduced   appetite   today  
EVAL: ✓      ✓    ✓     ✓          ✓     ✓           ✓     ✓       ✓      ✓    ✓     ✓    ✓           ✓     ✓         ✓          ✓      
```

---

### Voice: `v207.wav`
> **Ground Truth Reference**:
> *Yes; in the morning I had scrambled eggs with bread, for lunch I ate injera with meat stew and collard greens. Tonight, outside the regular meals, I had an extra glass of milk and a banana.*

#### Sahara
- **Latency**: 5.66s | **Ref Words**: 36 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 3.4%

```text
REF : yes   in   the   morning   i    had   scrambled   eggs   with   bread   for   lunch   i    ate   injera   with   meat   stew    and   collard   greens   tonight   outside   the   regular   meals   i    had   an   extra   glass   of   milk   and   a    banana  
HYP : yes   in   the   morning   i    had   scrambled   eggs   with   bread   for   lunch   i    ate   injera   with   ---    misti   and   collard   greens   tonight   outside   the   regular   meals   i    had   an   extra   glass   of   milk   and   a    banana  
EVAL: ✓     ✓    ✓     ✓         ✓    ✓     ✓           ✓      ✓      ✓       ✓     ✓       ✓    ✓     ✓        ✓      DEL    SUB     ✓     ✓         ✓        ✓         ✓         ✓     ✓         ✓       ✓    ✓     ✓    ✓       ✓       ✓    ✓      ✓     ✓    ✓       
```

#### Deepgram
- **Latency**: 3.93s | **Ref Words**: 36 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **2.8%** | **Word Accuracy**: **97.2%** | **CER**: 2.0%

```text
REF : yes   in   the   morning   i    had   scrambled   eggs   with   bread   for   lunch   i    ate   injera   with   meat   stew   and   collard   greens   tonight   outside   the   regular   meals   i    had   an   extra   glass   of   milk   and   a    banana  
HYP : yes   in   the   morning   i    had   scrambled   eggs   with   bread   for   lunch   i    ate   injera   with   meat   stew   and   color     greens   tonight   outside   the   regular   meals   i    had   an   extra   glass   of   milk   and   a    banana  
EVAL: ✓     ✓    ✓     ✓         ✓    ✓     ✓           ✓      ✓      ✓       ✓     ✓       ✓    ✓     ✓        ✓      ✓      ✓      ✓     SUB       ✓        ✓         ✓         ✓     ✓         ✓       ✓    ✓     ✓    ✓       ✓       ✓    ✓      ✓     ✓    ✓       
```

#### Gemini
- **Latency**: 4.73s | **Ref Words**: 36 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **2.8%** | **Word Accuracy**: **97.2%** | **CER**: 2.0%

```text
REF : yes   in   the   morning   i    had   scrambled   eggs   with   bread   for   lunch   i    ate   injera   with   meat   stew   and   collard   greens   tonight   outside   the   regular   meals   i    had   an   extra   glass   of   milk   and   a    banana  
HYP : yes   in   the   morning   i    had   scrambled   eggs   with   bread   for   lunch   i    ate   injera   with   meat   stew   and   colored   greens   tonight   outside   the   regular   meals   i    had   an   extra   glass   of   milk   and   a    banana  
EVAL: ✓     ✓    ✓     ✓         ✓    ✓     ✓           ✓      ✓      ✓       ✓     ✓       ✓    ✓     ✓        ✓      ✓      ✓      ✓     SUB       ✓        ✓         ✓         ✓     ✓         ✓       ✓    ✓     ✓    ✓       ✓       ✓    ✓      ✓     ✓    ✓       
```

---

### Voice: `v208.wav`
> **Ground Truth Reference**:
> *I ate well. During the day I had split lentil wot and salad, and for snack I took an extra boiled egg and avocado salad.*

#### Sahara
- **Latency**: 5.44s | **Ref Words**: 25 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **8.0%** | **Word Accuracy**: **92.0%** | **CER**: 2.1%

```text
REF : i    ate   well   during   the   day   i    had   split   lentil   wot   and   salad   and   for   ---   snack   i    took   an   extra   boiled   egg   and   avocado   salad  
HYP : i    ate   well   during   the   day   i    had   split   lentil   wet   and   salad   and   for   a     snack   i    took   an   extra   boiled   egg   and   avocado   salad  
EVAL: ✓    ✓     ✓      ✓        ✓     ✓     ✓    ✓     ✓       ✓        SUB   ✓     ✓       ✓     ✓     INS   ✓       ✓    ✓      ✓    ✓       ✓        ✓     ✓     ✓         ✓      
```

#### Deepgram
- **Latency**: 3.54s | **Ref Words**: 25 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.0%** | **Word Accuracy**: **96.0%** | **CER**: 2.1%

```text
REF : i    ate   well   during   the   day   i    had   split   lentil   wot    and   salad   and   for   snack   i    took   an   extra   boiled   egg   and   avocado   salad  
HYP : i    ate   well   during   the   day   i    had   split   lentil   with   and   salad   and   for   snack   i    took   an   extra   boiled   egg   and   avocado   salad  
EVAL: ✓    ✓     ✓      ✓        ✓     ✓     ✓    ✓     ✓       ✓        SUB    ✓     ✓       ✓     ✓     ✓       ✓    ✓      ✓    ✓       ✓        ✓     ✓     ✓         ✓      
```

#### Gemini
- **Latency**: 4.45s | **Ref Words**: 25 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.0%** | **Word Accuracy**: **96.0%** | **CER**: 3.2%

```text
REF : i    ate   well   during   the   day   i    had   split   lentil   wot    and   salad   and   for   snack   i    took   an   extra   boiled   egg   and   avocado   salad  
HYP : i    ate   well   during   the   day   i    had   split   lentil   wade   and   salad   and   for   snack   i    took   an   extra   boiled   egg   and   avocado   salad  
EVAL: ✓    ✓     ✓      ✓        ✓     ✓     ✓    ✓     ✓       ✓        SUB    ✓     ✓       ✓     ✓     ✓       ✓    ✓      ✓    ✓       ✓        ✓     ✓     ✓         ✓      
```

---

### Voice: `v209.wav`
> **Ground Truth Reference**:
> *Yes, I took an extra meal; after lunch in the afternoon genfo with spiced butter was prepared for me, and for fruit I ate orange and mango.*

#### Sahara
- **Latency**: 5.16s | **Ref Words**: 27 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **3.7%** | **Word Accuracy**: **96.3%** | **CER**: 1.8%

```text
REF : yes   i    took   an   extra   meal   after   lunch   in   the   afternoon   genfo   with   spiced   butter   was   prepared   for   me   and   for   fruit   i    ate   orange   and   mango  
HYP : yes   i    took   an   extra   meal   after   lunch   in   the   afternoon   gamfo   with   spiced   butter   was   prepared   for   me   and   for   fruit   i    ate   orange   and   mango  
EVAL: ✓     ✓    ✓      ✓    ✓       ✓      ✓       ✓       ✓    ✓     ✓           SUB     ✓      ✓        ✓        ✓     ✓          ✓     ✓    ✓     ✓     ✓       ✓    ✓     ✓        ✓     ✓      
```

#### Deepgram
- **Latency**: 4.4s | **Ref Words**: 27 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **7.4%** | **Word Accuracy**: **92.6%** | **CER**: 2.8%

```text
REF : yes   i    took   an   extra   meal   after   lunch   in   the   afternoon   genfo    with   spiced   butter   was   prepared   for   me   and   for   fruit    i    ate   orange   and   mango  
HYP : yes   i    took   an   extra   meal   after   lunch   in   the   afternoon   ganfou   with   spiced   butter   was   prepared   for   me   and   for   fruits   i    ate   orange   and   mango  
EVAL: ✓     ✓    ✓      ✓    ✓       ✓      ✓       ✓       ✓    ✓     ✓           SUB      ✓      ✓        ✓        ✓     ✓          ✓     ✓    ✓     ✓     SUB      ✓    ✓     ✓        ✓     ✓      
```

#### Gemini
- **Latency**: 4.92s | **Ref Words**: 27 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 7.3%

```text
REF : yes   i    took   an   extra   meal   after   lunch   in   the   afternoon   genfo    with   spiced   butter   was   prepared   for   me   and   for   fruit    i    ate   orange   and   mango  
HYP : yes   i    took   an   extra   meal   after   lunch   in   the   afternoon   gimbap   with   spicy    butter   was   prepared   for   me   and   for   fruits   i    ate   orange   and   mango  
EVAL: ✓     ✓    ✓      ✓    ✓       ✓      ✓       ✓       ✓    ✓     ✓           SUB      ✓      SUB      ✓        ✓     ✓          ✓     ✓    ✓     ✓     SUB      ✓    ✓     ✓        ✓     ✓      
```

---
