# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v81_v85_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:51:18 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 71 | 16 | 11 | 4 | 1 | **22.5%** | **77.5%** | 10.8% | 3.52s |
| **Addis Ai** | 71 | 51 | 48 | 0 | 3 | **71.8%** | **28.2%** | 74.1% | 3.97s |
| **Gemini** | 71 | 18 | 18 | 0 | 0 | **25.4%** | **74.6%** | 16.2% | 3.62s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v81.wav`
> **Ground Truth Reference**:
> *I have severe shortness of breath፤ lie down ሳደርግ chestቴ ላይ heavy pressure ይሰማኛል።*

#### Sahara
- **Latency**: 2.88s | **Ref Words**: 14 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **28.6%** | **Word Accuracy**: **71.4%** | **CER**: 20.0%

```text
REF : i    have   severe   shortness   of   breath   lie   down   ሳደርግ   chestቴ   ላይ     heavy   pressure   ይሰማኛል  
HYP : i    have   severe   shortness   of   breath   lie   down   ---    sade     jest   taily   pressure   ይሰማኛል  
EVAL: ✓    ✓      ✓        ✓           ✓    ✓        ✓     ✓      DEL    SUB      SUB    SUB     ✓          ✓      
```

#### Addis Ai
- **Latency**: 4.4s | **Ref Words**: 14 | **Errors**: 11 (S: 11, D: 0, I: 0)
- **WER**: **78.6%** | **Word Accuracy**: **21.4%** | **CER**: 81.5%

```text
REF : i     have   severe   shortness   of    breath   lie   down   ሳደርግ   chestቴ   ላይ   heavy   pressure   ይሰማኛል  
HYP : አይ    ሃቭ     ሰቪር      ሾርትነስ       ኦፍ    ብሬት      ላይ    ዳውን    ሳደርግ   ቸስቴ      ላይ   ሄቪ      ፕሬዘር       ይሰማኛል  
EVAL: SUB   SUB    SUB      SUB         SUB   SUB      SUB   SUB    ✓      SUB      ✓    SUB     SUB        ✓      
```

#### Gemini
- **Latency**: 3.58s | **Ref Words**: 14 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **42.9%** | **Word Accuracy**: **57.1%** | **CER**: 40.0%

```text
REF : i    have   severe   shortness   of   breath   lie   down   ሳደርግ    chestቴ   ላይ   heavy   pressure   ይሰማኛል  
HYP : i    have   severe   shortness   of   breath   ላይ    ዳውን    ስታደርግ   ቼስቴ      ላይ   ሄቪ      ፕሬዠር       ይሰማኛል  
EVAL: ✓    ✓      ✓        ✓           ✓    ✓        SUB   SUB    SUB     SUB      ✓    SUB     SUB        ✓      
```

---

### Voice: `v82.wav`
> **Ground Truth Reference**:
> *እጆቼና ፊቴ completely swollen ሆነዋል፤ my wedding ring ራሱ ማውለቅ አልቻልኩም፣ ዓይኖቼም puffy ናቸው።*

#### Sahara
- **Latency**: 3.94s | **Ref Words**: 14 | **Errors**: 3 (S: 2, D: 0, I: 1)
- **WER**: **21.4%** | **Word Accuracy**: **78.6%** | **CER**: 3.1%

```text
REF : ---   እጆቼና   ፊቴ   completely   swollen   ሆነዋል   my   wedding   ring   ራሱ   ማውለቅ   አልቻልኩም   ዓይኖቼም   puffy   ናቸው  
HYP : እጆቼ   እና     ፊቴ   completely   swollen   ሆነዋል   my   wedding   ring   ራሱ   ማውለቅ   አልቻልኩም   አይኖቼም   puffy   ናቸው  
EVAL: INS   SUB    ✓    ✓            ✓         ✓      ✓    ✓         ✓      ✓    ✓      ✓        SUB     ✓       ✓    
```

#### Addis Ai
- **Latency**: 4.37s | **Ref Words**: 14 | **Errors**: 7 (S: 7, D: 0, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 55.4%

```text
REF : እጆቼና   ፊቴ   completely   swollen   ሆነዋል   my    wedding   ring   ራሱ   ማውለቅ   አልቻልኩም   ዓይኖቼም   puffy   ናቸው  
HYP : እጆቼና   ፊቴ   ኮምፕሊትሊ       ስዋልን      ሆነዋል   ማይ    ዌዲንግ      ሪንግ    ራሱ   ማውለቅ   አልቻልኩም   አይኖቼም   ፐፊ      ናቸው  
EVAL: ✓      ✓    SUB          SUB       ✓      SUB   SUB       SUB    ✓    ✓      ✓        SUB     SUB     ✓    
```

#### Gemini
- **Latency**: 4.03s | **Ref Words**: 14 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **21.4%** | **Word Accuracy**: **78.6%** | **CER**: 9.2%

```text
REF : እጆቼና   ፊቴ   completely   swollen   ሆነዋል   my    wedding   ring   ራሱ   ማውለቅ   አልቻልኩም   ዓይኖቼም   puffy   ናቸው  
HYP : እጆቼና   ፊቴ   completely   swollen   ሆኗል    ማይ    wedding   ring   ራሱ   ማውለቅ   አልቻልኩም   ይሄኖቼም   puffy   ናቸው  
EVAL: ✓      ✓    ✓            ✓         SUB    SUB   ✓         ✓      ✓    ✓      ✓        SUB     ✓       ✓    
```

---

### Voice: `v83.wav`
> **Ground Truth Reference**:
> *Frequent vomiting አለብኝ፤ even water እንኳን keep ማድረግ አልቻልኩም፣ I feel very dehydrated.*

#### Sahara
- **Latency**: 3.02s | **Ref Words**: 13 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **7.7%** | **Word Accuracy**: **92.3%** | **CER**: 3.0%

```text
REF : frequent   vomiting   አለብኝ   even   water   እንኳን   keep   ማድረግ   አልቻልኩም   i    feel   very   dehydrated  
HYP : frequent   vomiting   አለብኝ   even   water   እንኳን   keep   ማድረግ   አልቻልኩም   i    feel   very   hydrated    
EVAL: ✓          ✓          ✓      ✓      ✓       ✓      ✓      ✓      ✓        ✓    ✓      ✓      SUB         
```

#### Addis Ai
- **Latency**: 3.69s | **Ref Words**: 13 | **Errors**: 12 (S: 9, D: 0, I: 3)
- **WER**: **92.3%** | **Word Accuracy**: **7.7%** | **CER**: 80.3%

```text
REF : ---      ---    ---    frequent   vomiting   አለብኝ   even   water   እንኳን   keep   ማድረግ   አልቻልኩም   i     feel   very   dehydrated  
HYP : ፍሪኩዌንት   0xe1   0x89   0xae       ሚቲንግ       አለብኝ   ኢቭን    ዋተር     እንኳን   ኪፕ     ማድረግ   አልቻልኩም   አይ    ፊል     ቬሪ     ሃይድሬትድ      
EVAL: INS      INS    INS    SUB        SUB        ✓      SUB    SUB     ✓      SUB    ✓      ✓        SUB   SUB    SUB    SUB         
```

#### Gemini
- **Latency**: 3.48s | **Ref Words**: 13 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 22.7%

```text
REF : frequent   vomiting   አለብኝ   even   water   እንኳን   keep   ማድረግ   አልቻልኩም   i    feel   very   dehydrated  
HYP : frequent   vomiting   አለብኝ   ኢቨን    ዋተር     እንኳን   ኪፕ     ማድረግ   አልቻልኩም   i    feel   very   hydrated    
EVAL: ✓          ✓          ✓      SUB    SUB     ✓      SUB    ✓      ✓        ✓    ✓      ✓      SUB         
```

---

### Voice: `v84.wav`
> **Ground Truth Reference**:
> *Yeah, terrible migraine-like headache አለብኝ፤ plus visionዬ በጣም ይዥጎረጎራል እናም ፊቴ ላይ strong swelling አለብኝ።*

#### Sahara
- **Latency**: 4.45s | **Ref Words**: 16 | **Errors**: 5 (S: 3, D: 2, I: 0)
- **WER**: **31.2%** | **Word Accuracy**: **68.8%** | **CER**: 14.6%

```text
REF : yeah   terrible   migraine   like   headache   አለብኝ   plus   visionዬ   በጣም   ይዥጎረጎራል   እናም   ፊቴ    ላይ   strong   swelling   አለብኝ  
HYP : yeah   terrible   migraine   like   headache   አለብኝ   clus   vision    በጣም   ---       ---   ይዥ    ላይ   strong   swelling   አለብኝ  
EVAL: ✓      ✓          ✓          ✓      ✓          ✓      SUB    SUB       ✓     DEL       DEL   SUB   ✓    ✓        ✓          ✓     
```

#### Addis Ai
- **Latency**: 3.82s | **Ref Words**: 16 | **Errors**: 10 (S: 10, D: 0, I: 0)
- **WER**: **62.5%** | **Word Accuracy**: **37.5%** | **CER**: 70.7%

```text
REF : yeah   terrible   migraine   like   headache   አለብኝ   plus   visionዬ   በጣም   ይዥጎረጎራል   እናም   ፊቴ   ላይ   strong   swelling   አለብኝ  
HYP : ያ      ቴሬቨር       ማይግሪን      ላይክ    ሄድክ        አለብኝ   ክላስ    ቪዥኔ       በጣም   ይጎረጎራል    እናም   ፊቴ   ላይ   ስትሮንግ    ስዌሊንግ      አለብኝ  
EVAL: SUB    SUB        SUB        SUB    SUB        ✓      SUB    SUB       ✓     SUB       ✓     ✓    ✓    SUB      SUB        ✓     
```

#### Gemini
- **Latency**: 3.55s | **Ref Words**: 16 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **18.8%** | **Word Accuracy**: **81.2%** | **CER**: 7.3%

```text
REF : yeah   terrible   migraine   like   headache   አለብኝ   plus   visionዬ   በጣም   ይዥጎረጎራል   እናም   ፊቴ   ላይ   strong   swelling   አለብኝ  
HYP : ያ      terrible   migraine   like   headache   አለብኝ   plus   vision    በጣም   ይጎረጎራል    እናም   ፊቴ   ላይ   strong   swelling   አለብኝ  
EVAL: SUB    ✓          ✓          ✓      ✓          ✓      ✓      SUB       ✓     SUB       ✓     ✓    ✓    ✓        ✓          ✓     
```

---

### Voice: `v85.wav`
> **Ground Truth Reference**:
> *Sharp abdominal pain አለኝ፤ simultaneously ደግሞ bright red blood እየፈሰሰኝ ነው, please advise me.*

#### Sahara
- **Latency**: 3.32s | **Ref Words**: 14 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **21.4%** | **Word Accuracy**: **78.6%** | **CER**: 12.2%

```text
REF : sharp   abdominal   pain   አለኝ   simultaneously   ደግሞ   bright   red    blood   እየፈሰሰኝ   ነው   please   advise   me  
HYP : sharp   abdominal   pain   ---   አለኝታniously      ደግሞ   bright   read   blood   እየፈሰሰኝ   ነው   please   advise   me  
EVAL: ✓       ✓           ✓      DEL   SUB              ✓     ✓        SUB    ✓       ✓        ✓    ✓        ✓        ✓   
```

#### Addis Ai
- **Latency**: 3.59s | **Ref Words**: 14 | **Errors**: 11 (S: 11, D: 0, I: 0)
- **WER**: **78.6%** | **Word Accuracy**: **21.4%** | **CER**: 82.4%

```text
REF : sharp   abdominal   pain   አለኝ   simultaneously   ደግሞ   bright   red   blood   እየፈሰሰኝ   ነው   please   advise   me   
HYP : ሻርፕ     አብዶሜናል      ፔን     አለኝ   ሳይመልታኒየስሊ        ደሞ    ብራይት     ሬድ    ብለድ     እየፈሰሰኝ   ነው   ፕሊስ      አድቫይዝ    ሚ    
EVAL: SUB     SUB         SUB    ✓     SUB              SUB   SUB      SUB   SUB     ✓        ✓    SUB      SUB      SUB  
```

#### Gemini
- **Latency**: 3.48s | **Ref Words**: 14 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **14.3%** | **Word Accuracy**: **85.7%** | **CER**: 5.4%

```text
REF : sharp   abdominal   pain   አለኝ   simultaneously   ደግሞ   bright   red   blood   እየፈሰሰኝ   ነው   please   advise   me  
HYP : sharp   abdominal   pain   አለኝ   simultaneous     ደሙ    bright   red   blood   እየፈሰሰኝ   ነው   please   advise   me  
EVAL: ✓       ✓           ✓      ✓     SUB              SUB   ✓        ✓     ✓       ✓        ✓    ✓        ✓        ✓   
```

---
