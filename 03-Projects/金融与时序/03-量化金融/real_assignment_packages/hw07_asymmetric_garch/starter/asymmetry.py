from __future__ import annotations

import csv
import math
from pathlib import Path


def build_asymmetry_summary(returns_csv: Path) -> dict[str, object]:
    with returns_csv.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    returns = [float(row["value"]) for row in rows]
    negatives = [x for x in returns if x < 0]
    positives = [x for x in returns if x >= 0]
    negative_vol = math.sqrt(sum(x * x for x in negatives) / len(negatives)) if negatives else 0.0
    positive_vol = math.sqrt(sum(x * x for x in positives) / len(positives)) if positives else 0.0
    return {
        "observations": len(returns),
        "negative_count": len(negatives),
        "positive_count": len(positives),
        "negative_volatility_proxy": round(negative_vol, 6),
        "positive_volatility_proxy": round(positive_vol, 6),
        "leverage_gap_proxy": round(negative_vol - positive_vol, 6),
    }
