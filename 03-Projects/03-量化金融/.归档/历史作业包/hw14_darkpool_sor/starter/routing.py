from __future__ import annotations

import csv
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_routing_summary(venue_quotes_csv: Path, latency_csv: Path) -> dict[str, object]:
    venue_rows = _read_rows(venue_quotes_csv)
    latency_rows = _read_rows(latency_csv)

    latency_penalty = sum(float(row["value"]) for row in latency_rows) / len(latency_rows)
    route_candidates = []
    for row in venue_rows:
        adjusted_ask = float(row["ask"]) + latency_penalty
        route_candidates.append({"venue": row["venue"], "adjusted_ask": round(adjusted_ask, 6)})

    best_route = min(route_candidates, key=lambda item: item["adjusted_ask"])
    return {
        "venue_count": len(route_candidates),
        "latency_penalty": round(latency_penalty, 6),
        "best_route": best_route,
        "route_candidates": route_candidates,
    }
