from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from capm_lab import fit_capm, make_demo_data, run_pipeline


class CapmLabTests(unittest.TestCase):
    def test_fit_recovers_synthetic_beta(self):
        data = make_demo_data(observations=1_000, seed=7)
        fit = fit_capm(data["asset_return"], data["market_return"])
        self.assertAlmostEqual(fit.beta, 1.2, delta=0.08)
        self.assertGreater(fit.beta_se, 0.0)
        self.assertTrue(np.isfinite(fit.alpha_t))

    def test_future_mutation_does_not_change_training_fit(self):
        data = make_demo_data(observations=200, seed=5)
        cutoff = 150
        changed = data.copy()
        changed.loc[cutoff:, "asset_return"] *= 10.0
        with tempfile.TemporaryDirectory() as first_tmp, tempfile.TemporaryDirectory() as second_tmp:
            first = run_pipeline(data, Path(first_tmp), train_fraction=0.75)
            second = run_pipeline(changed, Path(second_tmp), train_fraction=0.75)
            self.assertEqual(first["train_observations"], cutoff)
            self.assertAlmostEqual(first["alpha"], second["alpha"], places=12)
            self.assertAlmostEqual(first["beta"], second["beta"], places=12)

    def test_pipeline_writes_metrics_and_predictions(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            metrics = run_pipeline(make_demo_data(100), output)
            self.assertTrue((output / "metrics.json").is_file())
            self.assertTrue((output / "test_predictions.csv").is_file())
            saved = json.loads((output / "metrics.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["test_observations"], 20)
            self.assertEqual(metrics["observations"], 100)

    def test_rank_deficient_market_is_rejected(self):
        data = make_demo_data(40)
        data["market_return"] = 0.0
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "no variation"):
                run_pipeline(data, Path(tmp))


if __name__ == "__main__":
    unittest.main()
