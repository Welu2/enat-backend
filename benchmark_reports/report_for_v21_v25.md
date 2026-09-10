# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v21_v25_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:49:03 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 62 | 16 | 11 | 5 | 0 | **25.8%** | **74.2%** | 15.7% | 2.84s |
| **Addis Ai** | 62 | 10 | 9 | 1 | 0 | **16.1%** | **83.9%** | 3.7% | 3.26s |
| **Gemini** | 62 | 16 | 16 | 0 | 0 | **25.8%** | **74.2%** | 9.3% | 8.16s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v21.wav`
> **Ground Truth Reference**:
> *የበላሁትን ሁሉ እያስመለሰኝ ነው፣ ውኃ እንኳን መያዝ አልቻልኩም፤ መነሳት የማልችልበት ድካም ተሰምቶኛል።*

#### Sahara
- **Latency**: 2.81s | **Ref Words**: 12 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 5.8%

```text
REF : የበላሁትን   ሁሉ   እያስመለሰኝ   ነው   ውኃ    እንኳን   መያዝ   አልቻልኩም   መነሳት   የማልችልበት   ድካም   ተሰምቶኛል  
HYP : የበላሁትን   ሁሉ   እያስመለሰኝ   ነው   ውሃ    እንኳን   መያዝ   አልቻልኩም   መነሳት   የማልችልበት   ድጋፍ   ተሰምቶኛል  
EVAL: ✓        ✓    ✓         ✓    SUB   ✓      ✓     ✓        ✓      ✓         SUB   ✓       
```

#### Addis Ai
- **Latency**: 3.51s | **Ref Words**: 12 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **8.3%** | **Word Accuracy**: **91.7%** | **CER**: 1.9%

```text
REF : የበላሁትን   ሁሉ   እያስመለሰኝ   ነው   ውኃ   እንኳን   መያዝ   አልቻልኩም   መነሳት   የማልችልበት   ድካም   ተሰምቶኛል  
HYP : የበላሁትን   ሁሉ   እያስመለሰኝ   ነው   ውኃ   እንኳን   መያዝ   አልቻልኩም   መነሳት   የማልችልበት   ድጋም   ተሰምቶኛል  
EVAL: ✓        ✓    ✓         ✓    ✓    ✓      ✓     ✓        ✓      ✓         SUB   ✓       
```

#### Gemini
- **Latency**: 8.13s | **Ref Words**: 12 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 3.9%

```text
REF : የበላሁትን   ሁሉ   እያስመለሰኝ   ነው   ውኃ    እንኳን   መያዝ   አልቻልኩም   መነሳት   የማልችልበት   ድካም   ተሰምቶኛል  
HYP : የበላሁትን   ሁሉ   እያስመለሰኝ   ነው   ውሃ    እንኳን   መያዝ   አልቻልኩም   መነሳት   የማልችልበት   ድጋም   ተሰምቶኛል  
EVAL: ✓        ✓    ✓         ✓    SUB   ✓      ✓     ✓        ✓      ✓         SUB   ✓       
```

---

### Voice: `v22.wav`
> **Ground Truth Reference**:
> *ኧረ እኔንጃ! ሆዴን ትንሽ ያመኛል ግን የተለመደው የፅንሱ ግፊት ይሁን ሌላ ነገር መለየት አልቻልኩም።*

#### Sahara
- **Latency**: 2.72s | **Ref Words**: 14 | **Errors**: 6 (S: 4, D: 2, I: 0)
- **WER**: **42.9%** | **Word Accuracy**: **57.1%** | **CER**: 30.6%

```text
REF : ኧረ    እኔንጃ   ሆዴን    ትንሽ   ያመኛል   ግን   የተለመደው   የፅንሱ   ግፊት   ይሁን   ሌላ   ነገር   መለየት   አልቻልኩም  
HYP : ---   እረኔ    እንጆኝ   ትንሽ   ያመኛል   ግን   የተለመደው   የጽንሱ   ክፊት   ይሁን   ሌላ   ነገር   መለየት   ---     
EVAL: DEL   SUB    SUB    ✓     ✓      ✓    ✓        SUB    SUB   ✓     ✓    ✓     ✓      DEL     
```

#### Addis Ai
- **Latency**: 3.32s | **Ref Words**: 14 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **7.1%** | **Word Accuracy**: **92.9%** | **CER**: 2.0%

```text
REF : ኧረ   እኔንጃ   ሆዴን   ትንሽ   ያመኛል   ግን   የተለመደው   የፅንሱ   ግፊት   ይሁን   ሌላ   ነገር   መለየት   አልቻልኩም  
HYP : ኧረ   እኔንጃ   ሆዴን   ትንሽ   ያመኛል   ግን   የተለመደው   የፅንስ   ግፊት   ይሁን   ሌላ   ነገር   መለየት   አልቻልኩም  
EVAL: ✓    ✓      ✓     ✓     ✓      ✓    ✓        SUB    ✓     ✓     ✓    ✓     ✓      ✓       
```

#### Gemini
- **Latency**: 8.4s | **Ref Words**: 14 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **14.3%** | **Word Accuracy**: **85.7%** | **CER**: 4.1%

```text
REF : ኧረ    እኔንጃ   ሆዴን   ትንሽ   ያመኛል   ግን   የተለመደው   የፅንሱ   ግፊት   ይሁን   ሌላ   ነገር   መለየት   አልቻልኩም  
HYP : አረ    እኔንጃ   ሆዴን   ትንሽ   ያመኛል   ግን   የተለመደው   የጽንሱ   ግፊት   ይሁን   ሌላ   ነገር   መለየት   አልቻልኩም  
EVAL: SUB   ✓      ✓     ✓     ✓      ✓    ✓        SUB    ✓     ✓     ✓    ✓     ✓      ✓       
```

---

### Voice: `v23.wav`
> **Ground Truth Reference**:
> *ፈሳሽ ነገር አለ ግን ሽንቴ አምልጦኝ ይሁን ውኃዬ ፈሶ አላወቅኩም፣ ምን ላድርግ?*

#### Sahara
- **Latency**: 2.86s | **Ref Words**: 12 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 10.5%

```text
REF : ፈሳሽ   ነገር   አለ   ግን   ሽንቴ   አምልጦኝ   ይሁን   ውኃዬ   ፈሶ    አላወቅኩም   ምን   ላድርግ  
HYP : ፈሳሽ   ነገር   አለ   ግን   ሽንቴ   አምልጦኝ   ይሁን   ---   ውሃ    አላወቅኩም   ምን   ላድርግ  
EVAL: ✓     ✓     ✓    ✓    ✓     ✓       ✓     DEL   SUB   ✓        ✓    ✓     
```

#### Addis Ai
- **Latency**: 3.02s | **Ref Words**: 12 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **8.3%** | **Word Accuracy**: **91.7%** | **CER**: 2.6%

```text
REF : ፈሳሽ   ነገር   አለ   ግን   ሽንቴ   አምልጦኝ   ይሁን   ውኃዬ   ፈሶ   አላወቅኩም   ምን   ላድርግ  
HYP : ፈሳሽ   ነገር   አለ   ግን   ሽንቴ   አምልጦኝ   ይሁን   ውሃዬ   ፈሶ   አላወቅኩም   ምን   ላድርግ  
EVAL: ✓     ✓     ✓    ✓    ✓     ✓       ✓     SUB   ✓    ✓        ✓    ✓     
```

#### Gemini
- **Latency**: 7.86s | **Ref Words**: 12 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 10.5%

```text
REF : ፈሳሽ   ነገር   አለ   ግን   ሽንቴ    አምልጦኝ   ይሁን   ውኃዬ   ፈሶ   አላወቅኩም   ምን   ላድርግ  
HYP : ፈሳሽ   ነገር   አለ   ግን   ሽንትም   ልጦኝ     ይሁን   ውሃዬ   ፈሶ   አላወኩም    ምን   ላድርግ  
EVAL: ✓     ✓     ✓    ✓    SUB    SUB     ✓     SUB   ✓    SUB      ✓    ✓     
```

---

### Voice: `v24.wav`
> **Ground Truth Reference**:
> *ደም አይደለም ግን ቡናማ መልክ ያለው ፈሳሽ ትንሽ አያለሁ፣ እንደ አደገኛ ምልክት ይቆጠራል?*

#### Sahara
- **Latency**: 2.96s | **Ref Words**: 13 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 20.4%

```text
REF : ደም    አይደለም   ግን   ቡናማ    መልክ   ያለው   ፈሳሽ   ትንሽ   አያለሁ   እንደ   አደገኛ   ምልክት   ይቆጠራል  
HYP : ደግሞ   አይደለም   ግን   ቡናንማ   መልክ   ያለው   ፈሳሽ   ትንሽ   አያለው   እንደ   አደገኛ   ምልክት   ---    
EVAL: SUB   ✓       ✓    SUB    ✓     ✓     ✓     ✓     SUB    ✓     ✓      ✓      DEL    
```

#### Addis Ai
- **Latency**: 3.54s | **Ref Words**: 13 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 6.8%

```text
REF : ደም   አይደለም   ግን   ቡናማ   መልክ    ያለው   ፈሳሽ   ትንሽ   አያለሁ   እንደ   አደገኛ    ምልክት   ይቆጠራል  
HYP : ደም   አይደለም   ግን   ቡናን   ማመልክ   ያለው   ፈሳሽ   ትንሽ   አያለው   እንደ   አደገኛው   ምልክት   ይቆጠራል  
EVAL: ✓    ✓       ✓    SUB   SUB    ✓     ✓     ✓     SUB    ✓     SUB     ✓      ✓      
```

#### Gemini
- **Latency**: 9.17s | **Ref Words**: 13 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **23.1%** | **Word Accuracy**: **76.9%** | **CER**: 9.1%

```text
REF : ደም    አይደለም   ግን   ቡናማ    መልክ   ያለው   ፈሳሽ   ትንሽ   አያለሁ   እንደ   አደገኛ   ምልክት   ይቆጠራል  
HYP : ደሞ    አይደለም   ግን   ቡናንማ   መልክ   ያለው   ፈሳሽ   ትንሽ   አያለሁ   እንደ   አደገኛ   ምልክት   ይቆጠር   
EVAL: SUB   ✓       ✓    SUB    ✓     ✓     ✓     ✓     ✓      ✓     ✓      ✓      SUB    
```

---

### Voice: `v25.wav`
> **Ground Truth Reference**:
> *እ… ራስ ምታቱ አለ፣ ዓይኔም ትንሽ ይደበዝዛል ግን ደም መፍሰስ የለም።*

#### Sahara
- **Latency**: 2.85s | **Ref Words**: 11 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 9.1%

```text
REF : እ…    ራስ   ምታቱ   አለ   ዓይኔም   ትንሽ   ይደበዝዛል   ግን   ደም   መፍሰስ   የለም  
HYP : ---   ራስ   ምታቱ   አለ   አይኔም   ትንሽ   ይደበዝዛል   ግን   ደም   መፍሰስ   የለም  
EVAL: DEL   ✓    ✓     ✓    SUB    ✓     ✓        ✓    ✓    ✓      ✓    
```

#### Addis Ai
- **Latency**: 2.93s | **Ref Words**: 11 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **27.3%** | **Word Accuracy**: **72.7%** | **CER**: 6.1%

```text
REF : እ…    ራስ    ምታቱ   አለ   ዓይኔም   ትንሽ   ይደበዝዛል   ግን   ደም   መፍሰስ   የለም  
HYP : ---   እራስ   ምታቱ   አለ   አይኔም   ትንሽ   ይደበዝዛል   ግን   ደም   መፍሰስ   የለም  
EVAL: DEL   SUB   ✓     ✓    SUB    ✓     ✓        ✓    ✓    ✓      ✓    
```

#### Gemini
- **Latency**: 7.23s | **Ref Words**: 11 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **45.5%** | **Word Accuracy**: **54.5%** | **CER**: 24.2%

```text
REF : እ…    ራስ   ምታቱ   አለ   ዓይኔም   ትንሽ   ይደበዝዛል   ግን   ደም    መፍሰስ   የለም  
HYP : እ     ራስ   ምታት   አለ   አይኔም   ትንሽ   ይደበዝዛል   ግን   እንደ   መፍዘዝ   የለም  
EVAL: SUB   ✓    SUB   ✓    SUB    ✓     ✓        ✓    SUB   SUB    ✓    
```

---
