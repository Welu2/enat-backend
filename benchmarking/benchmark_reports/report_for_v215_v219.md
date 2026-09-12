# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v215_v219_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 10:02:39 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 106 | 5 | 4 | 1 | 0 | **4.7%** | **95.3%** | 2.6% | 4.91s |
| **Deepgram** | 106 | 4 | 3 | 1 | 0 | **3.8%** | **96.2%** | 3.0% | 3.55s |
| **Gemini** | 106 | 5 | 3 | 1 | 1 | **4.7%** | **95.3%** | 2.3% | 3.93s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v215.wav`
> **Ground Truth Reference**:
> *I didn't eat extra; I had tea and qitta in the morning and now for lunch I just ate a little rice.*

#### Sahara
- **Latency**: 4.49s | **Ref Words**: 22 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.5%** | **Word Accuracy**: **95.5%** | **CER**: 2.7%

```text
REF : i    didnt   eat   extra   i    had   tea   and   qitta   in   the   morning   and   now   for   lunch   i    just   ate   a    little   rice  
HYP : i    didnt   eat   extra   i    had   tea   and   kita    in   the   morning   and   now   for   lunch   i    just   ate   a    little   rice  
EVAL: ✓    ✓       ✓     ✓       ✓    ✓     ✓     ✓     SUB     ✓    ✓     ✓         ✓     ✓     ✓     ✓       ✓    ✓      ✓     ✓    ✓        ✓     
```

#### Deepgram
- **Latency**: 3.9s | **Ref Words**: 22 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.5%** | **Word Accuracy**: **95.5%** | **CER**: 5.4%

```text
REF : i    didnt   eat   extra   i    had   tea   and   qitta   in   the   morning   and   now   for   lunch   i    just   ate   a    little   rice  
HYP : i    didnt   eat   extra   i    had   tea   and   eat     in   the   morning   and   now   for   lunch   i    just   ate   a    little   rice  
EVAL: ✓    ✓       ✓     ✓       ✓    ✓     ✓     ✓     SUB     ✓    ✓     ✓         ✓     ✓     ✓     ✓       ✓    ✓      ✓     ✓    ✓        ✓     
```

#### Gemini
- **Latency**: 3.89s | **Ref Words**: 22 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 5.4%

```text
REF : i    didnt   eat   extra   i    had   tea   and   ---   qitta   in   the   morning   and   now   for   lunch   i    just   ate   a    little   rice  
HYP : i    didnt   eat   extra   i    had   tea   and   eat   uh      in   the   morning   and   now   for   lunch   i    just   ate   a    little   rice  
EVAL: ✓    ✓       ✓     ✓       ✓    ✓     ✓     ✓     INS   SUB     ✓    ✓     ✓         ✓     ✓     ✓     ✓       ✓    ✓      ✓     ✓    ✓        ✓     
```

---

### Voice: `v216.wav`
> **Ground Truth Reference**:
> *Because there wasn't even enough food at home I only ate once; I couldn't get an extra meat.*

#### Sahara
- **Latency**: 4.98s | **Ref Words**: 18 | **Errors**: 1 (S: 0, D: 1, I: 0)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 5.6%

```text
REF : because   there   wasnt   even   enough   food   at   home   i    only   ate   once   i    couldnt   get   an   extra   meat  
HYP : because   there   wasnt   ---    enough   food   at   home   i    only   ate   once   i    couldnt   get   an   extra   meat  
EVAL: ✓         ✓       ✓       DEL    ✓        ✓      ✓    ✓      ✓    ✓      ✓     ✓      ✓    ✓         ✓     ✓    ✓       ✓     
```

#### Deepgram
- **Latency**: 3.73s | **Ref Words**: 18 | **Errors**: 1 (S: 0, D: 1, I: 0)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 5.6%

```text
REF : because   there   wasnt   even   enough   food   at   home   i    only   ate   once   i    couldnt   get   an   extra   meat  
HYP : because   there   wasnt   ---    enough   food   at   home   i    only   ate   once   i    couldnt   get   an   extra   meat  
EVAL: ✓         ✓       ✓       DEL    ✓        ✓      ✓    ✓      ✓    ✓      ✓     ✓      ✓    ✓         ✓     ✓    ✓       ✓     
```

#### Gemini
- **Latency**: 3.85s | **Ref Words**: 18 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 7.0%

```text
REF : because   there   wasnt   even   enough   food   at   home   i    only   ate   once   i    couldnt   get   an   extra   meat   
HYP : because   there   wasnt   ---    enough   food   at   home   i    only   ate   once   i    couldnt   get   an   extra   meats  
EVAL: ✓         ✓       ✓       DEL    ✓        ✓      ✓    ✓      ✓    ✓      ✓     ✓      ✓    ✓         ✓     ✓    ✓       SUB    
```

---

### Voice: `v217.wav`
> **Ground Truth Reference**:
> *I couldn't eat; because the nausea wouldn't stop, all I ate was a little tea and biscuit, I couldn't take an extra meal.*

#### Sahara
- **Latency**: 5.26s | **Ref Words**: 23 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.3%** | **Word Accuracy**: **95.7%** | **CER**: 1.1%

```text
REF : i    couldnt   eat   because   the   nausea   wouldnt   stop   all   i    ate   was   a    little   tea   and   biscuit    i    couldnt   take   an   extra   meal  
HYP : i    couldnt   eat   because   the   nausea   wouldnt   stop   all   i    ate   was   a    little   tea   and   biscuits   i    couldnt   take   an   extra   meal  
EVAL: ✓    ✓         ✓     ✓         ✓     ✓        ✓         ✓      ✓     ✓    ✓     ✓     ✓    ✓        ✓     ✓     SUB        ✓    ✓         ✓      ✓    ✓       ✓     
```

#### Deepgram
- **Latency**: 4.0s | **Ref Words**: 23 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.3%** | **Word Accuracy**: **95.7%** | **CER**: 1.1%

```text
REF : i    couldnt   eat   because   the   nausea   wouldnt   stop   all   i    ate   was   a    little   tea   and   biscuit    i    couldnt   take   an   extra   meal  
HYP : i    couldnt   eat   because   the   nausea   wouldnt   stop   all   i    ate   was   a    little   tea   and   biscuits   i    couldnt   take   an   extra   meal  
EVAL: ✓    ✓         ✓     ✓         ✓     ✓        ✓         ✓      ✓     ✓    ✓     ✓     ✓    ✓        ✓     ✓     SUB        ✓    ✓         ✓      ✓    ✓       ✓     
```

#### Gemini
- **Latency**: 4.19s | **Ref Words**: 23 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.3%** | **Word Accuracy**: **95.7%** | **CER**: 1.1%

```text
REF : i    couldnt   eat   because   the   nausea   wouldnt   stop   all   i    ate   was   a    little   tea   and   biscuit    i    couldnt   take   an   extra   meal  
HYP : i    couldnt   eat   because   the   nausea   wouldnt   stop   all   i    ate   was   a    little   tea   and   biscuits   i    couldnt   take   an   extra   meal  
EVAL: ✓    ✓         ✓     ✓         ✓     ✓        ✓         ✓      ✓     ✓    ✓     ✓     ✓    ✓        ✓     ✓     SUB        ✓    ✓         ✓      ✓    ✓       ✓     
```

---

### Voice: `v218.wav`
> **Ground Truth Reference**:
> *Because heartburn was burning my chest I didn't take any food; I couldn't even hold down water, where would an extra meal come from?*

#### Sahara
- **Latency**: 5.06s | **Ref Words**: 24 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : because   heartburn   was   burning   my   chest   i    didnt   take   any   food   i    couldnt   even   hold   down   water   where   would   an   extra   meal   come   from  
HYP : because   heartburn   was   burning   my   chest   i    didnt   take   any   food   i    couldnt   even   hold   down   water   where   would   an   extra   meal   come   from  
EVAL: ✓         ✓           ✓     ✓         ✓    ✓       ✓    ✓       ✓      ✓     ✓      ✓    ✓         ✓      ✓      ✓      ✓       ✓       ✓       ✓    ✓       ✓      ✓      ✓     
```

#### Deepgram
- **Latency**: 3.17s | **Ref Words**: 24 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.2%** | **Word Accuracy**: **95.8%** | **CER**: 3.9%

```text
REF : because   heartburn   was   burning   my   chest   i    didnt   take   any   food   i    couldnt   even   hold   down   water   where   would   an   extra   meal   come   from  
HYP : because   heartburn   was   burning   my   chest   i    didnt   take   any   food   i    couldnt   even   hold   the    water   where   would   an   extra   meal   come   from  
EVAL: ✓         ✓           ✓     ✓         ✓    ✓       ✓    ✓       ✓      ✓     ✓      ✓    ✓         ✓      ✓      SUB    ✓       ✓       ✓       ✓    ✓       ✓      ✓      ✓     
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 24 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : because   heartburn   was   burning   my   chest   i    didnt   take   any   food   i    couldnt   even   hold   down   water   where   would   an   extra   meal   come   from  
HYP : because   heartburn   was   burning   my   chest   i    didnt   take   any   food   i    couldnt   even   hold   down   water   where   would   an   extra   meal   come   from  
EVAL: ✓         ✓           ✓     ✓         ✓    ✓       ✓    ✓       ✓      ✓     ✓      ✓    ✓         ✓      ✓      ✓      ✓       ✓       ✓       ✓    ✓       ✓      ✓      ✓     
```

---

### Voice: `v219.wav`
> **Ground Truth Reference**:
> *My appetite is completely blocked; in the morning I forced down one banana, but my stomach won't accept food.*

#### Sahara
- **Latency**: 4.75s | **Ref Words**: 19 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **10.5%** | **Word Accuracy**: **89.5%** | **CER**: 4.6%

```text
REF : my   appetite   is   completely   blocked   in   the   morning   i    forced   down   one   banana   but   my   stomach   wont   accept   food  
HYP : my   appetite   is   completely   blocked   in   the   morning   i    force    down   1     banana   but   my   stomach   wont   accept   food  
EVAL: ✓    ✓          ✓    ✓            ✓         ✓    ✓     ✓         ✓    SUB      ✓      SUB   ✓        ✓     ✓    ✓         ✓      ✓        ✓     
```

#### Deepgram
- **Latency**: 2.94s | **Ref Words**: 19 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   appetite   is   completely   blocked   in   the   morning   i    forced   down   one   banana   but   my   stomach   wont   accept   food  
HYP : my   appetite   is   completely   blocked   in   the   morning   i    forced   down   one   banana   but   my   stomach   wont   accept   food  
EVAL: ✓    ✓          ✓    ✓            ✓         ✓    ✓     ✓         ✓    ✓        ✓      ✓     ✓        ✓     ✓    ✓         ✓      ✓        ✓     
```

#### Gemini
- **Latency**: 4.04s | **Ref Words**: 19 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   appetite   is   completely   blocked   in   the   morning   i    forced   down   one   banana   but   my   stomach   wont   accept   food  
HYP : my   appetite   is   completely   blocked   in   the   morning   i    forced   down   one   banana   but   my   stomach   wont   accept   food  
EVAL: ✓    ✓          ✓    ✓            ✓         ✓    ✓     ✓         ✓    ✓        ✓      ✓     ✓        ✓     ✓    ✓         ✓      ✓        ✓     
```

---
