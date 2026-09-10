# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v31_v35_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:49:23 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 60 | 12 | 10 | 2 | 0 | **20.0%** | **80.0%** | 10.1% | 2.73s |
| **Addis Ai** | 60 | 9 | 8 | 1 | 0 | **15.0%** | **85.0%** | 4.0% | 3.46s |
| **Gemini** | 60 | 10 | 8 | 1 | 1 | **16.7%** | **83.3%** | 4.5% | 8.52s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v31.wav`
> **Ground Truth Reference**:
> *ጽኑ ህመም አይደለም፤ ህፃኑ ወደ ታች ሲገፋ የሚሰማኝ መደበኛ ግፊት ብቻ ነው ያለው።*

#### Sahara
- **Latency**: 2.72s | **Ref Words**: 13 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ጽኑ   ህመም   አይደለም   ህፃኑ   ወደ   ታች   ሲገፋ   የሚሰማኝ   መደበኛ   ግፊት   ብቻ   ነው   ያለው  
HYP : ጽኑ   ህመም   አይደለም   ህፃኑ   ወደ   ታች   ሲገፋ   የሚሰማኝ   መደበኛ   ግፊት   ብቻ   ነው   ያለው  
EVAL: ✓    ✓     ✓       ✓     ✓    ✓    ✓     ✓       ✓      ✓     ✓    ✓    ✓    
```

#### Addis Ai
- **Latency**: 3.59s | **Ref Words**: 13 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **23.1%** | **Word Accuracy**: **76.9%** | **CER**: 2.6%

```text
REF : ጽኑ   ህመም   አይደለም   ህፃኑ   ወደ    ታች     ሲገፋ   የሚሰማኝ   መደበኛ   ግፊት   ብቻ   ነው   ያለው  
HYP : ጽኑ   ህመም   አይደለም   ---   ህጻኑ   ወደታች   ሲገፋ   የሚሰማኝ   መደበኛ   ግፊት   ብቻ   ነው   ያለው  
EVAL: ✓    ✓     ✓       DEL   SUB   SUB    ✓     ✓       ✓      ✓     ✓    ✓    ✓    
```

#### Gemini
- **Latency**: 8.36s | **Ref Words**: 13 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 0.0%

```text
REF : ጽኑ   ህመም   አይደለም   ህፃኑ   ወደ    ታች     ሲገፋ   የሚሰማኝ   መደበኛ   ግፊት   ብቻ   ነው   ያለው  
HYP : ጽኑ   ህመም   አይደለም   ህፃኑ   ---   ወደታች   ሲገፋ   የሚሰማኝ   መደበኛ   ግፊት   ብቻ   ነው   ያለው  
EVAL: ✓    ✓     ✓       ✓     DEL   SUB    ✓     ✓       ✓      ✓     ✓    ✓    ✓    
```

---

### Voice: `v32.wav`
> **Ground Truth Reference**:
> *ጠዋት ስነሳ ትንሽ አቅለሽልሾኝ ነበር አሁን ግን በልቼ ተሽሎኛል፤ ማስመለስ የለም።*

#### Sahara
- **Latency**: 2.82s | **Ref Words**: 11 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **36.4%** | **Word Accuracy**: **63.6%** | **CER**: 25.0%

```text
REF : ጠዋት   ስነሳ   ትንሽ    አቅለሽልሾኝ   ነበር   አሁን   ግን   በልቼ   ተሽሎኛል   ማስመለስ    የለም  
HYP : ጠዋት   ---   ስንነሳ   ትንሿይ      ነበር   አሁን   ግን   በልቼ   ተሽሎኛል   ማስመለስም   የለም  
EVAL: ✓     DEL   SUB    SUB       ✓     ✓     ✓    ✓     ✓       SUB      ✓    
```

#### Addis Ai
- **Latency**: 3.27s | **Ref Words**: 11 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 5.0%

```text
REF : ጠዋት   ስነሳ   ትንሽ   አቅለሽልሾኝ   ነበር   አሁን   ግን   በልቼ   ተሽሎኛል   ማስመለስ    የለም  
HYP : ጠዋት   ስነሳ   ትንሽ   አቅለሽሾኝ    ነበር   አሁን   ግን   በልቼ   ተሽሎኛል   ማስመለስም   የለም  
EVAL: ✓     ✓     ✓     SUB       ✓     ✓     ✓    ✓     ✓       SUB      ✓    
```

#### Gemini
- **Latency**: 8.9s | **Ref Words**: 11 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 5.0%

```text
REF : ጠዋት   ስነሳ   ትንሽ   አቅለሽልሾኝ   ነበር   አሁን   ግን   በልቼ   ተሽሎኛል   ማስመለስ    የለም  
HYP : ጠዋት   ስነሳ   ትንሽ   አቅለሽልሸኝ   ነበር   አሁን   ግን   በልቼ   ተሽሎኛል   ማስመለስም   የለም  
EVAL: ✓     ✓     ✓     SUB       ✓     ✓     ✓    ✓     ✓       SUB      ✓    
```

---

### Voice: `v33.wav`
> **Ground Truth Reference**:
> *እግሬ ትንሽ አብጧል፤ ግን ቀኑን ሙሉ ቆሜ ስለዋልኩ መሰለኝ፣ እጄና ፊቴ ግን ደህና ነው።*

#### Sahara
- **Latency**: 2.46s | **Ref Words**: 14 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **21.4%** | **Word Accuracy**: **78.6%** | **CER**: 12.5%

```text
REF : እግሬ   ትንሽ   አብጧል   ግን   ቀኑን   ሙሉ   ቆሜ   ስለዋልኩ   መሰለኝ   እጄና   ፊቴ    ግን   ደህና   ነው  
HYP : እግሬ   ትንሽ   አብጧል   ግን   ቀኑን   ሙሉ   ቆሜ   ስለኩ     መሰለኝ   ---   እጄ    ግን   ደህና   ነው  
EVAL: ✓     ✓     ✓      ✓    ✓     ✓    ✓    SUB     ✓      DEL   SUB   ✓    ✓     ✓   
```

#### Addis Ai
- **Latency**: 2.92s | **Ref Words**: 14 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : እግሬ   ትንሽ   አብጧል   ግን   ቀኑን   ሙሉ   ቆሜ   ስለዋልኩ   መሰለኝ   እጄና   ፊቴ   ግን   ደህና   ነው  
HYP : እግሬ   ትንሽ   አብጧል   ግን   ቀኑን   ሙሉ   ቆሜ   ስለዋልኩ   መሰለኝ   እጄና   ፊቴ   ግን   ደህና   ነው  
EVAL: ✓     ✓     ✓      ✓    ✓     ✓    ✓    ✓       ✓      ✓     ✓    ✓    ✓     ✓   
```

#### Gemini
- **Latency**: 8.75s | **Ref Words**: 14 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **7.1%** | **Word Accuracy**: **92.9%** | **CER**: 2.5%

```text
REF : እግሬ   ትንሽ   አብጧል   ግን   ቀኑን   ሙሉ   ቆሜ   ስለዋልኩ   መሰለኝ   እጄና   ፊቴ   ግን   ደህና   ነው  
HYP : እግሬ   ትንሽ   አብጧል   ግን   ቀኑን   ሙሉ   ቆሜ   ስላዋልኩ   መሰለኝ   እጄና   ፊቴ   ግን   ደህና   ነው  
EVAL: ✓     ✓     ✓      ✓    ✓     ✓    ✓    SUB     ✓      ✓     ✓    ✓    ✓     ✓   
```

---

### Voice: `v34.wav`
> **Ground Truth Reference**:
> *ጀርባዬን አልፎ አልፎ ያመኛል ግን የጽኑ ህመም ደረጃ አይደለም።*

#### Sahara
- **Latency**: 2.54s | **Ref Words**: 9 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 3.2%

```text
REF : ጀርባዬን   አልፎ   አልፎ   ያመኛል   ግን   የጽኑ   ህመም   ደረጃ   አይደለም  
HYP : ጀርባዬን   አልፎ   አልፎ   ይመኛል   ግን   የጽኑ   ህመም   ደረጃ   አይደለም  
EVAL: ✓       ✓     ✓     SUB    ✓    ✓     ✓     ✓     ✓      
```

#### Addis Ai
- **Latency**: 4.17s | **Ref Words**: 9 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 12.9%

```text
REF : ጀርባዬን   አልፎ   አልፎ    ያመኛል   ግን   የጽኑ   ህመም   ደረጃ    አይደለም  
HYP : ጀርባዬን   አልፎ   አልፈህ   ይመኛል   ግን   የጽኑ   ህመም   ደረጃው   አይደለም  
EVAL: ✓       ✓     SUB    SUB    ✓    ✓     ✓     SUB    ✓      
```

#### Gemini
- **Latency**: 7.38s | **Ref Words**: 9 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 16.1%

```text
REF : ጀርባዬን   አልፎ   አልፎ    ያመኛል   ግን   የጽኑ   ህመም   ደረጃ   አይደለም  
HYP : ጆሮዬን    አልፎ   አልፎም   ነኛል    ግን   የጽኑ   ህመም   ደረጃ   አይደለም  
EVAL: SUB     ✓     SUB    SUB    ✓    ✓     ✓     ✓     ✓      
```

---

### Voice: `v35.wav`
> **Ground Truth Reference**:
> *ከትላንት ማታ ጀምሮ የልጁ ምት በጣም ቀንሷል፤ ዛሬ ደግሞ አንዴም አልተንቀሳቀሰም፣ በጣም ጨንቆኛል።*

#### Sahara
- **Latency**: 3.09s | **Ref Words**: 13 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 8.3%

```text
REF : ከትላንት   ማታ   ጀምሮ   የልጁ   ምት    በጣም   ቀንሷል   ዛሬ   ደግሞ   አንዴም   አልተንቀሳቀሰም   በጣም   ጨንቆኛል  
HYP : ከትናንት   ማታ   ጀምሮ   የልጁ   ምርት   በጣም   ቀንሷል   ዛሬ   ደግሞ   አንድም   አልተንቀሳቀስም   በጣም   ጨንቆኛል  
EVAL: SUB     ✓    ✓     ✓     SUB   ✓     ✓      ✓    ✓     SUB    SUB         ✓     ✓      
```

#### Addis Ai
- **Latency**: 3.33s | **Ref Words**: 13 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **7.7%** | **Word Accuracy**: **92.3%** | **CER**: 2.1%

```text
REF : ከትላንት   ማታ   ጀምሮ   የልጁ   ምት   በጣም   ቀንሷል   ዛሬ   ደግሞ   አንዴም   አልተንቀሳቀሰም   በጣም   ጨንቆኛል  
HYP : ከትናንት   ማታ   ጀምሮ   የልጁ   ምት   በጣም   ቀንሷል   ዛሬ   ደግሞ   አንዴም   አልተንቀሳቀሰም   በጣም   ጨንቆኛል  
EVAL: SUB     ✓    ✓     ✓     ✓    ✓     ✓      ✓    ✓     ✓      ✓           ✓     ✓      
```

#### Gemini
- **Latency**: 9.21s | **Ref Words**: 13 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 2.1%

```text
REF : ---   ከትላንት   ማታ   ጀምሮ   የልጁ   ምት   በጣም   ቀንሷል   ዛሬ   ደግሞ   አንዴም   አልተንቀሳቀሰም   በጣም   ጨንቆኛል  
HYP : ከ     ትናንት    ማታ   ጀምሮ   የልጁ   ምት   በጣም   ቀንሷል   ዛሬ   ደግሞ   አንዴም   አልተንቀሳቀሰም   በጣም   ጨንቆኛል  
EVAL: INS   SUB     ✓    ✓     ✓     ✓    ✓     ✓      ✓    ✓     ✓      ✓           ✓     ✓      
```

---
