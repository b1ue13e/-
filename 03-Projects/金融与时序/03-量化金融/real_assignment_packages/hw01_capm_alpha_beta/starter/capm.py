from __future__ import annotations

import csv
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _price_to_returns(rows: list[dict[str, str]]) -> dict[str, float]:
    returns: dict[str, float] = {}
    prev_close: float | None = None
    for row in rows:
        close = float(row["close"])
        if prev_close is not None and prev_close != 0:
            returns[row["date"]] = close / prev_close - 1.0
        prev_close = close
    return returns


def _benchmark_returns(rows: list[dict[str, str]]) -> dict[str, float]:
    if rows and "return" in rows[0]:
        return {row["date"]: float(row["return"]) for row in rows}
    return _price_to_returns(rows)


def _risk_free(rows: list[dict[str, str]]) -> dict[str, float]:
    return {row["date"]: float(row["rf"]) for row in rows}


def estimate_capm(prices_csv: Path, benchmark_csv: Path, risk_free_csv: Path) -> dict[str, object]:
    asset_rows = _read_rows(prices_csv)
    benchmark_rows = _read_rows(benchmark_csv)
    rf_rows = _read_rows(risk_free_csv)

    asset_returns = _price_to_returns(asset_rows)
    benchmark_returns = _benchmark_returns(benchmark_rows)
    risk_free = _risk_free(rf_rows)

    aligned_dates = sorted(set(asset_returns) & set(benchmark_returns) & set(risk_free))
    if len(aligned_dates) < 2:
        raise ValueError("At least two aligned return observations are required.")

    asset_excess = [asset_returns[d] - risk_free[d] for d in aligned_dates]
    benchmark_excess = [benchmark_returns[d] - risk_free[d] for d in aligned_dates]

    mean_asset = sum(asset_excess) / len(asset_excess)
    mean_benchmark = sum(benchmark_excess) / len(benchmark_excess)
    covariance = sum((a - mean_asset) * (b - mean_benchmark) for a, b in zip(asset_excess, benchmark_excess))
    variance = sum((b - mean_benchmark) ** 2 for b in benchmark_excess)
    beta = covariance / variance if variance else 0.0
    alpha = mean_asset - beta * mean_benchmark

    rolling = []
    for i in range(1, len(aligned_dates)):
        prev = aligned_dates[i - 1]
        curr = aligned_dates[i]
        delta_asset = asset_excess[i] - asset_excess[i - 1]
        delta_bench = benchmark_excess[i] - benchmark_excess[i - 1]
        rolling.append(
            {
                "window_end": curr,
                "asset_excess_change": round(delta_asset, 6),
                "benchmark_excess_change": round(delta_bench, 6),
                "beta_proxy": round(asset_excess[i] / benchmark_excess[i], 6) if benchmark_excess[i] else 0.0,
                "reference_start": prev,
            }
        )

    return {
        "ticker": asset_rows[0]["ticker"] if asset_rows else "UNKNOWN",
        "observations": len(aligned_dates),
        "alpha": round(alpha, 6),
        "beta": round(beta, 6),
        "mean_asset_excess": round(mean_asset, 6),
        "mean_benchmark_excess": round(mean_benchmark, 6),
        "aligned_dates": aligned_dates,
        "rolling_beta_proxy": rolling,
    }
