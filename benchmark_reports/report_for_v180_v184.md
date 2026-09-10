# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v180_v184_en.json`
- **Ground Truth**: `transcript.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:59:59 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 89 | 3 | 1 | 1 | 1 | **3.4%** | **96.6%** | 0.5% | 5.35s |
| **Deepgram** | 89 | 3 | 2 | 1 | 0 | **3.4%** | **96.6%** | 0.5% | 4.38s |
| **Gemini** | 89 | 3 | 2 | 1 | 0 | **3.4%** | **96.6%** | 0.5% | 5.58s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v180.wav`
> **Ground Truth Reference**:
> *Clear fluid suddenly poured out down to my seat; it's not urination, I couldn't control it.*

#### Sahara
- **Latency**: 5.95s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : clear   fluid   suddenly   poured   out   down   to   my   seat   its   not   urination   i    couldnt   control   it  
HYP : clear   fluid   suddenly   poured   out   down   to   my   seat   its   not   urination   i    couldnt   control   it  
EVAL: ✓       ✓       ✓          ✓        ✓     ✓      ✓    ✓    ✓      ✓     ✓     ✓           ✓    ✓         ✓         ✓   
```

#### Deepgram
- **Latency**: 4.97s | **Ref Words**: 16 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **6.2%** | **Word Accuracy**: **93.8%** | **CER**: 1.4%

```text
REF : clear   fluid   suddenly   poured   out   down   to   my   seat    its   not   urination   i    couldnt   control   it  
HYP : clear   fluid   suddenly   poured   out   down   to   my   seats   its   not   urination   i    couldnt   control   it  
EVAL: ✓       ✓       ✓          ✓        ✓     ✓      ✓    ✓    SUB     ✓     ✓     ✓           ✓    ✓         ✓         ✓   
```

#### Gemini
- **Latency**: 3.47s | **Ref Words**: 16 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **6.2%** | **Word Accuracy**: **93.8%** | **CER**: 1.4%

```text
REF : clear   fluid   suddenly   poured   out   down   to   my   seat    its   not   urination   i    couldnt   control   it  
HYP : clear   fluid   suddenly   poured   out   down   to   my   seats   its   not   urination   i    couldnt   control   it  
EVAL: ✓       ✓       ✓          ✓        ✓     ✓      ✓    ✓    SUB     ✓     ✓     ✓           ✓    ✓         ✓         ✓   
```

---

### Voice: `v181.wav`
> **Ground Truth Reference**:
> *I am bleeding; it started flowing red just like menstrual period.*

#### Sahara
- **Latency**: 4.92s | **Ref Words**: 11 | **Errors**: 3 (S: 1, D: 1, I: 1)
- **WER**: **27.3%** | **Word Accuracy**: **72.7%** | **CER**: 3.8%

```text
REF : i     am    bleeding   it   started   flowing   red   just   like   ---   menstrual   period  
HYP : ---   im    bleeding   it   started   flowing   red   just   like   a     menstrual   period  
EVAL: DEL   SUB   ✓          ✓    ✓         ✓         ✓     ✓      ✓      INS   ✓           ✓       
```

#### Deepgram
- **Latency**: 4.18s | **Ref Words**: 11 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 1.9%

```text
REF : i     am    bleeding   it   started   flowing   red   just   like   menstrual   period  
HYP : ---   im    bleeding   it   started   flowing   red   just   like   menstrual   period  
EVAL: DEL   SUB   ✓          ✓    ✓         ✓         ✓     ✓      ✓      ✓           ✓       
```

#### Gemini
- **Latency**: 4.53s | **Ref Words**: 11 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 1.9%

```text
REF : i     am    bleeding   it   started   flowing   red   just   like   menstrual   period  
HYP : ---   im    bleeding   it   started   flowing   red   just   like   menstrual   period  
EVAL: DEL   SUB   ✓          ✓    ✓         ✓         ✓     ✓      ✓      ✓           ✓       
```

---

### Voice: `v182.wav`
> **Ground Truth Reference**:
> *Yes; I have a headache throbbing violently on my forehead, on top of that my vision is blurry, and my hands are so swollen I can't close my fingers.*

#### Sahara
- **Latency**: 5.05s | **Ref Words**: 29 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    have   a    headache   throbbing   violently   on   my   forehead   on   top   of   that   my   vision   is   blurry   and   my   hands   are   so   swollen   i    cant   close   my   fingers  
HYP : yes   i    have   a    headache   throbbing   violently   on   my   forehead   on   top   of   that   my   vision   is   blurry   and   my   hands   are   so   swollen   i    cant   close   my   fingers  
EVAL: ✓     ✓    ✓      ✓    ✓          ✓           ✓           ✓    ✓    ✓          ✓    ✓     ✓    ✓      ✓    ✓        ✓    ✓        ✓     ✓    ✓       ✓     ✓    ✓         ✓    ✓      ✓       ✓    ✓        
```

#### Deepgram
- **Latency**: 4.71s | **Ref Words**: 29 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    have   a    headache   throbbing   violently   on   my   forehead   on   top   of   that   my   vision   is   blurry   and   my   hands   are   so   swollen   i    cant   close   my   fingers  
HYP : yes   i    have   a    headache   throbbing   violently   on   my   forehead   on   top   of   that   my   vision   is   blurry   and   my   hands   are   so   swollen   i    cant   close   my   fingers  
EVAL: ✓     ✓    ✓      ✓    ✓          ✓           ✓           ✓    ✓    ✓          ✓    ✓     ✓    ✓      ✓    ✓        ✓    ✓        ✓     ✓    ✓       ✓     ✓    ✓         ✓    ✓      ✓       ✓    ✓        
```

#### Gemini
- **Latency**: 7.58s | **Ref Words**: 29 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    have   a    headache   throbbing   violently   on   my   forehead   on   top   of   that   my   vision   is   blurry   and   my   hands   are   so   swollen   i    cant   close   my   fingers  
HYP : yes   i    have   a    headache   throbbing   violently   on   my   forehead   on   top   of   that   my   vision   is   blurry   and   my   hands   are   so   swollen   i    cant   close   my   fingers  
EVAL: ✓     ✓    ✓      ✓    ✓          ✓           ✓           ✓    ✓    ✓          ✓    ✓     ✓    ✓      ✓    ✓        ✓    ✓        ✓     ✓    ✓       ✓     ✓    ✓         ✓    ✓      ✓       ✓    ✓        
```

---

### Voice: `v183.wav`
> **Ground Truth Reference**:
> *My abdomen feels stiff like a rock and hurts; and fluid mixed with blood is leaking down.*

#### Sahara
- **Latency**: 5.37s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   abdomen   feels   stiff   like   a    rock   and   hurts   and   fluid   mixed   with   blood   is   leaking   down  
HYP : my   abdomen   feels   stiff   like   a    rock   and   hurts   and   fluid   mixed   with   blood   is   leaking   down  
EVAL: ✓    ✓         ✓       ✓       ✓      ✓    ✓      ✓     ✓       ✓     ✓       ✓       ✓      ✓       ✓    ✓         ✓     
```

#### Deepgram
- **Latency**: 4.3s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   abdomen   feels   stiff   like   a    rock   and   hurts   and   fluid   mixed   with   blood   is   leaking   down  
HYP : my   abdomen   feels   stiff   like   a    rock   and   hurts   and   fluid   mixed   with   blood   is   leaking   down  
EVAL: ✓    ✓         ✓       ✓       ✓      ✓    ✓      ✓     ✓       ✓     ✓       ✓       ✓      ✓       ✓    ✓         ✓     
```

#### Gemini
- **Latency**: 9.12s | **Ref Words**: 17 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   abdomen   feels   stiff   like   a    rock   and   hurts   and   fluid   mixed   with   blood   is   leaking   down  
HYP : my   abdomen   feels   stiff   like   a    rock   and   hurts   and   fluid   mixed   with   blood   is   leaking   down  
EVAL: ✓    ✓         ✓       ✓       ✓      ✓    ✓      ✓     ✓       ✓     ✓       ✓       ✓      ✓       ✓    ✓         ✓     
```

---

### Voice: `v184.wav`
> **Ground Truth Reference**:
> *My body is burning hot with fever, and along with that my lower abdomen is cramping.*

#### Sahara
- **Latency**: 5.47s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   body   is   burning   hot   with   fever   and   along   with   that   my   lower   abdomen   is   cramping  
HYP : my   body   is   burning   hot   with   fever   and   along   with   that   my   lower   abdomen   is   cramping  
EVAL: ✓    ✓      ✓    ✓         ✓     ✓      ✓       ✓     ✓       ✓      ✓      ✓    ✓       ✓         ✓    ✓         
```

#### Deepgram
- **Latency**: 3.74s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   body   is   burning   hot   with   fever   and   along   with   that   my   lower   abdomen   is   cramping  
HYP : my   body   is   burning   hot   with   fever   and   along   with   that   my   lower   abdomen   is   cramping  
EVAL: ✓    ✓      ✓    ✓         ✓     ✓      ✓       ✓     ✓       ✓      ✓      ✓    ✓       ✓         ✓    ✓         
```

#### Gemini
- **Latency**: 3.22s | **Ref Words**: 16 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : my   body   is   burning   hot   with   fever   and   along   with   that   my   lower   abdomen   is   cramping  
HYP : my   body   is   burning   hot   with   fever   and   along   with   that   my   lower   abdomen   is   cramping  
EVAL: ✓    ✓      ✓    ✓         ✓     ✓      ✓       ✓     ✓       ✓      ✓      ✓    ✓       ✓         ✓    ✓         
```

---
