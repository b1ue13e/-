from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy.stats import poisson


def build_queue_summary(lob_events_csv: Path) -> dict[str, object]:
    events = pd.read_csv(lob_events_csv)
    required = {
        "timestamp",
        "event_type",
        "units",
        "initial_ahead",
        "own_order_units",
        "horizon_seconds",
    }
    if not required <= set(events.columns) or events.empty:
        raise ValueError(f"queue events require columns: {sorted(required)}")

    initial_ahead = int(events.iloc[0]["initial_ahead"])
    own_order_units = int(events.iloc[0]["own_order_units"])
    horizon_seconds = float(events.iloc[0]["horizon_seconds"])
    if initial_ahead < 0 or own_order_units <= 0 or horizon_seconds <= 0 or (events["units"] < 0).any():
        raise ValueError("initial_ahead must be non-negative; own size and horizon must be positive")
    for column in ("initial_ahead", "own_order_units", "horizon_seconds"):
        if events[column].nunique() != 1:
            raise ValueError(f"{column} must be constant within one event replay")
    timestamps = pd.to_numeric(events["timestamp"], errors="raise")
    if float(timestamps.iloc[0]) != 0.0:
        raise ValueError("the first event timestamp must be t=0")
    if timestamps.tolist() != sorted(timestamps.tolist()):
        raise ValueError("queue events must be sorted")

    queue_ahead = initial_ahead
    own_remaining = own_order_units
    path = [queue_ahead]
    own_order_path = [own_remaining]
    depletion_units = 0
    reached_front_index: int | None = -1 if initial_ahead == 0 else None
    fill_index: int | None = None
    for index, event in events.iterrows():
        units = int(event["units"])
        if event["event_type"] == "trade":
            consumed_ahead = min(queue_ahead, units)
            queue_ahead -= consumed_ahead
            consumed_own = min(own_remaining, units - consumed_ahead)
            own_remaining -= consumed_own
            depletion_units += consumed_ahead + consumed_own
        elif event["event_type"] == "cancel_ahead":
            consumed_ahead = min(queue_ahead, units)
            queue_ahead -= consumed_ahead
            depletion_units += consumed_ahead
        elif event["event_type"] == "add_ahead":
            queue_ahead += units
        elif event["event_type"] == "cancel_behind":
            pass
        else:
            raise ValueError(f"unsupported queue event: {event['event_type']}")
        path.append(queue_ahead)
        own_order_path.append(own_remaining)
        if queue_ahead == 0 and reached_front_index is None:
            reached_front_index = int(index)
        if own_remaining == 0 and fill_index is None:
            fill_index = int(index)

    observed_seconds = float(timestamps.iloc[-1] - timestamps.iloc[0])
    if observed_seconds <= 0:
        raise ValueError("event timestamps must span a positive observation window")
    depletion_rate = depletion_units / observed_seconds
    reach_front_probability = float(poisson.sf(initial_ahead - 1, depletion_rate * horizon_seconds))
    fill_probability = float(
        poisson.sf(initial_ahead + own_order_units - 1, depletion_rate * horizon_seconds)
    )
    return {
        "method": "poisson_unit_depletion_fill_approximation",
        "initial_ahead": initial_ahead,
        "final_ahead": queue_ahead,
        "queue_path": path,
        "own_order_units": own_order_units,
        "own_order_path": own_order_path,
        "depletion_units": depletion_units,
        "depletion_rate": round(depletion_rate, 8),
        "observed_duration_seconds": observed_seconds,
        "horizon_seconds": horizon_seconds,
        "reach_front_probability": round(reach_front_probability, 8),
        "fill_probability": round(fill_probability, 8),
        "observed_reached_front": reached_front_index is not None,
        "reached_front_event_index": reached_front_index,
        "observed_filled": fill_index is not None,
        "fill_event_index": fill_index,
        "probability_model_ignores_add_ahead": True,
    }
