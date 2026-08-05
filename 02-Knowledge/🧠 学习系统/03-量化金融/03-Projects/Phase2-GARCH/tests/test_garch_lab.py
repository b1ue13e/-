from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from garch_lab import GarchFit, evaluate_out_of_sample, fit_garch, run_pipeline, simulate_garch


class GarchLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.returns, cls.true_variance = simulate_garch(observations=1_000, seed=7)

    def test_fit_respects_garch_constraints(self):
        fit = fit_garch(self.returns[:800])
        self.assertTrue(fit.success, fit.message)
        self.assertGreater(fit.omega, 0.0)
        self.assertGreaterEqual(fit.alpha, 0.0)
        self.assertGreaterEqual(fit.beta, 0.0)
        self.assertLess(fit.alpha + fit.beta, 1.0)
        self.assertTrue(np.all(fit.conditional_variance > 0.0))

    def test_future_mutation_does_not_change_training_fit(self):
        cutoff = 800
        changed = self.returns.copy()
        changed[cutoff:] *= 5.0
        dates = pd.date_range("2020-01-01", periods=len(self.returns), freq="D")
        first = evaluate_out_of_sample(self.returns, dates=dates)
        second = evaluate_out_of_sample(changed, dates=dates)
        self.assertEqual(len(first["test_returns"]), len(self.returns) - cutoff)
        self.assertGreater(len(first["test_returns"]), 0)
        self.assertAlmostEqual(first["fit"].omega, second["fit"].omega, places=12)
        self.assertAlmostEqual(first["fit"].alpha, second["fit"].alpha, places=12)
        self.assertAlmostEqual(first["fit"].beta, second["fit"].beta, places=12)
        self.assertAlmostEqual(
            first["garch_forecasts"][0], second["garch_forecasts"][0], places=12
        )
        self.assertNotEqual(first["test_returns"][0], second["test_returns"][0])

    def test_optimizer_failure_blocks_evaluation(self):
        failed_fit = GarchFit(
            omega=0.1,
            alpha=0.1,
            beta=0.8,
            success=False,
            message="synthetic failure",
            negative_log_likelihood=0.0,
            conditional_variance=np.ones(800),
        )
        with patch("garch_lab.fit_garch", return_value=failed_fit):
            with self.assertRaisesRegex(RuntimeError, "optimizer failed"):
                evaluate_out_of_sample(self.returns)

    def test_out_of_sample_forecasts_are_positive_and_aligned(self):
        result = evaluate_out_of_sample(self.returns, train_fraction=0.8, rolling_window=20)
        expected = len(self.returns) - int(len(self.returns) * 0.8)
        self.assertEqual(len(result["garch_forecasts"]), expected)
        self.assertEqual(len(result["rolling_forecasts"]), expected)
        self.assertTrue(np.all(result["garch_forecasts"] > 0.0))
        self.assertTrue(np.isfinite(result["garch_qlike"]))
        self.assertTrue(np.isfinite(result["rolling_qlike"]))

    def test_pipeline_writes_metrics_and_forecasts(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            metrics = run_pipeline(
                self.returns,
                output,
                train_fraction=0.8,
                rolling_window=20,
                data_mode="test_simulation",
                dates=pd.date_range("2020-01-01", periods=len(self.returns), freq="D"),
            )
            metrics_path = output / "phase2_metrics.json"
            forecasts_path = output / "phase2_forecasts.csv"
            self.assertTrue(metrics_path.is_file())
            self.assertTrue(forecasts_path.is_file())
            saved = json.loads(metrics_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["test_observations"], 200)
            self.assertEqual(metrics["data_mode"], "test_simulation")
            self.assertTrue(forecasts_path.read_text(encoding="utf-8").startswith("date,"))


if __name__ == "__main__":
    unittest.main()
