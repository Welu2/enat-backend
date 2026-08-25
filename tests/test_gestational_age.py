from datetime import date, timedelta
import pytest

from app.services.gestational_age import (
    calculate_gestational_age_and_edd,
    classify_trimester,
    format_gestational_age_am,
    format_gestational_age_en,
    get_current_pregnancy_status,
)


def test_classify_trimester_boundaries() -> None:
    # 1st Trimester: 0 to 13 weeks + 6 days
    assert classify_trimester(0, 0) == "first_trimester"
    assert classify_trimester(13, 6) == "first_trimester"
    assert classify_trimester(12, 0) == "first_trimester"

    # 2nd Trimester: 14 to 27 weeks + 6 days
    assert classify_trimester(14, 0) == "second_trimester"
    assert classify_trimester(20, 3) == "second_trimester"
    assert classify_trimester(27, 6) == "second_trimester"

    # 3rd Trimester: 28 weeks and above
    assert classify_trimester(28, 0) == "third_trimester"
    assert classify_trimester(36, 4) == "third_trimester"
    assert classify_trimester(40, 0) == "third_trimester"


def test_formatting_helpers() -> None:
    assert format_gestational_age_am(16, 3) == "16 ሳምንት ከ 3 ቀን"
    assert format_gestational_age_am(16, 0) == "16 ሳምንት"

    assert format_gestational_age_en(1, 1) == "1 week, 1 day"
    assert format_gestational_age_en(16, 3) == "16 weeks, 3 days"
    assert format_gestational_age_en(20, 0) == "20 weeks"


def test_calculate_gestational_age_from_lnmp() -> None:
    as_of = date(2026, 8, 25)
    # LNMP: 100 days ago -> 14 weeks and 2 days -> 2nd trimester
    lnmp = as_of - timedelta(days=100)

    result = calculate_gestational_age_and_edd(
        pregnancy_counting_method="lnmp",
        lnmp_date=lnmp,
        as_of_date=as_of,
    )

    assert result["gestational_age_weeks"] == 14
    assert result["gestational_age_days"] == 2
    assert result["gestational_age_total_days"] == 100
    assert result["trimester"] == "second_trimester"
    assert result["trimester_info"]["number"] == 2
    assert result["estimated_due_date"] == lnmp + timedelta(days=280)
    assert result["effective_lnmp_date"] == lnmp
    assert result["is_gestational_age_manual"] is False
    assert result["days_until_edd"] == 180  # 280 - 100


def test_calculate_gestational_age_from_ultrasound() -> None:
    as_of = date(2026, 8, 25)
    # Scan was 14 days ago on 2026-08-11 and showed 10 weeks, 0 days
    scan_date = as_of - timedelta(days=14)
    scan_weeks = 10

    result = calculate_gestational_age_and_edd(
        pregnancy_counting_method="ultrasound",
        ultrasound_date=scan_date,
        ultrasound_weeks=scan_weeks,
        ultrasound_days=0,
        as_of_date=as_of,
    )

    # Effective LNMP was 70 days before scan date (84 days before as_of)
    # Current gestational age: 12 weeks, 0 days -> 1st trimester
    assert result["gestational_age_weeks"] == 12
    assert result["gestational_age_days"] == 0
    assert result["gestational_age_total_days"] == 84
    assert result["trimester"] == "first_trimester"
    assert result["effective_lnmp_date"] == as_of - timedelta(days=84)
    assert result["estimated_due_date"] == result["effective_lnmp_date"] + timedelta(days=280)


def test_calculate_gestational_age_manual_override() -> None:
    as_of = date(2026, 8, 25)

    result = calculate_gestational_age_and_edd(
        pregnancy_counting_method="manual",
        manual_gestational_weeks=30,
        manual_gestational_days=4,
        as_of_date=as_of,
    )

    assert result["gestational_age_weeks"] == 30
    assert result["gestational_age_days"] == 4
    assert result["gestational_age_total_days"] == 214
    assert result["trimester"] == "third_trimester"
    assert result["is_gestational_age_manual"] is True
    assert result["effective_lnmp_date"] == as_of - timedelta(days=214)
    assert result["estimated_due_date"] == result["effective_lnmp_date"] + timedelta(days=280)


def test_get_current_pregnancy_status_progression() -> None:
    user_record = {
        "id": "11111111-1111-1111-1111-111111111111",
        "lnmp_date": "2026-05-01",
        "effective_lnmp_date": "2026-05-01",
        "estimated_due_date": "2027-02-05",
    }

    as_of = date(2026, 8, 25)  # 116 days after 2026-05-01 = 16 weeks + 4 days
    status = get_current_pregnancy_status(user_record, as_of_date=as_of)

    assert status is not None
    assert status["gestational_age_weeks"] == 16
    assert status["gestational_age_days"] == 4
    assert status["trimester"] == "second_trimester"
    assert "16 ሳምንት" in status["formatted_age_am"]
