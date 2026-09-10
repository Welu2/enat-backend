# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v66_v70_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:50:43 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 60 | 15 | 5 | 9 | 1 | **25.0%** | **75.0%** | 14.9% | 3.39s |
| **Addis Ai** | 60 | 23 | 22 | 1 | 0 | **38.3%** | **61.7%** | 45.5% | 3.56s |
| **Gemini** | 60 | 9 | 7 | 2 | 0 | **15.0%** | **85.0%** | 9.4% | 6.29s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v66.wav`
> **Ground Truth Reference**:
> *ከጠቀስካቸው ምልክቶች አንዱም የለም፤ ትንሽ ድካምና የምግብ ፍላጎት መቀነስ ብቻ ነው ዛሬ ያለው።*

#### Sahara
- **Latency**: 3.36s | **Ref Words**: 13 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 2.1%

```text
REF : ከጠቀስካቸው   ምልክቶች   አንዱም   የለም   ትንሽ   ---   ድካምና   የምግብ   ፍላጎት   መቀነስ   ብቻ   ነው   ዛሬ   ያለው  
HYP : ከጠቀስካቸው   ምልክቶች   አንዱም   የለም   ትንሽ   ድካም   እና     የምግብ   ፍላጎት   መቀነስ   ብቻ   ነው   ዛሬ   ያለው  
EVAL: ✓         ✓       ✓      ✓     ✓     INS   SUB    ✓      ✓      ✓      ✓    ✓    ✓    ✓    
```

#### Addis Ai
- **Latency**: 3.89s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ከጠቀስካቸው   ምልክቶች   አንዱም   የለም   ትንሽ   ድካምና   የምግብ   ፍላጎት   መቀነስ   ብቻ   ነው   ዛሬ   ያለው  
HYP : ከጠቀስካቸው   ምልክቶች   አንዱም   የለም   ትንሽ   ድካምና   የምግብ   ፍላጎት   መቀነስ   ብቻ   ነው   ዛሬ   ያለው  
EVAL: ✓         ✓       ✓      ✓     ✓     ✓      ✓      ✓      ✓      ✓    ✓    ✓    ✓    
```

#### Gemini
- **Latency**: 5.02s | **Ref Words**: 13 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **7.7%** | **Word Accuracy**: **92.3%** | **CER**: 2.1%

```text
REF : ከጠቀስካቸው   ምልክቶች   አንዱም   የለም   ትንሽ   ድካምና   የምግብ   ፍላጎት   መቀነስ   ብቻ   ነው   ዛሬ   ያለው  
HYP : ከጠቀስካቸው   ምልክቶች   አንድም   የለም   ትንሽ   ድካምና   የምግብ   ፍላጎት   መቀነስ   ብቻ   ነው   ዛሬ   ያለው  
EVAL: ✓         ✓       SUB    ✓     ✓     ✓      ✓      ✓      ✓      ✓    ✓    ✓    ✓    
```

---

### Voice: `v67.wav`
> **Ground Truth Reference**:
> *አይ ምንም symptom የለኝም፤ ዛሬ completely normal ነኝ።*

#### Sahara
- **Latency**: 3.53s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አይ   ምንም   symptom   የለኝም   ዛሬ   completely   normal   ነኝ  
HYP : አይ   ምንም   symptom   የለኝም   ዛሬ   completely   normal   ነኝ  
EVAL: ✓    ✓     ✓         ✓      ✓    ✓            ✓        ✓   
```

#### Addis Ai
- **Latency**: 3.38s | **Ref Words**: 8 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **37.5%** | **Word Accuracy**: **62.5%** | **CER**: 63.9%

```text
REF : አይ   ምንም   symptom   የለኝም   ዛሬ   completely   normal   ነኝ  
HYP : አይ   ምንም   ሲምፕተም     የለኝም   ዛሬ   ኮምፕሊትሊ       ኖርማል     ነኝ  
EVAL: ✓    ✓     SUB       ✓      ✓    SUB          SUB      ✓   
```

#### Gemini
- **Latency**: 9.73s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አይ   ምንም   symptom   የለኝም   ዛሬ   completely   normal   ነኝ  
HYP : አይ   ምንም   symptom   የለኝም   ዛሬ   completely   normal   ነኝ  
EVAL: ✓    ✓     ✓         ✓      ✓    ✓            ✓        ✓   
```

---

### Voice: `v68.wav`
> **Ground Truth Reference**:
> *ኧረ none of them! ራስ ምታትም bleeding ምናምን የሚባል ነገር የለም፣ I feel totally fine.*

#### Sahara
- **Latency**: 3.22s | **Ref Words**: 15 | **Errors**: 7 (S: 2, D: 5, I: 0)
- **WER**: **46.7%** | **Word Accuracy**: **53.3%** | **CER**: 28.6%

```text
REF : ኧረ    none   of    them   ራስ    ምታትም   bleeding   ምናምን   የሚባል   ነገር   የለም   i    feel   totally   fine  
HYP : ---   ---    ---   ---    ---   እረትም   bleeding   ምናምን   የሚባል   ነገር   የለም   i    feel   totaly    fine  
EVAL: DEL   DEL    DEL   DEL    DEL   SUB    ✓          ✓      ✓      ✓     ✓     ✓    ✓      SUB       ✓     
```

#### Addis Ai
- **Latency**: 3.48s | **Ref Words**: 15 | **Errors**: 10 (S: 9, D: 1, I: 0)
- **WER**: **66.7%** | **Word Accuracy**: **33.3%** | **CER**: 64.3%

```text
REF : ኧረ    none   of    them   ራስ   ምታትም   bleeding   ምናምን   የሚባል   ነገር   የለም   i     feel   totally   fine  
HYP : ---   አረ     ነኖህ   ዘም     ራስ   መታትም   ብሊዲንግ      ምናምን   የሚባል   ነገር   የለም   አይ    ፊል     ቶታሊ       ፋይን   
EVAL: DEL   SUB    SUB   SUB    ✓    SUB    SUB        ✓      ✓      ✓     ✓     SUB   SUB    SUB       SUB   
```

#### Gemini
- **Latency**: 5.94s | **Ref Words**: 15 | **Errors**: 3 (S: 1, D: 2, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 17.9%

```text
REF : ኧረ   none   of    them     ራስ   ምታትም   bleeding   ምናምን   የሚባል   ነገር   የለም   i    feel   totally   fine  
HYP : ኧረ   ---    ---   መደንዘዝም   ራስ   ምታትም   bleeding   ምናምን   የሚባል   ነገር   የለም   i    feel   totally   fine  
EVAL: ✓    DEL    DEL   SUB      ✓    ✓      ✓          ✓      ✓      ✓     ✓     ✓    ✓      ✓         ✓     
```

---

### Voice: `v69.wav`
> **Ground Truth Reference**:
> *No, no, no , no. የጠቀስካቸው severe complications ምንም አይታዩብኝም፤ ሰላም ነኝ።*

#### Sahara
- **Latency**: 3.42s | **Ref Words**: 11 | **Errors**: 4 (S: 1, D: 3, I: 0)
- **WER**: **36.4%** | **Word Accuracy**: **63.6%** | **CER**: 28.6%

```text
REF : no    no    no   no   የጠቀስካቸው   severe   complications   ምንም   አይታዩብኝም   ሰላም   ነኝ  
HYP : ---   ---   no   no   ---       severe   complications   ምንም   አይታይም     ሰላም   ነኝ  
EVAL: DEL   DEL   ✓    ✓    DEL       ✓        ✓               ✓     SUB       ✓     ✓   
```

#### Addis Ai
- **Latency**: 3.89s | **Ref Words**: 11 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **54.5%** | **Word Accuracy**: **45.5%** | **CER**: 55.1%

```text
REF : no    no    no    no    የጠቀስካቸው   severe   complications   ምንም   አይታዩብኝም   ሰላም   ነኝ  
HYP : ኖ     ኖ     ኖ     ኖ     የጠቀስካቸው   ሰቪር      ኮምፕሊኬሽንስ        ምንም   አይታዩብኝም   ሰላም   ነኝ  
EVAL: SUB   SUB   SUB   SUB   ✓         SUB      SUB             ✓     ✓         ✓     ✓   
```

#### Gemini
- **Latency**: 4.92s | **Ref Words**: 11 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **45.5%** | **Word Accuracy**: **54.5%** | **CER**: 22.4%

```text
REF : no    no    no    no    የጠቀስካቸው   severe   complications   ምንም   አይታዩብኝም   ሰላም   ነኝ  
HYP : ኖ     ኖ     ኖ     ኖ     የተጠቀሳቸው   severe   complications   ምንም   አይታዩብኝም   ሰላም   ነኝ  
EVAL: SUB   SUB   SUB   SUB   SUB       ✓        ✓               ✓     ✓         ✓     ✓   
```

---

### Voice: `v70.wav`
> **Ground Truth Reference**:
> *ምንም የተለየ ነገር የለም፣ everything is okay. ትንሽ tired መሆን ብቻ ነው ያለው።*

#### Sahara
- **Latency**: 3.44s | **Ref Words**: 13 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 8.5%

```text
REF : ምንም   የተለየ   ነገር   የለም   everything   is    okay   ትንሽ   tired   መሆን   ብቻ   ነው   ያለው  
HYP : ምንም   የተለየ   ነገር   የለም   everything   ---   ok     ትንሽ   tired   መሆን   ብቻ   ነው   ያለው  
EVAL: ✓     ✓      ✓     ✓     ✓            DEL   SUB    ✓     ✓       ✓     ✓    ✓    ✓    
```

#### Addis Ai
- **Latency**: 3.18s | **Ref Words**: 13 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 44.7%

```text
REF : ምንም   የተለየ   ነገር   የለም   everything   is    okay   ትንሽ   tired   መሆን   ብቻ   ነው   ያለው  
HYP : ምንም   የተለየ   ነገር   የለም   ኤቭሪቲንግ       ኢዝ    ኦኬ     ትንሽ   ታየርድ    መሆን   ብቻ   ነው   ያለው  
EVAL: ✓     ✓      ✓     ✓     SUB          SUB   SUB    ✓     SUB     ✓     ✓    ✓    ✓    
```

#### Gemini
- **Latency**: 5.84s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ምንም   የተለየ   ነገር   የለም   everything   is   okay   ትንሽ   tired   መሆን   ብቻ   ነው   ያለው  
HYP : ምንም   የተለየ   ነገር   የለም   everything   is   okay   ትንሽ   tired   መሆን   ብቻ   ነው   ያለው  
EVAL: ✓     ✓      ✓     ✓     ✓            ✓    ✓      ✓     ✓       ✓     ✓    ✓    ✓    
```

---
