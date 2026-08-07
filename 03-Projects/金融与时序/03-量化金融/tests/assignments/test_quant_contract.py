from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.assignments.quant_contract import (
    adjusted_prices,
    artifact_manifest_is_complete,
    feature_time_precedes_execution,
    historical_var_es,
    inventory_conservation,
    net_return,
    ols_slope,
    portfolio_return,
    purged_train_indices,
    seeded_draws,
    simple_returns,
    split_is_disjoint,
    stable_digest,
)


def test_time_splits_are_pairwise_disjoint() -> None:
    assert split_is_disjoint([0, 1], [2], [3, 4])
    assert not split_is_disjoint([0, 1], [1], [2])


def test_feature_time_must_precede_execution() -> None:
    assert feature_time_precedes_execution([1, 2], [2, 3])
    assert not feature_time_precedes_execution([1, 3], [2, 3])


def test_net_return_and_cost_contract() -> None:
    assert net_return([0.10, -0.02], [0.01, 0.02]) == pytest.approx([0.09, -0.04])
    with pytest.raises(ValueError, match="non-negative"):
        net_return([0.1], [-0.1])


def test_inventory_conservation() -> None:
    assert inventory_conservation(100, [-25, -25, -50], 0)
    assert not inventory_conservation(100, [-25, -25], 0)


def test_purge_and_embargo_remove_overlap() -> None:
    assert purged_train_indices(list(range(10)), [4, 5], embargo=2) == [0, 1, 2, 3, 8, 9]


def test_manifest_digest_is_stable() -> None:
    payload = {"seed": 7, "split": ["train", "test"]}
    assert stable_digest(payload) == stable_digest({"split": ["train", "test"], "seed": 7})


def test_adjustment_and_return_contract() -> None:
    adjusted = adjusted_prices([50.0, 25.0, 27.5], [1.0, 2.0, 2.0])
    assert adjusted == pytest.approx([50.0, 50.0, 55.0])
    assert simple_returns(adjusted) == pytest.approx([0.0, 0.1])


def test_regression_and_portfolio_invariants() -> None:
    x = [0.0, 1.0, 2.0, 3.0]
    y = [2.0 + 3.0 * value for value in x]
    assert ols_slope(x, y) == pytest.approx(3.0)
    assert ols_slope([value + 10.0 for value in x], y) == pytest.approx(3.0)
    assert portfolio_return([0.5, 0.5], [0.1, -0.1]) == pytest.approx(0.0)
    with pytest.raises(ValueError, match="sum to one"):
        portfolio_return([0.4, 0.4], [0.1, -0.1])


def test_historical_var_and_es_tail_contract() -> None:
    value_at_risk, expected_shortfall = historical_var_es([0, 1, 2, 3, 4], 0.8)
    assert value_at_risk == pytest.approx(3.0)
    assert expected_shortfall == pytest.approx(3.5)
    assert expected_shortfall >= value_at_risk


def test_seed_and_required_artifacts_are_reproducible() -> None:
    assert seeded_draws(17, 5) == seeded_draws(17, 5)
    required = {"config", "manifest", "gross", "net", "tests"}
    assert artifact_manifest_is_complete(required, required | {"report"})
    assert not artifact_manifest_is_complete(required, {"config", "gross"})
