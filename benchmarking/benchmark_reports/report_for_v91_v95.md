# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v91_v95_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:51:45 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 60 | 14 | 10 | 4 | 0 | **23.3%** | **76.7%** | 16.6% | 3.60s |
| **Addis Ai** | 60 | 42 | 40 | 2 | 0 | **70.0%** | **30.0%** | 73.1% | 3.85s |
| **Gemini** | 60 | 27 | 21 | 4 | 2 | **45.0%** | **55.0%** | 39.5% | 3.65s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v91.wav`
> **Ground Truth Reference**:
> *No, actually everything is super smooth; ምንም የሚያሰጋ pain አልተሰማኝም።*

#### Sahara
- **Latency**: 4.11s | **Ref Words**: 10 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 7.7%

```text
REF : no   actually   everything   is   super   smooth      ምንም   የሚያሰጋ   pain   አልተሰማኝም  
HYP : no   actually   everything   is   ---     supprsmos   ምንም   የሚያሰጋ   pain   አልተሰማኝም  
EVAL: ✓    ✓          ✓            ✓    DEL     SUB         ✓     ✓       ✓      ✓        
```

#### Addis Ai
- **Latency**: 4.3s | **Ref Words**: 10 | **Errors**: 7 (S: 7, D: 0, I: 0)
- **WER**: **70.0%** | **Word Accuracy**: **30.0%** | **CER**: 71.2%

```text
REF : no    actually   everything   is    super   smooth   ምንም   የሚያሰጋ   pain   አልተሰማኝም  
HYP : ኖ     አክችዋሊ      ኤቭሪቲንግ       ኢዝ    ሱፐር     ስሞዝ      ምንም   የሚያሰጋ   ፔይን    አልተሰማኝም  
EVAL: SUB   SUB        SUB          SUB   SUB     SUB      ✓     ✓       SUB    ✓        
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 10 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **40.0%** | **Word Accuracy**: **60.0%** | **CER**: 42.3%

```text
REF : no    actually   everything   is    super   smooth   ምንም   የሚያሰጋ   pain   አልተሰማኝም  
HYP : ኖ     አክቹዋሊ      ኤቭሪቲንግ       ኢዝ    super   smooth   ምንም   የሚያሰጋ   pain   አልተሰማኝም  
EVAL: SUB   SUB        SUB          SUB   ✓       ✓        ✓     ✓       ✓      ✓        
```

---

### Voice: `v92.wav`
> **Ground Truth Reference**:
> *I checked my BP ጠዋት ላይ፣ perfectly normal ነው፤ headache ወይም dizziness የለኝም።*

#### Sahara
- **Latency**: 3.53s | **Ref Words**: 13 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 29.3%

```text
REF : i    checked   my   bp   ጠዋት       ላይ     perfectly   normal   ነው    headache   ወይም    dizziness   የለኝም  
HYP : i    checked   my   bp   thought   like   perfectly   normal   ---   headache   wemb   dizziness   የለኝም  
EVAL: ✓    ✓         ✓    ✓    SUB       SUB    ✓           ✓        DEL   ✓          SUB    ✓           ✓     
```

#### Addis Ai
- **Latency**: 3.58s | **Ref Words**: 13 | **Errors**: 8 (S: 8, D: 0, I: 0)
- **WER**: **61.5%** | **Word Accuracy**: **38.5%** | **CER**: 75.9%

```text
REF : i     checked   my    bp    ጠዋት   ላይ   perfectly   normal   ነው   headache   ወይም   dizziness   የለኝም  
HYP : አይ    ቼክድ       ማይ    ቢፒ    ጠዋት   ላይ   ፐርፌክትሊ      ኖርማል     ነው   ሄዲክ        ወይም   ዲዚነስ        የለኝም  
EVAL: SUB   SUB       SUB   SUB   ✓     ✓    SUB         SUB      ✓    SUB        ✓     SUB         ✓     
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 13 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 15.5%

```text
REF : i    checked   my   bp   ጠዋት     ላይ     perfectly   normal   ነው   headache   ወይም   dizziness   የለኝም  
HYP : i    checked   my   bp   start   line   perfectly   normal   ነው   headache   ወይም   dizziness   የለኝም  
EVAL: ✓    ✓         ✓    ✓    SUB     SUB    ✓           ✓        ✓    ✓          ✓     ✓           ✓     
```

---

### Voice: `v93.wav`
> **Ground Truth Reference**:
> *ኧረ none of that, Bleeding የለም፣ fluid leakage የለም፤ today I feel energetic.*

#### Sahara
- **Latency**: 3.22s | **Ref Words**: 13 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **23.1%** | **Word Accuracy**: **76.9%** | **CER**: 15.8%

```text
REF : ኧረ    none   of   that   bleeding   የለም   fluid   leakage     የለም   today   i    feel   energetic  
HYP : ---   none   of   that   bleeding   የለም   fluid   leakaging   የለም   today   i    feel   energy     
EVAL: DEL   ✓      ✓    ✓      ✓          ✓     ✓       SUB         ✓     ✓       ✓    ✓      SUB        
```

#### Addis Ai
- **Latency**: 3.69s | **Ref Words**: 13 | **Errors**: 11 (S: 11, D: 0, I: 0)
- **WER**: **84.6%** | **Word Accuracy**: **15.4%** | **CER**: 87.7%

```text
REF : ኧረ    none   of    that   bleeding   የለም   fluid   leakage   የለም   today   i     feel   energetic  
HYP : አረ    ነን     ኦፍ    ዛት     ብሊዲንግ      የለም   ፍሎድ     ሊኬጅም      የለም   ቱዴይ     አይ    ፊል     ኢነርጂቲክ     
EVAL: SUB   SUB    SUB   SUB    SUB        ✓     SUB     SUB       ✓     SUB     SUB   SUB    SUB        
```

#### Gemini
- **Latency**: 3.48s | **Ref Words**: 13 | **Errors**: 11 (S: 8, D: 3, I: 0)
- **WER**: **84.6%** | **Word Accuracy**: **15.4%** | **CER**: 89.5%

```text
REF : ኧረ    none   of    that     bleeding   የለም   fluid   leakage   የለም   today   i     feel   energetic  
HYP : ---   ---    ---   እነነፍሳት   ብሊዲንግ      የለም   ፍሉድ     ሌኬጅ       የለም   ቱደይ     አይ    ፊል     ኢነርጀቲክ     
EVAL: DEL   DEL    DEL   SUB      SUB        ✓     SUB     SUB       ✓     SUB     SUB   SUB    SUB        
```

---

### Voice: `v94.wav`
> **Ground Truth Reference**:
> *Not really, የጠቀስካቸው red flags ምንም አልታዩብኝም፤ completely safe ነኝ።*

#### Sahara
- **Latency**: 3.63s | **Ref Words**: 10 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 10.0%

```text
REF : not   really   የጠቀስካቸው   red   flags   ምንም   አልታዩብኝም   completely   safe   ነኝ  
HYP : not   really   የጠቀስካቸው   ---   redux   ምንም   አልታዩብኝም   completely   safe   ነኝ  
EVAL: ✓     ✓        ✓         DEL   SUB     ✓     ✓         ✓            ✓      ✓   
```

#### Addis Ai
- **Latency**: 3.89s | **Ref Words**: 10 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **60.0%** | **Word Accuracy**: **40.0%** | **CER**: 62.0%

```text
REF : not   really   የጠቀስካቸው   red   flags   ምንም   አልታዩብኝም   completely   safe   ነኝ  
HYP : ኖት    ሪሊ       የጠቀስካቸው   ሬድ    ፍላክስ    ምንም   አልታዩብኝም   ኮምፕሊትሊ       ሴፍ     ነኝ  
EVAL: SUB   SUB      ✓         SUB   SUB     ✓     ✓         SUB          SUB    ✓   
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 10 | **Errors**: 5 (S: 4, D: 0, I: 1)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 34.0%

```text
REF : ---   not   really   የጠቀስካቸው   red   flags   ምንም   አልታዩብኝም   completely   safe   ነኝ  
HYP : ኖት    ቱ     ሪሊ       የጠቀስካቸው   ሬድ    ፍላግስ    ምንም   አልታዩብኝም   completely   safe   ነኝ  
EVAL: INS   SUB   SUB      ✓         SUB   SUB     ✓     ✓         ✓            ✓      ✓   
```

---

### Voice: `v95.wav`
> **Ground Truth Reference**:
> *The baby is active, kick ሲያረግ በደንብ ይሰማኛል፤ so no worries, ምንም sign የለኝም።*

#### Sahara
- **Latency**: 3.53s | **Ref Words**: 14 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **21.4%** | **Word Accuracy**: **78.6%** | **CER**: 18.5%

```text
REF : the   baby   is   active   kick   ሲያረግ    በደንብ   ይሰማኛል   so   no   worries   ምንም   sign   የለኝም  
HYP : so    baby   is   active   kick   ሲያደርግ   በደንብ   ይሰማኛል   so   no   voice     ምንም   sign   የለኝም  
EVAL: SUB   ✓      ✓    ✓        ✓      SUB     ✓      ✓       ✓    ✓    SUB       ✓     ✓      ✓     
```

#### Addis Ai
- **Latency**: 3.79s | **Ref Words**: 14 | **Errors**: 10 (S: 8, D: 2, I: 0)
- **WER**: **71.4%** | **Word Accuracy**: **28.6%** | **CER**: 66.7%

```text
REF : the   baby   is    active   kick   ሲያረግ    በደንብ   ይሰማኛል   so    no    worries   ምንም   sign   የለኝም  
HYP : ---   ---    በቤቢ   አክቲቭ     ኪክ     ሲያደርግ   በደንብ   ይሰማኛል   ሶ     ኖ     ወሪስ       ምንም   ሳይን    የለኝም  
EVAL: DEL   DEL    SUB   SUB      SUB    SUB     ✓      ✓       SUB   SUB   SUB       ✓     SUB    ✓     
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 14 | **Errors**: 5 (S: 3, D: 1, I: 1)
- **WER**: **35.7%** | **Word Accuracy**: **64.3%** | **CER**: 14.8%

```text
REF : the   baby   is      active   kick   ---   ሲያረግ   በደንብ   ይሰማኛል   so   no   worries   ምንም   sign   የለኝም  
HYP : ---   so     babys   active   kick   سی    አርግ    በደንብ   ይሰማኛል   so   no   worries   ምንም   sign   የለኝም  
EVAL: DEL   SUB    SUB     ✓        ✓      INS   SUB    ✓      ✓       ✓    ✓    ✓         ✓     ✓      ✓     
```

---
