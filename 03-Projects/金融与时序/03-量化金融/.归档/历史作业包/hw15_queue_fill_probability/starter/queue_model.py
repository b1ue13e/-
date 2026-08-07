from __future__ import annotations

import csv
from pathlib import Path


def build_queue_summary(lob_events_csv: Path) -> dict[str, object]:
    with lob_events_csv.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    bid_events = [row for row in rows if row["side"] == "B"]
    ask_events = [row for row in rows if row["side"] == "S"]
    total_size = sum(float(row["size"]) for row in rows)
    fill_probability_proxy = round(sum(float(row["size"]) for row in bid_events) / total_size, 6) if total_size else 0.0
    queue_depth_proxy = round(total_size / len(rows), 6) if rows else 0.0
    return {
        "event_count": len(rows),
        "bid_event_count": len(bid_events),
        "ask_event_count": len(ask_events),
        "queue_depth_proxy": queue_depth_proxy,
        "fill_probability_proxy": fill_probability_proxy,
    }
