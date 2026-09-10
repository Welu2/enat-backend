# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v145_v149_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:58:16 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 77 | 4 | 3 | 1 | 0 | **5.2%** | **94.8%** | 2.2% | 4.73s |
| **Deepgram** | 77 | 4 | 3 | 1 | 0 | **5.2%** | **94.8%** | 2.2% | 4.51s |
| **Gemini** | 77 | 8 | 5 | 3 | 0 | **10.4%** | **89.6%** | 4.4% | 3.88s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v145.wav`
> **Ground Truth Reference**:
> *It's not severe pain, but my lower back aches a bit from the weight; otherwise I'm fine.*

#### Sahara
- **Latency**: 4.59s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   severe   pain   but   my   lower   back   aches   a    bit   from   the   weight   otherwise   im   fine  
HYP : its   not   severe   pain   but   my   lower   back   aches   a    bit   from   the   weight   otherwise   im   fine  
EVAL: ✓     ✓     ✓        ✓      ✓     ✓    ✓       ✓      ✓       ✓    ✓     ✓      ✓     ✓        ✓           ✓    ✓     
```

#### Deepgram
- **Latency**: 8.19s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : its   not   severe   pain   but   my   lower   back   aches   a    bit   from   the   weight   otherwise   im   fine  
HYP : its   not   severe   pain   but   my   lower   back   aches   a    bit   from   the   weight   otherwise   im   fine  
EVAL: ✓     ✓     ✓        ✓      ✓     ✓    ✓       ✓      ✓       ✓    ✓     ✓      ✓     ✓        ✓           ✓    ✓     
```

#### Gemini
- **Latency**: 4.1s | **Ref Words**: 17 | **Errors**: 4 (S: 2, D: 2, I: 0)
- **WER**: **23.5%** | **Word Accuracy**: **76.5%** | **CER**: 13.4%

```text
REF : its   not   severe   pain   but   my   lower   back   aches   a     bit        from   the   weight   otherwise   im   fine  
HYP : its   not   severe   pain   but   my   lower   back   ---     ---   exhibits   from   the   waist    otherwise   im   fine  
EVAL: ✓     ✓     ✓        ✓      ✓     ✓    ✓       ✓      DEL     DEL   SUB        ✓      ✓     SUB      ✓           ✓    ✓     
```

---

### Voice: `v146.wav`
> **Ground Truth Reference**:
> *Well... I had a bit of morning nausea, but no headache and no bleeding.*

#### Sahara
- **Latency**: 4.45s | **Ref Words**: 14 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **7.1%** | **Word Accuracy**: **92.9%** | **CER**: 3.8%

```text
REF : well   i    had    a    bit   of   morning   nausea   but   no   headache   and   no   bleeding  
HYP : well   i    have   a    bit   of   morning   nausea   but   no   headache   and   no   bleeding  
EVAL: ✓      ✓    SUB    ✓    ✓     ✓    ✓         ✓        ✓     ✓    ✓          ✓     ✓    ✓         
```

#### Deepgram
- **Latency**: 3.7s | **Ref Words**: 14 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **7.1%** | **Word Accuracy**: **92.9%** | **CER**: 3.8%

```text
REF : well   i    had    a    bit   of   morning   nausea   but   no   headache   and   no   bleeding  
HYP : well   i    have   a    bit   of   morning   nausea   but   no   headache   and   no   bleeding  
EVAL: ✓      ✓    SUB    ✓    ✓     ✓    ✓         ✓        ✓     ✓    ✓          ✓     ✓    ✓         
```

#### Gemini
- **Latency**: 3.88s | **Ref Words**: 14 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **7.1%** | **Word Accuracy**: **92.9%** | **CER**: 3.8%

```text
REF : well   i    had    a    bit   of   morning   nausea   but   no   headache   and   no   bleeding  
HYP : well   i    have   a    bit   of   morning   nausea   but   no   headache   and   no   bleeding  
EVAL: ✓      ✓    SUB    ✓    ✓     ✓    ✓         ✓        ✓     ✓    ✓          ✓     ✓    ✓         
```

---

### Voice: `v147.wav`
> **Ground Truth Reference**:
> *My belly feels a bit heavy, but there is no severe pain or leaking fluid.*

#### Sahara
- **Latency**: 4.86s | **Ref Words**: 15 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **13.3%** | **Word Accuracy**: **86.7%** | **CER**: 1.8%

```text
REF : my   belly   feels   a    bit   heavy   but   there   is       no   severe   pain   or   leaking   fluid  
HYP : my   belly   feels   a    bit   heavy   but   ---     theres   no   severe   pain   or   leaking   fluid  
EVAL: ✓    ✓       ✓       ✓    ✓     ✓       ✓     DEL     SUB      ✓    ✓        ✓      ✓    ✓         ✓      
```

#### Deepgram
- **Latency**: 3.53s | **Ref Words**: 15 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **13.3%** | **Word Accuracy**: **86.7%** | **CER**: 1.8%

```text
REF : my   belly   feels   a    bit   heavy   but   there   is       no   severe   pain   or   leaking   fluid  
HYP : my   belly   feels   a    bit   heavy   but   ---     theres   no   severe   pain   or   leaking   fluid  
EVAL: ✓    ✓       ✓       ✓    ✓     ✓       ✓     DEL     SUB      ✓    ✓        ✓      ✓    ✓         ✓      
```

#### Gemini
- **Latency**: 3.57s | **Ref Words**: 15 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **13.3%** | **Word Accuracy**: **86.7%** | **CER**: 1.8%

```text
REF : my   belly   feels   a    bit   heavy   but   there   is       no   severe   pain   or   leaking   fluid  
HYP : my   belly   feels   a    bit   heavy   but   ---     theres   no   severe   pain   or   leaking   fluid  
EVAL: ✓    ✓       ✓       ✓    ✓     ✓       ✓     DEL     SUB      ✓    ✓        ✓      ✓    ✓         ✓      
```

---

### Voice: `v148.wav`
> **Ground Truth Reference**:
> *I just feel fatigued, but my eyes aren't blurry and my head isn't spinning.*

#### Sahara
- **Latency**: 4.92s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    just   feel   fatigued   but   my   eyes   arent   blurry   and   my   head   isnt   spinning  
HYP : i    just   feel   fatigued   but   my   eyes   arent   blurry   and   my   head   isnt   spinning  
EVAL: ✓    ✓      ✓      ✓          ✓     ✓    ✓      ✓       ✓        ✓     ✓    ✓      ✓      ✓         
```

#### Deepgram
- **Latency**: 3.48s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    just   feel   fatigued   but   my   eyes   arent   blurry   and   my   head   isnt   spinning  
HYP : i    just   feel   fatigued   but   my   eyes   arent   blurry   and   my   head   isnt   spinning  
EVAL: ✓    ✓      ✓      ✓          ✓     ✓    ✓      ✓       ✓        ✓     ✓    ✓      ✓      ✓         
```

#### Gemini
- **Latency**: 3.84s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    just   feel   fatigued   but   my   eyes   arent   blurry   and   my   head   isnt   spinning  
HYP : i    just   feel   fatigued   but   my   eyes   arent   blurry   and   my   head   isnt   spinning  
EVAL: ✓    ✓      ✓      ✓          ✓     ✓    ✓      ✓       ✓        ✓     ✓    ✓      ✓      ✓         
```

---

### Voice: `v149.wav`
> **Ground Truth Reference**:
> *Yes, in the morning I've had a severe, heavy headache; even after taking paracetamol it hasn't stopped.*

#### Sahara
- **Latency**: 4.81s | **Ref Words**: 17 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.9%** | **Word Accuracy**: **94.1%** | **CER**: 4.9%

```text
REF : yes   in   the   morning   ive      had   a    severe   heavy   headache   even   after   taking   paracetamol   it   hasnt   stopped  
HYP : yes   in   the   morning   theyve   had   a    severe   heavy   headache   even   after   taking   paracetamol   it   hasnt   stopped  
EVAL: ✓     ✓    ✓     ✓         SUB      ✓     ✓    ✓        ✓       ✓          ✓      ✓       ✓        ✓             ✓    ✓       ✓        
```

#### Deepgram
- **Latency**: 3.65s | **Ref Words**: 17 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.9%** | **Word Accuracy**: **94.1%** | **CER**: 4.9%

```text
REF : yes   in   the   morning   ive      had   a    severe   heavy   headache   even   after   taking   paracetamol   it   hasnt   stopped  
HYP : yes   in   the   morning   theyve   had   a    severe   heavy   headache   even   after   taking   paracetamol   it   hasnt   stopped  
EVAL: ✓     ✓    ✓     ✓         SUB      ✓     ✓    ✓        ✓       ✓          ✓      ✓       ✓        ✓             ✓    ✓       ✓        
```

#### Gemini
- **Latency**: 4.03s | **Ref Words**: 17 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.9%** | **Word Accuracy**: **94.1%** | **CER**: 2.5%

```text
REF : yes   in    the   morning   ive   had   a    severe   heavy   headache   even   after   taking   paracetamol   it   hasnt   stopped  
HYP : yes   and   the   morning   ive   had   a    severe   heavy   headache   even   after   taking   paracetamol   it   hasnt   stopped  
EVAL: ✓     SUB   ✓     ✓         ✓     ✓     ✓    ✓        ✓       ✓          ✓      ✓       ✓        ✓             ✓    ✓       ✓        
```

---
