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

STAGE_PROMPTS = {
    "symptoms": "እባክዎን ዛሬ ያላችሁትን ምልክቶች ይነግሩኝ።",
    "food": "ዛሬ ምን ምግብ በሉ?",
    "supplement": "የሚወስዱትን ተጨማሪ ምግብ ዛሬ ወስደዋል?",
    "closing": "ለመጨረስ ሌላ ነገር ማካፈል ይፈልጋሉ?",
}
