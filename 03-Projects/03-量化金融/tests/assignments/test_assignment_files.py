from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]
ASSIGNMENT_DIRS = [ROOT / "课后作业", ROOT / "阶段作业", ROOT / "大作业"]
SCRIPT_ROOT = ROOT / "scripts" / "assignments"
VAULT = ROOT.parents[2]
COURSE = VAULT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    assert text.startswith("---")
    return text.split("---", 2)[1]


def python_block_after(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8-sig")
    match = re.search(re.escape(heading) + r".*?```python\s*\n(?P<code>.*?)```", text, re.DOTALL)
    assert match, f"{path} lacks executable example after {heading}"
    return match.group("code")


def test_only_canonical_assignment_specs_are_in_tier_directories() -> None:
    specs = [path for directory in ASSIGNMENT_DIRS for path in directory.glob("*.md")]
    assert len(specs) == 14
    ids = []
    detail_blocks = []
    for path in specs:
        fm = frontmatter(path)
        for field in ("assignment_id:", "assignment_level:", "assignment_format:", "requires:", "source_url:", "license:"):
            assert field in fm, f"{path} missing {field}"
        text = path.read_text(encoding="utf-8-sig")
        for section in ("学习目标", "任务边界", "提交产物", "验收标准", "失败条件", "评分量表"):
            match = re.search(rf"^## {section}\s*$\n(?P<body>.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
            assert match and match.group("body").strip(), f"{path} has empty {section}"
        detail = re.search(r"^## 题目细化\s*$\n(?P<body>.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
        assert detail and detail.group("body").strip(), f"{path} has empty 题目细化"
        assignment_id = next(line.split(":", 1)[1].strip().strip('"') for line in fm.splitlines() if line.startswith("assignment_id:"))
        expected_prefix = "Q1" if assignment_id.startswith("QF-L") else "S1"
        assert expected_prefix in detail.group("body"), f"{path} lacks assignment-specific numbered tasks"
        detail_blocks.append(detail.group("body").strip())
        ids.append(next(line.split(":", 1)[1].strip().strip('"') for line in fm.splitlines() if line.startswith("assignment_id:")))
    assert len(ids) == len(set(ids))
    assert len(detail_blocks) == len(set(detail_blocks)), "assignment detail blocks must not be duplicated templates"


def test_support_scripts_are_valid_python() -> None:
    files = list(SCRIPT_ROOT.rglob("*.py"))
    assert files
    for path in files:
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))


def test_order_matching_example_executes_both_sides() -> None:
    path = COURSE / "04-深入精通" / "订单类型与交易所连续竞价撮合机制 (Order Types & Continuous Double Auction).md"
    code = python_block_after(path, "### 例子 3：实际应用（Python 模拟极简连续竞价撮合引擎）")
    namespace: dict[str, object] = {}
    exec(compile(code, str(path), "exec"), namespace)
    engine = namespace["engine"]
    engine2 = namespace["engine2"]
    assert engine.asks == [(100.0, 1, 20)]
    assert engine2.bids == [(-100.0, 1, 20)]


def test_factor_preprocessing_example_runs_without_dummy_trap() -> None:
    path = COURSE / "03-研究验证与稳健性" / "因子预处理：去极值、中性化与标准化 (Factor Preprocessing_ Winsorization, Neutralization & Z-Score).md"
    code = python_block_after(path, "### 例子 3：实际应用（Python 教学版单截面预处理函数）")
    namespace: dict[str, object] = {}
    exec(compile(code, str(path), "exec"), namespace)
    clean_factor = namespace["clean_factor"]
    fitted_model = namespace["fitted_model"]
    assert abs(float(clean_factor.mean())) < 1e-12
    assert float(clean_factor.std(ddof=1)) == pytest.approx(1.0)
    assert fitted_model.model.rank == fitted_model.model.exog.shape[1]


def test_queue_probability_example_distinguishes_front_and_fill() -> None:
    path = COURSE / "04-深入精通" / "跨市场排队优先权与挂单成交概率 (Queue Position & Fill Probability in High-Frequency Trading).md"
    code = python_block_after(path, "### 例子 3：实际应用（Python 模拟盘口队列消耗与成交概率实时计算）")
    namespace: dict[str, object] = {}
    exec(compile(code, str(path), "exec"), namespace)
    result = namespace["result"]
    assert result["reach_front_probability"] == pytest.approx(0.7576078, abs=1e-6)
    assert result["fill_probability"] == pytest.approx(0.5384027, abs=1e-6)
    assert result["fill_probability"] <= result["reach_front_probability"]


def test_active_course_has_no_prompt_or_legacy_assignment_residue() -> None:
    forbidden = (
        "李宏毅式",
        "李宏毅-CMU模式",
        "4-Tier",
        "Boss Baseline",
        "阶梯作业",
        "## 13. 给 Obsidian 的归档建议",
        "请帮我建立知识网络",
        "注意：不要只列链接",
        "刷怪通关",
        "专题实战任务",
        "7.5 实战模块",
    )
    for path in COURSE.rglob("*.md"):
        if ".归档" in path.parts:
            continue
        body = path.read_text(encoding="utf-8-sig")
        for phrase in forbidden:
            assert phrase not in body, f"{path} retains {phrase}"
        assert not re.search(r"\bHW\d+\b", body, re.IGNORECASE), f"{path} retains legacy HW identity"
        assert "\\n\\n" not in body, f"{path} contains escaped newline residue"
        assert not re.search(
            r"(?m)^(?:#{1,6}\s*)?(?:上游依赖|下游延伸)\s*$", body
        ), f"{path} retains a static relationship section"
        assert not re.search(
            r"(?:上一张|下一张|Capstone-AAPL|(?:\*\*|\|)Week\s*\d)", body, re.IGNORECASE
        ), f"{path} retains stale card-level sequence or capstone identity"


def test_route_only_advertises_delivered_scope() -> None:
    route = (COURSE / "🗺️ 量化金融学习路径.md").read_text(encoding="utf-8-sig")
    assert "正式路线为 16 周" in route
    for phrase in ("16+4", "第 17–20 周", "4 周进阶"):
        assert phrase not in route
    assert (COURSE / "04-深入精通" / "🧭 阶段4-微观结构与执行.md").is_file()


def test_stage_mocs_link_to_their_canonical_assignments() -> None:
    expected = {
        "01-夯实基础": "QF-ST01",
        "02-量化核心技能": "QF-ST02",
        "03-研究验证与稳健性": "QF-ST03",
        "04-深入精通": "QF-ST04",
    }
    for stage, assignment_id in expected.items():
        moc = next((COURSE / stage).glob("🧭*.md"))
        body = moc.read_text(encoding="utf-8-sig")
        assert re.search(rf"\[\[[^\]]+\|{assignment_id}(?:\s|\])", body), f"{moc} lacks a clickable assignment"


def test_stage_four_teaches_queue_model_before_assessment() -> None:
    queue_name = "跨市场排队优先权与挂单成交概率 (Queue Position & Fill Probability in High-Frequency Trading)"
    assignment = ROOT / "阶段作业" / "量化金融-阶段作业-04-市场冲击与最优执行.md"
    metadata = yaml.safe_load(frontmatter(assignment))
    assert any(queue_name in str(item) for item in metadata["requires"])
    moc = COURSE / "04-深入精通" / "🧭 阶段4-微观结构与执行.md"
    body = moc.read_text(encoding="utf-8-sig")
    assert body.index(f"[[{queue_name}]]") < body.index("QF-ST04 市场冲击与最优执行实验")


def test_non_start_study_cards_declare_direct_upstream() -> None:
    true_starts = {
        "量化金融-先修诊断与分流",
    }
    for path in COURSE.glob("[0-9][0-9]-*/*.md"):
        metadata = yaml.safe_load(frontmatter(path))
        if metadata.get("type") != "study" or metadata.get("assessment_exempt") is True:
            continue
        upstream = metadata.get("upstream")
        if path.stem in true_starts:
            assert not upstream
        else:
            assert upstream, f"{path} lacks direct upstream"


def test_active_packages_have_canonical_ids_and_smoke_fixtures() -> None:
    expected_ids = {
        "QF-ST01-BASELINE",
        "QF-ST02-EVT",
        "QF-ST03-BARS",
        "QF-ST03-HRP",
        "QF-ST03-RMT",
        "QF-ST03-PBO",
        "QF-ST04-AC",
        "QF-ST04-QUEUE",
        "QF-CAPSTONE-QLIB",
    }
    manifests = sorted(SCRIPT_ROOT.rglob("package_manifest.json"))
    assert len(manifests) == 9
    actual_ids = set()
    for path in manifests:
        manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
        actual_ids.add(manifest["id"])
        assert not re.search(r"\bhw\d+\b", str(path), re.IGNORECASE)
        fixture = ROOT / manifest["smoke_data_dir"]
        assert fixture.is_dir()
        assert (path.parent / "starter" / "run.py").is_file()
        for filename in manifest["real_files"]:
            assert (fixture / filename).is_file()
    assert actual_ids == expected_ids


def test_lesson_assignments_are_actionable_not_templates() -> None:
    lesson_specs = sorted((ROOT / "课后作业").glob("*.md"))
    assert len(lesson_specs) == 9

    required_sections = (
        "作业定位",
        "固定输入",
        "题目细化",
        "提交产物",
        "公开验收断言",
        "引导自检",
        "失败诊断",
        "验收标准",
        "失败条件",
        "评分量表",
        "来源与答案边界",
        "官方原题加练",
    )
    forbidden_template_phrases = (
        "检查时间、成本、随机种子和失败案例",
        "smoke、样本内、样本外和真实市场证据混写",
        "数据与版本 | 来源、区间、频率、校验值、许可",
        "若 `scripts/assignments/<assignment_id>/` 存在",
    )

    for path in lesson_specs:
        text = path.read_text(encoding="utf-8-sig")
        fm = frontmatter(path)
        for field in (
            "source_locator:",
            "official_assignment_url:",
            "official_assignment_scope:",
            "accessed:",
            "answer_policy:",
            "estimated_hours:",
            "fixture_path:",
            "updated:",
        ):
            assert field in fm, f"{path} missing {field}"
        assert "source_type: local_integration_task" in fm
        assert "starter_path:" not in fm
        hours = re.search(r'estimated_hours:\s*"(\d+)-(\d+)"', fm)
        assert hours and int(hours.group(2)) <= 5, f"{path} exceeds lesson scope"
        for section in required_sections:
            assert re.search(rf"^## {section}\s*$", text, re.MULTILINE), f"{path} missing {section}"
        detail = re.search(r"^## 题目细化\s*$\n(?P<body>.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
        assert detail
        headings = re.findall(r"^### Q([1-4])\b", detail.group("body"), re.MULTILINE)
        assert headings == ["1", "2", "3", "4"], f"{path} must contain ordered Q1-Q4"
        hidden_prerequisites = ("投影矩阵", "Cook 距离", "转移矩阵", "指数分布", "PCA", "Vasicek")
        for term in hidden_prerequisites:
            assert term not in detail.group("body"), f"{path} requires untaught topic {term}"
        assert "```text" in text, f"{path} must specify a submission tree"
        assert "```python" in text, f"{path} must expose machine-checkable assertions"
        assert text.count("| 现象 | 优先检查 |") == 1, f"{path} must have one diagnostic table"
        for phrase in forbidden_template_phrases:
            assert phrase not in text, f"{path} retains generic template prose: {phrase}"
        assert not re.search(r"\bHW\d+\b", text, re.IGNORECASE), f"{path} retains a legacy HW identity"


def test_lesson_assignment_sources_map_to_distinct_mit_problem_sets() -> None:
    lesson_specs = sorted((ROOT / "课后作业").glob("*.md"))
    urls = []
    for number, path in enumerate(lesson_specs, start=1):
        fm = frontmatter(path)
        source_url = next(
            line.split(":", 1)[1].strip().strip('"')
            for line in fm.splitlines()
            if line.startswith("source_url:")
        )
        assert f"pset{number}/" in source_url, f"{path} does not map to MIT Problem Set {number}"
        urls.append(source_url)
    assert len(urls) == len(set(urls)) == 9


def test_legacy_assignment_source_is_archived() -> None:
    assert not (ROOT / "real_assignment_packages").exists()
    assert (ROOT / ".归档" / "历史作业包").exists()


def test_every_core_study_card_is_required_by_a_canonical_assignment() -> None:
    vault = ROOT.parents[2]
    course = vault / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
    moc_paths = sorted(course.glob("[0-9][0-9]-*/🧭 *.md"))
    assert len(moc_paths) == 5

    core_names: set[str] = set()
    for moc in moc_paths:
        for target in re.findall(r"^\d+\. \[\[([^\]|]+)", moc.read_text(encoding="utf-8-sig"), re.MULTILINE):
            name = Path(target).name
            matches = list(course.rglob(f"{name}.md"))
            assert len(matches) == 1, f"core link must resolve uniquely: {name}"
            metadata = yaml.safe_load(frontmatter(matches[0]))
            if metadata.get("type") == "study":
                core_names.add(name)

    required: set[str] = set()
    for directory in ASSIGNMENT_DIRS:
        for spec in directory.glob("*.md"):
            metadata = yaml.safe_load(frontmatter(spec))
            for link in metadata.get("requires", []):
                match = re.fullmatch(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", link)
                assert match, f"invalid requires link in {spec}: {link}"
                required.add(Path(match.group(1)).name)

    assert len(core_names) == 43
    assert core_names <= required, f"unassessed core cards: {sorted(core_names - required)}"
