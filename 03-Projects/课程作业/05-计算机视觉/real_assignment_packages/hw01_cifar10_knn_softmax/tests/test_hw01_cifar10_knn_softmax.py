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
    assert summary["homework_id"] == "HW01"
    assert summary["classification_summary"]["knn_accuracy"] >= 0.5
    assert summary["classification_summary"]["softmax_accuracy"] >= 0.5
    assert (output_dir / "results" / "classification_summary.json").exists()
