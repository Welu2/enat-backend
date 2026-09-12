# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v165_v169_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:59:31 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 59 | 7 | 4 | 2 | 1 | **11.9%** | **88.1%** | 2.8% | 5.05s |
| **Deepgram** | 59 | 3 | 2 | 1 | 0 | **5.1%** | **94.9%** | 1.2% | 3.43s |
| **Gemini** | 59 | 5 | 4 | 1 | 0 | **8.5%** | **91.5%** | 1.6% | 5.26s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v165.wav`
> **Ground Truth Reference**:
> *No, I haven't felt anything, and the baby is kicking well, I'm fine.*

#### Sahara
- **Latency**: 5.67s | **Ref Words**: 13 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 2.0%

```text
REF : no   i    havent   felt   anything   and   the   baby   is      kicking   well   im   fine  
HYP : no   i    havent   felt   anything   and   the   ---    babys   kicking   well   im   fine  
EVAL: ✓    ✓    ✓        ✓      ✓          ✓     ✓     DEL    SUB     ✓         ✓      ✓    ✓     
```

#### Deepgram
- **Latency**: 3.35s | **Ref Words**: 13 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 2.0%

```text
REF : no   i    havent   felt   anything   and   the   baby   is      kicking   well   im   fine  
HYP : no   i    havent   felt   anything   and   the   ---    babys   kicking   well   im   fine  
EVAL: ✓    ✓    ✓        ✓      ✓          ✓     ✓     DEL    SUB     ✓         ✓      ✓    ✓     
```

#### Gemini
- **Latency**: 4.23s | **Ref Words**: 13 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 2.0%

```text
REF : no   i    havent   felt   anything   and   the   baby   is      kicking   well   im   fine  
HYP : no   i    havent   felt   anything   and   the   ---    babys   kicking   well   im   fine  
EVAL: ✓    ✓    ✓        ✓      ✓          ✓     ✓     DEL    SUB     ✓         ✓      ✓    ✓     
```

---

### Voice: `v166.wav`
> **Ground Truth Reference**:
> *Nothing at all today; I actually feel much better, I'm even doing my house chores.*

#### Sahara
- **Latency**: 5.06s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : nothing   at   all   today   i    actually   feel   much   better   im   even   doing   my   house   chores  
HYP : nothing   at   all   today   i    actually   feel   much   better   im   even   doing   my   house   chores  
EVAL: ✓         ✓    ✓     ✓       ✓    ✓          ✓      ✓      ✓        ✓    ✓      ✓       ✓    ✓       ✓       
```

#### Deepgram
- **Latency**: 3.79s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : nothing   at   all   today   i    actually   feel   much   better   im   even   doing   my   house   chores  
HYP : nothing   at   all   today   i    actually   feel   much   better   im   even   doing   my   house   chores  
EVAL: ✓         ✓    ✓     ✓       ✓    ✓          ✓      ✓      ✓        ✓    ✓      ✓       ✓    ✓       ✓       
```

#### Gemini
- **Latency**: 10.55s | **Ref Words**: 15 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : nothing   at   all   today   i    actually   feel   much   better   im   even   doing   my   house   chores  
HYP : nothing   at   all   today   i    actually   feel   much   better   im   even   doing   my   house   chores  
EVAL: ✓         ✓    ✓     ✓       ✓    ✓          ✓      ✓      ✓        ✓    ✓      ✓       ✓    ✓       ✓       
```

---

### Voice: `v167.wav`
> **Ground Truth Reference**:
> *None of the ones you mentioned have happened on me, thank God.*

#### Sahara
- **Latency**: 4.67s | **Ref Words**: 12 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **8.3%** | **Word Accuracy**: **91.7%** | **CER**: 4.1%

```text
REF : none   of   the   ones   you   mentioned   have   happened   on    me   thank   god  
HYP : none   of   the   ones   you   mentioned   have   happened   to    me   thank   god  
EVAL: ✓      ✓    ✓     ✓      ✓     ✓           ✓      ✓          SUB   ✓    ✓       ✓    
```

#### Deepgram
- **Latency**: 3.43s | **Ref Words**: 12 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : none   of   the   ones   you   mentioned   have   happened   on   me   thank   god  
HYP : none   of   the   ones   you   mentioned   have   happened   on   me   thank   god  
EVAL: ✓      ✓    ✓     ✓      ✓     ✓           ✓      ✓          ✓    ✓    ✓       ✓    
```

#### Gemini
- **Latency**: 3.76s | **Ref Words**: 12 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : none   of   the   ones   you   mentioned   have   happened   on   me   thank   god  
HYP : none   of   the   ones   you   mentioned   have   happened   on   me   thank   god  
EVAL: ✓      ✓    ✓     ✓      ✓     ✓           ✓      ✓          ✓    ✓    ✓       ✓    
```

---

### Voice: `v168.wav`
> **Ground Truth Reference**:
> *Neither headache nor stomach ache; I just felt a bit insomnia.*

#### Sahara
- **Latency**: 4.81s | **Ref Words**: 11 | **Errors**: 4 (S: 2, D: 1, I: 1)
- **WER**: **36.4%** | **Word Accuracy**: **63.6%** | **CER**: 8.0%

```text
REF : neither   headache   nor   stomach   ache          i    just   felt   a    bit   ---   insomnia  
HYP : neither   headache   nor   ---       stomachache   i    just   feel   a    bit   of    insomnia  
EVAL: ✓         ✓          ✓     DEL       SUB           ✓    ✓      SUB    ✓    ✓     INS   ✓         
```

#### Deepgram
- **Latency**: 3.22s | **Ref Words**: 11 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 4.0%

```text
REF : neither   headache   nor   stomach   ache   i    just   felt   a    bit   insomnia  
HYP : neither   headache   nor   stomach   ache   i    just   feel   a    bit   insomnia  
EVAL: ✓         ✓          ✓     ✓         ✓      ✓    ✓      SUB    ✓    ✓     ✓         
```

#### Gemini
- **Latency**: 3.95s | **Ref Words**: 11 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **27.3%** | **Word Accuracy**: **72.7%** | **CER**: 6.0%

```text
REF : neither   headache   nor   stomach   ache          i    just   felt   a    bit   insomnia  
HYP : neither   headache   nor   a         stomachache   i    just   feel   a    bit   insomnia  
EVAL: ✓         ✓          ✓     SUB       SUB           ✓    ✓      SUB    ✓    ✓     ✓         
```

---

### Voice: `v169.wav`
> **Ground Truth Reference**:
> *Everything is fine, there is no scary symptom.*

#### Sahara
- **Latency**: 5.05s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : everything   is   fine   there   is   no   scary   symptom  
HYP : everything   is   fine   there   is   no   scary   symptom  
EVAL: ✓            ✓    ✓      ✓       ✓    ✓    ✓       ✓        
```

#### Deepgram
- **Latency**: 3.34s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : everything   is   fine   there   is   no   scary   symptom  
HYP : everything   is   fine   there   is   no   scary   symptom  
EVAL: ✓            ✓    ✓      ✓       ✓    ✓    ✓       ✓        
```

#### Gemini
- **Latency**: 3.83s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : everything   is   fine   there   is   no   scary   symptom  
HYP : everything   is   fine   there   is   no   scary   symptom  
EVAL: ✓            ✓    ✓      ✓       ✓    ✓    ✓       ✓        
```

---
