from __future__ import annotations

import csv
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_execution_summary(parent_order_csv: Path, liquidity_csv: Path) -> dict[str, object]:
    orders = _read_rows(parent_order_csv)
    liquidity_rows = _read_rows(liquidity_csv)

    qty_list = [float(row["qty"]) for row in orders]
    liquidity_curve = [float(row["value"]) for row in liquidity_rows]
    total_qty = sum(qty_list)
    twap_schedule = [round(qty / len(liquidity_curve), 6) for qty in qty_list]
    risk_adjusted_schedule = [round(qty * liquidity_curve[0], 6) for qty in qty_list]

    return {
        "order_count": len(orders),
        "total_qty": round(total_qty, 6),
        "twap_schedule_proxy": twap_schedule,
        "risk_averse_schedule_proxy": risk_adjusted_schedule,
        "avg_liquidity_bucket": round(sum(liquidity_curve) / len(liquidity_curve), 6),
    }
