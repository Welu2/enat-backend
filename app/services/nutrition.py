from typing import Any, Literal

FoodGroupKey = Literal["grains", "proteins", "dairy", "fruits_and_vegetables"]

FOOD_GROUPS: list[FoodGroupKey] = ["grains", "proteins", "dairy", "fruits_and_vegetables"]

FOOD_GROUP_METADATA: dict[FoodGroupKey, dict[str, Any]] = {
    "grains": {
        "key": "grains",
        "name_en": "Grains & Cereals",
        "name_am": "እህል እና የእህል ውጤቶች",
        "examples_en": "Injera, teff, barley (gebs), besso, genfo, sorghum, millet, corn, wheat, dabo, kinche, rice, pasta",
        "examples_am": "እንጀራ፣ ጤፍ፣ ገብስ፣ በሶ፣ ገንፎ፣ ማሽላ፣ ዳጉሳ፣ በቆሎ፣ ስንዴ፣ ዳቦ፣ ቂንጬ፣ ሩዝ",
    },
    "proteins": {
        "key": "proteins",
        "name_en": "Proteins & Legumes",
        "name_am": "ፕሮቲን፣ ስጋ እና ጥራጥሬ",
        "examples_en": "Lentils (misir), split peas (kik), chickpeas (shiro), beef, chicken (doro), lamb, goat, fish, eggs, beans",
        "examples_am": "ምስር፣ ክክ፣ ሽሮ፣ የበሬ ስጋ፣ ዶሮ፣ በግ፣ ፍየል፣ አሳ፣ እንቁላል፣ ባቄላ፣ አተር",
    },
    "dairy": {
        "key": "dairy",
        "name_en": "Dairy Products",
        "name_am": "የወተት ተዋጽኦ",
        "examples_en": "Ayibe (cottage cheese), kibe (butter), ergo (sour milk / yogurt), milk (wetet)",
        "examples_am": "አይብ፣ ቅቤ፣ እርጎ፣ ወተት",
    },
    "fruits_and_vegetables": {
        "key": "fruits_and_vegetables",
        "name_en": "Fruits & Vegetables",
        "name_am": "አትክልት እና ፍራፍሬ",
        "examples_en": "Collard greens (gomen), cabbage, potatoes (dinich), beets (key sir), tomatoes, onions, carrots, peppers, banana, orange, avocado, mango, papaya",
        "examples_am": "ጎመን፣ ጥቅል ጎመን፣ ድንች፣ ቀይ ስር፣ ቲማቲም፣ ሽንኩርት፣ ካሮት፣ ቃሪያ፣ ሙዝ፣ ብርቱካን፣ አቮካዶ፣ ማንጎ፣ ፓፓያ",
    },
}

# Ethiopian keywords / dish dictionary mapping to food groups
_KEYWORD_TAXONOMY: dict[str, list[FoodGroupKey]] = {
    # Grains
    "እንጀራ": ["grains"],
    "injera": ["grains"],
    "ጤፍ": ["grains"],
    "teff": ["grains"],
    "ገብስ": ["grains"],
    "gebs": ["grains"],
    "barley": ["grains"],
    "በሶ": ["grains"],
    "besso": ["grains"],
    "ገንፎ": ["grains"],
    "genfo": ["grains"],
    "porridge": ["grains"],
    "ማሽላ": ["grains"],
    "sorghum": ["grains"],
    "ዳጉሳ": ["grains"],
    "millet": ["grains"],
    "በቆሎ": ["grains"],
    "corn": ["grains"],
    "ስንዴ": ["grains"],
    "wheat": ["grains"],
    "ዳቦ": ["grains"],
    "dabo": ["grains"],
    "bread": ["grains"],
    "ቂንጬ": ["grains"],
    "kinche": ["grains"],
    "ሩዝ": ["grains"],
    "rice": ["grains"],
    "ፓስታ": ["grains"],
    "pasta": ["grains"],
    "አጃ": ["grains"],
    "oats": ["grains"],
    "cereal": ["grains"],
    "እህል": ["grains"],

    # Proteins / Legumes / Meats
    "ምስር": ["proteins"],
    "misir": ["proteins"],
    "lentil": ["proteins"],
    "lentils": ["proteins"],
    "ክክ": ["proteins"],
    "kik": ["proteins"],
    "split peas": ["proteins"],
    "ሽሮ": ["proteins"],
    "ሺሮ": ["proteins"],
    "shiro": ["proteins"],
    "chickpea": ["proteins"],
    "chickpeas": ["proteins"],
    "ስጋ": ["proteins"],
    "sega": ["proteins"],
    "meat": ["proteins"],
    "beef": ["proteins"],
    "ክትፎ": ["proteins"],
    "kitfo": ["proteins"],
    "ጥብስ": ["proteins"],
    "tibs": ["proteins"],
    "ጎረድ": ["proteins"],
    "gored": ["proteins"],
    "ዶሮ": ["proteins"],
    "doro": ["proteins"],
    "chicken": ["proteins"],
    "በግ": ["proteins"],
    "bagi": ["proteins"],
    "lamb": ["proteins"],
    "ፍየል": ["proteins"],
    "goat": ["proteins"],
    "አሳ": ["proteins"],
    "ዓሳ": ["proteins"],
    "asa": ["proteins"],
    "fish": ["proteins"],
    "እንቁላል": ["proteins"],
    "inqulal": ["proteins"],
    "egg": ["proteins"],
    "eggs": ["proteins"],
    "ባቄላ": ["proteins"],
    "bakela": ["proteins"],
    "beans": ["proteins"],
    "አተር": ["proteins"],
    "peas": ["proteins"],
    "አኩሪ አተር": ["proteins"],
    "soy": ["proteins"],

    # Dairy
    "አይብ": ["dairy"],
    "ayibe": ["dairy"],
    "ayib": ["dairy"],
    "cottage cheese": ["dairy"],
    "cheese": ["dairy"],
    "ቅቤ": ["dairy"],
    "kibe": ["dairy"],
    "butter": ["dairy"],
    "እርጎ": ["dairy"],
    "ergo": ["dairy"],
    "yogurt": ["dairy"],
    "sour milk": ["dairy"],
    "ወተት": ["dairy"],
    "wetet": ["dairy"],
    "milk": ["dairy"],

    # Fruits & Vegetables
    "ጎመን": ["fruits_and_vegetables"],
    "gomen": ["fruits_and_vegetables"],
    "ጥቅል ጎመን": ["fruits_and_vegetables"],
    "cabbage": ["fruits_and_vegetables"],
    "ድንች": ["fruits_and_vegetables"],
    "dinich": ["fruits_and_vegetables"],
    "potato": ["fruits_and_vegetables"],
    "potatoes": ["fruits_and_vegetables"],
    "አትክልት": ["fruits_and_vegetables"],
    "vegetable": ["fruits_and_vegetables"],
    "vegetables": ["fruits_and_vegetables"],
    "ቀይ ስር": ["fruits_and_vegetables"],
    "key sir": ["fruits_and_vegetables"],
    "beet": ["fruits_and_vegetables"],
    "beets": ["fruits_and_vegetables"],
    "ቲማቲም": ["fruits_and_vegetables"],
    "timatim": ["fruits_and_vegetables"],
    "tomato": ["fruits_and_vegetables"],
    "tomatoes": ["fruits_and_vegetables"],
    "ሽንኩርት": ["fruits_and_vegetables"],
    "shinkurt": ["fruits_and_vegetables"],
    "onion": ["fruits_and_vegetables"],
    "onions": ["fruits_and_vegetables"],
    "ነጭ ሽንኩርት": ["fruits_and_vegetables"],
    "garlic": ["fruits_and_vegetables"],
    "ካሮት": ["fruits_and_vegetables"],
    "karot": ["fruits_and_vegetables"],
    "carrot": ["fruits_and_vegetables"],
    "carrots": ["fruits_and_vegetables"],
    "ሰላጣ": ["fruits_and_vegetables"],
    "salad": ["fruits_and_vegetables"],
    "lettuce": ["fruits_and_vegetables"],
    "በርበሬ": ["fruits_and_vegetables"],
    "ቃሪያ": ["fruits_and_vegetables"],
    "pepper": ["fruits_and_vegetables"],
    "peppers": ["fruits_and_vegetables"],
    "awaze": ["fruits_and_vegetables"],
    "mitmita": ["fruits_and_vegetables"],
    "ዱባ": ["fruits_and_vegetables"],
    "pumpkin": ["fruits_and_vegetables"],
    "ሙዝ": ["fruits_and_vegetables"],
    "muz": ["fruits_and_vegetables"],
    "banana": ["fruits_and_vegetables"],
    "ብርቱካን": ["fruits_and_vegetables"],
    "birtukan": ["fruits_and_vegetables"],
    "orange": ["fruits_and_vegetables"],
    "አቮካዶ": ["fruits_and_vegetables"],
    "avocado": ["fruits_and_vegetables"],
    "ማንጎ": ["fruits_and_vegetables"],
    "mango": ["fruits_and_vegetables"],
    "ፓፓያ": ["fruits_and_vegetables"],
    "papaya": ["fruits_and_vegetables"],
    "ፖም": ["fruits_and_vegetables"],
    "apple": ["fruits_and_vegetables"],
    "ፍራፍሬ": ["fruits_and_vegetables"],
    "fruit": ["fruits_and_vegetables"],
    "fruits": ["fruits_and_vegetables"],
    "ሀብሀብ": ["fruits_and_vegetables"],
    "watermelon": ["fruits_and_vegetables"],
    "ዘይቱን": ["fruits_and_vegetables"],
    "guava": ["fruits_and_vegetables"],
    "ሎሚ": ["fruits_and_vegetables"],
    "lemon": ["fruits_and_vegetables"],
}


def classify_ethiopian_food(raw_text: str | None) -> list[FoodGroupKey]:
    """Classifies an Amharic or English food description into one or more of the 4 food groups."""
    if not raw_text:
        return []

    text_lower = raw_text.lower()
    matched_groups: set[FoodGroupKey] = set()

    for keyword, groups in _KEYWORD_TAXONOMY.items():
        if keyword in text_lower:
            for g in groups:
                matched_groups.add(g)

    # Return in canonical order
    return [g for g in FOOD_GROUPS if g in matched_groups]


def calculate_food_group_shares(food_logs: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregates all confirmed food logs and computes the exact percentage share out of 100% for each food group.
    
    The sum of all group percentages is guaranteed to equal 100% when food data exists.
    """
    counts: dict[FoodGroupKey, int] = {
        "grains": 0,
        "proteins": 0,
        "dairy": 0,
        "fruits_and_vegetables": 0,
    }

    distinct_days: set[str] = set()
    daily_groups: dict[str, set[FoodGroupKey]] = {}

    for entry in food_logs:
        date_str = str(entry.get("date") or entry.get("timestamp") or "")[:10]
        if date_str:
            distinct_days.add(date_str)
            daily_groups.setdefault(date_str, set())

        # Check explicit food_groups or classify raw_text
        groups = entry.get("food_groups")
        if not groups:
            raw_text = entry.get("raw_text") or entry.get("name") or str(entry)
            groups = classify_ethiopian_food(raw_text)

        for g in groups:
            clean_g = str(g).lower().strip()
            # Normalize group keys
            if clean_g in ("grain", "grains", "cereal", "cereals"):
                counts["grains"] += 1
                if date_str:
                    daily_groups[date_str].add("grains")
            elif clean_g in ("protein", "proteins", "meat", "legume", "legumes"):
                counts["proteins"] += 1
                if date_str:
                    daily_groups[date_str].add("proteins")
            elif clean_g in ("dairy", "milk"):
                counts["dairy"] += 1
                if date_str:
                    daily_groups[date_str].add("dairy")
            elif clean_g in ("fruit", "fruits", "vegetable", "vegetables", "fruits_and_vegetables"):
                counts["fruits_and_vegetables"] += 1
                if date_str:
                    daily_groups[date_str].add("fruits_and_vegetables")

    total_occurrences = sum(counts.values())
    percentages: dict[FoodGroupKey, int] = {
        "grains": 0,
        "proteins": 0,
        "dairy": 0,
        "fruits_and_vegetables": 0,
    }

    if total_occurrences > 0:
        # Compute exact rounded percentages summing to 100
        raw_pcts = {g: (counts[g] / total_occurrences) * 100 for g in FOOD_GROUPS}
        floored = {g: int(raw_pcts[g]) for g in FOOD_GROUPS}
        remainder = 100 - sum(floored.values())

        # Distribute remaining points to the highest fractional parts
        fractional_parts = sorted(
            FOOD_GROUPS,
            key=lambda g: (raw_pcts[g] - floored[g]),
            reverse=True,
        )
        for i in range(remainder):
            floored[fractional_parts[i % len(fractional_parts)]] += 1

        percentages = floored

    # Average daily dietary diversity score (number of distinct groups per day, max 4)
    avg_diversity = 0.0
    if distinct_days:
        total_unique_groups = sum(len(groups) for groups in daily_groups.values())
        avg_diversity = round(total_unique_groups / len(distinct_days), 1)

    group_breakdown = [
        {
            "key": g,
            "name_en": FOOD_GROUP_METADATA[g]["name_en"],
            "name_am": FOOD_GROUP_METADATA[g]["name_am"],
            "count": counts[g],
            "percentage": percentages[g],
        }
        for g in FOOD_GROUPS
    ]

    return {
        "total_items_classified": total_occurrences,
        "tracked_days": len(distinct_days),
        "average_daily_diversity": avg_diversity,
        "counts": counts,
        "percentages": percentages,
        "group_breakdown": group_breakdown,
    }
