from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _continuous_ac_grid_schedule(
    quantity: float,
    intervals: int,
    total_time: float,
    risk_aversion: float,
    volatility: float,
    temporary_impact: float,
) -> tuple[np.ndarray, np.ndarray]:
    if min(quantity, intervals, total_time, volatility, temporary_impact) <= 0 or risk_aversion < 0:
        raise ValueError("invalid Almgren-Chriss parameters")
    times = np.linspace(0.0, total_time, intervals + 1)
    kappa = np.sqrt(risk_aversion * volatility**2 / temporary_impact)
    if kappa < 1e-12:
        inventory = quantity * (1.0 - times / total_time)
    else:
        inventory = quantity * np.sinh(kappa * (total_time - times)) / np.sinh(kappa * total_time)
    trades = inventory[:-1] - inventory[1:]
    return inventory, trades


def build_execution_summary(parent_order_csv: Path, liquidity_csv: Path) -> dict[str, object]:
    orders = pd.read_csv(parent_order_csv)
    if len(orders) != 1:
        raise ValueError("smoke contract expects exactly one parent order")
    order = orders.iloc[0]
    intervals = int(order["intervals"])
    quantity = float(order["qty"])
    total_time = float(order["total_time"])
    temporary_impact = float(order["temporary_impact"])
    inventory, optimal_schedule = _continuous_ac_grid_schedule(
        quantity=quantity,
        intervals=intervals,
        total_time=total_time,
        risk_aversion=float(order["risk_aversion"]),
        volatility=float(order["volatility"]),
        temporary_impact=temporary_impact,
    )

    liquidity = pd.read_csv(liquidity_csv)["volume_share"].to_numpy(dtype=float, copy=True)
    if liquidity.size != intervals or np.any(liquidity < 0) or liquidity.sum() <= 0:
        raise ValueError("liquidity profile must have one non-negative share per interval")
    liquidity /= liquidity.sum()
    twap_schedule = np.full(intervals, quantity / intervals)
    vwap_schedule = quantity * liquidity
    interval_time = total_time / intervals

    return {
        "method": "continuous_almgren_chriss_sampled_grid",
        "order_id": str(order["order_id"]),
        "side": str(order["side"]),
        "total_qty": quantity,
        "twap_schedule": [round(float(value), 8) for value in twap_schedule],
        "vwap_schedule": [round(float(value), 8) for value in vwap_schedule],
        "optimal_schedule": [round(float(value), 8) for value in optimal_schedule],
        "inventory_path": [round(float(value), 8) for value in inventory],
        "temporary_cost_estimate": round(float(temporary_impact * np.sum(optimal_schedule**2) / interval_time), 8),
        "inventory_conserved": bool(
            abs(optimal_schedule.sum() - quantity) < 1e-8 and abs(inventory[-1]) < 1e-8
        ),
    }
