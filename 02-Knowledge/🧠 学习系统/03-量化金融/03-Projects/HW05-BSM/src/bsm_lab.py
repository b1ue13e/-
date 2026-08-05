from __future__ import annotations

import argparse
import json
from math import exp, log, sqrt
from pathlib import Path

import numpy as np
from scipy.stats import norm


def validate_inputs(spot, strike, maturity, volatility):
    if min(spot, strike, maturity, volatility) <= 0:
        raise ValueError("spot, strike, maturity, and volatility must be positive")


def d1_d2(spot, strike, maturity, rate, volatility):
    validate_inputs(spot, strike, maturity, volatility)
    scale = volatility * sqrt(maturity)
    d1 = (
        log(spot / strike) + (rate + 0.5 * volatility**2) * maturity
    ) / scale
    return d1, d1 - scale


def black_scholes_call(spot, strike, maturity, rate, volatility):
    d1, d2 = d1_d2(spot, strike, maturity, rate, volatility)
    return spot * norm.cdf(d1) - strike * exp(-rate * maturity) * norm.cdf(d2)


def black_scholes_put(spot, strike, maturity, rate, volatility):
    d1, d2 = d1_d2(spot, strike, maturity, rate, volatility)
    return strike * exp(-rate * maturity) * norm.cdf(-d2) - spot * norm.cdf(-d1)


def call_delta(spot, strike, maturity, rate, volatility):
    d1, _ = d1_d2(spot, strike, maturity, rate, volatility)
    return norm.cdf(d1)


def monte_carlo_call(
    spot,
    strike,
    maturity,
    rate,
    volatility,
    paths=100_000,
    seed=42,
):
    validate_inputs(spot, strike, maturity, volatility)
    if paths < 4 or paths % 2:
        raise ValueError("paths must be an even number of at least 4")

    rng = np.random.default_rng(seed)
    half = paths // 2
    shocks = rng.standard_normal(half)
    terminal_positive = spot * np.exp(
        (rate - 0.5 * volatility**2) * maturity
        + volatility * sqrt(maturity) * shocks
    )
    terminal_negative = spot * np.exp(
        (rate - 0.5 * volatility**2) * maturity
        - volatility * sqrt(maturity) * shocks
    )
    discount = exp(-rate * maturity)
    payoff_positive = discount * np.maximum(terminal_positive - strike, 0.0)
    payoff_negative = discount * np.maximum(terminal_negative - strike, 0.0)
    pair_means = (payoff_positive + payoff_negative) / 2.0
    estimate = float(pair_means.mean())
    standard_error = float(pair_means.std(ddof=1) / sqrt(half))
    return estimate, standard_error


def simulate_delta_hedge(
    spot,
    strike,
    maturity,
    rate,
    volatility,
    paths=10_000,
    steps=52,
    cost_bps=0.0,
    seed=42,
):
    validate_inputs(spot, strike, maturity, volatility)
    if paths < 1 or steps < 1 or cost_bps < 0:
        raise ValueError("paths and steps must be positive; cost_bps cannot be negative")

    rng = np.random.default_rng(seed)
    dt = maturity / steps
    spots = np.full(paths, float(spot))
    delta = np.full(paths, call_delta(spot, strike, maturity, rate, volatility))
    cash = np.full(
        paths,
        black_scholes_call(spot, strike, maturity, rate, volatility),
    ) - delta * spot

    for step in range(1, steps + 1):
        shocks = rng.standard_normal(paths)
        spots *= np.exp(
            (rate - 0.5 * volatility**2) * dt
            + volatility * sqrt(dt) * shocks
        )
        cash *= exp(rate * dt)

        if step < steps:
            remaining = maturity - step * dt
            new_delta = norm.cdf(
                (
                    np.log(spots / strike)
                    + (rate + 0.5 * volatility**2) * remaining
                )
                / (volatility * sqrt(remaining))
            )
            trade = new_delta - delta
            cash -= trade * spots
            cash -= np.abs(trade) * spots * cost_bps / 10_000.0
            delta = new_delta

    portfolio = cash + delta * spots
    payoff = np.maximum(spots - strike, 0.0)
    error = portfolio - payoff
    return {
        "mean_error": float(error.mean()),
        "error_std": float(error.std(ddof=1)),
        "rmse": float(np.sqrt(np.mean(error**2))),
        "paths": int(paths),
        "steps": int(steps),
        "cost_bps": float(cost_bps),
    }


def run_experiment(paths, hedge_paths, hedge_steps, seed):
    params = {
        "spot": 100.0,
        "strike": 110.0,
        "maturity": 1.0,
        "rate": 0.05,
        "volatility": 0.20,
    }
    d1, d2 = d1_d2(**params)
    closed_form = black_scholes_call(**params)
    mc_price, mc_se = monte_carlo_call(**params, paths=paths, seed=seed)
    hedge = simulate_delta_hedge(
        **params,
        paths=hedge_paths,
        steps=hedge_steps,
        cost_bps=10.0,
        seed=seed,
    )
    return {
        **params,
        "d1": d1,
        "d2": d2,
        "closed_form_call": closed_form,
        "mc_call": mc_price,
        "mc_standard_error": mc_se,
        "mc_absolute_error": abs(mc_price - closed_form),
        "hedge": hedge,
        "seed": int(seed),
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Run the reproducible HW05 BSM lab.")
    parser.add_argument("--output", type=Path, default=Path("artifacts"))
    parser.add_argument("--paths", type=int, default=50_000)
    parser.add_argument("--hedge-paths", type=int, default=10_000)
    parser.add_argument("--hedge-steps", type=int, default=52)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    metrics = run_experiment(args.paths, args.hedge_paths, args.hedge_steps, args.seed)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
