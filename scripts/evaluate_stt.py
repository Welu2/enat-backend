#!/usr/bin/env python3
"""STT Accuracy & Error Evaluation Utility for EnatAI Benchmarking.

Evaluates hypothesis transcripts against reference ground-truth transcripts
using Levenshtein edit distance (Substitutions, Deletions, Insertions),
Word Error Rate (WER), Character Error Rate (CER), and visual word alignment.
Generates comprehensive file-by-file and overall summary Markdown reports.

Zero external dependencies (pure Python standard library).
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

AMHARIC_PUNCTUATION = "።፣፤፥፦፧፨፡"
LATIN_PUNCTUATION = ".,!?;:\"'()[]{}<>-–—/\\@#$%^&*_~`"
ALL_PUNCTUATION_PATTERN = re.compile(
    "[" + re.escape(AMHARIC_PUNCTUATION + LATIN_PUNCTUATION) + "]"
)


def normalize_text(text: str) -> str:
    """Normalize text for STT evaluation: lowercases Latin, strips punctuation and collapses spaces."""
    if not text:
        return ""
    # Lowercase Latin characters
    cleaned = text.lower()
    # Normalize unicode apostrophes and quotes
    cleaned = cleaned.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # Strip internal contractions apostrophe (e.g. couldn't -> couldnt, i'm -> im, it's -> its)
    cleaned = re.sub(r"(\w)'(\w)", r"\1\2", cleaned)
    # Strip Amharic and Latin punctuation
    cleaned = ALL_PUNCTUATION_PATTERN.sub(" ", cleaned)
    # Collapse multiple whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def align_sequences(
    ref_tokens: list[str], hyp_tokens: list[str]
) -> tuple[int, int, int, int, list[tuple[str, str, str]]]:
    """Compute NIST sclite-standard alignment between reference and hypothesis tokens.

    Uses standard speech recognition weights (Sub=4, Del=3, Ins=3) to prevent
    spurious multi-word substitutions when tokens are merely inserted or deleted.

    Returns:
        (total_errors, substitutions, deletions, insertions, alignment_list)
        where alignment_list contains tuples of (status, ref_token, hyp_token),
        with status in {"OK", "SUB", "DEL", "INS"}.
    """
    n, m = len(ref_tokens), len(hyp_tokens)

    # dp[i][j] = (weighted_cost, s, d, i)
    dp = [[(0, 0, 0, 0)] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][0] = (i * 3, 0, i, 0)
    for j in range(1, m + 1):
        dp[0][j] = (j * 3, 0, 0, j)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref_tokens[i - 1] == hyp_tokens[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                sub = (
                    dp[i - 1][j - 1][0] + 4,
                    dp[i - 1][j - 1][1] + 1,
                    dp[i - 1][j - 1][2],
                    dp[i - 1][j - 1][3],
                )
                dele = (
                    dp[i - 1][j][0] + 3,
                    dp[i - 1][j][1],
                    dp[i - 1][j][2] + 1,
                    dp[i - 1][j][3],
                )
                ins = (
                    dp[i][j - 1][0] + 3,
                    dp[i][j - 1][1],
                    dp[i][j - 1][2],
                    dp[i][j - 1][3] + 1,
                )
                dp[i][j] = min(sub, dele, ins, key=lambda x: x[0])

    _, s, d, ins_count = dp[n][m]
    total_errors = s + d + ins_count

    # Backtrace alignment
    alignment: list[tuple[str, str, str]] = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref_tokens[i - 1] == hyp_tokens[j - 1]:
            alignment.append(("OK", ref_tokens[i - 1], hyp_tokens[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j][0] == dp[i - 1][j - 1][0] + 4:
            alignment.append(("SUB", ref_tokens[i - 1], hyp_tokens[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j][0] == dp[i - 1][j][0] + 3:
            alignment.append(("DEL", ref_tokens[i - 1], "---"))
            i -= 1
        else:
            alignment.append(("INS", "---", hyp_tokens[j - 1]))
            j -= 1

    alignment.reverse()
    return total_errors, s, d, ins_count, alignment


def evaluate_pair(
    reference_text: str,
    hypothesis_text: str,
    normalize: bool = True,
) -> dict[str, Any]:
    """Compare a hypothesis transcript against a reference ground truth string.

    Returns an evaluation dictionary containing words count, errors count,
    S/D/I breakdown, WER %, Word Accuracy %, CER %, and word alignment.
    """
    ref_clean = normalize_text(reference_text) if normalize else reference_text.strip()
    hyp_clean = normalize_text(hypothesis_text) if normalize else hypothesis_text.strip()

    ref_words = ref_clean.split() if ref_clean else []
    hyp_words = hyp_clean.split() if hyp_clean else []

    total_words = len(ref_words)

    # 1. Word-level Evaluation
    if total_words == 0:
        error_count = len(hyp_words)
        s, d, i = 0, 0, error_count
        alignment = [("INS", "---", w) for w in hyp_words]
    else:
        error_count, s, d, i, alignment = align_sequences(ref_words, hyp_words)

    wer = round(error_count / max(total_words, 1), 4)
    word_accuracy = round(max(0.0, 1.0 - wer), 4)

    # 2. Character-level Evaluation (CER)
    ref_chars = list(ref_clean.replace(" ", ""))
    hyp_chars = list(hyp_clean.replace(" ", ""))
    total_chars = len(ref_chars)

    if total_chars == 0:
        char_errors = len(hyp_chars)
    else:
        char_errors, _, _, _, _ = align_sequences(ref_chars, hyp_chars)

    cer = round(char_errors / max(total_chars, 1), 4)
    char_accuracy = round(max(0.0, 1.0 - cer), 4)

    return {
        "reference_text": reference_text,
        "hypothesis_text": hypothesis_text,
        "normalized_reference": ref_clean,
        "normalized_hypothesis": hyp_clean,
        "total_words": total_words,
        "error_count": error_count,
        "substitutions": s,
        "deletions": d,
        "insertions": i,
        "wer": wer,
        "wer_percent": f"{wer * 100:.1f}%",
        "word_accuracy": word_accuracy,
        "word_accuracy_percent": f"{word_accuracy * 100:.1f}%",
        "total_chars": total_chars,
        "char_error_count": char_errors,
        "cer": cer,
        "cer_percent": f"{cer * 100:.1f}%",
        "char_accuracy_percent": f"{char_accuracy * 100:.1f}%",
        "alignment": alignment,
    }


def format_alignment_display(alignment: list[tuple[str, str, str]]) -> str:
    """Format token alignment into a clean visual comparison string."""
    if not alignment:
        return "(empty)"

    ref_row = ["REF :"]
    hyp_row = ["HYP :"]
    stat_row = ["EVAL:"]

    for stat, r_tok, h_tok in alignment:
        col_width = max(len(r_tok), len(h_tok), len(stat)) + 2
        ref_row.append(r_tok.ljust(col_width))
        hyp_row.append(h_tok.ljust(col_width))
        tag = "✓" if stat == "OK" else stat
        stat_row.append(tag.ljust(col_width))

    return "\n".join([" ".join(ref_row), " ".join(hyp_row), " ".join(stat_row)])


def get_reference_text(gt_data: dict[str, Any], filename: str) -> str | None:
    """Lookup reference text flexibly by filename, stem, or voice ID.

    Matches 'v1', 'v1.wav', 'V1', '1', etc.
    """
    stem = Path(filename).stem.lower()  # e.g. 'v1'
    num_str = stem.lstrip("v")          # e.g. '1'

    candidates = [
        stem,
        filename,
        filename.lower(),
        stem.upper(),
        num_str,
        f"v{num_str}",
        f"V{num_str}",
    ]
    for c in candidates:
        if c in gt_data and str(gt_data[c]).strip():
            return str(gt_data[c]).strip()
    return None


def derive_report_filename(results_path: Path, output_arg: str | None, metadata: dict[str, Any]) -> Path:
    """Determine destination Markdown filename (e.g. report_for_v1_v5.md)."""
    if output_arg:
        return Path(output_arg)

    # 1. Match 'v1_v5' in results filename
    match = re.search(r"v\d+_v\d+", results_path.stem, re.IGNORECASE)
    if match:
        return Path(f"report_for_{match.group(0).lower()}.md")

    # 2. Check metadata start/end index
    start = metadata.get("start_index")
    end = metadata.get("end_index")
    if start is not None and end is not None:
        return Path(f"report_for_v{start}_v{end}.md")

    # 3. Fallback
    return Path(f"report_for_{results_path.stem}.md")


def generate_markdown_report(
    res_filename: str,
    gt_filename: str,
    metadata: dict[str, Any],
    model_stats: dict[str, dict[str, Any]],
    file_evaluations: list[dict[str, Any]],
) -> str:
    """Generate comprehensive Markdown report containing executive summary and file breakdowns."""
    lang = metadata.get("language_code", "am").upper()
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = []
    lines.append(f"# STT Benchmark Evaluation Report")
    lines.append("")
    lines.append(f"- **Benchmark Results**: `{res_filename}`")
    lines.append(f"- **Ground Truth**: `{gt_filename}`")
    lines.append(f"- **Language**: {lang}")
    lines.append(f"- **Total Audio Files Evaluated**: {len(file_evaluations)}")
    lines.append(f"- **Evaluation Date**: {now_str}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Overall Model Comparison")
    lines.append("")
    lines.append(
        "| Model | Total Ref Words | Total Errors | Sub (S) | Del (D) | Ins (I) | Word Error Rate (WER) | Word Accuracy | Character Error (CER) | Avg Latency |"
    )
    lines.append(
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    )

    for m_name, st in model_stats.items():
        tot_w = max(int(st["total_words"]), 1)
        err_w = int(st["error_count"])
        sub_w = int(st["substitutions"])
        del_w = int(st["deletions"])
        ins_w = int(st["insertions"])
        wer_val = err_w / tot_w
        acc_val = max(0.0, 1.0 - wer_val)

        tot_c = max(int(st["total_chars"]), 1)
        err_c = int(st["char_errors"])
        cer_val = err_c / tot_c

        lats = st["latencies"]
        avg_lat = f"{sum(lats) / len(lats):.2f}s" if lats else "N/A"

        disp_name = m_name.replace("_", " ").title()
        lines.append(
            f"| **{disp_name}** | {tot_w} | {err_w} | {sub_w} | {del_w} | {ins_w} | **{wer_val * 100:.1f}%** | **{acc_val * 100:.1f}%** | {cer_val * 100:.1f}% | {avg_lat} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Detailed File-by-File Evaluation")
    lines.append("")

    for fe in file_evaluations:
        fname = fe["filename"]
        ref_text = fe["reference_text"]
        lines.append(f"### Voice: `{fname}`")
        lines.append(f"> **Ground Truth Reference**:")
        lines.append(f"> *{ref_text}*")
        lines.append("")

        for m_name, m_res in fe["models"].items():
            disp_name = m_name.replace("_", " ").title()
            lat_str = f"{m_res.get('latency_seconds', 'N/A')}s"

            if "error" in m_res and not m_res.get("hypothesis_text"):
                lines.append(f"#### {disp_name} (Failed)")
                lines.append(f"- **Error**: `{m_res['error']}`")
                lines.append(f"- **Latency**: {lat_str}")
                lines.append("")
                continue

            lines.append(f"#### {disp_name}")
            lines.append(
                f"- **Latency**: {lat_str} | **Ref Words**: {m_res['total_words']} | "
                f"**Errors**: {m_res['error_count']} (S: {m_res['substitutions']}, D: {m_res['deletions']}, I: {m_res['insertions']})"
            )
            lines.append(
                f"- **WER**: **{m_res['wer_percent']}** | **Word Accuracy**: **{m_res['word_accuracy_percent']}** | **CER**: {m_res['cer_percent']}"
            )
            lines.append("")
            lines.append("```text")
            lines.append(format_alignment_display(m_res["alignment"]))
            lines.append("```")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate STT hypothesis against ground truth reference text."
    )
    parser.add_argument(
        "--results",
        "-r",
        type=str,
        default=None,
        help="Path to benchmark JSON results file (e.g. 'benchmark_results_v1_v5_am.json').",
    )
    parser.add_argument(
        "--transcripts",
        "--transcript",
        "-t",
        "--ground-truth",
        "-g",
        dest="transcripts",
        type=str,
        default=None,
        help="Path to transcript.json containing ground truth mappings (e.g. {'v1': '...'}).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Destination markdown report file (e.g. 'report_for_v1_v5.md'). Defaults automatically.",
    )
    parser.add_argument(
        "--ref",
        type=str,
        default=None,
        help="Ground truth reference transcript string (for single comparison).",
    )
    parser.add_argument(
        "--hyp",
        type=str,
        default=None,
        help="Hypothesis transcript string produced by model (for single comparison).",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Audio filename in results JSON (e.g. 'v1.wav').",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help="STT model name in results JSON (e.g. 'sahara', 'addis_ai', 'gemini').",
    )
    parser.add_argument(
        "--no-normalize",
        dest="normalize",
        action="store_false",
        default=True,
        help="Do not normalize text (keep punctuation and casing as-is).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON output instead of formatted report.",
    )

    args = parser.parse_args()

    # Auto-detect transcript.json if not passed explicitly
    transcripts_path_str = args.transcripts
    if not transcripts_path_str and Path("transcript.json").exists():
        transcripts_path_str = "transcript.json"

    # Case 1: Batch evaluate whole results file against transcript.json
    if args.results and transcripts_path_str:
        res_path = Path(args.results)
        gt_path = Path(transcripts_path_str)

        if not res_path.exists():
            print(f"Error: Results file '{res_path}' not found.", file=sys.stderr)
            sys.exit(1)
        if not gt_path.exists():
            print(f"Error: Transcript / Ground Truth file '{gt_path}' not found.", file=sys.stderr)
            sys.exit(1)

        with open(res_path, "r", encoding="utf-8") as f:
            res_data = json.load(f)
        with open(gt_path, "r", encoding="utf-8") as f:
            gt_data = json.load(f)

        metadata = res_data.get("metadata", {})
        out_report_path = derive_report_filename(res_path, args.output, metadata)

        model_stats: dict[str, dict[str, Any]] = {}
        file_evaluations: list[dict[str, Any]] = []

        raw_results = res_data.get("results", [])
        total_files = len(raw_results)

        print("\n" + "=" * 70)
        print("EnatAI STT Benchmark Evaluator")
        print(f"• Results File     : {res_path.resolve()}")
        print(f"• Transcript File  : {gt_path.resolve()}")
        print(f"• Target Report    : {out_report_path.resolve()}")
        print("=" * 70)

        for idx, item in enumerate(raw_results, start=1):
            fname = item.get("filename", "")
            ref_text = get_reference_text(gt_data, fname)
            if not ref_text:
                print(f"[{idx}/{total_files}] [SKIP] No transcript found in '{gt_path.name}' for '{fname}'.")
                continue

            models_dict = item.get("models", {})
            file_entry: dict[str, Any] = {
                "filename": fname,
                "reference_text": ref_text,
                "models": {},
            }

            model_summaries = []
            for m_name, m_res in models_dict.items():
                if m_name not in model_stats:
                    model_stats[m_name] = {
                        "total_words": 0,
                        "error_count": 0,
                        "substitutions": 0,
                        "deletions": 0,
                        "insertions": 0,
                        "total_chars": 0,
                        "char_errors": 0,
                        "latencies": [],
                    }

                if "error" in m_res and not m_res.get("hypothesis_text"):
                    file_entry["models"][m_name] = {
                        "error": m_res.get("error", "Unknown error"),
                        "latency_seconds": m_res.get("latency_seconds", "N/A"),
                    }
                    model_summaries.append(f"{m_name}=FAIL")
                    continue

                hyp = m_res.get("hypothesis_text", "")
                eval_res = evaluate_pair(ref_text, hyp, normalize=args.normalize)
                eval_res["latency_seconds"] = m_res.get("latency_seconds", "N/A")

                st = model_stats[m_name]
                st["total_words"] += eval_res["total_words"]
                st["error_count"] += eval_res["error_count"]
                st["substitutions"] += eval_res["substitutions"]
                st["deletions"] += eval_res["deletions"]
                st["insertions"] += eval_res["insertions"]
                st["total_chars"] += eval_res["total_chars"]
                st["char_errors"] += eval_res["char_error_count"]
                if isinstance(eval_res["latency_seconds"], (int, float)):
                    st["latencies"].append(eval_res["latency_seconds"])

                file_entry["models"][m_name] = eval_res
                model_summaries.append(f"{m_name}={eval_res['error_count']}err")

            file_evaluations.append(file_entry)
            summary_str = ", ".join(model_summaries) if model_summaries else "Done"
            print(f"[{idx}/{total_files}] Evaluated '{fname}' (Ref: {len(ref_text.split())} words) -> [{summary_str}]")

        if not file_evaluations:
            print(f"[WARN] No matching transcripts found between '{res_path}' and '{gt_path}'.", file=sys.stderr)
            sys.exit(1)

        # Generate and save Markdown Report
        report_content = generate_markdown_report(
            res_filename=res_path.name,
            gt_filename=gt_path.name,
            metadata=metadata,
            model_stats=model_stats,
            file_evaluations=file_evaluations,
        )

        with open(out_report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        # Print Executive Summary in Console
        print("\n" + "=" * 78)
        print("OVERALL MODEL BENCHMARK SCOREBOARD")
        print("=" * 78)
        print(
            f"{'Model':<12} | {'Words':<7} | {'Errors':<7} | {'WER':<8} | {'Accuracy':<9} | {'CER':<8} | {'Avg Latency'}"
        )
        print("-" * 78)

        for m_name, st in model_stats.items():
            tot_w = max(int(st["total_words"]), 1)
            err_w = int(st["error_count"])
            wer_val = err_w / tot_w
            acc_val = max(0.0, 1.0 - wer_val)

            tot_c = max(int(st["total_chars"]), 1)
            err_c = int(st["char_errors"])
            cer_val = err_c / tot_c

            lats = st["latencies"]
            avg_lat = f"{sum(lats) / len(lats):.2f}s" if lats else "N/A"

            print(
                f"{m_name:<12} | {tot_w:<7} | {err_w:<7} | {wer_val * 100:>6.1f}% | {acc_val * 100:>7.1f}% | {cer_val * 100:>6.1f}% | {avg_lat}"
            )
        print("=" * 78)
        print(f"[SUCCESS] Complete evaluation report saved to: '{out_report_path.resolve()}'\n")
        return

    # Case 2: Read single hypothesis from results JSON
    hypothesis = args.hyp
    if args.results and args.file and args.model:
        res_path = Path(args.results)
        if not res_path.exists():
            print(f"Error: Results file '{res_path}' not found.", file=sys.stderr)
            sys.exit(1)
        with open(res_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        matched_item = None
        for item in data.get("results", []):
            if item.get("filename") == args.file:
                matched_item = item
                break
        if not matched_item:
            print(f"Error: File '{args.file}' not found in '{res_path}'.", file=sys.stderr)
            sys.exit(1)
        model_entry = matched_item.get("models", {}).get(args.model)
        if not model_entry:
            print(f"Error: Model '{args.model}' not found for '{args.file}'.", file=sys.stderr)
            sys.exit(1)
        if "hypothesis_text" not in model_entry:
            print(f"Error: Model '{args.model}' failed for '{args.file}': {model_entry.get('error')}", file=sys.stderr)
            sys.exit(1)
        hypothesis = model_entry["hypothesis_text"]

    if not args.ref:
        print("Error: Provide --transcripts transcript.json or --ref <reference_text>.", file=sys.stderr)
        sys.exit(1)

    if hypothesis is None:
        print("Error: Provide --hyp <text> or (--results <file.json> --file <vN.wav> --model <name>).", file=sys.stderr)
        sys.exit(1)

    eval_result = evaluate_pair(args.ref, hypothesis, normalize=args.normalize)

    if args.json:
        clean_json = dict(eval_result)
        print(json.dumps(clean_json, ensure_ascii=False, indent=2))
        return

    print("\n" + "=" * 65)
    print("STT TRANSCRIPT EVALUATION REPORT")
    print("=" * 65)
    print(f"Reference  : {eval_result['reference_text']}")
    print(f"Hypothesis : {eval_result['hypothesis_text']}")
    print("-" * 65)
    print(f"• Total Words (Reference) : {eval_result['total_words']}")
    print(f"• Error Count (S + D + I) : {eval_result['error_count']}")
    print(f"    - Substitutions (S)   : {eval_result['substitutions']}")
    print(f"    - Deletions     (D)   : {eval_result['deletions']}")
    print(f"    - Insertions    (I)   : {eval_result['insertions']}")
    print(f"• Word Error Rate (WER)   : {eval_result['wer_percent']}")
    print(f"• Word Accuracy           : {eval_result['word_accuracy_percent']}")
    print(f"• Character Error (CER)   : {eval_result['cer_percent']}")
    print("-" * 65)
    print("WORD ALIGNMENT VISUALIZER:")
    print(format_alignment_display(eval_result["alignment"]))
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
