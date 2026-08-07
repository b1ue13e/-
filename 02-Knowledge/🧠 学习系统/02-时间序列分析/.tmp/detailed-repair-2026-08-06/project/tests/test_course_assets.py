from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = REPO_ROOT / "02-Knowledge" / "🧠 学习系统" / "02-时间序列分析"
PROJECT_ROOT = REPO_ROOT / "03-Projects" / "02-时间序列分析"


class CourseAssetTests(unittest.TestCase):
    def test_audit_script_passes(self) -> None:
        path = PROJECT_ROOT / "scripts" / "audit_course.py"
        spec = importlib.util.spec_from_file_location("audit_course", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertEqual(module.COURSE_ROOT, COURSE_ROOT)
        self.assertGreaterEqual(len(module.markdown_files(module.COURSE_ROOT)), 80)
        self.assertEqual(module.main(), 0)

    def test_frontmatter_is_parseable_yaml(self) -> None:
        try:
            import yaml
        except ImportError as error:
            self.skipTest(f"PyYAML unavailable: {error}")
        for root in (COURSE_ROOT, PROJECT_ROOT):
            for path in root.rglob("*.md"):
                if ".tmp" in path.parts or ".reasonix" in path.parts:
                    continue
                text = path.read_text(encoding="utf-8-sig")
                match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
                self.assertIsNotNone(match, path)
                data = yaml.safe_load(match.group(1))
                self.assertIsInstance(data, dict, path)

    def test_prerequisite_examples(self) -> None:
        import numpy as np
        import pandas as pd

        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2025-02-01", "2025-01-01", "2025-03-01"]),
                "value": [12.0, 10.0, float("nan")],
            }
        ).sort_values("date")
        self.assertTrue(frame["date"].is_monotonic_increasing)
        self.assertEqual(int(frame["value"].isna().sum()), 1)

        values = np.array([1.0, 2.0, 3.0])
        doubled = np.array([2.0, 4.0, 6.0])
        self.assertTrue(np.isclose(np.var(values, ddof=1), 1.0))
        self.assertTrue(np.isclose(np.corrcoef(values, doubled)[0, 1], 1.0))

        design = np.array([[1.0, 2.0], [3.0, 4.0]])
        coefficients = np.array([5.0, 6.0])
        self.assertTrue(np.allclose(design @ coefficients, [17.0, 39.0]))

    def test_arima_interface_example(self) -> None:
        import numpy as np
        from statsmodels.tsa.arima.model import ARIMA

        random = np.random.default_rng(7)
        values = np.cumsum(random.normal(size=160))
        train, test = values[:140], values[140:]
        fit = ARIMA(train, order=(0, 1, 0), trend="n").fit()
        forecast = fit.get_forecast(steps=len(test))
        self.assertEqual(len(forecast.predicted_mean), len(test))
        self.assertEqual(forecast.conf_int(alpha=0.05).shape, (len(test), 2))

    def test_rolling_forecast_has_no_future_access(self) -> None:
        import numpy as np
        from statsmodels.tsa.ar_model import AutoReg

        random = np.random.default_rng(20260805)
        time = np.arange(72)
        values = 50 + 0.04 * time + 4 * np.sin(2 * np.pi * time / 12) + random.normal(0, 1.2, 72)
        predictions: list[float] = []
        truths: list[float] = []
        for origin in range(48, 72):
            train = values[:origin]
            self.assertEqual(len(train), origin)
            fit = AutoReg(train, lags=[1, 12], trend="ct", old_names=False).fit()
            predictions.append(float(fit.predict(start=origin, end=origin)[0]))
            truths.append(float(values[origin]))
        self.assertEqual(len(predictions), 24)
        self.assertTrue(np.isfinite(np.mean(np.abs(np.asarray(truths) - predictions))))


if __name__ == "__main__":
    unittest.main()
