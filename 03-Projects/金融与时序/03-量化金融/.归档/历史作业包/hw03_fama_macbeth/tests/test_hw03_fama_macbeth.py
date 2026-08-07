from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_smoke_runner(tmp_path: Path) -> None:
    package_root = Path(__file__).resolve().parents[1]
    workspace_root = package_root.parents[3]
    data_dir = workspace_root / "data" / "quant_finance" / "hw03_fama_macbeth"
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
    assert summary["homework_id"] == "HW03"
    assert summary["fama_macbeth_summary"]["asset_count"] >= 2
    assert "risk_premium_proxy" in summary["fama_macbeth_summary"]
    assert (output_dir / "results" / "fama_macbeth_summary.json").exists()
