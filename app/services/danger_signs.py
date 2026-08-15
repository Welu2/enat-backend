from app.core.constants import DANGER_SIGN_CATEGORIES


def check_danger_sign(category: str | None) -> bool:
    """Return True if *category* matches a protocol danger-sign category.

    Normalises the input to lowercase and strips whitespace before the lookup.
    Returns False if category is None or empty.
    """
    if not category:
        return False
    return category.lower().strip() in DANGER_SIGN_CATEGORIES
