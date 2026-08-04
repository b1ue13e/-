from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_train_starter_and_infer_template(tmp_path: Path) -> None:
    package_root = Path(__file__).resolve().parents[1]
    project_root = package_root.parents[1]
    data_dir = project_root / "data" / "ml_hw01"
    output_dir = tmp_path / "outputs"

    train_cmd = [
        sys.executable,
        str(package_root / "starter" / "train.py"),
        "--train-csv",
        str(data_dir / "covid.train.smoke.csv"),
        "--output-dir",
        str(output_dir),
        "--seed",
        "42",
    ]
    infer_cmd = [
        sys.executable,
        str(package_root / "starter" / "infer.py"),
        "--test-csv",
        str(data_dir / "covid.test.smoke.csv"),
        "--checkpoint",
        str(output_dir / "checkpoint.npz"),
        "--output",
        str(output_dir / "pred.csv"),
    ]

    subprocess.run(train_cmd, check=True)
    subprocess.run(infer_cmd, check=True)

    pred_lines = (output_dir / "pred.csv").read_text(encoding="utf-8").strip().splitlines()
    assert pred_lines[0] == "id,tested_positive"
    assert len(pred_lines) == 5
