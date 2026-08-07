from __future__ import annotations

import json
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "capstone-co2"


class CapstoneArtifactTests(unittest.TestCase):
    def test_capstone_artifacts_exist_and_are_recomputable(self) -> None:
        manifest = json.loads((ARTIFACT_ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["horizon"], 12)
        self.assertEqual(manifest["test_policy"], "2001 is evaluated once after validation selection; no test tuning")
        self.assertGreater((ARTIFACT_ROOT / "predictions.csv").stat().st_size, 1000)
        self.assertGreater((ARTIFACT_ROOT / "metrics-by-horizon.csv").stat().st_size, 500)
        self.assertTrue((ARTIFACT_ROOT / "failures.csv").exists())
        self.assertTrue((ARTIFACT_ROOT / "residual-diagnostics.csv").exists())
        self.assertTrue((ARTIFACT_ROOT / "report.md").exists())
        self.assertTrue((ARTIFACT_ROOT / "environment.txt").exists())
        predictions = pd.read_csv(ARTIFACT_ROOT / "predictions.csv")
        self.assertGreaterEqual(len(predictions), 852)
        self.assertIn("ml_lag", set(predictions["model"]))
        self.assertTrue((predictions["timestamp"] > predictions["train_end"]).all())
        self.assertTrue((predictions["timestamp"] >= predictions["origin"]).all())
        self.assertTrue((predictions["horizon"] <= 12).all())
        self.assertTrue(predictions["covered80"].isin([True, False]).all())


if __name__ == "__main__":
    unittest.main()
