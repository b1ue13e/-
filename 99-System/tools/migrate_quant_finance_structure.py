#!/usr/bin/env python3
"""Migrate the quant-finance course to the AGENTS.md directory contract.

The command is dry-run by default. Use --apply only after the recovery snapshot
has been created and the printed plan has been reviewed.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "03-量化金融"
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融"
SNAPSHOT = ROOT / ".recovery-hold" / "2026-08-06" / "quant-finance-comprehensive"
SKIP_PARTS = {
    ".git", ".obsidian", ".recovery-hold", ".pytest_cache", "__pycache__",
    "🗄️ 归档", ".归档",
}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def course_rel(path: str) -> Path:
    return COURSE / Path(path)


def project_rel(path: str) -> Path:
    return PROJECT / Path(path)


MOVES: tuple[tuple[Path, Path], ...] = (
    (course_rel("00-课程说明与先修诊断.md"), course_rel("00-前置知识/🧭 阶段0-先修诊断.md")),
    (
        course_rel("📈 主线：金融与时序 (Quantitative Finance, Time Series & Optimization Track).md"),
        course_rel("00-前置知识/量化金融-跨课程依赖与出口.md"),
    ),
    (course_rel("01-夯实基础/00-零基础补救-数学统计与Python.md"), course_rel("00-前置知识/量化金融-零基础补救-数学统计与Python.md")),
    (course_rel("01-夯实基础/00-量化金融符号与术语速查.md"), course_rel("00-前置知识/量化金融-符号与术语速查.md")),
    (
        course_rel("01-夯实基础/量化金融-实战起航-本地环境配置与依赖(requirements).md"),
        course_rel("00-前置知识/量化金融-本地环境配置与依赖.md"),
    ),
    (
        course_rel("01-夯实基础/量化金融-启蒙-主观交易与量化交易的本质区别.md"),
        course_rel("00-前置知识/量化金融-主观交易与量化交易.md"),
    ),
    (course_rel("知识地图/📦 外部实验资产索引.md"), course_rel("00-前置知识/量化金融-外部实验资产索引.md")),
    (
        course_rel("知识地图/🗺️ 量化金融全栈终极框架 (Academic + AFML + HFT).md"),
        course_rel("04-深入精通/量化金融-全栈资产地图.md"),
    ),
    (course_rel("03-Projects/Capstone-AAPL"), project_rel("validated_labs/Capstone-AAPL")),
    (course_rel("03-Projects/HW01-CAPM"), project_rel("validated_labs/HW01-CAPM")),
    (course_rel("03-Projects/HW05-BSM"), project_rel("validated_labs/HW05-BSM")),
    (course_rel("03-Projects/HW06-DynamicVaR"), project_rel("validated_labs/HW06-DynamicVaR")),
    (course_rel("03-Projects/Phase2-GARCH"), project_rel("validated_labs/Phase2-GARCH")),
    (course_rel("03-Projects/Tree-Model-Baseline"), project_rel("validated_labs/Tree-Model-Baseline")),
    (
        course_rel("03-Projects/Capstone-统一标的贯穿实战项目.md"),
        project_rel("大作业/量化金融-大作业-AAPL贯穿式量化研究.md"),
    ),
    (
        course_rel("03-Projects/课程质量自查记录.md"),
        project_rel("质量审计/历史-课程质量自查记录.md"),
    ),
    (
        course_rel("03-Projects/课程质量审计/2026-08-04-file-analysis.json"),
        project_rel("质量审计/历史/2026-08-04-file-analysis.json"),
    ),
    (
        course_rel("03-Projects/开源课程课后习题/README.md"),
        project_rel("课后作业/MIT-OCW-18S096-来源与作答说明.md"),
    ),
    (
        course_rel("03-Projects/开源课程课后习题/PS01-线性代数与概率基础.md"),
        project_rel("课后作业/量化金融-课后作业-01-线性代数与概率基础.md"),
    ),
    (
        course_rel("03-Projects/开源课程课后习题/PS02-回归与CAPM.md"),
        project_rel("课后作业/量化金融-课后作业-02-回归与CAPM.md"),
    ),
    (
        course_rel("03-Projects/开源课程课后习题/PS03-时间序列与波动率.md"),
        project_rel("课后作业/量化金融-课后作业-03-时间序列与波动率.md"),
    ),
    (
        course_rel("03-Projects/开源课程课后习题/PS04-组合与因子模型.md"),
        project_rel("课后作业/量化金融-课后作业-04-组合与因子模型.md"),
    ),
    (
        course_rel("03-Projects/开源课程课后习题/PS05-随机微积分与SDE.md"),
        project_rel("课后作业/量化金融-课后作业-05-随机微积分与SDE.md"),
    ),
)


PACKAGE_SLUGS = {
    "01": "hw01_capm_alpha_beta",
    "02": "hw02_markowitz_frontier",
    "03": "hw03_fama_macbeth",
    "04": "hw04_beneish_quality",
    "05": "hw05_black_scholes_hedging",
    "06": "hw06_garch_var",
    "07": "hw07_asymmetric_garch",
    "08": "hw08_evt_tail_risk",
    "09": "hw09_volume_dollar_bars",
    "10": "hw10_hrp_allocation",
    "11": "hw11_covariance_denoising",
    "12": "hw12_cpcv_pbo",
    "13": "hw13_almgren_chriss",
    "14": "hw14_darkpool_sor",
    "15": "hw15_queue_fill_probability",
    "16": "hw16_finrl_gymnasium",
    "17": "hw17_qlib_factor_research",
}


PACKAGE_TITLES = {
    "01": "CAPM与Alpha检验",
    "02": "马科维茨有效前沿",
    "03": "Fama-MacBeth回归",
    "04": "Beneish-M-Score财报排雷",
    "05": "Black-Scholes定价与对冲",
    "06": "GARCH波动率与动态VaR",
    "07": "非对称GARCH",
    "08": "EVT尾部风险",
    "09": "信息驱动采样",
    "10": "HRP资产配置",
    "11": "协方差去噪",
    "12": "CPCV与PBO审计",
    "13": "Almgren-Chriss最优执行",
    "14": "暗池与智能订单路由",
    "15": "盘口队列与挂单概率",
    "16": "金融交易环境与PPO",
    "17": "Qlib因子研究与成本敏感回测",
}


def assignment_target(number: str) -> str:
    title = PACKAGE_TITLES[number]
    if int(number) <= 8:
        return f"03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-{number}-{title}"
    if int(number) <= 16:
        stage = "03" if int(number) <= 12 else "04"
        return f"03-Projects/金融与时序/03-量化金融/阶段作业/量化金融-阶段作业-{stage}-{title}"
    return "03-Projects/金融与时序/03-量化金融/大作业/量化金融-大作业-Qlib因子研究与成本敏感回测"


HISTORICAL_FILES: tuple[Path, ...] = tuple(
    path
    for folder in (course_rel("02-量化核心技能"), course_rel("04-深入精通"), course_rel("03-Projects"))
    if folder.exists()
    for path in folder.glob("[[]支线任务[]] HW*.md")
)


def historical_number(path: Path) -> str:
    match = re.search(r"HW(\d{2})", path.name)
    if not match:
        raise ValueError(f"Cannot parse assignment number from {path}")
    return match.group(1)


def link_key(path: Path) -> str:
    return rel(path.with_suffix("")) if path.suffix else rel(path)


def build_link_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for source, destination in MOVES:
        if source.is_dir():
            continue
        target = link_key(destination)
        old_root = link_key(source)
        mapping[old_root] = target
        try:
            old_course = source.relative_to(COURSE).with_suffix("").as_posix()
            mapping[old_course] = target
        except ValueError:
            pass
        if source.stem != "README":
            mapping[source.stem] = target

    for path in HISTORICAL_FILES:
        number = historical_number(path)
        target = assignment_target(number)
        mapping[path.stem] = target
        mapping[link_key(path)] = target
        mapping[path.relative_to(COURSE).with_suffix("").as_posix()] = target

    explicit = {
        "知识地图/00-每周学习执行卡": "02-Knowledge/🧠 学习系统/03-量化金融/🗺️ 量化金融学习路径",
        "00-每周学习执行卡": "02-Knowledge/🧠 学习系统/03-量化金融/🗺️ 量化金融学习路径",
        "知识地图/🧭 开源作业体系-量化金融": "03-Projects/金融与时序/03-量化金融/🧭 课程作业总索引",
        "🧭 开源作业体系-量化金融": "03-Projects/金融与时序/03-量化金融/🧭 课程作业总索引",
        "03-Projects/课程质量自查记录": "03-Projects/金融与时序/03-量化金融/质量审计/课程严苛审计",
        "课程质量自查记录": "03-Projects/金融与时序/03-量化金融/质量审计/课程严苛审计",
        "03-Projects/Capstone-AAPL/README": "03-Projects/金融与时序/03-量化金融/大作业/量化金融-大作业-AAPL贯穿式量化研究",
        "03-Projects/HW01-CAPM/README": assignment_target("01"),
        "03-Projects/HW05-BSM/README": assignment_target("05"),
        "03-Projects/HW06-DynamicVaR/README": assignment_target("06"),
        "03-Projects/Phase2-GARCH/README": assignment_target("06"),
        "03-Projects/Tree-Model-Baseline/README": assignment_target("17"),
        "03-Projects/Capstone-统一标的贯穿实战项目": "03-Projects/金融与时序/03-量化金融/大作业/量化金融-大作业-AAPL贯穿式量化研究",
        "Capstone-统一标的贯穿实战项目": "03-Projects/金融与时序/03-量化金融/大作业/量化金融-大作业-AAPL贯穿式量化研究",
        "03-Projects/[支线任务] HW17-Qlib因子研究": assignment_target("17"),
        "[支线任务] HW17-Qlib因子研究": assignment_target("17"),
        "📚 教材挂载索引": "02-Knowledge/🧠 学习系统/03-量化金融/📚 教材挂载索引",
        "OHLCV字段清洗与复权": "02-Knowledge/🧠 学习系统/03-量化金融/01-夯实基础/OHLCV字段清洗与复权",
        "协方差矩阵": "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)",
    }
    for number in PACKAGE_SLUGS:
        slug = PACKAGE_SLUGS[number]
        explicit[f"03-Projects/金融与时序/03-量化金融/real_assignment_packages/{slug}/README"] = assignment_target(number)

    exercise_names = {
        "PS01-线性代数与概率基础": "量化金融-课后作业-01-线性代数与概率基础",
        "PS02-回归与CAPM": "量化金融-课后作业-02-回归与CAPM",
        "PS03-时间序列与波动率": "量化金融-课后作业-03-时间序列与波动率",
        "PS04-组合与因子模型": "量化金融-课后作业-04-组合与因子模型",
        "PS05-随机微积分与SDE": "量化金融-课后作业-05-随机微积分与SDE",
    }
    for old, new in exercise_names.items():
        target = f"03-Projects/金融与时序/03-量化金融/课后作业/{new}"
        explicit[old] = target
        explicit[f"03-Projects/开源课程课后习题/{old}"] = target
        explicit[f"../03-Projects/开源课程课后习题/{old}"] = target

    mapping.update(explicit)
    return mapping


def iter_markdown() -> list[Path]:
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        current = Path(dirpath)
        dirnames[:] = [name for name in dirnames if name not in SKIP_PARTS and not name.startswith(".tmp")]
        if any(part in SKIP_PARTS for part in current.parts):
            continue
        paths.extend(current / name for name in filenames if name.endswith(".md"))
    return paths


def split_inner(inner: str) -> tuple[str, str, str]:
    pipe = re.search(r"(?<!\\)\|", inner)
    alias = ""
    if pipe:
        alias = inner[pipe.end():]
        inner = inner[: pipe.start()]
    if "#" in inner:
        target, anchor = inner.split("#", 1)
        return target, f"#{anchor}", alias
    return inner, "", alias


def rewrite_links(text: str, mapping: dict[str, str], local_scope: bool) -> tuple[str, int]:
    replacements = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal replacements
        inner = match.group(1)
        target, anchor, alias = split_inner(inner)
        key = target.strip().replace("\\", "/").removesuffix(".md")
        if not local_scope and "/" not in key and not key.startswith("[支线任务]"):
            return match.group(0)
        new_target = mapping.get(key)
        if new_target is None:
            return match.group(0)
        replacements += 1
        suffix = f"|{alias}" if alias else ""
        return f"[[{new_target}{anchor}{suffix}]]"

    return WIKILINK_RE.sub(replace, text), replacements


def escape_table_aliases(text: str) -> tuple[str, int]:
    changed = 0
    lines: list[str] = []
    for line in text.splitlines(keepends=True):
        if not line.lstrip().startswith("|"):
            lines.append(line)
            continue

        def escape(match: re.Match[str]) -> str:
            nonlocal changed
            inner = match.group(1)
            if re.search(r"(?<!\\)\|", inner):
                changed += 1
                inner = re.sub(r"(?<!\\)\|", r"\|", inner, count=1)
            return f"[[{inner}]]"

        lines.append(WIKILINK_RE.sub(escape, line))
    return "".join(lines), changed


def clean_empty_dirs() -> list[Path]:
    removed: list[Path] = []
    for parent in (course_rel("03-Projects"), course_rel("知识地图")):
        if not parent.exists():
            continue
        for path in sorted(parent.rglob("*"), key=lambda item: len(item.parts), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                removed.append(path)
        if parent.exists() and not any(parent.iterdir()):
            parent.rmdir()
            removed.append(parent)
    return removed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="执行迁移；默认只显示计划")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not COURSE.exists() or not PROJECT.exists():
        raise SystemExit("Quant course/project roots are missing")
    if args.apply and not SNAPSHOT.exists():
        raise SystemExit(f"Recovery snapshot is required before apply: {SNAPSHOT}")

    conflicts = [(src, dst) for src, dst in MOVES if src.exists() and dst.exists()]
    if conflicts:
        for source, destination in conflicts:
            print(f"CONFLICT\t{source}\t{destination}")
        return 1

    active_moves = [(src, dst) for src, dst in MOVES if src.exists()]
    mapping = build_link_map()
    edits: list[tuple[Path, str, int, int]] = []
    for path in iter_markdown():
        text = path.read_text(encoding="utf-8-sig")
        local_scope = COURSE in path.parents or PROJECT in path.parents
        rewritten, link_count = rewrite_links(text, mapping, local_scope)
        if local_scope:
            rewritten, table_count = escape_table_aliases(rewritten)
        else:
            table_count = 0
        if rewritten != text:
            edits.append((path, rewritten, link_count, table_count))

    print(f"mode={'apply' if args.apply else 'dry-run'}")
    print(f"moves={len(active_moves)}")
    print(f"historical_files={len(HISTORICAL_FILES)}")
    print(f"link_files={len(edits)}")
    print(f"link_replacements={sum(row[2] for row in edits)}")
    print(f"table_alias_repairs={sum(row[3] for row in edits)}")
    for source, destination in active_moves:
        print(f"MOVE\t{rel(source)}\t{rel(destination)}")
    for path in HISTORICAL_FILES:
        print(f"ARCHIVE\t{rel(path)}\t{assignment_target(historical_number(path))}")
    for path, _, links, tables in edits:
        print(f"EDIT\t{rel(path)}\tlinks={links}\ttables={tables}")

    if not args.apply:
        return 0

    for path, rewritten, _, _ in edits:
        path.write_text(rewritten, encoding="utf-8", newline="\n")
    for source, destination in active_moves:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
    for path in HISTORICAL_FILES:
        if path.exists():
            path.unlink()
    for cache_name in ("__pycache__", ".pytest_cache"):
        for path in list(PROJECT.rglob(cache_name)) + list(COURSE.rglob(cache_name)):
            if path.is_dir():
                shutil.rmtree(path)
    removed_dirs = clean_empty_dirs()
    print(f"removed_empty_dirs={len(removed_dirs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
