# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v51_v55_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:50:08 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 61 | 16 | 12 | 4 | 0 | **26.2%** | **73.8%** | 13.5% | 3.79s |
| **Addis Ai** | 61 | 8 | 6 | 2 | 0 | **13.1%** | **86.9%** | 3.6% | 3.99s |
| **Gemini** | 61 | 8 | 7 | 1 | 0 | **13.1%** | **86.9%** | 4.5% | 5.96s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v51.wav`
> **Ground Truth Reference**:
> *የጠቀስከው ህመም የለም፤ ግን ምግብ ከበላሁ በኋላ ቃር ደረቴን ያቃጥለኛል፣ ውኃም ማሳረግ አልቻልኩም።*

#### Sahara
- **Latency**: 4.11s | **Ref Words**: 13 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **23.1%** | **Word Accuracy**: **76.9%** | **CER**: 8.2%

```text
REF : የጠቀስከው   ህመም   የለም   ግን   ምግብ   ከበላሁ   በኋላ   ቃር    ደረቴን   ያቃጥለኛል   ውኃም   ማሳረግ   አልቻልኩም  
HYP : የጠቀስከው   ህመም   የለም   ግን   ምግብ   ከበላሁ   በኋላ   ቃል    ደራሴን   ያቃጥለኛል   ውሃም   ማሳረግ   አልቻልኩም  
EVAL: ✓        ✓     ✓     ✓    ✓     ✓      ✓     SUB   SUB    ✓        SUB   ✓      ✓       
```

#### Addis Ai
- **Latency**: 3.48s | **Ref Words**: 13 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 6.1%

```text
REF : የጠቀስከው   ህመም   የለም   ግን   ምግብ   ከበላሁ   በኋላ   ቃር    ደረቴን   ያቃጥለኛል   ውኃም   ማሳረግ   አልቻልኩም  
HYP : የጠቀስከው   ህመም   የለም   ግን   ምግብ   ከበላሁ   በኋላ   ---   ደረቴን   ያቃጥለኛል   ውሃም   ማሳረግ   አልቻልኩም  
EVAL: ✓        ✓     ✓     ✓    ✓     ✓      ✓     DEL   ✓      ✓        SUB   ✓      ✓       
```

#### Gemini
- **Latency**: 4.81s | **Ref Words**: 13 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 10.2%

```text
REF : የጠቀስከው   ህመም   የለም   ግን   ምግብ   ከበላሁ   በኋላ   ቃር   ደረቴን   ያቃጥለኛል   ውኃም   ማሳረግ   አልቻልኩም  
HYP : የተቀሰቀሰ   ህመም   የለም   ግን   ምግብ   ከበላሁ   በኋላ   ቃር   ደረቴን   ያቃጥለኛል   ውሃም   ማሳረግ   አልቻልኩም  
EVAL: SUB      ✓     ✓     ✓    ✓     ✓      ✓     ✓    ✓      ✓        SUB   ✓      ✓       
```

---

### Voice: `v52.wav`
> **Ground Truth Reference**:
> *ጽኑ ህመም አይደለም፣ የሆድ ድርቀት ስላለብኝ እና ሆዴ ስለተነፋ ትንሽ መክበድ ተሰምቶኛል።*

#### Sahara
- **Latency**: 4.25s | **Ref Words**: 12 | **Errors**: 5 (S: 1, D: 4, I: 0)
- **WER**: **41.7%** | **Word Accuracy**: **58.3%** | **CER**: 31.8%

```text
REF : ጽኑ    ህመም   አይደለም   የሆድ   ድርቀት   ስላለብኝ   እና   ሆዴ   ስለተነፋ   ትንሽ   መክበድ   ተሰምቶኛል  
HYP : ---   ---   ---     ---   ድርቀት   ስላለብኝ   እና   ሆዴ   ስለተነፋ   ትንሽ   መክድ    ተሰምቶኛል  
EVAL: DEL   DEL   DEL     DEL   ✓      ✓       ✓    ✓    ✓       ✓     SUB    ✓       
```

#### Addis Ai
- **Latency**: 4.3s | **Ref Words**: 12 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 4.5%

```text
REF : ጽኑ   ህመም   አይደለም   የሆድ   ድርቀት   ስላለብኝ   እና       ሆዴ   ስለተነፋ   ትንሽ   መክበድ   ተሰምቶኛል  
HYP : ጽኑ   ህመም   አይደለም   የሆድ   ድርቀት   ---     ስላለብኝና   ሆዴ   ስለተነፋ   ትንሽ   መክፈድ   ተሰምቶኛል  
EVAL: ✓    ✓     ✓       ✓     ✓      DEL     SUB      ✓    ✓       ✓     SUB    ✓       
```

#### Gemini
- **Latency**: 6.97s | **Ref Words**: 12 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 2.3%

```text
REF : ጽኑ   ህመም   አይደለም   የሆድ   ድርቀት   ስላለብኝ   እና       ሆዴ   ስለተነፋ   ትንሽ   መክበድ   ተሰምቶኛል  
HYP : ጽኑ   ህመም   አይደለም   የሆድ   ድርቀት   ---     ስላለብኝና   ሆዴ   ስለተነፋ   ትንሽ   መክበድ   ተሰምቶኛል  
EVAL: ✓    ✓     ✓       ✓     ✓      DEL     SUB      ✓    ✓       ✓     ✓      ✓       
```

---

### Voice: `v53.wav`
> **Ground Truth Reference**:
> *ሆዴ ስለተወጣጠረ ትንሽ ያሳክከኛል እንጂ ቁርጠት ወይም የሚወጋ የሆድ ህመም የለም።*

#### Sahara
- **Latency**: 3.23s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ሆዴ   ስለተወጣጠረ   ትንሽ   ያሳክከኛል   እንጂ   ቁርጠት   ወይም   የሚወጋ   የሆድ   ህመም   የለም  
HYP : ሆዴ   ስለተወጣጠረ   ትንሽ   ያሳክከኛል   እንጂ   ቁርጠት   ወይም   የሚወጋ   የሆድ   ህመም   የለም  
EVAL: ✓    ✓         ✓     ✓        ✓     ✓      ✓     ✓      ✓     ✓     ✓    
```

#### Addis Ai
- **Latency**: 3.89s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ሆዴ   ስለተወጣጠረ   ትንሽ   ያሳክከኛል   እንጂ   ቁርጠት   ወይም   የሚወጋ   የሆድ   ህመም   የለም  
HYP : ሆዴ   ስለተወጣጠረ   ትንሽ   ያሳክከኛል   እንጂ   ቁርጠት   ወይም   የሚወጋ   የሆድ   ህመም   የለም  
EVAL: ✓    ✓         ✓     ✓        ✓     ✓      ✓     ✓      ✓     ✓     ✓    
```

#### Gemini
- **Latency**: 6.76s | **Ref Words**: 11 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ሆዴ   ስለተወጣጠረ   ትንሽ   ያሳክከኛል   እንጂ   ቁርጠት   ወይም   የሚወጋ   የሆድ   ህመም   የለም  
HYP : ሆዴ   ስለተወጣጠረ   ትንሽ   ያሳክከኛል   እንጂ   ቁርጠት   ወይም   የሚወጋ   የሆድ   ህመም   የለም  
EVAL: ✓    ✓         ✓     ✓        ✓     ✓      ✓     ✓      ✓     ✓     ✓    
```

---

### Voice: `v54.wav`
> **Ground Truth Reference**:
> *ድንገት ስነሳ ትንሽ ጎኔን ቆንጠጥ ያደርገኛል፣ ግን ወዲያው ይተወኛል፤ ጽኑ ህመም አይደለም።*

#### Sahara
- **Latency**: 3.75s | **Ref Words**: 12 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 9.1%

```text
REF : ድንገት   ስነሳ    ትንሽ   ጎኔን   ቆንጠጥ   ያደርገኛል   ግን   ወዲያው   ይተወኛል   ጽኑ   ህመም   አይደለም  
HYP : ድንገት   ስንነሳ   ትንሽ   ጎኒን   ቆንጠጥ   ያደርገኛል   ግን   ወዲያው   ይቶኛል    ጽኑ   ህመም   አይደለም  
EVAL: ✓      SUB    ✓     SUB   ✓      ✓        ✓    ✓      SUB     ✓    ✓     ✓      
```

#### Addis Ai
- **Latency**: 3.98s | **Ref Words**: 12 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : ድንገት   ስነሳ   ትንሽ   ጎኔን   ቆንጠጥ   ያደርገኛል   ግን   ወዲያው   ይተወኛል   ጽኑ   ህመም   አይደለም  
HYP : ድንገት   ስነሳ   ትንሽ   ጎኔን   ቆንጠጥ   ያደርገኛል   ግን   ወዲያው   ይተወኛል   ጽኑ   ህመም   አይደለም  
EVAL: ✓      ✓     ✓     ✓     ✓      ✓        ✓    ✓      ✓       ✓    ✓     ✓      
```

#### Gemini
- **Latency**: 5.33s | **Ref Words**: 12 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 4.5%

```text
REF : ድንገት   ስነሳ   ትንሽ   ጎኔን   ቆንጠጥ   ያደርገኛል   ግን   ወዲያው   ይተወኛል   ጽኑ    ህመም   አይደለም  
HYP : ድንገት   ስነሳ   ትንሽ   ጎኔን   ቆንጠጥ   ያደርገኛል   ግን   ወዲያው   ይተውኛል   ፅኑ    ህመም   አይደለም  
EVAL: ✓      ✓     ✓     ✓     ✓      ✓        ✓    ✓      SUB     SUB   ✓     ✓      
```

---

### Voice: `v55.wav`
> **Ground Truth Reference**:
> *ሆዴ ክብደት ሲጨምር ዳሌዬ እና የታችኛው ወገቤን ዛል ያደርገኛል፤ ጋደም ስል ግን ይሻለኛል።*

#### Sahara
- **Latency**: 3.63s | **Ref Words**: 13 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **38.5%** | **Word Accuracy**: **61.5%** | **CER**: 18.2%

```text
REF : ሆዴ   ክብደት   ሲጨምር   ዳሌዬ   እና   የታችኛው   ወገቤን   ዛል    ያደርገኛል   ጋደም   ስል    ግን   ይሻለኛል  
HYP : ሆዴ   ክብደት   ሲጨምር   ዳሌ    እና   የታችኛው   ወገቢ    ዛሌ    ያደረገ     ጋደም   ስር    ግን   ይሻለኛል  
EVAL: ✓    ✓      ✓      SUB   ✓    ✓       SUB    SUB   SUB      ✓     SUB   ✓    ✓      
```

#### Addis Ai
- **Latency**: 4.3s | **Ref Words**: 13 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **23.1%** | **Word Accuracy**: **76.9%** | **CER**: 6.8%

```text
REF : ሆዴ   ክብደት   ሲጨምር   ዳሌዬ   እና   የታችኛው   ወገቤን   ዛል   ያደርገኛል   ጋደም   ስል    ግን   ይሻለኛል  
HYP : ሆዴ   ክብደት   ሲጨምር   ዳሌ    እና   የታችኛው   ወገቤ    ዛል   ያደርገኛል   ጋደም   ስር    ግን   ይሻለኛል  
EVAL: ✓    ✓      ✓      SUB   ✓    ✓       SUB    ✓    ✓        ✓     SUB   ✓    ✓      
```

#### Gemini
- **Latency**: 5.94s | **Ref Words**: 13 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 4.5%

```text
REF : ሆዴ   ክብደት   ሲጨምር   ዳሌዬ   እና   የታችኛው   ወገቤን   ዛል   ያደርገኛል   ጋደም   ስል   ግን   ይሻለኛል  
HYP : ሆዴ   ክብደት   ሲጨምር   ዳሌዬ   እና   የታችኛው   ወገቤ    ዛል   ያደረገኛል   ጋደም   ስል   ግን   ይሻለኛል  
EVAL: ✓    ✓      ✓      ✓     ✓    ✓       SUB    ✓    SUB      ✓     ✓    ✓    ✓      
```

---
