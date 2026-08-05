from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from pandas.testing import assert_series_equal

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from phase1_baseline import build_baseline, make_demo_prices, run_pipeline


class Phase1BaselineTests(unittest.TestCase):
    def test_position_is_previous_period_signal(self) -> None:
        frame, _ = build_baseline(make_demo_prices(40), fast_window=2, slow_window=5)
        expected = frame["signal"].shift(1).fillna(0.0)
        assert_series_equal(frame["position"], expected, check_names=False)

    def test_future_price_does_not_rewrite_past_results(self) -> None:
        original = make_demo_prices(40)
        changed = original.copy()
        cutoff = 30
        changed.loc[changed.index[cutoff]:, "adj_close"] *= 2.0

        first, _ = build_baseline(original, fast_window=2, slow_window=5)
        second, _ = build_baseline(changed, fast_window=2, slow_window=5)

        past_first = first.iloc[:cutoff]["strategy_return"]
        past_second = second.iloc[:cutoff]["strategy_return"]
        self.assertEqual(len(past_first), cutoff)
        self.assertGreater(len(past_first), 0)
        assert_series_equal(
            past_first,
            past_second,
        )

    def test_duplicate_date_is_rejected(self) -> None:
        data = make_demo_prices(20)
        data.loc[1, "date"] = data.loc[0, "date"]
        with self.assertRaisesRegex(ValueError, "date must be unique"):
            build_baseline(data, fast_window=2, slow_window=5)

    def test_pipeline_writes_expected_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            metrics = run_pipeline(make_demo_prices(40), output, 2, 5, 10.0)
            self.assertTrue((output / "metrics.json").is_file())
            self.assertTrue((output / "equity_curve.csv").is_file())
            self.assertEqual(metrics["observations"], 40)


if __name__ == "__main__":
    unittest.main()
