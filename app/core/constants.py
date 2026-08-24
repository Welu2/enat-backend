DANGER_SIGN_CATEGORIES: frozenset[str] = frozenset(
    [
        "vaginal_bleeding",
        "swelling_hands_face",
        "blurred_vision",
        "severe_abdominal_pain",
        "fluid_leakage",
        "severe_headache",
        "persistent_nausea_vomiting",
        "high_fever",
        "convulsions_loss_of_consciousness",
        "difficulty_breathing",
        "severe_weakness_or_backache",
        "abnormal_fetal_movement",
    ]
)

# All valid topics for closing_mentions.
# supplement_taken is included because a woman may volunteer supplement info
# in the open-ended closing question even when the dedicated supplement stage
# was skipped (no active supplement on record).
NUTRITION_TOPICS = [
    "dietary_intake",
    "supplement_taken",
    "therapeutic_food",
    "breastfeeding_intent",
    "other",
]

CHECKIN_STAGES = ["symptoms", "food", "supplement", "closing"]

CHECKIN_STAGE_METADATA = {
    "symptoms": {
        "category_am": "የአደጋ ምልክቶች እና ህመም",
        "category_en": "DANGER SIGNS & SYMPTOMS",
        "prompt_am": "ዛሬ ጽኑ ራስ ምታት፣ የዓይን ብዥታ፣ ደም መፍሰስ፣ ፈሳሽ መፍሰስ ወይም ከፍተኛ የሆድ ህመም ተሰምቶዎታል?",
        "prompt_en": "Did you experience any severe headache, blurred vision, vaginal bleeding, fluid leakage, or abdominal pain today?",
    },
    "food": {
        "category_am": "የተመጣጠነ ምግብ እና አመጋገብ",
        "category_en": "NUTRITION & DIET",
        "prompt_am": "ዛሬ ምን ምን አይነት ምግቦችን ተመገቡ? ቢያንስ አንድ ተጨማሪ የተመጣጠነ ምግብ ወስደዋል?",
        "prompt_en": "What foods did you eat today? Did you have an additional nutrient-dense meal?",
    },
    "supplement": {
        "category_am": "የቅድመ ወሊድ እንክብሎች",
        "category_en": "PRENATAL SUPPLEMENTS",
        "prompt_am": "የዛሬውን የብረት እና ፎሊክ አሲድ (IFA) ወይም የካልሲየም እንክብል ወስደዋል?",
        "prompt_en": "Did you take your prescribed daily Iron-Folic Acid (IFA) or Calcium supplement today?",
    },
    "closing": {
        "category_am": "አጠቃላይ ስሜት እና ጥያቄዎች",
        "category_en": "CLOSING & QUESTIONS",
        "prompt_am": "ሌላ የሚያስጨንቅዎት ማንኛውም የጤና ለውጥ፣ ህመም ወይም ጥያቄ አለዎት?",
        "prompt_en": "Do you have any other questions, concerns, or symptoms you would like to report?",
    },
}

STAGE_PROMPTS = {
    "symptoms": CHECKIN_STAGE_METADATA["symptoms"]["prompt_am"],
    "food": CHECKIN_STAGE_METADATA["food"]["prompt_am"],
    "supplement": CHECKIN_STAGE_METADATA["supplement"]["prompt_am"],
    "closing": CHECKIN_STAGE_METADATA["closing"]["prompt_am"],
}
