from __future__ import annotations

import csv
import json
import math
from datetime import date, timedelta
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "smoke"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ohlcv_rows = []
    previous_close = 100.0
    for index in range(90):
        current_date = date(2024, 1, 2) + timedelta(days=index)
        close = 100.0 + 0.09 * index + 1.8 * math.sin(index * 0.19)
        open_price = previous_close * (1.0 + 0.001 * math.sin(index * 0.31))
        high = max(open_price, close) + 0.35
        low = min(open_price, close) - 0.35
        ohlcv_rows.append(
            {
                "date": current_date.isoformat(),
                "open": round(open_price, 6),
                "high": round(high, 6),
                "low": round(low, 6),
                "close": round(close, 6),
                "volume": 100000 + (index % 11) * 7000,
                "adjustment_factor": 1.0,
            }
        )
        previous_close = close
    write_csv(
        DATA / "data_protocol_baseline" / "ohlcv.csv",
        ["date", "open", "high", "low", "close", "volume", "adjustment_factor"],
        ohlcv_rows,
    )

    returns = []
    for index in range(60):
        current_date = date(2024, 1, 2) + timedelta(days=index)
        base = 0.006 * math.sin(index * 0.71) + 0.002 * math.cos(index * 0.19)
        shock = -0.025 - 0.002 * (index % 5) if index % 7 == 0 else 0.0
        returns.append({"date": current_date.isoformat(), "asset": "A", "value": round(base + shock, 8)})
    write_csv(DATA / "evt_tail_risk" / "returns.csv", ["date", "asset", "value"], returns)

    ticks = [
        {
            "timestamp": f"2024-01-02 09:30:{index:02d}",
            "price": round(100 + 0.03 * index + 0.04 * math.sin(index), 4),
            "size": 5 + (index * 3) % 11,
            "side": "B" if index % 2 == 0 else "S",
        }
        for index in range(18)
    ]
    write_csv(DATA / "volume_dollar_bars" / "ticks.csv", ["timestamp", "price", "size", "side"], ticks)

    asset_rows = []
    for day in range(24):
        market = 0.004 * math.sin(day * 0.43)
        for asset_index, asset in enumerate(("A", "B", "C", "D")):
            value = market * (0.7 + asset_index * 0.15) + 0.003 * math.cos(day * (0.31 + asset_index * 0.07) + asset_index)
            asset_rows.append({"date": f"2024-02-{day + 1:02d}", "asset": asset, "value": round(value, 8)})
    for directory in ("hrp_allocation", "covariance_denoising"):
        write_csv(DATA / directory / "asset_returns.csv", ["date", "asset", "value"], asset_rows)

    strategy_rows = []
    parameters = []
    for strategy_index, strategy in enumerate(("S1", "S2", "S3", "S4")):
        parameters.append({"strategy": strategy, "lookback": 5 + strategy_index * 5})
    for day in range(24):
        regime = 1.0 if day < 12 else -0.7
        for strategy_index, strategy in enumerate(("S1", "S2", "S3", "S4")):
            value = 0.002 * math.sin(day * (0.35 + strategy_index * 0.04)) + regime * 0.0007 * (strategy_index - 1.5)
            strategy_rows.append({"date": f"2024-03-{day + 1:02d}", "strategy": strategy, "value": round(value, 8)})
    write_csv(DATA / "cpcv_pbo" / "strategy_returns.csv", ["date", "strategy", "value"], strategy_rows)
    write_csv(DATA / "cpcv_pbo" / "parameter_grid.csv", ["strategy", "lookback"], parameters)

    write_csv(
        DATA / "almgren_chriss" / "parent_order.csv",
        ["order_id", "qty", "side", "intervals", "total_time", "risk_aversion", "volatility", "temporary_impact"],
        [{"order_id": "Q1", "qty": 120000, "side": "SELL", "intervals": 6, "total_time": 1.0, "risk_aversion": 0.2, "volatility": 0.025, "temporary_impact": 0.01}],
    )
    write_csv(
        DATA / "almgren_chriss" / "liquidity_profile.csv",
        ["bucket", "volume_share"],
        [{"bucket": index + 1, "volume_share": share} for index, share in enumerate((0.12, 0.16, 0.20, 0.21, 0.18, 0.13))],
    )

    queue_events = [
        {
            "timestamp": index,
            "event_type": event_type,
            "units": units,
            "initial_ahead": 20,
            "own_order_units": 2,
            "horizon_seconds": 10,
        }
        for index, (event_type, units) in enumerate(
            (
                ("trade", 3),
                ("cancel_ahead", 2),
                ("add_ahead", 1),
                ("trade", 4),
                ("cancel_ahead", 3),
                ("trade", 5),
                ("trade", 4),
                ("cancel_behind", 7),
                ("trade", 2),
            )
        )
    ]
    write_csv(
        DATA / "queue_fill_probability" / "lob_events.csv",
        ["timestamp", "event_type", "units", "initial_ahead", "own_order_units", "horizon_seconds"],
        queue_events,
    )

    qlib_dir = DATA / "qlib_factor_research"
    qlib_dir.mkdir(parents=True, exist_ok=True)
    (qlib_dir / "qlib_manifest.json").write_text(
        json.dumps(
            {
                "qlib_version": "0.9.7",
                "qlib_source_commit": None,
                "data_release": "synthetic-contract-template-v2",
                "data_license": "CC0 synthetic fixture",
                "provider_uri": "replace-before-qrun",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    workflow = {
        "qlib_init": {"provider_uri": "replace-before-qrun", "region": "cn"},
        "task": {
            "model": {"class": "LGBModel", "module_path": "qlib.contrib.model.gbdt", "kwargs": {"loss": "mse"}},
            "dataset": {
                "class": "DatasetH",
                "module_path": "qlib.data.dataset",
                "kwargs": {
                    "handler": {
                        "class": "Alpha158",
                        "module_path": "qlib.contrib.data.handler",
                        "kwargs": {
                            "start_time": "2018-01-01",
                            "end_time": "2022-12-31",
                            "fit_start_time": "2018-01-01",
                            "fit_end_time": "2020-12-31",
                            "instruments": "csi300",
                        },
                    },
                    "segments": {"train": ["2018-01-01", "2020-12-31"], "valid": ["2021-01-01", "2021-12-31"], "test": ["2022-01-01", "2022-12-31"]},
                },
            },
            "record": [
                {
                    "class": "SignalRecord",
                    "module_path": "qlib.workflow.record_temp",
                    "kwargs": {"model": "<MODEL>", "dataset": "<DATASET>"},
                },
                {
                    "class": "PortAnaRecord",
                    "module_path": "qlib.workflow.record_temp",
                    "kwargs": {
                        "config": {
                            "strategy": {
                                "class": "TopkDropoutStrategy",
                                "module_path": "qlib.contrib.strategy.signal_strategy",
                                "kwargs": {"signal": "<PRED>", "topk": 50, "n_drop": 5},
                            },
                            "backtest": {
                                "start_time": "2022-01-01",
                                "end_time": "2022-12-31",
                                "account": 100000000,
                                "benchmark": "SH000300",
                                "exchange_kwargs": {
                                    "freq": "day",
                                    "limit_threshold": 0.095,
                                    "deal_price": "close",
                                    "open_cost": 0.0005,
                                    "close_cost": 0.0015,
                                    "min_cost": 5,
                                },
                            },
                        }
                    },
                },
            ],
        },
    }
    (qlib_dir / "workflow_config.yaml").write_text(yaml.safe_dump(workflow, allow_unicode=True, sort_keys=False), encoding="utf-8")
    (qlib_dir / "baseline_protocol.json").write_text(
        json.dumps({"E0": "equal_weight", "E1": "naive_momentum", "E2": "qlib_lightgbm_alpha158"}, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
