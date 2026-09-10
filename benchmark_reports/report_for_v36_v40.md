# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v36_v40_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:49:31 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 50 | 13 | 11 | 1 | 1 | **26.0%** | **74.0%** | 11.8% | 2.75s |
| **Addis Ai** | 50 | 6 | 5 | 0 | 1 | **12.0%** | **88.0%** | 4.1% | 3.52s |
| **Gemini** | 50 | 8 | 8 | 0 | 0 | **16.0%** | **84.0%** | 5.6% | 9.05s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v36.wav`
> **Ground Truth Reference**:
> *መተንፈስ አቅቶኛል፤ አየር ወደ ውስጥ መሳብም አልቻልኩም፣ ልቤም በጣም ይመታል።*

#### Sahara
- **Latency**: 2.6s | **Ref Words**: 10 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 2.6%

```text
REF : መተንፈስ   አቅቶኛል   አየር   ወደ   ውስጥ   መሳብም   አልቻልኩም   ልቤም   በጣም   ይመታል  
HYP : መተንፈስ   አቅቶኛል   አየር   ወደ   ውስጥ   መሳብም   አልቻልኩም   ልቤም   በጣም   ይመሳል  
EVAL: ✓       ✓       ✓     ✓    ✓     ✓      ✓        ✓     ✓     SUB   
```

#### Addis Ai
- **Latency**: 4.31s | **Ref Words**: 10 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : መተንፈስ   አቅቶኛል   አየር   ወደ   ውስጥ   መሳብም   አልቻልኩም   ልቤም   በጣም   ይመታል  
HYP : መተንፈስ   አቅቶኛል   አየር   ወደ   ውስጥ   መሳብም   አልቻልኩም   ልቤም   በጣም   ይመታል  
EVAL: ✓       ✓       ✓     ✓    ✓     ✓      ✓        ✓     ✓     ✓     
```

#### Gemini
- **Latency**: 8.39s | **Ref Words**: 10 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : መተንፈስ   አቅቶኛል   አየር   ወደ   ውስጥ   መሳብም   አልቻልኩም   ልቤም   በጣም   ይመታል  
HYP : መተንፈስ   አቅቶኛል   አየር   ወደ   ውስጥ   መሳብም   አልቻልኩም   ልቤም   በጣም   ይመታል  
EVAL: ✓       ✓       ✓     ✓    ✓     ✓      ✓        ✓     ✓     ✓     
```

---

### Voice: `v37.wav`
> **Ground Truth Reference**:
> *ውኃ እንኳን ብጠጣ መልሶ ይወጣል፤ ዛሬ ብቻ ከአስር ጊዜ በላይ አስታወከኝ፣ በጣም ዝያለሁ።*

#### Sahara
- **Latency**: 2.76s | **Ref Words**: 13 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 21.4%

```text
REF : ውኃ    እንኳን   ብጠጣ   መልሶ   ይወጣል   ዛሬ   ብቻ   ከአስር   ጊዜ   በላይ   አስታወከኝ   በጣም   ዝያለሁ  
HYP : ውሃ    እንኳን   ብጠጣ   መልሶ   ---    ዛሬ   ብቻ   ከ10    ጊዜ   በላይ   አስታወቀኝ   በጣም   ዝያለሁ  
EVAL: SUB   ✓      ✓     ✓     DEL    ✓    ✓    SUB    ✓    ✓     SUB      ✓     ✓     
```

#### Addis Ai
- **Latency**: 3.29s | **Ref Words**: 13 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 4.8%

```text
REF : ውኃ    እንኳን   ብጠጣ    መልሶ   ይወጣል   ዛሬ   ብቻ   ከአስር   ጊዜ   በላይ   አስታወከኝ   በጣም   ዝያለሁ  
HYP : ውሃ    እንኳን   ብጠጣው   መልሶ   ይወጣል   ዛሬ   ብቻ   ከአስር   ጊዜ   በላይ   አስታወከኝ   በጣም   ዝያለሁ  
EVAL: SUB   ✓      SUB    ✓     ✓      ✓    ✓    ✓      ✓    ✓     ✓        ✓     ✓     
```

#### Gemini
- **Latency**: 10.15s | **Ref Words**: 13 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **23.1%** | **Word Accuracy**: **76.9%** | **CER**: 7.1%

```text
REF : ውኃ    እንኳን   ብጠጣ    መልሶ   ይወጣል   ዛሬ   ብቻ   ከአስር   ጊዜ   በላይ   አስታወከኝ   በጣም   ዝያለሁ  
HYP : ውሃ    እንኳን   ብጠጣው   መልሶ   ይወጣል   ዛሬ   ብቻ   ከአስር   ጊዜ   በላይ   አስታወከኝ   በጣም   ዘያለሁ  
EVAL: SUB   ✓      SUB    ✓     ✓      ✓    ✓    ✓      ✓    ✓     ✓        ✓     SUB   
```

---

### Voice: `v38.wav`
> **Ground Truth Reference**:
> *ሰውነቴ እየነደደ ነው፤ ብርድ ብርድ እራሱ እያንቀጠቀጠኝ ነው።*

#### Sahara
- **Latency**: 2.58s | **Ref Words**: 8 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 6.7%

```text
REF : ሰውነቴ   እየነደደ   ነው   ብርድ   ብርድ   እራሱ   እያንቀጠቀጠኝ   ነው  
HYP : ሰውነቴ   እየነደደ   ነው   ብርድ   ብርድ   ራሱ    እያንቀጠቀጠ    ነው  
EVAL: ✓      ✓       ✓    ✓     ✓     SUB   SUB        ✓   
```

#### Addis Ai
- **Latency**: 3.68s | **Ref Words**: 8 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 3.3%

```text
REF : ሰውነቴ   እየነደደ   ነው   ብርድ   ብርድ   እራሱ   እያንቀጠቀጠኝ   ነው  
HYP : ሰውነቴ   እየነደደ   ነው   ብርድ   ብርድ   ራሱ    እያንቀጠቀጠኝ   ነው  
EVAL: ✓      ✓       ✓    ✓     ✓     SUB   ✓          ✓   
```

#### Gemini
- **Latency**: 6.91s | **Ref Words**: 8 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 10.0%

```text
REF : ሰውነቴ   እየነደደ   ነው   ብርድ   ብርድ   እራሱ   እያንቀጠቀጠኝ   ነው  
HYP : ሰውነቴ   እየነደደ   ነው   ብርድ   ብርድ   ራሱ    ያንቀጠቅጠኝ    ነው  
EVAL: ✓      ✓       ✓    ✓     ✓     SUB   SUB        ✓   
```

---

### Voice: `v39.wav`
> **Ground Truth Reference**:
> *ወገቤን ከአጥንቴ ውስጥ የሚቆርጠኝ ይመስላል፤ አልጋ ላይ መገለባበጥ እንኳን አልቻልኩም።*

#### Sahara
- **Latency**: 3.23s | **Ref Words**: 10 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 11.4%

```text
REF : ወገቤን   ከአጥንቴ   ውስጥ   የሚቆርጠኝ   ይመስላል   አልጋ   ላይ   ---     መገለባበጥ   እንኳን   አልቻልኩም  
HYP : ወገቤን   ከአጥንቴ   ውስጥ   የሚቆርጠኝ   ይመስላል   አልጋ   ላይ   መንገላይ   ዋብጥ      እንኳን   አልቻልኩም  
EVAL: ✓      ✓       ✓     ✓        ✓       ✓     ✓    INS     SUB      ✓      ✓       
```

#### Addis Ai
- **Latency**: 2.96s | **Ref Words**: 10 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 6.8%

```text
REF : ወገቤን   ከአጥንቴ   ውስጥ   የሚቆርጠኝ   ይመስላል   አልጋ   ላይ   ---     መገለባበጥ   እንኳን   አልቻልኩም  
HYP : ወገቤን   ከአጥንቴ   ውስጥ   የሚቆርጠኝ   ይመስላል   አልጋ   ላይ   መገላያዋ   በጥ       እንኳን   አልቻልኩም  
EVAL: ✓      ✓       ✓     ✓        ✓       ✓     ✓    INS     SUB      ✓      ✓       
```

#### Gemini
- **Latency**: 8.8s | **Ref Words**: 10 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 4.5%

```text
REF : ወገቤን   ከአጥንቴ   ውስጥ   የሚቆርጠኝ   ይመስላል   አልጋ   ላይ   መገለባበጥ   እንኳን   አልቻልኩም  
HYP : ወገቤን   ከአጥንቴ   ውስጥ   የሚቆርጠኝ   ይመስላል   አልጋ   ላይ   መገላበጥ    እንኳን   አልቻልኩም  
EVAL: ✓      ✓       ✓     ✓        ✓       ✓     ✓    SUB      ✓      ✓       
```

---

### Voice: `v40.wav`
> **Ground Truth Reference**:
> *የተቀመጥኩበት ድረስ የደረሰ ንጹሕ ፈሳሽ በድንገት ፈሰሰኝ፤ መቆጣጠር አልቻልኩም።*

#### Sahara
- **Latency**: 2.57s | **Ref Words**: 9 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **44.4%** | **Word Accuracy**: **55.6%** | **CER**: 14.6%

```text
REF : የተቀመጥኩበት   ድረስ   የደረሰ    ንጹሕ   ፈሳሽ   በድንገት   ፈሰሰኝ   መቆጣጠር    አልቻልኩም  
HYP : የተቀመጥኩበት   ድረስ   የደረሰን   ንጹህ   ፈሶች   በድንገት   ፈሰሰኝ   መቆጣጠረው   አልቻልኩም  
EVAL: ✓          ✓     SUB     SUB   SUB   ✓       ✓      SUB      ✓       
```

#### Addis Ai
- **Latency**: 3.38s | **Ref Words**: 9 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 4.9%

```text
REF : የተቀመጥኩበት   ድረስ   የደረሰ   ንጹሕ   ፈሳሽ   በድንገት   ፈሰሰኝ   መቆጣጠር   አልቻልኩም  
HYP : የተቀመጥኩበት   ድረስ   የደረሰ   ንፁህ   ፈሳሽ   በድንገት   ፈሰሰኝ   መቆጣጠር   አልቻልኩም  
EVAL: ✓          ✓     ✓      SUB   ✓     ✓       ✓      ✓       ✓       
```

#### Gemini
- **Latency**: 11.01s | **Ref Words**: 9 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **22.2%** | **Word Accuracy**: **77.8%** | **CER**: 7.3%

```text
REF : የተቀመጥኩበት   ድረስ   የደረሰ   ንጹሕ   ፈሳሽ   በድንገት   ፈሰሰኝ   መቆጣጠር   አልቻልኩም  
HYP : የተቀመጥኩበት   ድረስ   የደረሰ   ንፁህ   ፈሶሽ   በድንገት   ፈሰሰኝ   መቆጣጠር   አልቻልኩም  
EVAL: ✓          ✓     ✓      SUB   SUB   ✓       ✓      ✓       ✓       
```

---
