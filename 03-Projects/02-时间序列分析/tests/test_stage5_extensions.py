from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "stage5-extensions"
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "run_stage5_extensions.py"


def load_module():
    spec = importlib.util.spec_from_file_location("run_stage5_extensions", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class StageFiveExtensionTests(unittest.TestCase):
    def test_artifacts_follow_frozen_selection_protocol(self) -> None:
        manifest = json.loads((ARTIFACT_ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["source_observations"], 203)
        self.assertEqual(manifest["transformed_observations"], 198)
        self.assertEqual(manifest["license"], "public domain")
        self.assertEqual(manifest["forecast_horizon"], 1)
        self.assertEqual(manifest["validation_origins"], 16)
        self.assertEqual(manifest["test_origins"], 16)
        self.assertIn("complete every validation origin", manifest["selection_policy"])

        predictions = pd.read_csv(ARTIFACT_ROOT / "predictions.csv")
        validation = predictions.loc[predictions["split"] == "validation"]
        test = predictions.loc[predictions["split"] == "test"]
        self.assertEqual(len(validation), 16 * 6)
        self.assertEqual(set(validation["model"]), set(manifest["models"]))
        self.assertTrue((validation.groupby("model").size() == 16).all())
        self.assertEqual(len(test), 16 * len(manifest["final_test_models"]))
        self.assertEqual(set(test["model"]), set(manifest["final_test_models"]))

        timestamps = pd.PeriodIndex(predictions["timestamp"], freq="Q")
        train_ends = pd.PeriodIndex(predictions["train_end"], freq="Q")
        self.assertTrue((timestamps > train_ends).all())
        self.assertTrue(np.isfinite(predictions["y_pred"]).all())
        self.assertTrue((predictions["mase_scale"] > 0).all())

        selection = pd.read_csv(ARTIFACT_ROOT / "validation-model-selection.csv")
        selected = selection.loc[selection["selected"]]
        self.assertEqual(selected["model"].tolist(), [manifest["selected_on_validation"]])
        self.assertTrue(selection["eligible"].all())
        self.assertEqual(
            manifest["final_test_models"],
            list(dict.fromkeys(["naive", manifest["selected_on_validation"]])),
        )

        failures = pd.read_csv(ARTIFACT_ROOT / "failures.csv")
        self.assertTrue(failures.empty)
        availability = pd.read_csv(ARTIFACT_ROOT / "feature-availability.csv")
        self.assertTrue(availability["available_at_origin"].all())

    def test_metrics_are_recomputable_from_predictions(self) -> None:
        predictions = pd.read_csv(ARTIFACT_ROOT / "predictions.csv")
        metrics = pd.read_csv(ARTIFACT_ROOT / "metrics.csv")
        for row in metrics.itertuples(index=False):
            group = predictions.loc[
                (predictions["split"] == row.split) & (predictions["model"] == row.model)
            ]
            self.assertEqual(len(group), row.n_predictions)
            self.assertAlmostEqual(float(group["abs_error"].mean()), row.mae, places=10)
            self.assertAlmostEqual(
                float(np.sqrt(group["squared_error"].mean())),
                row.rmse,
                places=10,
            )
            self.assertAlmostEqual(float(group["scaled_error"].mean()), row.mase, places=10)

    def test_feature_timing_and_all_model_interfaces(self) -> None:
        module = load_module()
        frame = module.build_dataset()
        self.assertEqual(len(frame), 198)
        self.assertTrue(frame.index.is_monotonic_increasing)
        self.assertTrue(frame.index.is_unique)

        np.testing.assert_allclose(
            frame["gdp_growth_lag1"].iloc[1:].to_numpy(),
            frame["gdp_growth"].iloc[:-1].to_numpy(),
        )
        np.testing.assert_allclose(
            frame["cons_growth_lag1"].iloc[1:].to_numpy(),
            frame["cons_growth"].iloc[:-1].to_numpy(),
        )
        np.testing.assert_allclose(
            frame["inv_growth_lag1"].iloc[1:].to_numpy(),
            frame["inv_growth"].iloc[:-1].to_numpy(),
        )

        origin = len(frame) - 1
        predictions, failures, _ = module.evaluate(
            frame,
            range(origin, origin + 1),
            "smoke",
            module.MODEL_NAMES,
        )
        self.assertTrue(failures.empty, failures.to_dict("records"))
        self.assertEqual(set(predictions["model"]), set(module.MODEL_NAMES))
        self.assertEqual(len(predictions), len(module.MODEL_NAMES))

    def test_incomplete_validation_model_cannot_win(self) -> None:
        module = load_module()
        validation = pd.DataFrame(
            [
                {
                    "split": "validation",
                    "origin": origin,
                    "model": model,
                    "squared_error": 1.0 if model == "complete" else 0.01,
                }
                for model in ("complete", "incomplete")
                for origin in (["2000Q1", "2000Q2"] if model == "complete" else ["2000Q1"])
            ]
        )
        failures = pd.DataFrame(
            [
                {
                    "split": "validation",
                    "origin": "2000Q2",
                    "model": "incomplete",
                    "error_type": "RuntimeError",
                    "message": "missing origin",
                }
            ]
        )
        selected, selection = module.select_model(
            validation,
            failures,
            ["complete", "incomplete"],
            expected_origins=2,
        )
        self.assertEqual(selected, "complete")
        self.assertFalse(
            bool(selection.loc[selection["model"] == "incomplete", "eligible"].iloc[0])
        )


if __name__ == "__main__":
    unittest.main()
