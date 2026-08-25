import pytest
from app.services.nutrition import (
    FOOD_GROUPS,
    calculate_food_group_shares,
    classify_ethiopian_food,
)


def test_classify_ethiopian_food_grains() -> None:
    assert classify_ethiopian_food("ዛሬ ጤፍ እንጀራ እና ዳቦ በላሁ") == ["grains"]
    assert classify_ethiopian_food("genfo with kinche") == ["grains"]
    assert classify_ethiopian_food("በሶ ጠጣሁ") == ["grains"]


def test_classify_ethiopian_food_multi_group() -> None:
    # Injera (Grains) + Shiro (Proteins) + Gomen (Fruits & Vegetables)
    text = "ዛሬ እንጀራ በሽሮ እና ጎመን በላሁ"
    groups = classify_ethiopian_food(text)
    assert "grains" in groups
    assert "proteins" in groups
    assert "fruits_and_vegetables" in groups
    assert "dairy" not in groups


def test_classify_ethiopian_food_dairy() -> None:
    text = "ክትፎ በአይብ እና ቅቤ በላሁ"
    groups = classify_ethiopian_food(text)
    assert "proteins" in groups  # kitfo
    assert "dairy" in groups     # ayib / kibe


def test_calculate_food_group_shares_sums_to_100_percent() -> None:
    # 7 food entries spanning multiple dates and groups
    food_logs = [
        {"date": "2026-08-20", "raw_text": "እንጀራ በሽሮ", "food_groups": ["grains", "proteins"]},
        {"date": "2026-08-21", "raw_text": "ዳቦ እና ወተት", "food_groups": ["grains", "dairy"]},
        {"date": "2026-08-22", "raw_text": "ጎመን እና ድንች", "food_groups": ["fruits_and_vegetables"]},
        {"date": "2026-08-23", "raw_text": "ምስር ወጥ", "food_groups": ["proteins"]},
        {"date": "2026-08-24", "raw_text": "ክትፎ በአይብ", "food_groups": ["proteins", "dairy"]},
        {"date": "2026-08-25", "raw_text": "ሙዝ እና አቮካዶ", "food_groups": ["fruits_and_vegetables"]},
    ]

    shares = calculate_food_group_shares(food_logs)

    assert shares["total_items_classified"] > 0
    assert shares["tracked_days"] == 6

    # Verify percentages sum to exactly 100
    percentages = shares["percentages"]
    assert sum(percentages.values()) == 100

    # Verify all 4 food groups are present in counts and percentages
    for group in FOOD_GROUPS:
        assert group in percentages
        assert group in shares["counts"]
        assert percentages[group] >= 0

    assert len(shares["group_breakdown"]) == 4


def test_calculate_food_group_shares_empty() -> None:
    shares = calculate_food_group_shares([])
    assert shares["total_items_classified"] == 0
    assert sum(shares["percentages"].values()) == 0
    assert shares["average_daily_diversity"] == 0.0
