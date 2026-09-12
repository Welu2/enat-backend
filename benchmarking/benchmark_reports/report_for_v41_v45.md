# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v41_v45_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:49:43 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 57 | 7 | 6 | 0 | 1 | **12.3%** | **87.7%** | 3.5% | 3.39s |
| **Addis Ai** | 57 | 10 | 7 | 0 | 3 | **17.5%** | **82.5%** | 10.4% | 3.18s |
| **Gemini** | 57 | 6 | 4 | 1 | 1 | **10.5%** | **89.5%** | 5.0% | 8.08s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v41.wav`
> **Ground Truth Reference**:
> *ደም እየፈሰሰኝ ነው፤ ልክ እንደ የወር አበባ ቀይ ሆኖ መፍሰስ ጀምሯል።*

#### Sahara
- **Latency**: 2.74s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ደም   እየፈሰሰኝ   ነው   ልክ   እንደ   የወር   አበባ   ቀይ   ሆኖ   መፍሰስ   ጀምሯል  
HYP : ደም   እየፈሰሰኝ   ነው   ልክ   እንደ   የወር   አበባ   ቀይ   ሆኖ   መፍሰስ   ጀምሯል  
EVAL: ✓    ✓        ✓    ✓    ✓     ✓     ✓     ✓    ✓    ✓      ✓     
```

#### Addis Ai
- **Latency**: 2.81s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ደም   እየፈሰሰኝ   ነው   ልክ   እንደ   የወር   አበባ   ቀይ   ሆኖ   መፍሰስ   ጀምሯል  
HYP : ደም   እየፈሰሰኝ   ነው   ልክ   እንደ   የወር   አበባ   ቀይ   ሆኖ   መፍሰስ   ጀምሯል  
EVAL: ✓    ✓        ✓    ✓    ✓     ✓     ✓     ✓    ✓    ✓      ✓     
```

#### Gemini
- **Latency**: 8.16s | **Ref Words**: 11 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 3.0%

```text
REF : ደም   እየፈሰሰኝ   ነው   ልክ   እንደ   ---   የወር   አበባ   ቀይ   ሆኖ   መፍሰስ   ጀምሯል  
HYP : ደም   እየፈሰሰኝ   ነው   ልክ   እንደ   የ     ወራ    አበባ   ቀይ   ሆኖ   መፍሰስ   ጀምሯል  
EVAL: ✓    ✓        ✓    ✓    ✓     INS   SUB   ✓     ✓    ✓    ✓      ✓     
```

---

### Voice: `v42.wav`
> **Ground Truth Reference**:
> *አዎ፤ ራሴን በጣም አሞኛል፣ ራስ ምታት አለብኝ፣ በዛ ላይ ዓይኔ ብዥ ብሎብኛል፣ እጆቼና እግሮቼም በጣም ተወጣጥረው አብጠዋል።*

#### Sahara
- **Latency**: 5.06s | **Ref Words**: 17 | **Errors**: 4 (S: 3, D: 0, I: 1)
- **WER**: **23.5%** | **Word Accuracy**: **76.5%** | **CER**: 5.2%

```text
REF : አዎ   ራሴን   በጣም   አሞኛል   ራስ   ምታት   አለብኝ   በዛ   ላይ   ዓይኔ   ብዥ   ብሎብኛል   ---   እጆቼና   እግሮቼም   በጣም   ተወጣጥረው   አብጠዋል  
HYP : አዎ   ራሴን   በጣም   አሞኛል   ራስ   ምታት   አለብኝ   በዛ   ላይ   አይኔ   ብዥ   ብሎብኛል   እጆቼ   እና     እግሮቼም   በጣም   ተበጣጥረው   አብጠዋል  
EVAL: ✓    ✓     ✓     ✓      ✓    ✓     ✓      ✓    ✓    SUB   ✓    ✓       INS   SUB    ✓       ✓     SUB      ✓      
```

#### Addis Ai
- **Latency**: 3.59s | **Ref Words**: 17 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **11.8%** | **Word Accuracy**: **88.2%** | **CER**: 3.5%

```text
REF : አዎ   ራሴን   በጣም   አሞኛል   ራስ   ምታት   አለብኝ   በዛ   ላይ   ዓይኔ   ብዥ   ብሎብኛል   እጆቼና   እግሮቼም   በጣም   ተወጣጥረው   አብጠዋል  
HYP : አዎ   ራሴን   በጣም   አሞኛል   ራስ   ምታት   አለብኝ   በዛ   ላይ   አይኔ   ብዥ   ብሎብኛል   እጆቼና   እግሮቼም   በጣም   ተወጣጥረው   አውጠዋል  
EVAL: ✓    ✓     ✓     ✓      ✓    ✓     ✓      ✓    ✓    SUB   ✓    ✓       ✓      ✓       ✓     ✓        SUB    
```

#### Gemini
- **Latency**: 7.47s | **Ref Words**: 17 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **11.8%** | **Word Accuracy**: **88.2%** | **CER**: 5.2%

```text
REF : አዎ    ራሴን   በጣም   አሞኛል   ራስ   ምታት   አለብኝ   በዛ   ላይ   ዓይኔ   ብዥ   ብሎብኛል   እጆቼና   እግሮቼም   በጣም   ተወጣጥረው   አብጠዋል  
HYP : ---   ራሴን   በጣም   አሞኛል   ራስ   ምታት   አለብኝ   በዛ   ላይ   አይኔ   ብዥ   ብሎብኛል   እጆቼና   እግሮቼም   በጣም   ተወጣጥረው   አብጠዋል  
EVAL: DEL   ✓     ✓     ✓      ✓    ✓     ✓      ✓    ✓    SUB   ✓    ✓       ✓      ✓       ✓     ✓        ✓      
```

---

### Voice: `v43.wav`
> **Ground Truth Reference**:
> *ሆዴን በድንገት በጣም እየቆርጠኝ ነው፤ ከዛም ደም የቀላቀለ ፈሳሽ እየወረደኝ ነው።*

#### Sahara
- **Latency**: 3.18s | **Ref Words**: 11 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 2.5%

```text
REF : ሆዴን   በድንገት   በጣም   እየቆርጠኝ   ነው   ከዛም   ደም   የቀላቀለ   ፈሳሽ   እየወረደኝ   ነው  
HYP : ሆዴን   በድንገት   በጣም   እየቆረጠኝ   ነው   ከዛም   ደም   የቀላቀለ   ፈሳሽ   እየወረደኝ   ነው  
EVAL: ✓     ✓       ✓     SUB      ✓    ✓     ✓    ✓       ✓     ✓        ✓   
```

#### Addis Ai
- **Latency**: 2.97s | **Ref Words**: 11 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 7.5%

```text
REF : ሆዴን   በድንገት   በጣም   እየቆርጠኝ   ነው   ከዛም   ደም   የቀላቀለ   ፈሳሽ   እየወረደኝ   ነው  
HYP : ሆዴን   በድንገት   በጣም   እየቆረጠኝ   ነው   ከዛም   ደም   የቀለ     ፈሳሽ   እየወረደኝ   ነው  
EVAL: ✓     ✓       ✓     SUB      ✓    ✓     ✓    SUB     ✓     ✓        ✓   
```

#### Gemini
- **Latency**: 7.23s | **Ref Words**: 11 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 2.5%

```text
REF : ሆዴን   በድንገት   በጣም   እየቆርጠኝ   ነው   ከዛም   ደም   የቀላቀለ   ፈሳሽ   እየወረደኝ   ነው  
HYP : ሆዴን   በድንገት   በጣም   እየቆረጠኝ   ነው   ከዛም   ደም   የቀላቀለ   ፈሳሽ   እየወረደኝ   ነው  
EVAL: ✓     ✓       ✓     SUB      ✓    ✓     ✓    ✓       ✓     ✓        ✓   
```

---

### Voice: `v44.wav`
> **Ground Truth Reference**:
> *ሰውነቴ በጣም ግሏል፣ በዛ ላይ ደግሞ ሆዴን ይቆርጠኛል።*

#### Sahara
- **Latency**: 2.81s | **Ref Words**: 8 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 3.9%

```text
REF : ሰውነቴ   በጣም   ግሏል   በዛ   ላይ   ደግሞ   ሆዴን   ይቆርጠኛል  
HYP : ሰውነቴ   በጣም   ግሏል   በዛ   ላይ   ደግሞ   ሆዴን   ይቆርጠኛ   
EVAL: ✓      ✓     ✓     ✓    ✓    ✓     ✓     SUB     
```

#### Addis Ai
- **Latency**: 2.95s | **Ref Words**: 8 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 3.9%

```text
REF : ሰውነቴ   በጣም   ግሏል   በዛ   ላይ   ደግሞ   ሆዴን   ይቆርጠኛል  
HYP : ሰውነቴ   በጣም   ግሏል   በዛ   ላይ   ደሞ    ሆዴን   ይቆርጠኛል  
EVAL: ✓      ✓     ✓     ✓    ✓    SUB   ✓     ✓       
```

#### Gemini
- **Latency**: 7.47s | **Ref Words**: 8 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ሰውነቴ   በጣም   ግሏል   በዛ   ላይ   ደግሞ   ሆዴን   ይቆርጠኛል  
HYP : ሰውነቴ   በጣም   ግሏል   በዛ   ላይ   ደግሞ   ሆዴን   ይቆርጠኛል  
EVAL: ✓      ✓     ✓     ✓    ✓    ✓     ✓     ✓       
```

---

### Voice: `v45.wav`
> **Ground Truth Reference**:
> *ትንፋሼ ተቆራርጧል፣ ቁጭ ብዬ እንኳን መተንፈስ አልቻልኩም፤ ፊቴና አንገቴም አብጠውብኛል።*

#### Sahara
- **Latency**: 3.17s | **Ref Words**: 10 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 4.5%

```text
REF : ትንፋሼ   ተቆራርጧል   ቁጭ   ብዬ   እንኳን   መተንፈስ   አልቻልኩም   ፊቴና   አንገቴም   አብጠውብኛል  
HYP : ትንፋሼ   ተቆራርጧል   ቁጭ   ብዬ   እንኳን   መተንፈስ   አልቻልኩም   ፊቴና   አንገቴም   አወጣውብኛል  
EVAL: ✓      ✓        ✓    ✓    ✓      ✓       ✓        ✓     ✓       SUB      
```

#### Addis Ai
- **Latency**: 3.6s | **Ref Words**: 10 | **Errors**: 5 (S: 2, D: 0, I: 3)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 34.1%

```text
REF : ---   ---    ---    ትንፋሼ   ተቆራርጧል   ቁጭ   ብዬ   እንኳን   መተንፈስ   አልቻልኩም   ፊቴና   አንገቴም   አብጠውብኛል  
HYP : ትንፋ   0xe1   0x88   0xbc   ተቆራርጧል   ቁጭ   ብዬ   እንኳን   መተንፈስ   አልቻልኩም   ፊቴና   አንገቴም   አወጣሁብኛል  
EVAL: INS   INS    INS    SUB    ✓        ✓    ✓    ✓      ✓       ✓        ✓     ✓       SUB      
```

#### Gemini
- **Latency**: 10.06s | **Ref Words**: 10 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 11.4%

```text
REF : ትንፋሼ   ተቆራርጧል   ቁጭ   ብዬ   እንኳን   መተንፈስ   አልቻልኩም   ፊቴና   አንገቴም   አብጠውብኛል   
HYP : ትንፋሼ   ተቆራርጧል   ቁጭ   ብዬ   እንኳን   መተንፈስ   አልቻልኩም   ፊቴና   አንገቴም   አወጣሁብኝአል  
EVAL: ✓      ✓        ✓    ✓    ✓      ✓       ✓        ✓     ✓       SUB       
```

---
