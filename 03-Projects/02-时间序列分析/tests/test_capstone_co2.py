from __future__ import annotations

import json
import importlib.util
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "capstone-co2"


class CapstoneArtifactTests(unittest.TestCase):
    def test_capstone_artifacts_exist_and_are_recomputable(self) -> None:
        manifest = json.loads((ARTIFACT_ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["horizon"], 12)
        self.assertEqual(manifest["source_url"], "https://www.statsmodels.org/stable/datasets/generated/co2.html")
        self.assertIn("Selection is frozen before", manifest["test_policy"])
        self.assertEqual(manifest["final_test_models"], ["naive", "seasonal_naive", "ets"])
        self.assertGreater((ARTIFACT_ROOT / "predictions.csv").stat().st_size, 1000)
        self.assertGreater((ARTIFACT_ROOT / "metrics-by-horizon.csv").stat().st_size, 500)
        self.assertTrue((ARTIFACT_ROOT / "failures.csv").exists())
        self.assertTrue((ARTIFACT_ROOT / "warnings.csv").exists())
        self.assertTrue((ARTIFACT_ROOT / "residual-diagnostics.csv").exists())
        self.assertTrue((ARTIFACT_ROOT / "report.md").exists())
        self.assertTrue((ARTIFACT_ROOT / "environment.txt").exists())
        predictions = pd.read_csv(ARTIFACT_ROOT / "predictions.csv")
        self.assertGreaterEqual(len(predictions), 1000)
        self.assertIn("ml_lag", set(predictions["model"]))
        self.assertTrue((predictions["timestamp"] > predictions["train_end"]).all())
        self.assertTrue((predictions["timestamp"] >= predictions["origin"]).all())
        self.assertTrue((predictions["horizon"] <= 12).all())
        self.assertTrue(predictions["covered80"].isin([True, False]).all())
        test_models = set(predictions.loc[predictions["split"] == "test", "model"])
        self.assertEqual(test_models, set(manifest["final_test_models"]))

        selection = pd.read_csv(ARTIFACT_ROOT / "validation-model-selection.csv")
        selected = selection.loc[selection["selected"]]
        self.assertEqual(selected["model"].tolist(), [manifest["selected_on_validation"]])
        self.assertTrue(selected["eligible"].all())
        arima = selection.loc[selection["model"] == "arima"].iloc[0]
        self.assertFalse(bool(arima["eligible"]))
        self.assertGreaterEqual(int(arima["failure_count"]), 1)
        self.assertLess(int(arima["prediction_count"]), int(arima["expected_prediction_count"]))

    def test_incomplete_validation_model_is_not_selectable(self) -> None:
        script = PROJECT_ROOT / "scripts" / "run_capstone_co2.py"
        spec = importlib.util.spec_from_file_location("run_capstone_co2", script)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)

        rows = []
        for model in ("complete", "incomplete"):
            origins = ("2025-01-01", "2025-02-01") if model == "complete" else ("2025-01-01",)
            for origin in origins:
                for horizon in (1, 2):
                    rows.append({
                        "split": "validation",
                        "origin": origin,
                        "model": model,
                        "horizon": horizon,
                        "error": 1.0 if model == "complete" else 0.01,
                        "covered80": True,
                        "covered95": True,
                        "lower80": 0.0,
                        "upper80": 1.0,
                        "lower95": 0.0,
                        "upper95": 1.0,
                    })
        validation = pd.DataFrame(rows)
        failures = pd.DataFrame([{"model": "incomplete", "origin": "2025-02-01"}])
        selected, selection = module.select_model(validation, failures, ["complete", "incomplete"], 2, 2)
        self.assertEqual(selected, "complete")
        self.assertFalse(bool(selection.loc[selection["model"] == "incomplete", "eligible"].iloc[0]))


if __name__ == "__main__":
    unittest.main()
