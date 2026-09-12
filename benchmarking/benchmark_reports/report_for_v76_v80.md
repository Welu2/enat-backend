# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v76_v80_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:51:09 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 57 | 21 | 15 | 6 | 0 | **36.8%** | **63.2%** | 22.1% | 3.43s |
| **Addis Ai** | 57 | 33 | 31 | 1 | 1 | **57.9%** | **42.1%** | 63.6% | 3.85s |
| **Gemini** | 57 | 32 | 28 | 4 | 0 | **56.1%** | **43.9%** | 46.1% | 3.46s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v76.wav`
> **Ground Truth Reference**:
> *Yes, በጣም severe headache አለብኝ፤ paracetamol ወስጄም relief ሊሰጠኝ አልቻለም።*

#### Sahara
- **Latency**: 3.52s | **Ref Words**: 10 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **30.0%** | **Word Accuracy**: **70.0%** | **CER**: 14.8%

```text
REF : yes   በጣም   severe     headache   አለብኝ   paracetamol   ወስጄም   relief   ሊሰጠኝ   አልቻለም  
HYP : yes   በጣም   servious   headache   አለብኝ   parastamol    ወስጄ    relief   ሊሰጠኝ   አልቻለም  
EVAL: ✓     ✓     SUB        ✓          ✓      SUB           SUB    ✓        ✓      ✓      
```

#### Addis Ai
- **Latency**: 4.0s | **Ref Words**: 10 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **60.0%** | **Word Accuracy**: **40.0%** | **CER**: 64.8%

```text
REF : yes   በጣም   severe   headache   አለብኝ   paracetamol   ወስጄም   relief   ሊሰጠኝ   አልቻለም  
HYP : የስ    በጣም   ሰፊው      ሄዴክ        አለብኝ   ፓራስታሞል        ወስጄ    ሪሊፍ      ሊሰጠኝ   አልቻለም  
EVAL: SUB   ✓     SUB      SUB        ✓      SUB           SUB    SUB      ✓      ✓      
```

#### Gemini
- **Latency**: 2.86s | **Ref Words**: 10 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 1.8%

```text
REF : yes   በጣም   severe   headache   አለብኝ   paracetamol   ወስጄም   relief   ሊሰጠኝ   አልቻለም  
HYP : yes   በጣም   severe   headache   አለብኝ   paracetamol   ወስጄ    relief   ሊሰጠኝ   አልቻለም  
EVAL: ✓     ✓     ✓        ✓          ✓      ✓             SUB    ✓        ✓      ✓      
```

---

### Voice: `v77.wav`
> **Ground Truth Reference**:
> *ራሴን አያመኝም but my vision is blurry; screen ወይም ሰው በደንብ focus ማረግ አልቻልኩም።*

#### Sahara
- **Latency**: 3.58s | **Ref Words**: 14 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **14.3%** | **Word Accuracy**: **85.7%** | **CER**: 3.6%

```text
REF : ራሴን   አያመኝም   but   my   vision   is   blurry   screen   ወይም   ሰው   በደንብ   focus   ማረግ    አልቻልኩም  
HYP : ራሴን   አያመኝም   but   my   vision   is   blury    screen   ወይም   ሰው   በደንብ   focus   ማድረግ   አልቻልኩም  
EVAL: ✓     ✓       ✓     ✓    ✓        ✓    SUB      ✓        ✓     ✓    ✓      ✓       SUB    ✓       
```

#### Addis Ai
- **Latency**: 3.95s | **Ref Words**: 14 | **Errors**: 8 (S: 8, D: 0, I: 0)
- **WER**: **57.1%** | **Word Accuracy**: **42.9%** | **CER**: 55.4%

```text
REF : ራሴን   አያመኝም   but   my    vision   is    blurry   screen   ወይም   ሰው   በደንብ   focus   ማረግ    አልቻልኩም  
HYP : ራሴን   አያመኝም   በት    ማይ    ቪዥን      ኢዝ    ብለሪ      ስክሪን     ወይም   ሰው   በደንብ   ፎከስ     ማድረግ   አልቻልኩም  
EVAL: ✓     ✓       SUB   SUB   SUB      SUB   SUB      SUB      ✓     ✓    ✓      SUB     SUB    ✓       
```

#### Gemini
- **Latency**: 3.89s | **Ref Words**: 14 | **Errors**: 12 (S: 12, D: 0, I: 0)
- **WER**: **85.7%** | **Word Accuracy**: **14.3%** | **CER**: 69.6%

```text
REF : ራሴን   አያመኝም   but   my    vision   is    blurry   screen   ወይም   ሰው    በደንብ   focus   ማረግ    አልቻልኩም  
HYP : ዳዴና   እመኝም    በቲስ   ማይ    ቪዥን      ኢዝ    ስፕሪ      ስክሪን     ዌይ    ሰብ    በደንብ   ፎከስ     ማድረግ   አልቻልኩም  
EVAL: SUB   SUB     SUB   SUB   SUB      SUB   SUB      SUB      SUB   SUB   ✓      SUB     SUB    ✓       
```

---

### Voice: `v78.wav`
> **Ground Truth Reference**:
> *አዎ፣ toilet ስሄድ vaginal bleeding አይቻለሁ፤ I am really worried.*

#### Sahara
- **Latency**: 3.43s | **Ref Words**: 10 | **Errors**: 8 (S: 4, D: 4, I: 0)
- **WER**: **80.0%** | **Word Accuracy**: **20.0%** | **CER**: 59.6%

```text
REF : አዎ    toilet   ስሄድ   vaginal   bleeding   አይቻለሁ   i       am    really   worried  
HYP : ---   ---      ---   ---       ኦይሊንግ      ጋር      አይቻለው   im    really   worried  
EVAL: DEL   DEL      DEL   DEL       SUB        SUB     SUB     SUB   ✓        ✓        
```

#### Addis Ai
- **Latency**: 4.1s | **Ref Words**: 10 | **Errors**: 8 (S: 6, D: 1, I: 1)
- **WER**: **80.0%** | **Word Accuracy**: **20.0%** | **CER**: 78.7%

```text
REF : አዎ   toilet   ስሄድ   ---     vaginal   bleeding   አይቻለሁ   i     am    really   worried  
HYP : አዎ   ቶይሌት     ስሄድ   ፈጃይናል   ብሊዲንግ     ጋር         አይቻለሁ   ---   አም    ሪሊ       ወሪድ      
EVAL: ✓    SUB      ✓     INS     SUB       SUB        ✓       DEL   SUB   SUB      SUB      
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 10 | **Errors**: 5 (S: 3, D: 2, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 27.7%

```text
REF : አዎ    toilet   ስሄድ     vaginal   bleeding   አይቻለሁ   i     am    really   worried  
HYP : oh    toilet   sight   vaginal   bleeding   ---     ---   im    really   worried  
EVAL: SUB   ✓        SUB     ✓         ✓          DEL     DEL   SUB   ✓        ✓        
```

---

### Voice: `v79.wav`
> **Ground Truth Reference**:
> *ሽንቴ ሳይሆን continuous የሆነ fluid አለ፤ my water broke መሰለኝ።*

#### Sahara
- **Latency**: 3.41s | **Ref Words**: 10 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 2.3%

```text
REF : ሽንቴ   ሳይሆን   continuous   የሆነ   fluid   አለ   my   water   broke   መሰለኝ  
HYP : ሽንቴ   ሳይሆን   continuous   የሆነ   fluid   አለ   my   water   brok    መሰለኝ  
EVAL: ✓     ✓      ✓            ✓     ✓       ✓    ✓    ✓       SUB     ✓     
```

#### Addis Ai
- **Latency**: 3.51s | **Ref Words**: 10 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 62.8%

```text
REF : ሽንቴ   ሳይሆን   continuous   የሆነ   fluid   አለ   my    water   broke   መሰለኝ  
HYP : ሽንቴ   ሳይሆን   ኮንቲኒየስ       የሆነ   ፍሉድ     አለ   ማይ    ዋተር     ብሩክ     መሰለኝ  
EVAL: ✓     ✓      SUB          ✓     SUB     ✓    SUB   SUB     SUB     ✓     
```

#### Gemini
- **Latency**: 3.28s | **Ref Words**: 10 | **Errors**: 7 (S: 6, D: 1, I: 0)
- **WER**: **70.0%** | **Word Accuracy**: **30.0%** | **CER**: 69.8%

```text
REF : ሽንቴ   ሳይሆን   continuous   የሆነ   fluid   አለ    my     water   broke   መሰለኝ  
HYP : ጤንጤ   ሳይሆን   ኮንቲኒየስ       የሆነ   ---     ፍሉይ   እንዳለ   ማይዋተር   ብሮክ     መሰለኝ  
EVAL: SUB   ✓      SUB          ✓     DEL     SUB   SUB    SUB     SUB     ✓     
```

---

### Voice: `v80.wav`
> **Ground Truth Reference**:
> *ህመም የለም but fetal movement ሙሉ በሙሉ ቆሟል፤ since yesterday ምንም kick አልተሰማኝም።*

#### Sahara
- **Latency**: 3.23s | **Ref Words**: 13 | **Errors**: 7 (S: 5, D: 2, I: 0)
- **WER**: **53.8%** | **Word Accuracy**: **46.2%** | **CER**: 31.0%

```text
REF : ህመም   የለም   but     fetal   movement   ሙሉ   በሙሉ   ቆሟል   since   yesterday   ምንም   kick   አልተሰማኝም  
HYP : ህመም   ---   የለምበት   fatal   movement   ሙሉ   በሙሉ   ቆሟል   ---     sincer      ምንም   ኪል     ተሰማኝ     
EVAL: ✓     DEL   SUB     SUB     ✓          ✓    ✓     ✓     DEL     SUB         ✓     SUB    SUB      
```

#### Addis Ai
- **Latency**: 3.68s | **Ref Words**: 13 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **46.2%** | **Word Accuracy**: **53.8%** | **CER**: 58.6%

```text
REF : ህመም   የለም   but   fetal   movement   ሙሉ   በሙሉ   ቆሟል   since   yesterday   ምንም   kick   አልተሰማኝም  
HYP : ህመም   የለም   በት    ፌታል     ሙቭመንት      ሙሉ   በሙሉ   ቆሟል   ሲንስ     ያስደርደይ      ምንም   ኪክ     አልተሰማኝም  
EVAL: ✓     ✓     SUB   SUB     SUB        ✓    ✓     ✓     SUB     SUB         ✓     SUB    ✓        
```

#### Gemini
- **Latency**: 3.59s | **Ref Words**: 13 | **Errors**: 7 (S: 6, D: 1, I: 0)
- **WER**: **53.8%** | **Word Accuracy**: **46.2%** | **CER**: 62.1%

```text
REF : ህመም   የለም   but   fetal   movement   ሙሉ   በሙሉ   ቆሟል   since   yesterday   ምንም   kick   አልተሰማኝም  
HYP : ሃማም   የለም   ---   በትፌታል   ሙቭመንት      ሙሉ   በሙሉ   ቆሟል   ሲንስ     ያስጀመረኝ      ምንም   ኪክ     አልተሰማኝም  
EVAL: SUB   ✓     DEL   SUB     SUB        ✓    ✓     ✓     SUB     SUB         ✓     SUB    ✓        
```

---
