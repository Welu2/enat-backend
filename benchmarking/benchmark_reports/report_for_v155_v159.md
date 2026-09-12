# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v155_v159_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:58:46 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 82 | 0 | 0 | 0 | 0 | **0.0%** | **100.0%** | 0.0% | 4.81s |
| **Deepgram** | 82 | 0 | 0 | 0 | 0 | **0.0%** | **100.0%** | 0.0% | 4.10s |
| **Gemini** | 82 | 0 | 0 | 0 | 0 | **0.0%** | **100.0%** | 0.0% | 4.23s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v155.wav`
> **Ground Truth Reference**:
> *No pain, but the baby's movements have completely stopped since yesterday, I feel nothing.*

#### Sahara
- **Latency**: 5.08s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   pain   but   the   babys   movements   have   completely   stopped   since   yesterday   i    feel   nothing  
HYP : no   pain   but   the   babys   movements   have   completely   stopped   since   yesterday   i    feel   nothing  
EVAL: ✓    ✓      ✓     ✓     ✓       ✓           ✓      ✓            ✓         ✓       ✓           ✓    ✓      ✓        
```

#### Deepgram
- **Latency**: 4.4s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   pain   but   the   babys   movements   have   completely   stopped   since   yesterday   i    feel   nothing  
HYP : no   pain   but   the   babys   movements   have   completely   stopped   since   yesterday   i    feel   nothing  
EVAL: ✓    ✓      ✓     ✓     ✓       ✓           ✓      ✓            ✓         ✓       ✓           ✓    ✓      ✓        
```

#### Gemini
- **Latency**: 5.02s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : no   pain   but   the   babys   movements   have   completely   stopped   since   yesterday   i    feel   nothing  
HYP : no   pain   but   the   babys   movements   have   completely   stopped   since   yesterday   i    feel   nothing  
EVAL: ✓    ✓      ✓     ✓     ✓       ✓           ✓      ✓            ✓         ✓       ✓           ✓    ✓      ✓        
```

---

### Voice: `v156.wav`
> **Ground Truth Reference**:
> *I have a high fever, my entire body is shivering; I feel very cold.*

#### Sahara
- **Latency**: 3.99s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   a    high   fever   my   entire   body   is   shivering   i    feel   very   cold  
HYP : i    have   a    high   fever   my   entire   body   is   shivering   i    feel   very   cold  
EVAL: ✓    ✓      ✓    ✓      ✓       ✓    ✓        ✓      ✓    ✓           ✓    ✓      ✓      ✓     
```

#### Deepgram
- **Latency**: 4.24s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   a    high   fever   my   entire   body   is   shivering   i    feel   very   cold  
HYP : i    have   a    high   fever   my   entire   body   is   shivering   i    feel   very   cold  
EVAL: ✓    ✓      ✓    ✓      ✓       ✓    ✓        ✓      ✓    ✓           ✓    ✓      ✓      ✓     
```

#### Gemini
- **Latency**: 4.0s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   a    high   fever   my   entire   body   is   shivering   i    feel   very   cold  
HYP : i    have   a    high   fever   my   entire   body   is   shivering   i    feel   very   cold  
EVAL: ✓    ✓      ✓    ✓      ✓       ✓    ✓        ✓      ✓    ✓           ✓    ✓      ✓      ✓     
```

---

### Voice: `v157.wav`
> **Ground Truth Reference**:
> *I'm short of breath; when I lie down my chest feels tight, breathing is so difficult.*

#### Sahara
- **Latency**: 5.06s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : im   short   of   breath   when   i    lie   down   my   chest   feels   tight   breathing   is   so   difficult  
HYP : im   short   of   breath   when   i    lie   down   my   chest   feels   tight   breathing   is   so   difficult  
EVAL: ✓    ✓       ✓    ✓        ✓      ✓    ✓     ✓      ✓    ✓       ✓       ✓       ✓           ✓    ✓    ✓          
```

#### Deepgram
- **Latency**: 4.61s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : im   short   of   breath   when   i    lie   down   my   chest   feels   tight   breathing   is   so   difficult  
HYP : im   short   of   breath   when   i    lie   down   my   chest   feels   tight   breathing   is   so   difficult  
EVAL: ✓    ✓       ✓    ✓        ✓      ✓    ✓     ✓      ✓    ✓       ✓       ✓       ✓           ✓    ✓    ✓          
```

#### Gemini
- **Latency**: 4.73s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : im   short   of   breath   when   i    lie   down   my   chest   feels   tight   breathing   is   so   difficult  
HYP : im   short   of   breath   when   i    lie   down   my   chest   feels   tight   breathing   is   so   difficult  
EVAL: ✓    ✓       ✓    ✓        ✓      ✓    ✓     ✓      ✓    ✓       ✓       ✓       ✓           ✓    ✓    ✓          
```

---

### Voice: `v158.wav`
> **Ground Truth Reference**:
> *Yes; since yesterday my head is pounding like a hammer, my vision has black spots, and my face is swollen.*

#### Sahara
- **Latency**: 4.76s | **Ref Words**: 20 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   since   yesterday   my   head   is   pounding   like   a    hammer   my   vision   has   black   spots   and   my   face   is   swollen  
HYP : yes   since   yesterday   my   head   is   pounding   like   a    hammer   my   vision   has   black   spots   and   my   face   is   swollen  
EVAL: ✓     ✓       ✓           ✓    ✓      ✓    ✓          ✓      ✓    ✓        ✓    ✓        ✓     ✓       ✓       ✓     ✓    ✓      ✓    ✓        
```

#### Deepgram
- **Latency**: 3.79s | **Ref Words**: 20 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   since   yesterday   my   head   is   pounding   like   a    hammer   my   vision   has   black   spots   and   my   face   is   swollen  
HYP : yes   since   yesterday   my   head   is   pounding   like   a    hammer   my   vision   has   black   spots   and   my   face   is   swollen  
EVAL: ✓     ✓       ✓           ✓    ✓      ✓    ✓          ✓      ✓    ✓        ✓    ✓        ✓     ✓       ✓       ✓     ✓    ✓      ✓    ✓        
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 20 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   since   yesterday   my   head   is   pounding   like   a    hammer   my   vision   has   black   spots   and   my   face   is   swollen  
HYP : yes   since   yesterday   my   head   is   pounding   like   a    hammer   my   vision   has   black   spots   and   my   face   is   swollen  
EVAL: ✓     ✓       ✓           ✓    ✓      ✓    ✓          ✓      ✓    ✓        ✓    ✓        ✓     ✓       ✓       ✓     ✓    ✓      ✓    ✓        
```

---

### Voice: `v159.wav`
> **Ground Truth Reference**:
> *I'm feeling sharp cramps on my lower abdomen, and red blood is leaking with it. Help me quickly.*

#### Sahara
- **Latency**: 5.16s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : im   feeling   sharp   cramps   on   my   lower   abdomen   and   red   blood   is   leaking   with   it   help   me   quickly  
HYP : im   feeling   sharp   cramps   on   my   lower   abdomen   and   red   blood   is   leaking   with   it   help   me   quickly  
EVAL: ✓    ✓         ✓       ✓        ✓    ✓    ✓       ✓         ✓     ✓     ✓       ✓    ✓         ✓      ✓    ✓      ✓    ✓        
```

#### Deepgram
- **Latency**: 3.47s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : im   feeling   sharp   cramps   on   my   lower   abdomen   and   red   blood   is   leaking   with   it   help   me   quickly  
HYP : im   feeling   sharp   cramps   on   my   lower   abdomen   and   red   blood   is   leaking   with   it   help   me   quickly  
EVAL: ✓    ✓         ✓       ✓        ✓    ✓    ✓       ✓         ✓     ✓     ✓       ✓    ✓         ✓      ✓    ✓      ✓    ✓        
```

#### Gemini
- **Latency**: 3.7s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : im   feeling   sharp   cramps   on   my   lower   abdomen   and   red   blood   is   leaking   with   it   help   me   quickly  
HYP : im   feeling   sharp   cramps   on   my   lower   abdomen   and   red   blood   is   leaking   with   it   help   me   quickly  
EVAL: ✓    ✓         ✓       ✓        ✓    ✓    ✓       ✓         ✓     ✓     ✓       ✓    ✓         ✓      ✓    ✓      ✓    ✓        
```

---
