from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_smoke_runner(tmp_path: Path) -> None:
    package_root = Path(__file__).resolve().parents[1]
    manifest = json.loads((package_root / "package_manifest.json").read_text(encoding="utf-8"))
    data_dir = Path(manifest["real_data_dir"])
    output_dir = tmp_path / "outputs"

    subprocess.run(
        [
            sys.executable,
            str(package_root / "starter" / "run.py"),
            "--input-dir",
            str(data_dir),
            "--output-dir",
            str(output_dir),
        ],
        check=True,
    )

    summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
    smoke = summary["project_summary"]
    assert summary["homework_id"] == "HW06"
    assert smoke["proposal_completeness"] == 1.0
    assert smoke["improvement_score"] > smoke["baseline_score"]
    assert smoke["milestone_status"] == "on_track"
    assert (package_root / "topic_boundary.md").exists()
    assert (package_root / "risk_casebook.md").exists()
    assert (output_dir / "results" / "project_summary.json").exists()
