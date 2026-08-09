from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


def load_and_split(
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    dataset = load_diabetes(as_frame=True)
    return train_test_split(
        dataset.data,
        dataset.target,
        test_size=0.2,
        random_state=random_state,
    )


def build_candidates(random_state: int = RANDOM_STATE) -> dict[str, Any]:
    inner_cv = KFold(n_splits=3, shuffle=True, random_state=random_state)

    ridge = GridSearchCV(
        Pipeline(
            [
                ("scale", StandardScaler()),
                ("model", Ridge()),
            ]
        ),
        {"model__alpha": np.logspace(-2, 2, 7)},
        scoring="neg_root_mean_squared_error",
        cv=inner_cv,
    )
    lasso = GridSearchCV(
        Pipeline(
            [
                ("scale", StandardScaler()),
                ("model", Lasso(max_iter=20000)),
            ]
        ),
        {"model__alpha": np.logspace(-2, 2, 7)},
        scoring="neg_root_mean_squared_error",
        cv=inner_cv,
    )
    return {
        "mean": DummyRegressor(strategy="mean"),
        "ols": Pipeline(
            [
                ("scale", StandardScaler()),
                ("model", LinearRegression()),
            ]
        ),
        "ridge": ridge,
        "lasso": lasso,
    }


def select_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = RANDOM_STATE,
) -> tuple[str, Any, dict[str, dict[str, float]]]:
    outer_cv = KFold(n_splits=5, shuffle=True, random_state=random_state)
    candidates = build_candidates(random_state)
    cv_results: dict[str, dict[str, float]] = {}

    for name, estimator in candidates.items():
        fold_rmse = -cross_val_score(
            estimator,
            X_train,
            y_train,
            scoring="neg_root_mean_squared_error",
            cv=outer_cv,
        )
        cv_results[name] = {
            "rmse_mean": float(fold_rmse.mean()),
            "rmse_std": float(fold_rmse.std(ddof=1)),
        }

    selected_name = min(cv_results, key=lambda name: cv_results[name]["rmse_mean"])
    selected_model = clone(candidates[selected_name])
    selected_model.fit(X_train, y_train)
    return selected_name, selected_model, cv_results


def run_experiment(
    output_dir: Path,
    random_state: int = RANDOM_STATE,
) -> dict[str, Any]:
    X_train, X_test, y_train, y_test = load_and_split(random_state)
    selected_name, selected_model, cv_results = select_model(
        X_train,
        y_train,
        random_state,
    )

    prediction = selected_model.predict(X_test)
    metrics: dict[str, Any] = {
        "dataset": "sklearn.datasets.load_diabetes",
        "random_state": random_state,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "selected_model": selected_name,
        "selection_source": "training-only nested cross-validation",
        "test_evaluations": 1,
        "cv": cv_results,
        "test": {
            "rmse": float(root_mean_squared_error(y_test, prediction)),
            "mae": float(mean_absolute_error(y_test, prediction)),
            "r2": float(r2_score(y_test, prediction)),
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    pd.DataFrame(
        {
            "row_id": y_test.index,
            "actual": y_test.to_numpy(),
            "prediction": prediction,
            "residual": y_test.to_numpy() - prediction,
        }
    ).to_csv(output_dir / "predictions.csv", index=False)
    return metrics


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Run the regression capstone baseline.")
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "artifacts",
        help="Directory for metrics.json and predictions.csv.",
    )
    parser.add_argument("--random-state", type=int, default=RANDOM_STATE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = run_experiment(args.output, args.random_state)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

