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
    def test_course_cards_have_assessment_contract(self) -> None:
        cards = []
        for path in COURSE_ROOT.rglob("*.md"):
            if ".tmp" in path.parts or ".reasonix" in path.parts:
                continue
            text = path.read_text(encoding="utf-8-sig")
            if re.search(r"^type:\s*study\s*$", text, re.MULTILINE):
                cards.append((path, text))
        self.assertEqual(len(cards), 69)
        for path, text in cards:
            self.assertIn("## 学完后可以完成", text, path)
            self.assertEqual(text.count("## 学完后可以完成"), 1, path)
            self.assertIn("WHERE contains(upstream, this.file.link)", text, path)
            self.assertIn("WHERE contains(requires, this.file.link)", text, path)
            if "otexts.com" in text:
                self.assertNotIn('license: "CC BY-NC-SA 4.0"', text, path)
                self.assertNotIn("official-free", text, path)
                self.assertNotIn("正文再分发边界待核验", text, path)
                self.assertIn("link-only", text, path)
            self.assertNotRegex(text, r"主卡：\[\[([^\]]+)\]\]｜本卡为深挖细节版", path)
            self.assertNotRegex(text, r"(?:AR|MA|ARMA)\(\([A-Za-z,]+\)\)", path)

    def test_stage_two_canonical_cards_replace_deep_note_files(self) -> None:
        stage_root = COURSE_ROOT / "02-平稳性与相关结构"
        migrations = {
            "PACF（深挖笔记）.md": "时间序列分析-偏自相关函数PACF.md",
            "随机游走（深挖笔记）.md": "时间序列分析-随机游走.md",
            "趋势平稳与差分平稳（深挖笔记）.md": "时间序列分析-趋势平稳与差分平稳.md",
        }
        active_text = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for path in COURSE_ROOT.rglob("*.md")
            if ".tmp" not in path.parts and ".reasonix" not in path.parts
        )
        for old_name, canonical_name in migrations.items():
            self.assertFalse((stage_root / old_name).exists(), old_name)
            canonical = stage_root / canonical_name
            self.assertTrue(canonical.exists(), canonical)
            text = canonical.read_text(encoding="utf-8-sig")
            self.assertIn(old_name.removesuffix(".md"), text, canonical)
            self.assertNotIn(f"[[{old_name.removesuffix('.md')}", active_text)

        concise_cards = [
            "平稳性.md",
            "平稳性与ACF-PACF.md",
            "自相关函数ACF.md",
            "白噪声.md",
            *migrations.values(),
        ]
        legacy_markers = (
            "给 Obsidian 的归档建议",
            "A 类知识点，必须深挖",
            "_（在此填写）_",
            "期末必考",
            "照妖镜",
            "金句",
        )
        for name in concise_cards:
            path = stage_root / name
            text = path.read_text(encoding="utf-8-sig")
            self.assertLess(len(text), 6000, path)
            for marker in legacy_markers:
                self.assertNotIn(marker, text, path)

    def test_stage_three_and_four_cards_are_concise_and_canonical(self) -> None:
        stage_three = COURSE_ROOT / "03-经典预测模型"
        stage_four = COURSE_ROOT / "04-识别诊断与评估"
        canonical_cards = [
            stage_three / "AR模型.md",
            stage_three / "MA模型.md",
            stage_three / "ARMA模型.md",
            stage_three / "差分运算.md",
            stage_four / "时间序列分析-Ljung-Box检验.md",
            stage_four / "时间序列分析-Box-Pierce检验.md",
        ]
        for path in canonical_cards:
            self.assertTrue(path.exists(), path)
            text = path.read_text(encoding="utf-8-sig")
            self.assertLess(len(text), 6000, path)
            self.assertIn("## 闭卷检索", text, path)
            self.assertNotIn("给 Obsidian 的归档建议", text, path)
            self.assertNotIn("_（在此填写）_", text, path)

        active_paths = [
            path
            for path in COURSE_ROOT.rglob("*.md")
            if ".tmp" not in path.parts and ".reasonix" not in path.parts
        ]
        self.assertFalse(
            [path for path in active_paths if "深挖笔记" in path.name],
            "活动课程不应再用历史深挖标签命名文件",
        )
        active_text = "\n".join(path.read_text(encoding="utf-8-sig") for path in active_paths)
        self.assertNotIn("[[Ljung-Box 检验（深挖笔记）", active_text)
        self.assertNotIn("[[Box-Pierce 检验（深挖笔记）", active_text)

    def test_rewritten_model_examples_match_theory(self) -> None:
        import numpy as np
        from statsmodels.stats.diagnostic import acorr_ljungbox
        from statsmodels.tsa.arima.model import ARIMA
        from statsmodels.tsa.arima_process import ArmaProcess
        from statsmodels.tsa.stattools import acf

        random = np.random.default_rng(42)
        innovations = random.normal(size=1200)
        ar_values = np.zeros_like(innovations)
        phi = -0.7
        for position in range(1, len(ar_values)):
            ar_values[position] = phi * ar_values[position - 1] + innovations[position]
        ar_acf = acf(ar_values, nlags=6, fft=True)
        self.assertLess(float(np.max(np.abs(ar_acf - phi ** np.arange(7)))), 0.08)

        random = np.random.default_rng(42)
        ma_values = ArmaProcess(ar=[1], ma=[1, 0.7]).generate_sample(
            nsample=1200,
            distrvs=random.normal,
        )
        ma_acf = acf(ma_values, nlags=6, fft=True)
        self.assertAlmostEqual(float(ma_acf[1]), 0.7 / (1 + 0.7**2), delta=0.08)
        self.assertLess(float(np.max(np.abs(ma_acf[2:]))), 0.1)

        random = np.random.default_rng(42)
        arma_values = ArmaProcess(ar=[1, -0.65], ma=[1, 0.4]).generate_sample(
            nsample=700,
            distrvs=random.normal,
        )
        fit = ARIMA(arma_values, order=(1, 0, 1), trend="n").fit()
        self.assertTrue(fit.mle_retvals.get("converged"))

        white = random.normal(size=20000)
        differenced = np.diff(white)
        rho1 = np.corrcoef(differenced[1:], differenced[:-1])[0, 1]
        self.assertAlmostEqual(float(rho1), -0.5, delta=0.03)

        diagnostics = acorr_ljungbox(
            random.normal(size=500),
            lags=[6, 12],
            boxpierce=True,
            return_df=True,
        )
        self.assertEqual(
            list(diagnostics.columns),
            ["lb_stat", "lb_pvalue", "bp_stat", "bp_pvalue"],
        )

    def test_markdown_tables_and_fences_are_structurally_sound(self) -> None:
        for root in (COURSE_ROOT, PROJECT_ROOT):
            for path in root.rglob("*.md"):
                if ".tmp" in path.parts or ".reasonix" in path.parts:
                    continue
                text = path.read_text(encoding="utf-8-sig")
                fences = re.findall(r"(?m)^\s*>?\s*(```|~~~)", text)
                self.assertEqual(fences.count("```") % 2, 0, path)
                self.assertEqual(fences.count("~~~") % 2, 0, path)

                table_width: int | None = None
                for line_number, line in enumerate(text.splitlines(), start=1):
                    stripped = line.strip()
                    if not stripped.startswith("|"):
                        table_width = None
                        continue
                    self.assertNotRegex(
                        stripped,
                        r"\[\[[^\]\n]*?(?<!\\)\|[^\]\n]*?\]\]",
                        f"{path}:{line_number}",
                    )
                    width = len(re.split(r"(?<!\\)\|", stripped)) - 2
                    if table_width is None:
                        table_width = width
                    else:
                        self.assertEqual(width, table_width, f"{path}:{line_number}")

    def test_unit_root_has_one_canonical_topic_card(self) -> None:
        stage_root = COURSE_ROOT / "02-平稳性与相关结构"
        self.assertTrue((stage_root / "单位根检验-ADF-KPSS.md").exists())
        self.assertFalse((stage_root / "单位根检验.md").exists())
        active_text = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for path in COURSE_ROOT.rglob("*.md")
            if ".tmp" not in path.parts and ".reasonix" not in path.parts
        )
        self.assertNotRegex(active_text, r"\[\[单位根检验(?:\||\]\])")

    def test_stage_mocs_have_review_nodes(self) -> None:
        stage_mocs = []
        for path in COURSE_ROOT.rglob("*.md"):
            if ".tmp" in path.parts or ".reasonix" in path.parts:
                continue
            text = path.read_text(encoding="utf-8-sig")
            if path.name.startswith("🧭 阶段") and re.search(r"^type:\s*index\s*$", text, re.MULTILINE) and re.search(r"^stage_id:\s*", text, re.MULTILINE):
                stage_mocs.append(path)
        self.assertEqual(len(stage_mocs), 6)
        for path in stage_mocs:
            text = path.read_text(encoding="utf-8-sig")
            self.assertIn("## 阶段验收与作业", text, path)
            self.assertRegex(text, r"复习与回顾", path)

    def test_navigation_queries_and_assignment_views_are_structurally_complete(self) -> None:
        stage_mocs = sorted(
            path for path in COURSE_ROOT.rglob("🧭 阶段*.md")
            if ".tmp" not in path.parts and ".reasonix" not in path.parts
        )
        self.assertEqual(len(stage_mocs), 6)
        for path in stage_mocs:
            text = path.read_text(encoding="utf-8-sig")
            stage_match = re.search(r'^stage_id:\s*"(\d+)"$', text, re.MULTILINE)
            self.assertIsNotNone(stage_match, path)
            stage_id = stage_match.group(1)
            self.assertIn('FROM "03-Projects/02-时间序列分析"', text, path)
            self.assertRegex(text, rf'WHERE stage_id = "{stage_id}"', path)
            self.assertNotRegex(text, r'WHERE\s+stage_id\s*=.*\s+OR\s+assignment_level\s*=\s*"capstone"', path)
        assignment_index = (PROJECT_ROOT / "🧭 课程作业总索引.md").read_text(encoding="utf-8-sig")
        for directory, level in (("课后作业", "lesson"), ("阶段作业", "stage"), ("大作业", "capstone")):
            self.assertIn(f'FROM "03-Projects/02-时间序列分析/{directory}"', assignment_index)
            self.assertIn(f'assignment_level = "{level}"', assignment_index)

    def test_stage_five_is_branch_based_and_capstone_has_no_hidden_hw(self) -> None:
        stage = (COURSE_ROOT / "05-多变量与现代扩展" / "🧭 阶段5-多变量与现代扩展.md").read_text(encoding="utf-8-sig")
        self.assertIn("完成共同核心后只选择一个分支", stage)
        self.assertIn("不要求把三个分支全部完成", stage)
        self.assertIn("时间序列分析-阶段作业-05-动态回归与信息边界", stage)
        self.assertIn("artifacts/stage5-extensions/", stage)

        stage_assignment = (PROJECT_ROOT / "阶段作业" / "时间序列分析-阶段作业-05-动态回归与信息边界.md").read_text(encoding="utf-8-sig")
        self.assertIn('assignment_id: "TS-ST05"', stage_assignment)
        self.assertIn('stage_id: "05"', stage_assignment)
        self.assertIn("https://www.statsmodels.org/stable/datasets/generated/macrodata.html", stage_assignment)
        self.assertIn("test 只运行 naïve 与验证期冻结胜者", stage_assignment)
        self.assertIn("## 100 分 Rubric", stage_assignment)

        capstone = (PROJECT_ROOT / "大作业" / "时间序列分析-大作业-漂移监控扩展.md").read_text(encoding="utf-8-sig")
        self.assertNotRegex(capstone, r"\bHW\d{2}\b")
        self.assertIn("PSI、KS 检验或特征分布监控只作为可选扩展", capstone)
        self.assertIn("## 100 分 Rubric", capstone)

    def test_stage_five_core_cards_are_concise_and_executable(self) -> None:
        stage_root = COURSE_ROOT / "05-多变量与现代扩展"
        cards = {
            "动态回归与ARIMAX.md": (
                "https://otexts.com/fpp3/dynamic.html",
                "https://online.stat.psu.edu/stat510/Lesson08",
                "validation 冻结胜者",
            ),
            "时序特征工程与ML预测.md": (
                "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
                "plot_time_series_lagged_features.html",
                "shift",
            ),
            "向量自回归VAR.md": (
                "https://online.stat.psu.edu/stat510/Lesson11",
                "statsmodels.tsa.vector_ar.var_model.VAR.html",
                "伴随矩阵",
            ),
            "状态空间模型与Kalman滤波.md": (
                "https://www.statsmodels.org/stable/statespace.html",
                "statsmodels.tsa.statespace.structural.UnobservedComponents.html",
                "filtered-states.csv",
            ),
        }
        legacy_markers = (
            "给 Obsidian 的归档建议",
            "我的主动回忆区",
            "## 0. 学习边界",
            "_（在此填写）_",
        )
        for name, required_markers in cards.items():
            path = stage_root / name
            self.assertTrue(path.exists(), path)
            text = path.read_text(encoding="utf-8-sig")
            self.assertLess(len(text), 6000, path)
            self.assertIn("## 学完后可以完成", text, path)
            for marker in required_markers:
                self.assertIn(marker, text, path)
            for marker in legacy_markers:
                self.assertNotIn(marker, text, path)

    def test_garch_uses_precise_official_source(self) -> None:
        card = (COURSE_ROOT / "04-识别诊断与评估" / "GARCH波动率建模.md").read_text(encoding="utf-8-sig")
        self.assertIn("https://online.stat.psu.edu/stat510/Lesson11", card)
        self.assertIn("Lesson 11.1: ARCH/GARCH Models", card)
        self.assertNotIn("量化金融 HW", card)

    def test_stage_two_official_source_urls_are_canonical(self) -> None:
        stage_root = COURSE_ROOT / "02-平稳性与相关结构"
        stationarity = (stage_root / "平稳性.md").read_text(encoding="utf-8-sig")
        acf_card = (stage_root / "自相关函数ACF.md").read_text(encoding="utf-8-sig")
        pacf_card = (stage_root / "时间序列分析-偏自相关函数PACF.md").read_text(encoding="utf-8-sig")
        self.assertIn("https://online.stat.psu.edu/stat510/Lesson01", stationarity)
        self.assertIn("https://online.stat.psu.edu/stat510/Lesson01", acf_card)
        self.assertIn("https://online.stat.psu.edu/stat510/Lesson02", pacf_card)
        self.assertNotIn("online.stat.psu.edu/stat510/lesson/", stationarity + acf_card + pacf_card)

    def test_audit_script_passes(self) -> None:
        path = PROJECT_ROOT / "scripts" / "audit_course.py"
        spec = importlib.util.spec_from_file_location("audit_course", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertEqual(module.COURSE_ROOT, COURSE_ROOT)
        self.assertGreaterEqual(len(module.markdown_files(module.COURSE_ROOT)), 79)
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

    def test_unit_root_example_expected_direction(self) -> None:
        import warnings

        import numpy as np
        from statsmodels.tsa.stattools import adfuller, kpss

        random = np.random.default_rng(61)
        noise = random.normal(size=400)
        stationary = np.empty(400)
        stationary[0] = noise[0]
        for position in range(1, len(stationary)):
            stationary[position] = 0.65 * stationary[position - 1] + noise[position]
        random_walk = np.cumsum(noise)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            stationary_adf = adfuller(stationary, regression="c", autolag="AIC")[1]
            stationary_kpss = kpss(stationary, regression="c", nlags="auto")[1]
            walk_adf = adfuller(random_walk, regression="c", autolag="AIC")[1]
            walk_kpss = kpss(random_walk, regression="c", nlags="auto")[1]

        self.assertLess(stationary_adf, 0.05)
        self.assertGreaterEqual(stationary_kpss, 0.05)
        self.assertGreaterEqual(walk_adf, 0.05)
        self.assertLess(walk_kpss, 0.05)

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
