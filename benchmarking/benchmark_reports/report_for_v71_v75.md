# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v71_v75_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:50:56 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 64 | 14 | 10 | 4 | 0 | **21.9%** | **78.1%** | 13.5% | 3.73s |
| **Addis Ai** | 64 | 41 | 37 | 0 | 4 | **64.1%** | **35.9%** | 71.2% | 4.12s |
| **Gemini** | 64 | 26 | 24 | 1 | 1 | **40.6%** | **59.4%** | 36.3% | 4.89s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v71.wav`
> **Ground Truth Reference**:
> *Severe pain የለም፤ just ትንሽ heartburn እና acidity ነው የሚያስቸግረኝ።*

#### Sahara
- **Latency**: 3.31s | **Ref Words**: 10 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 8.3%

```text
REF : severe   pain   የለም   just   ትንሽ   heartburn   እና   acidity   ነው   የሚያስቸግረኝ  
HYP : severe   pain   የለም   just   ትንሽ   hertburn    እና   acid      ነው   የሚያስቸግረኝ  
EVAL: ✓        ✓      ✓     ✓      ✓     SUB         ✓    SUB       ✓    ✓         
```

#### Addis Ai
- **Latency**: 3.82s | **Ref Words**: 10 | **Errors**: 6 (S: 5, D: 0, I: 1)
- **WER**: **60.0%** | **Word Accuracy**: **40.0%** | **CER**: 62.5%

```text
REF : severe   pain   የለም   just   ትንሽ   ---   heartburn   እና   acidity   ነው   የሚያስቸግረኝ  
HYP : ሰቪር      ፔን     የለም   ጀስት    ትንሽ   ሀርት   በርን         እና   አሲዲቲ      ነው   የሚያስቸግረኝ  
EVAL: SUB      SUB    ✓     SUB    ✓     INS   SUB         ✓    SUB       ✓    ✓         
```

#### Gemini
- **Latency**: 4.75s | **Ref Words**: 10 | **Errors**: 3 (S: 2, D: 0, I: 1)
- **WER**: **30.0%** | **Word Accuracy**: **70.0%** | **CER**: 4.2%

```text
REF : severe   pain   የለም   just   ትንሽ   ---     heartburn   እና    acidity   ነው   የሚያስቸግረኝ  
HYP : severe   pain   የለም   just   ትንሽ   heart   burn        ነው    acidity   ነው   የሚያስቸግረኝ  
EVAL: ✓        ✓      ✓     ✓      ✓     INS     SUB         SUB   ✓         ✓    ✓         
```

---

### Voice: `v72.wav`
> **Ground Truth Reference**:
> *እንትን… morning sickness ትንሽ ነበረኝ፤ but vomiting የለም፣ አሁን better ነኝ።*

#### Sahara
- **Latency**: 4.04s | **Ref Words**: 11 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **27.3%** | **Word Accuracy**: **72.7%** | **CER**: 26.9%

```text
REF : እንትን…   morning   sickness   ትንሽ   ነበረኝ   but   vomiting   የለም   አሁን   better   ነኝ  
HYP : ---     morning   sickness   ትንሽ   ነበረኝ   በ     vomiting   የለም   አሁን   ቤት       ነኝ  
EVAL: DEL     ✓         ✓          ✓     ✓      SUB   ✓          ✓     ✓     SUB      ✓   
```

#### Addis Ai
- **Latency**: 4.09s | **Ref Words**: 11 | **Errors**: 9 (S: 6, D: 0, I: 3)
- **WER**: **81.8%** | **Word Accuracy**: **18.2%** | **CER**: 76.9%

```text
REF : እንትን…   morning   sickness   ትንሽ   ነበረኝ   ---   ---    ---    but    vomiting   የለም   አሁን   better   ነኝ  
HYP : እንትን    ሞርኒንግ     ሲክነስ       ትንሽ   ነበረኝ   በት    0xe1   0x89   0xae   ሚቲንግ       የለም   አሁን   ቤተር      ነኝ  
EVAL: SUB     SUB       SUB        ✓     ✓      INS   INS    INS    SUB    SUB        ✓     ✓     SUB      ✓   
```

#### Gemini
- **Latency**: 3.93s | **Ref Words**: 11 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 5.8%

```text
REF : እንትን…   morning   sickness   ትንሽ   ነበረኝ   but   vomiting   የለም   አሁን   better   ነኝ  
HYP : እኔን     morning   sickness   ትንሽ   ነበረኝ   but   vomiting   የለም   አሁን   better   ነኝ  
EVAL: SUB     ✓         ✓          ✓     ✓      ✓     ✓          ✓     ✓     ✓        ✓   
```

---

### Voice: `v73.wav`
> **Ground Truth Reference**:
> *እግሬ ላይ mild swelling አለ፤ but mostly long time ስቆም ነው፣ face እና hand ግን normal ናቸው።*

#### Sahara
- **Latency**: 3.53s | **Ref Words**: 17 | **Errors**: 3 (S: 1, D: 2, I: 0)
- **WER**: **17.6%** | **Word Accuracy**: **82.3%** | **CER**: 9.7%

```text
REF : እግሬ   ላይ   mild   swelling   አለ   but   mostly   long   time   ስቆም   ነው   face   እና   hand   ግን    normal   ናቸው  
HYP : እግሬ   ላይ   mild   swelling   አለ   ---   mosly    long   time   ስቆም   ነው   face   እና   hand   ---   normal   ናቸው  
EVAL: ✓     ✓    ✓      ✓          ✓    DEL   SUB      ✓      ✓      ✓     ✓    ✓      ✓    ✓      DEL   ✓        ✓    
```

#### Addis Ai
- **Latency**: 4.1s | **Ref Words**: 17 | **Errors**: 9 (S: 9, D: 0, I: 0)
- **WER**: **52.9%** | **Word Accuracy**: **47.1%** | **CER**: 69.3%

```text
REF : እግሬ   ላይ   mild   swelling   አለ   but   mostly   long   time   ስቆም   ነው   face   እና   hand   ግን   normal   ናቸው  
HYP : እግሬ   ላይ   ማይልድ   ስዌሊንግ      አለ   በት    ሞስሊ      ሎንግ    ታይም    ስቆም   ነው   ፊስ     እና   ሃንድ    ግን   ኖርማል     ናቸው  
EVAL: ✓     ✓    SUB    SUB        ✓    SUB   SUB      SUB    SUB    ✓     ✓    SUB    ✓    SUB    ✓    SUB      ✓    
```

#### Gemini
- **Latency**: 3.76s | **Ref Words**: 17 | **Errors**: 9 (S: 9, D: 0, I: 0)
- **WER**: **52.9%** | **Word Accuracy**: **47.1%** | **CER**: 69.3%

```text
REF : እግሬ   ላይ   mild   swelling   አለ   but   mostly   long   time   ስቆም   ነው   face   እና   hand   ግን   normal   ናቸው  
HYP : እግሬ   ላይ   ማይልድ   ስዌሊንግ      አለ   በ     ሞስሊ      ሎንግ    ታይም    ስቆም   ነው   ፌስ     እና   አንድ    ግን   ኖርማል     ናቸው  
EVAL: ✓     ✓    SUB    SUB        ✓    SUB   SUB      SUB    SUB    ✓     ✓    SUB    ✓    SUB    ✓    SUB      ✓    
```

---

### Voice: `v74.wav`
> **Ground Truth Reference**:
> *Severe abdominal cramp አይደለም፤ Braxton Hicks መሰለኝ፣ ሆዴ just tight ሆኖ ይለቀኛል።*

#### Sahara
- **Latency**: 4.04s | **Ref Words**: 12 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 8.5%

```text
REF : severe   abdominal   cramp   አይደለም   braxton   hicks   መሰለኝ   ሆዴ   just   tight   ሆኖ   ይለቀኛል  
HYP : severe   abdominal   crump   አይደለም   broxton   hicks   መሰለኝ   ሆዴ   just   tie     ሆኖ   ይለቀኛል  
EVAL: ✓        ✓           SUB     ✓       SUB       ✓       ✓      ✓    ✓      SUB     ✓    ✓      
```

#### Addis Ai
- **Latency**: 3.89s | **Ref Words**: 12 | **Errors**: 7 (S: 7, D: 0, I: 0)
- **WER**: **58.3%** | **Word Accuracy**: **41.7%** | **CER**: 69.5%

```text
REF : severe   abdominal   cramp   አይደለም   braxton   hicks   መሰለኝ   ሆዴ   just   tight   ሆኖ   ይለቀኛል  
HYP : ሰቪር      አብዶሚናል      ክራምፕ    አይደለም   ብሮክስተን    ሂክስ     መሰለኝ   ሆዴ   ጀስት    ታይት     ሆኖ   ይለቀኛል  
EVAL: SUB      SUB         SUB     ✓       SUB       SUB     ✓      ✓    SUB    SUB     ✓    ✓      
```

#### Gemini
- **Latency**: 6.92s | **Ref Words**: 12 | **Errors**: 10 (S: 9, D: 1, I: 0)
- **WER**: **83.3%** | **Word Accuracy**: **16.7%** | **CER**: 78.0%

```text
REF : severe   abdominal   cramp    አይደለም   braxton   hicks    መሰለኝ   ሆዴ       just    tight   ሆኖ   ይለቀኛል  
HYP : ---      ሰቭዩር        አብዶሚናል   ክራምፕ    አይደለህም    ብሮክስትን   ሂክስ    መሰራሊንግ   ሁዴጅስቲ   ታይት     ሆኖ   ይለቀኛል  
EVAL: DEL      SUB         SUB      SUB     SUB       SUB      SUB    SUB      SUB     SUB     ✓    ✓      
```

---

### Voice: `v75.wav`
> **Ground Truth Reference**:
> *ትንሽ lower back pain ይሰማኛል because of the weight, but alarming የሆነ sign የለም።*

#### Sahara
- **Latency**: 3.74s | **Ref Words**: 14 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **21.4%** | **Word Accuracy**: **78.6%** | **CER**: 15.0%

```text
REF : ትንሽ   lower   back   pain   ይሰማኛል   because   of   the   weight   but   alarming   የሆነ   sign   የለም  
HYP : ትንሽ   low     back   pain   ይሰማኛል   because   of   the   weight   ---   alarming   የሆነ   ሳይን    የለም  
EVAL: ✓     SUB     ✓      ✓      ✓       ✓         ✓    ✓     ✓        DEL   ✓          ✓     SUB    ✓    
```

#### Addis Ai
- **Latency**: 4.71s | **Ref Words**: 14 | **Errors**: 10 (S: 10, D: 0, I: 0)
- **WER**: **71.4%** | **Word Accuracy**: **28.6%** | **CER**: 76.7%

```text
REF : ትንሽ   lower   back   pain   ይሰማኛል   because   of    the   weight   but   alarming   የሆነ   sign   የለም  
HYP : ትንሽ   ሎወር     ባክ     ፔን     ይሰማኛል   ቢኮዝ       ኦፍ    ዘ     ዌይት      በት    አላርሚንግ     የሆነ   ሳይን    የለም  
EVAL: ✓     SUB     SUB    SUB    ✓       SUB       SUB   SUB   SUB      SUB   SUB        ✓     SUB    ✓    
```

#### Gemini
- **Latency**: 5.08s | **Ref Words**: 14 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **21.4%** | **Word Accuracy**: **78.6%** | **CER**: 13.3%

```text
REF : ትንሽ   lower   back   pain   ይሰማኛል   because   of   the   weight   but   alarming   የሆነ   sign   የለም  
HYP : ትንሽ   lower   back   pain   ይሰማኛል   because   of   the   weight   but   alarm      ሆነ    ሳይን    የለም  
EVAL: ✓     ✓       ✓      ✓      ✓       ✓         ✓    ✓     ✓        ✓     SUB        SUB   SUB    ✓    
```

---
