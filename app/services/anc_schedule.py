from datetime import date, timedelta
from typing import Any

from app.services.extraction import _category_display

WHO_ANC_CONTACTS: list[dict[str, Any]] = [
    {
        "contact_number": 1,
        "trimester": "first_trimester",
        "trimester_en": "First Trimester",
        "trimester_am": "1ኛ ትሪሚስተር",
        "gestational_weeks": 12,
        "gestational_label_en": "Up to 12 weeks",
        "gestational_label_am": "እስከ 12 ሳምንት",
        "schedule_next_weeks": 8,  # Next at 20 weeks (12 + 8)
        "title_en": "1st ANC Contact (Up to 12 Weeks)",
        "title_am": "1ኛ የቅድመ ወሊድ ክትትል (እስከ 12 ሳምንት)",
    },
    {
        "contact_number": 2,
        "trimester": "second_trimester",
        "trimester_en": "Second Trimester",
        "trimester_am": "2ኛ ትሪሚስተር",
        "gestational_weeks": 20,
        "gestational_label_en": "20 weeks",
        "gestational_label_am": "20 ሳምንት",
        "schedule_next_weeks": 6,  # Next at 26 weeks (20 + 6)
        "title_en": "2nd ANC Contact (20 Weeks)",
        "title_am": "2ኛ የቅድመ ወሊድ ክትትል (20 ሳምንት)",
    },
    {
        "contact_number": 3,
        "trimester": "second_trimester",
        "trimester_en": "Second Trimester",
        "trimester_am": "2ኛ ትሪሚስተር",
        "gestational_weeks": 26,
        "gestational_label_en": "26 weeks",
        "gestational_label_am": "26 ሳምንት",
        "schedule_next_weeks": 4,  # Next at 30 weeks (26 + 4)
        "title_en": "3rd ANC Contact (26 Weeks)",
        "title_am": "3ኛ የቅድመ ወሊድ ክትትል (26 ሳምንት)",
    },
    {
        "contact_number": 4,
        "trimester": "third_trimester",
        "trimester_en": "Third Trimester",
        "trimester_am": "3ኛ ትሪሚስተር",
        "gestational_weeks": 30,
        "gestational_label_en": "30 weeks",
        "gestational_label_am": "30 ሳምንት",
        "schedule_next_weeks": 4,  # Next at 34 weeks (30 + 4)
        "title_en": "4th ANC Contact (30 Weeks)",
        "title_am": "4ኛ የቅድመ ወሊድ ክትትል (30 ሳምንት)",
    },
    {
        "contact_number": 5,
        "trimester": "third_trimester",
        "trimester_en": "Third Trimester",
        "trimester_am": "3ኛ ትሪሚስተር",
        "gestational_weeks": 34,
        "gestational_label_en": "34 weeks",
        "gestational_label_am": "34 ሳምንት",
        "schedule_next_weeks": 2,  # Next at 36 weeks (34 + 2)
        "title_en": "5th ANC Contact (34 Weeks)",
        "title_am": "5ኛ የቅድመ ወሊድ ክትትል (34 ሳምንት)",
    },
    {
        "contact_number": 6,
        "trimester": "third_trimester",
        "trimester_en": "Third Trimester",
        "trimester_am": "3ኛ ትሪሚስተር",
        "gestational_weeks": 36,
        "gestational_label_en": "36 weeks",
        "gestational_label_am": "36 ሳምንት",
        "schedule_next_weeks": 2,  # Next at 38 weeks (36 + 2)
        "title_en": "6th ANC Contact (36 Weeks)",
        "title_am": "6ኛ የቅድመ ወሊድ ክትትል (36 ሳምንት)",
    },
    {
        "contact_number": 7,
        "trimester": "third_trimester",
        "trimester_en": "Third Trimester",
        "trimester_am": "3ኛ ትሪሚስተር",
        "gestational_weeks": 38,
        "gestational_label_en": "38 weeks",
        "gestational_label_am": "38 ሳምንት",
        "schedule_next_weeks": 2,  # Next at 40 weeks (38 + 2)
        "title_en": "7th ANC Contact (38 Weeks)",
        "title_am": "7ኛ የቅድመ ወሊድ ክትትል (38 ሳምንት)",
    },
    {
        "contact_number": 8,
        "trimester": "third_trimester",
        "trimester_en": "Third Trimester",
        "trimester_am": "3ኛ ትሪሚስተር",
        "gestational_weeks": 40,
        "gestational_label_en": "40 weeks (Delivery)",
        "gestational_label_am": "40 ሳምንት (የመውለጃ ጊዜ)",
        "schedule_next_weeks": None,
        "title_en": "8th ANC Contact (40 Weeks - Delivery)",
        "title_am": "8ኛ የቅድመ ወሊድ ክትትል (40 ሳምንት - የመውለጃ ጊዜ)",
    },
]

_CONTACT_BY_NUM: dict[int, dict[str, Any]] = {
    c["contact_number"]: c for c in WHO_ANC_CONTACTS
}


def calculate_all_anc_dates(effective_lnmp: date) -> list[dict[str, Any]]:
    """Generates the full 8-contact WHO ANC schedule with calculated target calendar dates."""
    schedule = []
    for c in WHO_ANC_CONTACTS:
        target_date = effective_lnmp + timedelta(weeks=c["gestational_weeks"])
        schedule.append({
            **c,
            "target_date": target_date.isoformat(),
        })
    return schedule


def get_next_anc_contact(effective_lnmp: date, as_of_date: date | None = None) -> dict[str, Any]:
    """Determines the next upcoming WHO ANC contact for a pregnant mother based on current gestational age."""
    today = as_of_date or date.today()
    current_days = max(0, (today - effective_lnmp).days)
    current_weeks = current_days // 7

    # Find the earliest contact whose target gestational age is in the future (or current target)
    for c in WHO_ANC_CONTACTS:
        if current_weeks <= c["gestational_weeks"]:
            target_date = effective_lnmp + timedelta(weeks=c["gestational_weeks"])
            return {
                **c,
                "target_date": target_date.isoformat(),
                "current_gestational_weeks": current_weeks,
            }

    # If past 40 weeks, default to contact 8
    last = WHO_ANC_CONTACTS[-1]
    return {
        **last,
        "target_date": (effective_lnmp + timedelta(weeks=40)).isoformat(),
        "current_gestational_weeks": current_weeks,
    }


def advance_to_next_anc_contact(
    current_contact_num: int,
    current_appointment_date: date | None,
    effective_lnmp: date | None = None,
) -> dict[str, Any] | None:
    """Calculates the subsequent ANC contact after a contact report is generated.
    
    If current is Contact 1 (12w), advances after 8 weeks to Contact 2 (20w).
    If current is Contact 2 (20w), advances after 6 weeks to Contact 3 (26w), etc.
    """
    if current_contact_num >= 8:
        return None

    next_num = current_contact_num + 1
    next_spec = _CONTACT_BY_NUM.get(next_num)
    if not next_spec:
        return None

    current_spec = _CONTACT_BY_NUM.get(current_contact_num, {})
    schedule_next_weeks = current_spec.get("schedule_next_weeks", 4)

    if current_appointment_date:
        next_date = current_appointment_date + timedelta(weeks=schedule_next_weeks)
    elif effective_lnmp:
        next_date = effective_lnmp + timedelta(weeks=next_spec["gestational_weeks"])
    else:
        next_date = date.today() + timedelta(weeks=schedule_next_weeks)

    return {
        **next_spec,
        "appointment_date": next_date.isoformat(),
        "previous_contact_number": current_contact_num,
    }


def generate_checkin_summary_text(symptoms: list[dict[str, Any]] | None) -> dict[str, str]:
    """Generates localized daily check-in summary statements in Amharic and English.
    
    Outcomes:
    1. Danger Sign(s) detected:
       - AM: '{x} የአደጋ ምልክት ተገኝቷል፣ በአስቸቋይ የህክምና እርዳታ ያግኙ'
       - EN: '{x} danger sign detected, seek medical help immediately.'
    2. Non-danger symptom(s) recorded:
       - AM: 'ምንም የአደጋ ምልክት አልተገኘም፣ ነገር ግን {x} ምልክት ተመዝግቧል'
       - EN: 'No danger signs detected, but {x} symptom(s) recorded.'
    3. No symptoms / clear:
       - AM: 'ምንም የአደጋ ምልክት አልተገኘም'
       - EN: 'No danger signs detected.'
    """
    if not symptoms:
        return {
            "summary_text_am": "ምንም የአደጋ ምልክት አልተገኘም",
            "summary_text_en": "No danger signs detected.",
            "danger_sign_triggered": False,
        }

    danger_labels_am: list[str] = []
    danger_labels_en: list[str] = []
    general_labels_am: list[str] = []
    general_labels_en: list[str] = []

    for s in symptoms:
        if not isinstance(s, dict) or s.get("confirmed") is False:
            continue

        raw = (s.get("raw_text") or s.get("symptom") or "").strip()
        cat = s.get("category")
        is_danger = bool(s.get("danger_sign")) and cat not in (None, "none", "null", "no_danger_sign_detected")

        if is_danger and cat:
            lbl_am = _category_display(cat, lang="am")
            lbl_en = _category_display(cat, lang="en")
            if lbl_am not in danger_labels_am:
                danger_labels_am.append(lbl_am)
            if lbl_en not in danger_labels_en:
                danger_labels_en.append(lbl_en)
        elif raw:
            # Non-danger recorded symptom
            if raw not in general_labels_am:
                general_labels_am.append(raw)
            if raw not in general_labels_en:
                general_labels_en.append(raw)

    # 1. Danger sign alert
    if danger_labels_am:
        if len(danger_labels_am) == 1:
            am_names = danger_labels_am[0]
            en_names = danger_labels_en[0]
            summary_am = f"{am_names} የአደጋ ምልክት ተገኝቷል፣ በአስቸቋይ የህክምና እርዳታ ያግኙ"
            summary_en = f"{en_names} danger sign detected, seek medical help immediately."
        else:
            am_names = " እና ".join([", ".join(danger_labels_am[:-1]), danger_labels_am[-1]]) if len(danger_labels_am) > 2 else " እና ".join(danger_labels_am)
            en_names = ", ".join(danger_labels_en)
            summary_am = f"{am_names} የአደጋ ምልክቶች ተገኝተዋል፣ በአስቸቋይ የህክምና እርዳታ ያግኙ"
            summary_en = f"{en_names} danger signs detected, seek medical help immediately."

        return {
            "summary_text_am": summary_am,
            "summary_text_en": summary_en,
            "danger_sign_triggered": True,
        }

    # 2. General recorded symptoms
    if general_labels_am:
        if len(general_labels_am) == 1:
            am_names = general_labels_am[0]
            en_names = general_labels_en[0]
            summary_am = f"ምንም የአደጋ ምልክት አልተገኘም፣ ነገር ግን {am_names} ምልክት ተመዝግቧል"
            summary_en = f"No danger signs detected, but {en_names} symptom recorded."
        else:
            am_names = " እና ".join([", ".join(general_labels_am[:-1]), general_labels_am[-1]]) if len(general_labels_am) > 2 else " እና ".join(general_labels_am)
            en_names = ", ".join(general_labels_en)
            summary_am = f"ምንም የአደጋ ምልክት አልተገኘም፣ ነገር ግን {am_names} ምልክቶች ተመዝግበዋል"
            summary_en = f"No danger signs detected, but {en_names} symptoms recorded."

        return {
            "summary_text_am": summary_am,
            "summary_text_en": summary_en,
            "danger_sign_triggered": False,
        }

    # 3. No symptoms / clear
    return {
        "summary_text_am": "ምንም የአደጋ ምልክት አልተገኘም",
        "summary_text_en": "No danger signs detected.",
        "danger_sign_triggered": False,
    }
