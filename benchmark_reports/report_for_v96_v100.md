# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v96_v100_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:51:54 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 64 | 18 | 13 | 3 | 2 | **28.1%** | **71.9%** | 12.1% | 3.34s |
| **Addis Ai** | 64 | 48 | 45 | 2 | 1 | **75.0%** | **25.0%** | 81.5% | 3.75s |
| **Gemini** | 64 | 28 | 22 | 3 | 3 | **43.8%** | **56.2%** | 41.1% | 3.52s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v96.wav`
> **Ground Truth Reference**:
> *Severe cramp አይደለም፤ just slight bloating and indigestion ነው፣ I took antacid.*

#### Sahara
- **Latency**: 3.31s | **Ref Words**: 12 | **Errors**: 5 (S: 4, D: 0, I: 1)
- **WER**: **41.7%** | **Word Accuracy**: **58.3%** | **CER**: 4.8%

```text
REF : severe   cramp   አይደለም   just   slight   bloating   and   ---   indigestion   ነው   i    took   antacid   
HYP : severe   crump   አይደለም   just   slight   bloating   and   in    digestion     ነው   i    to     cantacid  
EVAL: ✓        SUB     ✓       ✓      ✓        ✓          ✓     INS   SUB           ✓    ✓    SUB    SUB       
```

#### Addis Ai
- **Latency**: 3.58s | **Ref Words**: 12 | **Errors**: 10 (S: 9, D: 1, I: 0)
- **WER**: **83.3%** | **Word Accuracy**: **16.7%** | **CER**: 88.7%

```text
REF : severe   cramp   አይደለም   just   slight   bloating   and   indigestion   ነው   i     took   antacid  
HYP : ሰቪር      ካምፕ     አይደለም   ጀስት    ስላይት     ብሎቲንግ      ኤንድ   ኢንዳይጀሽን       ነው   ---   አይቱ    ካንታሲድ    
EVAL: SUB      SUB     ✓       SUB    SUB      SUB        SUB   SUB           ✓    DEL   SUB    SUB      
```

#### Gemini
- **Latency**: 3.38s | **Ref Words**: 12 | **Errors**: 10 (S: 8, D: 2, I: 0)
- **WER**: **83.3%** | **Word Accuracy**: **16.7%** | **CER**: 88.7%

```text
REF : severe   cramp    አይደለም   just   slight   bloating   and   indigestion   ነው   i     took   antacid  
HYP : ---      ሰቪርክራም   አይደለም   ጀስት    ስላይት     ብሎቲንግ      ኤንድ   ኢንዲጀስሽን       ነው   ---   አይ     ቱካንታሲድ   
EVAL: DEL      SUB      ✓       SUB    SUB      SUB        SUB   SUB           ✓    DEL   SUB    SUB      
```

---

### Voice: `v97.wav`
> **Ground Truth Reference**:
> *እግሬ ላይ mild swelling አለ because of the standing, but hands and face totally clear ናቸው no swelling*

#### Sahara
- **Latency**: 3.02s | **Ref Words**: 18 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **22.2%** | **Word Accuracy**: **77.8%** | **CER**: 11.4%

```text
REF : እግሬ   ላይ   mild   swelling   አለ   because   of   the   standing   but   hands   and    face   totally   clear   ናቸው   no     swelling  
HYP : እግሬ   ላይ   mild   swelling   አለ   because   of   the   standing   but   my      hand   face   totally   clear   ---   noto   swelling  
EVAL: ✓     ✓    ✓      ✓          ✓    ✓         ✓    ✓     ✓          ✓     SUB     SUB    ✓      ✓         ✓       DEL   SUB    ✓         
```

#### Addis Ai
- **Latency**: 4.3s | **Ref Words**: 18 | **Errors**: 15 (S: 14, D: 0, I: 1)
- **WER**: **83.3%** | **Word Accuracy**: **16.7%** | **CER**: 87.3%

```text
REF : እግሬ   ላይ   mild   swelling   አለ   ---   because   of    the      standing   but   hands   and   face   totally   clear   ናቸው   no    swelling  
HYP : እግሬ   ላይ   ማይልድ   ስዌሊንግ      አለ   ቢኮዝ   ኦፍ        ዘ     ስታንዲንግ   በት         ማይ    ሃንድስ    ኤንድ   ፌስ     ቶታሊ       ክሊር     ናቸው   ኖ     ስዌሊንግ     
EVAL: ✓     ✓    SUB    SUB        ✓    INS   SUB       SUB   SUB      SUB        SUB   SUB     SUB   SUB    SUB       SUB     ✓     SUB   SUB       
```

#### Gemini
- **Latency**: 3.89s | **Ref Words**: 18 | **Errors**: 3 (S: 1, D: 0, I: 2)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 10.1%

```text
REF : እግሬ   ላይ   mild   swelling   አለ   because   of   the   standing   but   ---   hands   and   face   totally   clear   ---   ናቸው    no   swelling  
HYP : እግሬ   ላይ   mild   swelling   አለ   because   of   the   standing   but   my    hands   and   face   totally   clear   ነው    show   no   swelling  
EVAL: ✓     ✓    ✓      ✓          ✓    ✓         ✓    ✓     ✓          ✓     INS   ✓       ✓     ✓      ✓         ✓       INS   SUB    ✓    ✓         
```

---

### Voice: `v98.wav`
> **Ground Truth Reference**:
> *Sharp pain አይደለም፤ just ligament stretch መሰለኝ፣ ቶሎ ነው relief ያገኘሁት።*

#### Sahara
- **Latency**: 3.43s | **Ref Words**: 11 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **27.3%** | **Word Accuracy**: **72.7%** | **CER**: 26.9%

```text
REF : sharp   pain   አይደለም   just   ligament   stretch   መሰለኝ       ቶሎ   ነው    relief   ያገኘሁት  
HYP : sharp   pain   አይደለም   just   ligament   stretch   muscling   ቶሎ   ---   ሪሊፍ      ያገኘሁት  
EVAL: ✓       ✓      ✓       ✓      ✓          ✓         SUB        ✓    DEL   SUB      ✓      
```

#### Addis Ai
- **Latency**: 3.69s | **Ref Words**: 11 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **54.5%** | **Word Accuracy**: **45.5%** | **CER**: 65.4%

```text
REF : sharp   pain   አይደለም   just   ligament   stretch   መሰለኝ   ቶሎ   ነው   relief   ያገኘሁት  
HYP : ሻርፕ     ፔይን    አይደለም   ጀስት    ሪሊጋመንት     ስትረች      መሰለኝ   ቶሎ   ነው   ሪሊፍ      ያገኘሁት  
EVAL: SUB     SUB    ✓       SUB    SUB        SUB       ✓      ✓    ✓    SUB      ✓      
```

#### Gemini
- **Latency**: 3.07s | **Ref Words**: 11 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 7.7%

```text
REF : sharp   pain   አይደለም   just   ligament   stretch   መሰለኝ   ቶሎ   ነው   relief   ያገኘሁት    
HYP : sharp   pain   አይደለም   just   ligament   stretch   መሰልኝ   ቶሎ   ነው   relief   የሚያገኘውት  
EVAL: ✓       ✓      ✓       ✓      ✓          ✓         SUB    ✓    ✓    ✓        SUB      
```

---

### Voice: `v99.wav`
> **Ground Truth Reference**:
> *Morning nausea ነበረኝ but no persistent vomiting፤ breakfast በልቼ normal ሆኗል።*

#### Sahara
- **Latency**: 3.22s | **Ref Words**: 11 | **Errors**: 4 (S: 3, D: 0, I: 1)
- **WER**: **36.4%** | **Word Accuracy**: **63.6%** | **CER**: 13.1%

```text
REF : morning   nausea   ነበረኝ   but   no    persistent   vomiting   breakfast   በልቼ   ---   normal   ሆኗል  
HYP : morning   nausea   ነበረኝ   but   nor   persistant   vomiting   breakfast   በልቼ   ኖሮ    ማለት      ሆኗል  
EVAL: ✓         ✓        ✓      ✓     SUB   SUB          ✓          ✓           ✓     INS   SUB      ✓    
```

#### Addis Ai
- **Latency**: 3.69s | **Ref Words**: 11 | **Errors**: 8 (S: 8, D: 0, I: 0)
- **WER**: **72.7%** | **Word Accuracy**: **27.3%** | **CER**: 83.6%

```text
REF : morning   nausea   ነበረኝ   but   no    persistent   vomiting   breakfast   በልቼ   normal   ሆኗል  
HYP : ሞርኒንግ     ኖርሺያ     ነበረኝ   በት    ኖ     ፕሪዝስተንት      ቫሚቲንግ      ብሬክፋስት      በልቼ   ኖርማል     ሆኗል  
EVAL: SUB       SUB      ✓      SUB   SUB   SUB          SUB        SUB         ✓     SUB      ✓    
```

#### Gemini
- **Latency**: 3.8s | **Ref Words**: 11 | **Errors**: 9 (S: 8, D: 0, I: 1)
- **WER**: **81.8%** | **Word Accuracy**: **18.2%** | **CER**: 83.6%

```text
REF : morning   nausea   ነበረኝ   but   no    persistent   vomiting   breakfast   በልቼ   ---   normal   ሆኗል  
HYP : ሞርኒንግ     ናውሺያ     ነበረኝ   በት    ናው    ፕሪስትንት       ቫሚቲንግ      ብሬክፋስት      በልቼ   ኢን    ኖርማል     ሆኗል  
EVAL: SUB       SUB      ✓      SUB   SUB   SUB          SUB        SUB         ✓     INS   SUB      ✓    
```

---

### Voice: `v100.wav`
> **Ground Truth Reference**:
> *Pelvic pressure ይሰማኛል as the baby drops, but labor contraction ደረጃ አይደለም።*

#### Sahara
- **Latency**: 3.73s | **Ref Words**: 12 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 6.7%

```text
REF : pelvic   pressure   ይሰማኛል   as   the   baby   drops   but   labor   contraction   ደረጃ   አይደለም  
HYP : pelvic   pressure   ይሰማኛል   as   the   baby   drops   ---   lavor   contraction   ደረጃ   አይደለም  
EVAL: ✓        ✓          ✓       ✓    ✓     ✓      ✓       DEL   SUB     ✓             ✓     ✓      
```

#### Addis Ai
- **Latency**: 3.48s | **Ref Words**: 12 | **Errors**: 9 (S: 8, D: 1, I: 0)
- **WER**: **75.0%** | **Word Accuracy**: **25.0%** | **CER**: 78.3%

```text
REF : pelvic   pressure   ይሰማኛል   as    the   baby   drops   but   labor   contraction   ደረጃ   አይደለም  
HYP : ፔልቪክ     ፕሬዘር       ይሰማኛል   ---   አስደ   ቤቢ     ድሮፕስ    በት    ሊቨር     ኮንትራክሽን       ደረጃ   አይደለም  
EVAL: SUB      SUB        ✓       DEL   SUB   SUB    SUB     SUB   SUB     SUB           ✓     ✓      
```

#### Gemini
- **Latency**: 3.48s | **Ref Words**: 12 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 18.3%

```text
REF : pelvic   pressure   ይሰማኛል   as    the   baby   drops   but   labor   contraction   ደረጃ   አይደለም  
HYP : pelvic   pressure   ይሰማኛል   ---   አስደ   baby   drops   በ     liver   contraction   ደረጃ   አይደለም  
EVAL: ✓        ✓          ✓       DEL   SUB   ✓      ✓       SUB   SUB     ✓             ✓     ✓      
```

---
