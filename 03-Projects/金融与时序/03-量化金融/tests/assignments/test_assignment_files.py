from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ASSIGNMENT_DIRS = [ROOT / "课后作业", ROOT / "阶段作业", ROOT / "大作业"]
SCRIPT_ROOT = ROOT / "scripts" / "assignments"


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    assert text.startswith("---")
    return text.split("---", 2)[1]


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
        for field in ("source_locator:", "estimated_hours:", "fixture_path:", "updated:"):
            assert field in fm, f"{path} missing {field}"
        for section in required_sections:
            assert re.search(rf"^## {section}\s*$", text, re.MULTILINE), f"{path} missing {section}"
        detail = re.search(r"^## 题目细化\s*$\n(?P<body>.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
        assert detail
        headings = re.findall(r"^### Q([1-4])\b", detail.group("body"), re.MULTILINE)
        assert headings == ["1", "2", "3", "4"], f"{path} must contain ordered Q1-Q4"
        assert "```text" in text, f"{path} must specify a submission tree"
        assert "```python" in text, f"{path} must expose machine-checkable assertions"
        assert text.count("| 现象 | 优先检查 |") == 1, f"{path} must have one diagnostic table"
        for phrase in forbidden_template_phrases:
            assert phrase not in text, f"{path} retains generic template prose: {phrase}"


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
