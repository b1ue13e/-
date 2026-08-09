from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

import numpy as np
from scipy.stats import genpareto


def validate_returns_csv(returns_csv: Path) -> np.ndarray:
    with returns_csv.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    try:
        dates = [date.fromisoformat(row["date"]) for row in rows]
        returns = np.asarray([float(row["value"]) for row in rows], dtype=float)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("returns.csv requires parseable ISO dates and numeric values") from exc
    if any(current <= previous for previous, current in zip(dates, dates[1:])):
        raise ValueError("returns.csv dates must be unique and strictly increasing")
    if returns.size < 20 or not np.all(np.isfinite(returns)):
        raise ValueError("POT smoke input requires at least 20 finite returns")
    return returns


def build_tail_risk_summary(
    returns_csv: Path,
    threshold_quantile: float = 0.80,
    target_confidence: float = 0.95,
    min_exceedances: int = 8,
) -> dict[str, object]:
    returns = validate_returns_csv(returns_csv)
    if not 0 < threshold_quantile < target_confidence < 1:
        raise ValueError("require 0 < threshold_quantile < target_confidence < 1")

    losses = -returns
    threshold = float(np.quantile(losses, threshold_quantile))
    exceedances = losses[losses > threshold] - threshold
    if exceedances.size < min_exceedances:
        raise ValueError(
            f"only {exceedances.size} exceedances; require at least {min_exceedances}"
        )

    shape, _, scale = genpareto.fit(exceedances, floc=0.0)
    if not np.isfinite(shape) or not np.isfinite(scale) or scale <= 0:
        raise ValueError("GPD fit returned invalid parameters")
    if shape >= 1:
        raise ValueError("fitted GPD has infinite mean; expected shortfall is undefined")

    tail_fraction = exceedances.size / losses.size
    gpd_probability = 1.0 - (1.0 - target_confidence) / tail_fraction
    if not 0 < gpd_probability < 1:
        raise ValueError("target confidence is not beyond the fitted POT threshold")

    var = threshold + float(genpareto.ppf(gpd_probability, shape, loc=0.0, scale=scale))
    expected_shortfall = var + (scale + shape * (var - threshold)) / (1.0 - shape)
    return {
        "method": "POT-GPD",
        "observations": int(losses.size),
        "threshold_quantile": threshold_quantile,
        "threshold_loss": round(threshold, 8),
        "tail_event_count": int(exceedances.size),
        "shape": round(float(shape), 8),
        "scale": round(float(scale), 8),
        "target_confidence": target_confidence,
        "var": round(float(var), 8),
        "expected_shortfall": round(float(expected_shortfall), 8),
    }
