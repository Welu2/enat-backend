from datetime import date, timedelta
import pytest

from app.services.anc_schedule import (
    WHO_ANC_CONTACTS,
    advance_to_next_anc_contact,
    calculate_all_anc_dates,
    generate_checkin_summary_text,
    get_next_anc_contact,
)


def test_calculate_all_anc_dates() -> None:
    lnmp = date(2026, 1, 1)
    schedule = calculate_all_anc_dates(lnmp)

    assert len(schedule) == 8
    assert schedule[0]["contact_number"] == 1
    assert schedule[0]["target_date"] == (lnmp + timedelta(weeks=12)).isoformat()
    assert schedule[1]["target_date"] == (lnmp + timedelta(weeks=20)).isoformat()
    assert schedule[7]["contact_number"] == 8
    assert schedule[7]["target_date"] == (lnmp + timedelta(weeks=40)).isoformat()


def test_get_next_anc_contact_selection() -> None:
    lnmp = date(2026, 1, 1)

    # 1. Mother at 8 weeks gestational age -> Next is Contact 1 (12 weeks)
    contact_8w = get_next_anc_contact(lnmp, as_of_date=lnmp + timedelta(weeks=8))
    assert contact_8w["contact_number"] == 1
    assert contact_8w["gestational_weeks"] == 12

    # 2. Mother at 15 weeks gestational age -> Next is Contact 2 (20 weeks)
    contact_15w = get_next_anc_contact(lnmp, as_of_date=lnmp + timedelta(weeks=15))
    assert contact_15w["contact_number"] == 2
    assert contact_15w["gestational_weeks"] == 20

    # 3. Mother at 22 weeks gestational age -> Next is Contact 3 (26 weeks)
    contact_22w = get_next_anc_contact(lnmp, as_of_date=lnmp + timedelta(weeks=22))
    assert contact_22w["contact_number"] == 3
    assert contact_22w["gestational_weeks"] == 26

    # 4. Mother at 28 weeks gestational age -> Next is Contact 4 (30 weeks)
    contact_28w = get_next_anc_contact(lnmp, as_of_date=lnmp + timedelta(weeks=28))
    assert contact_28w["contact_number"] == 4
    assert contact_28w["gestational_weeks"] == 30


def test_advance_to_next_anc_contact_schedule() -> None:
    lnmp = date(2026, 1, 1)
    c1_date = date(2026, 3, 26)  # Contact 1 date

    # Contact 1 (12w) -> Next after 8 weeks = Contact 2 (20w)
    next_c = advance_to_next_anc_contact(
        current_contact_num=1,
        current_appointment_date=c1_date,
        effective_lnmp=lnmp,
    )
    assert next_c is not None
    assert next_c["contact_number"] == 2
    assert next_c["gestational_weeks"] == 20
    assert next_c["appointment_date"] == (c1_date + timedelta(weeks=8)).isoformat()

    # Contact 2 (20w) -> Next after 6 weeks = Contact 3 (26w)
    c2_date = date(2026, 5, 21)
    next_c2 = advance_to_next_anc_contact(
        current_contact_num=2,
        current_appointment_date=c2_date,
        effective_lnmp=lnmp,
    )
    assert next_c2 is not None
    assert next_c2["contact_number"] == 3
    assert next_c2["appointment_date"] == (c2_date + timedelta(weeks=6)).isoformat()

    # Contact 7 (38w) -> Next after 2 weeks = Contact 8 (40w)
    c7_date = date(2026, 9, 24)
    next_c7 = advance_to_next_anc_contact(
        current_contact_num=7,
        current_appointment_date=c7_date,
        effective_lnmp=lnmp,
    )
    assert next_c7 is not None
    assert next_c7["contact_number"] == 8
    assert next_c7["appointment_date"] == (c7_date + timedelta(weeks=2)).isoformat()

    # Contact 8 (40w) -> No next contact
    next_c8 = advance_to_next_anc_contact(
        current_contact_num=8,
        current_appointment_date=date(2026, 10, 8),
        effective_lnmp=lnmp,
    )
    assert next_c8 is None


def test_generate_checkin_summary_text_danger_sign() -> None:
    symptoms = [
        {
            "category": "severe_headache",
            "danger_sign": True,
            "raw_text": "ከባድ ራስ ምታት አለኝ",
            "confirmed": True,
        }
    ]
    res = generate_checkin_summary_text(symptoms)
    assert res["danger_sign_triggered"] is True
    assert "ከባድ ራስ ምታት" in res["summary_text_am"]
    assert "የአደጋ ምልክት ተገኝቷል፣ በአስቸቋይ የህክምና እርዳታ ያግኙ" in res["summary_text_am"]
    assert "severe headache" in res["summary_text_en"].lower()
    assert "danger sign detected, seek medical help immediately." in res["summary_text_en"]


def test_generate_checkin_summary_text_non_danger_symptoms() -> None:
    symptoms = [
        {
            "category": None,
            "danger_sign": False,
            "raw_text": "ቀላል የጀርባ ህመም",
            "confirmed": True,
        }
    ]
    res = generate_checkin_summary_text(symptoms)
    assert res["danger_sign_triggered"] is False
    assert "ምንም የአደጋ ምልክት አልተገኘም" in res["summary_text_am"]
    assert "ቀላል የጀርባ ህመም" in res["summary_text_am"]
    assert "ምልክት ተመዝግቧል" in res["summary_text_am"]


def test_generate_checkin_summary_text_no_symptoms() -> None:
    res = generate_checkin_summary_text([])
    assert res["danger_sign_triggered"] is False
    assert res["summary_text_am"] == "ምንም የአደጋ ምልክት አልተገኘም"
    assert res["summary_text_en"] == "No danger signs detected."
