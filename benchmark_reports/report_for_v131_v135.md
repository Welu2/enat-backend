# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v131_v135_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:55:54 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 74 | 27 | 19 | 7 | 1 | **36.5%** | **63.5%** | 19.0% | 4.30s |
| **Addis Ai** | 74 | 26 | 24 | 2 | 0 | **35.1%** | **64.9%** | 32.5% | 4.92s |
| **Gemini** | 74 | 30 | 26 | 3 | 1 | **40.5%** | **59.5%** | 22.0% | 8.08s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v131.wav`
> **Ground Truth Reference**:
> *አዎ፤ ጠዋት የገብስ አጥሚት በደንብ ጠጥቻለሁ፣ ምሳ ላይ ደግሞ የስንዴ ቂጣ በቅቤ በልቻለሁ፣ ጉልበት እንዲሆነኝ።*

#### Sahara
- **Latency**: 3.48s | **Ref Words**: 15 | **Errors**: 5 (S: 3, D: 1, I: 1)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 9.4%

```text
REF : አዎ   ጠዋት   የገብስ   አጥሚት   በደንብ   ጠጥቻለሁ   ምሳ    ላይ    ደግሞ   የስንዴ   ቂጣ   በቅቤ   በልቻለሁ    ጉልበት   ---   እንዲሆነኝ  
HYP : አዎ   ጠዋት   የገብስ   አጥሚት   በደንብ   ጠጥቻለሁ   ---   ምሳሌ   ደግሞ   የስንዴ   ቂጣ   በቅቤ   በልቼዋለሁ   ጉልበት   እንዴ   ሆነኝ     
EVAL: ✓    ✓     ✓      ✓      ✓      ✓       DEL   SUB   ✓     ✓      ✓    ✓     SUB      ✓      INS   SUB     
```

#### Addis Ai
- **Latency**: 4.53s | **Ref Words**: 15 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **6.7%** | **Word Accuracy**: **93.3%** | **CER**: 1.9%

```text
REF : አዎ   ጠዋት   የገብስ   አጥሚት   በደንብ   ጠጥቻለሁ   ምሳ   ላይ   ደግሞ   የስንዴ   ቂጣ   በቅቤ   በልቻለሁ   ጉልበት   እንዲሆነኝ  
HYP : አዎ   ጣዋት   የገብስ   አጥሚት   በደንብ   ጠጥቻለሁ   ምሳ   ላይ   ደግሞ   የስንዴ   ቂጣ   በቅቤ   በልቻለሁ   ጉልበት   እንዲሆነኝ  
EVAL: ✓    SUB   ✓      ✓      ✓      ✓       ✓    ✓    ✓     ✓      ✓    ✓     ✓       ✓      ✓       
```

#### Gemini
- **Latency**: 23.42s | **Ref Words**: 15 | **Errors**: 8 (S: 8, D: 0, I: 0)
- **WER**: **53.3%** | **Word Accuracy**: **46.7%** | **CER**: 26.4%

```text
REF : አዎ    ጠዋት    የገብስ   አጥሚት   በደንብ   ጠጥቻለሁ   ምሳ   ላይ   ደግሞ   የስንዴ   ቂጣ   በቅቤ   በልቻለሁ    ጉልበት   እንዲሆነኝ  
HYP : ው     ውሃውት   የገብሳ   ጭሚት    በደንብ   ጠጥቻቸው   ምሳ   ላይ   ደግሞ   የስንዴ   ቂጣ   በቁብ   ይበልቻለሁ   ጉልበት   እንዴሆነው  
EVAL: SUB   SUB    SUB    SUB    ✓      SUB     ✓    ✓    ✓     ✓      ✓    SUB   SUB      ✓      SUB     
```

---

### Voice: `v132.wav`
> **Ground Truth Reference**:
> *በሶ እና የሰሊጥ ገንፎ ወስጃለሁ፤ ለህፃኑም እድገት ጥሩ ነው ስለተባልኩ ተጨማሪ ምግብ በደንብ እየወሰድኩ ነው።*

#### Sahara
- **Latency**: 5.17s | **Ref Words**: 15 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **26.7%** | **Word Accuracy**: **73.3%** | **CER**: 11.1%

```text
REF : በሶ    እና    የሰሊጥ   ገንፎ   ወስጃለሁ    ለህፃኑም   እድገት   ጥሩ   ነው   ስለተባልኩ   ተጨማሪ   ምግብ   በደንብ   እየወሰድኩ   ነው  
HYP : በሱ    ነው    የሰሊጥ   ገንፎ   ወስጄዋለሁ   ለህፃኑ    እድገት   ጥሩ   ነው   ስለተባልኩ   ተጨማሪ   ምግብ   በደንብ   እየወሰድኩ   ነው  
EVAL: SUB   SUB   ✓      ✓     SUB      SUB     ✓      ✓    ✓    ✓        ✓      ✓     ✓      ✓        ✓   
```

#### Addis Ai
- **Latency**: 4.41s | **Ref Words**: 15 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **26.7%** | **Word Accuracy**: **73.3%** | **CER**: 7.4%

```text
REF : በሶ    እና    የሰሊጥ   ገንፎ   ወስጃለሁ    ለህፃኑም   እድገት   ጥሩ   ነው   ስለተባልኩ   ተጨማሪ   ምግብ   በደንብ   እየወሰድኩ   ነው  
HYP : ---   በሶና   የሰሊጥ   ገንፎ   ወስጄዋለሁ   ለህፃኑም   ምድገት   ጥሩ   ነው   ስለተባልኩ   ተጨማሪ   ምግብ   በደንብ   እየወሰድኩ   ነው  
EVAL: DEL   SUB   ✓      ✓     SUB      ✓       SUB    ✓    ✓    ✓        ✓      ✓     ✓      ✓        ✓   
```

#### Gemini
- **Latency**: 4.91s | **Ref Words**: 15 | **Errors**: 6 (S: 3, D: 2, I: 1)
- **WER**: **40.0%** | **Word Accuracy**: **60.0%** | **CER**: 18.5%

```text
REF : በሶ    እና    የሰሊጥ   ገንፎ   ወስጃለሁ   ለህፃኑም   ---   እድገት   ጥሩ   ነው   ስለተባልኩ   ተጨማሪ   ምግብ   በደንብ   እየወሰድኩ   ነው  
HYP : ---   በሶና   የሰሊጥ   ገንፎ   ወስጃለሁ   ለህፃኑም   ምግብ   እጅ     ጥሩ   ነው   ስለተባልኩ   ተጨማሪ   ምግብ   ---    በየወሰድኩ   ነው  
EVAL: DEL   SUB   ✓      ✓     ✓       ✓       INS   SUB    ✓    ✓    ✓        ✓      ✓     DEL    SUB      ✓   
```

---

### Voice: `v133.wav`
> **Ground Truth Reference**:
> *እንጀራ በአልጫ ስጋ ተመግቤያለሁ፤ መክሰስ ላይ ደግሞ ተልባ ተበጥብጦ ጠጥቻለሁ።*

#### Sahara
- **Latency**: 5.06s | **Ref Words**: 10 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 5.1%

```text
REF : እንጀራ   በአልጫ   ስጋ   ተመግቤያለሁ   መክሰስ   ላይ   ደግሞ   ተልባ   ተበጥብጦ   ጠጥቻለሁ  
HYP : እንጀራ   በአልጫ   ስጋ   ተመግቤያለሁ   መክሰስ   ላይ   ደግሞ   ተልባ   ተበዝብጦ   ተጥቻለሁ  
EVAL: ✓      ✓      ✓    ✓         ✓      ✓    ✓     ✓     SUB     SUB    
```

#### Addis Ai
- **Latency**: 6.04s | **Ref Words**: 10 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 7.7%

```text
REF : እንጀራ   በአልጫ   ስጋ   ተመግቤያለሁ   መክሰስ   ላይ   ደግሞ   ተልባ   ተበጥብጦ   ጠጥቻለሁ   
HYP : እንጀራ   በአልጫ   ስጋ   ተመግቤያለሁ   መክሰስ   ላይ   ደግሞ   ተልባ   ተበዝብጦ   ተሰጥቻለሁ  
EVAL: ✓      ✓      ✓    ✓         ✓      ✓    ✓     ✓     SUB     SUB     
```

#### Gemini
- **Latency**: 3.9s | **Ref Words**: 10 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **30.0%** | **Word Accuracy**: **70.0%** | **CER**: 7.7%

```text
REF : እንጀራ   በአልጫ   ስጋ   ተመግቤያለሁ   መክሰስ   ላይ   ደግሞ   ተልባ    ተበጥብጦ   ጠጥቻለሁ   
HYP : እንጀራ   አልጫ    ስጋ   ተመግቤያለሁ   መክሰስ   ላይ   ደግሞ   የተልባ   ተበጥብጦ   ተጠጥቻለሁ  
EVAL: ✓      SUB    ✓    ✓         ✓      ✓    ✓     SUB    ✓       SUB     
```

---

### Voice: `v134.wav`
> **Ground Truth Reference**:
> *አዎ፤ የሽንብራ አሳ እና ወተት በደንብ ወስጃለሁ፣ የተመጣጠነ እንዲሆንም ብርቱካን ጨምሬበታለሁ።*

#### Sahara
- **Latency**: 3.54s | **Ref Words**: 11 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **36.4%** | **Word Accuracy**: **63.6%** | **CER**: 8.5%

```text
REF : አዎ   የሽንብራ   አሳ      እና    ወተት   በደንብ   ወስጃለሁ   የተመጣጠነ   እንዲሆንም   ብርቱካን   ጨምሬበታለሁ  
HYP : አዎ   ---     የሽምብራ   ሳና    ወተት   በደንብ   ወስጃለሁ   የተመጣጠን   እንዲሆንም   ብርቱካን   ጨምሬበታለሁ  
EVAL: ✓    DEL     SUB     SUB   ✓     ✓      ✓       SUB      ✓        ✓       ✓        
```

#### Addis Ai
- **Latency**: 4.11s | **Ref Words**: 11 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **27.3%** | **Word Accuracy**: **72.7%** | **CER**: 6.4%

```text
REF : አዎ   የሽንብራ   አሳ       እና   ወተት   በደንብ   ወስጃለሁ   የተመጣጠነ   እንዲሆንም   ብርቱካን   ጨምሬበታለሁ  
HYP : አዎ   ---     የሽምብራሳ   እና   ወተት   በደንብ   ወስጃለሁ   የተመጣጠን   እንዲሆንም   ብርቱካን   ጨምሬበታለሁ  
EVAL: ✓    DEL     SUB      ✓    ✓     ✓      ✓       SUB      ✓        ✓       ✓        
```

#### Gemini
- **Latency**: 3.88s | **Ref Words**: 11 | **Errors**: 8 (S: 8, D: 0, I: 0)
- **WER**: **72.7%** | **Word Accuracy**: **27.3%** | **CER**: 40.4%

```text
REF : አዎ    የሽንብራ   አሳ    እና     ወተት     በደንብ   ወስጃለሁ   የተመጣጠነ   እንዲሆንም   ብርቱካን   ጨምሬበታለሁ  
HYP : ኦ     የሽምብራ   ሳና    ውህደት   ቫይታሚን   b6     አለው     የተመጣጠነ   እንዲሆንም   ብርትኳን   ጨምሬበታለሁ  
EVAL: SUB   SUB     SUB   SUB    SUB     SUB    SUB     ✓        ✓        SUB     ✓        
```

---

### Voice: `v135.wav`
> **Ground Truth Reference**:
> *Yes, perfectly balanced meal ነው የወሰድኩት፤ lunch ላይ injera with lentils and spinach በልቻለሁ፣ then afternoon ላይ boiled egg እና fruit snack ወስጃለሁ።*

#### Sahara
- **Latency**: 4.23s | **Ref Words**: 23 | **Errors**: 12 (S: 7, D: 5, I: 0)
- **WER**: **52.2%** | **Word Accuracy**: **47.8%** | **CER**: 36.6%

```text
REF : yes   perfectly   balanced   meal   ነው   የወሰድኩት   lunch   ላይ   injera   with   lentils   and   spinach   በልቻለሁ   then   afternoon   ላይ   boiled   egg   እና   fruit   snack   ወስጃለሁ  
HYP : yes   perfectly   balanced   mill   ነው   የወሰድኩት   lanch   ላይ   ---      ---    ---       ---   እንጀራች     በልቻለሁ   then   afternoo    ላይ   boild    ech   እና   fruit   ---     naco   
EVAL: ✓     ✓           ✓          SUB    ✓    ✓        SUB     ✓    DEL      DEL    DEL       DEL   SUB       ✓       ✓      SUB         ✓    SUB      SUB   ✓    ✓       DEL     SUB    
```

#### Addis Ai
- **Latency**: 5.53s | **Ref Words**: 23 | **Errors**: 16 (S: 16, D: 0, I: 0)
- **WER**: **69.6%** | **Word Accuracy**: **30.4%** | **CER**: 78.6%

```text
REF : yes   perfectly   balanced   meal   ነው   የወሰድኩት   lunch   ላይ   injera   with   lentils   and   spinach   በልቻለሁ   then   afternoon   ላይ   boiled   egg   እና   fruit   snack   ወስጃለሁ  
HYP : የስ    ፐርፌክትሊ      ባላንስድ      ሚል     ነው   የወሰድኩት   ላንቺ     ላይ   እንጀራ     ዊድ     ሌንቴልስ     ኤንድ   ስፒናች      በልቻለሁ   ዘን     አፍተርኑ       ላይ   ቦይልድ     ኤግ    እና   ፍሩት     ስናክ     ወስጃለሁ  
EVAL: SUB   SUB         SUB        SUB    ✓    ✓        SUB     ✓    SUB      SUB    SUB       SUB   SUB       ✓       SUB    SUB         ✓    SUB      SUB   ✓    SUB     SUB     ✓      
```

#### Gemini
- **Latency**: 4.29s | **Ref Words**: 23 | **Errors**: 5 (S: 4, D: 1, I: 0)
- **WER**: **21.7%** | **Word Accuracy**: **78.3%** | **CER**: 18.8%

```text
REF : yes   perfectly   balanced   meal   ነው   የወሰድኩት   lunch   ላይ   injera   with   lentils   and   spinach   በልቻለሁ   then   afternoon   ላይ   boiled   egg   እና   fruit   snack   ወስጃለሁ    
HYP : yes   perfectly   balanced   meal   ነው   ሰርኩት     ላንች     ላይ   እንጀራ     with   lentils   and   spinach   በልቻለሁ   then   afternoon   ላይ   boiled   egg   እና   fruit   ---     እናኮስጃለው  
EVAL: ✓     ✓           ✓          ✓      ✓    SUB      SUB     ✓    SUB      ✓      ✓         ✓     ✓         ✓       ✓      ✓           ✓    ✓        ✓     ✓    ✓       DEL     SUB      
```

---
