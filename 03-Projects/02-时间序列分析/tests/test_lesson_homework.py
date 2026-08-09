from __future__ import annotations

import importlib.util
import json
import re
import unittest
import warnings
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HOMEWORK_ROOT = PROJECT_ROOT / "课后作业"
FIXTURE_ROOT = PROJECT_ROOT / "artifacts" / "homework-fixtures"


def load_frontmatter(path: Path) -> dict[str, object]:
    import yaml

    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise AssertionError(f"missing frontmatter: {path}")
    return yaml.safe_load(match.group(1))


class LessonHomeworkTests(unittest.TestCase):
    def test_all_lesson_homework_meets_detail_contract(self) -> None:
        paths = sorted(HOMEWORK_ROOT.glob("*.md"))
        self.assertEqual(len(paths), 7)
        self.assertEqual(
            {load_frontmatter(path)["assignment_id"] for path in paths},
            {f"时间序列分析-{number:02d}" for number in range(7)},
        )
        required_sections = ("作业定位", "学习目标", "任务边界", "必要提示", "提交产物", "Rubric", "提交前自检与复盘", "来源说明")
        for path in paths:
            text = path.read_text(encoding="utf-8-sig")
            fields = load_frontmatter(path)
            self.assertEqual(fields["assignment_level"], "lesson", path)
            self.assertEqual(fields["assignment_format"], "lab", path)
            self.assertEqual(fields["source_type"], "local_integration_task", path)
            self.assertEqual(str(fields["updated"]), "2026-08-07", path)
            self.assertTrue(fields["requires"], path)
            self.assertIn("link-only", fields["license"], path)
            self.assertIn("estimated_time", fields, path)
            self.assertIn("通过线 80/100", text, path)
            self.assertRegex(text, r"(?m)^## 常见", path)
            for section in required_sections:
                self.assertRegex(text, rf"(?m)^## {re.escape(section)}", path)
            headings = re.findall(r"^## (.+)$", text, re.MULTILINE)
            self.assertEqual(len(headings), len(set(headings)), path)
            questions = re.findall(r"^### Q(\d+).*?（(\d+) 分）$", text, re.MULTILINE)
            self.assertTrue(questions, path)
            self.assertEqual([int(number) for number, _ in questions], list(range(1, len(questions) + 1)), path)
            self.assertEqual(sum(int(points) for _, points in questions), 100, path)
            self.assertNotRegex(path.name, r"李宏毅|4-Tier|Boss|阶梯")

    def test_fixture_builder_is_deterministic_and_matches_manifest(self) -> None:
        path = PROJECT_ROOT / "scripts" / "build_lesson_homework_fixtures.py"
        spec = importlib.util.spec_from_file_location("build_lesson_homework_fixtures", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertEqual(module.main(), 0)
        first = {item.name: item.read_bytes() for item in FIXTURE_ROOT.iterdir() if item.is_file()}
        self.assertEqual(module.main(), 0)
        second = {item.name: item.read_bytes() for item in FIXTURE_ROOT.iterdir() if item.is_file()}
        self.assertEqual(first, second)

        manifest = json.loads((FIXTURE_ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["seed"], 20260807)
        self.assertEqual({details["rows"] for details in manifest["files"].values()}, {6, 144, 160, 240})

        hw00 = pd.read_csv(FIXTURE_ROOT / "hw00_observations.csv")
        self.assertEqual(int(hw00["date"].duplicated(keep=False).sum()), 2)
        self.assertEqual(int(hw00["value"].isna().sum()), 1)
        self.assertEqual(int((hw00["value"] == 0).sum()), 1)
        self.assertTrue((pd.to_datetime(hw00["published_at"]) > pd.Timestamp("2025-08-15")).any())

        hw01 = pd.read_csv(FIXTURE_ROOT / "hw01_structure_series.csv")
        self.assertEqual(hw01.shape, (160, 5))
        self.assertEqual(pd.infer_freq(pd.to_datetime(hw01["timestamp"])), "MS")

    def test_hw05_fixed_sarima_interface_runs(self) -> None:
        from statsmodels.tsa.arima.model import ARIMA

        frame = pd.read_csv(FIXTURE_ROOT / "hw05_monthly_series.csv", parse_dates=["timestamp"])
        train = frame.set_index("timestamp")["value"].iloc[:120]
        evaluation = frame.set_index("timestamp")["value"].iloc[120:]
        seasonal_naive = np.resize(train.iloc[-12:].to_numpy(), len(evaluation))
        self.assertEqual(len(seasonal_naive), 24)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fit = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n").fit()
        forecast = fit.get_forecast(steps=24)
        self.assertEqual(len(forecast.predicted_mean), 24)
        self.assertTrue(np.isfinite(np.asarray(forecast.predicted_mean)).all())

    def test_hw06_candidates_share_sample_and_diagnostics_run(self) -> None:
        from statsmodels.stats.diagnostic import acorr_ljungbox
        from statsmodels.tsa.arima.model import ARIMA

        values = pd.read_csv(FIXTURE_ROOT / "hw06_diagnostic_series.csv")["value"]
        for order in ((0, 0, 0), (1, 0, 0), (2, 0, 0)):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fit = ARIMA(values, order=order, trend="c").fit()
            self.assertEqual(int(fit.nobs), 240)
            diagnostics = acorr_ljungbox(fit.resid, lags=[6, 12], model_df=order[0] + order[2], return_df=True)
            self.assertEqual(list(diagnostics.index), [6, 12])
            self.assertTrue(np.isfinite(diagnostics["lb_stat"]).all())


if __name__ == "__main__":
    unittest.main()
