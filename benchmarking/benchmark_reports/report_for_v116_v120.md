# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v116_v120_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:52:41 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 83 | 18 | 13 | 2 | 3 | **21.7%** | **78.3%** | 10.0% | 4.21s |
| **Addis Ai** | 83 | 23 | 17 | 2 | 4 | **27.7%** | **72.3%** | 21.0% | 4.33s |
| **Gemini** | 83 | 33 | 28 | 1 | 4 | **39.8%** | **60.2%** | 27.8% | 3.84s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v116.wav`
> **Ground Truth Reference**:
> *Stomachኬን stretch አርጎኛል፤ painful አይደለም ግን definitely tight ነው የሚሰማኝ።*

#### Sahara
- **Latency**: 3.76s | **Ref Words**: 10 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **30.0%** | **Word Accuracy**: **70.0%** | **CER**: 10.5%

```text
REF : stomachኬን   stretch   አርጎኛል   painful   አይደለም   ግን   definitely   tight   ነው   የሚሰማኝ  
HYP : stomachin   streat    አርጎኛል   painful   አይደለም   ግን   definitely   tight   ነው   ሚሰማኝ   
EVAL: SUB         SUB       ✓       ✓         ✓       ✓    ✓            ✓       ✓    SUB    
```

#### Addis Ai
- **Latency**: 3.87s | **Ref Words**: 10 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **60.0%** | **Word Accuracy**: **40.0%** | **CER**: 64.9%

```text
REF : stomachኬን   stretch   አርጎኛል    painful   አይደለም   ግን   definitely   tight   ነው   የሚሰማኝ  
HYP : ስቶማኬን       ስትርች      አድርጎኛል   ፔይፎን      አይደለም   ግን   ዴፊኔትሊ        ታይት     ነው   የሚሰማኝ  
EVAL: SUB         SUB       SUB      SUB       ✓       ✓    SUB          SUB     ✓    ✓      
```

#### Gemini
- **Latency**: 3.79s | **Ref Words**: 10 | **Errors**: 7 (S: 6, D: 0, I: 1)
- **WER**: **70.0%** | **Word Accuracy**: **30.0%** | **CER**: 68.4%

```text
REF : ---     stomachኬን   stretch   አርጎኛል   painful   አይደለም   ግን   definitely   tight   ነው   የሚሰማኝ  
HYP : ስታማኪኝ   ስትሬች        አድርጎኛል    ፔን      ፉል        አይደለም   ግን   ዴፊኔትሊ        ታይት     ነው   የሚሰማኝ  
EVAL: INS     SUB         SUB       SUB     SUB       ✓       ✓    SUB          SUB     ✓    ✓      
```

---

### Voice: `v117.wav`
> **Ground Truth Reference**:
> *አዎ፤ ጠዋት እንቁላል ፍርፍር በዳቦ በልቻለሁ፣ ምሳ ደግሞ እንጀራ በስጋ ወጥ እና ጎመን። ማታ ከመደበኛው ውጪ አንድ ተጨማሪ ብርጭቆ ወተትና ሙዝ ወስጃለሁ።*

#### Sahara
- **Latency**: 6.1s | **Ref Words**: 22 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 1.4%

```text
REF : አዎ   ጠዋት   እንቁላል   ፍርፍር   በዳቦ   በልቻለሁ   ምሳ   ደግሞ   እንጀራ   በስጋ   ወጥ   እና   ጎመን   ማታ   ከመደበኛው   ውጪ   አንድ   ተጨማሪ   ብርጭቆ   ---   ወተትና   ሙዝ   ወስጃለሁ  
HYP : አዎ   ጠዋት   እንቁላል   ፍርፍር   በዳቦ   በልቻለሁ   ምሳ   ደግሞ   እንጀራ   በስጋ   ወጥ   እና   ጎመን   ማታ   ከመደበኛው   ውጪ   አንድ   ተጨማሪ   ብርጭቆ   ወተት   እና     ሙዝ   ወስጃለሁ  
EVAL: ✓    ✓     ✓       ✓      ✓     ✓       ✓    ✓     ✓      ✓     ✓    ✓    ✓     ✓    ✓        ✓    ✓     ✓      ✓      INS   SUB    ✓    ✓      
```

#### Addis Ai
- **Latency**: 4.94s | **Ref Words**: 22 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **9.1%** | **Word Accuracy**: **90.9%** | **CER**: 1.4%

```text
REF : አዎ   ጠዋት   እንቁላል   ፍርፍር   በዳቦ   በልቻለሁ   ምሳ   ደግሞ   እንጀራ   በስጋ   ወጥ   እና   ጎመን   ማታ   ከመደበኛው   ውጪ   አንድ   ተጨማሪ   ብርጭቆ   ---   ወተትና   ሙዝ   ወስጃለሁ  
HYP : አዎ   ጠዋት   እንቁላል   ፍርፍር   በዳቦ   በልቻለሁ   ምሳ   ደግሞ   እንጀራ   በስጋ   ወጥ   እና   ጎመን   ማታ   ከመደበኛው   ውጪ   አንድ   ተጨማሪ   ብርጭቆ   ወተት   እና     ሙዝ   ወስጃለሁ  
EVAL: ✓    ✓     ✓       ✓      ✓     ✓       ✓    ✓     ✓      ✓     ✓    ✓    ✓     ✓    ✓        ✓    ✓     ✓      ✓      INS   SUB    ✓    ✓      
```

#### Gemini
- **Latency**: 4.79s | **Ref Words**: 22 | **Errors**: 8 (S: 7, D: 0, I: 1)
- **WER**: **36.4%** | **Word Accuracy**: **63.6%** | **CER**: 17.8%

```text
REF : አዎ    ጠዋት    እንቁላል   ፍርፍር   በዳቦ   በልቻለሁ   ምሳ   ደግሞ   እንጀራ   በስጋ   ወጥ   እና   ጎመን   ማታ   ከመደበኛው   ውጪ   አንድ   ተጨማሪ   ብርጭቆ   ---   ወተትና   ሙዝ    ወስጃለሁ  
HYP : ኧረ    ጣዕሙን   እንቁላል   ፈርፍር   በዳቦ   በልቻለሁ   ምሳ   ደግሞ   እንጀራ   በስጋ   ወጥ   እና   ጎመን   ማታ   ከመደወያው   ውጪ   አንድ   ተጨማሪ   ብርጭቆ   ተተት   እና     ሙዞ    ስጃለሁ   
EVAL: SUB   SUB    ✓       SUB    ✓     ✓       ✓    ✓     ✓      ✓     ✓    ✓    ✓     ✓    SUB      ✓    ✓     ✓      ✓      INS   SUB    SUB   SUB    
```

---

### Voice: `v118.wav`
> **Ground Truth Reference**:
> *በደንብ ተመግቤያለሁ። ቀን ምስር ክክ እና ሰላጣ በልቼ ነበር፣ መክሰስ ላይ ተጨማሪ የተቀቀለ እንቁላል እና አቮካዶ ሰላጣ ወስጃለሁ።*

#### Sahara
- **Latency**: 3.34s | **Ref Words**: 18 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **22.2%** | **Word Accuracy**: **77.8%** | **CER**: 19.1%

```text
REF : በደንብ   ተመግቤያለሁ   ቀን   ምስር   ክክ    እና   ሰላጣ   በልቼ   ነበር   መክሰስ   ላይ   ተጨማሪ   የተቀቀለ   እንቁላል   እና   አቮካዶ      ሰላጣ   ወስጃለሁ  
HYP : በደንብ   ተመግቤያለሁ   ቀን   ምስር   ---   እና   ሰላጣ   በልቼ   ነበር   መክሰስ   ላይ   ተጨማሪ   የተቀቀለ   እንቁላል   እና   avocado   ወስጄ   አለው    
EVAL: ✓      ✓         ✓    ✓     DEL   ✓    ✓     ✓     ✓     ✓      ✓    ✓      ✓       ✓       ✓    SUB       SUB   SUB    
```

#### Addis Ai
- **Latency**: 3.89s | **Ref Words**: 18 | **Errors**: 10 (S: 5, D: 2, I: 3)
- **WER**: **55.6%** | **Word Accuracy**: **44.4%** | **CER**: 25.4%

```text
REF : በደንብ   ተመግቤያለሁ   ቀን   ምስር   ክክ    እና       ሰላጣ   በልቼ   ነበር   መክሰስ   ላይ   ተጨማሪ   የተቀቀለ   ---      ---   ---    እንቁላል   እና     አቮካዶ   ሰላጣ   ወስጃለሁ   
HYP : በደንብ   ተመግቤያለሁ   ቀን   ---   ---   ምስርክክና   ሰላጣ   በልቼ   ነበር   መክሰስ   ላይ   ተጨማሪ   የተቀቀለ   እንቁላልና   አ     0xe1   0x89    0xae   ካዶ     ሰላጣ   ወስጄዋለሁ  
EVAL: ✓      ✓         ✓    DEL   DEL   SUB      ✓     ✓     ✓     ✓      ✓    ✓      ✓       INS      INS   INS    SUB     SUB    SUB    ✓     SUB     
```

#### Gemini
- **Latency**: 3.38s | **Ref Words**: 18 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : በደንብ   ተመግቤያለሁ   ቀን   ምስር   ክክ   እና   ሰላጣ   በልቼ   ነበር   መክሰስ   ላይ   ተጨማሪ   የተቀቀለ   እንቁላል   እና   አቮካዶ   ሰላጣ   ወስጃለሁ  
HYP : በደንብ   ተመግቤያለሁ   ቀን   ምስር   ክክ   እና   ሰላጣ   በልቼ   ነበር   መክሰስ   ላይ   ተጨማሪ   የተቀቀለ   እንቁላል   እና   አቮካዶ   ሰላጣ   ወስጃለሁ  
EVAL: ✓      ✓         ✓    ✓     ✓    ✓    ✓     ✓     ✓     ✓      ✓    ✓      ✓       ✓       ✓    ✓      ✓     ✓      
```

---

### Voice: `v119.wav`
> **Ground Truth Reference**:
> *አዎ ተጨማሪ ምግብ ወስጃለሁ፤ ምሳዬን ከበላሁ በኋላ ረፋድ ላይ ገንፎ በቅቤ በልቻለሁ፣ ፍራፍሬም ብርቱካንና ማንጎ በልቻለሁ።*

#### Sahara
- **Latency**: 3.12s | **Ref Words**: 16 | **Errors**: 5 (S: 4, D: 0, I: 1)
- **WER**: **31.2%** | **Word Accuracy**: **68.8%** | **CER**: 10.0%

```text
REF : አዎ   ተጨማሪ   ምግብ   ወስጃለሁ   ምሳዬን   ከበላሁ   በኋላ   ረፋድ   ላይ   ገንፎ   በቅቤ   በልቻለሁ   ---      ፍራፍሬም    ብርቱካንና   ማንጎ    በልቻለሁ  
HYP : አዎ   ተጨማሪ   ምግብ   ወስጃለሁ   ምሳይን   ከበላሁ   በኋላ   ረፋድ   ላይ   ገንፎ   በቅቤ   በልቻለሁ   ፍርፍሬንም   በብርቱካን   እና       በማንጎ   በልቻለሁ  
EVAL: ✓    ✓      ✓     ✓       SUB    ✓      ✓     ✓     ✓    ✓     ✓     ✓       INS      SUB      SUB      SUB    ✓      
```

#### Addis Ai
- **Latency**: 4.33s | **Ref Words**: 16 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 15.0%

```text
REF : አዎ   ተጨማሪ   ምግብ   ወስጃለሁ   ምሳዬን   ከበላሁ   በኋላ   ረፋድ   ላይ   ገንፎ   በቅቤ   በልቻለሁ   ፍራፍሬም    ብርቱካንና    ማንጎ    በልቻለሁ  
HYP : አዎ   ተጨማሪ   ምግብ   በልቻለሁ   ምሳዬን   ከበላሁ   በኋላ   ረፋድ   ላይ   ገንፎ   በቅቤ   በልቻለሁ   ፍርፍሬንም   በብርትኳንና   በማንጎ   በልቻለሁ  
EVAL: ✓    ✓      ✓     SUB     ✓      ✓      ✓     ✓     ✓    ✓     ✓     ✓       SUB      SUB       SUB    ✓      
```

#### Gemini
- **Latency**: 3.56s | **Ref Words**: 16 | **Errors**: 8 (S: 6, D: 0, I: 2)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 21.7%

```text
REF : አዎ    ተጨማሪ   ምግብ   ---   ወስጃለሁ   ምሳዬን   ከበላሁ   በኋላ   ረፋድ   ላይ   ገንፎ   በቅቤ   ---      በልቻለሁ   ፍራፍሬም    ብርቱካንና   ማንጎ    በልቻለሁ  
HYP : ው     ተጨማሪ   ምግብ   እጅ    አለው     ምሳዬን   ከበላሁ   በኋላ   ረፋድ   ላይ   ገንፎ   በቅቤ   እበላቻለሁ   ፍርፍሬን   በብርቱካን   እና       በማንጎ   በልቻለሁ  
EVAL: SUB   ✓      ✓     INS   SUB     ✓      ✓      ✓     ✓     ✓    ✓     ✓     INS      SUB     SUB      SUB      SUB    ✓      
```

---

### Voice: `v120.wav`
> **Ground Truth Reference**:
> *ጠዋት አጃ አጥሚት በወተት ጠጥቻለሁ፣ ምሳ ዶሮ ወጥ በልቼ ከሰዓት ደግሞ የተጠበሰ ቆሎና ለውዝ ከወተት ጋር ወስጃለሁ።*

#### Sahara
- **Latency**: 4.75s | **Ref Words**: 17 | **Errors**: 4 (S: 2, D: 1, I: 1)
- **WER**: **23.5%** | **Word Accuracy**: **76.5%** | **CER**: 10.7%

```text
REF : ጠዋት   አጃ   አጥሚት   በወተት   ጠጥቻለሁ   ምሳ   ዶሮ   ወጥ   በልቼ   ከሰዓት   ደግሞ   የተጠበሰ   ---   ቆሎና   ለውዝ   ከወተት   ጋር   ወስጃለሁ  
HYP : ጠዋት   አጃ   አጥሚት   በወተት   ጠጥቻለሁ   ምሳ   ዶሮ   ወጥ   በልቼ   ---    ከሳሞ   የተጠበሰ   ቆሎ    እና    ለውዝ   ከወተት   ጋር   ወስጃለሁ  
EVAL: ✓     ✓    ✓      ✓      ✓       ✓    ✓    ✓    ✓     DEL    SUB   ✓       INS   SUB   ✓     ✓      ✓    ✓      
```

#### Addis Ai
- **Latency**: 4.61s | **Ref Words**: 17 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.9%** | **Word Accuracy**: **94.1%** | **CER**: 3.6%

```text
REF : ጠዋት   አጃ   አጥሚት   በወተት   ጠጥቻለሁ   ምሳ   ዶሮ   ወጥ   በልቼ   ከሰዓት   ደግሞ   የተጠበሰ   ቆሎና   ለውዝ   ከወተት   ጋር   ወስጃለሁ  
HYP : ጠዋት   አጃ   አጥሚት   በወተት   ጠጥቻለሁ   ምሳ   ዶሮ   ወጥ   በልቼ   ከሳት    ደግሞ   የተጠበሰ   ቆሎና   ለውዝ   ከወተት   ጋር   ወስጃለሁ  
EVAL: ✓     ✓    ✓      ✓      ✓       ✓    ✓    ✓    ✓     SUB    ✓     ✓       ✓     ✓     ✓      ✓    ✓      
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 17 | **Errors**: 10 (S: 9, D: 1, I: 0)
- **WER**: **58.8%** | **Word Accuracy**: **41.2%** | **CER**: 37.5%

```text
REF : ጠዋት    አጃ    አጥሚት   በወተት   ጠጥቻለሁ    ምሳ     ዶሮ   ወጥ   በልቼ   ከሰዓት   ደግሞ   የተጠበሰ   ቆሎና   ለውዝ    ከወተት   ጋር   ወስጃለሁ  
HYP : ከወትሮ   ሃጅ    አድሚት   በወተት   አጠጣቻለሁ   እሳቸው   ዶሮ   ወጥ   ወለጄ   ከሳል    ደሞ    የተጠበሰ   ---   ቆሎውን   ከወተት   ጋር   ወስጃለሁ  
EVAL: SUB    SUB   SUB    ✓      SUB      SUB    ✓    ✓    SUB   SUB    SUB   ✓       DEL   SUB    ✓      ✓    ✓      
```

---
