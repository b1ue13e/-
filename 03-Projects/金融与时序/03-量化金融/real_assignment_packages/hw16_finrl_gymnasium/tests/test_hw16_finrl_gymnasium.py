from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_smoke_runner(tmp_path: Path) -> None:
    package_root = Path(__file__).resolve().parents[1]
    workspace_root = package_root.parents[3]
    data_dir = workspace_root / "data" / "quant_finance" / "hw16_finrl_gymnasium"
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
    assert summary["homework_id"] == "HW16"
    assert summary["env_summary"]["observations"] == 3
    assert "action_space" in summary["env_summary"]
    assert (output_dir / "results" / "env_summary.json").exists()
