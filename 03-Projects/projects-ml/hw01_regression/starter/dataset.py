from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

import numpy as np


def load_regression_csv(path: str | Path, has_target: bool = True) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    path = Path(path)
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"CSV is empty: {path}") from exc
        rows = [row for row in reader if row]

    if not rows:
        raise ValueError(f"CSV contains no data rows: {path}")

    if header[0] != "id":
        raise ValueError(f"Expected first column to be 'id', got {header[0]!r}")

    ids = np.array([int(float(row[0])) for row in rows], dtype=np.int64)

    if has_target:
        features = np.array([[float(value) for value in row[1:-1]] for row in rows], dtype=np.float64)
        targets = np.array([float(row[-1]) for row in rows], dtype=np.float64)
    else:
        features = np.array([[float(value) for value in row[1:]] for row in rows], dtype=np.float64)
        targets = None

    return ids, features, targets


def train_valid_split(
    x: np.ndarray,
    y: np.ndarray,
    valid_ratio: float = 0.25,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if not 0.0 < valid_ratio < 1.0:
        raise ValueError("valid_ratio must be between 0 and 1")

    rng = np.random.default_rng(seed)
    indices = np.arange(len(x))
    rng.shuffle(indices)

    valid_size = max(1, int(len(x) * valid_ratio))
    valid_idx = indices[:valid_size]
    train_idx = indices[valid_size:]

    return x[train_idx], y[train_idx], x[valid_idx], y[valid_idx]


def compute_standardizer(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    std[std == 0.0] = 1.0
    return mean, std


def apply_standardizer(x: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return (x - mean) / std


def save_predictions(ids: Iterable[int], preds: Iterable[float], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "tested_positive"])
        for sample_id, pred in zip(ids, preds):
            writer.writerow([int(sample_id), float(pred)])
