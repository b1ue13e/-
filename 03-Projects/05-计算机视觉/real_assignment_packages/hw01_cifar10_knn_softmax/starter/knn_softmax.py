from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _vector(row: dict[str, str]) -> list[float]:
    return [float(row["f1"]), float(row["f2"]), float(row["f3"])]


def _distance(a: list[float], b: list[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def _score_linear(vec: list[float]) -> str:
    scores = {
        "cat": 1.2 * vec[0] + 0.4 * vec[1] - 0.2 * vec[2],
        "dog": 0.3 * vec[0] + 1.1 * vec[1] + 0.2 * vec[2],
        "car": -0.2 * vec[0] + 0.2 * vec[1] + 1.3 * vec[2],
    }
    return max(scores, key=scores.get)


def evaluate(train_csv: Path, val_csv: Path) -> dict[str, object]:
    train_rows = _read_rows(train_csv)
    val_rows = _read_rows(val_csv)
    knn_correct = 0
    linear_correct = 0
    failures: list[dict[str, str]] = []

    for row in val_rows:
        vec = _vector(row)
        nearest = min(train_rows, key=lambda item: _distance(vec, _vector(item)))
        knn_pred = nearest["label"]
        linear_pred = _score_linear(vec)
        actual = row["label"]
        if knn_pred == actual:
            knn_correct += 1
        if linear_pred == actual:
            linear_correct += 1
        if knn_pred != actual or linear_pred != actual:
            failures.append(
                {
                    "sample_id": row["id"],
                    "label": actual,
                    "knn_pred": knn_pred,
                    "softmax_pred": linear_pred,
                }
            )

    label_counts = Counter(row["label"] for row in train_rows)
    return {
        "train_size": len(train_rows),
        "val_size": len(val_rows),
        "label_counts": dict(label_counts),
        "knn_accuracy": round(knn_correct / len(val_rows), 4),
        "softmax_accuracy": round(linear_correct / len(val_rows), 4),
        "failure_examples": failures[:3],
    }
