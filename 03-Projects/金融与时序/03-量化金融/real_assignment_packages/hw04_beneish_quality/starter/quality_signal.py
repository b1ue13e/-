from __future__ import annotations

import csv
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_quality_summary(financial_csv: Path, filing_calendar_csv: Path) -> dict[str, object]:
    financial_rows = _read_rows(financial_csv)
    filing_rows = _read_rows(filing_calendar_csv)
    filing_map = {row["ticker"]: row["filing_date"] for row in filing_rows}

    signals = []
    for row in financial_rows:
        revenue = float(row["revenue"])
        cash_flow = float(row["cash_flow"])
        assets = float(row["assets"])
        accrual_ratio = round((revenue - cash_flow) / assets, 6) if assets else 0.0
        signals.append(
            {
                "ticker": row["ticker"],
                "report_date": row["report_date"],
                "filing_date": filing_map.get(row["ticker"], ""),
                "accrual_ratio": accrual_ratio,
                "quality_flag": "watch" if accrual_ratio > 0.15 else "ok",
            }
        )

    watch_count = sum(1 for row in signals if row["quality_flag"] == "watch")
    return {
        "company_count": len(signals),
        "watch_count": watch_count,
        "quality_signals": signals,
    }
