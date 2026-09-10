# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v190_v194_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 10:00:17 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 97 | 1 | 1 | 0 | 0 | **1.0%** | **99.0%** | 0.2% | 5.12s |
| **Deepgram** | 97 | 3 | 2 | 0 | 1 | **3.1%** | **96.9%** | 1.4% | 4.08s |
| **Gemini** | 97 | 6 | 5 | 0 | 1 | **6.2%** | **93.8%** | 1.9% | 4.48s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v190.wav`
> **Ground Truth Reference**:
> *I don't understand by fluid do you mean urine or something else? Because today I'm urinating frequently, but I have no pain.*

#### Sahara
- **Latency**: 5.64s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    dont   understand   by   fluid   do   you   mean   urine   or   something   else   because   today   im   urinating   frequently   but   i    have   no   pain  
HYP : i    dont   understand   by   fluid   do   you   mean   urine   or   something   else   because   today   im   urinating   frequently   but   i    have   no   pain  
EVAL: ✓    ✓      ✓            ✓    ✓       ✓    ✓     ✓      ✓       ✓    ✓           ✓      ✓         ✓       ✓    ✓           ✓            ✓     ✓    ✓      ✓    ✓     
```

#### Deepgram
- **Latency**: 3.77s | **Ref Words**: 22 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 4.1%

```text
REF : i    dont   understand   by   fluid   do   you   mean   ---   urine   or   something   else   because   today   im   urinating   frequently   but   i    have   no   pain  
HYP : i    dont   understand   by   fluid   do   you   mean   you   rain    or   something   else   because   today   im   urinating   frequently   but   i    have   no   pain  
EVAL: ✓    ✓      ✓            ✓    ✓       ✓    ✓     ✓      INS   SUB     ✓    ✓           ✓      ✓         ✓       ✓    ✓           ✓            ✓     ✓    ✓      ✓    ✓     
```

#### Gemini
- **Latency**: 3.81s | **Ref Words**: 22 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    dont   understand   by   fluid   do   you   mean   urine   or   something   else   because   today   im   urinating   frequently   but   i    have   no   pain  
HYP : i    dont   understand   by   fluid   do   you   mean   urine   or   something   else   because   today   im   urinating   frequently   but   i    have   no   pain  
EVAL: ✓    ✓      ✓            ✓    ✓       ✓    ✓     ✓      ✓       ✓    ✓           ✓      ✓         ✓       ✓    ✓           ✓            ✓     ✓    ✓      ✓    ✓     
```

---

### Voice: `v191.wav`
> **Ground Truth Reference**:
> *None of the pain you mentioned; but after I eat, heartburn hurts my chest, I can't even keep water down.*

#### Sahara
- **Latency**: 4.44s | **Ref Words**: 20 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : none   of   the   pain   you   mentioned   but   after   i    eat   heartburn   hurts   my   chest   i    cant   even   keep   water   down  
HYP : none   of   the   pain   you   mentioned   but   after   i    eat   heartburn   hurts   my   chest   i    cant   even   keep   water   down  
EVAL: ✓      ✓    ✓     ✓      ✓     ✓           ✓     ✓       ✓    ✓     ✓           ✓       ✓    ✓       ✓    ✓      ✓      ✓      ✓       ✓     
```

#### Deepgram
- **Latency**: 4.3s | **Ref Words**: 20 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : none   of   the   pain   you   mentioned   but   after   i    eat   heartburn   hurts   my   chest   i    cant   even   keep   water   down  
HYP : none   of   the   pain   you   mentioned   but   after   i    eat   heartburn   hurts   my   chest   i    cant   even   keep   water   down  
EVAL: ✓      ✓    ✓     ✓      ✓     ✓           ✓     ✓       ✓    ✓     ✓           ✓       ✓    ✓       ✓    ✓      ✓      ✓      ✓       ✓     
```

#### Gemini
- **Latency**: 4.1s | **Ref Words**: 20 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 3.8%

```text
REF : none   of   the   pain   you   mentioned   but   after   i    eat   ---     heartburn   hurts   my   chest   i    cant   even   keep   water   down  
HYP : none   of   the   pain   you   mentioned   but   after   i    eat   hurts   burn        hurts   my   chest   i    cant   even   keep   water   down  
EVAL: ✓      ✓    ✓     ✓      ✓     ✓           ✓     ✓       ✓    ✓     INS     SUB         ✓       ✓    ✓       ✓    ✓      ✓      ✓      ✓       ✓     
```

---

### Voice: `v192.wav`
> **Ground Truth Reference**:
> *It's not severe pain; because I have constipation and bloating, my belly just feels a bit heavy.*

#### Sahara
- **Latency**: 4.85s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   severe   pain   because   i    have   constipation   and   bloating   my   belly   just   feels   a    bit   heavy  
HYP : its   not   severe   pain   because   i    have   constipation   and   bloating   my   belly   just   feels   a    bit   heavy  
EVAL: ✓     ✓     ✓        ✓      ✓         ✓    ✓      ✓              ✓     ✓          ✓    ✓       ✓      ✓       ✓    ✓     ✓      
```

#### Deepgram
- **Latency**: 3.89s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   severe   pain   because   i    have   constipation   and   bloating   my   belly   just   feels   a    bit   heavy  
HYP : its   not   severe   pain   because   i    have   constipation   and   bloating   my   belly   just   feels   a    bit   heavy  
EVAL: ✓     ✓     ✓        ✓      ✓         ✓    ✓      ✓              ✓     ✓          ✓    ✓       ✓      ✓       ✓    ✓     ✓      
```

#### Gemini
- **Latency**: 4.3s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   severe   pain   because   i    have   constipation   and   bloating   my   belly   just   feels   a    bit   heavy  
HYP : its   not   severe   pain   because   i    have   constipation   and   bloating   my   belly   just   feels   a    bit   heavy  
EVAL: ✓     ✓     ✓        ✓      ✓         ✓    ✓      ✓              ✓     ✓          ✓    ✓       ✓      ✓       ✓    ✓     ✓      
```

---

### Voice: `v193.wav`
> **Ground Truth Reference**:
> *Because the skin on my abdomen is stretching it started itching, but there are no cramps or sharp abdominal pain.*

#### Sahara
- **Latency**: 4.43s | **Ref Words**: 20 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.0%** | **Word Accuracy**: **95.0%** | **CER**: 1.1%

```text
REF : because   the   skin   on    my   abdomen   is   stretching   it   started   itching   but   there   are   no   cramps   or   sharp   abdominal   pain  
HYP : because   the   skin   of    my   abdomen   is   stretching   it   started   itching   but   there   are   no   cramps   or   sharp   abdominal   pain  
EVAL: ✓         ✓     ✓      SUB   ✓    ✓         ✓    ✓            ✓    ✓         ✓         ✓     ✓       ✓     ✓    ✓        ✓    ✓       ✓           ✓     
```

#### Deepgram
- **Latency**: 4.11s | **Ref Words**: 20 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.0%** | **Word Accuracy**: **95.0%** | **CER**: 2.2%

```text
REF : because   the   skin   on   my   abdomen   is   stretching   it   started   itching   but   there   are   no   cramps   or   sharp   abdominal   pain  
HYP : because   the   skin   on   my   abdomen   is   stretching   it   started   itching   but   there   are   no   crumbs   or   sharp   abdominal   pain  
EVAL: ✓         ✓     ✓      ✓    ✓    ✓         ✓    ✓            ✓    ✓         ✓         ✓     ✓       ✓     ✓    SUB      ✓    ✓       ✓           ✓     
```

#### Gemini
- **Latency**: 4.15s | **Ref Words**: 20 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 5.4%

```text
REF : because   the    skin   on    my   abdomen   is   stretching   it   started   itching   but   there   are   no   cramps   or   sharp   abdominal   pain  
HYP : because   this   kind   of    my   abdomen   is   stretching   it   started   itching   but   there   are   no   crumbs   or   sharp   abdominal   pain  
EVAL: ✓         SUB    SUB    SUB   ✓    ✓         ✓    ✓            ✓    ✓         ✓         ✓     ✓       ✓     ✓    SUB      ✓    ✓       ✓           ✓     
```

---

### Voice: `v194.wav`
> **Ground Truth Reference**:
> *When I stand up suddenly my side pulls slightly, but it stops right away; it’s not severe pain.*

#### Sahara
- **Latency**: 6.24s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : when   i    stand   up   suddenly   my   side   pulls   slightly   but   it   stops   right   away   its   not   severe   pain  
HYP : when   i    stand   up   suddenly   my   side   pulls   slightly   but   it   stops   right   away   its   not   severe   pain  
EVAL: ✓      ✓    ✓       ✓    ✓          ✓    ✓      ✓       ✓          ✓     ✓    ✓       ✓       ✓      ✓     ✓     ✓        ✓     
```

#### Deepgram
- **Latency**: 4.32s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : when   i    stand   up   suddenly   my   side   pulls   slightly   but   it   stops   right   away   its   not   severe   pain  
HYP : when   i    stand   up   suddenly   my   side   pulls   slightly   but   it   stops   right   away   its   not   severe   pain  
EVAL: ✓      ✓    ✓       ✓    ✓          ✓    ✓      ✓       ✓          ✓     ✓    ✓       ✓       ✓      ✓     ✓     ✓        ✓     
```

#### Gemini
- **Latency**: 6.03s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : when   i    stand   up   suddenly   my   side   pulls   slightly   but   it   stops   right   away   its   not   severe   pain  
HYP : when   i    stand   up   suddenly   my   side   pulls   slightly   but   it   stops   right   away   its   not   severe   pain  
EVAL: ✓      ✓    ✓       ✓    ✓          ✓    ✓      ✓       ✓          ✓     ✓    ✓       ✓       ✓      ✓     ✓     ✓        ✓     
```

---
