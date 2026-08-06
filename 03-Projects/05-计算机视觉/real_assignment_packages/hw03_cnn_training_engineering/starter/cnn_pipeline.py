from __future__ import annotations

import csv
import math
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _image(row: dict[str, str]) -> list[float]:
    return [float(row[f"p{i}"]) for i in range(16)]


def _extract_features(image: list[float]) -> list[float]:
    grid = [image[i * 4 : (i + 1) * 4] for i in range(4)]
    left = sum(grid[r][0] + grid[r][1] for r in range(4))
    right = sum(grid[r][2] + grid[r][3] for r in range(4))
    top = sum(grid[0]) + sum(grid[1])
    bottom = sum(grid[2]) + sum(grid[3])
    mean = sum(image) / len(image)
    return [left - right, top - bottom, mean]


def _dataset(path: Path) -> list[tuple[list[float], int]]:
    rows = _read_rows(path)
    return [(_extract_features(_image(row)), int(row["label"])) for row in rows]


def _softmax(logits: list[float]) -> list[float]:
    shift = max(logits)
    exps = [math.exp(v - shift) for v in logits]
    total = sum(exps)
    return [v / total for v in exps]


def _evaluate(weights: list[list[float]], bias: list[float], dataset: list[tuple[list[float], int]]) -> tuple[float, dict[str, int]]:
    correct = 0
    confusion: dict[str, int] = {}
    for features, label in dataset:
        logits = [sum(features[i] * weights[i][k] for i in range(3)) + bias[k] for k in range(2)]
        pred = max(range(2), key=lambda idx: logits[idx])
        if pred == label:
            correct += 1
        confusion[f"{label}->{pred}"] = confusion.get(f"{label}->{pred}", 0) + 1
    return correct / len(dataset), confusion


def run_smoke(train_csv: Path, val_csv: Path) -> dict[str, object]:
    train_set = _dataset(train_csv)
    val_set = _dataset(val_csv)
    weights = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
    bias = [0.0, 0.0]
    epoch_losses = []

    for _ in range(15):
        total_loss = 0.0
        for features, label in train_set:
            logits = [sum(features[i] * weights[i][k] for i in range(3)) + bias[k] for k in range(2)]
            probs = _softmax(logits)
            total_loss += -math.log(max(probs[label], 1e-12))
            dlogits = probs[:]
            dlogits[label] -= 1.0
            for i in range(3):
                for k in range(2):
                    weights[i][k] -= 0.05 * features[i] * dlogits[k]
            for k in range(2):
                bias[k] -= 0.05 * dlogits[k]
        epoch_losses.append(round(total_loss / len(train_set), 6))

    train_accuracy, _ = _evaluate(weights, bias, train_set)
    val_accuracy, confusion = _evaluate(weights, bias, val_set)
    return {
        "train_size": len(train_set),
        "val_size": len(val_set),
        "epoch_losses_head": epoch_losses[:5],
        "final_train_loss": epoch_losses[-1],
        "train_accuracy": round(train_accuracy, 4),
        "val_accuracy": round(val_accuracy, 4),
        "confusion_matrix": confusion,
    }
