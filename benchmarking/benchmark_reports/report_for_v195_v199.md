# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v195_v199_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 10:00:26 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 103 | 3 | 3 | 0 | 0 | **2.9%** | **97.1%** | 1.5% | 5.00s |
| **Deepgram** | 103 | 1 | 1 | 0 | 0 | **1.0%** | **99.0%** | 0.2% | 3.81s |
| **Gemini** | 103 | 2 | 2 | 0 | 0 | **1.9%** | **98.1%** | 0.5% | 3.96s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v195.wav`
> **Ground Truth Reference**:
> *As the weight of my belly increases, my hips and lower back feel weary; but when I lie down it gets better.*

#### Sahara
- **Latency**: 5.39s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : as   the   weight   of   my   belly   increases   my   hips   and   lower   back   feel   weary   but   when   i    lie   down   it   gets   better  
HYP : as   the   weight   of   my   belly   increases   my   hips   and   lower   back   feel   weary   but   when   i    lie   down   it   gets   better  
EVAL: ✓    ✓     ✓        ✓    ✓    ✓       ✓           ✓    ✓      ✓     ✓       ✓      ✓      ✓       ✓     ✓      ✓    ✓     ✓      ✓    ✓      ✓       
```

#### Deepgram
- **Latency**: 4.01s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : as   the   weight   of   my   belly   increases   my   hips   and   lower   back   feel   weary   but   when   i    lie   down   it   gets   better  
HYP : as   the   weight   of   my   belly   increases   my   hips   and   lower   back   feel   weary   but   when   i    lie   down   it   gets   better  
EVAL: ✓    ✓     ✓        ✓    ✓    ✓       ✓           ✓    ✓      ✓     ✓       ✓      ✓      ✓       ✓     ✓      ✓    ✓     ✓      ✓    ✓      ✓       
```

#### Gemini
- **Latency**: 3.99s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : as   the   weight   of   my   belly   increases   my   hips   and   lower   back   feel   weary   but   when   i    lie   down   it   gets   better  
HYP : as   the   weight   of   my   belly   increases   my   hips   and   lower   back   feel   weary   but   when   i    lie   down   it   gets   better  
EVAL: ✓    ✓     ✓        ✓    ✓    ✓       ✓           ✓    ✓      ✓     ✓       ✓      ✓      ✓       ✓     ✓      ✓    ✓     ✓      ✓    ✓      ✓       
```

---

### Voice: `v196.wav`
> **Ground Truth Reference**:
> *At night my calves cramp or stiffen; but during the day I feel no pain.*

#### Sahara
- **Latency**: 4.48s | **Ref Words**: 15 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **6.7%** | **Word Accuracy**: **93.3%** | **CER**: 7.3%

```text
REF : at   night   my   calves   cramp   or   stiffen   but   during   the   day   i    feel   no   pain  
HYP : at   night   my   cuffs    cramp   or   stiffen   but   during   the   day   i    feel   no   pain  
EVAL: ✓    ✓       ✓    SUB      ✓       ✓    ✓         ✓     ✓        ✓     ✓     ✓    ✓      ✓    ✓     
```

#### Deepgram
- **Latency**: 3.78s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : at   night   my   calves   cramp   or   stiffen   but   during   the   day   i    feel   no   pain  
HYP : at   night   my   calves   cramp   or   stiffen   but   during   the   day   i    feel   no   pain  
EVAL: ✓    ✓       ✓    ✓        ✓       ✓    ✓         ✓     ✓        ✓     ✓     ✓    ✓      ✓    ✓     
```

#### Gemini
- **Latency**: 3.87s | **Ref Words**: 15 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **6.7%** | **Word Accuracy**: **93.3%** | **CER**: 1.8%

```text
REF : at   night    my   calves   cramp   or   stiffen   but   during   the   day   i    feel   no   pain  
HYP : at   nights   my   calves   cramp   or   stiffen   but   during   the   day   i    feel   no   pain  
EVAL: ✓    SUB      ✓    ✓        ✓       ✓    ✓         ✓     ✓        ✓     ✓     ✓    ✓      ✓    ✓     
```

---

### Voice: `v197.wav`
> **Ground Truth Reference**:
> *My hands and face are not swollen; because I stood for long hours my ankles are slightly puffy, but it goes away when I elevate my feet.*

#### Sahara
- **Latency**: 5.05s | **Ref Words**: 27 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   hands   and   face   are   not   swollen   because   i    stood   for   long   hours   my   ankles   are   slightly   puffy   but   it   goes   away   when   i    elevate   my   feet  
HYP : my   hands   and   face   are   not   swollen   because   i    stood   for   long   hours   my   ankles   are   slightly   puffy   but   it   goes   away   when   i    elevate   my   feet  
EVAL: ✓    ✓       ✓     ✓      ✓     ✓     ✓         ✓         ✓    ✓       ✓     ✓      ✓       ✓    ✓        ✓     ✓          ✓       ✓     ✓    ✓      ✓      ✓      ✓    ✓         ✓    ✓     
```

#### Deepgram
- **Latency**: 4.03s | **Ref Words**: 27 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   hands   and   face   are   not   swollen   because   i    stood   for   long   hours   my   ankles   are   slightly   puffy   but   it   goes   away   when   i    elevate   my   feet  
HYP : my   hands   and   face   are   not   swollen   because   i    stood   for   long   hours   my   ankles   are   slightly   puffy   but   it   goes   away   when   i    elevate   my   feet  
EVAL: ✓    ✓       ✓     ✓      ✓     ✓     ✓         ✓         ✓    ✓       ✓     ✓      ✓       ✓    ✓        ✓     ✓          ✓       ✓     ✓    ✓      ✓      ✓      ✓    ✓         ✓    ✓     
```

#### Gemini
- **Latency**: 4.7s | **Ref Words**: 27 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   hands   and   face   are   not   swollen   because   i    stood   for   long   hours   my   ankles   are   slightly   puffy   but   it   goes   away   when   i    elevate   my   feet  
HYP : my   hands   and   face   are   not   swollen   because   i    stood   for   long   hours   my   ankles   are   slightly   puffy   but   it   goes   away   when   i    elevate   my   feet  
EVAL: ✓    ✓       ✓     ✓      ✓     ✓     ✓         ✓         ✓    ✓       ✓     ✓      ✓       ✓    ✓        ✓     ✓          ✓       ✓     ✓    ✓      ✓      ✓      ✓    ✓         ✓    ✓     
```

---

### Voice: `v198.wav`
> **Ground Truth Reference**:
> *I don't have a headache; I just feel heavy sleepiness and general exhaustion.*

#### Sahara
- **Latency**: 5.54s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    dont   have   a    headache   i    just   feel   heavy   sleepiness   and   general   exhaustion  
HYP : i    dont   have   a    headache   i    just   feel   heavy   sleepiness   and   general   exhaustion  
EVAL: ✓    ✓      ✓      ✓    ✓          ✓    ✓      ✓      ✓       ✓            ✓     ✓         ✓           
```

#### Deepgram
- **Latency**: 3.61s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    dont   have   a    headache   i    just   feel   heavy   sleepiness   and   general   exhaustion  
HYP : i    dont   have   a    headache   i    just   feel   heavy   sleepiness   and   general   exhaustion  
EVAL: ✓    ✓      ✓      ✓    ✓          ✓    ✓      ✓      ✓       ✓            ✓     ✓         ✓           
```

#### Gemini
- **Latency**: 3.7s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    dont   have   a    headache   i    just   feel   heavy   sleepiness   and   general   exhaustion  
HYP : i    dont   have   a    headache   i    just   feel   heavy   sleepiness   and   general   exhaustion  
EVAL: ✓    ✓      ✓      ✓    ✓          ✓    ✓      ✓      ✓       ✓            ✓     ✓         ✓           
```

---

### Voice: `v199.wav`
> **Ground Truth Reference**:
> *My vision isn't dim or clouded; when I go out of bed quickly I had a slight dizziness, but after sitting for a bit it left.*

#### Sahara
- **Latency**: 4.52s | **Ref Words**: 26 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **7.7%** | **Word Accuracy**: **92.3%** | **CER**: 2.1%

```text
REF : my   vision   isnt   dim   or   clouded   when   i    go    out   of   bed   quickly   i    had   a    slight   dizziness   but   after   sitting   for   a    bit   it    left  
HYP : my   vision   isnt   dim   or   clouded   when   i    got   out   of   bed   quickly   i    had   a    slight   dizziness   but   after   sitting   for   a    bit   its   left  
EVAL: ✓    ✓        ✓      ✓     ✓    ✓         ✓      ✓    SUB   ✓     ✓    ✓     ✓         ✓    ✓     ✓    ✓        ✓           ✓     ✓       ✓         ✓     ✓    ✓     SUB   ✓     
```

#### Deepgram
- **Latency**: 3.63s | **Ref Words**: 26 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **3.9%** | **Word Accuracy**: **96.2%** | **CER**: 1.1%

```text
REF : my   vision   isnt   dim   or   clouded   when   i    go   out   of   bed   quickly   i    had   a    slight   dizziness   but   after   sitting   for   a    bit   it    left  
HYP : my   vision   isnt   dim   or   clouded   when   i    go   out   of   bed   quickly   i    had   a    slight   dizziness   but   after   sitting   for   a    bit   its   left  
EVAL: ✓    ✓        ✓      ✓     ✓    ✓         ✓      ✓    ✓    ✓     ✓    ✓     ✓         ✓    ✓     ✓    ✓        ✓           ✓     ✓       ✓         ✓     ✓    ✓     SUB   ✓     
```

#### Gemini
- **Latency**: 3.54s | **Ref Words**: 26 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **3.9%** | **Word Accuracy**: **96.2%** | **CER**: 1.1%

```text
REF : my   vision   isnt   dim   or   clouded   when   i    go   out   of   bed   quickly   i    had   a    slight   dizziness   but   after   sitting   for   a    bit   it    left  
HYP : my   vision   isnt   dim   or   clouded   when   i    go   out   of   bed   quickly   i    had   a    slight   dizziness   but   after   sitting   for   a    bit   its   left  
EVAL: ✓    ✓        ✓      ✓     ✓    ✓         ✓      ✓    ✓    ✓     ✓    ✓     ✓         ✓    ✓     ✓    ✓        ✓           ✓     ✓       ✓         ✓     ✓    ✓     SUB   ✓     
```

---
