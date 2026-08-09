import unittest

from scripts.run_eval import load_cases, run_evaluation


class CourseEvaluationTests(unittest.TestCase):
    def test_dataset_has_required_20_10_10_splits(self) -> None:
        cases = load_cases()
        self.assertEqual(len(cases), 40)
        self.assertEqual(sum(case["split"] == "normal" for case in cases), 20)
        self.assertEqual(sum(case["split"] == "abnormal" for case in cases), 10)
        self.assertEqual(sum(case["split"] == "adversarial" for case in cases), 10)

    def test_full_offline_evaluation_gate_passes(self) -> None:
        report = run_evaluation(load_cases())
        self.assertTrue(report["gate_passed"])
        self.assertEqual(report["metrics"]["TSR"], 1.0)
        self.assertEqual(report["metrics"]["abnormal_fail_closed_rate"], 1.0)
        self.assertEqual(report["metrics"]["ASR"], 0.0)
        self.assertEqual(report["metrics"]["ToolAcc"], 1.0)


if __name__ == "__main__":
    unittest.main()
