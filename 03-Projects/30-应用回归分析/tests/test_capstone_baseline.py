from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from capstone_baseline import (  # noqa: E402
    RANDOM_STATE,
    build_candidates,
    load_and_split,
    run_experiment,
)


def test_split_is_deterministic_and_disjoint() -> None:
    first = load_and_split(RANDOM_STATE)
    second = load_and_split(RANDOM_STATE)
    X_train, X_test, y_train, y_test = first

    assert X_train.index.equals(second[0].index)
    assert X_test.index.equals(second[1].index)
    assert set(X_train.index).isdisjoint(X_test.index)
    assert X_train.index.equals(y_train.index)
    assert X_test.index.equals(y_test.index)


def test_all_learned_preprocessing_stays_inside_estimators() -> None:
    candidates = build_candidates(RANDOM_STATE)

    assert list(candidates["ols"].named_steps) == ["scale", "model"]
    assert list(candidates["ridge"].estimator.named_steps) == ["scale", "model"]
    assert list(candidates["lasso"].estimator.named_steps) == ["scale", "model"]


def test_experiment_writes_finite_reproducible_schema(tmp_path: Path) -> None:
    metrics = run_experiment(tmp_path, RANDOM_STATE)
    stored = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))
    predictions = pd.read_csv(tmp_path / "predictions.csv")

    assert stored == metrics
    assert metrics["selected_model"] in {"mean", "ols", "ridge", "lasso"}
    assert metrics["selection_source"] == "training-only nested cross-validation"
    assert metrics["test_evaluations"] == 1
    assert set(metrics["cv"]) == {"mean", "ols", "ridge", "lasso"}
    assert all(np.isfinite(value) for value in metrics["test"].values())
    assert len(predictions) == metrics["test_rows"]
    assert {"row_id", "actual", "prediction", "residual"} == set(predictions)

