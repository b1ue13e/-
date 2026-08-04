from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_smoke_runner(tmp_path: Path) -> None:
    package_root = Path(__file__).resolve().parents[1]
    workspace_root = package_root.parents[3]
    data_dir = workspace_root / "data" / "quant_finance" / "hw02_markowitz_frontier"
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
    assert summary["homework_id"] == "HW02"
    assert "equal_weight" in summary["frontier_summary"]
    assert "inverse_vol_weight" in summary["frontier_summary"]
    assert (output_dir / "results" / "frontier_summary.json").exists()
