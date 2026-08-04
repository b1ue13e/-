from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


LABELS = ("cat", "dog", "plane")


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _predicted_label(row: dict[str, str], prefix: str) -> str:
    scores = {label: float(row[f"{prefix}_{label}"]) for label in LABELS}
    return max(scores, key=scores.get)


def evaluate(train_csv: Path, val_csv: Path) -> dict[str, object]:
    train_rows = _read_rows(train_csv)
    val_rows = _read_rows(val_csv)
    frozen_correct = 0
    finetune_correct = 0
    per_class: dict[str, dict[str, float]] = {}
    failure_examples: list[dict[str, object]] = []

    for row in val_rows:
        actual = row["label"]
        frozen_pred = _predicted_label(row, "frozen")
        finetune_pred = _predicted_label(row, "finetune")

        stats = per_class.setdefault(actual, {"count": 0, "frozen_correct": 0, "finetune_correct": 0})
        stats["count"] += 1
        if frozen_pred == actual:
            frozen_correct += 1
            stats["frozen_correct"] += 1
        if finetune_pred == actual:
            finetune_correct += 1
            stats["finetune_correct"] += 1
        if frozen_pred != actual or finetune_pred != actual:
            failure_examples.append(
                {
                    "sample_id": row["id"],
                    "label": actual,
                    "frozen_pred": frozen_pred,
                    "finetune_pred": finetune_pred,
                }
            )

    per_class_delta: dict[str, float] = {}
    promoted_classes: list[str] = []
    stagnant_classes: list[str] = []
    for label, stats in per_class.items():
        frozen_acc = stats["frozen_correct"] / stats["count"]
        finetune_acc = stats["finetune_correct"] / stats["count"]
        delta = round(finetune_acc - frozen_acc, 4)
        per_class_delta[label] = delta
        if delta > 0:
            promoted_classes.append(label)
        else:
            stagnant_classes.append(label)

    label_counts = Counter(row["label"] for row in train_rows)
    return {
        "train_size": len(train_rows),
        "val_size": len(val_rows),
        "label_counts": dict(label_counts),
        "frozen_accuracy": round(frozen_correct / len(val_rows), 4),
        "finetune_accuracy": round(finetune_correct / len(val_rows), 4),
        "per_class_delta": per_class_delta,
        "promoted_classes": promoted_classes,
        "stagnant_classes": stagnant_classes,
        "cost_ratio": 1.8,
        "failure_examples": failure_examples[:4],
    }
