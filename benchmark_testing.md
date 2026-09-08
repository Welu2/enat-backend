# STT Model Benchmark Testing Guide

> **Context**: Benchmarking Speech-to-Text (STT) models for the **Sahara CodeSwitch Africa Challenge** on code-switched Amharic and English maternal health voice recordings.

This guide explains how to set up, configure, and run automated STT accuracy and latency benchmarks comparing:
- **Amharic (`language_code="am"`)**: **Sahara**, **Addis AI**, and **Gemini**
- **English (`language_code="en"`)**: **Sahara**, **Deepgram**, and **Gemini**

---

## 1. Prerequisites & Environment Setup

### A. Environment Variables (`.env`)
Ensure your `.env` file in the project root includes the required API keys and enables dev routes:

```env
# Enable development benchmark endpoints
ENABLE_DEV_ROUTES=true

# Model API Credentials
INTRON_API_KEY=your_sahara_api_key_here
INTRON_API_BASE_URL=https://api.intron.io

ADDIS_API_KEY=your_addis_ai_api_key_here
ADDIS_API_BASE_URL=https://api.addisassistant.com

GEMINI_API_KEY=your_gemini_api_key_here

DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

### B. Start the Backend Server
Launch the FastAPI development server:

```bash
uvicorn app.main:app --reload --port 8000
```

Verify that the server is running by opening: `http://localhost:8000/health` (should return `{"status": "ok"}`).

---

## 2. Voice Files Structure & Adjusting the Script

> [!IMPORTANT]
> **Adapting the script to your audio folder structure:**  
> By default, the automated script expects audio files organized as:
> ```text
> enat_voices/
> ├── v1/
> │   └── v1.wav
> ├── v2/
> │   └── v2.wav
> ├── v3/
> │   └── v3.wav
> ...
> ```

### How to adjust if your files are saved differently:

1. **Different Directory Name**:
   - Pass the `--voices-dir` flag when running the script:
     ```bash
     python scripts/run_benchmark.py --voices-dir my_custom_audio_folder --range 1-5
     ```

2. **Flat Directory (No subfolders)**:
   - If your audio files are stored flat as `enat_voices/v1.wav`, `enat_voices/v2.wav`, the script **already handles this automatically as a fallback**.

3. **Different Filename Pattern (e.g., `sample_01.wav` or `audio_1.wav`)**:
   - Open [`scripts/run_benchmark.py`](scripts/run_benchmark.py) and modify lines 112–115:
     ```python
     # Default pattern:
     voice_id = f"v{voice_num}"
     filename = f"{voice_id}.wav"
     audio_file = voices_path / voice_id / filename

     # Change to your pattern, for example:
     filename = f"sample_{voice_num:02d}.wav"
     audio_file = voices_path / filename
     ```

4. **Audio Format**:
   - The STT models require standard **`.wav`** files (16kHz or 44.1kHz PCM). Do not submit `.m4a` or `.mp3` files directly, as some models will reject them.

---

## 3. Running Automated Benchmarks

Use the dedicated CLI script [`scripts/run_benchmark.py`](scripts/run_benchmark.py). It runs requests **sequentially** (one file at a time), saves results **incrementally to disk**, and enforces rate-limit pauses.

### A. Recommended Batch Size: 5 Voices
Because model API keys (especially Addis AI and Sahara) have concurrency and per-minute rate limits, run batches of **5 voices** at a time.

### B. Run Amharic Batch (Voices 1 to 5)
```bash
python scripts/run_benchmark.py --range 1-5 --language am
```
*This sequentially tests Sahara, Addis AI, and Gemini on `v1.wav` through `v5.wav`.*

### C. Run English Batch (Voices 6 to 10)
```bash
python scripts/run_benchmark.py --range 6-10 --language en
```
*This sequentially tests Sahara, Deepgram, and Gemini on `v6.wav` through `v10.wav`.*

### D. Adjust Rate-Limit Pause (`--delay`)
If you hit HTTP 429 rate limits, increase the delay between files (e.g. 3 or 4 seconds):
```bash
python scripts/run_benchmark.py --range 1-5 --language am --delay 3.0
```

### E. Custom Output File (`--output`)
By default, results are saved to `benchmark_results_v{start}_v{end}_{lang}.json`. You can specify a custom filename:
```bash
python scripts/run_benchmark.py --range 1-5 --language am --output amharic_batch_01.json
```

---

## 4. Crash Recovery, Resuming & Smart Model-Level Retries

The script is built with zero-data-loss and zero-quota-waste guarantees:
- **Instant Persistence**: After each file finishes, the output JSON file on disk is immediately updated.
- **Smart Model-Level Retries**: A file is only considered truly complete if **all models succeeded without errors**. If one model (e.g. Gemini) failed due to a rate limit while Sahara and Addis AI succeeded:
  - Running the command again will **only re-call the failed model (Gemini)**.
  - It will **not** re-run or waste quota on the models that already succeeded.
  - Once the failed model succeeds, it patches its result **in-place** into the existing JSON entry!
- **Automatic Resume**: Re-running the command skips all files where all models succeeded and only processes incomplete/pending items:
  ```bash
  python scripts/run_benchmark.py --range 46-50 --language am
  ```
- **Start Fresh**: If you ever want to discard previous results instead of resuming/retrying, pass `--no-resume`:
  ```bash
  python scripts/run_benchmark.py --range 1-5 --language am --no-resume
  ```

---

## 5. Output JSON Format

The resulting JSON file matches the benchmarking evaluation format:

```json
{
  "metadata": {
    "language_code": "am",
    "stage_label": "symptoms",
    "start_index": 1,
    "end_index": 5,
    "total_requested": 5,
    "completed_count": 5,
    "last_updated": "2026-09-08T04:20:00Z"
  },
  "results": [
    {
      "filename": "v1.wav",
      "stage_label": "symptoms",
      "models": {
        "sahara": {
          "hypothesis_text": "ሁለት ቀን ከባድ ራስ ምታት እያለኝ ነው",
          "latency_seconds": 1.23
        },
        "addis_ai": {
          "hypothesis_text": "ሁለት ቀን ከባድ ራስ ምታት አለኝ",
          "latency_seconds": 0.87
        },
        "gemini": {
          "hypothesis_text": "ሁለት ቀን ከባድ ራስ ምታት እያለኝ ነው",
          "latency_seconds": 1.05
        }
      }
    }
  ]
}
```

If a specific model fails during a call, that model's slot will safely record the error and elapsed time without failing the other models or the batch:
```json
"addis_ai": {
  "error": "HTTP 429: Rate limit exceeded",
  "latency_seconds": 0.45
}
```

---

## 6. Calling the Endpoint Directly (cURL / Postman / Custom Scripts)

You can also send audio directly to the dev endpoint:

- **Endpoint**: `POST http://localhost:8000/dev/benchmark-stt`
- **Method**: `multipart/form-data`
- **Parameters**:
  - `files`: One or more audio files (e.g. `@v1.wav`)
  - `language_code`: `"am"` (default) or `"en"`
  - `stage_label`: `"symptoms"` (default metadata tag)

### cURL Example:
```bash
curl -X POST "http://localhost:8000/dev/benchmark-stt" \
  -F "files=@enat_voices/v1/v1.wav" \
  -F "language_code=am" \
  -F "stage_label=symptoms"
```

---

## 7. Next Step: Calculating Accuracy (WER / CER)

Once you collect the benchmark output JSON files, feed the `hypothesis_text` values into an offline evaluation script using `jiwer`:

```python
import json
import jiwer

# 1. Load benchmark hypotheses
with open("benchmark_results_v1_v5_am.json", "r", encoding="utf-8") as f:
    benchmark_data = json.load(f)

# 2. Reference ground truth transcripts
ground_truth = {
    "v1.wav": "ሁለት ቀን ከባድ ራስ ምታት እያለኝ ነው",
    # ...
}

# 3. Calculate Word Error Rate (WER) per model
for item in benchmark_data["results"]:
    filename = item["filename"]
    ref = ground_truth.get(filename)
    if not ref:
        continue
    for model_name, model_res in item["models"].items():
        hyp = model_res.get("hypothesis_text", "")
        wer = jiwer.wer(ref, hyp)
        print(f"[{model_name}] {filename} WER: {wer:.2%}")
```
