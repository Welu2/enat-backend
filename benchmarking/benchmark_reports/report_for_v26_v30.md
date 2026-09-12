# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v26_v30_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:49:13 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 46 | 14 | 5 | 9 | 0 | **30.4%** | **69.6%** | 29.3% | 3.27s |
| **Addis Ai** | 46 | 3 | 2 | 1 | 0 | **6.5%** | **93.5%** | 3.4% | 3.04s |
| **Gemini** | 46 | 5 | 4 | 1 | 0 | **10.9%** | **89.1%** | 4.0% | 8.79s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v26.wav`
> **Ground Truth Reference**:
> *አይ ምንም አልተሰማኝም፣ ህፃኑም በደንብ እየተንቀሳቀሰ ነው ደህና ነኝ።*

#### Sahara
- **Latency**: 3.15s | **Ref Words**: 9 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **22.2%** | **Word Accuracy**: **77.8%** | **CER**: 8.6%

```text
REF : አይ   ምንም   አልተሰማኝም   ህፃኑም   በደንብ   እየተንቀሳቀሰ   ነው   ደህና   ነኝ  
HYP : አይ   ምንም   አልተሰማኝም   ህፃኑ    በደንብ   እየተንቀሳቀሰ   ነው   ገና    ነኝ  
EVAL: ✓    ✓     ✓         SUB    ✓      ✓          ✓    SUB   ✓   
```

#### Addis Ai
- **Latency**: 3.09s | **Ref Words**: 9 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 5.7%

```text
REF : አይ   ምንም   አልተሰማኝም   ህፃኑም   በደንብ   እየተንቀሳቀሰ   ነው   ደህና   ነኝ  
HYP : አይ   ምንም   አልተሰማኝም   ሕፃኑ    በደንብ   እየተንቀሳቀሰ   ነው   ደህና   ነኝ  
EVAL: ✓    ✓     ✓         SUB    ✓      ✓          ✓    ✓     ✓   
```

#### Gemini
- **Latency**: 9.56s | **Ref Words**: 9 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 2.9%

```text
REF : አይ   ምንም   አልተሰማኝም   ህፃኑም   በደንብ   እየተንቀሳቀሰ   ነው   ደህና   ነኝ  
HYP : አይ   ምንም   አልተሰማኝም   ህጻኑም   በደንብ   እየተንቀሳቀሰ   ነው   ደህና   ነኝ  
EVAL: ✓    ✓     ✓         SUB    ✓      ✓          ✓    ✓     ✓   
```

---

### Voice: `v27.wav`
> **Ground Truth Reference**:
> *ምንም የለም፤ ዛሬማ በጣም ተሽሎኛል፣ የቤት ስራዬንም እየሰራሁ ነው።*

#### Sahara
- **Latency**: 2.61s | **Ref Words**: 9 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 15.6%

```text
REF : ምንም   የለም   ዛሬማ   በጣም   ተሽሎኛል   የቤት   ስራዬንም   እየሰራሁ   ነው  
HYP : ምንም   የለም   ---   ዛሬሞ   ተሽሎኛል   የቤት   ስራዬንም   እየሰራው   ነው  
EVAL: ✓     ✓     DEL   SUB   ✓       ✓     ✓       SUB     ✓   
```

#### Addis Ai
- **Latency**: 2.87s | **Ref Words**: 9 | **Errors**: 1 (S: 0, D: 1, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 9.4%

```text
REF : ምንም   የለም   ዛሬማ   በጣም   ተሽሎኛል   የቤት   ስራዬንም   እየሰራሁ   ነው  
HYP : ምንም   የለም   ዛሬማ   ---   ተሽሎኛል   የቤት   ስራዬንም   እየሰራሁ   ነው  
EVAL: ✓     ✓     ✓     DEL   ✓       ✓     ✓       ✓       ✓   
```

#### Gemini
- **Latency**: 8.1s | **Ref Words**: 9 | **Errors**: 1 (S: 0, D: 1, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 9.4%

```text
REF : ምንም   የለም   ዛሬማ   በጣም   ተሽሎኛል   የቤት   ስራዬንም   እየሰራሁ   ነው  
HYP : ምንም   የለም   ዛሬማ   ---   ተሽሎኛል   የቤት   ስራዬንም   እየሰራሁ   ነው  
EVAL: ✓     ✓     ✓     DEL   ✓       ✓     ✓       ✓       ✓   
```

---

### Voice: `v28.wav`
> **Ground Truth Reference**:
> *ኧረ እነዚህ ከየጠቀስካቸው ውስጥ አንዳቸውም አልታዩብኝም፣ እግዚአብሔር ይመስገን።*

#### Sahara
- **Latency**: 2.84s | **Ref Words**: 8 | **Errors**: 8 (S: 0, D: 8, I: 0)
- **WER**: **100.0%** | **Word Accuracy**: **0.0%** | **CER**: 100.0%

```text
REF : ኧረ    እነዚህ   ከየጠቀስካቸው   ውስጥ   አንዳቸውም   አልታዩብኝም   እግዚአብሔር   ይመስገን  
HYP : ---   ---    ---        ---   ---      ---       ---       ---    
EVAL: DEL   DEL    DEL        DEL   DEL      DEL       DEL       DEL    
```

#### Addis Ai
- **Latency**: 2.81s | **Ref Words**: 8 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 2.4%

```text
REF : ኧረ   እነዚህ   ከየጠቀስካቸው   ውስጥ   አንዳቸውም   አልታዩብኝም   እግዚአብሔር   ይመስገን  
HYP : ኧረ   እነዚህ   ከጠቀስካቸው    ውስጥ   አንዳቸውም   አልታዩብኝም   እግዚአብሔር   ይመስገን  
EVAL: ✓    ✓      SUB        ✓     ✓        ✓         ✓         ✓      
```

#### Gemini
- **Latency**: 10.65s | **Ref Words**: 8 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 4.8%

```text
REF : ኧረ   እነዚህ   ከየጠቀስካቸው   ውስጥ   አንዳቸውም   አልታዩብኝም   እግዚአብሔር   ይመስገን  
HYP : ኧረ   እነዚህ   ከተጠቀስካቸው   ውስጥ   አንዳቸውም   አልታዩኝም    እግዚአብሔር   ይመስገን  
EVAL: ✓    ✓      SUB        ✓     ✓        SUB       ✓         ✓      
```

---

### Voice: `v29.wav`
> **Ground Truth Reference**:
> *እራስ ምታትም ሆነ የሆድ ህመም የለም፤ ትንሽ እንቅልፍ ማጣት ብቻ ነው የተሰማኝ።*

#### Sahara
- **Latency**: 3.73s | **Ref Words**: 12 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **8.3%** | **Word Accuracy**: **91.7%** | **CER**: 2.6%

```text
REF : እራስ   ምታትም   ሆነ   የሆድ   ህመም   የለም   ትንሽ   እንቅልፍ   ማጣት   ብቻ   ነው   የተሰማኝ  
HYP : ራስ    ምታትም   ሆነ   የሆድ   ህመም   የለም   ትንሽ   እንቅልፍ   ማጣት   ብቻ   ነው   የተሰማኝ  
EVAL: SUB   ✓      ✓    ✓     ✓     ✓     ✓     ✓       ✓     ✓    ✓    ✓      
```

#### Addis Ai
- **Latency**: 3.66s | **Ref Words**: 12 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : እራስ   ምታትም   ሆነ   የሆድ   ህመም   የለም   ትንሽ   እንቅልፍ   ማጣት   ብቻ   ነው   የተሰማኝ  
HYP : እራስ   ምታትም   ሆነ   የሆድ   ህመም   የለም   ትንሽ   እንቅልፍ   ማጣት   ብቻ   ነው   የተሰማኝ  
EVAL: ✓     ✓      ✓    ✓     ✓     ✓     ✓     ✓       ✓     ✓    ✓    ✓      
```

#### Gemini
- **Latency**: 7.17s | **Ref Words**: 12 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **8.3%** | **Word Accuracy**: **91.7%** | **CER**: 2.6%

```text
REF : እራስ   ምታትም   ሆነ   የሆድ   ህመም   የለም   ትንሽ   እንቅልፍ   ማጣት   ብቻ   ነው   የተሰማኝ  
HYP : ራስ    ምታትም   ሆነ   የሆድ   ህመም   የለም   ትንሽ   እንቅልፍ   ማጣት   ብቻ   ነው   የተሰማኝ  
EVAL: SUB   ✓      ✓    ✓     ✓     ✓     ✓     ✓       ✓     ✓    ✓    ✓      
```

---

### Voice: `v30.wav`
> **Ground Truth Reference**:
> *ሁሉም ነገር ሰላም ነው፣ ምንም የሚያስፈራ ምልክት የለም።*

#### Sahara
- **Latency**: 4.04s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ሁሉም   ነገር   ሰላም   ነው   ምንም   የሚያስፈራ   ምልክት   የለም  
HYP : ሁሉም   ነገር   ሰላም   ነው   ምንም   የሚያስፈራ   ምልክት   የለም  
EVAL: ✓     ✓     ✓     ✓    ✓     ✓        ✓      ✓    
```

#### Addis Ai
- **Latency**: 2.78s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ሁሉም   ነገር   ሰላም   ነው   ምንም   የሚያስፈራ   ምልክት   የለም  
HYP : ሁሉም   ነገር   ሰላም   ነው   ምንም   የሚያስፈራ   ምልክት   የለም  
EVAL: ✓     ✓     ✓     ✓    ✓     ✓        ✓      ✓    
```

#### Gemini
- **Latency**: 8.46s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ሁሉም   ነገር   ሰላም   ነው   ምንም   የሚያስፈራ   ምልክት   የለም  
HYP : ሁሉም   ነገር   ሰላም   ነው   ምንም   የሚያስፈራ   ምልክት   የለም  
EVAL: ✓     ✓     ✓     ✓    ✓     ✓        ✓      ✓    
```

---
