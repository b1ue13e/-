from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from pandas.testing import assert_frame_equal

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from dynamic_var import evaluate_dynamic_var, make_demo_data, run_pipeline


class DynamicVarTests(unittest.TestCase):
    def test_future_mutation_does_not_rewrite_earlier_forecasts(self):
        data = make_demo_data(observations=500, seed=7)
        changed = data.copy()
        cutoff = 450
        changed.loc[cutoff:, "return"] *= 10.0
        first = evaluate_dynamic_var(data, train_fraction=0.8)
        second = evaluate_dynamic_var(changed, train_fraction=0.8)
        rows_before_cutoff = cutoff - first["split"]
        self.assertGreater(rows_before_cutoff, 0)
        columns = ["normal_var", "historical_var"]
        assert_frame_equal(
            first["forecasts"].iloc[:rows_before_cutoff][columns],
            second["forecasts"].iloc[:rows_before_cutoff][columns],
        )

    def test_forecasts_are_nonnegative_and_aligned(self):
        result = evaluate_dynamic_var(make_demo_data(500), train_fraction=0.8)
        forecasts = result["forecasts"]
        self.assertEqual(len(forecasts), 100)
        self.assertTrue((forecasts[["normal_var", "historical_var"]] >= 0).all().all())
        self.assertEqual(result["normal_kupiec"]["observations"], 100)

    def test_invalid_confidence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "confidence"):
            evaluate_dynamic_var(make_demo_data(200), confidence=1.0)

    def test_pipeline_writes_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            metrics = run_pipeline(make_demo_data(300), output)
            self.assertTrue((output / "var_metrics.json").is_file())
            self.assertTrue((output / "var_forecasts.csv").is_file())
            saved = json.loads((output / "var_metrics.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["test_observations"], 60)
            self.assertEqual(metrics["window"], 60)


if __name__ == "__main__":
    unittest.main()

