import json
from pathlib import Path
import pytest

from scripts.evaluate_stt import normalize_text, align_sequences, evaluate_pair


def test_normalize_text_amharic_and_english():
    text = "  Hello, World! ይህ ምርመራ ነው።  "
    cleaned = normalize_text(text)
    assert cleaned == "hello world ይህ ምርመራ ነው"


def test_align_sequences_perfect_match():
    ref = ["hello", "world"]
    hyp = ["hello", "world"]
    cost, s, d, i, alignment = align_sequences(ref, hyp)
    assert cost == 0
    assert s == 0
    assert d == 0
    assert i == 0
    assert len(alignment) == 2
    assert all(a[0] == "OK" for a in alignment)


def test_align_sequences_substitution_deletion_insertion():
    ref = ["i", "have", "severe", "headache"]
    hyp = ["i", "had", "headache", "today"]
    cost, s, d, i, alignment = align_sequences(ref, hyp)
    # "have" -> "had" (SUB)
    # "severe" -> deleted (DEL)
    # "headache" -> "headache" (OK)
    # "today" -> inserted (INS)
    assert s == 1
    assert d == 1
    assert i == 1
    assert cost == 3


def test_evaluate_pair_amharic():
    ref = "ሁለት ቀን ከባድ ራስ ምታት አለኝ"
    hyp = "ሁለት ቀን ራስ ምታት አለኝ።"
    res = evaluate_pair(ref, hyp, normalize=True)
    assert res["total_words"] == 6
    # "ከባድ" was deleted
    assert res["deletions"] == 1
    assert res["substitutions"] == 0
    assert res["insertions"] == 0
    assert res["error_count"] == 1
    assert res["wer"] == round(1 / 6, 4)
    assert res["word_accuracy"] == round(5 / 6, 4)


def test_evaluate_pair_empty_inputs():
    res1 = evaluate_pair("", "")
    assert res1["total_words"] == 0
    assert res1["error_count"] == 0

    res2 = evaluate_pair("hello world", "")
    assert res2["total_words"] == 2
    assert res2["error_count"] == 2
    assert res2["deletions"] == 2
