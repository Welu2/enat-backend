# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v136_v139_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 4
- **Evaluation Date**: 2026-09-08 09:56:11 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 64 | 30 | 20 | 10 | 0 | **46.9%** | **53.1%** | 28.3% | 4.16s |
| **Addis Ai** | 64 | 40 | 34 | 0 | 6 | **62.5%** | **37.5%** | 64.3% | 4.30s |
| **Gemini** | 64 | 49 | 41 | 4 | 4 | **76.6%** | **23.4%** | 70.6% | 4.10s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v136.wav`
> **Ground Truth Reference**:
> *No, actually appetite የለኝም፤ just morning ላይ toast እና tea ብቻ ነው የቀመስኩት, extra meal ምንም አልወሰድኩም።*

#### Sahara
- **Latency**: 4.22s | **Ref Words**: 17 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **35.3%** | **Word Accuracy**: **64.7%** | **CER**: 17.6%

```text
REF : no   actually   appetite   የለኝም   just   morning   ላይ     toast   እና   tea   ብቻ   ነው    የቀመስኩት   extra   meal   ምንም   አልወሰድኩም  
HYP : no   actually   apptiget   የለኝም   just   morning   like   tost    እና   t     ብቻ   እኔ    ቀመስኩት    extra   meal   ምንም   አልወሰድኩም  
EVAL: ✓    ✓          SUB        ✓      ✓      ✓         SUB    SUB     ✓    SUB   ✓    SUB   SUB      ✓       ✓      ✓     ✓        
```

#### Addis Ai
- **Latency**: 4.71s | **Ref Words**: 17 | **Errors**: 9 (S: 9, D: 0, I: 0)
- **WER**: **52.9%** | **Word Accuracy**: **47.1%** | **CER**: 62.2%

```text
REF : no    actually   appetite   የለኝም   just   morning   ላይ   toast   እና   tea   ብቻ   ነው   የቀመስኩት   extra   meal   ምንም   አልወሰድኩም  
HYP : ኖ     አክችዋሊ      አፕታይት      የለኝም   ጀስት    ሞርኒንግ     ላይ   ቶስት     እና   ቲ     ብቻ   ነው   የቀመስኩት   ኤክስትራ   ሚል     ምንም   አልወሰድኩም  
EVAL: SUB   SUB        SUB        ✓      SUB    SUB       ✓    SUB     ✓    SUB   ✓    ✓    ✓        SUB     SUB    ✓     ✓        
```

#### Gemini
- **Latency**: 4.54s | **Ref Words**: 17 | **Errors**: 12 (S: 9, D: 3, I: 0)
- **WER**: **70.6%** | **Word Accuracy**: **29.4%** | **CER**: 66.2%

```text
REF : no    actually   appetite   የለኝም    just      morning   ላይ   toast   እና   tea   ብቻ   ነው   የቀመስኩት   extra         meal   ምንም   አልወሰድኩም  
HYP : ---   ---        ኖ          አፕታይት   የለኝምጀስት   ሞርኒንግ     ላይ   ቶስት     እና   ቲ     ብቻ   ነው   ---      የቀመሥኩትኤክስትራ   ሚል     ምንም   ማልወስድኩም  
EVAL: DEL   DEL        SUB        SUB     SUB       SUB       ✓    SUB     ✓    SUB   ✓    ✓    DEL      SUB           SUB    ✓     SUB      
```

---

### Voice: `v137.wav`
> **Ground Truth Reference**:
> *አዎ extra snack ወስጃለሁ፤ avocado smoothie ከወተት ጋር ጠጣሁ፣ lunch ላይ ደግሞ chicken stew በልቻለሁ።*

#### Sahara
- **Latency**: 3.8s | **Ref Words**: 15 | **Errors**: 6 (S: 5, D: 1, I: 0)
- **WER**: **40.0%** | **Word Accuracy**: **60.0%** | **CER**: 22.4%

```text
REF : አዎ   extra   snack        ወስጃለሁ   avocado    smoothie   ከወተት   ጋር   ጠጣሁ   lunch   ላይ   ደግሞ   chicken   stew         በልቻለሁ  
HYP : አዎ   ---     extrasnack   ወስጃለሁ   avocados   music      ከወተት   ጋር   ጠጣሁ   lunch   ላይ   ደግሞ   እቺ        constitute   በልቻለሁ  
EVAL: ✓    DEL     SUB          ✓       SUB        SUB        ✓      ✓    ✓     ✓       ✓    ✓     SUB       SUB          ✓      
```

#### Addis Ai
- **Latency**: 4.71s | **Ref Words**: 15 | **Errors**: 11 (S: 7, D: 0, I: 4)
- **WER**: **73.3%** | **Word Accuracy**: **26.7%** | **CER**: 65.7%

```text
REF : አዎ   extra   snack   ወስጃለሁ   ---   ---    ---    ---    avocado   smoothie   ከወተት   ጋር   ጠጣሁ   lunch   ላይ   ደግሞ   chicken   stew   በልቻለሁ  
HYP : አዎ   ኤክስትራ   ስናክ     ወስጃለሁ   አ     0xe1   0x89   0xae   ካዶ        ስሙዚ        ከወተት   ጋር   ጠጣሁ   ላንች     ላይ   ደግሞ   ቺከን       ስቲው    በልቻለሁ  
EVAL: ✓    SUB     SUB     ✓       INS   INS    INS    INS    SUB       SUB        ✓      ✓    ✓     SUB     ✓    ✓     SUB       SUB    ✓      
```

#### Gemini
- **Latency**: 4.3s | **Ref Words**: 15 | **Errors**: 12 (S: 9, D: 0, I: 3)
- **WER**: **80.0%** | **Word Accuracy**: **20.0%** | **CER**: 64.2%

```text
REF : አዎ    extra   ---      snack   ወስጃለሁ   avocado   smoothie   ከወተት   ጋር   ---    ጠጣሁ     lunch   ላይ   ደግሞ   chicken   stew   ---    በልቻለሁ  
HYP : או    extra   snacks   መብላት    ይቻለኝ    አቮካዶ      ስሙዚ        ከቶስት   ጋር   መብላት   እችላለሁ   ላንች     ላይ   ደግሞ   chicken   stew   መብላት   እችላለሁ  
EVAL: SUB   ✓       INS      SUB     SUB     SUB       SUB        SUB    ✓    INS    SUB     SUB     ✓    ✓     ✓         ✓      INS    SUB    
```

---

### Voice: `v138.wav`
> **Ground Truth Reference**:
> *Heavy carbs ብቻ ነው የበላሁት፤ rice እና pasta, fruit እና vegetable አላገኘሁም፣ so balanced አይደለም።*

#### Sahara
- **Latency**: 3.62s | **Ref Words**: 15 | **Errors**: 11 (S: 5, D: 6, I: 0)
- **WER**: **73.3%** | **Word Accuracy**: **26.7%** | **CER**: 50.7%

```text
REF : heavy   carbs   ብቻ    ነው    የበላሁት    rice    እና   pasta   fruit   እና      vegetable   አላገኘሁም   so   balanced   አይደለም  
HYP : ---     ---     ---   ---   pastor   frout   እና   ---     ---     beach   table       አላገኘውም   so   balanced   አይደለም  
EVAL: DEL     DEL     DEL   DEL   SUB      SUB     ✓    DEL     DEL     SUB     SUB         SUB      ✓    ✓          ✓      
```

#### Addis Ai
- **Latency**: 4.27s | **Ref Words**: 15 | **Errors**: 10 (S: 8, D: 0, I: 2)
- **WER**: **66.7%** | **Word Accuracy**: **33.3%** | **CER**: 64.2%

```text
REF : ---   heavy   carbs   ብቻ   ነው   የበላሁት   rice   እና   pasta   fruit   እና   ---   vegetable   አላገኘሁም   so    balanced   አይደለም  
HYP : ይሄ    እዚህ     ካርብስ    ብቻ   ነው   የበላሁት   ራይስ    እና   ፓስታ     ፉርት     እና   ቤጅ    ቴብል         አላገኘሁም   ሶ     ባላንስድ      አይደለም  
EVAL: INS   SUB     SUB     ✓    ✓    ✓       SUB    ✓    SUB     SUB     ✓    INS   SUB         ✓        SUB   SUB        ✓      
```

#### Gemini
- **Latency**: 3.68s | **Ref Words**: 15 | **Errors**: 15 (S: 13, D: 1, I: 1)
- **WER**: **100.0%** | **Word Accuracy**: **0.0%** | **CER**: 88.1%

```text
REF : heavy   carbs   ብቻ      ነው    የበላሁት     rice   እና   ---   pasta   fruit   እና    vegetable   አላገኘሁም   so    balanced   አይደለም  
HYP : ---     ሄዚ      ካርብስት   ቻን    ivelout   አራይስ   እና   ፓስታ   ፍሩትና    ቢጂቴብል   እዚህ   ላይ          አገኘን     ሶ     ባላንስድ      አይደል   
EVAL: DEL     SUB     SUB     SUB   SUB       SUB    ✓    INS   SUB     SUB     SUB   SUB         SUB      SUB   SUB        SUB    
```

---

### Voice: `v139.wav`
> **Ground Truth Reference**:
> *Iron እና vitamin እንዲኖረው ብዬ orange juice ጠጣሁ፤ but severe nausea ስላለኝ heavy extra food መብላት አልቻልኩም።*

#### Sahara
- **Latency**: 4.98s | **Ref Words**: 17 | **Errors**: 7 (S: 4, D: 3, I: 0)
- **WER**: **41.2%** | **Word Accuracy**: **58.8%** | **CER**: 24.4%

```text
REF : iron   እና   vitamin   እንዲኖረው   ብዬ   orange   juice   ጠጣሁ       but     severe   nausea   ስላለኝ   heavy   extra   food   መብላት   አልቻልኩም  
HYP : iran   እና   vitamin   እንዲኖረው   ብዬ   ---      ---     oranges   ጠጣሁበት   severe   nausea   ስላለኝ   ---     የሄስትራ   food   መብላት   አልቻልኩም  
EVAL: SUB    ✓    ✓         ✓        ✓    DEL      DEL     SUB       SUB     ✓        ✓        ✓      DEL     SUB     ✓      ✓      ✓       
```

#### Addis Ai
- **Latency**: 3.53s | **Ref Words**: 17 | **Errors**: 10 (S: 10, D: 0, I: 0)
- **WER**: **58.8%** | **Word Accuracy**: **41.2%** | **CER**: 65.4%

```text
REF : iron   እና   vitamin   እንዲኖረው   ብዬ   orange   juice   ጠጣሁ   but   severe   nausea   ስላለኝ   heavy   extra   food   መብላት   አልቻልኩም  
HYP : አይረን   እና   ቪታሚን      እንዲኖረው   ብዬ   ኦሬንጅ     ውስጥ     ጠጣሁ   በት    ሰቪር      ናሽያ      ስላለኝ   ሄቪ      ኤክስትራ   ፉድ     መብላት   አልቻልኩም  
EVAL: SUB    ✓    SUB       ✓        ✓    SUB      SUB     ✓     SUB   SUB      SUB      ✓      SUB     SUB     SUB    ✓      ✓       
```

#### Gemini
- **Latency**: 3.87s | **Ref Words**: 17 | **Errors**: 10 (S: 10, D: 0, I: 0)
- **WER**: **58.8%** | **Word Accuracy**: **41.2%** | **CER**: 65.4%

```text
REF : iron   እና   vitamin   እንዲኖረው   ብዬ   orange   juice   ጠጣሁ   but   severe   nausea   ስላለኝ   heavy   extra   food   መብላት   አልቻልኩም  
HYP : አይረን   እና   ቪታሚን      እንዲኖረው   ብዬ   ኦሬንጅ     جوس     ጠጣሁ   በት    ሴቨር      ናውሻ      ስላለኝ   ሄቪ      ኤክስትራ   ፉድ     መብላት   አልቻልኩም  
EVAL: SUB    ✓    SUB       ✓        ✓    SUB      SUB     ✓     SUB   SUB      SUB      ✓      SUB     SUB     SUB    ✓      ✓       
```

---
