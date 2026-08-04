from __future__ import annotations

import csv
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _box(row: dict[str, str], prefix: str) -> tuple[float, float, float, float]:
    return (
        float(row[f"{prefix}_x1"]),
        float(row[f"{prefix}_y1"]),
        float(row[f"{prefix}_x2"]),
        float(row[f"{prefix}_y2"]),
    )


def _iou(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    inter_x1 = max(a[0], b[0])
    inter_y1 = max(a[1], b[1])
    inter_x2 = min(a[2], b[2])
    inter_y2 = min(a[3], b[3])
    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h
    area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = area_a + area_b - inter_area
    return inter_area / union if union else 0.0


def run_smoke(train_csv: Path, val_csv: Path) -> dict[str, object]:
    train_rows = _read_rows(train_csv)
    val_rows = _read_rows(val_csv)
    true_positive = 0
    predicted_positive = 0
    ious: list[float] = []
    failure_cases: list[dict[str, object]] = []

    for row in val_rows:
        pred_score = float(row["pred_score"])
        gt_box = _box(row, "gt")
        pred_box = _box(row, "pred")
        iou = _iou(gt_box, pred_box)
        ious.append(round(iou, 4))
        is_positive = pred_score >= 0.5
        if is_positive:
            predicted_positive += 1
        hit = row["label"] == row["pred_label"] and is_positive and iou >= 0.5
        if hit:
            true_positive += 1
        else:
            failure_cases.append(
                {
                    "image_id": row["image_id"],
                    "label": row["label"],
                    "pred_label": row["pred_label"],
                    "pred_score": pred_score,
                    "iou": round(iou, 4),
                }
            )

    train_images = len({row["image_id"] for row in train_rows})
    val_images = len({row["image_id"] for row in val_rows})
    return {
        "train_images": train_images,
        "val_images": val_images,
        "precision_at_50": round(true_positive / max(predicted_positive, 1), 4),
        "recall_at_50": round(true_positive / len(val_rows), 4),
        "mean_iou": round(sum(ious) / len(ious), 4),
        "pass_at_iou50": true_positive,
        "failure_cases": failure_cases[:4],
    }
