from __future__ import annotations

import sys
import unittest
from math import exp, sqrt
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from bsm_lab import (
    black_scholes_call,
    black_scholes_put,
    d1_d2,
    monte_carlo_call,
    simulate_delta_hedge,
)


PARAMS = {
    "spot": 100.0,
    "strike": 110.0,
    "maturity": 1.0,
    "rate": 0.05,
    "volatility": 0.20,
}


class BsmLabTests(unittest.TestCase):
    def test_verified_numerical_anchor(self):
        _, d2 = d1_d2(**PARAMS)
        call = black_scholes_call(**PARAMS)
        self.assertAlmostEqual(d2, -0.326551, places=6)
        self.assertAlmostEqual(call, 6.040088, places=6)

    def test_put_call_parity(self):
        call = black_scholes_call(**PARAMS)
        put = black_scholes_put(**PARAMS)
        parity = PARAMS["spot"] - PARAMS["strike"] * exp(
            -PARAMS["rate"] * PARAMS["maturity"]
        )
        self.assertAlmostEqual(call - put, parity, places=10)

    def test_call_price_increases_with_volatility(self):
        low = black_scholes_call(**{**PARAMS, "volatility": 0.10})
        high = black_scholes_call(**{**PARAMS, "volatility": 0.30})
        self.assertGreater(high, low)

    def test_antithetic_monte_carlo_matches_closed_form(self):
        closed = black_scholes_call(**PARAMS)
        estimate, standard_error = monte_carlo_call(
            **PARAMS,
            paths=100_000,
            seed=7,
        )
        self.assertLess(abs(estimate - closed), 4 * standard_error + 0.02)

        rng = np.random.default_rng(7)
        shocks = rng.standard_normal(50_000)
        discount = exp(-PARAMS["rate"] * PARAMS["maturity"])
        positive = PARAMS["spot"] * np.exp(
            (PARAMS["rate"] - 0.5 * PARAMS["volatility"] ** 2) * PARAMS["maturity"]
            + PARAMS["volatility"] * sqrt(PARAMS["maturity"]) * shocks
        )
        negative = PARAMS["spot"] * np.exp(
            (PARAMS["rate"] - 0.5 * PARAMS["volatility"] ** 2) * PARAMS["maturity"]
            - PARAMS["volatility"] * sqrt(PARAMS["maturity"]) * shocks
        )
        pair_means = discount * (
            np.maximum(positive - PARAMS["strike"], 0.0)
            + np.maximum(negative - PARAMS["strike"], 0.0)
        ) / 2.0
        expected_standard_error = pair_means.std(ddof=1) / sqrt(len(pair_means))
        self.assertAlmostEqual(standard_error, expected_standard_error, places=12)

    def test_antithetic_paths_must_be_even(self):
        with self.assertRaisesRegex(ValueError, "even"):
            monte_carlo_call(**PARAMS, paths=99, seed=7)

    def test_transaction_cost_reduces_replication_value(self):
        no_cost = simulate_delta_hedge(
            **PARAMS,
            paths=5_000,
            steps=52,
            cost_bps=0.0,
            seed=11,
        )
        with_cost = simulate_delta_hedge(
            **PARAMS,
            paths=5_000,
            steps=52,
            cost_bps=10.0,
            seed=11,
        )
        self.assertLess(with_cost["mean_error"], no_cost["mean_error"])


if __name__ == "__main__":
    unittest.main()
