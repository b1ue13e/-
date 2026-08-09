from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.assignments.lesson_fixtures import (  # noqa: E402
    qf_l01_fixture,
    qf_l02_fixture,
    qf_l03_fixture,
    qf_l04_fixture,
    qf_l05_fixture,
    qf_l06_fixture,
    qf_l07_fixture,
    qf_l08_fixture,
    qf_l09_fixture,
)


def test_linear_algebra_and_probability_fixtures() -> None:
    l01 = qf_l01_fixture()
    assert l01["payoffs"].shape == (2, 2)
    assert np.allclose(l01["payoffs"][0], [1.02, 1.02])
    assert np.linalg.eigvalsh(l01["covariance"]).min() > 0
    assert l01["weights"].sum() == 1.0

    l02 = qf_l02_fixture()
    assert np.isclose(l02["state_probability"].sum(), 1.0)
    assert l02["walk_steps"] == 252
    assert l02["path_counts"] == (100, 1_000, 10_000)
    assert l02["zero_drift"] == 0.0
    assert l02["nonzero_drift"] != 0.0


def test_capm_and_time_series_fixtures() -> None:
    l03 = qf_l03_fixture()
    assert l03["market_excess"].shape == l03["asset_excess"].shape == (12,)
    assert l03["influence_point"].shape == (2,)

    first = qf_l04_fixture()
    second = qf_l04_fixture()
    for key in ("ar2", "random_walk", "x", "y"):
        assert first[key].shape == (1000,)
        assert np.array_equal(first[key], second[key])
    assert first["ar_intercept"] == 0.2
    assert first["ar_coefficients"] == (0.6, -0.2)


def test_garch_fixture_is_reproducible_and_candidates_are_valid() -> None:
    fixture = qf_l05_fixture()
    returns = fixture["returns"]
    assert returns.shape == (2500,)
    assert fixture["train_end"] == 1800
    assert fixture["forecast_horizon"] == 400
    assert fixture["train_end"] + fixture["forecast_horizon"] <= returns.size
    assert fixture["initial_variance"] > 0
    assert np.array_equal(returns, qf_l05_fixture()["returns"])
    assert "true_variance" not in fixture
    assert not {"omega", "alpha", "beta"} <= set(fixture)
    candidates = fixture["candidate_parameters"]
    assert len(candidates) == 3
    assert len({candidate["candidate_id"] for candidate in candidates}) == 3
    assert all(
        candidate["omega"] > 0
        and candidate["alpha"] >= 0
        and candidate["beta"] >= 0
        and candidate["alpha"] + candidate["beta"] < 1
        for candidate in candidates
    )


def test_portfolio_and_factor_fixtures_are_reproducible() -> None:
    l06 = qf_l06_fixture()
    assert l06["returns"].shape == (5000, 4)
    assert l06["train_end"] == 3000
    assert l06["risk_confidence"] == 0.95
    assert l06["pot_target_confidence"] > l06["pot_threshold_quantile"]
    assert (l06["returns"].shape[0] - l06["train_end"]) * (
        1 - l06["pot_threshold_quantile"]
    ) >= l06["min_exceedances"]
    assert np.linalg.eigvalsh(l06["covariance"]).min() > 0
    assert np.array_equal(l06["returns"], qf_l06_fixture()["returns"])

    l07 = qf_l07_fixture()
    assert l07["factors"].shape == (240, 3)
    assert l07["returns"].shape == (240, 40)
    assert l07["decoy"].shape == (240,)
    assert l07["train_end"] == 180
    assert np.array_equal(l07["returns"], qf_l07_fixture()["returns"])
    assert "true_betas" not in l07


def test_option_and_hedging_configs_are_frozen() -> None:
    l08 = qf_l08_fixture()
    assert l08["spot"] > 0 and l08["strike"] > 0
    assert l08["volatility"] > 0 and l08["maturity"] > 0
    assert l08["paths"] == 200_000
    assert l08["confidence"] == 0.95
    assert l08["epsilon"] > 0

    l09 = qf_l09_fixture()
    assert "vasicek" not in l09
    assert l09["euler"]["steps"] == (12, 252)
    assert l09["euler"]["paths"] == 20_000
    assert l09["hedge"]["rebalances"] == (12, 52)
    assert l09["hedge"]["cost_rates"] == (0.0, 0.0005)
    assert l09["hedge"]["paths"] == 5_000
    assert l09["hedge"]["realized_volatility"] == l09["hedge"]["model_volatility"]
