# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v111_v115_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:52:28 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 74 | 23 | 16 | 7 | 0 | **31.1%** | **68.9%** | 13.7% | 3.91s |
| **Addis Ai** | 74 | 50 | 45 | 4 | 1 | **67.6%** | **32.4%** | 75.9% | 4.25s |
| **Gemini** | 74 | 38 | 34 | 3 | 1 | **51.4%** | **48.6%** | 38.1% | 3.67s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v111.wav`
> **Ground Truth Reference**:
> *ጥሩ ሽታ የሌለው fluid እየፈሰሰኝ ነው፤ high temperature እና severe abdominal tenderness አብሮ አለ።*

#### Sahara
- **Latency**: 3.78s | **Ref Words**: 14 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **28.6%** | **Word Accuracy**: **71.4%** | **CER**: 11.8%

```text
REF : ጥሩ   ሽታ   የሌለው   fluid   እየፈሰሰኝ   ነው   high   temperature   እና    severe   abdominal   tenderness   አብሮ   አለ     
HYP : ጥሩ   ሽታ   የሌለው   fluid   እየፈሰሰ    ነው   high   temperature   no    severe   abdominal   tenderness   ---   ovral  
EVAL: ✓    ✓    ✓      ✓       SUB      ✓    ✓      ✓             SUB   ✓        ✓           ✓            DEL   SUB    
```

#### Addis Ai
- **Latency**: 5.14s | **Ref Words**: 14 | **Errors**: 8 (S: 7, D: 1, I: 0)
- **WER**: **57.1%** | **Word Accuracy**: **42.9%** | **CER**: 70.6%

```text
REF : ጥሩ   ሽታ   የሌለው   fluid   እየፈሰሰኝ   ነው   high   temperature   እና   severe   abdominal   tenderness   አብሮ      አለ    
HYP : ጥሩ   ሽታ   የሌለው   ፍሉድ     እየፈሰሰኝ   ነው   ሃይ     ቴምፕሬቸር        እና   ---      ሰቪር         አብዶሚናል       ቴንደርነስ   አብሯል  
EVAL: ✓    ✓    ✓      SUB     ✓        ✓    SUB    SUB           ✓    DEL      SUB         SUB          SUB      SUB   
```

#### Gemini
- **Latency**: 3.6s | **Ref Words**: 14 | **Errors**: 6 (S: 5, D: 1, I: 0)
- **WER**: **42.9%** | **Word Accuracy**: **57.1%** | **CER**: 25.0%

```text
REF : ጥሩ   ሽታ       የሌለው   fluid   እየፈሰሰኝ   ነው   high   temperature   እና    severe   abdominal   tenderness   አብሮ   አለ    
HYP : ጥሩ   shutil   ያለው    ፍሉድ     እየፈሰሰኝ   ነው   high   temperature   no    severe   abdominal   tenderness   ---   አብሯል  
EVAL: ✓    SUB      SUB    SUB     ✓        ✓    ✓      ✓             SUB   ✓        ✓           ✓            DEL   SUB   
```

---

### Voice: `v112.wav`
> **Ground Truth Reference**:
> *I am confused… dischargeኡ pinkish ነው፤ does this qualify as bleeding ወይስ normal mucus ነው?*

#### Sahara
- **Latency**: 3.84s | **Ref Words**: 15 | **Errors**: 6 (S: 4, D: 2, I: 0)
- **WER**: **40.0%** | **Word Accuracy**: **60.0%** | **CER**: 13.9%

```text
REF : i     am    confused…   dischargeኡ   pinkish   ነው   does   this   qualify   as   bleeding   ወይስ   normal   mucus   ነው  
HYP : ---   im    confused    discharge    pinkish   ነው   ---    this   qualify   as   bleeding   way   normal   mucus   ነው  
EVAL: DEL   SUB   SUB         SUB          ✓         ✓    DEL    ✓      ✓         ✓    ✓          SUB   ✓        ✓       ✓   
```

#### Addis Ai
- **Latency**: 3.52s | **Ref Words**: 15 | **Errors**: 12 (S: 10, D: 2, I: 0)
- **WER**: **80.0%** | **Word Accuracy**: **20.0%** | **CER**: 90.3%

```text
REF : i     am    confused…   dischargeኡ   pinkish   ነው   does   this   qualify   as      bleeding   ወይስ   normal   mucus   ነው  
HYP : ---   አም    ኮንፊውዝድ      ዲስቻርጁ        ፒንኪሽ      ነው   ---    ደስ     ዲስ        ኳሊፋይስ   ብሊዲንግ      ወይስ   ኖርማል     ሚውከስ    ነው  
EVAL: DEL   SUB   SUB         SUB          SUB       ✓    DEL    SUB    SUB       SUB     SUB        ✓     SUB      SUB     ✓   
```

#### Gemini
- **Latency**: 2.85s | **Ref Words**: 15 | **Errors**: 10 (S: 8, D: 2, I: 0)
- **WER**: **66.7%** | **Word Accuracy**: **33.3%** | **CER**: 23.6%

```text
REF : i     am    confused…   dischargeኡ   pinkish   ነው    does    this   qualify   as          bleeding   ወይስ    normal   mucus   ነው   
HYP : ---   im    confused    discharge    pinkish   no    thats   this   ---       qualifies   bleeding   with   normal   mucus   no   
EVAL: DEL   SUB   SUB         SUB          ✓         SUB   SUB     ✓      DEL       SUB         ✓          SUB    ✓        ✓       SUB  
```

---

### Voice: `v113.wav`
> **Ground Truth Reference**:
> *Dizziness አለኝ but headache የለም፤ sugarሬ drop አድርጎ ይሆን ወይስ its sign of hypertension?*

#### Sahara
- **Latency**: 3.88s | **Ref Words**: 14 | **Errors**: 7 (S: 4, D: 3, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 28.4%

```text
REF : dizziness   አለኝ   but   headache   የለም   sugarሬ   drop   አድርጎ   ይሆን       ወይስ       its   sign   of   hypertension  
HYP : dizziness   አለኝ   በ     headache   የለም   ---      ---    ---    suggere   dropers   a     sign   of   hypertension  
EVAL: ✓           ✓     SUB   ✓          ✓     DEL      DEL    DEL    SUB       SUB       SUB   ✓      ✓    ✓             
```

#### Addis Ai
- **Latency**: 3.57s | **Ref Words**: 14 | **Errors**: 10 (S: 9, D: 0, I: 1)
- **WER**: **71.4%** | **Word Accuracy**: **28.6%** | **CER**: 74.6%

```text
REF : dizziness   አለኝ   but   headache   የለም   sugarሬ   drop   አድርጎ   ይሆን   ወይስ   ---   its   sign   of    hypertension  
HYP : ዲዚነስ        አለኝ   በት    ሄዴክ        የለም   ሹገሬ      ዶፕ     አድርጎ   ይሆን   ወይስ   ኢትስ   ኤ     ሳይን    ኦፍ    ሃይፐርቴንሽን      
EVAL: SUB         ✓     SUB   SUB        ✓     SUB      SUB    ✓      ✓     ✓     INS   SUB   SUB    SUB   SUB           
```

#### Gemini
- **Latency**: 3.83s | **Ref Words**: 14 | **Errors**: 11 (S: 10, D: 0, I: 1)
- **WER**: **78.6%** | **Word Accuracy**: **21.4%** | **CER**: 77.6%

```text
REF : ---   dizziness   አለኝ   but   headache   የለም   sugarሬ   drop   አድርጎ   ይሆን   ወይስ   its   sign   of    hypertension  
HYP : ድካም   ስሜት         አለኝ   ብት    ሄድኬ        የለም   ሡገር      ይድሮፕ   አርጎ    ይሆን   ወይስ   ዘ     ሳይን    ኦፍ    ሃይፐርቴንሽን      
EVAL: INS   SUB         ✓     SUB   SUB        ✓     SUB      SUB    SUB    ✓     ✓     SUB   SUB    SUB   SUB           
```

---

### Voice: `v114.wav`
> **Ground Truth Reference**:
> *Watery ፈሳሽ አለ ግን control ማድረግ እችላለሁ፤ urine leakage ይሁን ወይስ amniotic fluid እርግጠኛ አይደለሁም።*

#### Sahara
- **Latency**: 4.72s | **Ref Words**: 15 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **13.3%** | **Word Accuracy**: **86.7%** | **CER**: 4.2%

```text
REF : watery   ፈሳሽ   አለ   ግን   control   ማድረግ   እችላለሁ   urine   leakage   ይሁን   ወይስ   amniotic   fluid   እርግጠኛ   አይደለሁም  
HYP : watery   ፈሳሽ   አለ   ግን   control   ማድረግ   እችላለሁ   urine   leakage   ይሆን   ወይስ   aminotic   fluid   እርግጠኛ   አይደለሁም  
EVAL: ✓        ✓     ✓    ✓    ✓         ✓      ✓       ✓       ✓         SUB   ✓     SUB        ✓       ✓       ✓       
```

#### Addis Ai
- **Latency**: 4.31s | **Ref Words**: 15 | **Errors**: 7 (S: 7, D: 0, I: 0)
- **WER**: **46.7%** | **Word Accuracy**: **53.3%** | **CER**: 54.9%

```text
REF : watery   ፈሳሽ   አለ   ግን   control   ማድረግ   እችላለሁ   urine   leakage   ይሁን   ወይስ   amniotic   fluid   እርግጠኛ   አይደለሁም  
HYP : ዋተሪ      ፈሳሽ   አለ   ግን   ኮንትሮል     ማድረግ   እችላለሁ   ዩሪን     ሊኬጅ       ይሆን   ወይስ   አሚኖቲክ      ፍሉድ     እርግጠኛ   አይደለሁም  
EVAL: SUB      ✓     ✓    ✓    SUB       ✓      ✓       SUB     SUB       SUB   ✓     SUB        SUB     ✓       ✓       
```

#### Gemini
- **Latency**: 4.0s | **Ref Words**: 15 | **Errors**: 10 (S: 10, D: 0, I: 0)
- **WER**: **66.7%** | **Word Accuracy**: **33.3%** | **CER**: 64.8%

```text
REF : watery   ፈሳሽ   አለ      ግን   control   ማድረግ   እችላለሁ   urine   leakage   ይሁን   ወይስ   amniotic   fluid   እርግጠኛ   አይደለሁም  
HYP : ውሃ       ተረፍ   ይሰማሻል   ግን   ኮንትሮል     ማድረግ   ትችላለህ   ዩሪን     ሊኬጅ       ይሆን   ወይስ   አሚኖቲክ      ፍሉድ     እርግጠኛ   አይደለሁም  
EVAL: SUB      SUB   SUB     ✓    SUB       ✓      SUB     SUB     SUB       SUB   ✓     SUB        SUB     ✓       ✓       
```

---

### Voice: `v115.wav`
> **Ground Truth Reference**:
> *A little bit lower back ache አለኝ፤ nothing severe ግን irregular contractions ይመስላል፣ should I worry?*

#### Sahara
- **Latency**: 3.31s | **Ref Words**: 16 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 11.4%

```text
REF : a    little   bit   lower   back   ache   አለኝ   nothing   severe   ግን   irregular   contractions   ይመስላል   should   i    worry  
HYP : a    little   bet   low     back   ---    አለኝ   nothing   severe   ግን   irregular   contractions   ይመስላል   should   i    wary   
EVAL: ✓    ✓        SUB   SUB     ✓      DEL    ✓     ✓         ✓        ✓    ✓           ✓              ✓       ✓        ✓    SUB    
```

#### Addis Ai
- **Latency**: 4.72s | **Ref Words**: 16 | **Errors**: 13 (S: 12, D: 1, I: 0)
- **WER**: **81.2%** | **Word Accuracy**: **18.8%** | **CER**: 87.3%

```text
REF : a     little   bit   lower   back   ache   አለኝ   nothing   severe   ግን   irregular   contractions   ይመስላል   should   i     worry  
HYP : ---   አሊትል     ቤት    ሎር      ባክ     ኤክ     አለኝ   ነቲንግ      ሳይቪር     ግን   ኢሬጉላር       ኮንትራክሽንስ       ይመስላል   ሹድ       አይ    ወሪ     
EVAL: DEL   SUB      SUB   SUB     SUB    SUB    ✓     SUB       SUB      ✓    SUB         SUB            ✓       SUB      SUB   SUB    
```

#### Gemini
- **Latency**: 4.08s | **Ref Words**: 16 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **6.2%** | **Word Accuracy**: **93.8%** | **CER**: 5.1%

```text
REF : a    little   bit   lower   back   ache   አለኝ   nothing   severe   ግን   irregular   contractions   ይመስላል   should   i    worry  
HYP : a    little   bit   lower   back   pain   አለኝ   nothing   severe   ግን   irregular   contractions   ይመስላል   should   i    worry  
EVAL: ✓    ✓        ✓     ✓       ✓      SUB    ✓     ✓         ✓        ✓    ✓           ✓              ✓       ✓        ✓    ✓      
```

---
