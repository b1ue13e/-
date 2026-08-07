"""Small deterministic contracts shared by the quantitative-finance labs."""

from __future__ import annotations

import hashlib
import json
import math
import random
from collections.abc import Iterable, Sequence


def split_is_disjoint(train: Sequence[int], valid: Sequence[int], test: Sequence[int]) -> bool:
    """Return whether the three index sets are pairwise disjoint."""
    sets = [set(train), set(valid), set(test)]
    return all(left.isdisjoint(right) for i, left in enumerate(sets) for right in sets[i + 1 :])


def feature_time_precedes_execution(feature_time: Sequence[int], execution_time: Sequence[int]) -> bool:
    """Return whether every feature timestamp is strictly before execution."""
    return len(feature_time) == len(execution_time) and all(
        feature < execution for feature, execution in zip(feature_time, execution_time)
    )


def net_return(gross: Iterable[float], cost: Iterable[float]) -> list[float]:
    """Calculate period net returns and reject negative costs."""
    gross_values = list(gross)
    cost_values = list(cost)
    if len(gross_values) != len(cost_values):
        raise ValueError("gross and cost must have equal length")
    if any(value < 0 for value in cost_values):
        raise ValueError("cost must be non-negative")
    return [g - c for g, c in zip(gross_values, cost_values)]


def inventory_conservation(start: float, trades: Iterable[float], end: float, tolerance: float = 1e-12) -> bool:
    """Check that signed trades move inventory from start to end."""
    return abs(start + sum(trades) - end) <= tolerance


def purged_train_indices(
    train: Sequence[int], valid: Sequence[int], embargo: int = 0
) -> list[int]:
    """Remove training observations overlapping validation plus an embargo tail."""
    if embargo < 0:
        raise ValueError("embargo must be non-negative")
    if not valid:
        return list(train)
    cutoff = max(valid) + embargo
    return [index for index in train if index < min(valid) or index > cutoff]


def stable_digest(payload: object) -> str:
    """Create a reproducible digest for a JSON-serialisable experiment manifest."""
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def adjusted_prices(raw_prices: Sequence[float], adjustment_factors: Sequence[float]) -> list[float]:
    """Apply positive adjustment factors to raw prices."""
    if len(raw_prices) != len(adjustment_factors):
        raise ValueError("prices and adjustment factors must have equal length")
    if any(price <= 0 for price in raw_prices) or any(factor <= 0 for factor in adjustment_factors):
        raise ValueError("prices and adjustment factors must be positive")
    return [price * factor for price, factor in zip(raw_prices, adjustment_factors)]


def simple_returns(prices: Sequence[float]) -> list[float]:
    """Calculate consecutive simple returns from strictly positive prices."""
    if len(prices) < 2:
        raise ValueError("at least two prices are required")
    if any(price <= 0 for price in prices):
        raise ValueError("prices must be positive")
    return [current / previous - 1.0 for previous, current in zip(prices, prices[1:])]


def ols_slope(x: Sequence[float], y: Sequence[float]) -> float:
    """Return the OLS slope with an intercept for a one-factor regression."""
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("x and y must have equal length of at least two")
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    denominator = sum((value - x_mean) ** 2 for value in x)
    if denominator == 0:
        raise ValueError("x must have non-zero variance")
    return sum((left - x_mean) * (right - y_mean) for left, right in zip(x, y)) / denominator


def portfolio_return(weights: Sequence[float], asset_returns: Sequence[float]) -> float:
    """Calculate a fully invested portfolio return."""
    if len(weights) != len(asset_returns) or not weights:
        raise ValueError("weights and returns must have equal non-zero length")
    if not math.isclose(sum(weights), 1.0, abs_tol=1e-12):
        raise ValueError("weights must sum to one")
    return sum(weight * value for weight, value in zip(weights, asset_returns))


def historical_var_es(losses: Sequence[float], confidence: float) -> tuple[float, float]:
    """Return empirical VaR and ES using an upper-tail loss convention."""
    if not losses:
        raise ValueError("losses must not be empty")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between zero and one")
    ordered = sorted(float(loss) for loss in losses)
    index = max(0, math.ceil(confidence * len(ordered)) - 1)
    value_at_risk = ordered[index]
    tail = ordered[index:]
    return value_at_risk, sum(tail) / len(tail)


def seeded_draws(seed: int, count: int) -> list[float]:
    """Generate deterministic uniform draws without mutating global RNG state."""
    if count < 0:
        raise ValueError("count must be non-negative")
    generator = random.Random(seed)
    return [generator.random() for _ in range(count)]


def artifact_manifest_is_complete(required: Iterable[str], actual: Iterable[str]) -> bool:
    """Check that every required artifact name is present in a manifest."""
    return set(required).issubset(set(actual))
