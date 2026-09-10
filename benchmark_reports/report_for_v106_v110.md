# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v106_v110_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:52:16 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 72 | 23 | 19 | 4 | 0 | **31.9%** | **68.1%** | 14.9% | 4.29s |
| **Addis Ai** | 72 | 57 | 51 | 0 | 6 | **79.2%** | **20.8%** | 81.7% | 4.30s |
| **Gemini** | 72 | 27 | 25 | 2 | 0 | **37.5%** | **62.5%** | 36.3% | 4.03s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v106.wav`
> **Ground Truth Reference**:
> *Facial puffiness አለብኝ፤ my eyelids እና my fingers በጣም swell አድርገዋል፣ ቀለበቴ ራሱ በጣም እየወጠረኝ ነው።*

#### Sahara
- **Latency**: 3.65s | **Ref Words**: 16 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **37.5%** | **Word Accuracy**: **62.5%** | **CER**: 10.0%

```text
REF : facial   puffiness    አለብኝ   my   eyelids   እና   my   fingers   በጣም   swell   አድርገዋል   ቀለበቴ   ራሱ   በጣም   እየወጠረኝ   ነው  
HYP : facial   peffyiness   አለብኝ   my   eyelid    እና   my   fingers   በጣም   swill   አርገዋል    ቀለብቴ   ራሱ   በጣም   እየወጠረ    ነው  
EVAL: ✓        SUB          ✓      ✓    SUB       ✓    ✓    ✓         ✓     SUB     SUB      SUB    ✓    ✓     SUB      ✓   
```

#### Addis Ai
- **Latency**: 4.14s | **Ref Words**: 16 | **Errors**: 7 (S: 7, D: 0, I: 0)
- **WER**: **43.8%** | **Word Accuracy**: **56.2%** | **CER**: 54.3%

```text
REF : facial   puffiness   አለብኝ   my    eyelids   እና   my    fingers   በጣም   swell   አድርገዋል   ቀለበቴ   ራሱ   በጣም   እየወጠረኝ   ነው  
HYP : ፌሻል      ተፊነስ        አለብኝ   ማይ    አይሌድስ     እና   ማይ    ፊንገርስ     በጣም   ስዌል     አድርገዋል   ቀለበቴ   ራሱ   በጣም   እየወጠረኝ   ነው  
EVAL: SUB      SUB         ✓      SUB   SUB       ✓    SUB   SUB       ✓     SUB     ✓        ✓      ✓    ✓     ✓        ✓   
```

#### Gemini
- **Latency**: 3.17s | **Ref Words**: 16 | **Errors**: 8 (S: 7, D: 1, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 45.7%

```text
REF : facial   puffiness   አለብኝ   my    eyelids   እና       my    fingers   በጣም   swell     አድርገዋል   ቀለበቴ   ራሱ   በጣም   እየወጠረኝ   ነው  
HYP : facial   pain        አለብኝ   ---   ማይ        አይለድስና   ማይ    ፊንገርስ     በጣም   swollen   ይላልቀዋል   ቀለበቴ   ራሱ   በጣም   እየወጠረኝ   ነው  
EVAL: ✓        SUB         ✓      DEL   SUB       SUB      SUB   SUB       ✓     SUB       SUB      ✓      ✓    ✓     ✓        ✓   
```

---

### Voice: `v107.wav`
> **Ground Truth Reference**:
> *I can't keep fluid down, even ORS ብጠጣ ራሱ vomit ነው የማደርገው።*

#### Sahara
- **Latency**: 3.95s | **Ref Words**: 12 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **8.3%** | **Word Accuracy**: **91.7%** | **CER**: 7.0%

```text
REF : i    cant   keep   fluid   down   even   ors     ብጠጣ   ራሱ   vomit   ነው   የማደርገው  
HYP : i    cant   keep   fluid   down   even   areas   ብጠጣ   ራሱ   vomit   ነው   የማደርገው  
EVAL: ✓    ✓      ✓      ✓       ✓      ✓      SUB     ✓     ✓    ✓       ✓    ✓       
```

#### Addis Ai
- **Latency**: 4.46s | **Ref Words**: 12 | **Errors**: 12 (S: 9, D: 0, I: 3)
- **WER**: **100.0%** | **Word Accuracy**: **0.0%** | **CER**: 97.7%

```text
REF : i     cant   keep   fluid   down   even   ors   ብጠጣ   ራሱ   ---    ---    ---    vomit   ነው   የማደርገው  
HYP : አይ    ካንት    ኪፕ     ፍሉድ     ዳውን    ኢቭን    ኦርስ   ብጠጣ   ራሱ   0xe1   0x89   0xae   ሚት      ነው   ማረገው    
EVAL: SUB   SUB    SUB    SUB     SUB    SUB    SUB   ✓     ✓    INS    INS    INS    SUB     ✓    SUB     
```

#### Gemini
- **Latency**: 5.07s | **Ref Words**: 12 | **Errors**: 7 (S: 7, D: 0, I: 0)
- **WER**: **58.3%** | **Word Accuracy**: **41.7%** | **CER**: 76.7%

```text
REF : i    cant   keep   fluid   down   even   ors     ብጠጣ    ራሱ             vomit      ነው       የማደርገው  
HYP : i    cant   keep   food    down   even   water   isse   bhedhatarasu   vomiting   namare   ga      
EVAL: ✓    ✓      ✓      SUB     ✓      ✓      SUB     SUB    SUB            SUB        SUB      SUB     
```

---

### Voice: `v108.wav`
> **Ground Truth Reference**:
> *High grade fever አለኝ፤ thermometerሩ 39 አሳይቷል፣ shaking chills ይሰማኛል።*

#### Sahara
- **Latency**: 3.74s | **Ref Words**: 10 | **Errors**: 5 (S: 4, D: 1, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 29.6%

```text
REF : high   grade   fever   አለኝ   thermometerሩ   39   አሳይቷል    shaking   chills   ይሰማኛል  
HYP : high   grade   favor   አለኝ   thermo         39   አሳይተዋል   shaking   ---      chill  
EVAL: ✓      ✓       SUB     ✓     SUB            ✓    SUB      ✓         DEL      SUB    
```

#### Addis Ai
- **Latency**: 3.89s | **Ref Words**: 10 | **Errors**: 9 (S: 6, D: 0, I: 3)
- **WER**: **90.0%** | **Word Accuracy**: **10.0%** | **CER**: 77.8%

```text
REF : high   grade   fever   አለኝ   thermometerሩ   39   አሳይቷል   ---    ---    ---    shaking   chills   ይሰማኛል  
HYP : ሃይ     ግሬድ     ፌቨር     አለኝ   ቴርሞሜትሩ         39   አሳይቷል   0xe1   0x88   0xbc   ኪንግ       ቺልስ      ይሰማኛል  
EVAL: SUB    SUB     SUB     ✓     SUB            ✓    ✓       INS    INS    INS    SUB       SUB      ✓      
```

#### Gemini
- **Latency**: 4.1s | **Ref Words**: 10 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 29.6%

```text
REF : high   grade   fever   አለኝ   thermometerሩ   39   አሳይቷል    shaking   chills   ይሰማኛል  
HYP : high   grade   fever   አሊኝ   ቴርሞሜትሩ         39   አሳይቶኛል   shaking   chill    ሲሰማኛል  
EVAL: ✓      ✓       ✓       SUB   SUB            ✓    SUB      ✓         SUB      SUB    
```

---

### Voice: `v109.wav`
> **Ground Truth Reference**:
> *My headache በጣም unbearable ነው፤ visionዬ cloudy ሆኗል፣ plus my hands and face are completely swollen.*

#### Sahara
- **Latency**: 4.24s | **Ref Words**: 16 | **Errors**: 6 (S: 5, D: 1, I: 0)
- **WER**: **37.5%** | **Word Accuracy**: **62.5%** | **CER**: 16.5%

```text
REF : my   headache   በጣም   unbearable   ነው    visionዬ   cloudy   ሆኗል   plus     my   hands   and   face   are   completely   swollen  
HYP : my   headache   በጣም   unbarable    now   vision    cloudy   ---   honwol   my   hand    and   face   are   completely   swollen  
EVAL: ✓    ✓          ✓     SUB          SUB   SUB       ✓        DEL   SUB      ✓    SUB     ✓     ✓      ✓     ✓            ✓        
```

#### Addis Ai
- **Latency**: 4.51s | **Ref Words**: 16 | **Errors**: 14 (S: 14, D: 0, I: 0)
- **WER**: **87.5%** | **Word Accuracy**: **12.5%** | **CER**: 91.1%

```text
REF : my    headache   በጣም   unbearable   ነው   visionዬ   cloudy   ሆኗል   plus   my    hands   and   face   are   completely   swollen  
HYP : ማይ    ሂዲክ        በጣም   አንበርብል       ነው   ቪዥኒ       ክላውዲ     ሆንል   ፕላስ    ማይ    ሃንድስ    ኤንድ   ፋስ     አር    ኮምፕሊትሊ       ስዋርል     
EVAL: SUB   SUB        ✓     SUB          ✓    SUB       SUB      SUB   SUB    SUB   SUB     SUB   SUB    SUB   SUB          SUB      
```

#### Gemini
- **Latency**: 4.1s | **Ref Words**: 16 | **Errors**: 6 (S: 5, D: 1, I: 0)
- **WER**: **37.5%** | **Word Accuracy**: **62.5%** | **CER**: 46.8%

```text
REF : my    headache   በጣም   unbearable   ነው   visionዬ   cloudy   ሆኗል   plus   my   hands   and   face   are   completely   swollen  
HYP : ማይ    ሄዴክ        በጣም   አሜርብል        ነው   ቪዥኔ       ክላውዲ     ሆኗል   ---    my   hands   and   face   are   completely   swollen  
EVAL: SUB   SUB        ✓     SUB          ✓    SUB       SUB      ✓     DEL    ✓    ✓       ✓     ✓      ✓     ✓            ✓        
```

---

### Voice: `v110.wav`
> **Ground Truth Reference**:
> *Severe abdomenal pain አለኝ፤ በጣም sharp cramp ነው፣ with heavy bleeding, I think I need an emergency triage.*

#### Sahara
- **Latency**: 5.89s | **Ref Words**: 18 | **Errors**: 5 (S: 3, D: 2, I: 0)
- **WER**: **27.8%** | **Word Accuracy**: **72.2%** | **CER**: 12.2%

```text
REF : severe   abdomenal   pain   አለኝ   በጣም   sharp   cramp   ነው       with   heavy   bleeding   i    think   i    need   an   emergency   triage  
HYP : severe   abdominal   pain   አለኝ   ---   sharp   ---     cromto   with   heavy   bleeding   i    think   i    need   an   emergency   trigh   
EVAL: ✓        SUB         ✓      ✓     DEL   ✓       DEL     SUB      ✓      ✓       ✓          ✓    ✓       ✓    ✓      ✓    ✓           SUB     
```

#### Addis Ai
- **Latency**: 4.51s | **Ref Words**: 18 | **Errors**: 15 (S: 15, D: 0, I: 0)
- **WER**: **83.3%** | **Word Accuracy**: **16.7%** | **CER**: 90.2%

```text
REF : severe   abdomenal   pain   አለኝ   በጣም   sharp   cramp   ነው   with   heavy   bleeding   i     think   i     need   an    emergency   triage  
HYP : ሰቪር      አብዶሚናል      ፔን     አለኝ   በጣም   ሻርፕ     ክራምፕ    ነው   ዊዝ     ሄቪ      ብሊዲንግ      አይ    ቲንክ     አይ    ኒድ     ኤን    ኢመርጀንሲ      ትራይጅ    
EVAL: SUB      SUB         SUB    ✓     ✓     SUB     SUB     ✓    SUB    SUB     SUB        SUB   SUB     SUB   SUB    SUB   SUB         SUB     
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 18 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.6%** | **Word Accuracy**: **94.4%** | **CER**: 1.2%

```text
REF : severe   abdomenal   pain   አለኝ   በጣም   sharp   cramp   ነው   with   heavy   bleeding   i    think   i    need   an   emergency   triage  
HYP : severe   abdominal   pain   አለኝ   በጣም   sharp   cramp   ነው   with   heavy   bleeding   i    think   i    need   an   emergency   triage  
EVAL: ✓        SUB         ✓      ✓     ✓     ✓       ✓       ✓    ✓      ✓       ✓          ✓    ✓       ✓    ✓      ✓    ✓           ✓       
```

---
