from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
STARTER = PACKAGE_ROOT / "starter"
sys.path.insert(0, str(STARTER))

from dataset import (  # noqa: E402
    OFFICIAL_INPUT_DIM,
    OFFICIAL_NUM_CLASSES,
    stratified_train_valid_split,
    validate_official_contract,
)
from make_smoke_data import build_smoke_arrays  # noqa: E402
from model import MLPClassifier  # noqa: E402


def test_smoke_data_matches_official_contract() -> None:
    train, labels, test = build_smoke_arrays()
    validate_official_contract(train, labels)
    validate_official_contract(test)
    assert train.shape[1] == OFFICIAL_INPUT_DIM
    assert set(labels.tolist()) == set(range(OFFICIAL_NUM_CLASSES))

    train_idx, valid_idx = stratified_train_valid_split(labels, valid_ratio=0.25, seed=42)
    assert set(train_idx).isdisjoint(set(valid_idx))
    assert len(train_idx) + len(valid_idx) == len(labels)
    assert set(labels[train_idx]) == set(labels[valid_idx]) == set(range(OFFICIAL_NUM_CLASSES))


def test_model_output_shape() -> None:
    model = MLPClassifier(OFFICIAL_INPUT_DIM, OFFICIAL_NUM_CLASSES, hidden_dims=(32,), dropout=0.0)
    logits = model(torch.zeros(5, OFFICIAL_INPUT_DIM))
    assert logits.shape == (5, OFFICIAL_NUM_CLASSES)


def test_training_and_inference_roundtrip(tmp_path: Path) -> None:
    data_dir = tmp_path / "timit_11_smoke"
    output_dir = tmp_path / "outputs"
    submission = output_dir / "prediction.csv"

    subprocess.run(
        [
            sys.executable,
            str(STARTER / "make_smoke_data.py"),
            "--output-dir",
            str(data_dir),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(STARTER / "train.py"),
            "--data-dir",
            str(data_dir),
            "--output-dir",
            str(output_dir),
            "--epochs",
            "1",
            "--batch-size",
            "64",
            "--hidden-dims",
            "32",
            "--dropout",
            "0",
            "--device",
            "cpu",
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(STARTER / "infer.py"),
            "--data-dir",
            str(data_dir),
            "--checkpoint",
            str(output_dir / "checkpoint.pt"),
            "--output",
            str(submission),
            "--device",
            "cpu",
        ],
        check=True,
    )

    assert (output_dir / "checkpoint.pt").exists()
    assert (output_dir / "confusion_matrix.csv").exists()
    metrics = json.loads((output_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["input_dim"] == OFFICIAL_INPUT_DIM
    assert metrics["num_classes"] == OFFICIAL_NUM_CLASSES
    assert len(metrics["history"]) == 1

    with submission.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    assert rows[0] == ["Id", "Class"]
    assert len(rows) == 1 + len(build_smoke_arrays()[2])
    assert [int(row[0]) for row in rows[1:]] == list(range(len(rows) - 1))
    assert all(0 <= int(row[1]) < OFFICIAL_NUM_CLASSES for row in rows[1:])
