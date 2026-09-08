import json
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from scripts.run_benchmark import parse_range, run_benchmark, save_results_atomically


def test_parse_range_valid_formats() -> None:
    assert parse_range("1-5") == (1, 5)
    assert parse_range("v1-v5") == (1, 5)
    assert parse_range("1..10") == (1, 10)
    assert parse_range("v10-v20") == (10, 20)
    assert parse_range(" 5 - 15 ") == (5, 15)


def test_parse_range_invalid_formats() -> None:
    with pytest.raises(ValueError, match="Invalid range format"):
        parse_range("invalid")
    with pytest.raises(ValueError, match="Range start .* cannot be greater than end"):
        parse_range("10-5")


def test_save_results_atomically(tmp_path: Path) -> None:
    target_file = tmp_path / "test_out.json"
    data = {"hello": "world", "num": 42}
    save_results_atomically(target_file, data)

    assert target_file.exists()
    with open(target_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded == data


def test_run_benchmark_mocked_execution(tmp_path: Path) -> None:
    # Set up dummy voice directory structure: enat_voices/v1/v1.wav, v2/v2.wav
    voices_dir = tmp_path / "enat_voices"
    for v_num in (1, 2):
        v_folder = voices_dir / f"v{v_num}"
        v_folder.mkdir(parents=True)
        (v_folder / f"v{v_num}.wav").write_bytes(b"dummy audio wav")

    out_file = tmp_path / "benchmark_out.json"

    # Mock response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "results": [
            {
                "filename": "v1.wav",
                "stage_label": "symptoms",
                "models": {
                    "sahara": {"hypothesis_text": "t1", "latency_seconds": 1.2},
                    "addis_ai": {"hypothesis_text": "t2", "latency_seconds": 0.9},
                    "gemini": {"hypothesis_text": "t3", "latency_seconds": 1.0},
                },
            }
        ]
    }

    with patch("httpx.Client.post", return_value=mock_resp) as mock_post:
        payload = run_benchmark(
            start=1,
            end=2,
            language="am",
            stage="symptoms",
            voices_dir=voices_dir,
            output_file=out_file,
            delay=0.0,
            resume=False,
        )

    assert mock_post.call_count == 2
    assert out_file.exists()
    assert len(payload["results"]) == 2
    assert payload["metadata"]["completed_count"] == 2
    assert payload["metadata"]["language_code"] == "am"


def test_run_benchmark_resumes_skipping_completed(tmp_path: Path) -> None:
    voices_dir = tmp_path / "enat_voices"
    for v_num in (1, 2, 3):
        v_folder = voices_dir / f"v{v_num}"
        v_folder.mkdir(parents=True)
        (v_folder / f"v{v_num}.wav").write_bytes(b"dummy audio wav")

    out_file = tmp_path / "benchmark_out.json"
    # Pre-populate v1.wav as completed
    existing_data = {
        "metadata": {"completed_count": 1},
        "results": [
            {
                "filename": "v1.wav",
                "stage_label": "symptoms",
                "models": {"sahara": {"hypothesis_text": "already done", "latency_seconds": 1.0}},
            }
        ],
    }
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f)

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "results": [
            {
                "filename": "v2.wav",
                "stage_label": "symptoms",
                "models": {"sahara": {"hypothesis_text": "new", "latency_seconds": 0.8}},
            }
        ]
    }

    with patch("httpx.Client.post", return_value=mock_resp) as mock_post:
        payload = run_benchmark(
            start=1,
            end=3,
            language="am",
            stage="symptoms",
            voices_dir=voices_dir,
            output_file=out_file,
            delay=0.0,
            resume=True,
        )

    # v1 was already completed, so post should only be called for v2 and v3 (2 calls)
    assert mock_post.call_count == 2
    filenames = [r["filename"] for r in payload["results"]]
    assert "v1.wav" in filenames
    assert len(payload["results"]) == 3


def test_run_benchmark_network_error_retains_prior_results(tmp_path: Path) -> None:
    import httpx

    voices_dir = tmp_path / "enat_voices"
    for v_num in (1, 2):
        v_folder = voices_dir / f"v{v_num}"
        v_folder.mkdir(parents=True)
        (v_folder / f"v{v_num}.wav").write_bytes(b"dummy audio wav")

    out_file = tmp_path / "benchmark_out.json"

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "results": [
            {
                "filename": "v1.wav",
                "stage_label": "symptoms",
                "models": {"sahara": {"hypothesis_text": "v1 success", "latency_seconds": 1.0}},
            }
        ]
    }

    # First call succeeds for v1, second call raises RequestError for v2
    with patch("httpx.Client.post", side_effect=[mock_resp, httpx.ConnectError("Connection refused")]):
        payload = run_benchmark(
            start=1,
            end=2,
            language="am",
            voices_dir=voices_dir,
            output_file=out_file,
            delay=0.0,
            resume=False,
        )

    # Output file was saved with v1 intact
    assert out_file.exists()
    with open(out_file, "r", encoding="utf-8") as f:
        saved_on_disk = json.load(f)
    assert len(saved_on_disk["results"]) == 1
    assert saved_on_disk["results"][0]["filename"] == "v1.wav"
