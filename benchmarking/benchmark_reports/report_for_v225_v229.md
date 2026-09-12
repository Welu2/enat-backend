# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v225_v229_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 10:09:52 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 113 | 5 | 3 | 1 | 1 | **4.4%** | **95.6%** | 1.5% | 7.03s |
| **Deepgram** | 113 | 5 | 3 | 2 | 0 | **4.4%** | **95.6%** | 2.4% | 4.16s |
| **Gemini** | 113 | 6 | 3 | 2 | 1 | **5.3%** | **94.7%** | 2.9% | 5.07s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v225.wav`
> **Ground Truth Reference**:
> *Yes, I took a perfectly balanced meal; for lunch I ate injera with lentils and spinach, then in the afternoon I had boiled egg and flu-fruit as a snack.*

#### Sahara
- **Latency**: 6.22s | **Ref Words**: 30 | **Errors**: 5 (S: 3, D: 1, I: 1)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 5.9%

```text
REF : yes   i    took   a    perfectly   balanced   meal   for   lunch   i    ate   injera    with   lentils   and   spinach   then   in   the   afternoon   i    had   ---   boiled   egg   and   flu     fruit   as    a     snack  
HYP : yes   i    took   a    perfectly   balanced   meal   for   lunch   i    ate   sinjara   with   lentils   and   spinach   then   in   the   afternoon   i    had   a     boiled   egg   and   fluid   fruit   ---   and   snack  
EVAL: ✓     ✓    ✓      ✓    ✓           ✓          ✓      ✓     ✓       ✓    ✓     SUB       ✓      ✓         ✓     ✓         ✓      ✓    ✓     ✓           ✓    ✓     INS   ✓        ✓     ✓     SUB     ✓       DEL   SUB   ✓      
```

#### Deepgram
- **Latency**: 3.97s | **Ref Words**: 30 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **6.7%** | **Word Accuracy**: **93.3%** | **CER**: 3.4%

```text
REF : yes   i    took   a    perfectly   balanced   meal   for   lunch   i    ate   injera   with   lentils   and   spinach   then   in   the   afternoon   i    had   boiled   egg   and   flu    fruit   as   a     snack  
HYP : yes   i    took   a    perfectly   balanced   meal   for   lunch   i    ate   injera   with   lentils   and   spinach   then   in   the   afternoon   i    had   boiled   egg   and   food   fruit   as   ---   snack  
EVAL: ✓     ✓    ✓      ✓    ✓           ✓          ✓      ✓     ✓       ✓    ✓     ✓        ✓      ✓         ✓     ✓         ✓      ✓    ✓     ✓           ✓    ✓     ✓        ✓     ✓     SUB    ✓       ✓    DEL   ✓      
```

#### Gemini
- **Latency**: 7.29s | **Ref Words**: 30 | **Errors**: 4 (S: 1, D: 2, I: 1)
- **WER**: **13.3%** | **Word Accuracy**: **86.7%** | **CER**: 7.6%

```text
REF : yes   i    took   a    perfectly   balanced   meal   for   lunch   i    ate   ---    injera   with   lentils   and   spinach   then   in   the   afternoon   i    had   boiled   egg   and   flu   fruit   as   a     snack  
HYP : yes   i    took   a    perfectly   balanced   meal   for   lunch   i    ate   some   jar      with   lentils   and   spinach   then   in   the   afternoon   i    had   boiled   egg   and   ---   fruit   as   ---   snack  
EVAL: ✓     ✓    ✓      ✓    ✓           ✓          ✓      ✓     ✓       ✓    ✓     INS    SUB      ✓      ✓         ✓     ✓         ✓      ✓    ✓     ✓           ✓    ✓     ✓        ✓     ✓     DEL   ✓       ✓    DEL   ✓      
```

---

### Voice: `v226.wav`
> **Ground Truth Reference**:
> *No, actually I don't have an appetite; in the morning I just tasted toast and tea, I didn't take any extra meal.*

#### Sahara
- **Latency**: 6.93s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   actually   i    dont   have   an   appetite   in   the   morning   i    just   tasted   toast   and   tea   i    didnt   take   any   extra   meal  
HYP : no   actually   i    dont   have   an   appetite   in   the   morning   i    just   tasted   toast   and   tea   i    didnt   take   any   extra   meal  
EVAL: ✓    ✓          ✓    ✓      ✓      ✓    ✓          ✓    ✓     ✓         ✓    ✓      ✓        ✓       ✓     ✓     ✓    ✓       ✓      ✓     ✓       ✓     
```

#### Deepgram
- **Latency**: 4.71s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   actually   i    dont   have   an   appetite   in   the   morning   i    just   tasted   toast   and   tea   i    didnt   take   any   extra   meal  
HYP : no   actually   i    dont   have   an   appetite   in   the   morning   i    just   tasted   toast   and   tea   i    didnt   take   any   extra   meal  
EVAL: ✓    ✓          ✓    ✓      ✓      ✓    ✓          ✓    ✓     ✓         ✓    ✓      ✓        ✓       ✓     ✓     ✓    ✓       ✓      ✓     ✓       ✓     
```

#### Gemini
- **Latency**: 4.3s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   actually   i    dont   have   an   appetite   in   the   morning   i    just   tasted   toast   and   tea   i    didnt   take   any   extra   meal  
HYP : no   actually   i    dont   have   an   appetite   in   the   morning   i    just   tasted   toast   and   tea   i    didnt   take   any   extra   meal  
EVAL: ✓    ✓          ✓    ✓      ✓      ✓    ✓          ✓    ✓     ✓         ✓    ✓      ✓        ✓       ✓     ✓     ✓    ✓       ✓      ✓     ✓       ✓     
```

---

### Voice: `v227.wav`
> **Ground Truth Reference**:
> *Yes, I took an extra snack; I drank an avocado smoothie with milk, and for lunch I ate chicken stew.*

#### Sahara
- **Latency**: 6.3s | **Ref Words**: 20 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   an   extra   snack   i    drank   an   avocado   smoothie   with   milk   and   for   lunch   i    ate   chicken   stew  
HYP : yes   i    took   an   extra   snack   i    drank   an   avocado   smoothie   with   milk   and   for   lunch   i    ate   chicken   stew  
EVAL: ✓     ✓    ✓      ✓    ✓       ✓       ✓    ✓       ✓    ✓         ✓          ✓      ✓      ✓     ✓     ✓       ✓    ✓     ✓         ✓     
```

#### Deepgram
- **Latency**: 4.3s | **Ref Words**: 20 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   an   extra   snack   i    drank   an   avocado   smoothie   with   milk   and   for   lunch   i    ate   chicken   stew  
HYP : yes   i    took   an   extra   snack   i    drank   an   avocado   smoothie   with   milk   and   for   lunch   i    ate   chicken   stew  
EVAL: ✓     ✓    ✓      ✓    ✓       ✓       ✓    ✓       ✓    ✓         ✓          ✓      ✓      ✓     ✓     ✓       ✓    ✓     ✓         ✓     
```

#### Gemini
- **Latency**: 4.19s | **Ref Words**: 20 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   an   extra   snack   i    drank   an   avocado   smoothie   with   milk   and   for   lunch   i    ate   chicken   stew  
HYP : yes   i    took   an   extra   snack   i    drank   an   avocado   smoothie   with   milk   and   for   lunch   i    ate   chicken   stew  
EVAL: ✓     ✓    ✓      ✓    ✓       ✓       ✓    ✓       ✓    ✓         ✓          ✓      ✓      ✓     ✓     ✓       ✓    ✓     ✓         ✓     
```

---

### Voice: `v228.wav`
> **Ground Truth Reference**:
> *I only ate heavy carbs; rice and pasta, I didn't get fruits or vegetables, so it's not balanced.*

#### Sahara
- **Latency**: 9.08s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    only   ate   heavy   carbs   rice   and   pasta   i    didnt   get   fruits   or   vegetables   so   its   not   balanced  
HYP : i    only   ate   heavy   carbs   rice   and   pasta   i    didnt   get   fruits   or   vegetables   so   its   not   balanced  
EVAL: ✓    ✓      ✓     ✓       ✓       ✓      ✓     ✓       ✓    ✓       ✓     ✓        ✓    ✓            ✓    ✓     ✓     ✓         
```

#### Deepgram
- **Latency**: 4.31s | **Ref Words**: 18 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 2.7%

```text
REF : i    only   ate   heavy   carbs   rice   and   pasta   i    didnt   get   fruits   or   vegetables   so   its   not   balanced  
HYP : i    only   ate   heavy   carbs   rice   and   pasta   i    didnt   eat   fruits   or   vegetables   so   its   not   balanced  
EVAL: ✓    ✓      ✓     ✓       ✓       ✓      ✓     ✓       ✓    ✓       SUB   ✓        ✓    ✓            ✓    ✓     ✓     ✓         
```

#### Gemini
- **Latency**: 4.7s | **Ref Words**: 18 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 5.5%

```text
REF : i    only   ate   heavy   carbs   rice   and   pasta   i    didnt   get   fruits   or   vegetables   so   its   not   balanced  
HYP : i    only   eat   heavy   carbs   rice   and   pasta   i    didnt   eat   fruits   or   vegetables   so   its   not   balanced  
EVAL: ✓    ✓      SUB   ✓       ✓       ✓      ✓     ✓       ✓    ✓       SUB   ✓        ✓    ✓            ✓    ✓     ✓     ✓         
```

---

### Voice: `v229.wav`
> **Ground Truth Reference**:
> *Thinking of getting iron and vitamins I drank orange juice; but because I have severe nausea I couldn't eat a heavy extra meal.*

#### Sahara
- **Latency**: 6.62s | **Ref Words**: 23 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : thinking   of   getting   iron   and   vitamins   i    drank   orange   juice   but   because   i    have   severe   nausea   i    couldnt   eat   a    heavy   extra   meal  
HYP : thinking   of   getting   iron   and   vitamins   i    drank   orange   juice   but   because   i    have   severe   nausea   i    couldnt   eat   a    heavy   extra   meal  
EVAL: ✓          ✓    ✓         ✓      ✓     ✓          ✓    ✓       ✓        ✓       ✓     ✓         ✓    ✓      ✓        ✓        ✓    ✓         ✓     ✓    ✓       ✓       ✓     
```

#### Deepgram
- **Latency**: 3.53s | **Ref Words**: 23 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **8.7%** | **Word Accuracy**: **91.3%** | **CER**: 4.9%

```text
REF : thinking   of   getting   iron   and   vitamins   i    drank   orange   juice     but   because   i    have   severe   nausea   i    couldnt   eat   a    heavy   extra   meal  
HYP : thinking   of   getting   iron   and   vitamins   i    drank   ---      oranges   but   because   i    have   severe   nausea   i    couldnt   eat   a    heavy   extra   meal  
EVAL: ✓          ✓    ✓         ✓      ✓     ✓          ✓    ✓       DEL      SUB       ✓     ✓         ✓    ✓      ✓        ✓        ✓    ✓         ✓     ✓    ✓       ✓       ✓     
```

#### Gemini
- **Latency**: 4.85s | **Ref Words**: 23 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : thinking   of   getting   iron   and   vitamins   i    drank   orange   juice   but   because   i    have   severe   nausea   i    couldnt   eat   a    heavy   extra   meal  
HYP : thinking   of   getting   iron   and   vitamins   i    drank   orange   juice   but   because   i    have   severe   nausea   i    couldnt   eat   a    heavy   extra   meal  
EVAL: ✓          ✓    ✓         ✓      ✓     ✓          ✓    ✓       ✓        ✓       ✓     ✓         ✓    ✓      ✓        ✓        ✓    ✓         ✓     ✓    ✓       ✓       ✓     
```

---
