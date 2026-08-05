from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from tree_baseline import evaluate_tree_baseline, make_demo_data, run_pipeline


class TreeBaselineTests(unittest.TestCase):
    def test_splits_are_chronological_and_disjoint(self):
        result = evaluate_tree_baseline(make_demo_data(500, seed=7))
        train = result["train_slice"]
        validation = result["validation_slice"]
        test = result["test_slice"]
        self.assertEqual(train.stop, validation.start)
        self.assertEqual(validation.stop, test.start)
        self.assertGreater(test.stop - test.start, 0)

    def test_test_target_mutation_does_not_change_model_selection(self):
        data = make_demo_data(500, seed=5)
        changed = data.copy()
        test_start = 400
        changed.loc[test_start:, "target"] *= 100.0
        first = evaluate_tree_baseline(data)
        second = evaluate_tree_baseline(changed)
        self.assertEqual(first["test_slice"].start, test_start)
        self.assertEqual(first["selected_depth"], second["selected_depth"])
        self.assertEqual(
            first["model"].tree_.node_count,
            second["model"].tree_.node_count,
        )
        self.assertNotEqual(first["test_mse"], second["test_mse"])

    def test_tree_beats_mean_baseline_on_demo(self):
        result = evaluate_tree_baseline(make_demo_data(500, seed=42))
        self.assertLess(result["test_mse"], result["baseline_mse"])

    def test_pipeline_writes_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            metrics = run_pipeline(make_demo_data(200), output)
            self.assertTrue((output / "tree_metrics.json").is_file())
            self.assertTrue((output / "test_predictions.csv").is_file())
            saved = json.loads((output / "tree_metrics.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["test_observations"], 40)
            self.assertEqual(metrics["observations"], 200)


if __name__ == "__main__":
    unittest.main()

