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
    smoke = summary["cnn_summary"]
    assert summary["homework_id"] == "HW03"
    assert smoke["train_accuracy"] >= 0.5
    assert smoke["val_accuracy"] >= 0.5
    assert (output_dir / "results" / "cnn_summary.json").exists()
