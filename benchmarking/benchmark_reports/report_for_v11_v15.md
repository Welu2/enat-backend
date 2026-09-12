# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v11_v15_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:48:34 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 54 | 14 | 11 | 2 | 1 | **25.9%** | **74.1%** | 13.5% | 2.92s |
| **Addis Ai** | 54 | 7 | 7 | 0 | 0 | **13.0%** | **87.0%** | 4.5% | 3.05s |
| **Gemini** | 54 | 12 | 12 | 0 | 0 | **22.2%** | **77.8%** | 9.0% | 8.43s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v11.wav`
> **Ground Truth Reference**:
> *ራሴን አያመኝም ግን ከሰዓት ጀምሮ ዓይኔ በጣም ይብዥጎረጎራል፣ ነገሮችን በደንብ ማየት አልቻልኩም።*

#### Sahara
- **Latency**: 3.09s | **Ref Words**: 12 | **Errors**: 4 (S: 2, D: 2, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 28.6%

```text
REF : ራሴን   አያመኝም   ግን   ከሰዓት   ጀምሮ   ዓይኔ   በጣም   ይብዥጎረጎራል   ነገሮችን   በደንብ   ማየት   አልቻልኩም  
HYP : ራሴን   አያመኝም   ግን   ከሰዓት   ጀምሮ   አይኔ   በጣም   ይጅጎራል      ነገሮችን   በደንብ   ---   ---     
EVAL: ✓     ✓       ✓    ✓      ✓     SUB   ✓     SUB        ✓       ✓      DEL   DEL     
```

#### Addis Ai
- **Latency**: 3.69s | **Ref Words**: 12 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 6.1%

```text
REF : ራሴን    አያመኝም   ግን   ከሰዓት   ጀምሮ   ዓይኔ   በጣም   ይብዥጎረጎራል   ነገሮችን   በደንብ   ማየት   አልቻልኩም  
HYP : እራሴን   አያመኝም   ግን   ከሰዓት   ጀምሮ   አይኔ   በጣም   ይዥጎረጎራል    ነገሮችን   በደንብ   ማየት   አልቻልኩም  
EVAL: SUB    ✓       ✓    ✓      ✓     SUB   ✓     SUB        ✓       ✓      ✓     ✓       
```

#### Gemini
- **Latency**: 9.05s | **Ref Words**: 12 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 12.2%

```text
REF : ራሴን   አያመኝም   ግን   ከሰዓት   ጀምሮ   ዓይኔ   በጣም   ይብዥጎረጎራል   ነገሮችን   በደንብ   ማየት   አልቻልኩም  
HYP : ራሴን   አየመኝም   ግን   ከሰአት   ጀምሮ   አይኔ   በጣም   ይሽርጎጎራል    ነገሮችን   በደንብ   ማየት   አልቻልኩም  
EVAL: ✓     SUB     ✓    SUB    ✓     SUB   ✓     SUB        ✓       ✓      ✓     ✓       
```

---

### Voice: `v12.wav`
> **Ground Truth Reference**:
> *አዎ፤ ሽንት ቤት ስገባ ትንሽ ደም ነገር አይቻለሁ፣ በጣም አስፈርቶኛል።*

#### Sahara
- **Latency**: 2.64s | **Ref Words**: 10 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 3.0%

```text
REF : አዎ   ሽንት   ቤት    ስገባ   ትንሽ   ደም   ነገር   አይቻለሁ   በጣም   አስፈርቶኛል  
HYP : አዎ   ሽንት   ፊት    ስገባ   ትንሽ   ደም   ነገር   አይቻለሁ   በጣም   አስፈርቶኛል  
EVAL: ✓    ✓     SUB   ✓     ✓     ✓    ✓     ✓       ✓     ✓        
```

#### Addis Ai
- **Latency**: 3.0s | **Ref Words**: 10 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አዎ   ሽንት   ቤት   ስገባ   ትንሽ   ደም   ነገር   አይቻለሁ   በጣም   አስፈርቶኛል  
HYP : አዎ   ሽንት   ቤት   ስገባ   ትንሽ   ደም   ነገር   አይቻለሁ   በጣም   አስፈርቶኛል  
EVAL: ✓    ✓     ✓    ✓     ✓     ✓    ✓     ✓       ✓     ✓        
```

#### Gemini
- **Latency**: 8.03s | **Ref Words**: 10 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : አዎ   ሽንት   ቤት   ስገባ   ትንሽ   ደም   ነገር   አይቻለሁ   በጣም   አስፈርቶኛል  
HYP : አዎ   ሽንት   ቤት   ስገባ   ትንሽ   ደም   ነገር   አይቻለሁ   በጣም   አስፈርቶኛል  
EVAL: ✓    ✓     ✓    ✓     ✓     ✓    ✓     ✓       ✓     ✓        
```

---

### Voice: `v13.wav`
> **Ground Truth Reference**:
> *ሽንቴ ሳይሆን እንደ ውኃ ያለ ንጹሕ ፈሳሽ ያለማቋረጥ እየፈሰሰኝ ነው፣ ልብሴ ሁሉ ርሷል።*

#### Sahara
- **Latency**: 2.37s | **Ref Words**: 13 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 14.3%

```text
REF : ሽንቴ   ሳይሆን   እንደ   ውኃ    ያለ   ንጹሕ   ፈሳሽ   ያለማቋረጥ   እየፈሰሰኝ   ነው   ልብሴ   ሁሉ   ርሷል   
HYP : ሽንቴ   ሳይሆን   እንደ   ውሃ    ያለ   ንፁህ   ፈቶ    ያለማቋረጥ   እየፈሰሰኝ   ነው   ልብሴ   ሁሉ   እርሷል  
EVAL: ✓     ✓      ✓     SUB   ✓    SUB   SUB   ✓        ✓        ✓    ✓     ✓    SUB   
```

#### Addis Ai
- **Latency**: 2.94s | **Ref Words**: 13 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 4.8%

```text
REF : ሽንቴ   ሳይሆን   እንደ   ውኃ    ያለ   ንጹሕ   ፈሳሽ   ያለማቋረጥ   እየፈሰሰኝ   ነው   ልብሴ   ሁሉ   ርሷል  
HYP : ሽንቴ   ሳይሆን   እንደ   ውሃ    ያለ   ንጹህ   ፈሳሽ   ያለማቋረጥ   እየፈሰሰኝ   ነው   ልብሴ   ሁሉ   ርሷል  
EVAL: ✓     ✓      ✓     SUB   ✓    SUB   ✓     ✓        ✓        ✓    ✓     ✓    ✓    
```

#### Gemini
- **Latency**: 7.75s | **Ref Words**: 13 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 9.5%

```text
REF : ሽንቴ   ሳይሆን   እንደ   ውኃ    ያለ   ንጹሕ   ፈሳሽ   ያለማቋረጥ   እየፈሰሰኝ   ነው   ልብሴ   ሁሉ   ርሷል  
HYP : ሽንጤ   ሳይሆን   እንደ   ውሃ    ያለ   ንጹህ   ፈሳሽ   ያለማቋረጥ   እየፈሰሰኝ   ነው   ልብሴ   ሁሉ   ረሷል  
EVAL: SUB   ✓      ✓     SUB   ✓    SUB   ✓     ✓        ✓        ✓    ✓     ✓    SUB  
```

---

### Voice: `v14.wav`
> **Ground Truth Reference**:
> *ሆዴን በጣም አጥብቆ እየቆረጠኝ ነው፤ መቆምም ሆነ መቀመጥ አልቻልኩም።*

#### Sahara
- **Latency**: 3.11s | **Ref Words**: 9 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 8.8%

```text
REF : ሆዴን   በጣም   አጥብቆ   እየቆረጠኝ   ነው   መቆምም   ሆነ   መቀመጥ   አልቻልኩም  
HYP : ሆዴን   በጣም   አጥብቆ   እየወጠረኝ   ነው   መቆምም   ሆነ   መቀመጥ   አልቻልኩም  
EVAL: ✓     ✓     ✓      SUB      ✓    ✓      ✓    ✓      ✓       
```

#### Addis Ai
- **Latency**: 2.88s | **Ref Words**: 9 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 8.8%

```text
REF : ሆዴን   በጣም   አጥብቆ   እየቆረጠኝ   ነው   መቆምም   ሆነ   መቀመጥ   አልቻልኩም  
HYP : ሆዴን   በጣም   አጥብቆ   እየወጠረኝ   ነው   መቆምም   ሆነ   መቀመጥ   አልቻልኩም  
EVAL: ✓     ✓     ✓      SUB      ✓    ✓      ✓    ✓      ✓       
```

#### Gemini
- **Latency**: 8.32s | **Ref Words**: 9 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 8.8%

```text
REF : ሆዴን   በጣም   አጥብቆ   እየቆረጠኝ   ነው   መቆምም   ሆነ   መቀመጥ   አልቻልኩም  
HYP : ሆዴን   በጣም   አጥብቆ   እየወጣራኝ   ነው   መቆምም   ሆነ   መቀመጥ   አልቻልኩም  
EVAL: ✓     ✓     ✓      SUB      ✓    ✓      ✓    ✓      ✓       
```

---

### Voice: `v15.wav`
> **Ground Truth Reference**:
> *እጆቼና ፊቴ በጣም አብጠዋል፤ የጣት ቀለበቴ ሊወልቅ አልቻለም፣ ዓይኖቼም ተነፋፍተዋል።*

#### Sahara
- **Latency**: 3.38s | **Ref Words**: 10 | **Errors**: 4 (S: 3, D: 0, I: 1)
- **WER**: **40.0%** | **Word Accuracy**: **60.0%** | **CER**: 7.1%

```text
REF : ---   እጆቼና   ፊቴ   በጣም   አብጠዋል   የጣት   ቀለበቴ   ሊወልቅ   አልቻለም   ዓይኖቼም   ተነፋፍተዋል  
HYP : እጆቼ   እና     ፊቴ   በጣም   አብጠዋል   የጣት   ቀለበቴ   ሊልቅ    አልቻለም   አይኖቼም   ተነፋፍተዋል  
EVAL: INS   SUB    ✓    ✓     ✓       ✓     ✓      SUB    ✓       SUB     ✓        
```

#### Addis Ai
- **Latency**: 2.76s | **Ref Words**: 10 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 2.4%

```text
REF : እጆቼና   ፊቴ   በጣም   አብጠዋል   የጣት   ቀለበቴ   ሊወልቅ   አልቻለም   ዓይኖቼም   ተነፋፍተዋል  
HYP : እጆቼና   ፊቴ   በጣም   አብጠዋል   የጣት   ቀለበቴ   ሊወልቅ   አልቻለም   አይኖቼም   ተነፋፍተዋል  
EVAL: ✓      ✓    ✓     ✓       ✓     ✓      ✓      ✓       SUB     ✓        
```

#### Gemini
- **Latency**: 9.0s | **Ref Words**: 10 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **30.0%** | **Word Accuracy**: **70.0%** | **CER**: 11.9%

```text
REF : እጆቼና   ፊቴ   በጣም    አብጠዋል    የጣት   ቀለበቴ   ሊወልቅ   አልቻለም   ዓይኖቼም   ተነፋፍተዋል  
HYP : እጆቼና   ፊቴ   በጣሙን   አብጥተዋል   የጣት   ቀለበቴ   ሊወልቅ   አልቻለም   አይኖቼም   ተነፋፍተዋል  
EVAL: ✓      ✓    SUB    SUB      ✓     ✓      ✓      ✓       SUB     ✓        
```

---
