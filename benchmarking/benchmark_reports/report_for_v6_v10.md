# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v6_v10_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:48:21 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 53 | 13 | 10 | 2 | 1 | **24.5%** | **75.5%** | 15.4% | 3.42s |
| **Addis Ai** | 53 | 11 | 10 | 0 | 1 | **20.8%** | **79.2%** | 8.0% | 3.55s |
| **Gemini** | 53 | 10 | 10 | 0 | 0 | **18.9%** | **81.1%** | 10.9% | 8.76s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v6.wav`
> **Ground Truth Reference**:
> *ጽኑ ህመም አይደለም ግን ትንሽ ወገቤን ሸክም ስለበዛበት ይቆረጥመኛል፣ ሌላው ደህና ነው።*

#### Sahara
- **Latency**: 4.86s | **Ref Words**: 12 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 7.0%

```text
REF : ጽኑ   ህመም   አይደለም   ግን   ትንሽ   ወገቤን   ሸክም   ስለበዛበት   ይቆረጥመኛል   ሌላው   ደህና   ነው  
HYP : ጽኑ   ህመም   አይደለም   ግን   ትንሾ   ገቢን    ሸክም   ስለበዛበት   ይቆረጥመኛል   ሌላው   ደህና   ነው  
EVAL: ✓    ✓     ✓       ✓    SUB   SUB    ✓     ✓        ✓         ✓     ✓     ✓   
```

#### Addis Ai
- **Latency**: 3.68s | **Ref Words**: 12 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 7.0%

```text
REF : ጽኑ   ህመም   አይደለም   ግን   ትንሽ   ወገቤን   ሸክም   ስለበዛበት   ይቆረጥመኛል   ሌላው   ደህና   ነው  
HYP : ጽኑ   ህመም   አይደለም   ግን   ትንሹ   ገቢን    ሸክም   ስለበዛበት   ይቆረጥመኛል   ሌላው   ደህና   ነው  
EVAL: ✓    ✓     ✓       ✓    SUB   SUB    ✓     ✓        ✓         ✓     ✓     ✓   
```

#### Gemini
- **Latency**: 8.39s | **Ref Words**: 12 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **8.3%** | **Word Accuracy**: **91.7%** | **CER**: 4.7%

```text
REF : ጽኑ   ህመም   አይደለም   ግን   ትንሽ   ወገቤን    ሸክም   ስለበዛበት   ይቆረጥመኛል   ሌላው   ደህና   ነው  
HYP : ጽኑ   ህመም   አይደለም   ግን   ትንሽ   ወገبیን   ሸክም   ስለበዛበት   ይቆረጥመኛል   ሌላው   ደህና   ነው  
EVAL: ✓    ✓     ✓       ✓    ✓     SUB     ✓     ✓        ✓         ✓     ✓     ✓   
```

---

### Voice: `v7.wav`
> **Ground Truth Reference**:
> *እንትን… ጠዋት ላይ ትንሽ ማቅለሽለሽ ነበረኝ ግን ራሴን አላመመኝም፣ ደምም አልፈሰሰኝም።*

#### Sahara
- **Latency**: 2.94s | **Ref Words**: 11 | **Errors**: 4 (S: 2, D: 1, I: 1)
- **WER**: **36.4%** | **Word Accuracy**: **63.6%** | **CER**: 20.4%

```text
REF : እንትን…   ጠዋት   ላይ   ትንሽ   ---    ማቅለሽለሽ   ነበረኝ   ግን   ራሴን   አላመመኝም   ደምም   አልፈሰሰኝም  
HYP : ---     ጠዋት   ላይ   ትንሽ   ማቅለስ   ልጅ       ነበረኝ   ግን   ራሴን   አላመመኝም   ደምም   አልፈሰኝም   
EVAL: DEL     ✓     ✓    ✓     INS    SUB      ✓      ✓    ✓     ✓        ✓     SUB      
```

#### Addis Ai
- **Latency**: 3.43s | **Ref Words**: 11 | **Errors**: 4 (S: 3, D: 0, I: 1)
- **WER**: **36.4%** | **Word Accuracy**: **63.6%** | **CER**: 9.1%

```text
REF : እንትን…   ጠዋት   ላይ   ትንሽ   ---    ማቅለሽለሽ   ነበረኝ   ግን   ራሴን   አላመመኝም   ደምም   አልፈሰሰኝም  
HYP : እንትን    ጠዋት   ላይ   ትንሽ   ማቅለስ   ስለሽ      ነበረኝ   ግን   ራሴን   አላምመኝም   ደምም   አልፈሰሰኝም  
EVAL: SUB     ✓     ✓    ✓     INS    SUB      ✓      ✓    ✓     SUB      ✓     ✓        
```

#### Gemini
- **Latency**: 8.27s | **Ref Words**: 11 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 2.3%

```text
REF : እንትን…   ጠዋት   ላይ   ትንሽ   ማቅለሽለሽ   ነበረኝ   ግን   ራሴን   አላመመኝም   ደምም   አልፈሰሰኝም  
HYP : እንትን    ጠዋት   ላይ   ትንሽ   ማቅለሽለሽ   ነበረኝ   ግን   ራሴን   አላመመኝም   ደምም   አልፈሰሰኝም  
EVAL: SUB     ✓     ✓    ✓     ✓        ✓      ✓    ✓     ✓        ✓     ✓        
```

---

### Voice: `v8.wav`
> **Ground Truth Reference**:
> *ሆዴ ትንሽ ይከብደኛል እንጂ ከፍተኛ ህመም ወይም ፈሳሽ መፍሰስ የለም።*

#### Sahara
- **Latency**: 3.02s | **Ref Words**: 10 | **Errors**: 1 (S: 0, D: 1, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 8.8%

```text
REF : ሆዴ   ትንሽ   ይከብደኛል   እንጂ   ከፍተኛ   ህመም   ወይም   ፈሳሽ   መፍሰስ   የለም  
HYP : ሆዴ   ትንሽ   ይከብደኛል   እንጂ   ከፍተኛ   ህመም   ወይም   ፈሳሽ   መፍሰስ   ---  
EVAL: ✓    ✓     ✓        ✓     ✓      ✓     ✓     ✓     ✓      DEL  
```

#### Addis Ai
- **Latency**: 3.36s | **Ref Words**: 10 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ሆዴ   ትንሽ   ይከብደኛል   እንጂ   ከፍተኛ   ህመም   ወይም   ፈሳሽ   መፍሰስ   የለም  
HYP : ሆዴ   ትንሽ   ይከብደኛል   እንጂ   ከፍተኛ   ህመም   ወይም   ፈሳሽ   መፍሰስ   የለም  
EVAL: ✓    ✓     ✓        ✓     ✓      ✓     ✓     ✓     ✓      ✓    
```

#### Gemini
- **Latency**: 8.69s | **Ref Words**: 10 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 5.9%

```text
REF : ሆዴ    ትንሽ   ይከብደኛል   እንጂ   ከፍተኛ   ህመም   ወይም   ፈሳሽ   መፍሰስ   የለም  
HYP : ሆድህ   ትንሽ   ይከብደኛል   እንጂ   ከፍተኛ   ህመም   ወይም   ፈሳሽ   መፍሰስ   የለም  
EVAL: SUB   ✓     ✓        ✓     ✓      ✓     ✓     ✓     ✓      ✓    
```

---

### Voice: `v9.wav`
> **Ground Truth Reference**:
> *ድካም ድካም ይለኛል እንጂ ዓይኔም አይዥጎረጎረኝም ራሴም አይዞረኝም።*

#### Sahara
- **Latency**: 2.87s | **Ref Words**: 8 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **37.5%** | **Word Accuracy**: **62.5%** | **CER**: 11.4%

```text
REF : ድካም   ድካም   ይለኛል   እንጂ   ዓይኔም   አይዥጎረጎረኝም   ራሴም   አይዞረኝም  
HYP : ድካም   ድካም   ይለኛል   እንጂ   አይኔም   አይጎረጉረኝም    ራሴም   አያዞረኝም  
EVAL: ✓     ✓     ✓      ✓     SUB    SUB         ✓     SUB     
```

#### Addis Ai
- **Latency**: 3.38s | **Ref Words**: 8 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **37.5%** | **Word Accuracy**: **62.5%** | **CER**: 14.3%

```text
REF : ድካም   ድካም   ይለኛል   እንጂ   ዓይኔም   አይዥጎረጎረኝም   ራሴም   አይዞረኝም  
HYP : ድካም   ድካም   ይለኛል   እንጂ   አይኔም   አያሽጎረጉረኝም   ራሴም   አያዞረኝም  
EVAL: ✓     ✓     ✓      ✓     SUB    SUB         ✓     SUB     
```

#### Gemini
- **Latency**: 9.01s | **Ref Words**: 8 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **62.5%** | **Word Accuracy**: **37.5%** | **CER**: 37.1%

```text
REF : ድካም    ድካም    ይለኛል   እንጂ   ዓይኔም   አይዥጎረጎረኝም   ራሴም   አይዞረኝም  
HYP : ደከመኝ   ደከመኝ   ይለኛል   እንጂ   አይኔም   አይርገረገረኝም   ራሴም   አያዞረኝም  
EVAL: SUB    SUB    ✓      ✓     SUB    SUB         ✓     SUB     
```

---

### Voice: `v10.wav`
> **Ground Truth Reference**:
> *አዎ፣ ከጠዋት ጀምሮ በጣም የሚከብድ ጽኑ ራስ ምታት አለብኝ፤ ፓራሲታሞል ወስጄም አልለቀቀኝም።*

#### Sahara
- **Latency**: 3.39s | **Ref Words**: 12 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 26.7%

```text
REF : አዎ   ከጠዋት   ጀምሮ   በጣም   የሚከብድ   ጽኑ   ራስ   ምታት   አለብኝ   ፓራሲታሞል        ወስጄም   አልለቀቀኝም  
HYP : አዎ   ከጠዋት   ጀምሮ   በጣም   የሚከብድ   ጽኑ   ራስ   መታት   አለብኝ   parastamulo   ስጄም    አልለቀቀኝም  
EVAL: ✓    ✓      ✓     ✓     ✓       ✓    ✓    SUB   ✓      SUB           SUB    ✓        
```

#### Addis Ai
- **Latency**: 3.89s | **Ref Words**: 12 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 8.9%

```text
REF : አዎ   ከጠዋት   ጀምሮ   በጣም   የሚከብድ   ጽኑ   ራስ   ምታት   አለብኝ   ፓራሲታሞል   ወስጄም   አልለቀቀኝም  
HYP : አዎ   ከጠዋት   ጀምሮ   በጣም   የሚከብድ   ጽኑ   ራስ   መታት   አለብኝ   ፓራስታሚሎ   ወስጄም   አልለቀቀኝም  
EVAL: ✓    ✓      ✓     ✓     ✓       ✓    ✓    SUB   ✓      SUB      ✓      ✓        
```

#### Gemini
- **Latency**: 9.42s | **Ref Words**: 12 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 8.9%

```text
REF : አዎ    ከጠዋት   ጀምሮ   በጣም   የሚከብድ   ጽኑ   ራስ   ምታት   አለብኝ   ፓራሲታሞል    ወስጄም   አልለቀቀኝም  
HYP : ኦው    ከጠዋት   ጀምሮ   በጣም   የሚከብድ   ጽኑ   ራስ   ምታት   አለብኝ   ፓራስታሞልም   ወስጄም   አልለቀቀኝም  
EVAL: SUB   ✓      ✓     ✓     ✓       ✓    ✓    ✓     ✓      SUB       ✓      ✓        
```

---
