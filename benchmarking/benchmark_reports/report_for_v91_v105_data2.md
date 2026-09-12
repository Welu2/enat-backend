# STT Benchmark Evaluation Report

- **Benchmark Results**: `bench_eng_part1.json`
- **Ground Truth**: `ground_truth.json`
- **Language**: EN
- **Total Audio Files Evaluated**: 15
- **Evaluation Date**: 2026-09-09 19:22:37 UTC

---

## 1. Overall Model Comparison

| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sahara** | 696 | 13 | 9 | 4 | 0 | **1.9%** | **98.1%** | 1.1% | 6.72s |
| **Deepgram** | 696 | 12 | 7 | 1 | 4 | **1.7%** | **98.3%** | 0.6% | 4.14s |
| **Gemini** | 696 | 6 | 4 | 2 | 0 | **0.9%** | **99.1%** | 0.1% | 5.86s |

---

## 2. Detailed File-by-File Evaluation

### Voice: `v91.wav`
> **Ground Truth Reference**:
> *Yes, I took my iron and folic acid supplement this morning right after breakfast with a full glass of water. I usually take the calcium tablet separately at night because taking them together causes severe nausea and stomach upset. My doctor advised me to keep them hours apart, and I am following the routine.*

#### Sahara
- **Latency**: 12.37s | **Ref Words**: 54 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **3.7%** | **Word Accuracy**: **96.3%** | **CER**: 2.0%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet    separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablets   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   dr       advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         SUB       ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    SUB      ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Deepgram
- **Latency**: 3.92s | **Ref Words**: 54 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **3.7%** | **Word Accuracy**: **96.3%** | **CER**: 2.8%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet    separately   at   night   because   taking   them   together   causes   severe   ---      nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablets   separately   at   night   because   taking   them   together   causes   severe   nausea   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         SUB       ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        INS      ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Gemini
- **Latency**: 4.54s | **Ref Words**: 54 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         ✓        ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

---

### Voice: `v92.wav`
> **Ground Truth Reference**:
> *I have not taken my IFA tablet yet today because severe morning sickness made it hard to keep anything down. Now that I have had lunch and feel better, I will take the daily iron dose. Should I take the calcium supplement alongside it or wait until dinner time?*

#### Sahara
- **Latency**: 4.81s | **Ref Words**: 49 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **4.1%** | **Word Accuracy**: **95.9%** | **CER**: 2.4%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   ife   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   ---   
EVAL: ✓    ✓      ✓     ✓       ✓    SUB   ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       ✓        DEL   
```

#### Deepgram
- **Latency**: 2.97s | **Ref Words**: 49 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **4.1%** | **Word Accuracy**: **95.9%** | **CER**: 2.4%

```text
REF : i    have   not   taken   my   ---   ifa    tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   eye   fade   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
EVAL: ✓    ✓      ✓     ✓       ✓    INS   SUB    ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       ✓        ✓     
```

#### Gemini
- **Latency**: 3.86s | **Ref Words**: 49 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **4.1%** | **Word Accuracy**: **95.9%** | **CER**: 0.0%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time        
HYP : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   ---      dinnertime  
EVAL: ✓    ✓      ✓     ✓       ✓    ✓     ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       DEL      SUB         
```

---

### Voice: `v93.wav`
> **Ground Truth Reference**:
> *I have been having persistent throbbing headaches since morning accompanied by slight blurry vision. Both my feet and ankles are noticeably swollen today, and my shoes no longer fit. Could this indicate high blood pressure, and should I report to emergency triage immediately?*

#### Sahara
- **Latency**: 7.46s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Deepgram
- **Latency**: 2.61s | **Ref Words**: 43 | **Errors**: 1 (S: 0, D: 0, I: 1)
- **WER**: **2.3%** | **Word Accuracy**: **97.7%** | **CER**: 1.8%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   ---    this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       INS    ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Gemini
- **Latency**: 3.38s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

---

### Voice: `v94.wav`
> **Ground Truth Reference**:
> *I am very worried because the baby's movements have decreased significantly since yesterday morning. Usually there is active kicking after meals, but today it is quiet even after drinking cold juice and resting. Should I report to the maternal health clinic right away?*

#### Sahara
- **Latency**: 6.85s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

#### Deepgram
- **Latency**: 7.72s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

#### Gemini
- **Latency**: 3.39s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

---

### Voice: `v95.wav`
> **Ground Truth Reference**:
> *I have frequent lower abdominal cramping that feels like severe menstrual pain, accompanied by strong lower back pressure. I am not sure whether these are normal Braxton Hicks contractions or early labor signs. Please advise me on what danger signs I need to monitor.*

#### Sahara
- **Latency**: 5.31s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

#### Deepgram
- **Latency**: 3.08s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

#### Gemini
- **Latency**: 3.69s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

---

### Voice: `v96.wav`
> **Ground Truth Reference**:
> *I have severe acid reflux and heartburn that prevents me from sleeping comfortably at night, even when propped up with pillows. The burning sensation is quite painful. Are there safe over-the-counter antacids I can take during this stage of pregnancy?*

#### Sahara
- **Latency**: 6.99s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Deepgram
- **Latency**: 2.87s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Gemini
- **Latency**: 3.29s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

---

### Voice: `v97.wav`
> **Ground Truth Reference**:
> *Yes, I took my iron and folic acid supplement this morning right after breakfast with a full glass of water. I usually take the calcium tablet separately at night because taking them together causes severe nausea and stomach upset. My doctor advised me to keep them hours apart, and I am following the routine.*

#### Sahara
- **Latency**: 4.66s | **Ref Words**: 54 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **3.7%** | **Word Accuracy**: **96.3%** | **CER**: 2.0%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet    separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablets   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   dr       advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         SUB       ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    SUB      ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Deepgram
- **Latency**: 7.15s | **Ref Words**: 54 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **1.8%** | **Word Accuracy**: **98.2%** | **CER**: 0.4%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet    separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablets   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         SUB       ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Gemini
- **Latency**: 8.32s | **Ref Words**: 54 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         ✓        ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

---

### Voice: `v98.wav`
> **Ground Truth Reference**:
> *I have not taken my IFA tablet yet today because severe morning sickness made it hard to keep anything down. Now that I have had lunch and feel better, I will take the daily iron dose. Should I take the calcium supplement alongside it or wait until dinner time?*

#### Sahara
- **Latency**: 6.27s | **Ref Words**: 49 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **4.1%** | **Word Accuracy**: **95.9%** | **CER**: 2.4%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   ife   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   ---   
EVAL: ✓    ✓      ✓     ✓       ✓    SUB   ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       ✓        DEL   
```

#### Deepgram
- **Latency**: 3.01s | **Ref Words**: 49 | **Errors**: 2 (S: 1, D: 1, I: 0)
- **WER**: **4.1%** | **Word Accuracy**: **95.9%** | **CER**: 0.0%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time        
HYP : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   ---      dinnertime  
EVAL: ✓    ✓      ✓     ✓       ✓    ✓     ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       DEL      SUB         
```

#### Gemini
- **Latency**: 3.88s | **Ref Words**: 49 | **Errors**: 3 (S: 2, D: 1, I: 0)
- **WER**: **6.1%** | **Word Accuracy**: **93.9%** | **CER**: 1.0%

```text
REF : i    have   not   taken   my   ifa    tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time        
HYP : i    have   not   taken   my   ifet   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   ---      dinnertime  
EVAL: ✓    ✓      ✓     ✓       ✓    SUB    ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       DEL      SUB         
```

---

### Voice: `v99.wav`
> **Ground Truth Reference**:
> *I have been having persistent throbbing headaches since morning accompanied by slight blurry vision. Both my feet and ankles are noticeably swollen today, and my shoes no longer fit. Could this indicate high blood pressure, and should I report to emergency triage immediately?*

#### Sahara
- **Latency**: 5.02s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Deepgram
- **Latency**: 2.79s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Gemini
- **Latency**: 13.52s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

---

### Voice: `v100.wav`
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
- **Latency**: 3.67s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

#### Gemini
- **Latency**: 8.24s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
HYP : i    am   very   worried   because   the   babys   movements   have   decreased   significantly   since   yesterday   morning   usually   there   is   active   kicking   after   meals   but   today   it   is   quiet   even   after   drinking   cold   juice   and   resting   should   i    report   to   the   maternal   health   clinic   right   away  
EVAL: ✓    ✓    ✓      ✓         ✓         ✓     ✓       ✓           ✓      ✓           ✓               ✓       ✓           ✓         ✓         ✓       ✓    ✓        ✓         ✓       ✓       ✓     ✓       ✓    ✓    ✓       ✓      ✓       ✓          ✓      ✓       ✓     ✓         ✓        ✓    ✓        ✓    ✓     ✓          ✓        ✓        ✓       ✓     
```

---

### Voice: `v101.wav`
> **Ground Truth Reference**:
> *I have frequent lower abdominal cramping that feels like severe menstrual pain, accompanied by strong lower back pressure. I am not sure whether these are normal Braxton Hicks contractions or early labor signs. Please advise me on what danger signs I need to monitor.*

#### Sahara
- **Latency**: 7.07s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

#### Deepgram
- **Latency**: 3.9s | **Ref Words**: 44 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **2.3%** | **Word Accuracy**: **97.7%** | **CER**: 0.4%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor    signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labour   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       SUB      ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

#### Gemini
- **Latency**: 3.39s | **Ref Words**: 44 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
HYP : i    have   frequent   lower   abdominal   cramping   that   feels   like   severe   menstrual   pain   accompanied   by   strong   lower   back   pressure   i    am   not   sure   whether   these   are   normal   braxton   hicks   contractions   or   early   labor   signs   please   advise   me   on   what   danger   signs   i    need   to   monitor  
EVAL: ✓    ✓      ✓          ✓       ✓           ✓          ✓      ✓       ✓      ✓        ✓           ✓      ✓             ✓    ✓        ✓       ✓      ✓          ✓    ✓    ✓     ✓      ✓         ✓       ✓     ✓        ✓         ✓       ✓              ✓    ✓       ✓       ✓       ✓        ✓        ✓    ✓    ✓      ✓        ✓       ✓    ✓      ✓    ✓        
```

---

### Voice: `v102.wav`
> **Ground Truth Reference**:
> *I have severe acid reflux and heartburn that prevents me from sleeping comfortably at night, even when propped up with pillows. The burning sensation is quite painful. Are there safe over-the-counter antacids I can take during this stage of pregnancy?*

#### Sahara
- **Latency**: 9.74s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Deepgram
- **Latency**: 2.66s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

#### Gemini
- **Latency**: 4.26s | **Ref Words**: 42 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
HYP : i    have   severe   acid   reflux   and   heartburn   that   prevents   me   from   sleeping   comfortably   at   night   even   when   propped   up   with   pillows   the   burning   sensation   is   quite   painful   are   there   safe   over   the   counter   antacids   i    can   take   during   this   stage   of   pregnancy  
EVAL: ✓    ✓      ✓        ✓      ✓        ✓     ✓           ✓      ✓          ✓    ✓      ✓          ✓             ✓    ✓       ✓      ✓      ✓         ✓    ✓      ✓         ✓     ✓         ✓           ✓    ✓       ✓         ✓     ✓       ✓      ✓      ✓     ✓         ✓          ✓    ✓     ✓      ✓        ✓      ✓       ✓    ✓          
```

---

### Voice: `v103.wav`
> **Ground Truth Reference**:
> *Yes, I took my iron and folic acid supplement this morning right after breakfast with a full glass of water. I usually take the calcium tablet separately at night because taking them together causes severe nausea and stomach upset. My doctor advised me to keep them hours apart, and I am following the routine.*

#### Sahara
- **Latency**: 5.29s | **Ref Words**: 54 | **Errors**: 2 (S: 2, D: 0, I: 0)
- **WER**: **3.7%** | **Word Accuracy**: **96.3%** | **CER**: 2.0%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet    separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablets   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   dr       advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         SUB       ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    SUB      ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Deepgram
- **Latency**: 6.49s | **Ref Words**: 54 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **1.8%** | **Word Accuracy**: **98.2%** | **CER**: 0.4%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet    separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablets   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         SUB       ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

#### Gemini
- **Latency**: 3.54s | **Ref Words**: 54 | **Errors**: 1 (S: 1, D: 0, I: 0)
- **WER**: **1.8%** | **Word Accuracy**: **98.2%** | **CER**: 0.4%

```text
REF : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablet    separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
HYP : yes   i    took   my   iron   and   folic   acid   supplement   this   morning   right   after   breakfast   with   a    full   glass   of   water   i    usually   take   the   calcium   tablets   separately   at   night   because   taking   them   together   causes   severe   nausea   and   stomach   upset   my   doctor   advised   me   to   keep   them   hours   apart   and   i    am   following   the   routine  
EVAL: ✓     ✓    ✓      ✓    ✓      ✓     ✓       ✓      ✓            ✓      ✓         ✓       ✓       ✓           ✓      ✓    ✓      ✓       ✓    ✓       ✓    ✓         ✓      ✓     ✓         SUB       ✓            ✓    ✓       ✓         ✓        ✓      ✓          ✓        ✓        ✓        ✓     ✓         ✓       ✓    ✓        ✓         ✓    ✓    ✓      ✓      ✓       ✓       ✓     ✓    ✓    ✓           ✓     ✓        
```

---

### Voice: `v104.wav`
> **Ground Truth Reference**:
> *I have not taken my IFA tablet yet today because severe morning sickness made it hard to keep anything down. Now that I have had lunch and feel better, I will take the daily iron dose. Should I take the calcium supplement alongside it or wait until dinner time?*

#### Sahara
- **Latency**: 7.21s | **Ref Words**: 49 | **Errors**: 3 (S: 1, D: 2, I: 0)
- **WER**: **6.1%** | **Word Accuracy**: **93.9%** | **CER**: 5.3%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   ife   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   ---      ---   
EVAL: ✓    ✓      ✓     ✓       ✓    SUB   ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       DEL      DEL   
```

#### Deepgram
- **Latency**: 4.49s | **Ref Words**: 49 | **Errors**: 2 (S: 1, D: 0, I: 1)
- **WER**: **4.1%** | **Word Accuracy**: **95.9%** | **CER**: 1.0%

```text
REF : i    have   not   taken   my   ---   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   i     fey   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
EVAL: ✓    ✓      ✓     ✓       ✓    INS   SUB   ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       ✓        ✓     
```

#### Gemini
- **Latency**: 9.67s | **Ref Words**: 49 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
HYP : i    have   not   taken   my   ifa   tablet   yet   today   because   severe   morning   sickness   made   it   hard   to   keep   anything   down   now   that   i    have   had   lunch   and   feel   better   i    will   take   the   daily   iron   dose   should   i    take   the   calcium   supplement   alongside   it   or   wait   until   dinner   time  
EVAL: ✓    ✓      ✓     ✓       ✓    ✓     ✓        ✓     ✓       ✓         ✓        ✓         ✓          ✓      ✓    ✓      ✓    ✓      ✓          ✓      ✓     ✓      ✓    ✓      ✓     ✓       ✓     ✓      ✓        ✓    ✓      ✓      ✓     ✓       ✓      ✓      ✓        ✓    ✓      ✓     ✓         ✓            ✓           ✓    ✓    ✓      ✓       ✓        ✓     
```

---

### Voice: `v105.wav`
> **Ground Truth Reference**:
> *I have been having persistent throbbing headaches since morning accompanied by slight blurry vision. Both my feet and ankles are noticeably swollen today, and my shoes no longer fit. Could this indicate high blood pressure, and should I report to emergency triage immediately?*

#### Sahara
- **Latency**: 6.82s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Deepgram
- **Latency**: 4.84s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

#### Gemini
- **Latency**: 10.94s | **Ref Words**: 43 | **Errors**: 0 (S: 0, D: 0, I: 0)
- **WER**: **0.0%** | **Word Accuracy**: **100.0%** | **CER**: 0.0%

```text
REF : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
HYP : i    have   been   having   persistent   throbbing   headaches   since   morning   accompanied   by   slight   blurry   vision   both   my   feet   and   ankles   are   noticeably   swollen   today   and   my   shoes   no   longer   fit   could   this   indicate   high   blood   pressure   and   should   i    report   to   emergency   triage   immediately  
EVAL: ✓    ✓      ✓      ✓        ✓            ✓           ✓           ✓       ✓         ✓             ✓    ✓        ✓        ✓        ✓      ✓    ✓      ✓     ✓        ✓     ✓            ✓         ✓       ✓     ✓    ✓       ✓    ✓        ✓     ✓       ✓      ✓          ✓      ✓       ✓          ✓     ✓        ✓    ✓        ✓    ✓           ✓        ✓            
```

---
