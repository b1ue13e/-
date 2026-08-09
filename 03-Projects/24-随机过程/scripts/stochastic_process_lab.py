"""Reproducible low-compute reference simulations for the stochastic-process course."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Iterable, Sequence


def validate_transition_matrix(matrix: Sequence[Sequence[float]]) -> None:
    if not matrix or any(len(row) != len(matrix) for row in matrix):
        raise ValueError("transition matrix must be non-empty and square")
    for row in matrix:
        if any(value < 0.0 for value in row):
            raise ValueError("transition probabilities must be non-negative")
        if not math.isclose(sum(row), 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("each transition-matrix row must sum to one")


def stationary_distribution(
    matrix: Sequence[Sequence[float]],
    tolerance: float = 1e-13,
    max_iterations: int = 100_000,
) -> list[float]:
    """Power iteration for the finite, aperiodic examples used in the course."""
    validate_transition_matrix(matrix)
    size = len(matrix)
    distribution = [1.0 / size] * size
    for _ in range(max_iterations):
        updated = [
            sum(distribution[i] * matrix[i][j] for i in range(size))
            for j in range(size)
        ]
        if max(abs(a - b) for a, b in zip(updated, distribution)) < tolerance:
            return updated
        distribution = updated
    raise RuntimeError("stationary iteration did not converge; check periodicity")


def _categorical(probabilities: Sequence[float], rng: random.Random) -> int:
    draw = rng.random()
    cumulative = 0.0
    for index, probability in enumerate(probabilities):
        cumulative += probability
        if draw <= cumulative:
            return index
    return len(probabilities) - 1


def simulate_markov_chain(
    matrix: Sequence[Sequence[float]],
    initial_state: int,
    steps: int,
    seed: int,
) -> list[int]:
    validate_transition_matrix(matrix)
    if initial_state not in range(len(matrix)):
        raise ValueError("initial state is outside the state space")
    if steps < 0:
        raise ValueError("steps must be non-negative")
    rng = random.Random(seed)
    state = initial_state
    path = [state]
    for _ in range(steps):
        state = _categorical(matrix[state], rng)
        path.append(state)
    return path


def simulate_poisson_counts(
    rate: float,
    horizon: float,
    samples: int,
    seed: int,
) -> list[int]:
    if rate <= 0.0 or horizon <= 0.0 or samples <= 0:
        raise ValueError("rate, horizon, and samples must be positive")
    rng = random.Random(seed)
    counts: list[int] = []
    for _ in range(samples):
        time = 0.0
        count = 0
        while True:
            time += rng.expovariate(rate)
            if time > horizon:
                break
            count += 1
        counts.append(count)
    return counts


def simulate_brownian_summary(
    paths: int,
    steps: int,
    horizon: float,
    seed: int,
) -> dict[str, float]:
    if paths <= 1 or steps <= 0 or horizon <= 0.0:
        raise ValueError("paths > 1, steps > 0, and horizon > 0 are required")
    rng = random.Random(seed)
    dt = horizon / steps
    scale = math.sqrt(dt)
    terminals: list[float] = []
    quadratic_variations: list[float] = []
    for _ in range(paths):
        value = 0.0
        qv = 0.0
        for _ in range(steps):
            increment = scale * rng.gauss(0.0, 1.0)
            value += increment
            qv += increment * increment
        terminals.append(value)
        quadratic_variations.append(qv)
    return {
        "terminal_mean": _mean(terminals),
        "terminal_variance": _sample_variance(terminals),
        "quadratic_variation_mean": _mean(quadratic_variations),
        "theory_terminal_mean": 0.0,
        "theory_terminal_variance": horizon,
        "theory_quadratic_variation": horizon,
    }


def simulate_brownian_maximum(
    paths: int,
    steps: int,
    horizon: float,
    threshold: float,
    seed: int,
) -> dict[str, float]:
    """Compare a discretized Brownian maximum with the reflection principle."""
    if paths <= 1 or steps <= 0 or horizon <= 0.0 or threshold <= 0.0:
        raise ValueError(
            "paths > 1 and positive steps, horizon, and threshold are required"
        )
    rng = random.Random(seed)
    scale = math.sqrt(horizon / steps)
    maximum_hits = 0
    terminal_hits = 0
    for _ in range(paths):
        value = 0.0
        maximum = 0.0
        for _ in range(steps):
            value += scale * rng.gauss(0.0, 1.0)
            maximum = max(maximum, value)
        maximum_hits += maximum >= threshold
        terminal_hits += value >= threshold

    theory_maximum_probability = math.erfc(
        threshold / math.sqrt(2.0 * horizon)
    )
    return {
        "empirical_maximum_probability": maximum_hits / paths,
        "empirical_terminal_probability": terminal_hits / paths,
        "theory_maximum_probability": theory_maximum_probability,
        "theory_terminal_probability": theory_maximum_probability / 2.0,
        "paths": float(paths),
        "steps": float(steps),
    }


def simulate_gamblers_ruin(
    start: int,
    upper: int,
    trials: int,
    seed: int,
) -> dict[str, float]:
    """Simulate a fair stopped random walk on {0, ..., upper}."""
    if upper <= 1 or start <= 0 or start >= upper or trials <= 0:
        raise ValueError("require upper > 1, 0 < start < upper, and trials > 0")
    rng = random.Random(seed)
    upper_hits = 0
    stopping_times: list[int] = []
    for _ in range(trials):
        state = start
        steps = 0
        while 0 < state < upper:
            state += 1 if rng.random() < 0.5 else -1
            steps += 1
        upper_hits += state == upper
        stopping_times.append(steps)
    return {
        "empirical_upper_hit_probability": upper_hits / trials,
        "theory_upper_hit_probability": start / upper,
        "empirical_mean_stopping_time": _mean(stopping_times),
        "theory_mean_stopping_time": float(start * (upper - start)),
        "trials": float(trials),
    }


def simulate_mm1(
    arrival_rate: float,
    service_rate: float,
    horizon: float,
    burn_in: float,
    seed: int,
) -> dict[str, float | int]:
    if arrival_rate <= 0.0 or service_rate <= 0.0:
        raise ValueError("arrival and service rates must be positive")
    if arrival_rate >= service_rate:
        raise ValueError("M/M/1 steady-state metrics require arrival_rate < service_rate")
    if not 0.0 <= burn_in < horizon:
        raise ValueError("burn_in must satisfy 0 <= burn_in < horizon")

    rng = random.Random(seed)
    time = 0.0
    number = 0
    arrivals = 0
    departures = 0
    area = 0.0
    next_arrival = rng.expovariate(arrival_rate)
    next_departure = math.inf

    while time < horizon:
        event_time = min(next_arrival, next_departure, horizon)
        overlap_start = max(time, burn_in)
        if event_time > overlap_start:
            area += number * (event_time - overlap_start)
        time = event_time
        if time >= horizon:
            break
        if next_arrival <= next_departure:
            number += 1
            arrivals += 1
            next_arrival = time + rng.expovariate(arrival_rate)
            if number == 1:
                next_departure = time + rng.expovariate(service_rate)
        else:
            number -= 1
            departures += 1
            next_departure = (
                time + rng.expovariate(service_rate) if number > 0 else math.inf
            )

    rho = arrival_rate / service_rate
    return {
        "rho": rho,
        "time_average_number": area / (horizon - burn_in),
        "theory_average_number": rho / (1.0 - rho),
        "arrivals": arrivals,
        "departures": departures,
        "final_number": number,
    }


def simulate_ou_endpoints(
    kappa: float,
    theta: float,
    sigma: float,
    x0: float,
    horizon: float,
    steps: int,
    paths: int,
    seed: int,
) -> dict[str, float]:
    if kappa <= 0.0 or sigma < 0.0 or horizon <= 0.0:
        raise ValueError("kappa and horizon must be positive; sigma must be non-negative")
    if steps <= 0 or paths <= 1:
        raise ValueError("steps > 0 and paths > 1 are required")
    rng = random.Random(seed)
    dt = horizon / steps
    scale = sigma * math.sqrt(dt)
    endpoints: list[float] = []
    for _ in range(paths):
        value = x0
        for _ in range(steps):
            value += kappa * (theta - value) * dt + scale * rng.gauss(0.0, 1.0)
        endpoints.append(value)
    theory_mean = theta + (x0 - theta) * math.exp(-kappa * horizon)
    theory_variance = sigma * sigma * (1.0 - math.exp(-2.0 * kappa * horizon)) / (
        2.0 * kappa
    )
    return {
        "endpoint_mean": _mean(endpoints),
        "endpoint_variance": _sample_variance(endpoints),
        "theory_mean": theory_mean,
        "theory_variance": theory_variance,
        "dt": dt,
    }


def simulate_gbm_error_study(
    mu: float,
    sigma: float,
    s0: float,
    horizon: float,
    step_counts: Sequence[int],
    paths: int,
    seed: int,
) -> dict[str, object]:
    """Estimate Euler-Maruyama strong order using coupled Brownian increments."""
    counts = sorted(set(step_counts))
    if sigma <= 0.0 or s0 <= 0.0 or horizon <= 0.0 or paths <= 1:
        raise ValueError("sigma, s0, horizon must be positive and paths must exceed one")
    if len(counts) < 2 or any(count <= 0 for count in counts):
        raise ValueError("at least two positive step counts are required")
    finest_steps = counts[-1]
    if any(finest_steps % count != 0 for count in counts):
        raise ValueError("the finest step count must be divisible by every coarser count")

    rng = random.Random(seed)
    finest_dt = horizon / finest_steps
    accumulators = {
        count: {"absolute_errors": [], "endpoints": []} for count in counts
    }
    for _ in range(paths):
        fine_increments = [
            math.sqrt(finest_dt) * rng.gauss(0.0, 1.0)
            for _ in range(finest_steps)
        ]
        terminal_w = sum(fine_increments)
        exact = s0 * math.exp(
            (mu - 0.5 * sigma * sigma) * horizon + sigma * terminal_w
        )
        for count in counts:
            factor = finest_steps // count
            dt = horizon / count
            value = s0
            for offset in range(0, finest_steps, factor):
                increment = sum(fine_increments[offset : offset + factor])
                value += mu * value * dt + sigma * value * increment
            accumulators[count]["absolute_errors"].append(abs(exact - value))
            accumulators[count]["endpoints"].append(value)

    theory_mean = s0 * math.exp(mu * horizon)
    rows: list[dict[str, float | int]] = []
    for count in counts:
        endpoints = accumulators[count]["endpoints"]
        strong_mae = _mean(accumulators[count]["absolute_errors"])
        endpoint_mean = _mean(endpoints)
        rows.append(
            {
                "steps": count,
                "dt": horizon / count,
                "strong_mae": strong_mae,
                "endpoint_mean": endpoint_mean,
                "theory_mean": theory_mean,
                "weak_abs_error": abs(endpoint_mean - theory_mean),
                "monte_carlo_standard_error": math.sqrt(
                    _sample_variance(endpoints) / paths
                ),
            }
        )

    estimated_strong_order = _linear_regression_slope(
        [math.log(row["dt"]) for row in rows],
        [math.log(row["strong_mae"]) for row in rows],
    )
    return {
        "coupling": "coarse increments are sums of finest-grid increments",
        "paths": paths,
        "rows": rows,
        "estimated_strong_order": estimated_strong_order,
        "theory_strong_order": 0.5,
    }


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values)


def _sample_variance(values: Iterable[float]) -> float:
    values = list(values)
    mean = _mean(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)


def _linear_regression_slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("regression requires paired sequences with at least two values")
    mean_x = _mean(xs)
    mean_y = _mean(ys)
    denominator = sum((value - mean_x) ** 2 for value in xs)
    if denominator == 0.0:
        raise ValueError("regression x values must not all be equal")
    return sum(
        (x_value - mean_x) * (y_value - mean_y)
        for x_value, y_value in zip(xs, ys)
    ) / denominator


def build_reference_report(seed: int = 20260808) -> dict[str, object]:
    matrix = [[0.8, 0.2], [0.3, 0.7]]
    markov_path = simulate_markov_chain(matrix, initial_state=0, steps=50_000, seed=seed)
    frequencies = [markov_path.count(state) / len(markov_path) for state in range(2)]
    poisson_counts = simulate_poisson_counts(3.0, 2.0, 10_000, seed + 1)
    return {
        "manifest": {
            "seed": seed,
            "implementation": "Python standard library",
            "purpose": "reference toolchain check, not learner completion evidence",
        },
        "markov": {
            "matrix": matrix,
            "stationary": stationary_distribution(matrix),
            "empirical_frequencies": frequencies,
            "steps": 50_000,
        },
        "poisson": {
            "rate": 3.0,
            "horizon": 2.0,
            "empirical_mean": _mean(poisson_counts),
            "empirical_variance": _sample_variance(poisson_counts),
            "theory_mean_variance": 6.0,
            "samples": 10_000,
        },
        "brownian": simulate_brownian_summary(4_000, 200, 1.0, seed + 2),
        "brownian_reflection": simulate_brownian_maximum(
            2_500, 200, 1.0, 0.75, seed + 3
        ),
        "stopped_walk": simulate_gamblers_ruin(3, 10, 8_000, seed + 4),
        "mm1": simulate_mm1(2.0, 3.0, 20_000.0, 2_000.0, seed + 5),
        "ou": simulate_ou_endpoints(1.5, 0.5, 0.7, -1.0, 2.0, 400, 4_000, seed + 6),
        "gbm_error_study": simulate_gbm_error_study(
            0.08, 0.3, 1.0, 1.0, [16, 32, 64, 128], 1_200, seed + 7
        ),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["all"])
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    report = build_reference_report(args.seed)
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
        print(args.output)
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
