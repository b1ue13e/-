#!/usr/bin/env python3
"""Deterministic internal score; never substitutes for independent A/B review."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融"
STAGES = ["00-前置知识", "01-夯实基础", "02-量化核心技能", "03-研究验证与稳健性", "04-深入精通"]


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def score() -> tuple[dict[str, int], list[str]]:
    issues: list[str] = []
    route = text(COURSE / "🗺️ 量化金融学习路径.md")
    source = text(COURSE / "📚 教材挂载索引.md")
    mocs = [path for stage in STAGES for path in (COURSE / stage).glob("🧭*.md")]
    cards = [path for stage in STAGES for path in (COURSE / stage).glob("*.md") if not path.name.startswith("🧭")]
    assignments = [path for tier in ("课后作业", "阶段作业", "大作业") for path in (PROJECT / tier).glob("*.md")]

    guidance = 20
    if "## 通过标准" not in route or len(mocs) != 5:
        guidance -= 4
        issues.append("route or stage MOC guidance incomplete")
    if "## 阶段验收与作业" not in "\n".join(text(path) for path in mocs):
        guidance -= 4
        issues.append("stage assessment sections incomplete")

    cognition = 20
    if "诊断" not in text(COURSE / "00-前置知识" / "🧭 阶段0-先修诊断与研究协议.md") or "重测" not in route:
        cognition -= 4
        issues.append("diagnostic/retest protocol incomplete")
    if not any("累计交错测验" in path.name for path in cards):
        cognition -= 4
        issues.append("retrieval practice entry missing")

    detail = 20
    if len(assignments) != 14:
        detail -= 6
        issues.append(f"expected 14 canonical assignments, found {len(assignments)}")
    if not (PROJECT / "tests" / "assignments").exists():
        detail -= 4
        issues.append("assignment tests directory missing")

    beginner = 20
    stage0_cards = list((COURSE / "00-前置知识").glob("*.md"))
    if len(stage0_cards) < 5 or "最低前置" not in route:
        beginner -= 4
        issues.append("stage 0 minimum prerequisite contract incomplete")
    if "停止" not in route:
        beginner -= 4
        issues.append("route lacks explicit stop conditions")

    knowledge = 20
    for path in cards:
        body = text(path)
        if "## 学完后可以完成" not in body:
            knowledge -= 1
        if re.search(r"source_url:\s*[\"']?\[待验证\]", body):
            knowledge -= 1
    knowledge = max(0, knowledge)
    if knowledge < 16:
        issues.append("one or more formal cards lack derived assessment or verified sources")

    return {"引导性教学": max(guidance, 0), "认知科学": max(cognition, 0), "课程详细度": max(detail, 0), "小白适配性": max(beginner, 0), "知识点详细度": knowledge}, issues


def main() -> int:
    scores, issues = score()
    total = sum(scores.values())
    print(f"量化金融课程内部评分：{total}/100")
    for name, value in scores.items():
        print(f"- {name}: {value}/20")
    if issues:
        print("整改项：")
        for issue in issues:
            print(f"- {issue}")
    if total >= 85 and all(value >= 16 for value in scores.values()):
        print("结论：INTERNAL PASS（不替代独立 A/B 复审）")
        return 0
    print("结论：INTERNAL FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
