# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v1_v5_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:47:06 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 37 | 4 | 4 | 0 | 0 | **10.8%** | **89.2%** | 4.5% | 7.73s |
| **Addis Ai** | 37 | 2 | 2 | 0 | 0 | **5.4%** | **94.6%** | 3.0% | 5.22s |
| **Gemini** | 37 | 5 | 4 | 0 | 1 | **13.5%** | **86.5%** | 6.1% | 10.02s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v1.wav`
> **Ground Truth Reference**:
> *አይ ምንም አልተሰማኝም፣ ዛሬ በጣም ደህና ነኝ አመሰግናለሁ።*

#### Sahara
- **Latency**: 19.2s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አይ   ምንም   አልተሰማኝም   ዛሬ   በጣም   ደህና   ነኝ   አመሰግናለሁ  
HYP : አይ   ምንም   አልተሰማኝም   ዛሬ   በጣም   ደህና   ነኝ   አመሰግናለሁ  
EVAL: ✓    ✓     ✓         ✓    ✓     ✓     ✓    ✓        
```

#### Addis Ai
- **Latency**: 8.17s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አይ   ምንም   አልተሰማኝም   ዛሬ   በጣም   ደህና   ነኝ   አመሰግናለሁ  
HYP : አይ   ምንም   አልተሰማኝም   ዛሬ   በጣም   ደህና   ነኝ   አመሰግናለሁ  
EVAL: ✓    ✓     ✓         ✓    ✓     ✓     ✓    ✓        
```

#### Gemini
- **Latency**: 11.88s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አይ   ምንም   አልተሰማኝም   ዛሬ   በጣም   ደህና   ነኝ   አመሰግናለሁ  
HYP : አይ   ምንም   አልተሰማኝም   ዛሬ   በጣም   ደህና   ነኝ   አመሰግናለሁ  
EVAL: ✓    ✓     ✓         ✓    ✓     ✓     ✓    ✓        
```

---

### Voice: `v2.wav`
> **Ground Truth Reference**:
> *ኧረ ምንም የለም። ራስ ምታትም ሆነ የሆድ ቁርጠት አልተሰማኝም፣ ሰላም ነኝ።*

#### Sahara
- **Latency**: 6.13s | **Ref Words**: 11 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 8.6%

```text
REF : ኧረ    ምንም   የለም   ራስ   ምታትም   ሆነ   የሆድ    ቁርጠት   አልተሰማኝም   ሰላም   ነኝ  
HYP : እረ    ምንም   የለም   ራስ   ምታትም   ሆነ   የኡርድ   ቁርጠት   አልተሰማኝም   ሰላም   ነኝ  
EVAL: SUB   ✓     ✓     ✓    ✓      ✓    SUB    ✓      ✓         ✓     ✓   
```

#### Addis Ai
- **Latency**: 5.94s | **Ref Words**: 11 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 11.4%

```text
REF : ኧረ   ምንም   የለም   ራስ   ምታትም   ሆነ   የሆድ    ቁርጠት   አልተሰማኝም   ሰላም   ነኝ  
HYP : ኧረ   ምንም   የለም   ራስ   ምታትም   ሆነ   የውድቅ   ውርቀት   አልተሰማኝም   ሰላም   ነኝ  
EVAL: ✓    ✓     ✓     ✓    ✓      ✓    SUB    SUB    ✓         ✓     ✓   
```

#### Gemini
- **Latency**: 11.08s | **Ref Words**: 11 | **Errors**: 3 (S: 2, D: 0, I: 1)
- **WER**: **27.3%** | **Word Accuracy**: **72.7%** | **CER**: 17.1%

```text
REF : ኧረ    ምንም   የለም   ራስ   ምታትም   ሆነ   ---   የሆድ   ቁርጠት   አልተሰማኝም   ሰላም   ነኝ  
HYP : እረ    ምንም   የለም   ራስ   ምታትም   ሆነ   የወር   አበባ   ቁርጠት   አልተሰማኝም   ሰላም   ነኝ  
EVAL: SUB   ✓     ✓     ✓    ✓      ✓    INS   SUB   ✓      ✓         ✓     ✓   
```

---

### Voice: `v3.wav`
> **Ground Truth Reference**:
> *አልተሰማኝም፤ እንደውም ዛሬ ቀለል ብሎኛል።*

#### Sahara
- **Latency**: 4.85s | **Ref Words**: 5 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 4.8%

```text
REF : አልተሰማኝም   እንደውም   ዛሬ   ቀለል   ብሎኛል  
HYP : አልተሰማኝም   እንደውም   ዛሬ   ቀላል   ብሎኛል  
EVAL: ✓         ✓       ✓    SUB   ✓     
```

#### Addis Ai
- **Latency**: 3.71s | **Ref Words**: 5 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አልተሰማኝም   እንደውም   ዛሬ   ቀለል   ብሎኛል  
HYP : አልተሰማኝም   እንደውም   ዛሬ   ቀለል   ብሎኛል  
EVAL: ✓         ✓       ✓    ✓     ✓     
```

#### Gemini
- **Latency**: 9.83s | **Ref Words**: 5 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 4.8%

```text
REF : አልተሰማኝም   እንደውም   ዛሬ   ቀለል   ብሎኛል  
HYP : አልሰማኝም    እንደውም   ዛሬ   ቀለል   ብሎኛል  
EVAL: SUB       ✓       ✓    ✓     ✓     
```

---

### Voice: `v4.wav`
> **Ground Truth Reference**:
> *ምንም የተለየ ነገር የለም፣ ሁሉም ነገር ደህና ነው።*

#### Sahara
- **Latency**: 4.38s | **Ref Words**: 8 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 8.3%

```text
REF : ምንም   የተለየ   ነገር   የለም   ሁሉም   ነገር   ደህና   ነው  
HYP : ምንም   የተለየ   ነገር   የለም   ሁሉም   ነገር   ደናው   ነው  
EVAL: ✓     ✓      ✓     ✓     ✓     ✓     SUB   ✓   
```

#### Addis Ai
- **Latency**: 4.4s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ምንም   የተለየ   ነገር   የለም   ሁሉም   ነገር   ደህና   ነው  
HYP : ምንም   የተለየ   ነገር   የለም   ሁሉም   ነገር   ደህና   ነው  
EVAL: ✓     ✓      ✓     ✓     ✓     ✓     ✓     ✓   
```

#### Gemini
- **Latency**: 8.91s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ምንም   የተለየ   ነገር   የለም   ሁሉም   ነገር   ደህና   ነው  
HYP : ምንም   የተለየ   ነገር   የለም   ሁሉም   ነገር   ደህና   ነው  
EVAL: ✓     ✓      ✓     ✓     ✓     ✓     ✓     ✓   
```

---

### Voice: `v5.wav`
> **Ground Truth Reference**:
> *አይ የጠቀስካቸው ነገሮች ምንም አልታዩብኝም።*

#### Sahara
- **Latency**: 4.08s | **Ref Words**: 5 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አይ   የጠቀስካቸው   ነገሮች   ምንም   አልታዩብኝም  
HYP : አይ   የጠቀስካቸው   ነገሮች   ምንም   አልታዩብኝም  
EVAL: ✓    ✓         ✓      ✓     ✓        
```

#### Addis Ai
- **Latency**: 3.89s | **Ref Words**: 5 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አይ   የጠቀስካቸው   ነገሮች   ምንም   አልታዩብኝም  
HYP : አይ   የጠቀስካቸው   ነገሮች   ምንም   አልታዩብኝም  
EVAL: ✓    ✓         ✓      ✓     ✓        
```

#### Gemini
- **Latency**: 8.42s | **Ref Words**: 5 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 4.3%

```text
REF : አይ   የጠቀስካቸው   ነገሮች   ምንም   አልታዩብኝም  
HYP : አይ   የጠቀسካቸው   ነገሮች   ምንም   አልታዩብኝም  
EVAL: ✓    SUB       ✓      ✓     ✓        
```

---
