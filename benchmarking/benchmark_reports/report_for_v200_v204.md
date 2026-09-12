# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v200_v204_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 10:00:43 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 95 | 10 | 6 | 4 | 0 | **10.5%** | **89.5%** | 2.2% | 5.10s |
| **Deepgram** | 95 | 11 | 7 | 4 | 0 | **11.6%** | **88.4%** | 1.9% | 4.03s |
| **Gemini** | 95 | 11 | 7 | 4 | 0 | **11.6%** | **88.4%** | 2.4% | 3.97s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v200.wav`
> **Ground Truth Reference**:
> *Because the baby is pushing upward I get a bit winded when climbing stairs, but it’s not choking or severe breathlessness.*

#### Sahara
- **Latency**: 4.73s | **Ref Words**: 21 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **4.8%** | **Word Accuracy**: **95.2%** | **CER**: 1.0%

```text
REF : because   the   baby   is   pushing   upward   i    get   a    bit   winded   when   climbing   stairs   but   its   not   choking   or   severe   breathlessness  
HYP : because   the   baby   is   pushing   upward   i    get   a    bit   winded   when   climbing   stairs   but   its   no    choking   or   severe   breathlessness  
EVAL: ✓         ✓     ✓      ✓    ✓         ✓        ✓    ✓     ✓    ✓     ✓        ✓      ✓          ✓        ✓     ✓     SUB   ✓         ✓    ✓        ✓               
```

#### Deepgram
- **Latency**: 4.4s | **Ref Words**: 21 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : because   the   baby   is   pushing   upward   i    get   a    bit   winded   when   climbing   stairs   but   its   not   choking   or   severe   breathlessness  
HYP : because   the   baby   is   pushing   upward   i    get   a    bit   winded   when   climbing   stairs   but   its   not   choking   or   severe   breathlessness  
EVAL: ✓         ✓     ✓      ✓    ✓         ✓        ✓    ✓     ✓    ✓     ✓        ✓      ✓          ✓        ✓     ✓     ✓     ✓         ✓    ✓        ✓               
```

#### Gemini
- **Latency**: 3.9s | **Ref Words**: 21 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : because   the   baby   is   pushing   upward   i    get   a    bit   winded   when   climbing   stairs   but   its   not   choking   or   severe   breathlessness  
HYP : because   the   baby   is   pushing   upward   i    get   a    bit   winded   when   climbing   stairs   but   its   not   choking   or   severe   breathlessness  
EVAL: ✓         ✓     ✓      ✓    ✓         ✓        ✓    ✓     ✓    ✓     ✓        ✓      ✓          ✓        ✓     ✓     ✓     ✓         ✓    ✓        ✓               
```

---

### Voice: `v201.wav`
> **Ground Truth Reference**:
> *No vomiting; but in the mornings when food smells hit me I feel nauseous, then later it goes away.*

#### Sahara
- **Latency**: 4.85s | **Ref Words**: 19 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   vomiting   but   in   the   mornings   when   food   smells   hit   me   i    feel   nauseous   then   later   it   goes   away  
HYP : no   vomiting   but   in   the   mornings   when   food   smells   hit   me   i    feel   nauseous   then   later   it   goes   away  
EVAL: ✓    ✓          ✓     ✓    ✓     ✓          ✓      ✓      ✓        ✓     ✓    ✓    ✓      ✓          ✓      ✓       ✓    ✓      ✓     
```

#### Deepgram
- **Latency**: 4.51s | **Ref Words**: 19 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **15.8%** | **Word Accuracy**: **84.2%** | **CER**: 6.5%

```text
REF : no      vomiting   but   in   the   mornings   when   food   smells   hit    me   i    feel   nauseous   then   later   it   goes   away  
HYP : novel   meeting    but   in   the   mornings   when   food   smells   hits   me   i    feel   nauseous   then   later   it   goes   away  
EVAL: SUB     SUB        ✓     ✓    ✓     ✓          ✓      ✓      ✓        SUB    ✓    ✓    ✓      ✓          ✓      ✓       ✓    ✓      ✓     
```

#### Gemini
- **Latency**: 4.5s | **Ref Words**: 19 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.3%** | **Word Accuracy**: **94.7%** | **CER**: 1.3%

```text
REF : no   vomiting   but   in   the   mornings   when   food   smells   hit    me   i    feel   nauseous   then   later   it   goes   away  
HYP : no   vomiting   but   in   the   mornings   when   food   smells   hits   me   i    feel   nauseous   then   later   it   goes   away  
EVAL: ✓    ✓          ✓     ✓    ✓     ✓          ✓      ✓      ✓        SUB    ✓    ✓    ✓      ✓          ✓      ✓       ✓    ✓      ✓     
```

---

### Voice: `v202.wav`
> **Ground Truth Reference**:
> *There is no leaking fluid; because the baby pushes down I am just frequenting the bathroom often, but I have no pain.*

#### Sahara
- **Latency**: 4.66s | **Ref Words**: 22 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 1.1%

```text
REF : there   is   no   leaking   fluid   because   the   baby   pushes   down   i     am    just   frequenting   the   bathroom   often   but   i    have   no   pain  
HYP : there   is   no   leaking   fluid   because   the   baby   pushes   down   ---   im    just   frequenting   the   bathroom   often   but   i    have   no   pain  
EVAL: ✓       ✓    ✓    ✓         ✓       ✓         ✓     ✓      ✓        ✓      DEL   SUB   ✓      ✓             ✓     ✓          ✓       ✓     ✓    ✓      ✓    ✓     
```

#### Deepgram
- **Latency**: 3.5s | **Ref Words**: 22 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 1.1%

```text
REF : there   is   no   leaking   fluid   because   the   baby   pushes   down   i     am    just   frequenting   the   bathroom   often   but   i    have   no   pain  
HYP : there   is   no   leaking   fluid   because   the   baby   pushes   down   ---   im    just   frequenting   the   bathroom   often   but   i    have   no   pain  
EVAL: ✓       ✓    ✓    ✓         ✓       ✓         ✓     ✓      ✓        ✓      DEL   SUB   ✓      ✓             ✓     ✓          ✓       ✓     ✓    ✓      ✓    ✓     
```

#### Gemini
- **Latency**: 3.88s | **Ref Words**: 22 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **13.6%** | **Word Accuracy**: **86.4%** | **CER**: 6.5%

```text
REF : there   is   no   leaking   fluid   because   the   baby   pushes   down   i     am    just   frequenting   the   bathroom   often   but   i    have   no   pain  
HYP : there   is   no   leaking   fluid   because   the   baby   pushes   down   ---   and   just   frequently    the   bathroom   often   but   i    have   no   pain  
EVAL: ✓       ✓    ✓    ✓         ✓       ✓         ✓     ✓      ✓        ✓      DEL   SUB   ✓      SUB           ✓     ✓          ✓       ✓     ✓    ✓      ✓    ✓     
```

---

### Voice: `v203.wav`
> **Ground Truth Reference**:
> *Occasionally my belly tightens but it doesn't cramp, and it lets go quickly; it is not continuous pain.*

#### Sahara
- **Latency**: 5.88s | **Ref Words**: 18 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 1.2%

```text
REF : occasionally   my   belly   tightens   but   it   doesnt   cramp   and   it   lets   go   quickly   it    is    not   continuous   pain  
HYP : occasionally   my   belly   tightens   but   it   doesnt   cramp   and   it   lets   go   quickly   ---   its   not   continuous   pain  
EVAL: ✓              ✓    ✓       ✓          ✓     ✓    ✓        ✓       ✓     ✓    ✓      ✓    ✓         DEL   SUB   ✓     ✓            ✓     
```

#### Deepgram
- **Latency**: 3.95s | **Ref Words**: 18 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 1.2%

```text
REF : occasionally   my   belly   tightens   but   it   doesnt   cramp   and   it   lets   go   quickly   it    is    not   continuous   pain  
HYP : occasionally   my   belly   tightens   but   it   doesnt   cramp   and   it   lets   go   quickly   ---   its   not   continuous   pain  
EVAL: ✓              ✓    ✓       ✓          ✓     ✓    ✓        ✓       ✓     ✓    ✓      ✓    ✓         DEL   SUB   ✓     ✓            ✓     
```

#### Gemini
- **Latency**: 3.67s | **Ref Words**: 18 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 1.2%

```text
REF : occasionally   my   belly   tightens   but   it   doesnt   cramp   and   it   lets   go   quickly   it    is    not   continuous   pain  
HYP : occasionally   my   belly   tightens   but   it   doesnt   cramp   and   it   lets   go   quickly   ---   its   not   continuous   pain  
EVAL: ✓              ✓    ✓       ✓          ✓     ✓    ✓        ✓       ✓     ✓    ✓      ✓    ✓         DEL   SUB   ✓     ✓            ✓     
```

---

### Voice: `v204.wav`
> **Ground Truth Reference**:
> *Oh, there is nothing severe like that; just the usual heavy belly and back ache.*

#### Sahara
- **Latency**: 5.36s | **Ref Words**: 15 | **Errors**: 5 (S: 3, D: 2, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 9.5%

```text
REF : oh   there   is       nothing   severe   like   that   just   the   usual   heavy   belly     and   back   ache      
HYP : oh   ---     theres   nothing   severe   like   that   just   the   usual   heavy   bailing   and   ---    backache  
EVAL: ✓    DEL     SUB      ✓         ✓        ✓      ✓      ✓      ✓     ✓       ✓       SUB       ✓     DEL    SUB       
```

#### Deepgram
- **Latency**: 3.78s | **Ref Words**: 15 | **Errors**: 4 (S: 2, D: 2, I: 0)
- **WER**: **26.7%** | **Word Accuracy**: **73.3%** | **CER**: 1.6%

```text
REF : oh   there   is       nothing   severe   like   that   just   the   usual   heavy   belly   and   back   ache      
HYP : oh   ---     theres   nothing   severe   like   that   just   the   usual   heavy   belly   and   ---    backache  
EVAL: ✓    DEL     SUB      ✓         ✓        ✓      ✓      ✓      ✓     ✓       ✓       ✓       ✓     DEL    SUB       
```

#### Gemini
- **Latency**: 3.89s | **Ref Words**: 15 | **Errors**: 5 (S: 3, D: 2, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 3.2%

```text
REF : oh   there   is       nothing   severe   like   that   just   the   usual   heavy   belly   and   back   ache      
HYP : oh   ---     theres   nothing   severe   like   that   just   the   usual   heavy   beily   and   ---    backache  
EVAL: ✓    DEL     SUB      ✓         ✓        ✓      ✓      ✓      ✓     ✓       ✓       SUB     ✓     DEL    SUB       
```

---
