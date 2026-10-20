"""Score a protected labeled corpus against captured provider results offline.

No clinical thresholds are supplied by this tool. A named reviewer must provide
an explicit evaluation policy. Passing the score does not approve patient use.
"""

import argparse
import hashlib
import json
import math
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


def require(condition):
    if not condition:
        raise ValueError("Invalid or incomplete evaluation inputs")


def words(text):
    require(isinstance(text, str) and len(text) <= 16000)
    result = unicodedata.normalize("NFC", text).split()
    require(len(result) <= 2000)
    return result


def distance(expected, actual):
    row = list(range(len(actual) + 1))
    for i, left in enumerate(expected, 1):
        next_row = [i]
        for j, right in enumerate(actual, 1):
            next_row.append(
                min(next_row[-1] + 1, row[j] + 1, row[j - 1] + (left != right))
            )
        row = next_row
    return row[-1]


def indexed(cases):
    require(isinstance(cases, list) and 0 < len(cases) <= 10000)
    result = {}
    for case in cases:
        key = case["id"]
        require(
            isinstance(key, str)
            and re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", key)
            and key not in result
        )
        require(isinstance(case["fields"], dict))
        categories = case["danger_categories"]
        require(
            isinstance(categories, list) and all(isinstance(c, str) for c in categories)
        )
        require(len(categories) == len(set(categories)))
        words(case["transcript"])
        result[key] = case
    return result


def score(corpus, predictions, policy, corpus_digest):
    expected, actual = indexed(corpus["cases"]), indexed(predictions["cases"])
    require(expected.keys() == actual.keys())
    require(predictions["corpus_sha256"] == corpus_digest)
    require(bool(corpus["version"]) and bool(policy["approved_by"].strip()))
    approval = datetime.fromisoformat(policy["approved_at"].replace("Z", "+00:00"))
    captured = datetime.fromisoformat(
        predictions["generated_at"].replace("Z", "+00:00")
    )
    require(approval.tzinfo is not None and captured.tzinfo is not None)
    require(approval <= captured <= datetime.now(timezone.utc))
    for key in ("source_revision", "provider", "prompt_version", "policy_version"):
        require(isinstance(predictions[key], str) and bool(predictions[key].strip()))
    require(re.fullmatch(r"[0-9a-f]{40}", predictions["source_revision"]))
    for key in (
        "max_word_error_rate",
        "min_field_accuracy",
        "min_danger_recall",
        "min_danger_precision",
    ):
        value = policy[key]
        require(
            type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1
        )
    for key in ("min_cases", "min_danger_cases"):
        require(type(policy[key]) is int and policy[key] > 0)
    edits = word_count = correct_fields = field_count = true_positive = (
        false_positive
    ) = false_negative = danger_cases = 0
    for key, reference in expected.items():
        candidate = actual[key]
        reference_words = words(reference["transcript"])
        edits += distance(reference_words, words(candidate["transcript"]))
        word_count += len(reference_words)
        fields = set(reference["fields"]) | set(candidate["fields"])
        field_count += len(fields)
        correct_fields += sum(
            k in reference["fields"]
            and k in candidate["fields"]
            and json.dumps(reference["fields"][k], sort_keys=True, allow_nan=False)
            == json.dumps(candidate["fields"][k], sort_keys=True, allow_nan=False)
            for k in fields
        )
        ref, pred = (
            set(reference["danger_categories"]),
            set(candidate["danger_categories"]),
        )
        danger_cases += bool(ref)
        true_positive += len(ref & pred)
        false_positive += len(pred - ref)
        false_negative += len(ref - pred)
    require(word_count > 0 and field_count > 0 and danger_cases > 0)
    metrics = {
        "cases": len(expected),
        "danger_cases": danger_cases,
        "word_error_rate": edits / word_count,
        "field_accuracy": correct_fields / field_count,
        "danger_recall": true_positive / (true_positive + false_negative),
        "danger_precision": true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0,
        "missed_danger_labels": false_negative,
        "extra_danger_labels": false_positive,
    }
    passed = (
        metrics["cases"] >= policy["min_cases"]
        and danger_cases >= policy["min_danger_cases"]
        and metrics["word_error_rate"] <= policy["max_word_error_rate"]
        and metrics["field_accuracy"] >= policy["min_field_accuracy"]
        and metrics["danger_recall"] >= policy["min_danger_recall"]
        and metrics["danger_precision"] >= policy["min_danger_precision"]
    )
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "corpus_sha256": corpus_digest,
        "thresholds_met": passed,
        "clinical_release_approved": False,
        "metrics": metrics,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("corpus", "predictions", "policy", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    try:
        corpus_bytes = args.corpus.read_bytes()
        report = score(
            json.loads(corpus_bytes),
            json.loads(args.predictions.read_bytes()),
            json.loads(args.policy.read_bytes()),
            hashlib.sha256(corpus_bytes).hexdigest(),
        )
        report["input_sha256"] = {
            name: hashlib.sha256(getattr(args, name).read_bytes()).hexdigest()
            for name in ("corpus", "predictions", "policy")
        }
        with args.output.open("x") as stream:
            json.dump(report, stream, indent=2)
            stream.write("\n")
    except (ValueError, KeyError, TypeError, OSError, AttributeError):
        raise SystemExit(
            "Evaluation refused: verify input schema, coverage, policy and provenance."
        ) from None
    print(
        "Evaluation thresholds "
        + ("met" if report["thresholds_met"] else "not met")
        + "; clinical review still required."
    )
    raise SystemExit(0 if report["thresholds_met"] else 1)


if __name__ == "__main__":
    main()
