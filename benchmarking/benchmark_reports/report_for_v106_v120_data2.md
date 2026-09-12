# STT Benchmark Evaluation Report

- **Benchmark Results**: `bench_eng_part2.json`
- **Ground Truth**: `ground_truth.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 15
- **Evaluation Date**: 2026-09-09 19:24:35 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 679 | 3 | 3 | 0 | 0 | **0.4%** | **99.6%** | 0.3% | 7.90s |
| **Deepgram** | 679 | 8 | 3 | 3 | 2 | **1.2%** | **98.8%** | 0.6% | 4.22s |
| **Gemini** | 679 | 3 | 2 | 1 | 0 | **0.4%** | **99.6%** | 0.1% | 6.81s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v106.wav`
> **Ground Truth Reference**:
> *I am very worried because the baby's movements have decreased significantly since yesterday morning. Usually there is active kicking after meals, but today it is quiet even after drinking cold juice and resting. Should I report to the maternal health clinic right away?*

#### Sahara
- **Latency**: 6.8s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

#### Deepgram
- **Latency**: 2.8s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

#### Gemini
- **Latency**: 9.33s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

---

### Voice: `v107.wav`
> **Ground Truth Reference**:
> *I have frequent lower abdominal cramping that feels like severe menstrual pain, accompanied by strong lower back pressure. I am not sure whether these are normal Braxton Hicks contractions or early labor signs. Please advise me on what danger signs I need to monitor.*

#### Sahara
- **Latency**: 8.67s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

#### Deepgram
- **Latency**: 6.22s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

#### Gemini
- **Latency**: 4.39s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

---

### Voice: `v108.wav`
> **Ground Truth Reference**:
> *I have severe acid reflux and heartburn that prevents me from sleeping comfortably at night, even when propped up with pillows. The burning sensation is quite painful. Are there safe over-the-counter antacids I can take during this stage of pregnancy?*

#### Sahara
- **Latency**: 11.37s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Deepgram
- **Latency**: 2.22s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Gemini
- **Latency**: 7.1s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

---

### Voice: `v109.wav`
> **Ground Truth Reference**:
> *Yes, I took my iron and folic acid supplement this morning right after breakfast with a full glass of water. I usually take the calcium tablet separately at night because taking them together causes severe nausea and stomach upset. My doctor advised me to keep them hours apart, and I am following the routine.*

#### Sahara
- **Latency**: 7.97s | **Ref Words**: 54 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **1.8%** | **Word Accuracy**: **98.2%** | **CER**: 1.6%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   dr       advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         ✓        ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    SUB      ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Deepgram
- **Latency**: 5.01s | **Ref Words**: 54 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         ✓        ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Gemini
- **Latency**: 4.59s | **Ref Words**: 54 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         ✓        ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

---

### Voice: `v110.wav`
> **Ground Truth Reference**:
> *I have not taken my IFA tablet yet today because severe morning sickness made it hard to keep anything down. Now that I have had lunch and feel better, I will take the daily iron dose. Should I take the calcium supplement alongside it or wait until dinner time?*

#### Sahara
- **Latency**: 4.9s | **Ref Words**: 49 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
EVAL: ✓    ✓      ✓     ✓       ✓    ✓     ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       ✓        ✓     
```

#### Deepgram
- **Latency**: 3.05s | **Ref Words**: 49 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
EVAL: ✓    ✓      ✓     ✓       ✓    ✓     ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       ✓        ✓     
```

#### Gemini
- **Latency**: 4.52s | **Ref Words**: 49 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
EVAL: ✓    ✓      ✓     ✓       ✓    ✓     ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       ✓        ✓     
```

---

### Voice: `v111.wav`
> **Ground Truth Reference**:
> *I have been having persistent throbbing headaches since morning accompanied by slight blurry vision. Both my feet and ankles are noticeably swollen today, and my shoes no longer fit. Could this indicate high blood pressure, and should I report to emergency triage immediately?*

#### Sahara
- **Latency**: 8.72s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Deepgram
- **Latency**: 3.82s | **Ref Words**: 43 | **Errors**: 1 (S: 0, D: 0, I: 1)
- **WER**: **2.3%** | **Word Accuracy**: **97.7%** | **CER**: 0.9%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   ---   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no    no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       INS   ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Gemini
- **Latency**: 10.5s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

---

### Voice: `v112.wav`
> **Ground Truth Reference**:
> *I am very worried because the baby's movements have decreased significantly since yesterday morning. Usually there is active kicking after meals, but today it is quiet even after drinking cold juice and resting. Should I report to the maternal health clinic right away?*

#### Sahara
- **Latency**: 5.34s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

#### Deepgram
- **Latency**: 4.24s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

#### Gemini
- **Latency**: 3.9s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

---

### Voice: `v113.wav`
> **Ground Truth Reference**:
> *I have frequent lower abdominal cramping that feels like severe menstrual pain, accompanied by strong lower back pressure. I am not sure whether these are normal Braxton Hicks contractions or early labor signs. Please advise me on what danger signs I need to monitor.*

#### Sahara
- **Latency**: 12.78s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

#### Deepgram
- **Latency**: 9.63s | **Ref Words**: 44 | **Errors**: 2 (S: 0, D: 2, I: 0)
- **WER**: **4.5%** | **Word Accuracy**: **95.5%** | **CER**: 5.5%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   ---       ---     contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        DEL       DEL     ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

#### Gemini
- **Latency**: 11.53s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

---

### Voice: `v114.wav`
> **Ground Truth Reference**:
> *I have severe acid reflux and heartburn that prevents me from sleeping comfortably at night, even when propped up with pillows. The burning sensation is quite painful. Are there safe over-the-counter antacids I can take during this stage of pregnancy?*

#### Sahara
- **Latency**: 9.37s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Deepgram
- **Latency**: 4.14s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Gemini
- **Latency**: 4.08s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

---

### Voice: `v115.wav`
> **Ground Truth Reference**:
> *Yes, I took my iron and folic acid supplement this morning right after breakfast with a full glass of water. I usually take the calcium tablet separately at night because taking them together causes severe nausea and stomach upset. My doctor advised me to keep them hours apart, and I am following the routine.*

#### Sahara
- **Latency**: 10.36s | **Ref Words**: 54 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **1.8%** | **Word Accuracy**: **98.2%** | **CER**: 1.6%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   dr       advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         ✓        ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    SUB      ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Deepgram
- **Latency**: 5.7s | **Ref Words**: 54 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **1.8%** | **Word Accuracy**: **98.2%** | **CER**: 0.4%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet    separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablets   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         SUB       ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Gemini
- **Latency**: 10.78s | **Ref Words**: 54 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         ✓        ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

---

### Voice: `v116.wav`
> **Ground Truth Reference**:
> *I have not taken my IFA tablet yet today because severe morning sickness made it hard to keep anything down. Now that I have had lunch and feel better, I will take the daily iron dose. Should I take the calcium supplement alongside it or wait until dinner time?*

#### Sahara
- **Latency**: 6.4s | **Ref Words**: 49 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **2.0%** | **Word Accuracy**: **98.0%** | **CER**: 0.5%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   ife   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
EVAL: ✓    ✓      ✓     ✓       ✓    SUB   ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       ✓        ✓     
```

#### Deepgram
- **Latency**: 2.38s | **Ref Words**: 49 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **6.1%** | **Word Accuracy**: **93.9%** | **CER**: 0.5%

```text
REF : i    have   not   taken   my   ifa    tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time        
HYP : i    have   not   taken   my   ifay   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   ---      dinnertime  
EVAL: ✓    ✓      ✓     ✓       ✓    SUB    ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       DEL      SUB         
```

#### Gemini
- **Latency**: 4.21s | **Ref Words**: 49 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **6.1%** | **Word Accuracy**: **93.9%** | **CER**: 1.0%

```text
REF : i    have   not   taken   my   ifa     tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time        
HYP : i    have   not   taken   my   iface   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   ---      dinnertime  
EVAL: ✓    ✓      ✓     ✓       ✓    SUB     ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       DEL      SUB         
```

---

### Voice: `v117.wav`
> **Ground Truth Reference**:
> *I have been having persistent throbbing headaches since morning accompanied by slight blurry vision. Both my feet and ankles are noticeably swollen today, and my shoes no longer fit. Could this indicate high blood pressure, and should I report to emergency triage immediately?*

#### Sahara
- **Latency**: 5.48s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Deepgram
- **Latency**: 2.32s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Gemini
- **Latency**: 7.23s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

---

### Voice: `v118.wav`
> **Ground Truth Reference**:
> *I am very worried because the baby's movements have decreased significantly since yesterday morning. Usually there is active kicking after meals, but today it is quiet even after drinking cold juice and resting. Should I report to the maternal health clinic right away?*

#### Sahara
- **Latency**: 4.99s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

#### Deepgram
- **Latency**: 3.16s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

#### Gemini
- **Latency**: 8.83s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

---

### Voice: `v119.wav`
> **Ground Truth Reference**:
> *I have frequent lower abdominal cramping that feels like severe menstrual pain, accompanied by strong lower back pressure. I am not sure whether these are normal Braxton Hicks contractions or early labor signs. Please advise me on what danger signs I need to monitor.*

#### Sahara
- **Latency**: 5.65s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

#### Deepgram
- **Latency**: 3.37s | **Ref Words**: 44 | **Errors**: 1 (S: 0, D: 0, I: 1)
- **WER**: **2.3%** | **Word Accuracy**: **97.7%** | **CER**: 2.3%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor   ---    
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor   enter  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓         INS    
```

#### Gemini
- **Latency**: 6.31s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

---

### Voice: `v120.wav`
> **Ground Truth Reference**:
> *I have severe acid reflux and heartburn that prevents me from sleeping comfortably at night, even when propped up with pillows. The burning sensation is quite painful. Are there safe over-the-counter antacids I can take during this stage of pregnancy?*

#### Sahara
- **Latency**: 9.65s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Deepgram
- **Latency**: 5.18s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Gemini
- **Latency**: 4.86s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

---
