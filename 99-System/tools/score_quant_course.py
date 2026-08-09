#!/usr/bin/env python3
"""Mechanical rubric evidence inventory; never emits a teaching-quality score."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融"
STAGES = ["00-前置知识", "01-夯实基础", "02-量化核心技能", "03-研究验证与稳健性", "04-深入精通"]


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def diagnose() -> tuple[list[str], list[str]]:
    passed: list[str] = []
    issues: list[str] = []
    route = text(COURSE / "🗺️ 量化金融学习路径.md")
    source = text(COURSE / "📚 教材挂载索引.md")
    mocs = [path for stage in STAGES for path in (COURSE / stage).glob("🧭*.md")]
    cards = [
        path
        for stage in STAGES
        for path in (COURSE / stage).glob("*.md")
        if not path.name.startswith("🧭")
        and re.search(r"^type:\s*study\s*$", text(path), re.MULTILINE)
        and not re.search(r"^assessment_exempt:\s*true\s*$", text(path), re.MULTILINE)
    ]
    assignments = [path for tier in ("课后作业", "阶段作业", "大作业") for path in (PROJECT / tier).glob("*.md")]

    if "## 通过标准" in route and len(mocs) == 5 and all("## 阶段验收与作业" in text(path) for path in mocs):
        passed.append("三级导航、阶段顺序与阶段闸门可机械定位")
    else:
        issues.append("route or stage MOC guidance incomplete")

    stage0_moc = COURSE / "00-前置知识" / "🧭 阶段0-先修诊断与研究协议.md"
    if "诊断" in text(stage0_moc) and "重测" in route and any("累计交错测验" in path.name for path in cards):
        passed.append("诊断、重测与累计检索入口存在")
    else:
        issues.append("diagnostic/retest protocol incomplete")

    manifests = list((PROJECT / "scripts" / "assignments").rglob("package_manifest.json"))
    if len(assignments) == 14 and len(manifests) == 9 and (PROJECT / "tests" / "assignments" / "test_stage_runners.py").is_file():
        passed.append("14 份规范作业、9 个执行包与 runner 测试存在")
    else:
        issues.append(f"expected 14 canonical assignments, found {len(assignments)}")

    stage0_cards = list((COURSE / "00-前置知识").glob("*.md"))
    if len(stage0_cards) >= 5 and "最低前置" in route and "停止" in route:
        passed.append("最低前置、停止条件与补学入口存在")
    else:
        issues.append("stage 0 minimum prerequisite contract incomplete")

    incomplete_cards = []
    for path in cards:
        body = text(path)
        if "## 学完后可以完成" not in body or re.search(r"source_url:\s*[\"']?\[待验证\]", body):
            incomplete_cards.append(path.name)
    if incomplete_cards:
        issues.append("one or more formal cards lack derived assessment or verified sources")
    else:
        passed.append("活动知识卡具备来源与派生验收入口")

    if "## 覆盖矩阵" in source and ("单源充分性判断" in source or "## 多源课程融合自评" in source):
        passed.append("来源角色、覆盖矩阵与单源/多源判断有记录")
    else:
        issues.append("source registry lacks coverage or sufficiency evidence")

    return passed, issues


def main() -> int:
    passed, issues = diagnose()
    print("量化金融课程机械证据清单（不评分，不替代逐卡审阅）：")
    for item in passed:
        print(f"- PASS: {item}")
    if issues:
        print("- FAIL: 存在以下机械缺口")
        for issue in issues:
            print(f"  - {issue}")
        print("结论：EVIDENCE FAIL；不得进入人工评分。")
        return 1
    print("结论：EVIDENCE READY；五维教学质量只能由逐卡人工/独立复审评分。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
