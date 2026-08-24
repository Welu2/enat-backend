from datetime import date, timedelta
from typing import Any, Literal

TrimesterKey = Literal["first_trimester", "second_trimester", "third_trimester"]

TRIMESTER_INFO: dict[TrimesterKey, dict[str, Any]] = {
    "first_trimester": {
        "number": 1,
        "key": "first_trimester",
        "name_en": "1st Trimester",
        "name_am": "1ኛ ትሪሚስተር (1-13 ሳምንት)",
        "week_range": "1 - 13 weeks",
    },
    "second_trimester": {
        "number": 2,
        "key": "second_trimester",
        "name_en": "2nd Trimester",
        "name_am": "2ኛ ትሪሚስተር (14-27 ሳምንት)",
        "week_range": "14 - 27 weeks",
    },
    "third_trimester": {
        "number": 3,
        "key": "third_trimester",
        "name_en": "3rd Trimester",
        "name_am": "3ኛ ትሪሚስተር (28-40+ ሳምንት)",
        "week_range": "28 - 40+ weeks",
    },
}


def classify_trimester(gestational_weeks: int, gestational_days: int = 0) -> TrimesterKey:
    """Classify pregnancy stage into 1st, 2nd, or 3rd trimester based on gestational age."""
    total_days = (gestational_weeks * 7) + gestational_days
    if total_days < 14 * 7:  # 0 to 13 weeks + 6 days (< 98 days)
        return "first_trimester"
    elif total_days < 28 * 7:  # 14 to 27 weeks + 6 days (< 196 days)
        return "second_trimester"
    else:  # 28 weeks and above
        return "third_trimester"


def format_gestational_age_am(weeks: int, days: int = 0) -> str:
    """Format gestational age in Amharic (e.g., '16 ሳምንት ከ 3 ቀን')."""
    if days > 0:
        return f"{weeks} ሳምንት ከ {days} ቀን"
    return f"{weeks} ሳምንት"


def format_gestational_age_en(weeks: int, days: int = 0) -> str:
    """Format gestational age in English (e.g., '16 weeks, 3 days')."""
    week_str = f"{weeks} week" if weeks == 1 else f"{weeks} weeks"
    if days > 0:
        day_str = f"{days} day" if days == 1 else f"{days} days"
        return f"{week_str}, {day_str}"
    return week_str


def calculate_gestational_age_and_edd(
    pregnancy_counting_method: str = "lnmp",
    lnmp_date: date | None = None,
    ultrasound_date: date | None = None,
    ultrasound_weeks: int | None = None,
    ultrasound_days: int | None = None,
    manual_gestational_weeks: int | None = None,
    manual_gestational_days: int | None = None,
    as_of_date: date | None = None,
) -> dict[str, Any]:
    """Calculates fetal gestational age, trimester classification, and Estimated Due Date (EDD).
    
    Standard obstetric rules:
    - EDD = LNMP + 280 days (40 weeks) via Naegele's rule.
    - Gestational age = as_of_date - LNMP.
    - If ultrasound is used, effective LNMP = ultrasound_date - (ultrasound_weeks * 7 + days).
    - If manual weeks are entered, effective LNMP is computed backwards and stored alongside manual values.
    """
    today = as_of_date or date.today()
    clean_method = (pregnancy_counting_method or "lnmp").lower().strip()

    is_manual = False
    effective_lnmp: date | None = None

    # Case 1: Manual gestational age entered or overridden
    if manual_gestational_weeks is not None and manual_gestational_weeks >= 0:
        is_manual = True
        weeks = manual_gestational_weeks
        days = manual_gestational_days or 0
        total_days = (weeks * 7) + days
        effective_lnmp = today - timedelta(days=total_days)
        edd = effective_lnmp + timedelta(days=280)

    # Case 2: Ultrasound scan method
    elif clean_method == "ultrasound" and ultrasound_date and ultrasound_weeks is not None:
        us_days = (ultrasound_weeks * 7) + (ultrasound_days or 0)
        effective_lnmp = ultrasound_date - timedelta(days=us_days)
        total_days = max(0, (today - effective_lnmp).days)
        weeks = total_days // 7
        days = total_days % 7
        edd = effective_lnmp + timedelta(days=280)

    # Case 3: LNMP / LMNP (Last Normal Menstrual Period)
    elif lnmp_date:
        effective_lnmp = lnmp_date
        total_days = max(0, (today - lnmp_date).days)
        weeks = total_days // 7
        days = total_days % 7
        edd = lnmp_date + timedelta(days=280)

    else:
        # Fallback empty metrics
        return {
            "gestational_age_weeks": None,
            "gestational_age_days": None,
            "gestational_age_total_days": None,
            "formatted_age_am": None,
            "formatted_age_en": None,
            "trimester": None,
            "trimester_info": None,
            "estimated_due_date": None,
            "effective_lnmp_date": None,
            "is_gestational_age_manual": False,
            "days_until_edd": None,
        }

    trimester_key = classify_trimester(weeks, days)
    trimester_details = TRIMESTER_INFO[trimester_key]
    days_until_edd = max(0, (edd - today).days)

    return {
        "gestational_age_weeks": weeks,
        "gestational_age_days": days,
        "gestational_age_total_days": (weeks * 7) + days,
        "formatted_age_am": format_gestational_age_am(weeks, days),
        "formatted_age_en": format_gestational_age_en(weeks, days),
        "trimester": trimester_key,
        "trimester_info": trimester_details,
        "estimated_due_date": edd,
        "effective_lnmp_date": effective_lnmp,
        "is_gestational_age_manual": is_manual,
        "days_until_edd": days_until_edd,
    }


def get_current_pregnancy_status(user: dict[str, Any], as_of_date: date | None = None) -> dict[str, Any] | None:
    """Calculates live current gestational metrics for a user profile based on stored LNMP / EDD."""
    today = as_of_date or date.today()

    eff_lnmp = user.get("effective_lnmp_date") or user.get("lnmp_date")
    edd_raw = user.get("estimated_due_date")

    if eff_lnmp:
        lnmp_d = date.fromisoformat(eff_lnmp) if isinstance(eff_lnmp, str) else eff_lnmp
        return calculate_gestational_age_and_edd(
            pregnancy_counting_method="lnmp",
            lnmp_date=lnmp_d,
            as_of_date=today,
        )

    if edd_raw:
        edd_d = date.fromisoformat(edd_raw) if isinstance(edd_raw, str) else edd_raw
        approx_lnmp = edd_d - timedelta(days=280)
        return calculate_gestational_age_and_edd(
            pregnancy_counting_method="lnmp",
            lnmp_date=approx_lnmp,
            as_of_date=today,
        )

    # If only static weeks were stored
    if user.get("gestational_age_weeks") is not None:
        weeks = int(user["gestational_age_weeks"])
        days = int(user.get("gestational_age_days") or 0)
        trimester_key = classify_trimester(weeks, days)
        return {
            "gestational_age_weeks": weeks,
            "gestational_age_days": days,
            "gestational_age_total_days": (weeks * 7) + days,
            "formatted_age_am": format_gestational_age_am(weeks, days),
            "formatted_age_en": format_gestational_age_en(weeks, days),
            "trimester": trimester_key,
            "trimester_info": TRIMESTER_INFO[trimester_key],
            "estimated_due_date": None,
            "effective_lnmp_date": None,
            "is_gestational_age_manual": bool(user.get("is_gestational_age_manual")),
            "days_until_edd": None,
        }

    return None
