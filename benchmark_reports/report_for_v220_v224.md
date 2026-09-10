# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v220_v224_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 10:02:47 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 100 | 11 | 8 | 2 | 1 | **11.0%** | **89.0%** | 4.3% | 5.26s |
| **Deepgram** | 100 | 6 | 2 | 3 | 1 | **6.0%** | **94.0%** | 3.3% | 4.28s |
| **Gemini** | 100 | 10 | 8 | 2 | 0 | **10.0%** | **90.0%** | 6.7% | 3.92s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v220.wav`
> **Ground Truth Reference**:
> *Because the smell of food makes me vomit I haven't eaten anything; I spent today fasting.*

#### Sahara
- **Latency**: 4.75s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : because   the   smell   of   food   makes   me   vomit   i    havent   eaten   anything   i    spent   today   fasting  
HYP : because   the   smell   of   food   makes   me   vomit   i    havent   eaten   anything   i    spent   today   fasting  
EVAL: ✓         ✓     ✓       ✓    ✓      ✓       ✓    ✓       ✓    ✓        ✓       ✓          ✓    ✓       ✓       ✓        
```

#### Deepgram
- **Latency**: 3.71s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : because   the   smell   of   food   makes   me   vomit   i    havent   eaten   anything   i    spent   today   fasting  
HYP : because   the   smell   of   food   makes   me   vomit   i    havent   eaten   anything   i    spent   today   fasting  
EVAL: ✓         ✓     ✓       ✓    ✓      ✓       ✓    ✓       ✓    ✓        ✓       ✓          ✓    ✓       ✓       ✓        
```

#### Gemini
- **Latency**: 3.11s | **Ref Words**: 16 | **Errors**: 1 (S: 0, D: 1, I: 0)
- **WER**: **6.2%** | **Word Accuracy**: **93.8%** | **CER**: 2.8%

```text
REF : because   the   smell   of    food   makes   me   vomit   i    havent   eaten   anything   i    spent   today   fasting  
HYP : because   the   smell   ---   food   makes   me   vomit   i    havent   eaten   anything   i    spent   today   fasting  
EVAL: ✓         ✓     ✓       DEL   ✓      ✓       ✓    ✓       ✓    ✓        ✓       ✓          ✓    ✓       ✓       ✓        
```

---

### Voice: `v221.wav`
> **Ground Truth Reference**:
> *Yes; in the morning I drank plenty of barley atmit, and for lunch barley and wheat qitta with spiced butter was served for me; to give me strength.*

#### Sahara
- **Latency**: 5.3s | **Ref Words**: 28 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **10.7%** | **Word Accuracy**: **89.3%** | **CER**: 3.5%

```text
REF : yes   in   the   morning   i    drank   plenty   of   barley   atmit   and   for   lunch   barley   and   wheat   qitta   with   spiced   butter   was   served   for   me   to   give   me   strength  
HYP : yes   in   the   morning   i    drank   plenty   of   barley   admit   and   for   lunch   barley   and   wheat   kita    with   spiced   batter   was   served   for   me   to   give   me   strength  
EVAL: ✓     ✓    ✓     ✓         ✓    ✓       ✓        ✓    ✓        SUB     ✓     ✓     ✓       ✓        ✓     ✓       SUB     ✓      ✓        SUB      ✓     ✓        ✓     ✓    ✓    ✓      ✓    ✓         
```

#### Deepgram
- **Latency**: 5.94s | **Ref Words**: 28 | **Errors**: 3 (S: 1, D: 1, I: 1)
- **WER**: **10.7%** | **Word Accuracy**: **89.3%** | **CER**: 6.9%

```text
REF : yes   in   the   morning   i    drank   plenty   of   barley   ---   atmit   and   for   lunch   barley   and   wheat   qitta   with   spiced   butter   was   served   for   me   to   give   me   strength  
HYP : yes   in   the   morning   i    drank   plenty   of   barley   ad    meat    and   for   lunch   barley   and   wheat   ---     with   spiced   butter   was   served   for   me   to   give   me   strength  
EVAL: ✓     ✓    ✓     ✓         ✓    ✓       ✓        ✓    ✓        INS   SUB     ✓     ✓     ✓       ✓        ✓     ✓       DEL     ✓      ✓        ✓        ✓     ✓        ✓     ✓    ✓    ✓      ✓    ✓         
```

#### Gemini
- **Latency**: 4.71s | **Ref Words**: 28 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **7.1%** | **Word Accuracy**: **92.9%** | **CER**: 6.0%

```text
REF : yes   in   the   morning   i    drank   plenty   of   barley   atmit     and   for   lunch   barley   and   wheat   qitta   with   spiced   butter   was   served   for   me   to   give   me   strength  
HYP : yes   in   the   morning   i    drank   plenty   of   barley   oatmeal   and   for   lunch   barley   and   wheat   kicha   with   spiced   butter   was   served   for   me   to   give   me   strength  
EVAL: ✓     ✓    ✓     ✓         ✓    ✓       ✓        ✓    ✓        SUB       ✓     ✓     ✓       ✓        ✓     ✓       SUB     ✓      ✓        ✓        ✓     ✓        ✓     ✓    ✓    ✓      ✓    ✓         
```

---

### Voice: `v222.wav`
> **Ground Truth Reference**:
> *I took beso and sesame genfo; because I was told it's good for the baby's growth, I am taking extra food properly.*

#### Sahara
- **Latency**: 6.02s | **Ref Words**: 22 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 5.7%

```text
REF : i    took   beso     and   sesame   genfo   because   i    was   told   its   good   for   the   babys   growth   i     am    taking   extra   food   properly  
HYP : i    took   bessel   and   sesame   ganfo   because   i    was   told   its   good   for   the   babys   growth   ---   im    taking   extra   food   properly  
EVAL: ✓    ✓      SUB      ✓     ✓        SUB     ✓         ✓    ✓     ✓      ✓     ✓      ✓     ✓     ✓       ✓        DEL   SUB   ✓        ✓       ✓      ✓         
```

#### Deepgram
- **Latency**: 4.65s | **Ref Words**: 22 | **Errors**: 3 (S: 1, D: 2, I: 0)
- **WER**: **13.6%** | **Word Accuracy**: **86.4%** | **CER**: 6.8%

```text
REF : i    took   beso   and   sesame   genfo     because   i    was   told   its   good   for   the   babys   growth   i     am    taking   extra   food   properly  
HYP : i    took   beso   and   sesame   ganfold   because   i    was   told   its   good   for   the   babys   growth   ---   ---   taking   extra   food   properly  
EVAL: ✓    ✓      ✓      ✓     ✓        SUB       ✓         ✓    ✓     ✓      ✓     ✓      ✓     ✓     ✓       ✓        DEL   DEL   ✓        ✓       ✓      ✓         
```

#### Gemini
- **Latency**: 4.19s | **Ref Words**: 22 | **Errors**: 5 (S: 4, D: 1, I: 0)
- **WER**: **22.7%** | **Word Accuracy**: **77.3%** | **CER**: 12.5%

```text
REF : i    took   beso   and   sesame     genfo   because   i    was   told   its   good   for   the   babys   growth   i     am    taking    extra   food   properly  
HYP : i    took   beso   and   sasmegan   4       because   i    was   told   its   good   for   the   babys   growth   ---   and   picking   extra   food   properly  
EVAL: ✓    ✓      ✓      ✓     SUB        SUB     ✓         ✓    ✓     ✓      ✓     ✓      ✓     ✓     ✓       ✓        DEL   SUB   SUB       ✓       ✓      ✓         
```

---

### Voice: `v223.wav`
> **Ground Truth Reference**:
> *I ate injera with meat stew; and for snack I drank roasted flaxseed mixed with water.*

#### Sahara
- **Latency**: 5.31s | **Ref Words**: 16 | **Errors**: 4 (S: 2, D: 1, I: 1)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 13.2%

```text
REF : i    ate   ---   injera    with   meat   stew       and   for   snack   i    drank   roasted   flaxseed   mixed   with   water  
HYP : i    ate   in    general   with   ---    midsteel   and   for   snack   i    drank   roasted   flaxseed   mixed   with   water  
EVAL: ✓    ✓     INS   SUB       ✓      DEL    SUB        ✓     ✓     ✓       ✓    ✓       ✓         ✓          ✓       ✓      ✓      
```

#### Deepgram
- **Latency**: 3.76s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    ate   injera   with   meat   stew   and   for   snack   i    drank   roasted   flaxseed   mixed   with   water  
HYP : i    ate   injera   with   meat   stew   and   for   snack   i    drank   roasted   flaxseed   mixed   with   water  
EVAL: ✓    ✓     ✓        ✓      ✓      ✓      ✓     ✓     ✓       ✓    ✓       ✓         ✓          ✓       ✓      ✓      
```

#### Gemini
- **Latency**: 4.03s | **Ref Words**: 16 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 11.8%

```text
REF : i    ate   injera   with   meat   stew   and   for   snack   i    drank   roasted   flaxseed   mixed   with   water  
HYP : i    ate   cereal   with   milk   stew   and   for   snack   i    drank   roasted   flaxseed   mixed   with   water  
EVAL: ✓    ✓     SUB      ✓      SUB    ✓      ✓     ✓     ✓       ✓    ✓       ✓         ✓          ✓       ✓      ✓      
```

---

### Voice: `v224.wav`
> **Ground Truth Reference**:
> *Yes; I took roasted chickpea snack and milk properly, and to make it balanced I added an orange.*

#### Sahara
- **Latency**: 4.9s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   roasted   chickpea   snack   and   milk   properly   and   to   make   it   balanced   i    added   an   orange  
HYP : yes   i    took   roasted   chickpea   snack   and   milk   properly   and   to   make   it   balanced   i    added   an   orange  
EVAL: ✓     ✓    ✓      ✓         ✓          ✓       ✓     ✓      ✓          ✓     ✓    ✓      ✓    ✓          ✓    ✓       ✓    ✓       
```

#### Deepgram
- **Latency**: 3.33s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   roasted   chickpea   snack   and   milk   properly   and   to   make   it   balanced   i    added   an   orange  
HYP : yes   i    took   roasted   chickpea   snack   and   milk   properly   and   to   make   it   balanced   i    added   an   orange  
EVAL: ✓     ✓    ✓      ✓         ✓          ✓       ✓     ✓      ✓          ✓     ✓    ✓      ✓    ✓          ✓    ✓       ✓    ✓       
```

#### Gemini
- **Latency**: 3.58s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   roasted   chickpea   snack   and   milk   properly   and   to   make   it   balanced   i    added   an   orange  
HYP : yes   i    took   roasted   chickpea   snack   and   milk   properly   and   to   make   it   balanced   i    added   an   orange  
EVAL: ✓     ✓    ✓      ✓         ✓          ✓       ✓     ✓      ✓          ✓     ✓    ✓      ✓    ✓          ✓    ✓       ✓    ✓       
```

---
