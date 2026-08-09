from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate QF-ST01 OHLCV input.")
    parser.add_argument("--input-dir", required=True)
    args = parser.parse_args()
    path = Path(args.input_dir) / "ohlcv.csv"
    frame = pd.read_csv(path)
    required = {"date", "open", "high", "low", "close", "volume", "adjustment_factor"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise SystemExit(f"missing columns: {missing}")
    if frame.empty or frame["date"].duplicated().any():
        raise SystemExit("OHLCV input is empty or has duplicate dates")


if __name__ == "__main__":
    main()
