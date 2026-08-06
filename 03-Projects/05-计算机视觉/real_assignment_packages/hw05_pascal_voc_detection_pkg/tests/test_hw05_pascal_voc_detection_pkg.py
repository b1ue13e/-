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
    smoke = summary["detection_summary"]
    assert summary["homework_id"] == "HW05"
    assert smoke["precision_at_50"] >= 0.5
    assert smoke["recall_at_50"] >= 0.5
    assert len(smoke["failure_cases"]) >= 1
    assert (package_root / "configs" / "voc2007_tiny_subset.template.json").exists()
    assert (package_root / "artifacts" / "templates" / "eval_export_template.csv").exists()
    assert (output_dir / "results" / "detection_summary.json").exists()
