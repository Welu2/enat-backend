# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v16_v20_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:48:54 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 56 | 15 | 12 | 3 | 0 | **26.8%** | **73.2%** | 13.9% | 2.65s |
| **Addis Ai** | 56 | 7 | 7 | 0 | 0 | **12.5%** | **87.5%** | 5.2% | 3.19s |
| **Gemini** | 56 | 10 | 10 | 0 | 0 | **17.9%** | **82.1%** | 5.7% | 8.18s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v16.wav`
> **Ground Truth Reference**:
> *ህመሙ የለም ግን የልጁ መንቀሳቀስ ከትላንት ወዲህ ሙሉ በሙሉ ቆሟል፣ ምንም አይሰማኝም።*

#### Sahara
- **Latency**: 2.62s | **Ref Words**: 12 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 9.5%

```text
REF : ህመሙ   የለም   ግን   የልጁ   መንቀሳቀስ   ከትላንት   ወዲህ   ሙሉ   በሙሉ   ቆሟል   ምንም   አይሰማኝም  
HYP : ህመሙ   የለም   ግን   የልጁ   መንቀሳቀስ   ከትናንት   ወዲህ   ሙሉ   በሙሉ   ---   ምንም   አይሰማኝም  
EVAL: ✓     ✓     ✓    ✓     ✓        SUB     ✓     ✓    ✓     DEL   ✓     ✓       
```

#### Addis Ai
- **Latency**: 3.56s | **Ref Words**: 12 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 4.8%

```text
REF : ህመሙ   የለም   ግን   የልጁ   መንቀሳቀስ   ከትላንት   ወዲህ   ሙሉ   በሙሉ   ቆሟል   ምንም   አይሰማኝም  
HYP : ህማሙ   የለም   ግን   የልጁ   መንቀሳቀስ   ከትናንት   ወዲህ   ሙሉ   በሙሉ   ቆሟል   ምንም   አይሰማኝም  
EVAL: SUB   ✓     ✓    ✓     ✓        SUB     ✓     ✓    ✓     ✓     ✓     ✓       
```

#### Gemini
- **Latency**: 8.67s | **Ref Words**: 12 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 7.1%

```text
REF : ህመሙ   የለም   ግን   የልጁ   መንቀሳቀስ   ከትላንት   ወዲህ   ሙሉ   በሙሉ   ቆሟል   ምንም   አይሰማኝም  
HYP : ህማሙ   የለም   ግን   የልጁ   መንቀሳቀስ   ከትናንት   ወዲያ   ሙሉ   በሙሉ   ቆሟል   ምንም   አይሰማኝም  
EVAL: SUB   ✓     ✓    ✓     ✓        SUB     SUB   ✓    ✓     ✓     ✓     ✓       
```

---

### Voice: `v17.wav`
> **Ground Truth Reference**:
> *ከፍተኛ ትኩሳት አለብኝ፣ ሰውነቴ በሙሉ ይንቀጠቀጣል፤ በጣም በርዶኛል።*

#### Sahara
- **Latency**: 2.7s | **Ref Words**: 8 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 11.8%

```text
REF : ከፍተኛ   ትኩሳት   አለብኝ   ሰውነቴ    በሙሉ   ይንቀጠቀጣል   በጣም   በርዶኛል  
HYP : ከፍተኛ   ትኩሳት   አለብኝ   ሰውነቴን   በሙሉ   ይንቀጠቀጣል   በጣም   በር     
EVAL: ✓      ✓      ✓      SUB     ✓     ✓         ✓     SUB    
```

#### Addis Ai
- **Latency**: 3.34s | **Ref Words**: 8 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 2.9%

```text
REF : ከፍተኛ   ትኩሳት   አለብኝ   ሰውነቴ    በሙሉ   ይንቀጠቀጣል   በጣም   በርዶኛል  
HYP : ከፍተኛ   ትኩሳት   አለብኝ   ሰውነቴን   በሙሉ   ይንቀጠቀጣል   በጣም   በርዶኛል  
EVAL: ✓      ✓      ✓      SUB     ✓     ✓         ✓     ✓      
```

#### Gemini
- **Latency**: 8.28s | **Ref Words**: 8 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 2.9%

```text
REF : ከፍተኛ   ትኩሳት   አለብኝ   ሰውነቴ    በሙሉ   ይንቀጠቀጣል   በጣም   በርዶኛል  
HYP : ከፍተኛ   ትኩሳት   አለብኝ   ሰውነቴን   በሙሉ   ይንቀጠቀጣል   በጣም   በርዶኛል  
EVAL: ✓      ✓      ✓      SUB     ✓     ✓         ✓     ✓      
```

---

### Voice: `v18.wav`
> **Ground Truth Reference**:
> *ትንፋሽ እያጠረኝ ነው፤ ጋደም ስል ደረቴን ይጫነኛል፣ መተንፈስ ከብዶኛል።*

#### Sahara
- **Latency**: 2.45s | **Ref Words**: 9 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **22.2%** | **Word Accuracy**: **77.8%** | **CER**: 8.6%

```text
REF : ትንፋሽ   እያጠረኝ   ነው   ጋደም   ስል    ደረቴን   ይጫነኛል   መተንፈስ   ከብዶኛል  
HYP : ትንፋሽ   እያጠረኝ   ነው   ጋደም   ምስል   ደረቴን   ይጫነኛል   መተንፈስ   ገብቶኛል  
EVAL: ✓      ✓       ✓    ✓     SUB   ✓      ✓       ✓       SUB    
```

#### Addis Ai
- **Latency**: 3.22s | **Ref Words**: 9 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 2.9%

```text
REF : ትንፋሽ   እያጠረኝ   ነው   ጋደም   ስል   ደረቴን   ይጫነኛል   መተንፈስ   ከብዶኛል  
HYP : ትንፋሽ   እያጠረኝ   ነው   ጋደም   ስል   ደረቴን   ይጫነኛል   መተንፈስ   ገብዶኛል  
EVAL: ✓      ✓       ✓    ✓     ✓    ✓      ✓       ✓       SUB    
```

#### Gemini
- **Latency**: 8.03s | **Ref Words**: 9 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **22.2%** | **Word Accuracy**: **77.8%** | **CER**: 5.7%

```text
REF : ትንፋሽ   እያጠረኝ   ነው   ጋደም   ስል   ደረቴን   ይጫነኛል   መተንፈስ   ከብዶኛል  
HYP : ትንፋሽ   እያጥረኝ   ነው   ጋደም   ስል   ደረቴን   ይጫነኛል   መተንፈስ   ገብዶኛል  
EVAL: ✓      SUB     ✓    ✓     ✓    ✓      ✓       ✓       SUB    
```

---

### Voice: `v19.wav`
> **Ground Truth Reference**:
> *አዎ፤ ከትላንት ጀምሮ ራሴን በጣም እያመመኝ ነው፣ ዓይኔ ሁሉ ጥቁር ጥቁር ነገር ያያል፣ ፊቴም አብጧል።*

#### Sahara
- **Latency**: 2.78s | **Ref Words**: 15 | **Errors**: 6 (S: 5, D: 1, I: 0)
- **WER**: **40.0%** | **Word Accuracy**: **60.0%** | **CER**: 25.5%

```text
REF : አዎ   ከትላንት   ጀምሮ   ራሴን   በጣም   እያመመኝ   ነው   ዓይኔ   ሁሉ   ጥቁር   ጥቁር   ነገር   ያያል   ፊቴም   አብጧል   
HYP : አዎ   ከትናንት   ጀምሮ   ራሴን   በጣም   እያመ     ነው   አይኔ   ሁሉ   ---   ጥቁር   ነገር   ያለ    ፊቴም   ማብጠዋል  
EVAL: ✓    SUB     ✓     ✓     ✓     SUB     ✓    SUB   ✓    DEL   ✓     ✓     SUB   ✓     SUB    
```

#### Addis Ai
- **Latency**: 2.99s | **Ref Words**: 15 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **13.3%** | **Word Accuracy**: **86.7%** | **CER**: 6.4%

```text
REF : አዎ   ከትላንት   ጀምሮ   ራሴን   በጣም   እያመመኝ   ነው   ዓይኔ   ሁሉ   ጥቁር   ጥቁር   ነገር   ያያል   ፊቴም   አብጧል  
HYP : አዎ   ከትላንት   ጀምሮ   ራሴን   በጣም   እያመመኝ   ነው   አይኔ   ሁሉ   ጥቁር   ጥቁር   ነገር   ያለው   ፊቴም   አብጧል  
EVAL: ✓    ✓       ✓     ✓     ✓     ✓       ✓    SUB   ✓    ✓     ✓     ✓     SUB   ✓     ✓     
```

#### Gemini
- **Latency**: 8.0s | **Ref Words**: 15 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **26.7%** | **Word Accuracy**: **73.3%** | **CER**: 10.6%

```text
REF : አዎ    ከትላንት   ጀምሮ   ራሴን   በጣም   እያመመኝ   ነው   ዓይኔ   ሁሉ   ጥቁር   ጥቁር   ነገር   ያያል   ፊቴም   አብጧል  
HYP : አው    ከትናንት   ጀምሮ   ራሴን   በጣም   እያመመኝ   ነው   አይኔ   ሁሉ   ጥቁር   ጥቁር   ነገር   ይላል   ፊቴም   አብጧል  
EVAL: SUB   SUB     ✓     ✓     ✓     ✓       ✓    SUB   ✓    ✓     ✓     ✓     SUB   ✓     ✓     
```

---

### Voice: `v20.wav`
> **Ground Truth Reference**:
> *ሆዴን በጣም እያመመኝ ነው፣ ከዛም ጋር ቀይ ደም እየፈሰሰኝ ነው። ቶሎ እርዱኝ።*

#### Sahara
- **Latency**: 2.69s | **Ref Words**: 12 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 11.1%

```text
REF : ሆዴን   በጣም   እያመመኝ   ነው      ከዛም   ጋር   ቀይ   ደም   እየፈሰሰኝ   ነው   ቶሎ   እርዱኝ  
HYP : ሆዴን   በጣም   ---     እያመነው   ከዛም   ጋር   ቀይ   ደም   እየፈሰሰኝ   ነው   ቶሎ   ኦርኝ   
EVAL: ✓     ✓     DEL     SUB     ✓     ✓    ✓    ✓    ✓        ✓    ✓    SUB   
```

#### Addis Ai
- **Latency**: 2.84s | **Ref Words**: 12 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **8.3%** | **Word Accuracy**: **91.7%** | **CER**: 8.3%

```text
REF : ሆዴን   በጣም   እያመመኝ   ነው   ከዛም   ጋር   ቀይ   ደም   እየፈሰሰኝ   ነው   ቶሎ   እርዱኝ    
HYP : ሆዴን   በጣም   እያመመኝ   ነው   ከዛም   ጋር   ቀይ   ደም   እየፈሰሰኝ   ነው   ቶሎ   እወርድሁኝ  
EVAL: ✓     ✓     ✓       ✓    ✓     ✓    ✓    ✓    ✓        ✓    ✓    SUB     
```

#### Gemini
- **Latency**: 7.92s | **Ref Words**: 12 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ሆዴን   በጣም   እያመመኝ   ነው   ከዛም   ጋር   ቀይ   ደም   እየፈሰሰኝ   ነው   ቶሎ   እርዱኝ  
HYP : ሆዴን   በጣም   እያመመኝ   ነው   ከዛም   ጋር   ቀይ   ደም   እየፈሰሰኝ   ነው   ቶሎ   እርዱኝ  
EVAL: ✓     ✓     ✓       ✓    ✓     ✓    ✓    ✓    ✓        ✓    ✓    ✓     
```

---
