#!/usr/bin/env python3
"""Audit the quantitative-finance route and its one-way assignment contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融"
STAGES = ["00-前置知识", "01-夯实基础", "02-量化核心技能", "03-研究验证与稳健性", "04-深入精通"]
EXPECTED_CORE_COUNTS = {
    "00-前置知识": 5,
    "01-夯实基础": 9,
    "02-量化核心技能": 13,
    "03-研究验证与稳健性": 10,
    "04-深入精通": 7,
}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def fm(text: str) -> dict:
    if not text.startswith("---") or text.count("---") < 2:
        return {}
    raw = text.split("---", 2)[1]
    if yaml is None:
        return {}
    try:
        value = yaml.safe_load(raw)
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def clean(raw: str) -> str:
    return raw.replace("\\|", "|").split("|", 1)[0].split("#", 1)[0].strip()


def main() -> int:
    errors: list[str] = []
    route = COURSE / "🗺️ 量化金融学习路径.md"
    source = COURSE / "📚 教材挂载索引.md"
    index = PROJECT / "🧭 课程作业总索引.md"
    for path in (route, source, index):
        if not path.exists():
            errors.append(f"missing canonical page: {path.relative_to(ROOT)}")

    route_text = read(route) if route.exists() else ""
    source_text = read(source) if source.exists() else ""
    if "16 周" not in route_text or "17–20" not in route_text:
        errors.append("learning path must declare the 16+4 week contract")
    for token in ("阶段 0", "阶段 1", "阶段 2", "阶段 3", "阶段 4"):
        if token not in route_text:
            errors.append(f"learning path missing {token}")
    if "## 多源课程融合自评" not in source_text:
        errors.append("source index missing multi-source self-assessment")
    if not re.search(r"\|\s*\*\*总分\*\*\s*\|\s*\*\*([0-9]+)\*\*", source_text):
        errors.append("source index missing fusion score")

    formal_cards: dict[str, tuple[Path, dict]] = {}
    alias_to_stem: dict[str, str] = {}
    for stage in STAGES:
        for card in (COURSE / stage).glob("*.md"):
            value = fm(read(card))
            if value.get("type") != "study":
                continue
            formal_cards[card.stem] = (card, value)
            aliases = value.get("aliases", []) or []
            aliases = [aliases] if isinstance(aliases, str) else aliases
            for alias in aliases:
                alias_to_stem[str(alias)] = card.stem

    core_order: dict[str, int] = {}
    for stage in STAGES:
        directory = COURSE / stage
        mocs = list(directory.glob("🧭*.md"))
        if len(mocs) != 1:
            errors.append(f"{stage} must contain exactly one MOC")
            continue
        text = read(mocs[0])
        if "## 阶段验收与作业" not in text:
            errors.append(f"{mocs[0].relative_to(ROOT)} missing assessment section")
        core_match = re.search(
            r"^## 核心学习顺序[^\n]*\n(?P<body>.*?)(?=^## |\Z)",
            text,
            re.MULTILINE | re.DOTALL,
        )
        core_count = len(re.findall(r"^\d+\.\s+\[\[", core_match.group("body"), re.MULTILINE)) if core_match else 0
        if core_count != EXPECTED_CORE_COUNTS[stage]:
            errors.append(
                f"{mocs[0].relative_to(ROOT)} has {core_count} core cards; "
                f"expected {EXPECTED_CORE_COUNTS[stage]}"
            )
        if core_match:
            for raw in WIKILINK_RE.findall(core_match.group("body")):
                target = Path(clean(raw)).stem
                target = alias_to_stem.get(target, target)
                if target in formal_cards:
                    core_order[target] = len(core_order)
        for card in directory.glob("*.md"):
            if not card.name.startswith("🧭") and card.stem not in text:
                errors.append(f"stage MOC omits formal card {card.name}")

    for current, (path, value) in formal_cards.items():
        if current not in core_order:
            continue
        upstream = value.get("upstream", []) or []
        upstream = [upstream] if isinstance(upstream, str) else upstream
        for raw in upstream:
            target = Path(clean(str(raw).strip("[]"))).stem
            target = alias_to_stem.get(target, target)
            if target in core_order and core_order[target] >= core_order[current]:
                errors.append(
                    f"core upstream is not earlier in stage order: {path.relative_to(ROOT)} -> {target}"
                )

    expected = {*(f"QF-L{i:02d}" for i in range(1, 10)), *(f"QF-ST{i:02d}" for i in range(1, 5)), "QF-CAPSTONE-QLIB"}
    actual: set[str] = set()
    for tier in ("课后作业", "阶段作业", "大作业"):
        directory = PROJECT / tier
        files = list(directory.glob("*.md"))
        if not files:
            errors.append(f"missing assignment tier: {tier}")
        for path in files:
            value = fm(read(path))
            actual.add(str(value.get("assignment_id", "")))
            if value.get("assignment_level") not in {"lesson", "stage", "capstone"}:
                errors.append(f"invalid assignment_level: {path.relative_to(ROOT)}")
            if value.get("project_type") != "homework":
                errors.append(f"assignment must use project_type homework: {path.relative_to(ROOT)}")
    if actual != expected:
        errors.append(f"canonical assignment set mismatch: {sorted(actual)}")
    if (PROJECT / "real_assignment_packages").exists():
        errors.append("real_assignment_packages remains outside archive")

    forbidden = ("李宏毅式", "李宏毅-CMU模式", "4-Tier", "Boss Baseline", "阶梯作业", "[支线任务]")
    scoped = [path for path in COURSE.rglob("*.md") if ".归档" not in path.parts] + [path for tier in ("课后作业", "阶段作业", "大作业") for path in (PROJECT / tier).glob("*.md")]
    for path in scoped:
        text = read(path)
        for term in forbidden:
            if term in text:
                errors.append(f"forbidden legacy label in {path.relative_to(ROOT)}: {term}")

    if errors:
        print(f"Quant route audit failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Quant route audit passed: 16+4 week path, five stage MOCs, canonical assignments, and project boundaries are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
