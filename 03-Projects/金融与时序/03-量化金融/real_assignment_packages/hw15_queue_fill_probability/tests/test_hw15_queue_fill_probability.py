from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_smoke_runner(tmp_path: Path) -> None:
    package_root = Path(__file__).resolve().parents[1]
    workspace_root = package_root.parents[3]
    data_dir = workspace_root / "data" / "quant_finance" / "hw15_queue_fill_probability"
    output_dir = tmp_path / "outputs"

    subprocess.run([
        sys.executable,
        str(package_root / "starter" / "run.py"),
        "--input-dir",
        str(data_dir),
        "--output-dir",
        str(output_dir),
    ], check=True)

    summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
    assert summary["homework_id"] == "HW15"
    assert summary["queue_summary"]["event_count"] == 3
    assert "fill_probability_proxy" in summary["queue_summary"]
    assert (output_dir / "results" / "queue_summary.json").exists()
