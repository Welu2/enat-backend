import copy
from datetime import datetime, timedelta, timezone

import pytest

from scripts.evaluate_voice import score


@pytest.fixture
def evaluation():
    cases = [
        {
            "id": "case-1",
            "transcript": "ትኩሳት አለኝ",
            "fields": {"category": "synthetic-danger"},
            "danger_categories": ["synthetic-danger"],
        },
        {
            "id": "case-2",
            "transcript": "ደህና ነኝ",
            "fields": {"category": None},
            "danger_categories": [],
        },
    ]
    now = datetime.now(timezone.utc)
    corpus = {"version": "synthetic-only", "cases": cases}
    predictions = {
        "corpus_sha256": "abc",
        "source_revision": "a" * 40,
        "provider": "synthetic",
        "prompt_version": "test",
        "policy_version": "test",
        "generated_at": now.isoformat(),
        "cases": copy.deepcopy(cases),
    }
    policy = {
        "approved_by": "synthetic-test-reviewer",
        "approved_at": (now - timedelta(hours=1)).isoformat(),
        "min_cases": 2,
        "min_danger_cases": 1,
        "max_word_error_rate": 0,
        "min_field_accuracy": 1,
        "min_danger_recall": 1,
        "min_danger_precision": 1,
    }
    return corpus, predictions, policy


def test_scores_do_not_grant_clinical_approval(evaluation):
    report = score(*evaluation, "abc")
    assert report["thresholds_met"]
    assert report["clinical_release_approved"] is False
    assert report["metrics"]["danger_recall"] == 1
    assert "cases" not in report


def test_missed_danger_and_invented_fields_fail(evaluation):
    corpus, predictions, policy = evaluation
    predictions["cases"][0]["danger_categories"] = []
    predictions["cases"][1]["fields"]["invented"] = "value"
    report = score(corpus, predictions, policy, "abc")
    assert not report["thresholds_met"]
    assert report["metrics"]["missed_danger_labels"] == 1
    assert report["metrics"]["field_accuracy"] < 1


@pytest.mark.parametrize(
    "kind", ["missing", "duplicate", "unapproved", "wrong_corpus", "threshold_nan"]
)
def test_incomplete_or_unreviewed_evaluation_rejected(evaluation, kind):
    corpus, predictions, policy = evaluation
    if kind == "missing":
        predictions["cases"].pop()
    if kind == "duplicate":
        predictions["cases"].append(predictions["cases"][0])
    if kind == "unapproved":
        policy["approved_by"] = ""
    if kind == "wrong_corpus":
        predictions["corpus_sha256"] = "wrong"
    if kind == "threshold_nan":
        policy["max_word_error_rate"] = float("nan")
    with pytest.raises(ValueError):
        score(corpus, predictions, policy, "abc")


def test_field_accuracy_does_not_coerce_boolean_and_number(evaluation):
    corpus, predictions, policy = evaluation
    corpus["cases"][0]["fields"] = {"confirmed": True}
    predictions["cases"][0]["fields"] = {"confirmed": 1}
    report = score(corpus, predictions, policy, "abc")
    assert not report["thresholds_met"]
    assert report["metrics"]["field_accuracy"] == 0.5
