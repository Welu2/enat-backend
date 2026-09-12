# STT Benchmark Evaluation Report

- **Benchmark Results**: `bench_am_eng_part1.json`
- **Ground Truth**: `ground_truth.json`
- **Language**: AM
- **Total Audio Files Evaluated**: 25
- **Evaluation Date**: 2026-09-09 19:22:30 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 966 | 209 | 156 | 51 | 2 | **21.6%** | **78.4%** | 15.5% | 6.97s |
| **Addis Ai** | 966 | 544 | 509 | 24 | 11 | **56.3%** | **43.7%** | 64.6% | 8.12s |
| **Gemini** | 966 | 119 | 89 | 28 | 2 | **12.3%** | **87.7%** | 7.1% | 34.31s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v1.wav`
> **Ground Truth Reference**:
> *አዎ ዛሬ morning ላይ ከ breakfast በኋላ the iron and folic acid tablet ወስጃለሁ። ግን calcium tabletቱን ማታ ከመተኛቴ በፊት ነው የምወስደው፤ ምክንያቱም simultaneously ከወሰድኳቸው severe nausea እና mild constipation ይፈጥርብኛል። doctorሩም separate አድርጌ እንድወስድ ነግሮኛል፣ so far strictly scheduleሩን እየተከተልኩ ነው።*

#### Sahara
- **Latency**: 21.58s | **Ref Words**: 42 | **Errors**: 10 (S: 8, D: 2, I: 0)
- **WER**: **23.8%** | **Word Accuracy**: **76.2%** | **CER**: 21.6%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው        
HYP : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   ካልሲውም     ታብሌቱን      ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   ሲሙልቴን            ከወሰድኳቸው   severe   nausea   እና   mild   conspation     ይፈጥርብኛል   doctor     supprise   አድርጌ   እንዲወስድ   ነግሮኛል   so   far   strictly   ---          ---       schedule  
EVAL: ✓    ✓    ✓         ✓    ✓    ✓           ✓     ✓     ✓      ✓     ✓       ✓      ✓        ✓       ✓    SUB       SUB        ✓    ✓       ✓     ✓    ✓        ✓        SUB              ✓         ✓        ✓        ✓    ✓      SUB            ✓         SUB        SUB        ✓      SUB      ✓       ✓    ✓     ✓          DEL          DEL       SUB       
```

#### Addis Ai
- **Latency**: 36.1s | **Ref Words**: 42 | **Errors**: 23 (S: 22, D: 1, I: 0)
- **WER**: **54.8%** | **Word Accuracy**: **45.2%** | **CER**: 61.0%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ     breakfast   በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so    far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   ሞኒንግ      ላይ   ---   ከብሬክፋስት     በኋላ   ዘ     አይረን   ኤንድ   ፎሊክ     አሲድ    ታብሌት     ወስጃለሁ   ግን   ካልሲየም     ታብሌቱ       ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   ሲሞልቲኒዩስ          ከወሰድኳቸው   ሲቪር      ኖዜ       እና   ማይልድ   ኮንስፔሽን         ይፈጥርብኛል   ዶክተሩም      ሰፕራይት      አድርጌ   እንዲወስድ   ነግሮኛል   ሶ     ፋር    ስትሪክሊ      ስኬድዮሩን       እየተከተልኩ   ነው  
EVAL: ✓    ✓    SUB       ✓    DEL   SUB         ✓     SUB   SUB    SUB   SUB     SUB    SUB      ✓       ✓    SUB       SUB        ✓    ✓       ✓     ✓    ✓        ✓        SUB              ✓         SUB      SUB      ✓    SUB    SUB            ✓         SUB        SUB        ✓      SUB      ✓       SUB   SUB   SUB        SUB          ✓         ✓   
```

#### Gemini
- **Latency**: 21.82s | **Ref Words**: 42 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **2.4%** | **Word Accuracy**: **97.6%** | **CER**: 2.8%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   ዶክተሩም      separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው  
EVAL: ✓    ✓    ✓         ✓    ✓    ✓           ✓     ✓     ✓      ✓     ✓       ✓      ✓        ✓       ✓    ✓         ✓          ✓    ✓       ✓     ✓    ✓        ✓        ✓                ✓         ✓        ✓        ✓    ✓      ✓              ✓         SUB        ✓          ✓      ✓        ✓       ✓    ✓     ✓          ✓            ✓         ✓   
```

---

### Voice: `v2.wav`
> **Ground Truth Reference**:
> *ዛሬ morning ጀምሮ the fetal kick በጣም decrease አድርጓል። normally after breakfast very active ነበር የሚሆነው፤ ዛሬ ግን hardly any movement ተሰማኝ። cold juice ጠጥቼ ቆይቻለሁ ግን still quiet ነው። please hospital emergency triage መሄድ አለብኝ ወይስ ትንሽ ልጠብቅ?*

#### Sahara
- **Latency**: 5.28s | **Ref Words**: 39 | **Errors**: 6 (S: 5, D: 1, I: 0)
- **WER**: **15.4%** | **Word Accuracy**: **84.6%** | **CER**: 8.2%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very        active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   the   fetal   cake   በጣም   decrease   አድርጓል   normally   after   ---         breakfery   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   col    just    ጠጥቼ   ቆይቻለሁ   ግን   still   quate   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
EVAL: ✓    ✓         ✓     ✓     ✓       SUB    ✓     ✓          ✓       ✓          ✓       DEL         SUB         ✓        ✓     ✓       ✓    ✓    ✓        ✓     ✓          ✓      SUB    SUB     ✓     ✓       ✓    ✓       SUB     ✓    ✓        ✓          ✓           ✓        ✓     ✓      ✓     ✓     ✓     
```

#### Addis Ai
- **Latency**: 6.45s | **Ref Words**: 39 | **Errors**: 22 (S: 21, D: 0, I: 1)
- **WER**: **56.4%** | **Word Accuracy**: **43.6%** | **CER**: 69.2%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ   ---  
HYP : ዛሬ   ሞርኒንግ     ጀምሮ   ዘ     ፊተል     ኪክ     በጣም   ዲክሪስ       አድርጓል   ኖርማሊ       አፍተር    ብሬክፋስት      ቬሪ     አክቲቭ     ነበር   የሚሆነው   ዛሬ   ግን   ሃርድሊ     ኤኒ    ሙቭመንት      ተሰማኝ   ኮል     ጁስ      ጠጥቼ   ቆይቻለሁ   ግን   ስቲል     ኳየት     ነው   ፕሊስ      ሆስፒታል      ኢመርጀንሲ      ትራያጅ     መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ   አዎ   
EVAL: ✓    SUB       ✓     SUB   SUB     SUB    ✓     SUB        ✓       SUB        SUB     SUB         SUB    SUB      ✓     ✓       ✓    ✓    SUB      SUB   SUB        ✓      SUB    SUB     ✓     ✓       ✓    SUB     SUB     ✓    SUB      SUB        SUB         SUB      ✓     ✓      ✓     ✓     ✓      INS  
```

#### Gemini
- **Latency**: 33.14s | **Ref Words**: 39 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **5.1%** | **Word Accuracy**: **94.9%** | **CER**: 2.2%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   ---   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠበቅ  
EVAL: ✓    ✓         ✓     DEL   ✓       ✓      ✓     ✓          ✓       ✓          ✓       ✓           ✓      ✓        ✓     ✓       ✓    ✓    ✓        ✓     ✓          ✓      ✓      ✓       ✓     ✓       ✓    ✓       ✓       ✓    ✓        ✓          ✓           ✓        ✓     ✓      ✓     ✓     SUB   
```

---

### Voice: `v3.wav`
> **Ground Truth Reference**:
> *ዛሬ lower back pain እና pelvic pressure በጣም ይሰማኛል፣ especially ስራ ላይ standing for a long time ስሆን unbearable ይሆናል። fetal movement ግን active ነው፣ baby normal kick እያደረገ ነው። ይሄ normal third-trimester symptom ነው ወይስ doctorሩን emergency ማናገር አለብኝ?*

#### Sahara
- **Latency**: 14.38s | **Ref Words**: 41 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **4.9%** | **Word Accuracy**: **95.1%** | **CER**: 6.2%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   አንበረቦ        ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctor     emergency   ማናገር   አለብኝ  
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            ✓    ✓    ✓          ✓     ✓    ✓      ✓      ✓     SUB          ✓      ✓       ✓          ✓    ✓        ✓    ✓      ✓        ✓      ✓       ✓    ✓    ✓        ✓       ✓           ✓         ✓    ✓     SUB        ✓           ✓      ✓     
```

#### Addis Ai
- **Latency**: 13.23s | **Ref Words**: 41 | **Errors**: 25 (S: 25, D: 0, I: 0)
- **WER**: **61.0%** | **Word Accuracy**: **39.0%** | **CER**: 74.1%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a     long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   ሎወር     ባክ     ፔን     እና   ኬልቪክ     ፕሬሸር       በጣም   ይሰማኛል   ስፔሻሊ         ስራ   ላይ   ስቴንዲንግ     ፎር    ኤ     ሎንግ    ታይም    ሲሆን   አንበርቦ        ይሆናል   ፊትል     ሙቭመንት      ግን   አክቲቭ     ነው   ፔዲ     ኖርማል     ኪክ     እያደረገ   ነው   ይሄ   ኖርማል     ተርድ     ትራይምስተር     ሲምፕተም     ነው   ወይስ   ዶክተሩን      ኢመርጀንሲ      ማናገር   አለብኝ  
EVAL: ✓    SUB     SUB    SUB    ✓    SUB      SUB        ✓     ✓       SUB          ✓    ✓    SUB        SUB   SUB   SUB    SUB    SUB   SUB          ✓      SUB     SUB        ✓    SUB      ✓    SUB    SUB      SUB    ✓       ✓    ✓    SUB      SUB     SUB         SUB       ✓    ✓     SUB        SUB         ✓      ✓     
```

#### Gemini
- **Latency**: 7.71s | **Ref Words**: 41 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **4.9%** | **Word Accuracy**: **95.1%** | **CER**: 5.7%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   ብሶብ          ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctorን    emergency   ማናገር   አለብኝ  
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            ✓    ✓    ✓          ✓     ✓    ✓      ✓      ✓     SUB          ✓      ✓       ✓          ✓    ✓        ✓    ✓      ✓        ✓      ✓       ✓    ✓    ✓        ✓       ✓           ✓         ✓    ✓     SUB        ✓           ✓      ✓     
```

---

### Voice: `v4.wav`
> **Ground Truth Reference**:
> *ዛሬ taken አድርጌያለሁ፣ but yesterday ሙሉ ቀን ስራ ስለነበርኩ the calcium supplementቱን መውሰድ forget አድርጌ ነበር። ዛሬ double dose መውሰድ አለብኝ ወይስ just continue with one tablet? IFAውን ግን today as usual ጠዋት ወስጃለሁ፣ no complications።*

#### Sahara
- **Latency**: 5.35s | **Ref Words**: 36 | **Errors**: 6 (S: 5, D: 1, I: 0)
- **WER**: **16.7%** | **Word Accuracy**: **83.3%** | **CER**: 17.4%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን    መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
HYP : ዛሬ   techn   አድርጌያለሁ   ---   በስትዴ        ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplasmantun   መውሰድ   ፈጌት      አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   አይፈውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
EVAL: ✓    SUB     ✓         DEL   SUB         ✓    ✓    ✓    ✓        ✓     ✓         SUB             ✓      SUB      ✓      ✓     ✓    ✓        ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        SUB     ✓    ✓       ✓    ✓       ✓     ✓       ✓    ✓              
```

#### Addis Ai
- **Latency**: 5.84s | **Ref Words**: 36 | **Errors**: 21 (S: 20, D: 1, I: 0)
- **WER**: **58.3%** | **Word Accuracy**: **41.7%** | **CER**: 65.3%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ    ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose    መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as    usual   ጠዋት   ወስጃለሁ   no    complications  
HYP : ዛሬ   ቴከን     አድርጌያለሁ   በት    ይስትዴይ       የሙሉ   ቀን   ስራ   ስለነበርኩ   ዘ     ካልሲየም     ሳፕላስማንቱን       መውሰድ   ፈጌት      አድርጌ   ነበር   ዛሬ   ---      ዳቦልዶስ   መውሰድ   አለብኝ   ወይስ   ጀስት    ኮንቲኒው      ዊዝ     ዋን    ታብሌት     አይፎን    ግን   ትዴይ     አዝ    ዩዝዋል    ጠዋት   ወስጃለሁ   ኖ     ኮምፕሊኬሽንስ       
EVAL: ✓    SUB     ✓         SUB   SUB         SUB   ✓    ✓    ✓        SUB   SUB       SUB            ✓      SUB      ✓      ✓     ✓    DEL      SUB     ✓      ✓      ✓     SUB    SUB        SUB    SUB   SUB      SUB     ✓    SUB     SUB   SUB     ✓     ✓       SUB   SUB            
```

#### Gemini
- **Latency**: 14.86s | **Ref Words**: 36 | **Errors**: 5 (S: 5, D: 0, I: 0)
- **WER**: **13.9%** | **Word Accuracy**: **86.1%** | **CER**: 5.4%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ    ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
HYP : ዛሬ   take    አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ሥራ    ስለነበርኩ   the   calcium   supplementኡን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   iron    ግን   today   as   usual   ጧት    ወስጃለሁ   no   complications  
EVAL: ✓    SUB     ✓         ✓     ✓           ✓    ✓    SUB   ✓        ✓     ✓         SUB            ✓      ✓        ✓      ✓     ✓    ✓        ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        SUB     ✓    ✓       ✓    ✓       SUB   ✓       ✓    ✓              
```

---

### Voice: `v5.wav`
> **Ground Truth Reference**:
> *ዛሬማ ገና አልወሰድኩም እኮ። ጠዋት morning sicknessሱ በጣም አስቸግሮኝ vomit ሳደርግ ነው የረፈደው፤ empty stomach መውሰድ አልቻልኩም። አሁን after lunch ትንሽ ሻል ሲለኝ the daily IFA supplementቱን ከብዙ water ጋር እወስደዋለሁ። calcium ደሞ አብሬ ልውሰደው ወይስ gap ልስጠው?*

#### Sahara
- **Latency**: 9.46s | **Ref Words**: 38 | **Errors**: 15 (S: 13, D: 2, I: 0)
- **WER**: **39.5%** | **Word Accuracy**: **60.5%** | **CER**: 31.6%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል    ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ    ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   ሲቅንሱ        በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   እምት     ስተማክ      መውሰድ   አልቻልኩም   አሁን   አፍ      ላይ      ትንሽ   ---   አልኝ   the   daily   if    supplement     ከብዙ   ወተረ     ጋር   እወስደዋለሁ   ካልሲየም     ደግሞ   አብሬን   ውሰደው    ወይስ   ---   ልስጠው  
EVAL: ✓     ✓    ✓         ✓    ✓     ✓         SUB         ✓     ✓        ✓       ✓      ✓    ✓       SUB     SUB       ✓      ✓        ✓     SUB     SUB     ✓     DEL   SUB   ✓     ✓       SUB   SUB            ✓     SUB     ✓    ✓         SUB       SUB   SUB    SUB     ✓     DEL   ✓     
```

#### Addis Ai
- **Latency**: 10.19s | **Ref Words**: 38 | **Errors**: 21 (S: 16, D: 2, I: 3)
- **WER**: **55.3%** | **Word Accuracy**: **44.7%** | **CER**: 54.8%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   ---    ---    ---    vomit   ሳደርግ   ነው   የረፈደው   empty    stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ    ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   ---       ሞኒሲክንሱ      በጣም   አስቸግሮኝ   0xe1   0x89   0xae   ሚት      ሳደርግ   ነው   ---     የረፈድኩት   እምቲስተማክ   መውሰድ   አልቻልኩም   አሁን   አፍተር    ላንች     ትንሽ   ሻል   ሲለኝ   ዘ     ዴይሊ     አይፍ   ሳፕልማንቱን        ከብዙ   ወተር     ጋር   እወስደዋለሁ   ካልሲየም     ደግሞ   አብረን   ውሰደው    ወይስ   ጌብስ   ልስጠው  
EVAL: ✓     ✓    ✓         ✓    ✓     DEL       SUB         ✓     ✓        INS    INS    INS    SUB     ✓      ✓    DEL     SUB      SUB       ✓      ✓        ✓     SUB     SUB     ✓     ✓    ✓     SUB   SUB     SUB   SUB            ✓     SUB     ✓    ✓         SUB       SUB   SUB    SUB     ✓     SUB   ✓     
```

#### Gemini
- **Latency**: 46.65s | **Ref Words**: 38 | **Errors**: 10 (S: 10, D: 0, I: 0)
- **WER**: **26.3%** | **Word Accuracy**: **73.7%** | **CER**: 14.9%

```text
REF : ዛሬማ   ገና    አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው    empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   ifa    supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬም   ግን    አልወሰድኩም   እኮ   ጠዋት   morning   sicknessኡ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   ያረፈድኩት   አምስት    ታብሌት      መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   iron   supplementኡን   ከብዙ   water   ጋር   ወስደዋለሁ    calcium   ደግሞ   አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
EVAL: SUB   SUB   ✓         ✓    ✓     ✓         SUB         ✓     ✓        ✓       ✓      ✓    SUB      SUB     SUB       ✓      ✓        ✓     ✓       ✓       ✓     ✓    ✓     ✓     ✓       SUB    SUB            ✓     ✓       ✓    SUB       ✓         SUB   ✓     ✓       ✓     ✓     ✓     
```

---

### Voice: `v6.wav`
> **Ground Truth Reference**:
> *እግሬ በጣም እያበጠ ነው፤ today both feet ላይ severe swelling አለ፣ ጫማዬም አልገባ ብሎኛል። ከዚህም በተጨማሪ mild headache አለኝ። BPዬ high ሆኖ እንዳይሆን ፈርቻለሁ፤ nearby clinic ሄጄ blood pressure check ማድረግ አለብኝ ወይስ tomorrow morning መምጣት ይሻላል?*

#### Sahara
- **Latency**: 11.57s | **Ref Words**: 37 | **Errors**: 6 (S: 4, D: 2, I: 0)
- **WER**: **16.2%** | **Word Accuracy**: **83.8%** | **CER**: 11.5%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   today   ቦት     ፊት     ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   ---   bp     ሆኖ   እንዳይሆን   ፈርቻለሁ   neby     clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ---   
EVAL: ✓     ✓     ✓      ✓    ✓       SUB    SUB    ✓    ✓        ✓          ✓    ✓      ✓      ✓      ✓      ✓       ✓      ✓          ✓     DEL   SUB    ✓    ✓        ✓       SUB      ✓        ✓    ✓       ✓          ✓       ✓      ✓      ✓     ✓          ✓         ✓      DEL   
```

#### Addis Ai
- **Latency**: 6.91s | **Ref Words**: 37 | **Errors**: 18 (S: 16, D: 0, I: 2)
- **WER**: **48.6%** | **Word Accuracy**: **51.3%** | **CER**: 55.8%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   ---   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል   ---  
HYP : እግሬ   በጣም   እያበጠ   ነው   ቱዴይ     ቦት     ፊት     ላይ   ሲቪር      ስዌሊንግ      አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   ማይልድ   ሄዴክ        አለኝ   ቢፒዬ   ሃይ     ሆኖ   እንዳይሆን   ፈርቻለሁ   ኔ     ባይ       ክሊኒክ     ሄጄ   ብላድ     ፕሬሸር       ቼክ      ማድረግ   አለብኝ   ወይስ   ቱሞሮ        ሞኒንግ      መምጣት   ይሻላል   ተማ   
EVAL: ✓     ✓     ✓      ✓    SUB     SUB    SUB    ✓    SUB      SUB        ✓    ✓      ✓      ✓      ✓      ✓       SUB    SUB        ✓     SUB   SUB    ✓    ✓        ✓       INS   SUB      SUB      ✓    SUB     SUB        SUB     ✓      ✓      ✓     SUB        SUB       ✓      ✓      INS  
```

#### Gemini
- **Latency**: 34.48s | **Ref Words**: 37 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
EVAL: ✓     ✓     ✓      ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓    ✓      ✓      ✓      ✓      ✓       ✓      ✓          ✓     ✓     ✓      ✓    ✓        ✓       ✓        ✓        ✓    ✓       ✓          ✓       ✓      ✓      ✓     ✓          ✓         ✓      ✓     
```

---

### Voice: `v7.wav`
> **Ground Truth Reference**:
> *እኔ የ folic acid እና iron supplementቱን correctly ወስጃለሁ፣ ምንም side effect የለብኝም። ግን the calcium tablets አልቀውብኛል፤ ባለፈው clinic ስሄድ pharmacy ውስጥ out of stock ነበር ያሉት። ዛሬ private pharmacy ፈልጌ መግዛት አለብኝ ወይስ next appointment ድረስ መጠበቅ እችላለሁ?*

#### Sahara
- **Latency**: 4.86s | **Ref Words**: 40 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **10.0%** | **Word Accuracy**: **90.0%** | **CER**: 6.5%

```text
REF : እኔ   የ    folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplement     creatly     ወስጃለሁ   ምንም   side   ---      የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ሲሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      SUB            SUB         ✓       ✓     ✓      DEL      ✓       ✓    ✓     ✓         ✓         ✓         ✓      ✓        SUB   ✓          ✓     ✓     ✓    ✓       ✓     ✓     ✓    ✓         ✓          ✓     ✓      ✓      ✓     ✓      ✓             ✓     ✓      ✓      
```

#### Addis Ai
- **Latency**: 6.91s | **Ref Words**: 40 | **Errors**: 22 (S: 19, D: 3, I: 0)
- **WER**: **55.0%** | **Word Accuracy**: **45.0%** | **CER**: 62.9%

```text
REF : እኔ   የ     folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of    stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ     መጠበቅ   እችላለሁ  
HYP : እኔ   ---   የፎሊክ    አሲድ    እና   አይሮን   ሳፕልማንቱን        ከራክሊ        ወስጃለሁ   ምንም   ---    ሳይዲፍት    የለብኝም   ግን   ዘ     ካልሲየም     ታብሌትስ     አልቀውብኛል   ባለፈው   ክሊኒክ     ሲሄድ   ፋርማሲ       ውስጥ   አውት   ኦፍ    ስቶክ     ነበር   ያሉት   ዛሬ   ፕራይቬት     ፋርማሲ       ፈልጌ   መግዛት   አለብኝ   ወይስ   ---    ኔክስት          አፖይንት   መጠበቅ   እችላለሁ  
EVAL: ✓    DEL   SUB     SUB    ✓    SUB    SUB            SUB         ✓       ✓     DEL    SUB      ✓       ✓    SUB   SUB       SUB       ✓         ✓      SUB      SUB   SUB        ✓     SUB   SUB   SUB     ✓     ✓     ✓    SUB       SUB        ✓     ✓      ✓      ✓     DEL    SUB           SUB     ✓      ✓      
```

#### Gemini
- **Latency**: 69.88s | **Ref Words**: 40 | **Errors**: 11 (S: 5, D: 6, I: 0)
- **WER**: **27.5%** | **Word Accuracy**: **72.5%** | **CER**: 22.6%

```text
REF : እኔ   የ    folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም      ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplementኡን   correctly   ወስጃለሁ   ምንም   side   effect   አልነበረብኝም   ግን   የ     calcium   tablets   አልቆብኛል    ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበረ   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ---   ---    ---           ---   ---    ---    
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      SUB            ✓           ✓       ✓     ✓      ✓        SUB        ✓    SUB   ✓         ✓         SUB       ✓      ✓        ✓     ✓          ✓     ✓     ✓    ✓       SUB   ✓     ✓    ✓         ✓          ✓     ✓      ✓      DEL   DEL    DEL           DEL   DEL    DEL    
```

---

### Voice: `v8.wav`
> **Ground Truth Reference**:
> *ዛሬ afternoon ላይ lower abdomenኔ tight እያደረገ frequent cramps ይሰማኛል፣ like period pain። intervalሉ ግን regular አይደለም። these are just Braxton Hicks contractions or early labor signs መሆናቸውን distinguish ማድረግ አልቻልኩም። what other warning signs should I monitor?*

#### Sahara
- **Latency**: 2.8s | **Ref Words**: 38 | **Errors**: 7 (S: 5, D: 2, I: 0)
- **WER**: **18.4%** | **Word Accuracy**: **81.6%** | **CER**: 12.6%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs     መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs     should   i     monitor  
HYP : ዛሬ   afternoon   ላይ   ---     ለወርኔ       tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   interval    ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   science   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   science   should   ---   mon      
EVAL: ✓    ✓           ✓    DEL     SUB        ✓       ✓       ✓          ✓        ✓       ✓      ✓        ✓      SUB         ✓    ✓         ✓       ✓       ✓     ✓      ✓         ✓       ✓              ✓    ✓       ✓       SUB       ✓        ✓             ✓      ✓        ✓      ✓       ✓         SUB       ✓        DEL   SUB      
```

#### Addis Ai
- **Latency**: 4.48s | **Ref Words**: 38 | **Errors**: 29 (S: 29, D: 0, I: 0)
- **WER**: **76.3%** | **Word Accuracy**: **23.7%** | **CER**: 81.2%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or    early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i     monitor  
HYP : ዛሬ   አፍትኑን       ላይ   ሎወር     አብደሚኔ      ታይት     እያደረገ   ፍሪኩዌንት     ክራምፕስ    ይሰማኛል   ላይክ    ፒሪድ      ፔይን    ኢንተርቫሉ      ግን   ሬጉላር      አይደለም   ዚዝ      አር    ጀስት    ብራክስተን    ሂክስ     ኮንትራክሽንስ       ኦር    ኤርሊ     ሌበር     ሳይንስ    መሆናቸውን   ዲስቲንጉሽ        ማድረግ   አልቻልኩም   ዋት     አዘር     ዋርኒንግ     ሳይንስ    ሹድ       አይ    ሞኒተር     
EVAL: ✓    SUB         ✓    SUB     SUB        SUB     ✓       SUB        SUB      ✓       SUB    SUB      SUB    SUB         ✓    SUB       ✓       SUB     SUB   SUB    SUB       SUB     SUB            SUB   SUB     SUB     SUB     ✓        SUB           ✓      ✓        SUB    SUB     SUB       SUB     SUB      SUB   SUB      
```

#### Gemini
- **Latency**: 59.12s | **Ref Words**: 38 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **7.9%** | **Word Accuracy**: **92.1%** | **CER**: 10.6%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
HYP : ዛሬ   አፍተርኑን      ላይ   lower   abdomenኔ   ታይት     እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   ኢንተርቫሉ      ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
EVAL: ✓    SUB         ✓    ✓       ✓          SUB     ✓       ✓          ✓        ✓       ✓      ✓        ✓      SUB         ✓    ✓         ✓       ✓       ✓     ✓      ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓             ✓      ✓        ✓      ✓       ✓         ✓       ✓        ✓    ✓        
```

---

### Voice: `v9.wav`
> **Ground Truth Reference**:
> *አዎ ወስጃለሁ፣ daily IFA ኪኒኑን ጠዋት ላይ with freshly squeezed orange juice ነው የወሰድኩት፣ iron absorptionኑን ይጨምራል ብለውኝ። calciumሙን ግን yesterday ማታ ወስጄዋለሁ፤ ዛሬም after dinner እወስደዋለሁ። እስካሁን ምንም stomach pain አልተሰማኝም፣ perfectly fine ነኝ።*

#### Sahara
- **Latency**: 9.07s | **Ref Words**: 35 | **Errors**: 16 (S: 10, D: 5, I: 1)
- **WER**: **45.7%** | **Word Accuracy**: **54.3%** | **CER**: 33.3%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን      ጠዋት   ላይ   with   freshly   squeezed   orange    juice     ነው   የወሰድኩት   ---    iron      absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ   
HYP : አዎ   ወስጃለሁ   daily   ---   facinum   ጠዋት   ላይ   with   freshly   ---        squezed   orinjue   ነው   የወሰድኩት   አይሮን   absorbs   ን              ይጨምራል   ብለውኝ   ካልሲያሙን      ግን   የስቴዴ        ማታ   ወስጄዋለሁ   ዛሬም   after   diner    ወስደዋለሁ    እስካሁን   ምንም   stag      pain   አልተሰማኝም   ---         ---    ---  
EVAL: ✓    ✓       ✓       DEL   SUB       ✓     ✓    ✓      ✓         DEL        SUB       SUB       ✓    ✓        INS    SUB       SUB            ✓       ✓      SUB         ✓    SUB         ✓    ✓        ✓     ✓       SUB      SUB       ✓       ✓     SUB       ✓      ✓         DEL         DEL    DEL  
```

#### Addis Ai
- **Latency**: 9.25s | **Ref Words**: 35 | **Errors**: 21 (S: 18, D: 3, I: 0)
- **WER**: **60.0%** | **Word Accuracy**: **40.0%** | **CER**: 61.0%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን     ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain     አልተሰማኝም   perfectly   fine    ነኝ     
HYP : አዎ   ወስጃለሁ   ---     ዲሊ    አይፋኪኒን   ጠዋት   ላይ   ዊዝ     ፈርሽሊ      ስኩዊዝድ      ኦረንጅ     ውስጥ     ነው   የወሰድኩት   አይሮን   አብዞብሰንኑን       ይጨምራል   ብለውኝ   ካልሲየሙን      ግን   የስተዴይ       ማታ   ወስጀዋለሁ   ዛሬም   አፍተር    ዲነር      ወስደዋለሁ    እስካሁን   ምንም   ---       ስተማክቴን   አልተሰማኝም   ---         ፐርፌክት   የፈውንድ  
EVAL: ✓    ✓       DEL     SUB   SUB      ✓     ✓    SUB    SUB       SUB        SUB      SUB     ✓    ✓        SUB    SUB            ✓       ✓      SUB         ✓    SUB         ✓    SUB      ✓     SUB     SUB      SUB       ✓       ✓     DEL       SUB      ✓         DEL         SUB     SUB    
```

#### Gemini
- **Latency**: 64.47s | **Ref Words**: 35 | **Errors**: 5 (S: 4, D: 1, I: 0)
- **WER**: **14.3%** | **Word Accuracy**: **85.7%** | **CER**: 6.8%

```text
REF : አዎ    ወስጃለሁ   daily   ifa       ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
HYP : ---   ወስጃለሁ   daily   vitamin   ኤን     ጧት    ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   ወስጄዋለሁ    እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
EVAL: DEL   ✓       ✓       SUB       SUB    SUB   ✓    ✓      ✓         ✓          ✓        ✓       ✓    ✓        ✓      ✓              ✓       ✓      ✓           ✓    ✓           ✓    ✓        ✓     ✓       ✓        SUB       ✓       ✓     ✓         ✓      ✓         ✓           ✓      ✓   
```

---

### Voice: `v10.wav`
> **Ground Truth Reference**:
> *ምንም serious pain የለብኝም ግን the heartburn እና acid reflux በጣም severe ሆኗል። night time ላይ sleep መተኛት አልቻልኩም፤ two pillows አድርጌ እንኳን burning sensation ይኖረዋል። safe የሆነ antacid syrup ወይም medication ከመድሃኒት ቤት መግዛት እችላለሁ ወይስ prescription ያስፈልጋል?*

#### Sahara
- **Latency**: 5.57s | **Ref Words**: 39 | **Errors**: 11 (S: 7, D: 3, I: 1)
- **WER**: **28.2%** | **Word Accuracy**: **71.8%** | **CER**: 10.4%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና    acid   reflux   በጣም   severe   ሆኗል   night   time        ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   ---   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት    መግዛት   እችላለሁ   ወይስ   prescription    ያስፈልጋል  
HYP : ምንም   serious   pain   የለብኝም   ግን   ---   ደሃር         በንና   acid   reflux   በጣም   severe   ሆኗል   ---     nighttime   ላይ   sleep   መተኛት   አልቻልኩም   two   pilos     አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   ant   acid      syrop   ወይም   medication   ከመድሃኒት   ---   መግዛት   እችላለሁ   ወይስ   screscription   ያስፈልጋል  
EVAL: ✓     ✓         ✓      ✓       ✓    DEL   SUB         SUB   ✓      ✓        ✓     ✓        ✓     DEL     SUB         ✓    ✓       ✓      ✓        ✓     SUB       ✓      ✓      ✓         ✓           ✓       ✓      ✓     INS   SUB       SUB     ✓     ✓            ✓        DEL   ✓      ✓       ✓     SUB             ✓       
```

#### Addis Ai
- **Latency**: 14.18s | **Ref Words**: 39 | **Errors**: 21 (S: 20, D: 1, I: 0)
- **WER**: **53.8%** | **Word Accuracy**: **46.2%** | **CER**: 63.0%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ    prescription   ያስፈልጋል  
HYP : ምንም   ሲሪየስ      ፔይን    የለብኝም   ግን   ---   ድሃርበን       እና   አሲድ    ሪፍሌክስ    በጣም   ስቪር      ሆኗል   ናይት     ታይም    ላይ   ስሊፕ     መተኛት   አልቻልኩም   ቱ     ፒሎውዝ      አድርጌ   እንኳን   በርኒንግ     ሴንሴሽን       ይኖረዋል   ሴፍ     የሆነ   አንታሲድ     ሲሮፕ     ወይም   ሜዲኬሽን        ከመድሃኒት   ቤት   መግዛት   ትችላለህ   በውስጥ   ስክሪፕሽን         ያስፈልጋል  
EVAL: ✓     SUB       SUB    ✓       ✓    DEL   SUB         ✓    SUB    SUB      ✓     SUB      ✓     SUB     SUB    ✓    SUB     ✓      ✓        SUB   SUB       ✓      ✓      SUB       SUB         ✓       SUB    ✓     SUB       SUB     ✓     SUB          ✓        ✓    ✓      SUB     SUB    SUB            ✓       
```

#### Gemini
- **Latency**: 37.65s | **Ref Words**: 39 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **7.7%** | **Word Accuracy**: **92.3%** | **CER**: 0.5%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time        ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   ---     nighttime   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድኃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
EVAL: ✓     ✓         ✓      ✓       ✓    ✓     ✓           ✓    ✓      ✓        ✓     ✓        ✓     DEL     SUB         ✓    ✓       ✓      ✓        ✓     ✓         ✓      ✓      ✓         ✓           ✓       ✓      ✓     ✓         ✓       ✓     ✓            SUB      ✓    ✓      ✓       ✓     ✓              ✓       
```

---

### Voice: `v11.wav`
> **Ground Truth Reference**:
> *አዎ ዛሬ morning ላይ ከ breakfast በኋላ the iron and folic acid tablet ወስጃለሁ። ግን calcium tabletቱን ማታ ከመተኛቴ በፊት ነው የምወስደው፤ ምክንያቱም simultaneously ከወሰድኳቸው severe nausea እና mild constipation ይፈጥርብኛል። doctorሩም separate አድርጌ እንድወስድ ነግሮኛል፣ so far strictly scheduleሩን እየተከተልኩ ነው።*

#### Sahara
- **Latency**: 14.53s | **Ref Words**: 42 | **Errors**: 13 (S: 10, D: 3, I: 0)
- **WER**: **30.9%** | **Word Accuracy**: **69.0%** | **CER**: 17.4%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron         and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው     
HYP : አዎ   ዛሬ   morning   ላይ   ከ    ---         ---   ---   breakfalan   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tableቱን    ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   cymmultenacy     ከወሰድኳቸው   severe   nazea    እና   mild   constipation   ይፈጥርብኛል   doctor     suprit     አድርጌ   እንዲወስድ   ነግሮኛል   so   far   strictly   schedule     roon      እየተከተ  
EVAL: ✓    ✓    ✓         ✓    ✓    DEL         DEL   DEL   SUB          ✓     ✓       ✓      ✓        ✓       ✓    ✓         SUB        ✓    ✓       ✓     ✓    ✓        ✓        SUB              ✓         ✓        SUB      ✓    ✓      ✓              ✓         SUB        SUB        ✓      SUB      ✓       ✓    ✓     ✓          SUB          SUB       SUB    
```

#### Addis Ai
- **Latency**: 6.35s | **Ref Words**: 42 | **Errors**: 23 (S: 20, D: 3, I: 0)
- **WER**: **54.8%** | **Word Accuracy**: **45.2%** | **CER**: 61.0%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ     breakfast   በኋላ   the   iron   and    folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so    far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   ሞኒንግ      ላይ   ---   ከብሬክፈስት     በኋላ   ---   ዘ      አይረን   አንፎሊክ   አሴት    ታብሌት     ወስጃለው   ግን   ካልሲየም     ታብሌቱን      ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   ሲማልቴኒሲ           ከወሰድኳቸው   ---      ስቪርናዚያ   እና   ማይልድ   ኮንስቲፔሽን        ይፈጥርብኛል   ዶክተሩም      ሰፕራይት      አድርጌ   እንድወስድ   ነግሮኛል   ሶ     ፋር    ስትሪክሊ      ስካጁዋሉን       እየተከተልኩ   ነው  
EVAL: ✓    ✓    SUB       ✓    DEL   SUB         ✓     DEL   SUB    SUB    SUB     SUB    SUB      SUB     ✓    SUB       SUB        ✓    ✓       ✓     ✓    ✓        ✓        SUB              ✓         DEL      SUB      ✓    SUB    SUB            ✓         SUB        SUB        ✓      ✓        ✓       SUB   SUB   SUB        SUB          ✓         ✓   
```

#### Gemini
- **Latency**: 9.59s | **Ref Words**: 42 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **7.1%** | **Word Accuracy**: **92.9%** | **CER**: 3.7%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወስድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   ዶክተሩም      separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleኡን   እየተከተልኩ   ነው  
EVAL: ✓    ✓    ✓         ✓    ✓    ✓           ✓     ✓     ✓      ✓     ✓       ✓      ✓        ✓       ✓    ✓         ✓          ✓    ✓       ✓     ✓    ✓        ✓        ✓                SUB       ✓        ✓        ✓    ✓      ✓              ✓         SUB        ✓          ✓      ✓        ✓       ✓    ✓     ✓          SUB          ✓         ✓   
```

---

### Voice: `v12.wav`
> **Ground Truth Reference**:
> *ዛሬ morning ጀምሮ the fetal kick በጣም decrease አድርጓል። normally after breakfast very active ነበር የሚሆነው፤ ዛሬ ግን hardly any movement ተሰማኝ። cold juice ጠጥቼ ቆይቻለሁ ግን still quiet ነው። please hospital emergency triage መሄድ አለብኝ ወይስ ትንሽ ልጠብቅ?*

#### Sahara
- **Latency**: 4.55s | **Ref Words**: 39 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **10.3%** | **Word Accuracy**: **89.7%** | **CER**: 5.0%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice     ጠጥቼ   ቆይቻለሁ   ግን   still   quiet    ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normly     after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   ---    coljust   ጠጥቼ   ቆይቻለሁ   ግን   still   quarte   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
EVAL: ✓    ✓         ✓     ✓     ✓       ✓      ✓     ✓          ✓       SUB        ✓       ✓           ✓      ✓        ✓     ✓       ✓    ✓    ✓        ✓     ✓          ✓      DEL    SUB       ✓     ✓       ✓    ✓       SUB      ✓    ✓        ✓          ✓           ✓        ✓     ✓      ✓     ✓     ✓     
```

#### Addis Ai
- **Latency**: 6.7s | **Ref Words**: 39 | **Errors**: 22 (S: 21, D: 0, I: 1)
- **WER**: **56.4%** | **Word Accuracy**: **43.6%** | **CER**: 68.7%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ   ---  
HYP : ዛሬ   ሞኒንግ      ጀምሮ   ዘ     ፊታል     ኪክ     በጣም   ዲክሪስ       አድርጓል   ኖርማሊ       አፍተር    ብሬክፋስት      በሪ     አክቲቭ     ነበር   የሚሆነው   ዛሬ   ግን   ሃርድሊ     ኤኒ    ሙቭመንት      ተሰማኝ   ኮል     ጁስ      ጠጥቼ   ቆይቻለሁ   ግን   ስቲል     ኳየት     ነው   ፕሊዝ      ሆስፒታል      ኢመርጀንሲ      ትራያጅ     መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ   እ    
EVAL: ✓    SUB       ✓     SUB   SUB     SUB    ✓     SUB        ✓       SUB        SUB     SUB         SUB    SUB      ✓     ✓       ✓    ✓    SUB      SUB   SUB        ✓      SUB    SUB     ✓     ✓       ✓    SUB     SUB     ✓    SUB      SUB        SUB         SUB      ✓     ✓      ✓     ✓     ✓      INS  
```

#### Gemini
- **Latency**: 27.04s | **Ref Words**: 39 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **5.1%** | **Word Accuracy**: **94.9%** | **CER**: 3.3%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   ጁስ      ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠበቅ  
EVAL: ✓    ✓         ✓     ✓     ✓       ✓      ✓     ✓          ✓       ✓          ✓       ✓           ✓      ✓        ✓     ✓       ✓    ✓    ✓        ✓     ✓          ✓      ✓      SUB     ✓     ✓       ✓    ✓       ✓       ✓    ✓        ✓          ✓           ✓        ✓     ✓      ✓     ✓     SUB   
```

---

### Voice: `v13.wav`
> **Ground Truth Reference**:
> *ዛሬ lower back pain እና pelvic pressure በጣም ይሰማኛል፣ especially ስራ ላይ standing for a long time ስሆን unbearable ይሆናል። fetal movement ግን active ነው፣ baby normal kick እያደረገ ነው። ይሄ normal third-trimester symptom ነው ወይስ doctorሩን emergency ማናገር አለብኝ?*

#### Sahara
- **Latency**: 5.68s | **Ref Words**: 41 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **4.9%** | **Word Accuracy**: **95.1%** | **CER**: 1.6%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   unbarable    ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctor     emergency   ማናገር   አለብኝ  
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            ✓    ✓    ✓          ✓     ✓    ✓      ✓      ✓     SUB          ✓      ✓       ✓          ✓    ✓        ✓    ✓      ✓        ✓      ✓       ✓    ✓    ✓        ✓       ✓           ✓         ✓    ✓     SUB        ✓           ✓      ✓     
```

#### Addis Ai
- **Latency**: 9.47s | **Ref Words**: 41 | **Errors**: 25 (S: 25, D: 0, I: 0)
- **WER**: **61.0%** | **Word Accuracy**: **39.0%** | **CER**: 74.1%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a     long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   ሎወር     ባክ     ፔን     እና   ፔልቪክ     ፕሬሸር       በጣም   ይሰማኛል   ስፔሻሊ         ስራ   ላይ   ስታንዲንግ     ፎር    ኤ     ሎንግ    ታይም    ሲሆን   አንቤረቦ        ይሆናል   ፊታል     ሙቭመንት      ግን   አክቲቭ     ነው   ቤቢ     ኖርማል     ኪክ     እያደረገ   ነው   ይሄ   ኖርማል     ተርድ     ትራይሚስተር     ሲምፕትም     ነው   ወይስ   ዶክተሩን      ኢመርጀንሲ      ማናገር   አለብኝ  
EVAL: ✓    SUB     SUB    SUB    ✓    SUB      SUB        ✓     ✓       SUB          ✓    ✓    SUB        SUB   SUB   SUB    SUB    SUB   SUB          ✓      SUB     SUB        ✓    SUB      ✓    SUB    SUB      SUB    ✓       ✓    ✓    SUB      SUB     SUB         SUB       ✓    ✓     SUB        SUB         ✓      ✓     
```

#### Gemini
- **Latency**: 18.24s | **Ref Words**: 41 | **Errors**: 11 (S: 2, D: 9, I: 0)
- **WER**: **26.8%** | **Word Accuracy**: **73.2%** | **CER**: 27.5%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ    ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው    ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ሥራ    ላይ   standing   for   a    long   time   ሲሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   ---     ---         ---       ---   ---   ---        ---         ---    ---   
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            SUB   ✓    ✓          ✓     ✓    ✓      ✓      SUB   ✓            ✓      ✓       ✓          ✓    ✓        ✓    ✓      ✓        ✓      ✓       ✓    ✓    ✓        DEL     DEL         DEL       DEL   DEL   DEL        DEL         DEL    DEL   
```

---

### Voice: `v14.wav`
> **Ground Truth Reference**:
> *ዛሬ taken አድርጌያለሁ፣ but yesterday ሙሉ ቀን ስራ ስለነበርኩ the calcium supplementቱን መውሰድ forget አድርጌ ነበር። ዛሬ double dose መውሰድ አለብኝ ወይስ just continue with one tablet? IFAውን ግን today as usual ጠዋት ወስጃለሁ፣ no complications።*

#### Sahara
- **Latency**: 4.55s | **Ref Words**: 36 | **Errors**: 12 (S: 9, D: 3, I: 0)
- **WER**: **33.3%** | **Word Accuracy**: **66.7%** | **CER**: 30.5%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as    usual   ጠዋት    ወስጃለሁ   no   complications  
HYP : ዛሬ   tech    አድርጌያለሁ   ---   በትርዴ        ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplement     መውሰድ   ፍግያ      አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   አይፈውን   ግን   ---     ---   ትዴ      አዝዋት   ወስጃለው   no   camp           
EVAL: ✓    SUB     ✓         DEL   SUB         ✓    ✓    ✓    ✓        ✓     ✓         SUB            ✓      SUB      ✓      ✓     ✓    ✓        ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        SUB     ✓    DEL     DEL   SUB     SUB    SUB     ✓    SUB            
```

#### Addis Ai
- **Latency**: 6.25s | **Ref Words**: 36 | **Errors**: 21 (S: 21, D: 0, I: 0)
- **WER**: **58.3%** | **Word Accuracy**: **41.7%** | **CER**: 65.9%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as    usual   ጠዋት   ወስጃለሁ   no    complications  
HYP : ዛሬ   ቴክ      አድርጌያለሁ   በት    ይስተርዴይ      ሙሉ   ቀን   ስራ   ስለነገርኩ   ዘ     ካልሲየም     ሳፕልመንቱን        መውሰድ   ፍጌ       አድርጌ   ነበር   ዛሬ   ዳብል      ዶስ     መውሰድ   አለብኝ   ወይስ   ጀስት    ኮንቲኒው      ዊዝ     ዋን    ታብሌት     አይሆን    ግን   ቱዴይ     አዝ    ዩዙዋል    ጠዋት   ወስጃለሁ   ኖ     ኮምፕሊኬሽንስ       
EVAL: ✓    SUB     ✓         SUB   SUB         ✓    ✓    ✓    SUB      SUB   SUB       SUB            ✓      SUB      ✓      ✓     ✓    SUB      SUB    ✓      ✓      ✓     SUB    SUB        SUB    SUB   SUB      SUB     ✓    SUB     SUB   SUB     ✓     ✓       SUB   SUB            
```

#### Gemini
- **Latency**: 42.63s | **Ref Words**: 36 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **11.1%** | **Word Accuracy**: **88.9%** | **CER**: 5.4%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium    supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን    ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
HYP : ዛሬ   take    አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   ---   የcalcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   iphone   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
EVAL: ✓    SUB     ✓         ✓     ✓           ✓    ✓    ✓    ✓        DEL   SUB        ✓              ✓      ✓        ✓      ✓     ✓    ✓        ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        SUB      ✓    ✓       ✓    ✓       ✓     ✓       ✓    ✓              
```

---

### Voice: `v15.wav`
> **Ground Truth Reference**:
> *ዛሬማ ገና አልወሰድኩም እኮ። ጠዋት morning sicknessሱ በጣም አስቸግሮኝ vomit ሳደርግ ነው የረፈደው፤ empty stomach መውሰድ አልቻልኩም። አሁን after lunch ትንሽ ሻል ሲለኝ the daily IFA supplementቱን ከብዙ water ጋር እወስደዋለሁ። calcium ደሞ አብሬ ልውሰደው ወይስ gap ልስጠው?*

#### Sahara
- **Latency**: 7.57s | **Ref Words**: 38 | **Errors**: 12 (S: 7, D: 5, I: 0)
- **WER**: **31.6%** | **Word Accuracy**: **68.4%** | **CER**: 35.1%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል    ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   ሲክነሱ        በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   ---     ---       መውሰድ   አልቻልኩም   አሁን   ---     አፍትለኝ   ትንሽ   አል    ሲለኝ   the   daily   ---   አይፍሊምንቱን       ከብዙ   water   ጋር   እወስደዋለሁ   ካልሲየም     ደግሞ   አብሬ   ልውሰደው   ወይስ   ---   ጋብ    
EVAL: ✓     ✓    ✓         ✓    ✓     ✓         SUB         ✓     ✓        ✓       ✓      ✓    ✓       DEL     DEL       ✓      ✓        ✓     DEL     SUB     ✓     SUB   ✓     ✓     ✓       DEL   SUB            ✓     ✓       ✓    ✓         SUB       SUB   ✓     ✓       ✓     DEL   SUB   
```

#### Addis Ai
- **Latency**: 5.48s | **Ref Words**: 38 | **Errors**: 18 (S: 15, D: 0, I: 3)
- **WER**: **47.4%** | **Word Accuracy**: **52.6%** | **CER**: 52.4%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   ---    ---    ---    vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   ሞኒንግ      ሲከነሱ        በጣም   አስቸግሮኝ   0xe1   0x89   0xae   ሚት      ሳደርግ   ነው   የረፈደው   እምቲስ    ታመክ       መውሰድ   አልቻልኩም   አሁን   አፍት     ለንች     ትንሽ   ሻል   ሲለኝ   ዘ     ዴይሊ     አይፍ   ሳፕለመንቱን        ከብዙ   ወተር     ጋር   እወስደዋለሁ   ካልሲየም     ደግሞ   አብሬ   ልውሰደው   ወይስ   ጋፕ    ልስጠው  
EVAL: ✓     ✓    ✓         ✓    ✓     SUB       SUB         ✓     ✓        INS    INS    INS    SUB     ✓      ✓    ✓       SUB     SUB       ✓      ✓        ✓     SUB     SUB     ✓     ✓    ✓     SUB   SUB     SUB   SUB            ✓     SUB     ✓    ✓         SUB       SUB   ✓     ✓       ✓     SUB   ✓     
```

#### Gemini
- **Latency**: 44.49s | **Ref Words**: 38 | **Errors**: 9 (S: 9, D: 0, I: 0)
- **WER**: **23.7%** | **Word Accuracy**: **76.3%** | **CER**: 8.3%

```text
REF : ዛሬማ   ገና      አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   ifa    supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬ    magna   አልወሰድኩም   እኮ   ጧት    morning   sicknessኡ   በጣም   አስቸግሮኝ   vomit   ሳደርግ   ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   life   supplementኡን   ከብዙ   water   ጋር   ወስደዋለሁ    calcium   ደግሞ   አብሬ   ልውሰደው   ወይስ   gap   ልስተው  
EVAL: SUB   SUB     ✓         ✓    SUB   ✓         SUB         ✓     ✓        ✓       ✓      ✓    ✓       ✓       ✓         ✓      ✓        ✓     ✓       ✓       ✓     ✓    ✓     ✓     ✓       SUB    SUB            ✓     ✓       ✓    SUB       ✓         SUB   ✓     ✓       ✓     ✓     SUB   
```

---

### Voice: `v16.wav`
> **Ground Truth Reference**:
> *እግሬ በጣም እያበጠ ነው፤ today both feet ላይ severe swelling አለ፣ ጫማዬም አልገባ ብሎኛል። ከዚህም በተጨማሪ mild headache አለኝ። BPዬ high ሆኖ እንዳይሆን ፈርቻለሁ፤ nearby clinic ሄጄ blood pressure check ማድረግ አለብኝ ወይስ tomorrow morning መምጣት ይሻላል?*

#### Sahara
- **Latency**: 5.37s | **Ref Words**: 37 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **10.8%** | **Word Accuracy**: **89.2%** | **CER**: 7.9%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   today   ቦት     ፊት     ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   ---   bp     ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
EVAL: ✓     ✓     ✓      ✓    ✓       SUB    SUB    ✓    ✓        ✓          ✓    ✓      ✓      ✓      ✓      ✓       ✓      ✓          ✓     DEL   SUB    ✓    ✓        ✓       ✓        ✓        ✓    ✓       ✓          ✓       ✓      ✓      ✓     ✓          ✓         ✓      ✓     
```

#### Addis Ai
- **Latency**: 5.22s | **Ref Words**: 37 | **Errors**: 18 (S: 17, D: 0, I: 1)
- **WER**: **48.6%** | **Word Accuracy**: **51.3%** | **CER**: 57.0%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ---   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   ቱዴይ     ቦት     ፊት     ላይ   ሰገር      ስወልኝ       አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   ማይል    ሀዴግ        አለኝ   ቢፒ    ሃይ     ሆኖ   እንዳይሆን   ፈርቻለሁ   ኔርባይ     ክሊኒክ     ሄጄ   ብላድ     ፕረሽር       ቼክ      ማድረግ   አለብኝ   ወይስ   ትሞሮ        ሞኒንግ      መምጣት   አስ    ሻላ    
EVAL: ✓     ✓     ✓      ✓    SUB     SUB    SUB    ✓    SUB      SUB        ✓    ✓      ✓      ✓      ✓      ✓       SUB    SUB        ✓     SUB   SUB    ✓    ✓        ✓       SUB      SUB      ✓    SUB     SUB        SUB     ✓      ✓      ✓     SUB        SUB       ✓      INS   SUB   
```

#### Gemini
- **Latency**: 16.69s | **Ref Words**: 37 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
HYP : እግሬ   በጣም   እያበጠ   ነው   today   both   feet   ላይ   severe   swelling   አለ   ጫማዬም   አልገባ   ብሎኛል   ከዚህም   በተጨማሪ   mild   headache   አለኝ   bpዬ   high   ሆኖ   እንዳይሆን   ፈርቻለሁ   nearby   clinic   ሄጄ   blood   pressure   check   ማድረግ   አለብኝ   ወይስ   tomorrow   morning   መምጣት   ይሻላል  
EVAL: ✓     ✓     ✓      ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓    ✓      ✓      ✓      ✓      ✓       ✓      ✓          ✓     ✓     ✓      ✓    ✓        ✓       ✓        ✓        ✓    ✓       ✓          ✓       ✓      ✓      ✓     ✓          ✓         ✓      ✓     
```

---

### Voice: `v17.wav`
> **Ground Truth Reference**:
> *እኔ የ folic acid እና iron supplementቱን correctly ወስጃለሁ፣ ምንም side effect የለብኝም። ግን the calcium tablets አልቀውብኛል፤ ባለፈው clinic ስሄድ pharmacy ውስጥ out of stock ነበር ያሉት። ዛሬ private pharmacy ፈልጌ መግዛት አለብኝ ወይስ next appointment ድረስ መጠበቅ እችላለሁ?*

#### Sahara
- **Latency**: 5.65s | **Ref Words**: 40 | **Errors**: 5 (S: 3, D: 2, I: 0)
- **WER**: **12.5%** | **Word Accuracy**: **87.5%** | **CER**: 8.1%

```text
REF : እኔ   የ    folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplement     correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   ---   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmcy    ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   ነክስ    appointment   ድረስ   መጠበቅ   ---    
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      SUB            ✓           ✓       ✓     ✓      ✓        ✓       ✓    DEL   ✓         ✓         ✓         ✓      ✓        ✓     SUB        ✓     ✓     ✓    ✓       ✓     ✓     ✓    ✓         ✓          ✓     ✓      ✓      ✓     SUB    ✓             ✓     ✓      DEL    
```

#### Addis Ai
- **Latency**: 5.48s | **Ref Words**: 40 | **Errors**: 20 (S: 19, D: 1, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 60.8%

```text
REF : እኔ   የ     folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of    stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   ---   የፎሊክ    አሲድ    እና   አይሮን   ሳፕለመንቱን        ኮሬክትሊ       ወስጃለሁ   ምንም   ሳይድ    ኢፌክት     የለብኝም   ግን   ዘ     ካልሲየም     ታብለስ      አልቀውብኛል   ባለፈው   ክሊኒክ     ስሄድ   ፋርማሲ       ውስጥ   አውት   ኦፍ    ስቶክ     ነበር   ያሉት   ዛሬ   ፕራይቬት     ፋርማሲ       ፈልጌ   መግዛት   አለብኝ   ወይስ   ኔክስት   አፖይንትመንት      ድረስ   መጠበቅ   እችላለሁ  
EVAL: ✓    DEL   SUB     SUB    ✓    SUB    SUB            SUB         ✓       ✓     SUB    SUB      ✓       ✓    SUB   SUB       SUB       ✓         ✓      SUB      ✓     SUB        ✓     SUB   SUB   SUB     ✓     ✓     ✓    SUB       SUB        ✓     ✓      ✓      ✓     SUB    SUB           ✓     ✓      ✓      
```

#### Gemini
- **Latency**: 32.23s | **Ref Words**: 40 | **Errors**: 3 (S: 3, D: 0, I: 0)
- **WER**: **7.5%** | **Word Accuracy**: **92.5%** | **CER**: 3.2%

```text
REF : እኔ   የ    folic   acid   እና   iron   supplementቱን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   the   calcium   tablets   አልቀውብኛል   ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
HYP : እኔ   የ    folic   acid   እና   iron   supplementኡን   correctly   ወስጃለሁ   ምንም   side   effect   የለብኝም   ግን   የ     calcium   tablets   አልቆብኛል    ባለፈው   clinic   ስሄድ   pharmacy   ውስጥ   out   of   stock   ነበር   ያሉት   ዛሬ   private   pharmacy   ፈልጌ   መግዛት   አለብኝ   ወይስ   next   appointment   ድረስ   መጠበቅ   እችላለሁ  
EVAL: ✓    ✓    ✓       ✓      ✓    ✓      SUB            ✓           ✓       ✓     ✓      ✓        ✓       ✓    SUB   ✓         ✓         SUB       ✓      ✓        ✓     ✓          ✓     ✓     ✓    ✓       ✓     ✓     ✓    ✓         ✓          ✓     ✓      ✓      ✓     ✓      ✓             ✓     ✓      ✓      
```

---

### Voice: `v18.wav`
> **Ground Truth Reference**:
> *ዛሬ afternoon ላይ lower abdomenኔ tight እያደረገ frequent cramps ይሰማኛል፣ like period pain። intervalሉ ግን regular አይደለም። these are just Braxton Hicks contractions or early labor signs መሆናቸውን distinguish ማድረግ አልቻልኩም። what other warning signs should I monitor?*

#### Sahara
- **Latency**: 3.78s | **Ref Words**: 38 | **Errors**: 10 (S: 6, D: 4, I: 0)
- **WER**: **26.3%** | **Word Accuracy**: **73.7%** | **CER**: 18.4%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs     መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i     monitor  
HYP : ዛሬ   afternoon   ላይ   ---     ለወር        tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalu   ግን   regular   አይደለም   these   are   just   bruxton   hicks   contractions   or   early   labor   science   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   adder   warning   ---     ---      ---   science  
EVAL: ✓    ✓           ✓    DEL     SUB        ✓       ✓       ✓          ✓        ✓       ✓      ✓        ✓      SUB         ✓    ✓         ✓       ✓       ✓     ✓      SUB       ✓       ✓              ✓    ✓       ✓       SUB       ✓        ✓             ✓      ✓        ✓      SUB     ✓         DEL     DEL      DEL   SUB      
```

#### Addis Ai
- **Latency**: 5.22s | **Ref Words**: 38 | **Errors**: 29 (S: 29, D: 0, I: 0)
- **WER**: **76.3%** | **Word Accuracy**: **23.7%** | **CER**: 81.2%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or    early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i     monitor  
HYP : ዛሬ   አፍትኑ        ላይ   ሎወር     አብደመኔ      ታይት     እያደረገ   ፍሪኩዌንት     ክራምፕስ    ይሰማኛል   ላይክ    ፒሪዮድ     ፔይን    ኢንተርቫሉ      ግን   ሬጉለር      አይደለም   ዚዝ      አር    ጀስት    ብራክስተን    ሂክስ     ኮንትራክሽንስ       ኦር    እርሊ     ሌበር     ሳይንስ    መሆናቸውን   ዲስቲንጉሽ        ማድረግ   አልቻልኩም   ዋት     አዘር     ዎርኒንግ     ሳይንስ    ሹድ       አይ    ሞኒተር     
EVAL: ✓    SUB         ✓    SUB     SUB        SUB     ✓       SUB        SUB      ✓       SUB    SUB      SUB    SUB         ✓    SUB       ✓       SUB     SUB   SUB    SUB       SUB     SUB            SUB   SUB     SUB     SUB     ✓        SUB           ✓      ✓        SUB    SUB     SUB       SUB     SUB      SUB   SUB      
```

#### Gemini
- **Latency**: 26.15s | **Ref Words**: 38 | **Errors**: 4 (S: 4, D: 0, I: 0)
- **WER**: **10.5%** | **Word Accuracy**: **89.5%** | **CER**: 11.1%

```text
REF : ዛሬ   afternoon   ላይ   lower   abdomenኔ   tight   እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   intervalሉ   ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
HYP : ዛሬ   አፍተርኑን      ላይ   lower   abdomen    ታይት     እያደረገ   frequent   cramps   ይሰማኛል   like   period   pain   ኢንተርቫሉ      ግን   regular   አይደለም   these   are   just   braxton   hicks   contractions   or   early   labor   signs   መሆናቸውን   distinguish   ማድረግ   አልቻልኩም   what   other   warning   signs   should   i    monitor  
EVAL: ✓    SUB         ✓    ✓       SUB        SUB     ✓       ✓          ✓        ✓       ✓      ✓        ✓      SUB         ✓    ✓         ✓       ✓       ✓     ✓      ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓             ✓      ✓        ✓      ✓       ✓         ✓       ✓        ✓    ✓        
```

---

### Voice: `v19.wav`
> **Ground Truth Reference**:
> *አዎ ወስጃለሁ፣ daily IFA ኪኒኑን ጠዋት ላይ with freshly squeezed orange juice ነው የወሰድኩት፣ iron absorptionኑን ይጨምራል ብለውኝ። calciumሙን ግን yesterday ማታ ወስጄዋለሁ፤ ዛሬም after dinner እወስደዋለሁ። እስካሁን ምንም stomach pain አልተሰማኝም፣ perfectly fine ነኝ።*

#### Sahara
- **Latency**: 4.09s | **Ref Words**: 35 | **Errors**: 9 (S: 8, D: 1, I: 0)
- **WER**: **25.7%** | **Word Accuracy**: **74.3%** | **CER**: 17.5%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange    juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ   
HYP : አዎ   ወስጃለው   daily   አይፋ   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orrange   juice   ነው   የወሰድኩት   iron   absorbeኑን      ይጨምራል   ብለውኝ   ካልሲያሙን      ግን   የስቴ         ማታ   ወስጄዋለሁ   ዛሬም   after   dine     ወስደዋለሁ    እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ---  
EVAL: ✓    SUB     ✓       SUB   ✓      ✓     ✓    ✓      ✓         ✓          SUB       ✓       ✓    ✓        ✓      SUB            ✓       ✓      SUB         ✓    SUB         ✓    ✓        ✓     ✓       SUB      SUB       ✓       ✓     ✓         ✓      ✓         ✓           ✓      DEL  
```

#### Addis Ai
- **Latency**: 5.08s | **Ref Words**: 35 | **Errors**: 19 (S: 18, D: 1, I: 0)
- **WER**: **54.3%** | **Word Accuracy**: **45.7%** | **CER**: 59.9%

```text
REF : አዎ   ወስጃለሁ   daily   ifa   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner   እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ   
HYP : አዎ   ወስጃለሁ   ዴሊ      አይፋ   ኪኒኑን   ጠዋት   ላይ   ዊዝ     ፍሬሽሊ      ስኩዊዝድ      ኦረንጅ     ጁስ      ነው   የወሰድኩት   አይሮን   አብዞብሰኑን        ይጨምራል   ብለውኝ   ካልሲያሙን      ግን   የስተዴ        ማታ   ወስጄዋለሁ   ዛሬም   ---     አፍተዲና    ወስደዋለሁ    እስካሁን   ምንም   ስታማክ      ፔን     አልተሰማኝም   አስፈላጊ       ይሆናል   እኔ   
EVAL: ✓    ✓       SUB     SUB   ✓      ✓     ✓    SUB    SUB       SUB        SUB      SUB     ✓    ✓        SUB    SUB            ✓       ✓      SUB         ✓    SUB         ✓    ✓        ✓     DEL     SUB      SUB       ✓       ✓     SUB       SUB    ✓         SUB         SUB    SUB  
```

#### Gemini
- **Latency**: 30.13s | **Ref Words**: 35 | **Errors**: 7 (S: 5, D: 2, I: 0)
- **WER**: **20.0%** | **Word Accuracy**: **80.0%** | **CER**: 6.8%

```text
REF : አዎ    ወስጃለሁ    daily   ifa    ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወሰድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   after   dinner      እወስደዋለሁ   እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
HYP : ---   አወስጃለሁ   daily   iron   ኪኒኑን   ጠዋት   ላይ   with   freshly   squeezed   orange   juice   ነው   የወስድኩት   iron   absorptionኑን   ይጨምራል   ብለውኝ   calciumሙን   ግን   yesterday   ማታ   ወስጄዋለሁ   ዛሬም   ---     afternoon   ወስጄዋለሁ    እስካሁን   ምንም   stomach   pain   አልተሰማኝም   perfectly   fine   ነኝ  
EVAL: DEL   SUB      ✓       SUB    ✓      ✓     ✓    ✓      ✓         ✓          ✓        ✓       ✓    SUB      ✓      ✓              ✓       ✓      ✓           ✓    ✓           ✓    ✓        ✓     DEL     SUB         SUB       ✓       ✓     ✓         ✓      ✓         ✓           ✓      ✓   
```

---

### Voice: `v20.wav`
> **Ground Truth Reference**:
> *ምንም serious pain የለብኝም ግን the heartburn እና acid reflux በጣም severe ሆኗል። night time ላይ sleep መተኛት አልቻልኩም፤ two pillows አድርጌ እንኳን burning sensation ይኖረዋል። safe የሆነ antacid syrup ወይም medication ከመድሃኒት ቤት መግዛት እችላለሁ ወይስ prescription ያስፈልጋል?*

#### Sahara
- **Latency**: 4.04s | **Ref Words**: 39 | **Errors**: 9 (S: 8, D: 1, I: 0)
- **WER**: **23.1%** | **Word Accuracy**: **76.9%** | **CER**: 12.0%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time      ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም    medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል   
HYP : ምንም   serious   pain   የለብኝም   ግን   ደሀድ   ብር          እና   acid   reflux   በጣም   severe   ሆኗል   ---     nightim   ላይ   sleep   መተኛት   አልቻልኩም   2     pilos     አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrop   ወይንም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልገናል  
EVAL: ✓     ✓         ✓      ✓       ✓    SUB   SUB         ✓    ✓      ✓        ✓     ✓        ✓     DEL     SUB       ✓    ✓       ✓      ✓        SUB   SUB       ✓      ✓      ✓         ✓           ✓       ✓      ✓     ✓         SUB     SUB    ✓            ✓        ✓    ✓      ✓       ✓     ✓              SUB      
```

#### Addis Ai
- **Latency**: 5.22s | **Ref Words**: 39 | **Errors**: 20 (S: 19, D: 1, I: 0)
- **WER**: **51.3%** | **Word Accuracy**: **48.7%** | **CER**: 62.0%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   ሲሪየስ      ፔይን    የለብኝም   ግን   ---   ድሃድበርን      እና   አሲድ    ሪፍሉክስ    በጣም   ሲቪር      ሆኗል   ናይት     ታይም    ላይ   ስሊፕ     መተኛት   አልቻልኩም   ቱ     ፒሎዝ       አድርጌ   እንኳን   ግርኒንግ     ሴንሴሽን       ይኖረዋል   ሴፍ     የሆነ   አንታሲድ     ሲሮፕ     ወይም   ሜዲኬሽን        ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ውስጥ   ፕሬስክሪፕሽን       ያስፈልጋል  
EVAL: ✓     SUB       SUB    ✓       ✓    DEL   SUB         ✓    SUB    SUB      ✓     SUB      ✓     SUB     SUB    ✓    SUB     ✓      ✓        SUB   SUB       ✓      ✓      SUB       SUB         ✓       SUB    ✓     SUB       SUB     ✓     SUB          ✓        ✓    ✓      ✓       SUB   SUB            ✓       
```

#### Gemini
- **Latency**: 35.25s | **Ref Words**: 39 | **Errors**: 4 (S: 2, D: 2, I: 0)
- **WER**: **10.3%** | **Word Accuracy**: **89.7%** | **CER**: 2.1%

```text
REF : ምንም   serious   pain   የለብኝም   ግን   the   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   night   time        ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድሃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
HYP : ምንም   serious   pain   የለብኝም   ግን   ---   heartburn   እና   acid   reflux   በጣም   severe   ሆኗል   ---     nighttime   ላይ   sleep   መተኛት   አልቻልኩም   two   pillows   አድርጌ   እንኳን   burning   sensation   ይኖረዋል   safe   የሆነ   antacid   syrup   ወይም   medication   ከመድኃኒት   ቤት   መግዛት   እችላለሁ   ወይስ   prescription   ያስፈልጋል  
EVAL: ✓     ✓         ✓      ✓       ✓    DEL   ✓           ✓    ✓      ✓        ✓     ✓        ✓     DEL     SUB         ✓    ✓       ✓      ✓        ✓     ✓         ✓      ✓      ✓         ✓           ✓       ✓      ✓     ✓         ✓       ✓     ✓            SUB      ✓    ✓      ✓       ✓     ✓              ✓       
```

---

### Voice: `v21.wav`
> **Ground Truth Reference**:
> *አዎ ዛሬ morning ላይ ከ breakfast በኋላ the iron and folic acid tablet ወስጃለሁ። ግን calcium tabletቱን ማታ ከመተኛቴ በፊት ነው የምወስደው፤ ምክንያቱም simultaneously ከወሰድኳቸው severe nausea እና mild constipation ይፈጥርብኛል። doctorሩም separate አድርጌ እንድወስድ ነግሮኛል፣ so far strictly scheduleሩን እየተከተልኩ ነው።*

#### Sahara
- **Latency**: 6.13s | **Ref Words**: 42 | **Errors**: 8 (S: 8, D: 0, I: 0)
- **WER**: **19.1%** | **Word Accuracy**: **81.0%** | **CER**: 11.0%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and   folic    acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate    አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   morning   ላይ   ከ    breakfast   በኋላ   the   iron   and   follic   acid   tablet   ወስጃለሁ   ግን   ካልሲያ      ታብሌቱን      ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nazea    እና   mild   constipation   ይፈጥርብኛል   doctor     sepretate   አድርጌ   እንዲወስድ   ነግሮኛል   so   far   strictly   schedule     እየተከተልኩ   ነው  
EVAL: ✓    ✓    ✓         ✓    ✓    ✓           ✓     ✓     ✓      ✓     SUB      ✓      ✓        ✓       ✓    SUB       SUB        ✓    ✓       ✓     ✓    ✓        ✓        ✓                ✓         ✓        SUB      ✓    ✓      ✓              ✓         SUB        SUB         ✓      SUB      ✓       ✓    ✓     ✓          SUB          ✓         ✓   
```

#### Addis Ai
- **Latency**: 5.89s | **Ref Words**: 42 | **Errors**: 23 (S: 21, D: 2, I: 0)
- **WER**: **54.8%** | **Word Accuracy**: **45.2%** | **CER**: 61.0%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ     breakfast   በኋላ   the   iron   and    folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so    far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   ሞኒንግ      ላይ   ---   ከብሬክፈስት     በኋላ   ---   ዘ      አየርን   አንፎሊክ   አሲድ    ታብሌት     ወስጃለሁ   ግን   ካልሲየም     ታብሌቱን      ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   ሲማልቴኒየስሊ         ከወሰድኳቸው   ስቪር      ናዚያ      እና   ማይልድ   ኮንስቲፔሽን        ይፈጥርብኛል   ዶክተሩ       ሰፕረቴት      አድርጌ   እንዲወስድ   ነግሮኛል   ሶ     ፋር    ስትሪክትሊ     ስኬደሩን        እየተከተልኩ   ነው  
EVAL: ✓    ✓    SUB       ✓    DEL   SUB         ✓     DEL   SUB    SUB    SUB     SUB    SUB      ✓       ✓    SUB       SUB        ✓    ✓       ✓     ✓    ✓        ✓        SUB              ✓         SUB      SUB      ✓    SUB    SUB            ✓         SUB        SUB        ✓      SUB      ✓       SUB   SUB   SUB        SUB          ✓         ✓   
```

#### Gemini
- **Latency**: 26.09s | **Ref Words**: 42 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **9.5%** | **Word Accuracy**: **90.5%** | **CER**: 3.2%

```text
REF : አዎ   ዛሬ   morning   ላይ   ከ     breakfast    በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወሰድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   doctorሩም   separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው  
HYP : አዎ   ዛሬ   morning   ላይ   ---   ከbreakfast   በኋላ   the   iron   and   folic   acid   tablet   ወስጃለሁ   ግን   calcium   tabletቱን   ማታ   ከመተኛቴ   በፊት   ነው   የምወስደው   ምክንያቱም   simultaneously   ከወስድኳቸው   severe   nausea   እና   mild   constipation   ይፈጥርብኛል   ዶክተሩም      separate   አድርጌ   እንድወስድ   ነግሮኛል   so   far   strictly   scheduleሩን   እየተከተልኩ   ነው  
EVAL: ✓    ✓    ✓         ✓    DEL   SUB          ✓     ✓     ✓      ✓     ✓       ✓      ✓        ✓       ✓    ✓         ✓          ✓    ✓       ✓     ✓    ✓        ✓        ✓                SUB       ✓        ✓        ✓    ✓      ✓              ✓         SUB        ✓          ✓      ✓        ✓       ✓    ✓     ✓          ✓            ✓         ✓   
```

---

### Voice: `v22.wav`
> **Ground Truth Reference**:
> *ዛሬ morning ጀምሮ the fetal kick በጣም decrease አድርጓል። normally after breakfast very active ነበር የሚሆነው፤ ዛሬ ግን hardly any movement ተሰማኝ። cold juice ጠጥቼ ቆይቻለሁ ግን still quiet ነው። please hospital emergency triage መሄድ አለብኝ ወይስ ትንሽ ልጠብቅ?*

#### Sahara
- **Latency**: 3.68s | **Ref Words**: 39 | **Errors**: 4 (S: 3, D: 1, I: 0)
- **WER**: **10.3%** | **Word Accuracy**: **89.7%** | **CER**: 4.4%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice     ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normly     after   breakft     very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   ---    coljust   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
EVAL: ✓    ✓         ✓     ✓     ✓       ✓      ✓     ✓          ✓       SUB        ✓       SUB         ✓      ✓        ✓     ✓       ✓    ✓    ✓        ✓     ✓          ✓      DEL    SUB       ✓     ✓       ✓    ✓       ✓       ✓    ✓        ✓          ✓           ✓        ✓     ✓      ✓     ✓     ✓     
```

#### Addis Ai
- **Latency**: 5.02s | **Ref Words**: 39 | **Errors**: 21 (S: 20, D: 1, I: 0)
- **WER**: **53.8%** | **Word Accuracy**: **46.2%** | **CER**: 68.1%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very     active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   ሞኒንግ      ጀምሮ   ዘ     ፊታል     ኪክ     በጣም   ዲክሪስ       አድርጓል   ---        ኖርማሊ    አፍተር        ብሬክፋስት   በሪአክቲቭ   ነበር   የሚሆነው   ዛሬ   ግን   ሃርሊ      ኤኒ    ሙቭመንት      ተሰማኝ   ኮልጁ    ውስጥ     ጠጥቼ   ቆይቻለሁ   ግን   ስቲል     ኳየት     ነው   ፕሊስ      ሆስፒታል      ኢመርጀንሲ      ትራያዥ     መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
EVAL: ✓    SUB       ✓     SUB   SUB     SUB    ✓     SUB        ✓       DEL        SUB     SUB         SUB      SUB      ✓     ✓       ✓    ✓    SUB      SUB   SUB        ✓      SUB    SUB     ✓     ✓       ✓    SUB     SUB     ✓    SUB      SUB        SUB         SUB      ✓     ✓      ✓     ✓     ✓     
```

#### Gemini
- **Latency**: 31.63s | **Ref Words**: 39 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **5.1%** | **Word Accuracy**: **94.9%** | **CER**: 2.2%

```text
REF : ዛሬ   morning   ጀምሮ   the   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠብቅ  
HYP : ዛሬ   morning   ጀምሮ   ---   fetal   kick   በጣም   decrease   አድርጓል   normally   after   breakfast   very   active   ነበር   የሚሆነው   ዛሬ   ግን   hardly   any   movement   ተሰማኝ   cold   juice   ጠጥቼ   ቆይቻለሁ   ግን   still   quiet   ነው   please   hospital   emergency   triage   መሄድ   አለብኝ   ወይስ   ትንሽ   ልጠበቅ  
EVAL: ✓    ✓         ✓     DEL   ✓       ✓      ✓     ✓          ✓       ✓          ✓       ✓           ✓      ✓        ✓     ✓       ✓    ✓    ✓        ✓     ✓          ✓      ✓      ✓       ✓     ✓       ✓    ✓       ✓       ✓    ✓        ✓          ✓           ✓        ✓     ✓      ✓     ✓     SUB   
```

---

### Voice: `v23.wav`
> **Ground Truth Reference**:
> *ዛሬ lower back pain እና pelvic pressure በጣም ይሰማኛል፣ especially ስራ ላይ standing for a long time ስሆን unbearable ይሆናል። fetal movement ግን active ነው፣ baby normal kick እያደረገ ነው። ይሄ normal third-trimester symptom ነው ወይስ doctorሩን emergency ማናገር አለብኝ?*

#### Sahara
- **Latency**: 4.09s | **Ref Words**: 41 | **Errors**: 8 (S: 5, D: 3, I: 0)
- **WER**: **19.5%** | **Word Accuracy**: **80.5%** | **CER**: 16.1%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom      ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a    long   time   ሲሆን   አንቤሮ         ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   ---     ---         tedrimestm   ነው   ወይስ   doctor     emergency   ---    ማና    
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            ✓    ✓    ✓          ✓     ✓    ✓      ✓      SUB   SUB          ✓      ✓       ✓          ✓    ✓        ✓    ✓      ✓        ✓      ✓       ✓    ✓    ✓        DEL     DEL         SUB          ✓    ✓     SUB        ✓           DEL    SUB   
```

#### Addis Ai
- **Latency**: 6.66s | **Ref Words**: 41 | **Errors**: 25 (S: 24, D: 1, I: 0)
- **WER**: **61.0%** | **Word Accuracy**: **39.0%** | **CER**: 74.1%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ   ላይ   standing   for   a     long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   ሎውር     ባክ     ፔን     እና   ፐልቪክ     ፕረሸር       በጣም   ይሰማኛል   ---          ስራ   ላይ   ስታንዲንግ     ፎር    ኤ     ሎንግ    ታይም    ሲሆን   አንበረቡ        ይሆናል   ፊትል     ሙቭመንት      ግን   አክቲቭ     ነው   ቤቢ     ኖርማል     ኪክ     እያደረገ   ነው   ይሄ   ኖርማል     ተርድ     ትራይምስተር     ስንተም      ነው   ወይስ   ዶክተሩን      ኢመርጀንሲ      ማናገር   አለብኝ  
EVAL: ✓    SUB     SUB    SUB    ✓    SUB      SUB        ✓     ✓       DEL          ✓    ✓    SUB        SUB   SUB   SUB    SUB    SUB   SUB          ✓      SUB     SUB        ✓    SUB      ✓    SUB    SUB      SUB    ✓       ✓    ✓    SUB      SUB     SUB         SUB       ✓    ✓     SUB        SUB         ✓      ✓     
```

#### Gemini
- **Latency**: 45.23s | **Ref Words**: 41 | **Errors**: 5 (S: 4, D: 0, I: 1)
- **WER**: **12.2%** | **Word Accuracy**: **87.8%** | **CER**: 4.7%

```text
REF : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ስራ    ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   normal   kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   ---      doctorሩን   emergency   ማናገር   አለብኝ  
HYP : ዛሬ   lower   back   pain   እና   pelvic   pressure   በጣም   ይሰማኛል   especially   ሥራ    ላይ   standing   for   a    long   time   ስሆን   unbearable   ይሆናል   fetal   movement   ግን   active   ነው   baby   በጥሩ      kick   እያደረገ   ነው   ይሄ   normal   third   trimester   symptom   ነው   ወይስ   doctor   ን          emergency   መናገር   አለብኝ  
EVAL: ✓    ✓       ✓      ✓      ✓    ✓        ✓          ✓     ✓       ✓            SUB   ✓    ✓          ✓     ✓    ✓      ✓      ✓     ✓            ✓      ✓       ✓          ✓    ✓        ✓    ✓      SUB      ✓      ✓       ✓    ✓    ✓        ✓       ✓           ✓         ✓    ✓     INS      SUB        ✓           SUB    ✓     
```

---

### Voice: `v24.wav`
> **Ground Truth Reference**:
> *ዛሬ taken አድርጌያለሁ፣ but yesterday ሙሉ ቀን ስራ ስለነበርኩ the calcium supplementቱን መውሰድ forget አድርጌ ነበር። ዛሬ double dose መውሰድ አለብኝ ወይስ just continue with one tablet? IFAውን ግን today as usual ጠዋት ወስጃለሁ፣ no complications።*

#### Sahara
- **Latency**: 4.4s | **Ref Words**: 36 | **Errors**: 7 (S: 5, D: 2, I: 0)
- **WER**: **19.4%** | **Word Accuracy**: **80.6%** | **CER**: 15.0%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
HYP : ዛሬ   take    አድርጌያለሁ   ---   ---         ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplement     መውሰድ   ፈጌት      አድርጌ   ነበር   ዛሬ   dauble   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   አይፈውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
EVAL: ✓    SUB     ✓         DEL   DEL         ✓    ✓    ✓    ✓        ✓     ✓         SUB            ✓      SUB      ✓      ✓     ✓    SUB      ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        SUB     ✓    ✓       ✓    ✓       ✓     ✓       ✓    ✓              
```

#### Addis Ai
- **Latency**: 5.79s | **Ref Words**: 36 | **Errors**: 20 (S: 19, D: 1, I: 0)
- **WER**: **55.6%** | **Word Accuracy**: **44.4%** | **CER**: 65.3%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose    መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ifaውን   ግን   today   as    usual   ጠዋት   ወስጃለሁ   no    complications  
HYP : ዛሬ   ቴክን     አድርጌያለሁ   በት    የስተዴይ       ሙሉ   ቀን   ስራ   ስለነበርኩ   ደ     ካልሲየም     ሳፕልማንቱን        መውሰድ   ፈጌት      አድርጌ   ነበር   ዛሬ   ---      ዳቦልዶስ   መውሰድ   አለብኝ   ወይስ   ጀስት    ኮንቲኒው      ዊዝ     ዋን    ታብሌት     አይሆን    ግን   ትዴይ     አዝ    ዩዝዋል    ጠዋት   ወስጃለሁ   ኖ     ኮምፕሊኬሽንስ       
EVAL: ✓    SUB     ✓         SUB   SUB         ✓    ✓    ✓    ✓        SUB   SUB       SUB            ✓      SUB      ✓      ✓     ✓    DEL      SUB     ✓      ✓      ✓     SUB    SUB        SUB    SUB   SUB      SUB     ✓    SUB     SUB   SUB     ✓     ✓       SUB   SUB            
```

#### Gemini
- **Latency**: 35.65s | **Ref Words**: 36 | **Errors**: 9 (S: 6, D: 2, I: 1)
- **WER**: **25.0%** | **Word Accuracy**: **75.0%** | **CER**: 12.0%

```text
REF : ዛሬ   taken   አድርጌያለሁ   but          yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   the   calcium   supplementቱን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   ---   ifaውን   ግን   today   as   usual   ጠዋት   ወስጃለሁ   no   complications  
HYP : ዛሬ   ---     take      አድርጌያለሁbut   yesterday   ሙሉ   ቀን   ስራ   ስለነበርኩ   ---   የካልሲየም    supplementኡን   መውሰድ   forget   አድርጌ   ነበር   ዛሬ   double   dose   መውሰድ   አለብኝ   ወይስ   just   continue   with   one   tablet   አይ    iron    ግን   today   as   usual   ጧት    ወስጃለሁ   no   complications  
EVAL: ✓    DEL     SUB       SUB          ✓           ✓    ✓    ✓    ✓        DEL   SUB       SUB            ✓      ✓        ✓      ✓     ✓    ✓        ✓      ✓      ✓      ✓     ✓      ✓          ✓      ✓     ✓        INS   SUB     ✓    ✓       ✓    ✓       SUB   ✓       ✓    ✓              
```

---

### Voice: `v25.wav`
> **Ground Truth Reference**:
> *ዛሬማ ገና አልወሰድኩም እኮ። ጠዋት morning sicknessሱ በጣም አስቸግሮኝ vomit ሳደርግ ነው የረፈደው፤ empty stomach መውሰድ አልቻልኩም። አሁን after lunch ትንሽ ሻል ሲለኝ the daily IFA supplementቱን ከብዙ water ጋር እወስደዋለሁ። calcium ደሞ አብሬ ልውሰደው ወይስ gap ልስጠው?*

#### Sahara
- **Latency**: 6.19s | **Ref Words**: 38 | **Errors**: 19 (S: 14, D: 5, I: 0)
- **WER**: **50.0%** | **Word Accuracy**: **50.0%** | **CER**: 34.5%

```text
REF : ዛሬማ   ገና    አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ     ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል    ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬ    ማገና   አልወሰድኩም   እኮ   ጠዋት   morning   ሲቅነሱ        በጣም   ---      አስቸግሩ   ይቦሳደርግ   ነው   የረፈደው   emty    stamk     መውሰድ   አልቻልኩም   አሁን   ---     አፍላንች   ትንሽ   ---   አልኝ   the   daily   አይፍ   supplement     ከብዙ   ቦታ      ጋር   እወስደዋለሁ   ካልሲየም     ደግሞ   አብሬ   ልውሰደው   ወይስ   ---   ---   
EVAL: SUB   SUB   ✓         ✓    ✓     ✓         SUB         ✓     DEL      SUB     SUB      ✓    ✓       SUB     SUB       ✓      ✓        ✓     DEL     SUB     ✓     DEL   SUB   ✓     ✓       SUB   SUB            ✓     SUB     ✓    ✓         SUB       SUB   ✓     ✓       ✓     DEL   DEL   
```

#### Addis Ai
- **Latency**: 5.68s | **Ref Words**: 38 | **Errors**: 17 (S: 15, D: 2, I: 0)
- **WER**: **44.7%** | **Word Accuracy**: **55.3%** | **CER**: 47.6%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ      ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch    ትንሽ   ሻል   ሲለኝ   the   daily   ifa   supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   ሞርኒንግ     ሲነሱ         በጣም   ---      አስቸግሮ   የሚያሳደርግ   ነው   የረፈደው   ኤምቲ     ስታማክ      መውሰድ   አልቻልኩም   አሁን   ---     አፍትላንች   ትንሽ   ሻል   ሲለኝ   ዘ     ዴሊ      አይፍ   ሳፕሊመንቱን        ከብዙ   ቦታ      ጋር   እወስደዋለሁ   ካልሲየም     ደግሞ   አብሬ   ልውሰደው   ወይስ   ጋፕ    ልስጠው  
EVAL: ✓     ✓    ✓         ✓    ✓     SUB       SUB         ✓     DEL      SUB     SUB       ✓    ✓       SUB     SUB       ✓      ✓        ✓     DEL     SUB      ✓     ✓    ✓     SUB   SUB     SUB   SUB            ✓     SUB     ✓    ✓         SUB       SUB   ✓     ✓       ✓     SUB   ✓     
```

#### Gemini
- **Latency**: 46.93s | **Ref Words**: 38 | **Errors**: 10 (S: 9, D: 1, I: 0)
- **WER**: **26.3%** | **Word Accuracy**: **73.7%** | **CER**: 12.5%

```text
REF : ዛሬማ   ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessሱ   በጣም   አስቸግሮኝ   vomit   ሳደርግ     ነው   የረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   ifa    supplementቱን   ከብዙ   water   ጋር   እወስደዋለሁ   calcium   ደሞ    አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
HYP : ዛሬ    ገና   አልወሰድኩም   እኮ   ጠዋት   morning   sicknessኡ   በጣም   ---      አስቸጋሪ   በሚያደርግ   ነው   ያረፈደው   empty   stomach   መውሰድ   አልቻልኩም   አሁን   after   lunch   ትንሽ   ሻል   ሲለኝ   the   daily   life   supplementኡን   ከብዙ   ውሃ      ጋር   እወስደዋለሁ   calcium   ደግሞ   አብሬ   ልውሰደው   ወይስ   gap   ልስጠው  
EVAL: SUB   ✓    ✓         ✓    ✓     ✓         SUB         ✓     DEL      SUB     SUB      ✓    SUB     ✓       ✓         ✓      ✓        ✓     ✓       ✓       ✓     ✓    ✓     ✓     ✓       SUB    SUB            ✓     SUB     ✓    ✓         ✓         SUB   ✓     ✓       ✓     ✓     ✓     
```

---
