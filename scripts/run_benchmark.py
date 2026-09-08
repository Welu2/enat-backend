#!/usr/bin/env python3
"""Automated STT Model Benchmark Runner for EnatAI.

Sequentially submits audio files from enat_voices to /dev/benchmark-stt,
persists results incrementally after each file, and supports resuming.
"""

import argparse
import json
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import sys
import time
from typing import Any

import httpx


def parse_range(range_str: str) -> tuple[int, int]:
    """Parse range strings like '1-5', 'v1-v5', '1..5', 'v1..v5'."""
    clean = range_str.strip().lower().replace("v", "")
    match = re.match(r"^(\d+)\s*(?:-|\.\.)\s*(\d+)$", clean)
    if not match:
        raise ValueError(
            f"Invalid range format '{range_str}'. Expected formats like '1-5' or 'v1-v5'."
        )
    start, end = int(match.group(1)), int(match.group(2))
    if start > end:
        raise ValueError(f"Range start ({start}) cannot be greater than end ({end}).")
    return start, end


def save_results_atomically(output_path: Path, data: dict[str, Any]) -> None:
    """Save JSON data atomically via temp file to prevent corruption on interrupt."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(f".tmp.{os.getpid()}")
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp_path.replace(output_path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


def run_benchmark(
    start: int = 1,
    end: int = 5,
    language: str = "am",
    stage: str = "symptoms",
    voices_dir: str | Path = "enat_voices",
    output_file: str | Path | None = None,
    endpoint_url: str = "http://localhost:8000/dev/benchmark-stt",
    delay: float = 3.5,
    resume: bool = True,
    timeout: float = 120.0,
    gemini_model: str | None = None,
) -> dict[str, Any]:
    """Run sequential benchmark requests across a range of voice audio files."""
    voices_path = Path(voices_dir)
    lang_code = "en" if str(language).lower().startswith("en") else "am"
    effective_stage = stage.strip() or "symptoms"

    effective_gemini_model = (gemini_model or "").strip()
    if not effective_gemini_model:
        try:
            from dotenv import dotenv_values
            effective_gemini_model = (dotenv_values(".env").get("GEMINI_TRANSCRIBE_MODEL") or "").strip()
        except Exception:
            pass

    if output_file:
        out_path = Path(output_file)
    else:
        out_path = Path(f"benchmark_results_v{start}_v{end}_{lang_code}.json")

    # Load existing results if resuming
    results: list[dict[str, Any]] = []
    results_by_filename: dict[str, dict[str, Any]] = {}

    expected_models = (
        ["sahara", "addis_ai", "gemini"]
        if lang_code == "am"
        else ["sahara", "deepgram", "gemini"]
    )

    if resume and out_path.exists():
        try:
            with open(out_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                results = existing_data.get("results", [])
                for r in results:
                    fname = r.get("filename")
                    if fname:
                        results_by_filename[fname] = r
            fully_complete = sum(
                1 for r in results
                if r.get("models") and not any("error" in m for m in r["models"].values())
            )
            print(
                f"[RESUME] Found existing output file '{out_path}' with {len(results)} records "
                f"({fully_complete} fully successful, {len(results) - fully_complete} needing model retries)."
            )
        except Exception as e:
            print(f"[WARN] Could not parse existing '{out_path}' ({e}). Starting fresh.")
            results = []
            results_by_filename = {}

    target_indices = list(range(start, end + 1))
    total_requested = len(target_indices)

    print("=" * 65)
    print(f"EnatAI STT Benchmark Runner")
    print(f"• Voice Range   : v{start} to v{end} ({total_requested} files)")
    print(f"• Language      : {lang_code.upper()}")
    print(f"• Stage Label   : {effective_stage}")
    print(f"• Voices Dir    : {voices_path.resolve()}")
    print(f"• Endpoint URL  : {endpoint_url}")
    if effective_gemini_model:
        print(f"• Gemini Model  : {effective_gemini_model}")
    print(f"• Rate Delay    : {delay}s between requests")
    print(f"• Output Path   : {out_path.resolve()}")
    print("=" * 65)

    def build_payload() -> dict[str, Any]:
        fully_complete = sum(
            1 for r in results
            if r.get("models") and not any("error" in m for m in r["models"].values())
        )
        return {
            "metadata": {
                "language_code": lang_code,
                "stage_label": effective_stage,
                "start_index": start,
                "end_index": end,
                "total_requested": total_requested,
                "completed_count": fully_complete,
                "last_updated": datetime.now(timezone.utc).isoformat(),
            },
            "results": results,
        }

    client = httpx.Client(timeout=timeout)
    try:
        for idx, voice_num in enumerate(target_indices, start=1):
            voice_id = f"v{voice_num}"
            filename = f"{voice_id}.wav"

            # Check nested folder v{n}/v{n}.wav then flat fallback
            audio_file = voices_path / voice_id / filename
            if not audio_file.exists():
                audio_file = voices_path / filename

            if not audio_file.exists():
                print(f"[{idx}/{total_requested}] [MISSING] File '{audio_file}' not found. Skipping.")
                continue

            existing_entry = results_by_filename.get(filename)
            models_to_run = expected_models
            if existing_entry and resume:
                existing_models = existing_entry.get("models", {})
                failed_or_missing = [
                    m for m in expected_models
                    if m not in existing_models or "error" in existing_models[m]
                ]
                if not failed_or_missing:
                    print(f"[{idx}/{total_requested}] [SKIP] '{filename}' already fully completed.")
                    continue
                models_to_run = failed_or_missing
                retry_str = ", ".join(models_to_run)
                print(
                    f"[{idx}/{total_requested}] [RETRY] '{filename}' ({audio_file.stat().st_size / 1024:.1f} KB) - retrying {retry_str}...",
                    end="",
                    flush=True,
                )
            else:
                print(
                    f"[{idx}/{total_requested}] Benchmarking '{filename}' ({audio_file.stat().st_size / 1024:.1f} KB)...",
                    end="",
                    flush=True,
                )

            try:
                with open(audio_file, "rb") as af:
                    audio_bytes = af.read()

                req_data: dict[str, Any] = {
                    "language_code": lang_code,
                    "stage_label": effective_stage,
                }
                if effective_gemini_model:
                    req_data["gemini_model"] = effective_gemini_model
                # Pass targeted models if only a subset needs retrying
                if models_to_run != expected_models:
                    req_data["models"] = ",".join(models_to_run)

                resp = client.post(
                    endpoint_url,
                    files={"files": (filename, audio_bytes, "audio/wav")},
                    data=req_data,
                )

                if resp.status_code != 200:
                    err_msg = f"HTTP {resp.status_code}: {resp.text[:150]}"
                    print(f" FAILED ({err_msg})")
                    if not existing_entry:
                        failed_entry = {
                            "filename": filename,
                            "stage_label": effective_stage,
                            "request_error": err_msg,
                            "models": {},
                        }
                        results.append(failed_entry)
                        results_by_filename[filename] = failed_entry
                else:
                    data = resp.json()
                    file_results = data.get("results", [])
                    returned_item = file_results[0] if file_results else {}
                    new_models = returned_item.get("models", {})

                    if existing_entry:
                        # Patch in-place without losing other successful models!
                        existing_entry.setdefault("models", {}).update(new_models)
                        item = existing_entry
                    else:
                        item = {
                            "filename": filename,
                            "stage_label": effective_stage,
                            "models": new_models,
                        }
                        results.append(item)
                        results_by_filename[filename] = item

                    # Summarize model latencies
                    models = item.get("models", {})
                    lat_parts = []
                    for m_name, m_val in models.items():
                        if "latency_seconds" in m_val and "error" not in m_val:
                            lat_parts.append(f"{m_name}={m_val['latency_seconds']}s")
                        elif "error" in m_val:
                            lat_parts.append(f"{m_name}=ERR")
                    lat_str = ", ".join(lat_parts) if lat_parts else "Done"
                    print(f" OK [{lat_str}]")

                # Persist immediately to disk after each file
                save_results_atomically(out_path, build_payload())

            except httpx.RequestError as exc:
                print(f" NETWORK ERROR ({exc})")
                print(
                    f"[WARN] Halting run due to network error on '{filename}'. Existing results saved to '{out_path}'."
                )
                save_results_atomically(out_path, build_payload())
                break

            except Exception as exc:
                print(f" UNEXPECTED ERROR ({exc})")
                print(
                    f"[WARN] Halting run on '{filename}'. Existing results saved to '{out_path}'."
                )
                save_results_atomically(out_path, build_payload())
                break

            # Rate-limit delay before next file
            if delay > 0 and idx < total_requested:
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\n" + "-" * 65)
        print(f"[INTERRUPT] Benchmark aborted by user (Ctrl+C).")
        save_results_atomically(out_path, build_payload())
        print(f"[INFO] Successfully saved {len(results)} completed results to '{out_path}'.")

    finally:
        client.close()

    # Final Summary
    final_payload = build_payload()
    save_results_atomically(out_path, final_payload)

    print("\n" + "=" * 65)
    print("Benchmark Run Summary")
    print(f"• Total Saved Files : {len(results)} / {total_requested}")
    print(f"• Output File       : {out_path.resolve()}")

    if results:
        # Compute average latencies across all successful results
        model_latencies: dict[str, list[float]] = {}
        for r in results:
            for m_name, m_data in r.get("models", {}).items():
                if "latency_seconds" in m_data and "error" not in m_data:
                    model_latencies.setdefault(m_name, []).append(
                        m_data["latency_seconds"]
                    )

        if model_latencies:
            print("\n• Average Model Latencies:")
            for m_name, lats in model_latencies.items():
                avg_lat = sum(lats) / len(lats)
                print(
                    f"  - {m_name:10s}: {avg_lat:.2f}s avg across {len(lats)} samples"
                )
    print("=" * 65)

    return final_payload


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automated sequential STT benchmark runner for EnatAI audio voices."
    )
    parser.add_argument(
        "--start",
        "-s",
        type=int,
        default=1,
        help="Starting voice index (e.g. 1 for v1). Default: 1.",
    )
    parser.add_argument(
        "--end",
        "-e",
        type=int,
        default=5,
        help="Ending voice index (e.g. 5 for v5). Default: 5.",
    )
    parser.add_argument(
        "--range",
        "-r",
        type=str,
        default=None,
        help="Voice range shortcut, e.g. '1-5' or 'v1-v5'. Overrides --start/--end.",
    )
    parser.add_argument(
        "--language",
        "-l",
        type=str,
        default="am",
        choices=["am", "en"],
        help="Language code: 'am' (Amharic) or 'en' (English). Default: 'am'.",
    )
    parser.add_argument(
        "--stage",
        type=str,
        default="symptoms",
        help="Check-in stage label (symptoms, food, supplement, closing). Default: 'symptoms'.",
    )
    parser.add_argument(
        "--voices-dir",
        type=str,
        default="enat_voices",
        help="Path to directory containing voice folders. Default: 'enat_voices'.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Path for destination JSON. Default: benchmark_results_v{start}_v{end}_{lang}.json.",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000/dev/benchmark-stt",
        help="Endpoint URL. Default: 'http://localhost:8000/dev/benchmark-stt'.",
    )
    parser.add_argument(
        "--delay",
        "-d",
        type=float,
        default=3.5,
        help="Delay in seconds between requests to prevent API rate-limiting. Default: 3.5.",
    )
    parser.add_argument(
        "--resume",
        dest="resume",
        action="store_true",
        default=True,
        help="Resume previously saved file if it exists, skipping already processed files. (Default: True).",
    )
    parser.add_argument(
        "--no-resume",
        dest="resume",
        action="store_false",
        help="Do not resume; start fresh and overwrite output file.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="HTTP request timeout in seconds per audio file. Default: 120.0.",
    )
    parser.add_argument(
        "--gemini-model",
        type=str,
        default=None,
        help="Explicit Gemini model to use (e.g. 'gemini-3.5-flash', 'gemini-3.5-transcribe'). Defaults to GEMINI_TRANSCRIBE_MODEL in .env.",
    )

    args = parser.parse_args()

    start, end = args.start, args.end
    if args.range:
        start, end = parse_range(args.range)

    run_benchmark(
        start=start,
        end=end,
        language=args.language,
        stage=args.stage,
        voices_dir=args.voices_dir,
        output_file=args.output,
        endpoint_url=args.url,
        delay=args.delay,
        resume=args.resume,
        timeout=args.timeout,
        gemini_model=args.gemini_model,
    )


if __name__ == "__main__":
    main()
