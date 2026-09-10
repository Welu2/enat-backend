# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v46_v50_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:49:57 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 71 | 21 | 16 | 5 | 0 | **29.6%** | **70.4%** | 17.0% | 3.49s |
| **Addis Ai** | 71 | 17 | 14 | 3 | 0 | **23.9%** | **76.1%** | 8.7% | 3.94s |
| **Gemini** | 71 | 15 | 13 | 2 | 0 | **21.1%** | **78.9%** | 7.1% | 7.83s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v46.wav`
> **Ground Truth Reference**:
> *እ… እንዴት ልንገርህ… ደም አይደለም ግን ሮዝ የመሰለ ፈሳሽ ዛሬ ጠዋት አይቻለሁ፤ ያ ችግር አለው?*

#### Sahara
- **Latency**: 2.96s | **Ref Words**: 15 | **Errors**: 4 (S: 1, D: 3, I: 0)
- **WER**: **26.7%** | **Word Accuracy**: **73.3%** | **CER**: 23.4%

```text
REF : እ…    እንዴት   ልንገርህ…   ደም    አይደለም   ግን   ሮዝ   የመሰለ   ፈሳሽ   ዛሬ   ጠዋት   አይቻለሁ   ያ    ችግር   አለው  
HYP : ---   እንዴት   ---      ---   ልንገረም   ግን   ሮዝ   የመሰለ   ፈሳሽ   ዛሬ   ጠዋት   አይቻለሁ   ያ    ችግር   አለው  
EVAL: DEL   ✓      DEL      DEL   SUB     ✓    ✓    ✓      ✓     ✓    ✓     ✓       ✓    ✓     ✓    
```

#### Addis Ai
- **Latency**: 3.73s | **Ref Words**: 15 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 10.6%

```text
REF : እ…    እንዴት   ልንገርህ…   ደም    አይደለም   ግን   ሮዝ   የመሰለ   ፈሳሽ   ዛሬ   ጠዋት   አይቻለሁ   ያ    ችግር   አለው  
HYP : ---   እንዴት   ልንገርህ    ደግሞ   አይደለም   ግን   ሮዝ   የመሰለ   ፈሳሽ   ዛሬ   ጠዋት   አይቻለሁ   ያ    ችግር   አለው  
EVAL: DEL   ✓      SUB      SUB   ✓       ✓    ✓    ✓      ✓     ✓    ✓     ✓       ✓    ✓     ✓    
```

#### Gemini
- **Latency**: 8.9s | **Ref Words**: 15 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 8.5%

```text
REF : እ…    እንዴት   ልንገርህ…   ደም    አይደለም   ግን   ሮዝ   የመሰለ   ፈሳሽ   ዛሬ   ጠዋት   አይቻለሁ   ያ    ችግር   አለው  
HYP : ---   እንዴት   ልንገርህ    ደው    አይደለም   ግን   ሮዝ   የመሰለ   ፈሳሽ   ዛሬ   ጠዋት   አይቻለሁ   ያ    ችግር   አለው  
EVAL: DEL   ✓      SUB      SUB   ✓       ✓    ✓    ✓      ✓     ✓    ✓     ✓       ✓    ✓     ✓    
```

---

### Voice: `v47.wav`
> **Ground Truth Reference**:
> *እራሴን ያመኛል ግን ደም መፍሰስ ምናምን የሚባል ነገር የለም፣ ሻይ ብጠጣ ይተወኛል ብዬ አስባለው።*

#### Sahara
- **Latency**: 2.79s | **Ref Words**: 14 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **28.6%** | **Word Accuracy**: **71.4%** | **CER**: 10.6%

```text
REF : እራሴን   ያመኛል   ግን   ደም   መፍሰስ   ምናምን   የሚባል   ነገር   የለም   ሻይ   ብጠጣ   ይተወኛል   ብዬ   አስባለው  
HYP : ራሴን    ያመኛል   ግን   ደም   መፍሰስ   ምናምን   የሚባል   ነገር   የለም   ሻይ   ጠጣው   ይተውኛል   ብዬ   አስባለሁ  
EVAL: SUB    ✓      ✓    ✓    ✓      ✓      ✓      ✓     ✓     ✓    SUB   SUB     ✓    SUB    
```

#### Addis Ai
- **Latency**: 4.22s | **Ref Words**: 14 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **35.7%** | **Word Accuracy**: **64.3%** | **CER**: 10.6%

```text
REF : እራሴን   ያመኛል   ግን   ደም   መፍሰስ   ምናምን   የሚባል   ነገር   የለም   ሻይ   ብጠጣ    ይተወኛል   ብዬ   አስባለው  
HYP : ራሴን    ያመኛል   ግን   ደም   መብሰስ   ምናምን   የሚባል   ነገር   የለም   ሻይ   ብጠጣው   ይተውኛል   ብዬ   አስባለሁ  
EVAL: SUB    ✓      ✓    ✓    SUB    ✓      ✓      ✓     ✓     ✓    SUB    SUB     ✓    SUB    
```

#### Gemini
- **Latency**: 8.87s | **Ref Words**: 14 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **21.4%** | **Word Accuracy**: **78.6%** | **CER**: 6.4%

```text
REF : እራሴን   ያመኛል   ግን   ደም   መፍሰስ   ምናምን   የሚባል   ነገር   የለም   ሻይ   ብጠጣ   ይተወኛል   ብዬ   አስባለው  
HYP : ራሴን    ያመኛል   ግን   ደም   መብሰስ   ምናምን   የሚባል   ነገር   የለም   ሻይ   ብጠጣ   ይተወኛል   ብዬ   አስባለሁ  
EVAL: SUB    ✓      ✓    ✓    SUB    ✓      ✓      ✓     ✓     ✓    ✓     ✓       ✓    SUB    
```

---

### Voice: `v48.wav`
> **Ground Truth Reference**:
> *ዓይኔ የሚዥጎረጎረው በመድኃኒቱ ምክንያት ይሆን ወይስ በህመሙ አላወቅኩም፤ ግን ራሴን ያመኛል።*

#### Sahara
- **Latency**: 3.19s | **Ref Words**: 11 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **45.5%** | **Word Accuracy**: **54.5%** | **CER**: 19.1%

```text
REF : ዓይኔ   የሚዥጎረጎረው   በመድኃኒቱ    ምክንያት   ይሆን   ወይስ   በህመሙ   አላወቅኩም   ግን   ራሴን   ያመኛል  
HYP : አይኔ   የሚዥጎራው     በመድሀኒቱም   ምክንያት   ይሁን   ወይስ   በህመሙ   አላወቅ     ግን   ራሴን   ያመኛል  
EVAL: SUB   SUB        SUB       ✓       SUB   ✓     ✓      SUB      ✓    ✓     ✓     
```

#### Addis Ai
- **Latency**: 3.29s | **Ref Words**: 11 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **27.3%** | **Word Accuracy**: **72.7%** | **CER**: 6.4%

```text
REF : ዓይኔ   የሚዥጎረጎረው   በመድኃኒቱ   ምክንያት   ይሆን   ወይስ   በህመሙ   አላወቅኩም   ግን   ራሴን   ያመኛል  
HYP : አይኔ   የሚሽጎረጎረው   በመድሃኒቱ   ምክንያት   ይሆን   ወይስ   በህመሙ   አላወቅኩም   ግን   ራሴን   ያመኛል  
EVAL: SUB   SUB        SUB      ✓       ✓     ✓     ✓      ✓        ✓    ✓     ✓     
```

#### Gemini
- **Latency**: 11.56s | **Ref Words**: 11 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **36.4%** | **Word Accuracy**: **63.6%** | **CER**: 8.5%

```text
REF : ዓይኔ   የሚዥጎረጎረው   በመድኃኒቱ   ምክንያት   ይሆን   ወይስ   በህመሙ   አላወቅኩም   ግን   ራሴን   ያመኛል  
HYP : አይኔ   የሚዥጎረጎረው   በመድሃኒቱ   ምክንያት   ይሁን   ወይስ   በህመሙ   አላወኩም    ግን   ራሴን   ያመኛል  
EVAL: SUB   ✓          SUB      ✓       SUB   ✓     ✓      SUB      ✓    ✓     ✓     
```

---

### Voice: `v49.wav`
> **Ground Truth Reference**:
> *ሆዴን ይነፋኛል፣ ቁርጠት አለው… ቆይ ግን እንደዚህ አይነት ህመም መደበኛ ነው ወይስ ወደ ክሊኒክ ልሂድ?*

#### Sahara
- **Latency**: 2.86s | **Ref Words**: 15 | **Errors**: 5 (S: 3, D: 2, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 24.0%

```text
REF : ሆዴን   ይነፋኛል   ቁርጠት   አለው…   ቆይ   ግን   እንደዚህ   አይነት   ህመም   መደበኛ   ነው   ወይስ   ወደ    ክሊኒክ   ልሂድ         
HYP : ሁዴን   ይነፋኛል   ቁርጠት   አለው    ቆይ   ግን   እንደዚህ   አይነት   ህመም   መደበኛ   ነው   ወይስ   ---   ---    clinically  
EVAL: SUB   ✓       ✓      SUB    ✓    ✓    ✓       ✓      ✓     ✓      ✓    ✓     DEL   DEL    SUB         
```

#### Addis Ai
- **Latency**: 3.05s | **Ref Words**: 15 | **Errors**: 4 (S: 2, D: 2, I: 0)
- **WER**: **26.7%** | **Word Accuracy**: **73.3%** | **CER**: 12.0%

```text
REF : ሆዴን   ይነፋኛል   ቁርጠት   አለው…     ቆይ   ግን   እንደዚህ   አይነት   ህመም   መደበኛ   ነው   ወይስ   ወደ    ክሊኒክ   ልሂድ  
HYP : ሆዴን   ይነፋኛል   ---    ቁርጠታለው   ቆይ   ግን   እንደዚህ   አይነት   ህመም   መደበኛ   ነው   ወይስ   ---   ክሊኒክ   ሊሂድ  
EVAL: ✓     ✓       DEL    SUB      ✓    ✓    ✓       ✓      ✓     ✓      ✓    ✓     DEL   ✓      SUB  
```

#### Gemini
- **Latency**: 4.44s | **Ref Words**: 15 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **13.3%** | **Word Accuracy**: **86.7%** | **CER**: 6.0%

```text
REF : ሆዴን   ይነፋኛል   ቁርጠት   አለው…   ቆይ   ግን   እንደዚህ   አይነት   ህመም   መደበኛ   ነው   ወይስ   ወደ    ክሊኒክ   ልሂድ  
HYP : ሆዴን   ይነፋኛል   ቁርጠት   አለው    ቆይ   ግን   እንደዚህ   አይነት   ህመም   መደበኛ   ነው   ወይስ   ---   ክሊኒክ   ልሂድ  
EVAL: ✓     ✓       ✓      SUB    ✓    ✓    ✓       ✓      ✓     ✓      ✓    ✓     DEL   ✓      ✓    
```

---

### Voice: `v50.wav`
> **Ground Truth Reference**:
> *አልገባኝም… ፈሳሽ ማለት ሽንት ነው ወይስ ሌላ? ምክንያቱም ዛሬ ቶሎ ቶሎ ስሸና ነበረ፣ ህመም ግን የለኝም።*

#### Sahara
- **Latency**: 5.66s | **Ref Words**: 16 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **18.8%** | **Word Accuracy**: **81.2%** | **CER**: 8.0%

```text
REF : አልገባኝም…   ፈሳሽ   ማለት   ሽንት   ነው   ወይስ   ሌላ   ምክንያቱም   ዛሬ   ቶሎ   ቶሎ   ስሸና   ነበረ   ህመም   ግን   የለኝም  
HYP : አልገባኝም    ፈሳሽ   ማለት   ሽንት   ነው   ወይስ   ሌላ   ምክንያቱም   ዛሬ   ቶሎ   ቶሎ   ስሻራ   ነበር   ህመም   ግን   የለኝም  
EVAL: SUB       ✓     ✓     ✓     ✓    ✓     ✓    ✓        ✓    ✓    ✓    SUB   SUB   ✓     ✓    ✓     
```

#### Addis Ai
- **Latency**: 5.4s | **Ref Words**: 16 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 4.0%

```text
REF : አልገባኝም…   ፈሳሽ   ማለት   ሽንት   ነው   ወይስ   ሌላ   ምክንያቱም   ዛሬ   ቶሎ   ቶሎ   ስሸና   ነበረ   ህመም   ግን   የለኝም  
HYP : አልገባኝም    ፈሳሽ   ማለት   ሽንት   ነው   ወይስ   ሌላ   ምክንያቱም   ዛሬ   ቶሎ   ቶሎ   ስሸና   ነበር   ህመም   ግን   የለኝም  
EVAL: SUB       ✓     ✓     ✓     ✓    ✓     ✓    ✓        ✓    ✓    ✓    ✓     SUB   ✓     ✓    ✓     
```

#### Gemini
- **Latency**: 5.4s | **Ref Words**: 16 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **18.8%** | **Word Accuracy**: **81.2%** | **CER**: 6.0%

```text
REF : አልገባኝም…   ፈሳሽ   ማለት   ሽንት   ነው   ወይስ   ሌላ   ምክንያቱም   ዛሬ   ቶሎ   ቶሎ   ስሸና   ነበረ   ህመም   ግን   የለኝም  
HYP : አልገባኝም    ፈሳሽ   ማለት   ሽንት   ነው   ወይስ   ሌላ   ምክንያቱም   ዛሬ   ቶሎ   ቶሎ   እሸና   ነበር   ህመም   ግን   የለኝም  
EVAL: SUB       ✓     ✓     ✓     ✓    ✓     ✓    ✓        ✓    ✓    ✓    SUB   SUB   ✓     ✓    ✓     
```

---
