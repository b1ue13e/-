from __future__ import annotations

from math import sqrt

import numpy as np


def qf_l01_fixture() -> dict[str, np.ndarray]:
    return {
        "payoffs": np.array([[1.02, 1.02], [132.0, 88.0]]),
        "prices": np.array([1.0, 100.0]),
        "claim_c": np.array([15.0, 0.0]),
        "claim_d": np.array([6.0, 4.0]),
        "mean_returns": np.array([0.04, 0.07, 0.10]),
        "covariance": np.array(
            [
                [0.0100, 0.0018, 0.0012],
                [0.0018, 0.0225, 0.0045],
                [0.0012, 0.0045, 0.0400],
            ]
        ),
        "weights": np.array([0.50, 0.30, 0.20]),
    }


def qf_l02_fixture() -> dict[str, np.ndarray | float | int | tuple[int, ...]]:
    return {
        "state_probability": np.array([0.8, 0.2]),
        "conditional_mean": np.array([0.001, -0.004]),
        "conditional_variance": np.array([0.0001, 0.0009]),
        "walk_steps": 252,
        "increment_volatility": 0.01,
        "zero_drift": 0.0,
        "nonzero_drift": 0.0002,
        "path_counts": (100, 1_000, 10_000),
        "seed": 17,
    }


def qf_l03_fixture() -> dict[str, np.ndarray]:
    market = np.array(
        [0.020, -0.010, 0.015, 0.030, -0.020, 0.005, 0.012, -0.015, 0.025, -0.005, 0.018, 0.008]
    )
    asset = np.array(
        [0.031, -0.012, 0.021, 0.043, -0.027, 0.009, 0.016, -0.019, 0.035, -0.006, 0.025, 0.012]
    )
    return {
        "market_excess": market,
        "asset_excess": asset,
        "influence_point": np.array([0.080, -0.040]),
    }


def qf_l04_fixture() -> dict[str, np.ndarray | dict[str, object]]:
    rng = np.random.default_rng(404)
    n = 1200
    burn_in = 200

    z = np.zeros(n)
    eps = rng.normal(size=n)
    for t in range(2, n):
        z[t] = 0.2 + 0.6 * z[t - 1] - 0.2 * z[t - 2] + eps[t]

    x = np.cumsum(rng.normal(size=n))
    u = np.zeros(n)
    nu = rng.normal(scale=0.5, size=n)
    for t in range(1, n):
        u[t] = 0.65 * u[t - 1] + nu[t]
    y = 2.0 + 1.5 * x + u
    a = np.cumsum(rng.normal(size=n))
    b = np.cumsum(rng.normal(size=n))
    keep = slice(burn_in, None)

    return {
        "ar2": z[keep],
        "ar_intercept": 0.2,
        "ar_coefficients": (0.6, -0.2),
        "random_walk": x[keep],
        "x": x[keep],
        "y": y[keep],
        "independent_walk_a": a[keep],
        "independent_walk_b": b[keep],
        "adf_config": {"regression": "c", "maxlag": 1, "autolag": None},
    }


def qf_l05_fixture() -> dict[str, object]:
    rng = np.random.default_rng(505)
    omega, alpha, beta = 0.000002, 0.07, 0.90
    total, burn_in = 3000, 500
    z = rng.normal(size=total)
    variance = np.empty(total)
    returns = np.empty(total)
    variance[0] = omega / (1.0 - alpha - beta)
    returns[0] = sqrt(variance[0]) * z[0]
    for t in range(1, total):
        variance[t] = omega + alpha * returns[t - 1] ** 2 + beta * variance[t - 1]
        returns[t] = sqrt(variance[t]) * z[t]

    return {
        "returns": returns[burn_in:],
        "train_end": 1800,
        "forecast_horizon": 400,
        "initial_variance": omega / (1.0 - alpha - beta),
        "candidate_parameters": (
            {"candidate_id": "low_memory", "omega": 0.000004, "alpha": 0.12, "beta": 0.78},
            {"candidate_id": "persistent", "omega": 0.000002, "alpha": 0.07, "beta": 0.90},
            {"candidate_id": "smooth", "omega": 0.000003, "alpha": 0.04, "beta": 0.90},
        ),
        "seed": 505,
    }


def qf_l06_fixture() -> dict[str, np.ndarray | float | int]:
    mean = np.array([0.04, 0.06, 0.09, 0.05])
    volatility = np.array([0.10, 0.15, 0.20, 0.12])
    correlation = np.array(
        [
            [1.00, 0.30, 0.10, 0.20],
            [0.30, 1.00, 0.40, 0.25],
            [0.10, 0.40, 1.00, 0.15],
            [0.20, 0.25, 0.15, 1.00],
        ]
    )
    covariance = np.diag(volatility) @ correlation @ np.diag(volatility)
    daily_covariance = covariance / 252.0
    rng = np.random.default_rng(606)
    degrees_of_freedom = 5
    z = rng.standard_t(df=degrees_of_freedom, size=(5000, 4)) / sqrt(
        degrees_of_freedom / (degrees_of_freedom - 2)
    )
    returns = z @ np.linalg.cholesky(daily_covariance).T
    return {
        "mean": mean,
        "volatility": volatility,
        "correlation": correlation,
        "covariance": covariance,
        "returns": returns,
        "train_end": 3000,
        "risk_confidence": 0.95,
        "pot_threshold_quantile": 0.95,
        "pot_target_confidence": 0.99,
        "min_exceedances": 80,
    }


def qf_l07_fixture() -> dict[str, np.ndarray | int]:
    rng = np.random.default_rng(707)
    factor_mean = np.array([0.005, 0.002, 0.003])
    factor_covariance = np.array(
        [
            [0.0016, 0.0002, 0.0001],
            [0.0002, 0.0009, 0.00015],
            [0.0001, 0.00015, 0.0012],
        ]
    )
    factors = rng.multivariate_normal(factor_mean, factor_covariance, size=240)
    betas = np.empty((40, 3))
    betas[:, 0] = rng.normal(1.0, 0.20, size=40)
    betas[:, 1] = rng.normal(0.0, 0.50, size=40)
    betas[:, 2] = rng.normal(0.0, 0.50, size=40)
    idiosyncratic = rng.normal(0.0, 0.03, size=(240, 40))
    returns = factors @ betas.T + idiosyncratic
    decoy = rng.normal(0.0, factors[:, 0].std(ddof=0), size=240)
    return {
        "factor_mean": factor_mean,
        "factor_covariance": factor_covariance,
        "factors": factors,
        "returns": returns,
        "decoy": decoy,
        "train_end": 180,
    }


def qf_l08_fixture() -> dict[str, float | int]:
    return {
        "spot": 100.0,
        "strike": 105.0,
        "rate": 0.03,
        "dividend_yield": 0.01,
        "volatility": 0.20,
        "maturity": 0.75,
        "seed": 808,
        "paths": 200_000,
        "confidence": 0.95,
        "epsilon": 0.10,
        "delta_tolerance": 1e-4,
        "gamma_tolerance": 1e-5,
    }


def qf_l09_fixture() -> dict[str, object]:
    return {
        "gbm": {"spot": 100.0, "drift": 0.06, "volatility": 0.20, "maturity": 1.0},
        "euler": {
            "paths": 20_000,
            "steps": (12, 252),
        },
        "hedge": {
            "spot": 100.0,
            "strike": 100.0,
            "rate": 0.02,
            "dividend_yield": 0.0,
            "model_volatility": 0.20,
            "maturity": 1.0,
            "realized_volatility": 0.20,
            "paths": 5_000,
            "rebalances": (12, 52),
            "cost_rates": (0.0, 0.0005),
        },
        "seed": 909,
    }
