# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v86_v90_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:51:33 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 71 | 20 | 10 | 10 | 0 | **28.2%** | **71.8%** | 17.5% | 3.30s |
| **Addis Ai** | 71 | 50 | 37 | 13 | 0 | **70.4%** | **29.6%** | 75.2% | 3.85s |
| **Gemini** | 71 | 34 | 31 | 1 | 2 | **47.9%** | **52.1%** | 34.3% | 4.23s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v86.wav`
> **Ground Truth Reference**:
> *Chest pain እና breathing difficulty አለብኝ፤ in addition to that ወገቤን ወጥሮ ይዞኛል I coulldn't stand.*

#### Sahara
- **Latency**: 3.35s | **Ref Words**: 16 | **Errors**: 4 (S: 1, D: 3, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 18.7%

```text
REF : chest   pain   እና   breathing   difficulty   አለብኝ   in   addition   to   that   ወገቤን   ወጥሮ   ይዞኛል   i    coulldnt   stand  
HYP : chest   pain   እና   breathing   difficulty   አለብኝ   in   addition   to   that   ---    ---   ---    i    could      stand  
EVAL: ✓       ✓      ✓    ✓           ✓            ✓      ✓    ✓          ✓    ✓      DEL    DEL   DEL    ✓    SUB        ✓      
```

#### Addis Ai
- **Latency**: 3.38s | **Ref Words**: 16 | **Errors**: 11 (S: 0, D: 11, I: 0)
- **WER**: **68.8%** | **Word Accuracy**: **31.2%** | **CER**: 77.3%

```text
REF : chest   pain   እና   breathing   difficulty   አለብኝ   in    addition   to    that   ወገቤን   ወጥሮ   ይዞኛል   i     coulldnt   stand  
HYP : ---     ---    እና   ---         ---          አለብኝ   ---   ---        ---   ---    ወገቤን   ወጥሮ   ይዞኛል   ---   ---        ---    
EVAL: DEL     DEL    ✓    DEL         DEL          ✓      DEL   DEL        DEL   DEL    ✓      ✓     ✓      DEL   DEL        DEL    
```

#### Gemini
- **Latency**: 3.55s | **Ref Words**: 16 | **Errors**: 4 (S: 3, D: 0, I: 1)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 10.7%

```text
REF : chest   pain   እና    breathing   difficulty   አለብኝ   in   addition   to   that   ---   ወገቤን   ወጥሮ   ይዞኛል   i    coulldnt   stand  
HYP : chest   pain   ነው    breathing   difficulty   አለብኝ   in   addition   to   that   ውጋቢ   ነው     ወጥሮ   ይዞኛል   i    couldnt    stand  
EVAL: ✓       ✓      SUB   ✓           ✓            ✓      ✓    ✓          ✓    ✓      INS   SUB    ✓     ✓      ✓    SUB        ✓      
```

---

### Voice: `v87.wav`
> **Ground Truth Reference**:
> *I am not sure… ፈሳሹ water leakage ይሁን normal vaginal discharge መለየት አልቻልኩም።*

#### Sahara
- **Latency**: 3.57s | **Ref Words**: 13 | **Errors**: 5 (S: 3, D: 2, I: 0)
- **WER**: **38.5%** | **Word Accuracy**: **61.5%** | **CER**: 9.8%

```text
REF : i     am    not   sure…   ፈሳሹ   water   leakage   ይሁን   normal   vaginal   discharge   መለየት         አልቻልኩም  
HYP : ---   im    not   sure    ፈሳሹ   water   leakage   ይሁን   normal   vaginal   ---         discharget   አልቻልኩም  
EVAL: DEL   SUB   ✓     SUB     ✓     ✓       ✓         ✓     ✓        ✓         DEL         SUB          ✓       
```

#### Addis Ai
- **Latency**: 4.91s | **Ref Words**: 13 | **Errors**: 9 (S: 8, D: 1, I: 0)
- **WER**: **69.2%** | **Word Accuracy**: **30.8%** | **CER**: 73.8%

```text
REF : i     am    not   sure…   ፈሳሹ   water   leakage   ይሁን   normal   vaginal   discharge   መለየት   አልቻልኩም  
HYP : ---   አም    ኖት    ሹር      ፈሳሹ   ዋተር     ሊኬጅ       ይሁን   ኖርማል     ቫጅናል      ዲስቸርጅ       መለየት   አልቻልኩም  
EVAL: DEL   SUB   SUB   SUB     ✓     SUB     SUB       ✓     SUB      SUB       SUB         ✓      ✓       
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 13 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 3.3%

```text
REF : i    am   not   sure…   ፈሳሹ   water   leakage   ይሁን   normal   vaginal   discharge   መለየት   አልቻልኩም  
HYP : i    am   not   sure    ፈሳሹ   water   leakage   ይሆን   normal   vaginal   discharge   መለየት   አልቻልኩም  
EVAL: ✓    ✓    ✓     SUB     ✓     ✓       ✓         SUB   ✓        ✓         ✓           ✓      ✓       
```

---

### Voice: `v88.wav`
> **Ground Truth Reference**:
> *ራስ ምታቱ አለ but its not that severe, ቡና ባለመጠጣቴ ይሁን another complication አላወቅኩም።*

#### Sahara
- **Latency**: 3.43s | **Ref Words**: 14 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **14.3%** | **Word Accuracy**: **85.7%** | **CER**: 12.9%

```text
REF : ራስ   ምታቱ   አለ   but   its   not   that   severe   ቡና   ባለመጠጣቴ   ይሁን   another   complication   አላወቅኩም  
HYP : ራስ   ምታቱ   አለ   but   its   not   that   severe   ቡና   ባለመጠጣት   ይሁን   ናዝ        complication   አላወቅኩም  
EVAL: ✓    ✓     ✓    ✓     ✓     ✓     ✓      ✓        ✓    SUB      ✓     SUB       ✓              ✓       
```

#### Addis Ai
- **Latency**: 3.84s | **Ref Words**: 14 | **Errors**: 8 (S: 8, D: 0, I: 0)
- **WER**: **57.1%** | **Word Accuracy**: **42.9%** | **CER**: 62.9%

```text
REF : ራስ   ምታቱ   አለ   but   its   not   that   severe   ቡና   ባለመጠጣቴ   ይሁን   another   complication   አላወቅኩም  
HYP : ራስ   ምታቱ   አለ   በት    ኢትስ   ኖት    ዛት     ሰቪር      ቡና   ባለመጠጣት   ይሁን   አናዘር      ኮምፕሊኬሽን        አላወቅኩም  
EVAL: ✓    ✓     ✓    SUB   SUB   SUB   SUB    SUB      ✓    SUB      ✓     SUB       SUB            ✓       
```

#### Gemini
- **Latency**: 3.87s | **Ref Words**: 14 | **Errors**: 12 (S: 11, D: 1, I: 0)
- **WER**: **85.7%** | **Word Accuracy**: **14.3%** | **CER**: 67.7%

```text
REF : ራስ    ምታቱ   አለ    but   its   not   that   severe   ቡና   ባለመጠጣቴ   ይሁን        another   complication   አላወቅኩም  
HYP : ራሽ    መታቶ   አለህ   ብት    ኢትስ   ኖት    ዳት     ሴቭየር     ቡና   ---      ባለመጠጣቴሁን   አናዘር      ኮምፕሊኬሽን        አላወቅኩም  
EVAL: SUB   SUB   SUB   SUB   SUB   SUB   SUB    SUB      ✓    DEL      SUB        SUB       SUB            ✓       
```

---

### Voice: `v89.wav`
> **Ground Truth Reference**:
> *ሆዴን ይቆርጠኛል፤ is it normal contractions ወይስ I should visit the clinic right now?*

#### Sahara
- **Latency**: 3.33s | **Ref Words**: 14 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **14.3%** | **Word Accuracy**: **85.7%** | **CER**: 12.7%

```text
REF : ሆዴን     ይቆርጠኛል   is   it   normal   contractions   ወይስ   i    should   visit   the   clinic   right   now  
HYP : hodin   ይቆርጠኛል   is   it   normal   contractions   way   i    should   visit   the   clinic   right   now  
EVAL: SUB     ✓        ✓    ✓    ✓        ✓              SUB   ✓    ✓        ✓       ✓     ✓        ✓       ✓    
```

#### Addis Ai
- **Latency**: 3.65s | **Ref Words**: 14 | **Errors**: 11 (S: 11, D: 0, I: 0)
- **WER**: **78.6%** | **Word Accuracy**: **21.4%** | **CER**: 81.0%

```text
REF : ሆዴን   ይቆርጠኛል   is    it    normal   contractions   ወይስ   i     should   visit   the   clinic   right   now  
HYP : ሆዴን   ይቆርጠኛል   ኢዝ    ኢት    ኖርማል     ኮንትራክሽንስ       ወይስ   አይ    ሹድ       ቪዚት     ዘ     ክሊኒክ     ራይት     ናው   
EVAL: ✓     ✓        SUB   SUB   SUB      SUB            ✓     SUB   SUB      SUB     SUB   SUB      SUB     SUB  
```

#### Gemini
- **Latency**: 4.51s | **Ref Words**: 14 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **21.4%** | **Word Accuracy**: **78.6%** | **CER**: 15.9%

```text
REF : ሆዴን   ይቆርጠኛል   is    it    normal   contractions   ወይስ   i    should   visit   the   clinic   right   now  
HYP : ሆዴን   ይቆርጠኛል   इज    इट    नॉर्मल   contractions   ወይስ   i    should   visit   the   clinic   right   now  
EVAL: ✓     ✓        SUB   SUB   SUB      ✓              ✓     ✓    ✓        ✓       ✓     ✓        ✓       ✓    
```

---

### Voice: `v90.wav`
> **Ground Truth Reference**:
> *ኧረ blood ሳይሆን ትንሽ brownish spot ነው፤ does that count as a danger sign?*

#### Sahara
- **Latency**: 2.81s | **Ref Words**: 14 | **Errors**: 7 (S: 2, D: 5, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 35.2%

```text
REF : ኧረ    blood   ሳይሆን   ትንሽ   brownish   spot   ነው   does   that   count   as     a     danger   sign  
HYP : ---   ---     ---    ---   brownish   spot   ነው   does   that   ---     come   to    danger   sign  
EVAL: DEL   DEL     DEL    DEL   ✓          ✓      ✓    ✓      ✓      DEL     SUB    SUB   ✓        ✓     
```

#### Addis Ai
- **Latency**: 3.48s | **Ref Words**: 14 | **Errors**: 11 (S: 10, D: 1, I: 0)
- **WER**: **78.6%** | **Word Accuracy**: **21.4%** | **CER**: 81.5%

```text
REF : ኧረ    blood   ሳይሆን   ትንሽ   brownish   spot   ነው   does   that   count   as     a     danger   sign  
HYP : አረ    ብለድ     ሳይሆን   ትንሽ   ብራውኒሽ      ስፖት    ነው   ---    ደዝ     ዳዝ      ካውንታ   ሰ     ዳንጀር     ሳይን   
EVAL: SUB   SUB     ✓      ✓     SUB        SUB    ✓    DEL    SUB    SUB     SUB    SUB   SUB      SUB   
```

#### Gemini
- **Latency**: 5.53s | **Ref Words**: 14 | **Errors**: 13 (S: 12, D: 0, I: 1)
- **WER**: **92.9%** | **Word Accuracy**: **7.1%** | **CER**: 85.2%

```text
REF : ኧረ    blood   ሳይሆን   ትንሽ   ---    brownish   spot   ነው   does   that   count   as    a     danger   sign  
HYP : አረ    በልድ     ሳዮን    ትንሽ   ብራውን   እሽ         ስፖት    ነው   ደዝ     ዘት     ካውንት    አስ    ኤ     ዳንጀር     ሳይን   
EVAL: SUB   SUB     SUB    ✓     INS    SUB        SUB    ✓    SUB    SUB    SUB     SUB   SUB   SUB      SUB   
```

---
