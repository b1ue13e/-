from __future__ import annotations

import csv
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_hedging_summary(underlying_csv: Path, option_csv: Path, risk_free_csv: Path) -> dict[str, object]:
    underlying_rows = _read_rows(underlying_csv)
    option_rows = _read_rows(option_csv)
    rf_rows = _read_rows(risk_free_csv)

    closes = [float(row["close"]) for row in underlying_rows]
    call_prices = [float(row["call_price"]) for row in option_rows]
    put_prices = [float(row["put_price"]) for row in option_rows]
    risk_free = [float(row["rf"]) for row in rf_rows]

    delta_path = []
    for i in range(1, min(len(closes), len(call_prices))):
        underlying_change = closes[i] - closes[i - 1]
        call_change = call_prices[i] - call_prices[i - 1]
        delta_path.append(round(call_change / underlying_change, 6) if underlying_change else 0.0)

    hedge_cost_proxy = round(sum(abs(c - p) for c, p in zip(call_prices, put_prices)) / len(call_prices), 6)
    funding_rate_proxy = round(sum(risk_free) / len(risk_free), 6)
    return {
        "observations": len(option_rows),
        "delta_proxy_path": delta_path,
        "hedge_cost_proxy": hedge_cost_proxy,
        "funding_rate_proxy": funding_rate_proxy,
        "final_underlying_close": round(closes[-1], 6),
    }
