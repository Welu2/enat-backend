# STT Benchmark Evaluation Report

- **Benchmark Results**: `benchmark_results_v101_v105_am.json`
- **Ground Truth**: `transcript.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 5
- **Evaluation Date**: 2026-09-08 09:52:06 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 67 | 23 | 19 | 4 | 0 | **34.3%** | **65.7%** | 17.3% | 3.53s |
| **Addis Ai** | 67 | 35 | 35 | 0 | 0 | **52.2%** | **47.8%** | 56.7% | 3.77s |
| **Gemini** | 67 | 21 | 18 | 2 | 1 | **31.3%** | **68.7%** | 21.2% | 3.86s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v101.wav`
> **Ground Truth Reference**:
> *I have massive headache፤ throbbing pain ነው፣ darkness ውስጥ ካልተኛሁ አይለቀኝም።*

#### Sahara
- **Latency**: 3.92s | **Ref Words**: 11 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **27.3%** | **Word Accuracy**: **72.7%** | **CER**: 7.0%

```text
REF : i    have   massive   headache   throbbing   pain   ነው   darkness   ውስጥ   ካልተኛሁ   አይለቀኝም  
HYP : i    have   massive   headache   drobbing    pain   ነው   darkness   ውስጥ   ካልተኘሁ   አይለቅኝም  
EVAL: ✓    ✓      ✓         ✓          SUB         ✓      ✓    ✓          ✓     SUB     SUB     
```

#### Addis Ai
- **Latency**: 3.42s | **Ref Words**: 11 | **Errors**: 7 (S: 7, D: 0, I: 0)
- **WER**: **63.6%** | **Word Accuracy**: **36.4%** | **CER**: 71.9%

```text
REF : i     have   massive   headache   throbbing   pain   ነው   darkness   ውስጥ   ካልተኛሁ   አይለቀኝም  
HYP : አይ    ሃቭ     ማሲቭ       ሄደክ        ትራቪንግ       ፔን     ነው   ዳርክነስ      ውስጥ   ካልተኛሁ   አይለቀኝም  
EVAL: SUB   SUB    SUB       SUB        SUB         SUB    ✓    SUB        ✓     ✓       ✓       
```

#### Gemini
- **Latency**: 4.36s | **Ref Words**: 11 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **18.2%** | **Word Accuracy**: **81.8%** | **CER**: 8.8%

```text
REF : i    have   massive   headache   throbbing   pain   ነው    darkness   ውስጥ   ካልተኛሁ   አይለቀኝም  
HYP : i    have   massive   headache   throbbing   pain   ---   darkness   ኝ     ካልተኛሁ   አይለቀኝም  
EVAL: ✓    ✓      ✓         ✓          ✓           ✓      DEL   ✓          SUB   ✓       ✓       
```

---

### Voice: `v102.wav`
> **Ground Truth Reference**:
> *ዓይኔ completely blurry ሆኗል፤ spots እና flashing lights ይታየኛል፣ I can't read anything.*

#### Sahara
- **Latency**: 3.84s | **Ref Words**: 13 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **46.2%** | **Word Accuracy**: **53.8%** | **CER**: 23.1%

```text
REF : ዓይኔ   completely   blurry   ሆኗል   spots   እና    flashing   lights   ይታየኛል   i    cant   read   anything  
HYP : i     necetly      barry    ሆኗል   spots   and   flushing   lights   ይታይኛል   i    cant   read   anything  
EVAL: SUB   SUB          SUB      ✓     ✓       SUB   SUB        ✓        SUB     ✓    ✓      ✓      ✓         
```

#### Addis Ai
- **Latency**: 4.59s | **Ref Words**: 13 | **Errors**: 11 (S: 11, D: 0, I: 0)
- **WER**: **84.6%** | **Word Accuracy**: **15.4%** | **CER**: 84.6%

```text
REF : ዓይኔ   completely   blurry   ሆኗል   spots   እና    flashing   lights   ይታየኛል   i     cant   read   anything  
HYP : አይኔ   ኮምፕሊትሊ       ብረሪ      ሆኗል   ስፖትስ    ኤንድ   ፍላሽንግ      ላይትስ     ይታየኛል   አይ    ካንት    ሪድ     ኤኒቲንግ     
EVAL: SUB   SUB          SUB      ✓     SUB     SUB   SUB        SUB      ✓       SUB   SUB    SUB    SUB       
```

#### Gemini
- **Latency**: 4.22s | **Ref Words**: 13 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **30.8%** | **Word Accuracy**: **69.2%** | **CER**: 18.5%

```text
REF : ዓይኔ    completely   blurry   ሆኗል   spots   እና    flashing   lights   ይታየኛል   i     cant   read   anything  
HYP : አይንዬ   completely   blurry   ሆኗል   spots   and   flashing   lights   ይታየኛል   አይ    कांट   read   anything  
EVAL: SUB    ✓            ✓        ✓     ✓       SUB   ✓          ✓        ✓       SUB   SUB    ✓      ✓         
```

---

### Voice: `v103.wav`
> **Ground Truth Reference**:
> *ቶሎ ቶሎ የሚወጣ fluid አለኝ፤ like watery discharge ነው፣ padን fully soak አድርጎታል።*

#### Sahara
- **Latency**: 3.03s | **Ref Words**: 13 | **Errors**: 5 (S: 4, D: 1, I: 0)
- **WER**: **38.5%** | **Word Accuracy**: **61.5%** | **CER**: 28.6%

```text
REF : ቶሎ   ቶሎ   የሚወጣ   fluid   አለኝ   like   watery     discharge   ነው   padን      fully   soak   አድርጎታል  
HYP : ቶሎ   ቶሎ   የሚወጣ   ---     አለኝ   like   watering   discharge   ነው   padding   fully   so     ካርጎታል   
EVAL: ✓    ✓    ✓      DEL     ✓     ✓      SUB        ✓           ✓    SUB       ✓       SUB    SUB     
```

#### Addis Ai
- **Latency**: 3.88s | **Ref Words**: 13 | **Errors**: 7 (S: 7, D: 0, I: 0)
- **WER**: **53.8%** | **Word Accuracy**: **46.2%** | **CER**: 64.3%

```text
REF : ቶሎ   ቶሎ   የሚወጣ   fluid   አለኝ   like   watery   discharge   ነው   padን   fully   soak   አድርጎታል  
HYP : ቶሎ   ቶሎ   የሚወጣ   ፍሉድ     አለኝ   ላይክ    ዋተሪን     ዲስቻርጅ       ነው   ፓዴን    ፉሊ      ሶክ     አድርጎታል  
EVAL: ✓    ✓    ✓      SUB     ✓     SUB    SUB      SUB         ✓    SUB    SUB     SUB    ✓       
```

#### Gemini
- **Latency**: 3.49s | **Ref Words**: 13 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **46.2%** | **Word Accuracy**: **53.8%** | **CER**: 25.0%

```text
REF : ቶሎ   ቶሎ   የሚወጣ   fluid   አለኝ    like   watery   discharge   ነው   padን      fully   soak   አድርጎታል  
HYP : ቶሎ   ቶሎ   የሚመጣ   ﬂuid    አልነኝ   like   watery   discharge   ነው   padding   fully   so     ሰካጎታል   
EVAL: ✓    ✓    SUB    SUB     SUB    ✓      ✓        ✓           ✓    SUB       ✓       SUB    SUB     
```

---

### Voice: `v104.wav`
> **Ground Truth Reference**:
> *Spotting ሳይሆን actual fresh red bleeding አለ፤ clot ነገርም አይቻለሁ፣ its በጣም scary.*

#### Sahara
- **Latency**: 3.82s | **Ref Words**: 13 | **Errors**: 7 (S: 5, D: 2, I: 0)
- **WER**: **53.8%** | **Word Accuracy**: **46.2%** | **CER**: 25.0%

```text
REF : spotting   ሳይሆን   actual     fresh   red   bleeding   አለ    clot   ነገርም   አይቻለሁ   its   በጣም    scary  
HYP : sputting   ሳይሆን   actually   fresh   red   bleeding   ---   ---    አለም    አይቻለሁ   its   bets   gay    
EVAL: SUB        ✓      SUB        ✓       ✓     ✓          DEL   DEL    SUB    ✓       ✓     SUB    SUB    
```

#### Addis Ai
- **Latency**: 3.48s | **Ref Words**: 13 | **Errors**: 9 (S: 9, D: 0, I: 0)
- **WER**: **69.2%** | **Word Accuracy**: **30.8%** | **CER**: 71.7%

```text
REF : spotting   ሳይሆን   actual   fresh   red   bleeding   አለ   clot   ነገርም   አይቻለሁ   its   በጣም   scary  
HYP : ስፖቲንግ      ሳይሆን   አክቹዋል    ፍሬሽ     ሬድ    ብሊዲንግ      አለ   ክሎት    ነገርም   ወይቻለሁ   ኢትስ   በጣም   ስኬሪ    
EVAL: SUB        ✓      SUB      SUB     SUB   SUB        ✓    SUB    ✓      SUB     SUB   ✓     SUB    
```

#### Gemini
- **Latency**: 3.46s | **Ref Words**: 13 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 6.7%

```text
REF : spotting   ሳይሆን   actual   fresh   red   bleeding   አለ   clot   ነገርም   አይቻለሁ   its   በጣም   scary  
HYP : spotting   ሳይሆን   actual   fresh   red   bleeding   አለ   clot   ነገርም   ሆይቻለሁ   እሱ    በጣም   scary  
EVAL: ✓          ✓      ✓        ✓       ✓     ✓          ✓    ✓      ✓      SUB     SUB   ✓     ✓      
```

---

### Voice: `v105.wav`
> **Ground Truth Reference**:
> *The baby is barely moving፤ count ሳደርግ since morning two kicks ብቻ ነው፣ usually very active ነበር።*

#### Sahara
- **Latency**: 3.06s | **Ref Words**: 17 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **11.8%** | **Word Accuracy**: **88.2%** | **CER**: 5.4%

```text
REF : the   baby   is   barely   moving   count   ሳደርግ       since   morning   two   kicks   ብቻ   ነው   usually   very   active   ነበር  
HYP : the   baby   is   barely   moving   ---     countade   since   morning   two   kicks   ብቻ   ነው   usually   very   active   ነበር  
EVAL: ✓     ✓      ✓    ✓        ✓        DEL     SUB        ✓       ✓         ✓     ✓       ✓    ✓    ✓         ✓      ✓        ✓    
```

#### Addis Ai
- **Latency**: 3.46s | **Ref Words**: 17 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **5.9%** | **Word Accuracy**: **94.1%** | **CER**: 2.7%

```text
REF : the   baby   is   barely   moving   count   ሳደርግ   since   morning   two   kicks   ብቻ   ነው   usually   very   active   ነበር  
HYP : the   baby   is   barely   moving   count   ሳረግ    since   morning   two   kicks   ብቻ   ነው   usually   very   active   ነበር  
EVAL: ✓     ✓      ✓    ✓        ✓        ✓       SUB    ✓       ✓         ✓     ✓       ✓    ✓    ✓         ✓      ✓        ✓    
```

#### Gemini
- **Latency**: 3.79s | **Ref Words**: 17 | **Errors**: 7 (S: 5, D: 1, I: 1)
- **WER**: **41.2%** | **Word Accuracy**: **58.8%** | **CER**: 41.9%

```text
REF : the   baby   is   barely   moving   count   ሳደርግ    since   morning   two   kicks   ብቻ     ነው        usually   ---   very   active   ነበር     
HYP : the   baby   is   barely   moving   ---     ቀንሳለች   since   morning   2     kicks   with   channel   usually   you   very   active   number  
EVAL: ✓     ✓      ✓    ✓        ✓        DEL     SUB     ✓       ✓         SUB   ✓       SUB    SUB       ✓         INS   ✓      ✓        SUB     
```

---
