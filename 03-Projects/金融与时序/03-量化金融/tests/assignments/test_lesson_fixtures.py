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
    assert np.linalg.matrix_rank(l01["payoffs"]) == 2
    assert np.linalg.eigvalsh(l01["covariance"]).min() > 0
    assert l01["weights"].sum() == 1.0

    l02 = qf_l02_fixture()
    assert np.allclose(l02["transition"].sum(axis=1), 1.0)
    assert np.all(l02["transition"] >= 0)
    assert l02["walk_steps"] == 252


def test_capm_and_time_series_fixtures() -> None:
    l03 = qf_l03_fixture()
    assert l03["market_excess"].shape == l03["asset_excess"].shape == (12,)
    assert l03["influence_point"].shape == (2,)

    first = qf_l04_fixture()
    second = qf_l04_fixture()
    for key in ("ar2", "random_walk", "x", "y", "cointegration_error"):
        assert first[key].shape == (1000,)
        assert np.array_equal(first[key], second[key])
    assert np.allclose(first["y"] - 2.0 - 1.5 * first["x"], first["cointegration_error"])


def test_garch_fixture_obeys_variance_recursion() -> None:
    fixture = qf_l05_fixture()
    returns = fixture["returns"]
    variance = fixture["true_variance"]
    assert returns.shape == variance.shape == (2500,)
    assert fixture["train_end"] == 1800
    assert np.all(variance > 0)
    expected = (
        fixture["omega"]
        + fixture["alpha"] * returns[:-1] ** 2
        + fixture["beta"] * variance[:-1]
    )
    assert np.allclose(variance[1:], expected)


def test_portfolio_and_factor_fixtures_are_reproducible() -> None:
    l06 = qf_l06_fixture()
    assert l06["returns"].shape == (5000, 4)
    assert l06["train_end"] == 3000
    assert np.linalg.eigvalsh(l06["covariance"]).min() > 0
    assert np.array_equal(l06["returns"], qf_l06_fixture()["returns"])

    l07 = qf_l07_fixture()
    assert l07["factors"].shape == (240, 3)
    assert l07["true_betas"].shape == (40, 3)
    assert l07["returns"].shape == (240, 40)
    assert l07["decoy"].shape == (240,)
    assert l07["train_end"] == 180
    assert np.array_equal(l07["returns"], qf_l07_fixture()["returns"])


def test_option_and_hedging_configs_are_frozen() -> None:
    l08 = qf_l08_fixture()
    assert l08["spot"] > 0 and l08["strike"] > 0
    assert l08["volatility"] > 0 and l08["maturity"] > 0
    assert l08["paths"] == 200_000

    l09 = qf_l09_fixture()
    assert l09["hedge"]["rebalances"] == (12, 52, 252)
    assert l09["hedge"]["cost_rates"] == (0.0, 0.0005, 0.0010)
    assert l09["misspecification"]["realized_volatility"] == 0.25
    assert l09["misspecification"]["hedger_volatility"] == 0.20
