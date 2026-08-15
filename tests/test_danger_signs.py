import pytest

from app.core.constants import DANGER_SIGN_CATEGORIES
from app.services.danger_signs import check_danger_sign


@pytest.mark.parametrize(
    "category,expected",
    [
        ("severe_headache", True),
        ("vaginal_bleeding", True),
        ("mild_discomfort", False),
        ("", False),
    ],
)
def test_check_danger_sign(category: str, expected: bool) -> None:
    assert check_danger_sign(category) is expected


def test_all_categories_are_known() -> None:
    assert len(DANGER_SIGN_CATEGORIES) == 12
