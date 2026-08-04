from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

import numpy as np


OFFICIAL_INPUT_DIM = 429
OFFICIAL_NUM_CLASSES = 39
TRAIN_FEATURES = "train_11.npy"
TRAIN_LABELS = "train_label_11.npy"
TEST_FEATURES = "test_11.npy"


def _load_array(path: Path, *, mmap: bool = False) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(f"Missing required data file: {path}")
    array = np.load(path, mmap_mode="r" if mmap else None, allow_pickle=False)
    if not np.issubdtype(array.dtype, np.number):
        raise ValueError(f"Expected a numeric NumPy array: {path}")
    return array


def load_training_arrays(
    data_dir: str | Path,
    *,
    mmap: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    data_dir = Path(data_dir)
    x = _load_array(data_dir / TRAIN_FEATURES, mmap=mmap)
    y = _load_array(data_dir / TRAIN_LABELS, mmap=mmap)

    if x.ndim != 2:
        raise ValueError(f"Training features must be 2-D, got shape={x.shape}")
    if y.ndim != 1:
        raise ValueError(f"Training labels must be 1-D, got shape={y.shape}")
    if len(x) != len(y):
        raise ValueError(f"Feature/label row mismatch: {len(x)} != {len(y)}")
    if len(x) < 2:
        raise ValueError("At least two training rows are required")
    if not np.isfinite(x).all():
        raise ValueError("Training features contain NaN or infinite values")
    if not np.isfinite(y).all():
        raise ValueError("Training labels contain NaN or infinite values")
    if not np.all(y == np.floor(y)):
        raise ValueError("Training labels must be integers")

    return np.asarray(x, dtype=np.float32), np.asarray(y, dtype=np.int64)


def load_test_array(data_dir: str | Path, *, mmap: bool = False) -> np.ndarray:
    data_dir = Path(data_dir)
    x = _load_array(data_dir / TEST_FEATURES, mmap=mmap)
    if x.ndim != 2:
        raise ValueError(f"Test features must be 2-D, got shape={x.shape}")
    if len(x) == 0:
        raise ValueError("Test features contain no rows")
    if not np.isfinite(x).all():
        raise ValueError("Test features contain NaN or infinite values")
    return np.asarray(x, dtype=np.float32)


def validate_official_contract(
    x: np.ndarray,
    y: np.ndarray | None = None,
    *,
    input_dim: int = OFFICIAL_INPUT_DIM,
    num_classes: int = OFFICIAL_NUM_CLASSES,
) -> None:
    if x.ndim != 2 or x.shape[1] != input_dim:
        raise ValueError(
            f"Expected feature shape (n, {input_dim}), got {tuple(x.shape)}"
        )
    if y is None:
        return
    if y.ndim != 1 or len(y) != len(x):
        raise ValueError("Labels must be one-dimensional and aligned with features")
    if int(y.min()) < 0 or int(y.max()) >= num_classes:
        raise ValueError(
            f"Labels must be in [0, {num_classes - 1}], got [{int(y.min())}, {int(y.max())}]"
        )


def stratified_train_valid_split(
    y: np.ndarray,
    *,
    valid_ratio: float = 0.1,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    if not 0.0 < valid_ratio < 1.0:
        raise ValueError("valid_ratio must be between 0 and 1")
    if y.ndim != 1 or len(y) < 2:
        raise ValueError("y must be a one-dimensional array with at least two rows")

    rng = np.random.default_rng(seed)
    train_parts: list[np.ndarray] = []
    valid_parts: list[np.ndarray] = []

    for label in np.unique(y):
        indices = np.flatnonzero(y == label)
        rng.shuffle(indices)
        if len(indices) == 1:
            train_parts.append(indices)
            continue
        valid_size = min(len(indices) - 1, max(1, int(round(len(indices) * valid_ratio))))
        valid_parts.append(indices[:valid_size])
        train_parts.append(indices[valid_size:])

    train_idx = np.concatenate(train_parts)
    valid_idx = np.concatenate(valid_parts) if valid_parts else np.array([], dtype=np.int64)
    if len(valid_idx) == 0:
        raise ValueError("A validation split could not be formed; add at least two rows to one class")
    rng.shuffle(train_idx)
    rng.shuffle(valid_idx)
    return train_idx.astype(np.int64), valid_idx.astype(np.int64)


def compute_standardizer(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = np.asarray(x.mean(axis=0), dtype=np.float32)
    std = np.asarray(x.std(axis=0), dtype=np.float32)
    std[std < 1e-8] = 1.0
    return mean, std


def apply_standardizer(x: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    if x.shape[1] != len(mean) or len(mean) != len(std):
        raise ValueError("Feature dimension does not match the saved standardizer")
    return np.asarray((x - mean) / std, dtype=np.float32)


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int) -> np.ndarray:
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    matrix = np.zeros((num_classes, num_classes), dtype=np.int64)
    np.add.at(matrix, (y_true.astype(np.int64), y_pred.astype(np.int64)), 1)
    return matrix


def macro_f1_from_confusion(matrix: np.ndarray) -> float:
    scores: list[float] = []
    for label in range(matrix.shape[0]):
        tp = float(matrix[label, label])
        fp = float(matrix[:, label].sum() - tp)
        fn = float(matrix[label, :].sum() - tp)
        denominator = 2.0 * tp + fp + fn
        scores.append(0.0 if denominator == 0.0 else (2.0 * tp) / denominator)
    return float(np.mean(scores))


def save_confusion_matrix(matrix: np.ndarray, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["true\\pred", *range(matrix.shape[1])])
        for label, row in enumerate(matrix):
            writer.writerow([label, *row.tolist()])


def save_submission(predictions: Iterable[int], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Id", "Class"])
        for sample_id, label in enumerate(predictions):
            writer.writerow([sample_id, int(label)])
