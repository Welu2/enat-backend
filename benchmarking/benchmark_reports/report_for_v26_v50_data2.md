# STT Benchmark Evaluation Report

- **Benchmark Results**: `bench_am_eng_part2.json`
- **Ground Truth**: `ground_truth.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 25
- **Evaluation Date**: 2026-09-09 19:23:59 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 959 | 256 | 175 | 76 | 5 | **26.7%** | **73.3%** | 17.3% | 5.99s |
| **Addis Ai** | 959 | 553 | 510 | 28 | 15 | **57.7%** | **42.3%** | 65.2% | 6.00s |
| **Gemini** | 959 | 126 | 85 | 26 | 15 | **13.1%** | **86.9%** | 6.4% | 21.09s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v26.wav`
> **Ground Truth Reference**:
> *እግሬ በጣም እያበጠ ነው፤ today both feet ላይ severe swelling አለ፣ ጫማዬም አልገባ ብሎኛል። ከዚህም በተጨማሪ mild headache አለኝ። BPዬ high ሆኖ እንዳይሆን ፈርቻለሁ፤ nearby clinic ሄጄ blood pressure check ማድረግ አለብኝ ወይስ tomorrow morning መምጣት ይሻላል?*

#### Sahara
- **Latency**: 4.8s | **Ref Words**: 37 | **Errors**: 8 (S: 2, D: 6, I: 0)
- **WER**: **21.6%** | **Word Accuracy**: **78.4%** | **CER**: 19.4%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ    እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   today   ---    ቦታ     ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   ---   ---    ---   ---      ---     bp       clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
EVAL: ✓     ✓     ✓      ✓    ✓       DEL    SUB    ✓    ✓        ✓          ✓    ✓      ✓      ✓      ✓      ✓       ✓      ✓          ✓     DEL   DEL    DEL   DEL      DEL     SUB      ✓        ✓    ✓       ✓          ✓       ✓      ✓      ✓     ✓          ✓         ✓      ✓     
```

#### Addis Ai
- **Latency**: 5.68s | **Ref Words**: 37 | **Errors**: 16 (S: 16, D: 0, I: 0)
- **WER**: **43.2%** | **Word Accuracy**: **56.8%** | **CER**: 54.5%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   ቱዴይ     ቦት     ፊት     ላይ   ሲቪር      ስዌሊንግ      አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   ማይል    ሄዴክ        አለኝ   ቢፒዬ   ሃይ     ሆኖ   እንዳይሆን   ፈርቻለሁ   ኒርባይ     ክሊኒክ     ሄጄ   ብላት     ፕረሽር       ቼክ      ማድረግ   አለብኝ   ወይስ   ሞሮ         ሞኒንግ      መምጣት   ይሻላል  
EVAL: ✓     ✓     ✓      ✓    SUB     SUB    SUB    ✓    SUB      SUB        ✓    ✓      ✓      ✓      ✓      ✓       SUB    SUB        ✓     SUB   SUB    ✓    ✓        ✓       SUB      SUB      ✓    SUB     SUB        SUB     ✓      ✓      ✓     SUB        SUB       ✓      ✓     
```

#### Gemini
- **Latency**: 9.11s | **Ref Words**: 37 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
EVAL: ✓     ✓     ✓      ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓    ✓      ✓      ✓      ✓      ✓       ✓      ✓          ✓     ✓     ✓      ✓    ✓        ✓       ✓        ✓        ✓    ✓       ✓          ✓       ✓      ✓      ✓     ✓          ✓         ✓      ✓     
```

---

### Voice: `v27.wav`
> **Ground Truth Reference**:
> *እኔ የ folic acid እና iron supplementቱን correctly ወስጃለሁ፣ ምንም side effect የለብኝም። ግን the calcium tablets አልቀውብኛል፤ ባለፈው clinic ስሄድ pharmacy ውስጥ out of stock ነበር ያሉት። ዛሬ private pharmacy ፈልጌ መግዛት አለብኝ ወይስ next appointment ድረስ መጠበቅ እችላለሁ?*

#### Sahara
- **Latency**: 5.55s | **Ref Words**: 40 | **Errors**: 6 (S: 4, D: 2, I: 0)
- **WER**: **15.0%** | **Word Accuracy**: **85.0%** | **CER**: 14.5%

```text
REF : እኔ   የ    folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplement     correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   ታብለስ      አልቀውብኛል   ባለፈው   clinic   ስሄድ   ፋይ         ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmcy    ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   ---    ---    
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      SUB            ✓           ✓       ✓     ✓      ✓        ✓       ✓    ✓     ✓         SUB       ✓         ✓      ✓        ✓     SUB        ✓     ✓     ✓    ✓       ✓     ✓     ✓    ✓         SUB        ✓     ✓      ✓      ✓     ✓      ✓             ✓     DEL    DEL    
```

#### Addis Ai
- **Latency**: 5.43s | **Ref Words**: 40 | **Errors**: 21 (S: 20, D: 1, I: 0)
- **WER**: **52.5%** | **Word Accuracy**: **47.5%** | **CER**: 60.8%

```text
REF : እኔ   የ     folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ    ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of    stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   ---   የፎሊክ    አሲድ    እና   አይሮን   ሳፕሊመንቱን        ከሬክ         እወስጃለሁ   ምንም   ሳይድ    ኢፌክት     የለብኝም   ግን   ዘ     ካልሲየም     ታብለስ      አልቀውብኛል   ባለፈው   ክሊኒክ     ስሄድ   ፋርማሲ       ውስጥ   አውት   ኦፍ    ስቶክ     ነበር   ያሉት   ዛሬ   ፕራይቬት     ፋርማሲ       ፈልጌ   መግዛት   አለብኝ   ወይስ   ኔክስት   አፖይትመንት       ድረስ   መጠበቅ   እችላለሁ  
EVAL: ✓    DEL   SUB     SUB    ✓    SUB    SUB            SUB         SUB      ✓     SUB    SUB      ✓       ✓    SUB   SUB       SUB       ✓         ✓      SUB      ✓     SUB        ✓     SUB   SUB   SUB     ✓     ✓     ✓    SUB       SUB        ✓     ✓      ✓      ✓     SUB    SUB           ✓     ✓      ✓      
```

#### Gemini
- **Latency**: 15.05s | **Ref Words**: 40 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **7.5%** | **Word Accuracy**: **92.5%** | **CER**: 2.7%

```text
REF : እኔ   የ    folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplementኡን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   የ     calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበሩ   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      SUB            ✓           ✓       ✓     ✓      ✓        ✓       ✓    SUB   ✓         ✓         ✓         ✓      ✓        ✓     ✓          ✓     ✓     ✓    ✓       SUB   ✓     ✓    ✓         ✓          ✓     ✓      ✓      ✓     ✓      ✓             ✓     ✓      ✓      
```

---

### Voice: `v28.wav`
> **Ground Truth Reference**:
> *ዛሬ afternoon ላይ lower abdomenኔ tight እያደረገ frequent cramps ይሰማኛል፣ like period pain። intervalሉ ግን regular አይደለም። these are just Braxton Hicks contractions or early labor signs መሆናቸውን distinguish ማድረግ አልቻልኩም። what other warning signs should I monitor?*

#### Sahara
- **Latency**: 4.14s | **Ref Words**: 38 | **Errors**: 6 (S: 6, D: 0, I: 0)
- **WER**: **15.8%** | **Word Accuracy**: **84.2%** | **CER**: 7.2%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs     መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs      should   i    monitor  
HYP : ዛሬ   afternoon   ላይ   lower   abdomen    tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalu   ግን   regular   አይደለም   these   are   just   bruxton   hicks   contractions   or   early   labor   science   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   at      warning   sciences   should   i    monitor  
EVAL: ✓    ✓           ✓    ✓       SUB        ✓       ✓       ✓          ✓        ✓       ✓      ✓        ✓      SUB         ✓    ✓         ✓       ✓       ✓     ✓      SUB       ✓       ✓              ✓    ✓       ✓       SUB       ✓        ✓             ✓      ✓        ✓      SUB     ✓         SUB        ✓        ✓    ✓        
```

#### Addis Ai
- **Latency**: 5.94s | **Ref Words**: 38 | **Errors**: 30 (S: 29, D: 0, I: 1)
- **WER**: **79.0%** | **Word Accuracy**: **21.1%** | **CER**: 81.2%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   ---   these   are   just   braxton   hicks   contractions   or    early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i     monitor  
HYP : ዛሬ   አፍትኑን       ላይ   ሎወር     አብዶሚኔ      ታይት     እያደረገ   ፍሪኩዌንት     ክራምፕስ    ይሰማኛል   ላይክ    ፒርድ      ፔይን    ኢንተርቫሉ      ግን   ሬጉላር      አይደለም   ዚዝ    አር      ጀስት   ብራክስ   ኤንድ       ሂክስ     ኮንትራክሽንስ       ኦር    ኤርሊ     ሌበር     ሳይንስ    መሆናቸውን   ዲስቲንጉሽ        ማድረግ   አልቻልኩም   ዋት     አዘር     ዋንንግ      ሳይንስ    ሹድ       አይ    ሞኒተር     
EVAL: ✓    SUB         ✓    SUB     SUB        SUB     ✓       SUB        SUB      ✓       SUB    SUB      SUB    SUB         ✓    SUB       ✓       INS   SUB     SUB   SUB    SUB       SUB     SUB            SUB   SUB     SUB     SUB     ✓        SUB           ✓      ✓        SUB    SUB     SUB       SUB     SUB      SUB   SUB      
```

#### Gemini
- **Latency**: 10.09s | **Ref Words**: 38 | **Errors**: 5 (S: 3, D: 0, I: 2)
- **WER**: **13.2%** | **Word Accuracy**: **86.8%** | **CER**: 3.4%

```text
REF : ዛሬ   afternoon   ላይ   lower   ---       abdomenኔ   tight   እያደረገ    frequent   cramps   ይሰማኛል   like   period   pain   ---        intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
HYP : ዛሬ   afternoon   ላይ   lower   abdomen   ኤን         tight   የሚያደርግ   frequent   cramps   ይሰማኛል   like   period   pain   interval   ኡ           ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
EVAL: ✓    ✓           ✓    ✓       INS       SUB        ✓       SUB      ✓          ✓        ✓       ✓      ✓        ✓      INS        SUB         ✓    ✓         ✓       ✓       ✓     ✓      ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓             ✓      ✓        ✓      ✓       ✓         ✓       ✓        ✓    ✓        
```

---

### Voice: `v29.wav`
> **Ground Truth Reference**:
> *አዎ ወስጃለሁ፣ daily IFA ኪኒኑን ጠዋት ላይ with freshly squeezed orange juice ነው የወሰድኩት፣ iron absorptionኑን ይጨምራል ብለውኝ። calciumሙን ግን yesterday ማታ ወስጄዋለሁ፤ ዛሬም after dinner እወስደዋለሁ። እስካሁን ምንም stomach pain አልተሰማኝም፣ perfectly fine ነኝ።*

#### Sahara
- **Latency**: 5.6s | **Ref Words**: 35 | **Errors**: 16 (S: 11, D: 4, I: 1)
- **WER**: **45.7%** | **Word Accuracy**: **54.3%** | **CER**: 30.5%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   ---   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ   
HYP : አዎ   ወስጃለው   daily   አይፋ   ኪኒኑን   ጠዋት   ላይ   with   fresh     squezed    orrang   just    ነው   የወሰድኩት   ---    አይራብስንውን       ይጨምራል   ብለውኝ   ካልሲያሙን      ግን   የ     sturday     ማታ   ወስጄዋለሁ   ዛሬም   after   diner    ወስደዋለሁ    እስካሁን   ምንም   stomach   pain   አልተሰማኝም   ---         ---    ---  
EVAL: ✓    SUB     ✓       SUB   ✓      ✓     ✓    ✓      SUB       SUB        SUB      SUB     ✓    ✓        DEL    SUB            ✓       ✓      SUB         ✓    INS   SUB         ✓    ✓        ✓     ✓       SUB      SUB       ✓       ✓     ✓         ✓      ✓         DEL         DEL    DEL  
```

#### Addis Ai
- **Latency**: 6.2s | **Ref Words**: 35 | **Errors**: 20 (S: 18, D: 2, I: 0)
- **WER**: **57.1%** | **Word Accuracy**: **42.9%** | **CER**: 61.6%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine    ነኝ   
HYP : አዎ   ወስጃለሁ   ዴሊ      አይፋ   ኪኒኑን   ጠዋት   ላይ   ዊዝ     ፍሬሽ       ስኩዝ        ኦረንጅ     ጁስ      ነው   የወሰድኩት   ---    አይራብዞብሰንኑን     ይጨምራል   ብለውኝ   ካልሲያሙን      ግን   የስተርዴይ      ማታ   ወስጄዋለሁ   ዛሬም   አፍተ     ዲነር      ወስደዋለሁ    እስካሁን   ምንም   ---       ስቶማክ   በእነርሱ     አማኝ         በእነርሱ   አማኝ  
EVAL: ✓    ✓       SUB     SUB   ✓      ✓     ✓    SUB    SUB       SUB        SUB      SUB     ✓    ✓        DEL    SUB            ✓       ✓      SUB         ✓    SUB         ✓    ✓        ✓     SUB     SUB      SUB       ✓       ✓     DEL       SUB    SUB       SUB         SUB     SUB  
```

#### Gemini
- **Latency**: 45.97s | **Ref Words**: 35 | **Errors**: 13 (S: 6, D: 7, I: 0)
- **WER**: **37.1%** | **Word Accuracy**: **62.9%** | **CER**: 30.5%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ   
HYP : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን   ጧት    ላይ   with   fresh     squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኡን   ይጨምራል   ብለውኝ   ካልሲየም       ግን   yesterday   ማታ   ወስጃለሁ    ዛሬም   after   dinner   እወስደዋለሁ   ---     ---   ---       ---    ---       ---         ---    እስካ  
EVAL: ✓    ✓       ✓       ✓     ✓      SUB   ✓    ✓      SUB       ✓          ✓        ✓       ✓    ✓        ✓      SUB            ✓       ✓      SUB         ✓    ✓           ✓    SUB      ✓     ✓       ✓        ✓         DEL     DEL   DEL       DEL    DEL       DEL         DEL    SUB  
```

---

### Voice: `v30.wav`
> **Ground Truth Reference**:
> *ምንም serious pain የለብኝም ግን the heartburn እና acid reflux በጣም severe ሆኗል። night time ላይ sleep መተኛት አልቻልኩም፤ two pillows አድርጌ እንኳን burning sensation ይኖረዋል። safe የሆነ antacid syrup ወይም medication ከመድሃኒት ቤት መግዛት እችላለሁ ወይስ prescription ያስፈልጋል?*

#### Sahara
- **Latency**: 21.35s | **Ref Words**: 39 | **Errors**: 11 (S: 5, D: 5, I: 1)
- **WER**: **28.2%** | **Word Accuracy**: **71.8%** | **CER**: 10.4%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   ---     heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time        ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup       ወይም     medication   ከመድሃኒት   ቤት    መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   serious   pain   የለብኝም   ግን   the   heart   burn        እና   acid   reflux   በጣም   severe   ሆኗል   ---     nighttime   ላይ   sleep   መተኛት   አልቻልኩም   ---   twos      አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   ---       anteracid   syrop   medication   ከመድሃኒት   ---   መግዛት   እችላለሁ   ወይስ   prescription   ---     
EVAL: ✓     ✓         ✓      ✓       ✓    ✓     INS     SUB         ✓    ✓      ✓        ✓     ✓        ✓     DEL     SUB         ✓    ✓       ✓      ✓        DEL   SUB       ✓      ✓      ✓         ✓           ✓       ✓      ✓     DEL       SUB         SUB     ✓            ✓        DEL   ✓      ✓       ✓     ✓              DEL     
```

#### Addis Ai
- **Latency**: 5.22s | **Ref Words**: 39 | **Errors**: 23 (S: 20, D: 1, I: 2)
- **WER**: **59.0%** | **Word Accuracy**: **41.0%** | **CER**: 64.1%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the    heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   ---   ---   prescription   ያስፈልጋል  
HYP : ምንም   ሲሪየስ      ፔን     የለብኝም   ግን   ዘሃርት   በርን         እና   አሲድ    ሪፍሉክስ    በጣም   ሲቪር      ሆኗል   ናይት     ታይም    ላይ   ስሊፕ     መተኛት   አልቻልኩም   ---   ቱፕሎዝ      አድርጌ   እንኳን   በርኒንግ     ሰንሴሽን       ይኖረዋል   ሴፍ     የሆነ   አንታሲድ     ሲሮፕ     ወይም   ሜዲኬሽን        ከመድሃኒት   ቤት   መግዛት   እችላለው   ወይስ   እስኪ   እስኪ   እስኪ            እስኪ     
EVAL: ✓     SUB       SUB    ✓       ✓    SUB    SUB         ✓    SUB    SUB      ✓     SUB      ✓     SUB     SUB    ✓    SUB     ✓      ✓        DEL   SUB       ✓      ✓      SUB       SUB         ✓       SUB    ✓     SUB       SUB     ✓     SUB          ✓        ✓    ✓      SUB     ✓     INS   INS   SUB            SUB     
```

#### Gemini
- **Latency**: 11.1s | **Ref Words**: 39 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **5.1%** | **Word Accuracy**: **94.9%** | **CER**: 2.1%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   serious   pain   የለብኝም   ግን   ---   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድኃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
EVAL: ✓     ✓         ✓      ✓       ✓    DEL   ✓           ✓    ✓      ✓        ✓     ✓        ✓     ✓       ✓      ✓    ✓       ✓      ✓        ✓     ✓         ✓      ✓      ✓         ✓           ✓       ✓      ✓     ✓         ✓       ✓     ✓            SUB      ✓    ✓      ✓       ✓     ✓              ✓       
```

---

### Voice: `v31.wav`
> **Ground Truth Reference**:
> *አዎ ዛሬ morning ላይ ከ breakfast በኋላ the iron and folic acid tablet ወስጃለሁ። ግን calcium tabletቱን ማታ ከመተኛቴ በፊት ነው የምወስደው፤ ምክንያቱም simultaneously ከወሰድኳቸው severe nausea እና mild constipation ይፈጥርብኛል። doctorሩም separate አድርጌ እንድወስድ ነግሮኛል፣ so far strictly scheduleሩን እየተከተልኩ ነው።*

#### Sahara
- **Latency**: 6.44s | **Ref Words**: 42 | **Errors**: 16 (S: 10, D: 6, I: 0)
- **WER**: **38.1%** | **Word Accuracy**: **61.9%** | **CER**: 28.0%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and        folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so    far   strictly   scheduleሩን   እየተከተልኩ   ነው    
HYP : አዎ   ዛሬ   morning   ላይ   ከ    ---         ---   ---   ---    breakfal   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tableቱን    ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   ሲመልቴ             ከወሰድኳቸው   severe   naze     እና   mild   constipation   ይፈጥርብኛል   doctor     supprite   አድርጌ   እንዲወስድ   ነግሮኛል   ---   ሶፋር   strictly   ---          እስከ       ዱዋሩን  
EVAL: ✓    ✓    ✓         ✓    ✓    DEL         DEL   DEL   DEL    SUB        ✓       ✓      ✓        ✓       ✓    ✓         SUB        ✓    ✓       ✓     ✓    ✓        ✓        SUB              ✓         ✓        SUB      ✓    ✓      ✓              ✓         SUB        SUB        ✓      SUB      ✓       DEL   SUB   ✓          DEL          SUB       SUB   
```

#### Addis Ai
- **Latency**: 5.89s | **Ref Words**: 42 | **Errors**: 23 (S: 20, D: 2, I: 1)
- **WER**: **54.8%** | **Word Accuracy**: **45.2%** | **CER**: 61.0%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ     breakfast   በኋላ   the   iron   and    folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   ---   so    far      strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   ሞኒንግ      ላይ   ---   ከብሬክፈስት     በኋላ   ---   ዲ      አይረን   ፎሊክ     አሲድ    ታብሌት     ወስጃለሁ   ግን   ካልሲየም     ታብሌቱን      ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   ሲማልቴኒሲ           ከወሰድኳቸው   ስቪየር     ናዚያ      እና   ማይልድ   ኮንስቲፔሽን        ይፈጥርብኛል   ዶክተሩ       ሰፕራይዝ      አድርጌ   እንድወስድ   ነግሮኛል   ሶ     ፋር    ስትሪክትሊ   እስከ        ድዋሩም         እየተከተልኩ   ነው  
EVAL: ✓    ✓    SUB       ✓    DEL   SUB         ✓     DEL   SUB    SUB    SUB     SUB    SUB      ✓       ✓    SUB       SUB        ✓    ✓       ✓     ✓    ✓        ✓        SUB              ✓         SUB      SUB      ✓    SUB    SUB            ✓         SUB        SUB        ✓      ✓        ✓       INS   SUB   SUB      SUB        SUB          ✓         ✓   
```

#### Gemini
- **Latency**: 9.78s | **Ref Words**: 42 | **Errors**: 6 (S: 5, D: 1, I: 0)
- **WER**: **14.3%** | **Word Accuracy**: **85.7%** | **CER**: 7.3%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate     አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   የ     iron   ---   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወስድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   ዶክተሩም      separately   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleኡን   እየተከተልኩ   ነው  
EVAL: ✓    ✓    ✓         ✓    ✓    ✓           ✓     SUB   ✓      DEL   ✓       ✓      ✓        ✓       ✓    ✓         ✓          ✓    ✓       ✓     ✓    ✓        ✓        ✓                SUB       ✓        ✓        ✓    ✓      ✓              ✓         SUB        SUB          ✓      ✓        ✓       ✓    ✓     ✓          SUB          ✓         ✓   
```

---

### Voice: `v32.wav`
> **Ground Truth Reference**:
> *ዛሬ morning ጀምሮ the fetal kick በጣም decrease አድርጓል። normally after breakfast very active ነበር የሚሆነው፤ ዛሬ ግን hardly any movement ተሰማኝ። cold juice ጠጥቼ ቆይቻለሁ ግን still quiet ነው። please hospital emergency triage መሄድ አለብኝ ወይስ ትንሽ ልጠብቅ?*

#### Sahara
- **Latency**: 3.78s | **Ref Words**: 39 | **Errors**: 8 (S: 7, D: 1, I: 0)
- **WER**: **20.5%** | **Word Accuracy**: **79.5%** | **CER**: 8.2%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal     kick    በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   ---   defitel   chick   በጣም   decrease   አድርጓል   normally   after   breakft     very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   coal   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quaet   ነው   please   hospital   emergency   treage   መሄድ   አለብኝ   ወይስ   ትንሽ   ል     
EVAL: ✓    ✓         ✓     DEL   SUB       SUB     ✓     ✓          ✓       ✓          ✓       SUB         ✓      ✓        ✓     ✓       ✓    ✓    ✓        ✓     ✓          ✓      SUB    ✓       ✓     ✓       ✓    ✓       SUB     ✓    ✓        ✓          ✓           SUB      ✓     ✓      ✓     ✓     SUB   
```

#### Addis Ai
- **Latency**: 5.02s | **Ref Words**: 39 | **Errors**: 22 (S: 20, D: 1, I: 1)
- **WER**: **56.4%** | **Word Accuracy**: **43.6%** | **CER**: 69.8%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ   ---  
HYP : ዛሬ   ሞኒንግ      ጀምሮ   ---   ደፊተል    ቺክ     በጣም   ዲክሪስ       አድርጓል   ኖርማሊ       አፍተር    ብሬክፈስት      ቬሪ     አክቲቭ     ነበር   የሚሆነው   ዛሬ   ግን   ሃድሊ      ኤኒ    ሙቭመንት      ተሰማኝ   ኮል     ጁስ      ጠጥቼ   ቆይቻለሁ   ግን   ስቲል     ኳየት     ነው   ፕሊዝ      ሆስፒታል      ኢመርጀንሲ      ትሪያጅ     መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ   በብቁ  
EVAL: ✓    SUB       ✓     DEL   SUB     SUB    ✓     SUB        ✓       SUB        SUB     SUB         SUB    SUB      ✓     ✓       ✓    ✓    SUB      SUB   SUB        ✓      SUB    SUB     ✓     ✓       ✓    SUB     SUB     ✓    SUB      SUB        SUB         SUB      ✓     ✓      ✓     ✓     ✓      INS  
```

#### Gemini
- **Latency**: 7.73s | **Ref Words**: 39 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **5.1%** | **Word Accuracy**: **94.9%** | **CER**: 2.2%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   ---   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠበቅ  
EVAL: ✓    ✓         ✓     DEL   ✓       ✓      ✓     ✓          ✓       ✓          ✓       ✓           ✓      ✓        ✓     ✓       ✓    ✓    ✓        ✓     ✓          ✓      ✓      ✓       ✓     ✓       ✓    ✓       ✓       ✓    ✓        ✓          ✓           ✓        ✓     ✓      ✓     ✓     SUB   
```

---

### Voice: `v33.wav`
> **Ground Truth Reference**:
> *ዛሬ lower back pain እና pelvic pressure በጣም ይሰማኛል፣ especially ስራ ላይ standing for a long time ስሆን unbearable ይሆናል። fetal movement ግን active ነው፣ baby normal kick እያደረገ ነው። ይሄ normal third-trimester symptom ነው ወይስ doctorሩን emergency ማናገር አለብኝ?*

#### Sahara
- **Latency**: 3.88s | **Ref Words**: 41 | **Errors**: 10 (S: 5, D: 4, I: 1)
- **WER**: **24.4%** | **Word Accuracy**: **75.6%** | **CER**: 16.1%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom              ነው   ወይስ   ---   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ሲሆን   አምበረቦ        ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   cick   እያደረገ   ነው   ይሄ   ---      ---     ---         normaltrimestyment   ነው   ወይስ   የ     doctor     emergency   ማናገር   ---   
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            ✓    ✓    ✓          ✓     ✓    ✓      ✓      SUB   SUB          ✓      ✓       ✓          ✓    ✓        ✓    ✓      ✓        SUB    ✓       ✓    ✓    DEL      DEL     DEL         SUB                  ✓    ✓     INS   SUB        ✓           ✓      DEL   
```

#### Addis Ai
- **Latency**: 5.63s | **Ref Words**: 41 | **Errors**: 27 (S: 24, D: 2, I: 1)
- **WER**: **65.8%** | **Word Accuracy**: **34.2%** | **CER**: 76.7%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for      a     long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   ---   አለብኝ  
HYP : ዛሬ   ሎወር     ባክ     ፔይን    እና   ፐርቪክ     ፕሬሸር       በጣም   ይሰማኛል   ስፔሻሊ         ስራ   ላይ   ---        ስታንዲንግ   ፎር    ሎንግ    ታይም    ሲሆን   አንበረቦ        ይሆናል   ፊትል     ሙቭመንት      ግን   አክቲቭ     ነው   ቤቢ     ኖርማል     ኪክ     እያደረገ   ነው   ይሄ   ---      ኖርማል    ትራይምስተር     ስንተም      ነው   ወይስ   የዶክተሩን     ኢመርጀንሲ      ማናገር   አንድ   ነጥብ   
EVAL: ✓    SUB     SUB    SUB    ✓    SUB      SUB        ✓     ✓       SUB          ✓    ✓    DEL        SUB      SUB   SUB    SUB    SUB   SUB          ✓      SUB     SUB        ✓    SUB      ✓    SUB    SUB      SUB    ✓       ✓    ✓    DEL      SUB     SUB         SUB       ✓    ✓     SUB        SUB         ✓      INS   SUB   
```

#### Gemini
- **Latency**: 40.98s | **Ref Words**: 41 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **12.2%** | **Word Accuracy**: **87.8%** | **CER**: 10.4%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ    ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ    normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ሥራ    ላይ   standing   for   a    long   time   ሲሆን   አምበልቦ        ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይህ    normal   third   trimester   symptom   ነው   ወይስ   ዶክተሬን      emergency   ማናገር   አለብኝ  
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            SUB   ✓    ✓          ✓     ✓    ✓      ✓      SUB   SUB          ✓      ✓       ✓          ✓    ✓        ✓    ✓      ✓        ✓      ✓       ✓    SUB   ✓        ✓       ✓           ✓         ✓    ✓     SUB        ✓           ✓      ✓     
```

---

### Voice: `v34.wav`
> **Ground Truth Reference**:
> *ዛሬ taken አድርጌያለሁ፣ but yesterday ሙሉ ቀን ስራ ስለነበርኩ the calcium supplementቱን መውሰድ forget አድርጌ ነበር። ዛሬ double dose መውሰድ አለብኝ ወይስ just continue with one tablet? IFAውን ግን today as usual ጠዋት ወስጃለሁ፣ no complications።*

#### Sahara
- **Latency**: 2.33s | **Ref Words**: 36 | **Errors**: 6 (S: 4, D: 2, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 16.8%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
HYP : ዛሬ   taken   አድርጌያለሁ   ---   ---         ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplement     መውሰድ   ፈጌት      አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   አይፋውን   ግን   ትዴ      as   usual   ጠዋት   ወስጃለሁ   no   complications  
EVAL: ✓    ✓       ✓         DEL   DEL         ✓    ✓    ✓    ✓        ✓     ✓         SUB            ✓      SUB      ✓      ✓     ✓    ✓        ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        SUB     ✓    SUB     ✓    ✓       ✓     ✓       ✓    ✓              
```

#### Addis Ai
- **Latency**: 5.53s | **Ref Words**: 36 | **Errors**: 21 (S: 20, D: 0, I: 1)
- **WER**: **58.3%** | **Word Accuracy**: **41.7%** | **CER**: 64.7%

```text
REF : ዛሬ   taken   አድርጌያለሁ   ---   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as    usual   ጠዋት   ወስጃለሁ   no    complications  
HYP : ዛሬ   ቴክን     አድርጌያለሁ   በት    ጀስት   ዴይ          ሙሉ   ቀን   ስራ   ስለነበርኩ   ደካል   ሲያም       ሳፕልመንቱን        መውሰድ   ፈጌጥ      አድርጌ   ነበር   ዛሬ   ደብል      ዶስ     መውሰድ   አለብኝ   ወይስ   ጀስት    ኮንቲኒው      ዊዝ     ዋን    ታብሌት     አይፋውን   ግን   ትዴይ     አዝ    ዩዙዋል    ጠዋት   ወስጃለሁ   ኖ     ካምፕሊኬሽንስ       
EVAL: ✓    SUB     ✓         INS   SUB   SUB         ✓    ✓    ✓    ✓        SUB   SUB       SUB            ✓      SUB      ✓      ✓     ✓    SUB      SUB    ✓      ✓      ✓     SUB    SUB        SUB    SUB   SUB      SUB     ✓    SUB     SUB   SUB     ✓     ✓       SUB   SUB            
```

#### Gemini
- **Latency**: 10.03s | **Ref Words**: 36 | **Errors**: 4 (S: 3, D: 0, I: 1)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 4.8%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ---   ifaውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ    no   complications  
HYP : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   የ     calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   i     fine    ግን   today   as   usual   ጠዋት   ወስጄያለሁ   no   complications  
EVAL: ✓    ✓       ✓         ✓     ✓           ✓    ✓    ✓    ✓        SUB   ✓         ✓              ✓      ✓        ✓      ✓     ✓    ✓        ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        INS   SUB     ✓    ✓       ✓    ✓       ✓     SUB      ✓    ✓              
```

---

### Voice: `v35.wav`
> **Ground Truth Reference**:
> *ዛሬማ ገና አልወሰድኩም እኮ። ጠዋት morning sicknessሱ በጣም አስቸግሮኝ vomit ሳደርግ ነው የረፈደው፤ empty stomach መውሰድ አልቻልኩም። አሁን after lunch ትንሽ ሻል ሲለኝ the daily IFA supplementቱን ከብዙ water ጋር እወስደዋለሁ። calcium ደሞ አብሬ ልውሰደው ወይስ gap ልስጠው?*

#### Sahara
- **Latency**: 3.73s | **Ref Words**: 38 | **Errors**: 16 (S: 12, D: 4, I: 0)
- **WER**: **42.1%** | **Word Accuracy**: **57.9%** | **CER**: 24.4%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit    ሳደርግ   ነው   የረፈደው   empty   stomach    መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል    ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር    እወስደዋለሁ   calcium   ደሞ    አብሬ    ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   ሲነሱ         በጣም   አስቸግሮኝ   vommit   ሳደርግ   ነው   የረፈደው   ---     emtistac   መውሰድ   አልቻልኩም   አሁን   after   lench   ትንሽ   አል    ሲለኝ   the   daily   if    supplement     ከብዙ   ---     ዋጋ    እወስደዋለሁ   ካልሲየም     ደግሞ   አብሬን   ውሰደው    ወይስ   ---   ---   
EVAL: ✓     ✓    ✓         ✓    ✓     ✓         SUB         ✓     ✓        SUB      ✓      ✓    ✓       DEL     SUB        ✓      ✓        ✓     ✓       SUB     ✓     SUB   ✓     ✓     ✓       SUB   SUB            ✓     DEL     SUB   ✓         SUB       SUB   SUB    SUB     ✓     DEL   DEL   
```

#### Addis Ai
- **Latency**: 4.86s | **Ref Words**: 38 | **Errors**: 23 (S: 18, D: 2, I: 3)
- **WER**: **60.5%** | **Word Accuracy**: **39.5%** | **CER**: 58.3%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   ---    ---    ---    vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ    ልውሰደው   ወይስ   gap    ልስጠው   
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   ሞኒንግ      ሲክንሱ        በጣም   አስቸግሮኝ   0xe1   0x89   0xae   ሚት      ሳደርግ   ነው   የረፈደው   ---     እምቲስተማክ   መውሰድ   አልቻልኩም   አሁን   አፍተር    ለንች     ትንሽ   ሻል   ሲለኝ   ---   ዘዴሊ     አይፍ   ሳፕልማንቱን        ከብዙ   ዋታ      ጋር   ወስደዋለሁ    ካልሲየም     ደግሞ   አብሬል   ውስጥ     ያለው   ይስቃል   እስካሁን  
EVAL: ✓     ✓    ✓         ✓    ✓     SUB       SUB         ✓     ✓        INS    INS    INS    SUB     ✓      ✓    ✓       DEL     SUB       ✓      ✓        ✓     SUB     SUB     ✓     ✓    ✓     DEL   SUB     SUB   SUB            ✓     SUB     ✓    SUB       SUB       SUB   SUB    SUB     SUB   SUB    SUB    
```

#### Gemini
- **Latency**: 12.49s | **Ref Words**: 38 | **Errors**: 7 (S: 6, D: 1, I: 0)
- **WER**: **18.4%** | **Word Accuracy**: **81.6%** | **CER**: 4.8%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily    ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessኡ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   ---   የdaily   if    supplementኡን   ከብዙ   water   ጋር   ወስደዋለሁ    calcium   ደግሞ   አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
EVAL: ✓     ✓    ✓         ✓    ✓     ✓         SUB         ✓     ✓        ✓       ✓      ✓    ✓       ✓       ✓         ✓      ✓        ✓     ✓       ✓       ✓     ✓    ✓     DEL   SUB      SUB   SUB            ✓     ✓       ✓    SUB       ✓         SUB   ✓     ✓       ✓     ✓     ✓     
```

---

### Voice: `v36.wav`
> **Ground Truth Reference**:
> *እግሬ በጣም እያበጠ ነው፤ today both feet ላይ severe swelling አለ፣ ጫማዬም አልገባ ብሎኛል። ከዚህም በተጨማሪ mild headache አለኝ። BPዬ high ሆኖ እንዳይሆን ፈርቻለሁ፤ nearby clinic ሄጄ blood pressure check ማድረግ አለብኝ ወይስ tomorrow morning መምጣት ይሻላል?*

#### Sahara
- **Latency**: 4.14s | **Ref Words**: 37 | **Errors**: 13 (S: 5, D: 8, I: 0)
- **WER**: **35.1%** | **Word Accuracy**: **64.9%** | **CER**: 30.3%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ    እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ    blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   today   ቦት     ፊት     ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   ---   ---    ---   ---      ---     bp       clinic   ---   hegad   pressure   check   ማድረግ   አለብኝ   ---   ወይስሞሮ      morning   መምጣት   ---   
EVAL: ✓     ✓     ✓      ✓    ✓       SUB    SUB    ✓    ✓        ✓          ✓    ✓      ✓      ✓      ✓      ✓       ✓      ✓          ✓     DEL   DEL    DEL   DEL      DEL     SUB      ✓        DEL   SUB     ✓          ✓       ✓      ✓      DEL   SUB        ✓         ✓      DEL   
```

#### Addis Ai
- **Latency**: 7.01s | **Ref Words**: 37 | **Errors**: 18 (S: 18, D: 0, I: 0)
- **WER**: **48.6%** | **Word Accuracy**: **51.3%** | **CER**: 57.6%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ    blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   ቱደይ     ቦት     ፊት     ላይ   ሲቪር      ስወሊንግ      አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   ማይልድ   ሄዴክ        አለኝ   ዲፒኤ   ሃይ     ሆኖ   እንዳይሆን   ፈርቻለሁ   ኒርባይ     ክሊኒክ     ሄጅ    ብላድ     ፕሬሽር       ቼክ      ማድረግ   አለብኝ   ወይስ   ትሞሮ        ሞኒንግ      መምጣት   እንሻላ  
EVAL: ✓     ✓     ✓      ✓    SUB     SUB    SUB    ✓    SUB      SUB        ✓    ✓      ✓      ✓      ✓      ✓       SUB    SUB        ✓     SUB   SUB    ✓    ✓        ✓       SUB      SUB      SUB   SUB     SUB        SUB     ✓      ✓      ✓     SUB        SUB       ✓      SUB   
```

#### Gemini
- **Latency**: 37.18s | **Ref Words**: 37 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **2.7%** | **Word Accuracy**: **97.3%** | **CER**: 0.6%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚያም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
EVAL: ✓     ✓     ✓      ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓    ✓      ✓      ✓      SUB    ✓       ✓      ✓          ✓     ✓     ✓      ✓    ✓        ✓       ✓        ✓        ✓    ✓       ✓          ✓       ✓      ✓      ✓     ✓          ✓         ✓      ✓     
```

---

### Voice: `v37.wav`
> **Ground Truth Reference**:
> *እኔ የ folic acid እና iron supplementቱን correctly ወስጃለሁ፣ ምንም side effect የለብኝም። ግን the calcium tablets አልቀውብኛል፤ ባለፈው clinic ስሄድ pharmacy ውስጥ out of stock ነበር ያሉት። ዛሬ private pharmacy ፈልጌ መግዛት አለብኝ ወይስ next appointment ድረስ መጠበቅ እችላለሁ?*

#### Sahara
- **Latency**: 4.83s | **Ref Words**: 40 | **Errors**: 5 (S: 4, D: 1, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 6.5%

```text
REF : እኔ   የ    folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplimant     correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   ---   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   phamacy    ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   phamacy    ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   ይችላል   
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      SUB            ✓           ✓       ✓     ✓      ✓        ✓       ✓    DEL   ✓         ✓         ✓         ✓      ✓        ✓     SUB        ✓     ✓     ✓    ✓       ✓     ✓     ✓    ✓         SUB        ✓     ✓      ✓      ✓     ✓      ✓             ✓     ✓      SUB    
```

#### Addis Ai
- **Latency**: 6.34s | **Ref Words**: 40 | **Errors**: 22 (S: 18, D: 4, I: 0)
- **WER**: **55.0%** | **Word Accuracy**: **45.0%** | **CER**: 62.9%

```text
REF : እኔ   የ     folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of    stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   ---   የፎሊክ    አሲድ    እና   አይሮን   ስፕሪማንቱን        ካሬክትሊ       ወስጃለሁ   ምንም   ሳይድ    ኢፌክት     የለብኝም   ግን   ዘ     ካልሲየም     ታብሌት      አልቀውብኛል   ባለፈው   ክሊኒክ     ስሄድ   ፋርማሲ       ውስጥ   አውት   ኦፍ    ስቶክ     ነበር   ያሉት   ዛሬ   ፕራይቬት     ፋርማሲ       ፈልጌ   መግዛት   አለብኝ   ---   ---    ---           ወይ    መጠበቅ   እችላለሁ  
EVAL: ✓    DEL   SUB     SUB    ✓    SUB    SUB            SUB         ✓       ✓     SUB    SUB      ✓       ✓    SUB   SUB       SUB       ✓         ✓      SUB      ✓     SUB        ✓     SUB   SUB   SUB     ✓     ✓     ✓    SUB       SUB        ✓     ✓      ✓      DEL   DEL    DEL           SUB   ✓      ✓      
```

#### Gemini
- **Latency**: 33.08s | **Ref Words**: 40 | **Errors**: 4 (S: 3, D: 0, I: 1)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 2.7%

```text
REF : እኔ   የ    folic   acid   እና   iron   ---          supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplement   ቱን             correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   የ     calcium   tablets   አልቆብኛል    ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      INS          SUB            ✓           ✓       ✓     ✓      ✓        ✓       ✓    SUB   ✓         ✓         SUB       ✓      ✓        ✓     ✓          ✓     ✓     ✓    ✓       ✓     ✓     ✓    ✓         ✓          ✓     ✓      ✓      ✓     ✓      ✓             ✓     ✓      ✓      
```

---

### Voice: `v38.wav`
> **Ground Truth Reference**:
> *ዛሬ afternoon ላይ lower abdomenኔ tight እያደረገ frequent cramps ይሰማኛል፣ like period pain። intervalሉ ግን regular አይደለም። these are just Braxton Hicks contractions or early labor signs መሆናቸውን distinguish ማድረግ አልቻልኩም። what other warning signs should I monitor?*

#### Sahara
- **Latency**: 5.58s | **Ref Words**: 38 | **Errors**: 9 (S: 8, D: 1, I: 0)
- **WER**: **23.7%** | **Word Accuracy**: **76.3%** | **CER**: 10.6%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight          እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs     መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs     should   i    monitor  
HYP : ዛሬ   afternoon   ላይ   ---     low        abdomination   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalu   ግን   regular   አይደለም   these   are   just   bruxton   hex     contractions   or   early   labor   science   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   ather   warning   science   should   i    monitor  
EVAL: ✓    ✓           ✓    DEL     SUB        SUB            ✓       ✓          ✓        ✓       ✓      ✓        ✓      SUB         ✓    ✓         ✓       ✓       ✓     ✓      SUB       SUB     ✓              ✓    ✓       ✓       SUB       ✓        ✓             ✓      ✓        ✓      SUB     ✓         SUB       ✓        ✓    ✓        
```

#### Addis Ai
- **Latency**: 5.68s | **Ref Words**: 38 | **Errors**: 29 (S: 29, D: 0, I: 0)
- **WER**: **76.3%** | **Word Accuracy**: **23.7%** | **CER**: 81.2%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or    early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i     monitor  
HYP : ዛሬ   አፍትኑን       ላይ   ሎወር     አብዶሚኔ      ታይት     እያደረገ   ፍሪኮንት      ክራምፕስ    ይሰማኛል   ላይክ    ፒሪዮድ     ፔይን    ኢንተርቫሉ      ግን   ሬጉላር      አይደለም   ዚዝ      አር    ጀስት    ብራክስተን    ሄክስ     ኮንትራክሽንስ       ኦር    ኤርሊ     ሌበር     ሳይንስ    መሆናቸውን   ዲስቲንጉሽ        ማድረግ   አልቻልኩም   ዋት     አዘር     ዋርኒንግ     ሳይንስ    ሹድ       አይ    ሞኒተር     
EVAL: ✓    SUB         ✓    SUB     SUB        SUB     ✓       SUB        SUB      ✓       SUB    SUB      SUB    SUB         ✓    SUB       ✓       SUB     SUB   SUB    SUB       SUB     SUB            SUB   SUB     SUB     SUB     ✓        SUB           ✓      ✓        SUB    SUB     SUB       SUB     SUB      SUB   SUB      
```

#### Gemini
- **Latency**: 21.4s | **Ref Words**: 38 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **10.5%** | **Word Accuracy**: **89.5%** | **CER**: 11.1%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
HYP : ዛሬ   አፍተርኑን      ላይ   lower   abdomen    ታይት     እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   ኢንተርቫሉ      ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
EVAL: ✓    SUB         ✓    ✓       SUB        SUB     ✓       ✓          ✓        ✓       ✓      ✓        ✓      SUB         ✓    ✓         ✓       ✓       ✓     ✓      ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓             ✓      ✓        ✓      ✓       ✓         ✓       ✓        ✓    ✓        
```

---

### Voice: `v39.wav`
> **Ground Truth Reference**:
> *አዎ ወስጃለሁ፣ daily IFA ኪኒኑን ጠዋት ላይ with freshly squeezed orange juice ነው የወሰድኩት፣ iron absorptionኑን ይጨምራል ብለውኝ። calciumሙን ግን yesterday ማታ ወስጄዋለሁ፤ ዛሬም after dinner እወስደዋለሁ። እስካሁን ምንም stomach pain አልተሰማኝም፣ perfectly fine ነኝ።*

#### Sahara
- **Latency**: 3.94s | **Ref Words**: 35 | **Errors**: 9 (S: 9, D: 0, I: 0)
- **WER**: **25.7%** | **Word Accuracy**: **74.3%** | **CER**: 18.1%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
HYP : አዎ   ወስጃለው   daily   አይፋ   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orrang   just    ነው   የወሰድኩት   iron   absorbeኑን      ይጨምራል   ብለውኝ   ካልሲያሙን      ግን   የስቴ         ማታ   ወስጄዋለሁ   ዛሬም   after   diner    ወስደዋለሁ    እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
EVAL: ✓    SUB     ✓       SUB   ✓      ✓     ✓    ✓      ✓         ✓          SUB      SUB     ✓    ✓        ✓      SUB            ✓       ✓      SUB         ✓    SUB         ✓    ✓        ✓     ✓       SUB      SUB       ✓       ✓     ✓         ✓      ✓         ✓           ✓      ✓   
```

#### Addis Ai
- **Latency**: 5.28s | **Ref Words**: 35 | **Errors**: 18 (S: 17, D: 1, I: 0)
- **WER**: **51.4%** | **Word Accuracy**: **48.6%** | **CER**: 58.8%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain     አልተሰማኝም   perfectly   fine   ነኝ  
HYP : አዎ   ወስጃለሁ   ዴሊ      አይፋ   ኪኒኑን   ጠዋት   ላይ   ዊት     ፍሬሽሊ      ስኩዊዝድ      ኦረንጅ     ጁስ      ነው   የወሰድኩት   አይሮን   አብዞብሰኑን        ይጨምራል   ብለውኝ   ካልሲያሙን      ግን   የስተዴ        ማታ   ወስጄዋለሁ   ዛሬም   አፍተ     ዲነር      ወስደዋለሁ    እስካሁን   ምንም   ---       ስተማክፔን   አልተሰማኝም   ፐርፌክሊ       ፋይን    ነኝ  
EVAL: ✓    ✓       SUB     SUB   ✓      ✓     ✓    SUB    SUB       SUB        SUB      SUB     ✓    ✓        SUB    SUB            ✓       ✓      SUB         ✓    SUB         ✓    ✓        ✓     SUB     SUB      SUB       ✓       ✓     DEL       SUB      ✓         SUB         SUB    ✓   
```

#### Gemini
- **Latency**: 21.1s | **Ref Words**: 35 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **8.6%** | **Word Accuracy**: **91.4%** | **CER**: 5.7%

```text
REF : አዎ    ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
HYP : ---   ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   ካልሲየሙን      ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬ    after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
EVAL: DEL   ✓       ✓       ✓     ✓      ✓     ✓    ✓      ✓         ✓          ✓        ✓       ✓    ✓        ✓      ✓              ✓       ✓      SUB         ✓    ✓           ✓    ✓        SUB   ✓       ✓        ✓         ✓       ✓     ✓         ✓      ✓         ✓           ✓      ✓   
```

---

### Voice: `v40.wav`
> **Ground Truth Reference**:
> *ምንም serious pain የለብኝም ግን the heartburn እና acid reflux በጣም severe ሆኗል። night time ላይ sleep መተኛት አልቻልኩም፤ two pillows አድርጌ እንኳን burning sensation ይኖረዋል። safe የሆነ antacid syrup ወይም medication ከመድሃኒት ቤት መግዛት እችላለሁ ወይስ prescription ያስፈልጋል?*

#### Sahara
- **Latency**: 5.42s | **Ref Words**: 39 | **Errors**: 10 (S: 6, D: 4, I: 0)
- **WER**: **25.6%** | **Word Accuracy**: **74.4%** | **CER**: 13.5%

```text
REF : ምንም   serious   pain    የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት         ቤት       መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል   
HYP : ምንም   serious   spain   የለብኝም   ግን   ---   ድሀድበን       እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pilows    አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   ---     ---   ---          syropecation   ከመድሀኒት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልገናል  
EVAL: ✓     ✓         SUB     ✓       ✓    DEL   SUB         ✓    ✓      ✓        ✓     ✓        ✓     ✓       ✓      ✓    ✓       ✓      ✓        ✓     SUB       ✓      ✓      ✓         ✓           ✓       ✓      ✓     ✓         DEL     DEL   DEL          SUB            SUB      ✓      ✓       ✓     ✓              SUB      
```

#### Addis Ai
- **Latency**: 12.9s | **Ref Words**: 39 | **Errors**: 20 (S: 19, D: 1, I: 0)
- **WER**: **51.3%** | **Word Accuracy**: **48.7%** | **CER**: 61.5%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   ሲሪየስ      ፔን     የለብኝም   ግን   ---   ድሃድበን       እና   አሲድ    ሪፍሉክስ    በጣም   ሲቪር      ሆኗል   ናይት     ታይም    ላይ   ስሊፕ     መተኛት   አልቻልኩም   ቱ     ፒሎዝ       አድርጌ   እንኳን   ቨርሚንግ     ሴንሴሽን       ይኖረዋል   ሴፍ     የሆነ   አንታሲድ     ሲሮፕ     ወይም   ሜዲኬሽን        ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ውይስ   ፕሮስክሪፕሽን       ያስፈልጋል  
EVAL: ✓     SUB       SUB    ✓       ✓    DEL   SUB         ✓    SUB    SUB      ✓     SUB      ✓     SUB     SUB    ✓    SUB     ✓      ✓        SUB   SUB       ✓      ✓      SUB       SUB         ✓       SUB    ✓     SUB       SUB     ✓     SUB          ✓        ✓    ✓      ✓       SUB   SUB            ✓       
```

#### Gemini
- **Latency**: 32.21s | **Ref Words**: 39 | **Errors**: 5 (S: 3, D: 2, I: 0)
- **WER**: **12.8%** | **Word Accuracy**: **87.2%** | **CER**: 4.2%

```text
REF : ምንም   serious   pain   የለብኝም     ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time        ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   serious   pain   ባይኖርብኝም   ግን   ---   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   ---     nighttime   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድኃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
EVAL: ✓     ✓         ✓      SUB       ✓    DEL   ✓           ✓    ✓      ✓        ✓     ✓        ✓     DEL     SUB         ✓    ✓       ✓      ✓        ✓     ✓         ✓      ✓      ✓         ✓           ✓       ✓      ✓     ✓         ✓       ✓     ✓            SUB      ✓    ✓      ✓       ✓     ✓              ✓       
```

---

### Voice: `v41.wav`
> **Ground Truth Reference**:
> *አዎ ዛሬ morning ላይ ከ breakfast በኋላ the iron and folic acid tablet ወስጃለሁ። ግን calcium tabletቱን ማታ ከመተኛቴ በፊት ነው የምወስደው፤ ምክንያቱም simultaneously ከወሰድኳቸው severe nausea እና mild constipation ይፈጥርብኛል። doctorሩም separate አድርጌ እንድወስድ ነግሮኛል፣ so far strictly scheduleሩን እየተከተልኩ ነው።*

#### Sahara
- **Latency**: 4.74s | **Ref Words**: 42 | **Errors**: 15 (S: 12, D: 2, I: 1)
- **WER**: **35.7%** | **Word Accuracy**: **64.3%** | **CER**: 19.3%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron    and   folic   acid   tablet    ወስጃለሁ   ግን   ---    calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   morning   ላይ   ከ    breakft     በኋላ   ---   diron   and   folic   ---    stablet   ወስጃለሁ   ግን   ካልሲም   tablet    ትቱን        ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nozia    እና   mid    conspation     ይፈጥርብኛል   doctor     ሰፕራ        አድርጌ   እንዲወስድ   ነግሮኛል   so   far   strictly   scadon       እየተከተልኩ   ነው  
EVAL: ✓    ✓    ✓         ✓    ✓    SUB         ✓     DEL   SUB     ✓     ✓       DEL    SUB       ✓       ✓    INS    SUB       SUB        ✓    ✓       ✓     ✓    ✓        ✓        ✓                ✓         ✓        SUB      ✓    SUB    SUB            ✓         SUB        SUB        ✓      SUB      ✓       ✓    ✓     ✓          SUB          ✓         ✓   
```

#### Addis Ai
- **Latency**: 6.66s | **Ref Words**: 42 | **Errors**: 23 (S: 20, D: 3, I: 0)
- **WER**: **54.8%** | **Word Accuracy**: **45.2%** | **CER**: 60.6%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ     breakfast   በኋላ   the   iron   and    folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so    far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   ሞኒንግ      ላይ   ---   ከብሬክፋስት     በኋላ   ---   ዲ      አይሮን   አንድ     ፎሊክስ   ታብሌት     ወስጃለሁ   ግን   ካልሲም      ታብሌትቱን     ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   ሲሞልቴኒየስሊ         ከወሰድኳቸው   ---      ስቪርኖዚያ   እና   ማይድ    ኮንስፔሽን         ይፈጥርብኛል   ዶክተሩም      ሰፕራይ       አድርጌ   እንዲወስድ   ነግሮኛል   ሶ     ፋር    ስትሪክሊ      ኤስኬዱሩን       እየተከተልኩ   ነው  
EVAL: ✓    ✓    SUB       ✓    DEL   SUB         ✓     DEL   SUB    SUB    SUB     SUB    SUB      ✓       ✓    SUB       SUB        ✓    ✓       ✓     ✓    ✓        ✓        SUB              ✓         DEL      SUB      ✓    SUB    SUB            ✓         SUB        SUB        ✓      SUB      ✓       SUB   SUB   SUB        SUB          ✓         ✓   
```

#### Gemini
- **Latency**: 10.49s | **Ref Words**: 42 | **Errors**: 8 (S: 5, D: 3, I: 0)
- **WER**: **19.1%** | **Word Accuracy**: **81.0%** | **CER**: 7.8%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ     breakfast    በኋላ   the   iron    and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   morning   ላይ   ---   ከbreakfast   በኋላ   ---   የiron   እና    folic   ---    tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   ዶክተሩም      separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሉን   እየተከተልኩ   ነው  
EVAL: ✓    ✓    ✓         ✓    DEL   SUB          ✓     DEL   SUB     SUB   ✓       DEL    ✓        ✓       ✓    ✓         ✓          ✓    ✓       ✓     ✓    ✓        ✓        ✓                ✓         ✓        ✓        ✓    ✓      ✓              ✓         SUB        ✓          ✓      ✓        ✓       ✓    ✓     ✓          SUB          ✓         ✓   
```

---

### Voice: `v42.wav`
> **Ground Truth Reference**:
> *ዛሬ morning ጀምሮ the fetal kick በጣም decrease አድርጓል። normally after breakfast very active ነበር የሚሆነው፤ ዛሬ ግን hardly any movement ተሰማኝ። cold juice ጠጥቼ ቆይቻለሁ ግን still quiet ነው። please hospital emergency triage መሄድ አለብኝ ወይስ ትንሽ ልጠብቅ?*

#### Sahara
- **Latency**: 4.24s | **Ref Words**: 39 | **Errors**: 7 (S: 3, D: 4, I: 0)
- **WER**: **17.9%** | **Word Accuracy**: **82.0%** | **CER**: 13.7%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal    kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice     ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   the   feetly   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   ---    coljust   ጠጥቼ   ቆይቻለሁ   ግን   still   coየት    ነው   please   hospital   emergency   ---      መሄድ   አለብኝ   ወይስ   ---   ---   
EVAL: ✓    ✓         ✓     ✓     SUB      ✓      ✓     ✓          ✓       ✓          ✓       ✓           ✓      ✓        ✓     ✓       ✓    ✓    ✓        ✓     ✓          ✓      DEL    SUB       ✓     ✓       ✓    ✓       SUB     ✓    ✓        ✓          ✓           DEL      ✓     ✓      ✓     DEL   DEL   
```

#### Addis Ai
- **Latency**: 5.28s | **Ref Words**: 39 | **Errors**: 21 (S: 21, D: 0, I: 0)
- **WER**: **53.8%** | **Word Accuracy**: **46.2%** | **CER**: 68.1%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   ሞርኒንግ     ጀምሮ   ዘ     ፊትል     ኪክ     በጣም   ዲክሪስ       አድርጓል   ኖርማሊ       አፍተር    ብሬክፋስት      ቬሪ     አክቲቭ     ነበር   የሚሆነው   ዛሬ   ግን   ሃርድሊ     ኤኒ    ሙቭመንት      ተሰማኝ   ኮል     ጁስ      ጠጥቼ   ቆይቻለሁ   ግን   ስቲል     ኳየት     ነው   ፕሊስ      ሆስፒታል      ኢመርጀንሲ      ትራያዥ     መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
EVAL: ✓    SUB       ✓     SUB   SUB     SUB    ✓     SUB        ✓       SUB        SUB     SUB         SUB    SUB      ✓     ✓       ✓    ✓    SUB      SUB   SUB        ✓      SUB    SUB     ✓     ✓       ✓    SUB     SUB     ✓    SUB      SUB        SUB         SUB      ✓     ✓      ✓     ✓     ✓     
```

#### Gemini
- **Latency**: 18.17s | **Ref Words**: 39 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **7.7%** | **Word Accuracy**: **92.3%** | **CER**: 2.8%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   ---   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበረ   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠበቅ  
EVAL: ✓    ✓         ✓     DEL   ✓       ✓      ✓     ✓          ✓       ✓          ✓       ✓           ✓      ✓        SUB   ✓       ✓    ✓    ✓        ✓     ✓          ✓      ✓      ✓       ✓     ✓       ✓    ✓       ✓       ✓    ✓        ✓          ✓           ✓        ✓     ✓      ✓     ✓     SUB   
```

---

### Voice: `v43.wav`
> **Ground Truth Reference**:
> *ዛሬ lower back pain እና pelvic pressure በጣም ይሰማኛል፣ especially ስራ ላይ standing for a long time ስሆን unbearable ይሆናል። fetal movement ግን active ነው፣ baby normal kick እያደረገ ነው። ይሄ normal third-trimester symptom ነው ወይስ doctorሩን emergency ማናገር አለብኝ?*

#### Sahara
- **Latency**: 4.61s | **Ref Words**: 41 | **Errors**: 8 (S: 5, D: 3, I: 0)
- **WER**: **19.5%** | **Word Accuracy**: **80.5%** | **CER**: 13.5%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል        fetal   movement   ግን   active   ነው   baby   normal   kick    እያደረገ   ነው   ይሄ   normal   third   trimester   symptom     ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   ---          umbarible   fetal   movement   ግን   active   ነው   baby   no       mokik   እያደረገ   ነው   ይሄ   normal   ---     ---         temestemt   ነው   ወይስ   doctor     emergency   ማናገር   አለብኝ  
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            ✓    ✓    ✓          ✓     ✓    ✓      ✓      ✓     DEL          SUB         ✓       ✓          ✓    ✓        ✓    ✓      SUB      SUB     ✓       ✓    ✓    ✓        DEL     DEL         SUB         ✓    ✓     SUB        ✓           ✓      ✓     
```

#### Addis Ai
- **Latency**: 5.37s | **Ref Words**: 41 | **Errors**: 24 (S: 23, D: 1, I: 0)
- **WER**: **58.5%** | **Word Accuracy**: **41.5%** | **CER**: 73.6%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a     long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   ሎዋር     ባክ     ፔን     እና   ፔልቪክ     ፕረሸር       በጣም   ይሰማኛል   እስፔሻሊ        ስራ   ላይ   ስታንዲንግ     ፎር    ኤ     ሎንግ    ታይም    ስሆን   አምቤርቦ        ይሆናል   ፊትል     ሙቭመንት      ግን   አክቲቭ     ነው   ቤቢ     ኖሞል      ኪክ     እያደረገ   ነው   ይሄ   ---      ኖሞል     ተርትራይምስት    ሲምፕተም     ነው   ወይስ   ዶክተሩን      ኢመርጀንሲ      ማናገር   አለብኝ  
EVAL: ✓    SUB     SUB    SUB    ✓    SUB      SUB        ✓     ✓       SUB          ✓    ✓    SUB        SUB   SUB   SUB    SUB    ✓     SUB          ✓      SUB     SUB        ✓    SUB      ✓    SUB    SUB      SUB    ✓       ✓    ✓    DEL      SUB     SUB         SUB       ✓    ✓     SUB        SUB         ✓      ✓     
```

#### Gemini
- **Latency**: 10.75s | **Ref Words**: 41 | **Errors**: 5 (S: 4, D: 1, I: 0)
- **WER**: **12.2%** | **Word Accuracy**: **87.8%** | **CER**: 7.2%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ    ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ    normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ሥራ    ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   ---    babyውም   kick   እያደረገ   ነው   ይህ    normal   third   trimester   symptom   ነው   ወይስ   ዶክተሩን      emergency   ማናገር   አለብኝ  
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            SUB   ✓    ✓          ✓     ✓    ✓      ✓      ✓     ✓            ✓      ✓       ✓          ✓    ✓        ✓    DEL    SUB      ✓      ✓       ✓    SUB   ✓        ✓       ✓           ✓         ✓    ✓     SUB        ✓           ✓      ✓     
```

---

### Voice: `v44.wav`
> **Ground Truth Reference**:
> *ዛሬ taken አድርጌያለሁ፣ but yesterday ሙሉ ቀን ስራ ስለነበርኩ the calcium supplementቱን መውሰድ forget አድርጌ ነበር። ዛሬ double dose መውሰድ አለብኝ ወይስ just continue with one tablet? IFAውን ግን today as usual ጠዋት ወስጃለሁ፣ no complications።*

#### Sahara
- **Latency**: 4.09s | **Ref Words**: 36 | **Errors**: 6 (S: 5, D: 1, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 16.8%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
HYP : ዛሬ   taken   አድርጌያለሁ   ---   በ           ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplement     መውሰድ   ፈጌት      አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ይፋውን    ግን   ትዴ      as   usual   ጠዋት   ወስጃለሁ   no   complications  
EVAL: ✓    ✓       ✓         DEL   SUB         ✓    ✓    ✓    ✓        ✓     ✓         SUB            ✓      SUB      ✓      ✓     ✓    ✓        ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        SUB     ✓    SUB     ✓    ✓       ✓     ✓       ✓    ✓              
```

#### Addis Ai
- **Latency**: 5.68s | **Ref Words**: 36 | **Errors**: 21 (S: 19, D: 1, I: 1)
- **WER**: **58.3%** | **Word Accuracy**: **41.7%** | **CER**: 65.3%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   ---   just    continue   with   one    tablet   ifaውን   ግን   today   as    usual   ጠዋት   ወስጃለሁ   no    complications  
HYP : ዛሬ   ቴክን     አድርጌያለሁ   በት    የስተዴይ       ሙሉ   ቀን   ስራ   ስለነበርኩ   ---   ዘካልሲየም    ሳፕሊመንቱን        መውሰድ   ፈጌት      አድርጌ   ነበር   ዛሬ   ዳብል      ዶስ     መውሰድ   አለብኝ   ወይስ   ጀስት   ኮንቲኒው   ዊዝ         ዋን     ታብሌት   ኢት       አይሆን    ግን   ቱዴይ     አዝ    ዩዝዋል    ጠዋት   ወስጃለሁ   ኖ     ኮምፕኬሽንስ        
EVAL: ✓    SUB     ✓         SUB   SUB         ✓    ✓    ✓    ✓        DEL   SUB       SUB            ✓      SUB      ✓      ✓     ✓    SUB      SUB    ✓      ✓      ✓     INS   SUB     SUB        SUB    SUB    SUB      SUB     ✓    SUB     SUB   SUB     ✓     ✓       SUB   SUB            
```

#### Gemini
- **Latency**: 40.96s | **Ref Words**: 36 | **Errors**: 9 (S: 6, D: 0, I: 3)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 7.2%

```text
REF : ዛሬ   ---    taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ    ስለነበርኩ   the   calcium   ---          supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ---      ifaውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
HYP : ዛሬ   take   ን       አድርጌአለሁ   but   yesterday   ሙሉ   ቀን   ሥራ    ስለነበርኩ   the   calcium   supplement   ን              መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   thyron   ን       ግን   today   as   usual   ጧት    ወስጃለሁ   no   complications  
EVAL: ✓    INS    SUB     SUB       ✓     ✓           ✓    ✓    SUB   ✓        ✓     ✓         INS          SUB            ✓      ✓        ✓      ✓     ✓    ✓        ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        INS      SUB     ✓    ✓       ✓    ✓       SUB   ✓       ✓    ✓              
```

---

### Voice: `v45.wav`
> **Ground Truth Reference**:
> *ዛሬማ ገና አልወሰድኩም እኮ። ጠዋት morning sicknessሱ በጣም አስቸግሮኝ vomit ሳደርግ ነው የረፈደው፤ empty stomach መውሰድ አልቻልኩም። አሁን after lunch ትንሽ ሻል ሲለኝ the daily IFA supplementቱን ከብዙ water ጋር እወስደዋለሁ። calcium ደሞ አብሬ ልውሰደው ወይስ gap ልስጠው?*

#### Sahara
- **Latency**: 21.55s | **Ref Words**: 38 | **Errors**: 17 (S: 15, D: 2, I: 0)
- **WER**: **44.7%** | **Word Accuracy**: **55.3%** | **CER**: 28.6%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit    ሳደርግ   ነው   የረፈደው   empty   stomach      መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል    ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ    ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   ሲክነሱ        በጣም   አስቸግሮኝ   wommit   ሳደርግ   ነው   ---     የረፈ     emtystamac   መውሰድ   አልቻልኩም   አሁን   አፍ      ላንቺ     ትንሽ   ትንሽ   አልኝ   the   daily   if    supplement     ከብዙ   ---     ጋር   እወስደዋለሁ   ካልሲም      ደግሞ   አብሬን   ውሰደው    ወይስ   ጋፕ    ልስጠው  
EVAL: ✓     ✓    ✓         ✓    ✓     ✓         SUB         ✓     ✓        SUB      ✓      ✓    DEL     SUB     SUB          ✓      ✓        ✓     SUB     SUB     ✓     SUB   SUB   ✓     ✓       SUB   SUB            ✓     DEL     ✓    ✓         SUB       SUB   SUB    SUB     ✓     SUB   ✓     
```

#### Addis Ai
- **Latency**: 5.42s | **Ref Words**: 38 | **Errors**: 17 (S: 16, D: 0, I: 1)
- **WER**: **44.7%** | **Word Accuracy**: **55.3%** | **CER**: 48.2%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   ---   gap   ልስጠው  
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   ሞኒንግ      ሲክነሱ        በጣም   አስቸግሮኝ   ወሚት     ሳደርግ   ነው   የረፈደው   እምቲስ    ተማክ       መውሰድ   አልቻልኩም   አሁን   አፍተር    ላንች     ትንሽ   ሻል   ሲለኝ   ዘ     ዴይሊ     አይፍ   ሳፕልማንቱን        ከብዙ   ዋተር     ጋር   እወስደዋለሁ   ካልሲየም     ደግሞ   አብሬ   ልውሰደው   ወይስ   ከአብ   ልስጥ   አው    
EVAL: ✓     ✓    ✓         ✓    ✓     SUB       SUB         ✓     ✓        SUB     ✓      ✓    ✓       SUB     SUB       ✓      ✓        ✓     SUB     SUB     ✓     ✓    ✓     SUB   SUB     SUB   SUB            ✓     SUB     ✓    ✓         SUB       SUB   ✓     ✓       ✓     INS   SUB   SUB   
```

#### Gemini
- **Latency**: 32.42s | **Ref Words**: 38 | **Errors**: 10 (S: 8, D: 0, I: 2)
- **WER**: **26.3%** | **Word Accuracy**: **73.7%** | **CER**: 5.4%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   ---        sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል    ሲለኝ   the   daily   ---   ifa          supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬ    ገና   አልወሰድኩም   እኮ   ጧት    morning   sickness   ኡ           በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ይሻል   ሲለኝ   the   daily   if    supplement   ኡን             ከብዙ   water   ጋር   ወስደዋለሁ    calcium   ደግሞ   አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
EVAL: SUB   ✓    ✓         ✓    SUB   ✓         INS        SUB         ✓     ✓        ✓       ✓      ✓    ✓       ✓       ✓         ✓      ✓        ✓     ✓       ✓       ✓     SUB   ✓     ✓     ✓       INS   SUB          SUB            ✓     ✓       ✓    SUB       ✓         SUB   ✓     ✓       ✓     ✓     ✓     
```

---

### Voice: `v46.wav`
> **Ground Truth Reference**:
> *እግሬ በጣም እያበጠ ነው፤ today both feet ላይ severe swelling አለ፣ ጫማዬም አልገባ ብሎኛል። ከዚህም በተጨማሪ mild headache አለኝ። BPዬ high ሆኖ እንዳይሆን ፈርቻለሁ፤ nearby clinic ሄጄ blood pressure check ማድረግ አለብኝ ወይስ tomorrow morning መምጣት ይሻላል?*

#### Sahara
- **Latency**: 5.17s | **Ref Words**: 37 | **Errors**: 12 (S: 6, D: 6, I: 0)
- **WER**: **32.4%** | **Word Accuracy**: **67.6%** | **CER**: 18.8%

```text
REF : እግሬ   በጣም   እያበጠ   ነው    today   both   feet    ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ    high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic       ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : ---   ---   ---    ---   today   ---    በወጥፊት   ላይ   severe   swelling   አለ   ጫማዬን   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mill   headache   አለኝ   deep   high   ሆኖ   እንዳይሆን   ---     ፈርጫለሁ    nibiclinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
EVAL: DEL   DEL   DEL    DEL   ✓       DEL    SUB     ✓    ✓        ✓          ✓    SUB    ✓      ✓      ✓      ✓       SUB    ✓          ✓     SUB    ✓      ✓    ✓        DEL     SUB      SUB          ✓    ✓       ✓          ✓       ✓      ✓      ✓     ✓          ✓         ✓      ✓     
```

#### Addis Ai
- **Latency**: 5.57s | **Ref Words**: 37 | **Errors**: 21 (S: 17, D: 4, I: 0)
- **WER**: **56.8%** | **Word Accuracy**: **43.2%** | **CER**: 63.0%

```text
REF : እግሬ   በጣም   እያበጠ   ነው    today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : ---   ---   ---    ---   ትዴይ     ቦት     ፊት     ላይ   ስቪየርስ    ወልኝ        አለ   ጫማዬን   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   ማይል    ሄዴክ        አለኝ   ቢፕ    ሃይ     ሆኖ   እንዳይሆን   ፈርቻለሁ   ኒባይ      ክሊኒክ     ሄጄ   ብላክ     ፕርሸር       ቼክ      ማድረግ   አለብኝ   ወይስ   ትሞሮ        ሞኒንግ      መምጣት   ይሻላል  
EVAL: DEL   DEL   DEL    DEL   SUB     SUB    SUB    ✓    SUB      SUB        ✓    SUB    ✓      ✓      ✓      ✓       SUB    SUB        ✓     SUB   SUB    ✓    ✓        ✓       SUB      SUB      ✓    SUB     SUB        SUB     ✓      ✓      ✓     SUB        SUB       ✓      ✓     
```

#### Gemini
- **Latency**: 41.8s | **Ref Words**: 37 | **Errors**: 10 (S: 2, D: 6, I: 2)
- **WER**: **27.0%** | **Word Accuracy**: **73.0%** | **CER**: 18.2%

```text
REF : ---    እግሬ   በጣም   እያበጠ   ነው    today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   ---   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : ሁለቱም   እግሬ   ---   ---    ---   ---     ---    ---    ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bp    high   ሆኖ   እንዳይሆን   ፈርቻለሁ   እኔ    ወደ       clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
EVAL: INS    ✓     DEL   DEL    DEL   DEL     DEL    DEL    ✓    ✓        ✓          ✓    ✓      ✓      ✓      ✓      ✓       ✓      ✓          ✓     SUB   ✓      ✓    ✓        ✓       INS   SUB      ✓        ✓    ✓       ✓          ✓       ✓      ✓      ✓     ✓          ✓         ✓      ✓     
```

---

### Voice: `v47.wav`
> **Ground Truth Reference**:
> *እኔ የ folic acid እና iron supplementቱን correctly ወስጃለሁ፣ ምንም side effect የለብኝም። ግን the calcium tablets አልቀውብኛል፤ ባለፈው clinic ስሄድ pharmacy ውስጥ out of stock ነበር ያሉት። ዛሬ private pharmacy ፈልጌ መግዛት አለብኝ ወይስ next appointment ድረስ መጠበቅ እችላለሁ?*

#### Sahara
- **Latency**: 7.06s | **Ref Words**: 40 | **Errors**: 8 (S: 5, D: 3, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 12.9%

```text
REF : እኔ   የ    folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplimant     correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   ---   ---       tablet    ያልቀውብኛል   ባለፈው   clinic   ሲሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   ነክ     appointment   ---   መጠበቅ   እችላለሁ  
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      SUB            ✓           ✓       ✓     ✓      ✓        ✓       ✓    DEL   DEL       SUB       SUB       ✓      ✓        SUB   ✓          ✓     ✓     ✓    ✓       ✓     ✓     ✓    ✓         ✓          ✓     ✓      ✓      ✓     SUB    ✓             DEL   ✓      ✓      
```

#### Addis Ai
- **Latency**: 5.53s | **Ref Words**: 40 | **Errors**: 25 (S: 23, D: 1, I: 1)
- **WER**: **62.5%** | **Word Accuracy**: **37.5%** | **CER**: 63.4%

```text
REF : እኔ   የ     folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of    stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ---   ወይስ   next   appointment   ድረስ     መጠበቅ   እችላለሁ  
HYP : እኔ   ---   የፎሊክ    አሲድ    እና   አይሮን   ሳፕልማንቱን        ኮሬክትሊ       ወስጃለሁ   ምንም   ሳይድ    ኢፌክት     የለብኝም   ግን   ዘ     ካልሲየም     ታብሌትስ     አልቆብኛል    ባለፈው   ክሊኒክ     ስሄድ   ፋርማሲ       ውስጥ   አውት   ኦፍ    ስቶክ     ነበር   ያሉት   ዛሬ   ፕራይቬት     ፋርማሲ       ፈልጌ   መግዛት   አለብኝ   ወደ    እስ    ነክስት   አፕዋይንት        መንድረስ   መጠበቅ   ችላለሁ   
EVAL: ✓    DEL   SUB     SUB    ✓    SUB    SUB            SUB         ✓       ✓     SUB    SUB      ✓       ✓    SUB   SUB       SUB       SUB       ✓      SUB      ✓     SUB        ✓     SUB   SUB   SUB     ✓     ✓     ✓    SUB       SUB        ✓     ✓      ✓      INS   SUB   SUB    SUB           SUB     ✓      SUB    
```

#### Gemini
- **Latency**: 13.6s | **Ref Words**: 40 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **7.5%** | **Word Accuracy**: **92.5%** | **CER**: 3.2%

```text
REF : እኔ   የ    folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplementኡን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   የ     calcium   tablets   አልቆብኛል    ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      SUB            ✓           ✓       ✓     ✓      ✓        ✓       ✓    SUB   ✓         ✓         SUB       ✓      ✓        ✓     ✓          ✓     ✓     ✓    ✓       ✓     ✓     ✓    ✓         ✓          ✓     ✓      ✓      ✓     ✓      ✓             ✓     ✓      ✓      
```

---

### Voice: `v48.wav`
> **Ground Truth Reference**:
> *ዛሬ afternoon ላይ lower abdomenኔ tight እያደረገ frequent cramps ይሰማኛል፣ like period pain። intervalሉ ግን regular አይደለም። these are just Braxton Hicks contractions or early labor signs መሆናቸውን distinguish ማድረግ አልቻልኩም። what other warning signs should I monitor?*

#### Sahara
- **Latency**: 3.38s | **Ref Words**: 38 | **Errors**: 12 (S: 9, D: 2, I: 1)
- **WER**: **31.6%** | **Word Accuracy**: **68.4%** | **CER**: 14.5%

```text
REF : ዛሬ   afternoon    ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs     መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   ---   other   warning   signs   should   i         monitor  
HYP : ዛሬ   afternonon   ላይ   ለወር     abdoment   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalu   ግን   regular   አይደለም   these   are   just   bruxton   hicks   contractions   or   early   labor   science   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   at    there   warning   ---     ---      science   shudy    
EVAL: ✓    SUB          ✓    SUB     SUB        ✓       ✓       ✓          ✓        ✓       ✓      ✓        ✓      SUB         ✓    ✓         ✓       ✓       ✓     ✓      SUB       ✓       ✓              ✓    ✓       ✓       SUB       ✓        ✓             ✓      ✓        ✓      INS   SUB     ✓         DEL     DEL      SUB       SUB      
```

#### Addis Ai
- **Latency**: 4.86s | **Ref Words**: 38 | **Errors**: 29 (S: 29, D: 0, I: 0)
- **WER**: **76.3%** | **Word Accuracy**: **23.7%** | **CER**: 81.6%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or    early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i     monitor  
HYP : ዛሬ   አፍትኑን       ላይ   ሎወር     አብዶሜንቴ     ታይት     እያደረገ   ፍሪኩዌንት     ክራምስ     ይሰማኛል   ላይክ    ፒሪያድ     ፔይን    ኢንተርቫሉ      ግን   ሬጉላር      አይደለም   ዚስ      አር    ጀስት    ብራክስትን    ሂክስ     ኮንትራክሽንስ       ኦር    ኤርሊ     ሌበር     ሳይንስ    መሆናቸውን   ዲስቲንጉሽ        ማድረግ   አልቻልኩም   ዋት     አዘር     ዎርኒንግ     ሳይንስ    ሹድ       አይ    ሞኒተር     
EVAL: ✓    SUB         ✓    SUB     SUB        SUB     ✓       SUB        SUB      ✓       SUB    SUB      SUB    SUB         ✓    SUB       ✓       SUB     SUB   SUB    SUB       SUB     SUB            SUB   SUB     SUB     SUB     ✓        SUB           ✓      ✓        SUB    SUB     SUB       SUB     SUB      SUB   SUB      
```

#### Gemini
- **Latency**: 12.77s | **Ref Words**: 38 | **Errors**: 4 (S: 2, D: 0, I: 2)
- **WER**: **10.5%** | **Word Accuracy**: **89.5%** | **CER**: 0.5%

```text
REF : ዛሬ   afternoon   ላይ   lower   ---       abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   ---        intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
HYP : ዛሬ   afternoon   ላይ   lower   abdomen   ኔን         tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   interval   ሉ           ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
EVAL: ✓    ✓           ✓    ✓       INS       SUB        ✓       ✓       ✓          ✓        ✓       ✓      ✓        ✓      INS        SUB         ✓    ✓         ✓       ✓       ✓     ✓      ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓             ✓      ✓        ✓      ✓       ✓         ✓       ✓        ✓    ✓        
```

---

### Voice: `v49.wav`
> **Ground Truth Reference**:
> *አዎ ወስጃለሁ፣ daily IFA ኪኒኑን ጠዋት ላይ with freshly squeezed orange juice ነው የወሰድኩት፣ iron absorptionኑን ይጨምራል ብለውኝ። calciumሙን ግን yesterday ማታ ወስጄዋለሁ፤ ዛሬም after dinner እወስደዋለሁ። እስካሁን ምንም stomach pain አልተሰማኝም፣ perfectly fine ነኝ።*

#### Sahara
- **Latency**: 6.75s | **Ref Words**: 35 | **Errors**: 17 (S: 13, D: 4, I: 0)
- **WER**: **48.6%** | **Word Accuracy**: **51.4%** | **CER**: 38.4%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን     ጠዋት   ላይ   with   freshly   squeezed   orange    juice      ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ   
HYP : አዎ   ወስጃለሁ   ዴቪ      አይፋ   tininu   ጠዋት   ላይ   with   ---       fresh      squezed   orrengus   ነው   የወሰድኩት   ---    irons          ይጨምራል   ብለውኝ   calcium     ግን   የስቴዴ        ማታ   ወስደዋለሁ   ዛሬም   after   ---      dineral   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   ---         ተፈቅቢ   ፋይን  
EVAL: ✓    ✓       SUB     SUB   SUB      ✓     ✓    ✓      DEL       SUB        SUB       SUB        ✓    ✓        DEL    SUB            ✓       ✓      SUB         ✓    SUB         ✓    SUB      ✓     ✓       DEL      SUB       ✓       ✓     ✓         ✓      ✓         DEL         SUB    SUB  
```

#### Addis Ai
- **Latency**: 4.03s | **Ref Words**: 35 | **Errors**: 20 (S: 18, D: 0, I: 2)
- **WER**: **57.1%** | **Word Accuracy**: **42.9%** | **CER**: 62.2%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   ---    yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   ---     stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
HYP : አዎ   ወስጃለሁ   ዴሊ      አይፋ   ኪኒኑን   ጠዋት   ላይ   ዊት     ፍሬሽ       ስኩዝድ       ኦረንጅ     ጁስ      ነው   የወሰድኩት   አይሮን   እንደዚህም         ይጨምራል   ብለውኝ   ከያልዚያሙን     ግን   የተያየ   ስትዴይ        ማታ   ወስጄዋለሁ   ዛሬም   አፍት     ዲነር      እወስደዋለሁ   እስካሁን   ምንም   ስተማክቴ   አስተሳሰብ    ማን     ነው        አክቲቪስት      ነኝ     ነኝ  
EVAL: ✓    ✓       SUB     SUB   ✓      ✓     ✓    SUB    SUB       SUB        SUB      SUB     ✓    ✓        SUB    SUB            ✓       ✓      SUB         ✓    INS    SUB         ✓    ✓        ✓     SUB     SUB      ✓         ✓       ✓     INS     SUB       SUB    SUB       SUB         SUB    ✓   
```

#### Gemini
- **Latency**: 20.26s | **Ref Words**: 35 | **Errors**: 8 (S: 6, D: 0, I: 2)
- **WER**: **22.9%** | **Word Accuracy**: **77.1%** | **CER**: 13.6%

```text
REF : አዎ   ወስጃለሁ   daily   ---    ifa    ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   ---       calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
HYP : አዎ   ወስጃለሁ   daily   iron   pill   ኡን     ጧት    ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   ደረጃዬን          ይጨምራል   ብለውኝ   calcium   ኡን          ግን   yesterday   ማታ   ወስጃለሁ    ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
EVAL: ✓    ✓       ✓       INS    SUB    SUB    SUB   ✓    ✓      ✓         ✓          ✓        ✓       ✓    ✓        ✓      SUB            ✓       ✓      INS       SUB         ✓    ✓           ✓    SUB      ✓     ✓       ✓        ✓         ✓       ✓     ✓         ✓      ✓         ✓           ✓      ✓   
```

---

### Voice: `v50.wav`
> **Ground Truth Reference**:
> *ምንም serious pain የለብኝም ግን the heartburn እና acid reflux በጣም severe ሆኗል። night time ላይ sleep መተኛት አልቻልኩም፤ two pillows አድርጌ እንኳን burning sensation ይኖረዋል። safe የሆነ antacid syrup ወይም medication ከመድሃኒት ቤት መግዛት እችላለሁ ወይስ prescription ያስፈልጋል?*

#### Sahara
- **Latency**: 2.57s | **Ref Words**: 39 | **Errors**: 5 (S: 4, D: 1, I: 0)
- **WER**: **12.8%** | **Word Accuracy**: **87.2%** | **CER**: 8.3%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና    acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   serious   pain   የለብኝም   ግን   ---   ደሃት         በንና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pilos     አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrop   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
EVAL: ✓     ✓         ✓      ✓       ✓    DEL   SUB         SUB   ✓      ✓        ✓     ✓        ✓     ✓       ✓      ✓    ✓       ✓      ✓        ✓     SUB       ✓      ✓      ✓         ✓           ✓       ✓      ✓     ✓         SUB     ✓     ✓            ✓        ✓    ✓      ✓       ✓     ✓              ✓       
```

#### Addis Ai
- **Latency**: 9.11s | **Ref Words**: 39 | **Errors**: 19 (S: 18, D: 1, I: 0)
- **WER**: **48.7%** | **Word Accuracy**: **51.3%** | **CER**: 60.9%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   ሲሪየስ      ፔይን    የለብኝም   ግን   ---   ዳትበርን       እና   አሲድ    ሪፍልክስ    በጣም   ሰቪየር     ሆኗል   ናይት     ታይም    ላይ   ስሊፕ     መተኛት   አልቻልኩም   ቱ     ፒሎውዝ      አድርጌ   እንኳን   በርኒንግ     ሴንሴሽን       ይኖረዋል   ሴፍ     የሆነ   አንታሲድ     ሲሮፕ     ወይም   ሜዲኬሽን        ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   ፕሮስክሪፕሽን       ያስፈልጋል  
EVAL: ✓     SUB       SUB    ✓       ✓    DEL   SUB         ✓    SUB    SUB      ✓     SUB      ✓     SUB     SUB    ✓    SUB     ✓      ✓        SUB   SUB       ✓      ✓      SUB       SUB         ✓       SUB    ✓     SUB       SUB     ✓     SUB          ✓        ✓    ✓      ✓       ✓     SUB            ✓       
```

#### Gemini
- **Latency**: 8.81s | **Ref Words**: 39 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **5.1%** | **Word Accuracy**: **94.9%** | **CER**: 2.1%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   serious   pain   የለብኝም   ግን   ---   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድኃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
EVAL: ✓     ✓         ✓      ✓       ✓    DEL   ✓           ✓    ✓      ✓        ✓     ✓        ✓     ✓       ✓      ✓    ✓       ✓      ✓        ✓     ✓         ✓      ✓      ✓         ✓           ✓       ✓      ✓     ✓         ✓       ✓     ✓            SUB      ✓    ✓      ✓       ✓     ✓              ✓       
```

---
