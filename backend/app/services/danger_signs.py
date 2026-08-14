from app.core.constants import DANGER_SIGN_CATEGORIES


def check_danger_sign(category: str) -> bool:
    """Return True if *category* matches a protocol danger-sign category.

    Normalises the input to lowercase and strips whitespace before the lookup
    so that LLM responses with unexpected casing (e.g. "Severe_Headache") are
    still matched correctly rather than silently missing a danger sign.
    """
    return category.lower().strip() in DANGER_SIGN_CATEGORIES
