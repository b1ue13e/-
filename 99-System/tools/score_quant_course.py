#!/usr/bin/env python3
"""Deterministic teaching-quality score for the quant-finance course."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
QUANT = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"

ENTRY = QUANT / "00-课程说明与先修诊断.md"
LEARNING_PATH = QUANT / "🗺️ 量化金融学习路径.md"
WEEKLY = QUANT / "知识地图" / "00-每周学习执行卡.md"
BOOTSTRAP = QUANT / "01-夯实基础" / "00-零基础补救-数学统计与Python.md"
GLOSSARY = QUANT / "01-夯实基础" / "00-量化金融符号与术语速查.md"
EXERCISE_DIR = QUANT / "03-Projects" / "开源课程课后习题"
EXERCISE_HUB = EXERCISE_DIR / "README.md"
LEVEL_ZERO = QUANT / "01-夯实基础" / "量化金融-Level0-累计交错测验.md"

CORE_NOTES = [
    QUANT / "01-夯实基础" / "收益率与对数收益率.md",
    QUANT / "01-夯实基础" / "OHLCV字段清洗与复权.md",
    QUANT / "01-夯实基础" / "时间索引与频率（量化）.md",
    QUANT / "01-夯实基础" / "Pandas分组聚合与透视表.md",
    QUANT / "01-夯实基础" / "滚动窗口与波动率特征.md",
    QUANT / "02-量化核心技能" / "样本泄漏.md",
    QUANT / "02-量化核心技能" / "CAPM 资本资产定价模型.md",
    QUANT / "02-量化核心技能" / "Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model).md",
]


@dataclass
class Dimension:
    name: str
    score: float
    max_score: int
    evidence: list[str]
    gaps: list[str]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def has_all(text: str, markers: list[str]) -> bool:
    return all(marker in text for marker in markers)


def ratio(paths: list[Path], predicate) -> float:
    existing = [path for path in paths if path.exists()]
    if not existing:
        return 0.0
    return sum(bool(predicate(read(path))) for path in existing) / len(paths)


def teaching_structure(text: str) -> int:
    """Count semantic sections without depending on one exact heading template."""
    groups = [
        ["解决什么问题", "定义、机制", "为什么它重要"],
        ["前置", "prerequisites:"],
        ["直觉", "机制"],
        ["例子", "example"],
        ["误区", "边界", "失败"],
        ["闭卷", "主动回忆"],
        ["自测", "先测"],
    ]
    lowered = text.lower()
    return sum(any(marker.lower() in lowered for marker in group) for group in groups)


def knowledge_structure(text: str) -> int:
    groups = [
        ["定义"],
        ["公式", "$$"],
        ["符号", "量纲", "字段"],
        ["推导", "机制", "为什么"],
        ["例子", "example"],
        ["误区", "边界", "失败"],
        ["自测", "先测", "闭卷"],
        ["source", "可定位来源", "来源"],
    ]
    lowered = text.lower()
    return sum(any(marker.lower() in lowered for marker in group) for group in groups)


def add_item(
    dimension: Dimension,
    points: float,
    passed: bool,
    evidence: str,
    gap: str,
) -> None:
    if passed:
        dimension.score += points
        dimension.evidence.append(f"+{points:g} {evidence}")
    else:
        dimension.gaps.append(f"-{points:g} {gap}")


def add_ratio(
    dimension: Dimension,
    points: float,
    value: float,
    evidence: str,
    gap: str,
) -> None:
    earned = round(points * value, 2)
    dimension.score += earned
    if value >= 0.8:
        dimension.evidence.append(f"+{earned:g}/{points:g} {evidence} ({value:.0%})")
    else:
        dimension.gaps.append(f"-{points-earned:g}/{points:g} {gap} ({value:.0%})")


def exercise_files() -> list[Path]:
    if not EXERCISE_DIR.exists():
        return []
    return sorted(EXERCISE_DIR.glob("PS*.md"))


def guided_teaching() -> Dimension:
    d = Dimension("引导性教学", 0, 20, [], [])
    entry = read(ENTRY)
    learning_path = read(LEARNING_PATH)
    weekly = read(WEEKLY)
    exercises = exercise_files()
    add_item(d, 2, has_all(entry, ["目标用户", "完成结果", "先修诊断"]),
             "入口定义用户、结果和诊断", "入口缺少用户、结果或诊断")
    week_rows = sum(bool(re.search(rf"(?m)^\|\s*\*\*?{week}\*\*?\s*\|", learning_path)) for week in range(10))
    path_contract = week_rows == 10 and has_all(
        learning_path,
        ["唯一学习入口", "实作与解锁", "知识地图/00-每周学习执行卡"],
    )
    weekly_contract = (
        weekly.count("### 当周练习") == 10
        and weekly.count("### 通过闸门") == 10
    )
    add_item(d, 3, path_contract and weekly_contract,
             "唯一入口展示 10 周短索引，执行卡保存练习与闸门", "路线索引或执行卡契约不完整")
    week_sections = sum(bool(re.search(rf"(?m)^##\s+Week\s+{week}\b", weekly)) for week in range(10))
    add_item(d, 3, week_sections == 10, "10 周执行卡逐周展开", "缺少逐周执行卡")
    coverage = ratio(CORE_NOTES, lambda text: teaching_structure(text) >= 6)
    add_ratio(d, 6, coverage, "核心卡具备教学脚手架", "核心卡教学脚手架不完整")
    scaffold = ratio(
        exercises,
        lambda text: has_all(text, ["作答协议", "提示 1", "提示 2", "答案锚点", "错因"]),
    ) if exercises else 0.0
    add_ratio(d, 4, scaffold, "习题有提示和反馈闭环", "习题缺少分层提示或反馈")
    add_item(d, 2, has_all(entry + weekly, ["未通过", "补救", "重测"]),
             "失败后有补救与重测决策", "失败后缺少补救或重测规则")
    return d


def cognitive_science() -> Dimension:
    d = Dimension("认知科学", 0, 20, [], [])
    entry = read(ENTRY)
    weekly = read(WEEKLY)
    level_zero = read(LEVEL_ZERO)
    exercises = exercise_files()
    exercise_text = "\n".join(read(path) for path in exercises)
    add_item(d, 2, "信心" in entry and "高置信误区" in entry,
             "诊断包含信心校准", "诊断缺少信心校准")
    retrieval = ratio(CORE_NOTES, lambda text: "闭卷" in text or "主动回忆" in text)
    add_ratio(d, 3, retrieval, "核心卡含提取练习", "核心卡缺少提取练习")
    add_item(d, 2, has_all(weekly + exercise_text, ["24 小时", "72 小时", "7 天"]),
             "使用间隔重测节奏", "缺少 24h/72h/7d 间隔重测")
    add_item(d, 3, LEVEL_ZERO.exists() and "交错" in level_zero and "48 小时" in level_zero,
             "存在累计交错测验和延迟复测", "缺少累计交错或延迟复测")
    fading = ratio(exercises, lambda text: has_all(text, ["示例题", "仿做题", "独立题", "迁移题"])) if exercises else 0.0
    add_ratio(d, 4, fading, "习题按脚手架渐隐排列", "未形成示例到迁移的渐隐序列")
    add_item(d, 3, has_all(entry + weekly + exercise_text, ["错因", "重测日期", "高置信"]),
             "记录错因、信心与重测", "错题闭环字段不完整")
    add_item(d, 1, has_all(exercise_text, ["作答前信心", "作答后信心"]),
             "习题记录前后信心", "习题缺少前后信心校准")
    add_item(d, 2, has_all(exercise_text, ["手算", "代码", "解释", "反例"]),
             "练习形式包含手算、代码、解释和反例", "练习形式不够多样")
    return d


def course_detail() -> Dimension:
    d = Dimension("课程详细度", 0, 20, [], [])
    weekly = read(WEEKLY)
    hub = read(EXERCISE_HUB)
    exercises = exercise_files()
    exercise_text = "\n".join(read(path) for path in exercises)
    detailed_weeks = sum(
        bool(re.search(rf"(?ms)^##\s+Week\s+{week}\b.*?(?=^##\s+Week\s+|\Z)", weekly))
        for week in range(10)
    )
    add_ratio(d, 5, detailed_weeks / 10, "逐周目标、任务和闸门已展开", "逐周设计不完整")
    source_count = len({item.lower() for item in re.findall(r"MIT18_S096F13_pset[1-9]", hub, re.I)})
    add_item(d, 4, source_count == 9 and "CC BY-NC-SA 4.0" in hub,
             "9 份 MIT OCW 作业与许可完整登记", "开源作业或许可登记不完整")
    problem_count = len(re.findall(r"(?m)^###\s+题\s*\d+", exercise_text))
    add_item(d, 4, len(exercises) >= 5 and problem_count >= 25,
             f"收录 {len(exercises)} 份练习、{problem_count} 道题", "实际可做习题不足 5 份或 25 道")
    projects = [path.parents[1] for path in (QUANT / "03-Projects").rglob("tests/test_*.py")]
    test_methods = sum(
        len(re.findall(r"(?m)^\s*def\s+test_", read(path)))
        for path in (QUANT / "03-Projects").rglob("tests/test_*.py")
    )
    add_item(d, 3, len(set(projects)) >= 6 and test_methods >= 27,
             f"{len(set(projects))} 个实验包、{test_methods} 个测试", "可执行实验或测试不足")
    add_item(d, 2, "Capstone" in weekly and "开源课程课后习题" in weekly,
             "习题与 Capstone 接入周计划", "习题或 Capstone 未接入周计划")
    index = read(QUANT / "知识地图" / "🧭 开源作业体系-量化金融.md")
    add_item(d, 2, has_all(index, ["学习顺序", "课程范围", "当前进度", "规格", "可执行"]),
             "学习顺序、课程范围与当前进度职责分离", "导航或状态职责边界不清")
    return d


def beginner_fit() -> Dimension:
    d = Dimension("小白适配性", 0, 20, [], [])
    entry = read(ENTRY)
    bootstrap = read(BOOTSTRAP)
    glossary = read(GLOSSARY)
    weekly = read(WEEKLY)
    exercises = "\n".join(read(path) for path in exercise_files())
    add_item(d, 3, has_all(entry, ["先修诊断", "诊断分流", "补救路线"]),
             "诊断、分流和补救齐全", "诊断补救链不完整")
    add_item(d, 4, BOOTSTRAP.exists() and has_all(bootstrap, ["Python", "数学", "统计", "金融"]),
             "存在 Python、数学统计和金融补底", "缺少零基础补底卡")
    glossary_rows = len(re.findall(r"(?m)^\|\s*`?[^|]+`?\s*\|", glossary)) - 2
    add_item(d, 3, GLOSSARY.exists() and glossary_rows >= 20,
             f"术语表含至少 {max(glossary_rows, 0)} 个条目", "术语与符号速查不足 20 项")
    early_complete = all(
        has_all(
            re.search(rf"(?ms)^##\s+Week\s+{week}\b(.*?)(?=^##\s+Week\s+|\Z)", weekly).group(1),
            ["学习顺序", "当周练习", "通过闸门"],
        )
        if re.search(rf"(?ms)^##\s+Week\s+{week}\b(.*?)(?=^##\s+Week\s+|\Z)", weekly)
        else False
        for week in range(4)
    )
    add_item(d, 3, early_complete, "Week 0-3 提供逐步操作", "新手前四周缺少逐步操作")
    add_item(d, 2, has_all(bootstrap, ["预期输出", "故障排查"]),
             "补底卡包含预期输出与故障排查", "缺少预期输出或故障排查")
    add_item(d, 2, has_all(entry + weekly, ["建议学时", "停止条件"]),
             "给出学时和停止条件", "缺少学时或停止条件")
    hints = len(re.findall(r"提示 1", exercises))
    anchors = len(re.findall(r"答案锚点", exercises))
    add_item(d, 3, hints >= 25 and anchors >= 25,
             f"{hints} 道题提供分层提示和答案锚点", "少于 25 道题具备提示与答案校验")
    return d


def knowledge_detail() -> Dimension:
    d = Dimension("知识点详细度", 0, 20, [], [])
    coverage = ratio(CORE_NOTES, lambda text: knowledge_structure(text) >= 6)
    add_ratio(d, 6, coverage, "核心卡覆盖定义到自测", "核心卡知识结构不完整")
    caveats = ratio(CORE_NOTES, lambda text: "适用条件" in text or "限制" in text or "不等于" in text)
    add_ratio(d, 2, caveats, "核心卡说明适用边界", "核心卡缺少适用边界")
    symbols = ratio(
        CORE_NOTES,
        lambda text: ("公式" in text or "$$" in text)
        and ("符号" in text or "量纲" in text or "字段" in text),
    )
    add_ratio(d, 3, symbols, "核心卡含公式和符号解释", "核心卡公式或符号说明不足")
    examples = ratio(CORE_NOTES, lambda text: "手算" in text and ("```python" in text or "代码" in text))
    add_ratio(d, 3, examples, "核心卡兼有手算与代码", "核心卡缺少手算或代码")
    exercises = exercise_files()
    source_mapping = ratio(
        exercises,
        lambda text: "MIT18_S096F13_pset" in text and "对应知识卡" in text,
    ) if exercises else 0.0
    add_ratio(d, 3, source_mapping, "练习逐份映射来源和知识卡", "练习来源或知识映射不完整")
    hub = read(EXERCISE_HUB)
    add_item(d, 3, len(re.findall(r"https://ocw\.mit\.edu/", hub)) >= 10,
             "课程页、许可页和 9 份作业均可追溯", "开源来源链接不足")
    return d


def main() -> int:
    dimensions = [
        guided_teaching(),
        cognitive_science(),
        course_detail(),
        beginner_fit(),
        knowledge_detail(),
    ]
    total = round(sum(item.score for item in dimensions), 2)
    floor_passed = all(item.score >= 15 for item in dimensions)
    passed = total >= 85 and floor_passed
    report = {
        "course": "03-量化金融",
        "total": total,
        "maximum": 100,
        "threshold": 85,
        "dimension_floor": 15,
        "passed": passed,
        "dimensions": [asdict(item) for item in dimensions],
    }
    if "--json" in sys.argv:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"量化金融课程严格评分：{total:.2f}/100")
        for item in dimensions:
            print(f"- {item.name}: {item.score:.2f}/{item.max_score}")
            for gap in item.gaps:
                print(f"  {gap}")
        print(f"结论：{'PASS' if passed else 'FAIL'}（总分 >= 85 且每维 >= 15）")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
