#!/usr/bin/env python3
"""Repair explicit and uniquely resolvable wikilinks in the quant course/project."""
from __future__ import annotations

import argparse
import difflib
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "03-量化金融"
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融"
SNAPSHOT = ROOT / ".recovery-hold" / "2026-08-06" / "quant-finance-comprehensive"
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
SKIP = {".git", ".obsidian", ".recovery-hold", ".pytest_cache", "__pycache__", "🗄️ 归档", ".归档"}


MANUAL = {
    "00-前置知识/🧭 阶段0-先修诊断": "02-Knowledge/🧠 学习系统/03-量化金融/00-前置知识/🧭 阶段0-先修诊断与研究协议",
    "🧭 阶段0-先修诊断": "02-Knowledge/🧠 学习系统/03-量化金融/00-前置知识/🧭 阶段0-先修诊断与研究协议",
    "02-Knowledge/🧠 学习系统/03-量化金融/00-前置知识/🧭 阶段0-先修诊断": "02-Knowledge/🧠 学习系统/03-量化金融/00-前置知识/🧭 阶段0-先修诊断与研究协议",
    "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/🧠 夏普比率 (Sharpe Ratio)": "02-Knowledge/🧠 学习系统/03-量化金融/03-研究验证与稳健性/策略评价指标",
    "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho)": "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)",
    "02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/ARIMA模型": "02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典预测模型/ARIMA模型",
    "02-Knowledge/🧠 学习系统/02-时间序列分析/01-基础认知层/时间索引与频率": "02-Knowledge/🧠 学习系统/02-时间序列分析/01-时序结构与数据契约/时间索引与频率",
    "ML 如何规范地进入金融建模常见题型": "03-Projects/金融与时序/03-量化金融/大作业/量化金融-大作业-AAPL贯穿式量化研究",
    "奖励函数设计 (Reward Function Design)": "02-Knowledge/🧠 学习系统/03-量化金融/04-深入精通/风险约束下的RL",
    "期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho)": "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)",
    "🧠 夏普比率 (Sharpe Ratio)": "02-Knowledge/🧠 学习系统/03-量化金融/03-研究验证与稳健性/策略评价指标",
    "RL 交易实验常见题型": "02-Knowledge/🧠 学习系统/03-量化金融/04-深入精通/风险约束下的RL",
    "低延迟系统设计与 C++_FPGA 极致性能优化 (Low-Latency System Design & C++_FPGA Optimization)": "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/高频交易系统架构与模块解耦设计 (High-Frequency Trading System Architecture)",
    "信息交易模型推导 (Kyle 1985 经典单期模型)": "02-Knowledge/🧠 学习系统/03-量化金融/04-深入精通/信息交易模型与 VPIN 毒性订单流度量 (Information-Based Models & VPIN)",
    "03-Projects/开源课程课后习题/README": "03-Projects/金融与时序/03-量化金融/课后作业/MIT-OCW-18S096-来源与作答说明",
    "03-Projects/开源课程课后习题/PS01-线性代数与概率基础": "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-01-线性代数与概率基础",
    "03-Projects/开源课程课后习题/PS02-回归与CAPM": "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-02-回归与CAPM",
    "03-Projects/开源课程课后习题/PS03-时间序列与波动率": "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-03-时间序列与波动率",
    "03-Projects/开源课程课后习题/PS04-组合与因子模型": "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-04-组合与因子模型",
    "03-Projects/开源课程课后习题/PS05-随机微积分与SDE": "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-05-随机微积分与SDE",
    "知识地图/🗺️ 量化金融全栈终极框架 (Academic + AFML + HFT)": "02-Knowledge/🧠 学习系统/03-量化金融/04-深入精通/量化金融-全栈资产地图",
    "夏普比率": "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/🧠 夏普比率 (Sharpe Ratio)",
    "🧠 量化金融李宏毅式实战作业总索引": "03-Projects/金融与时序/03-量化金融/🧭 课程作业总索引",
    "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/分层回测": "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/回测框架与无泄漏实验",
    "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/历史模拟VaR": "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)",
    "02-Knowledge/🧠 学习系统/03-量化金融/18-实战作业说明书/HW17-Qlib因子研究与成本敏感回测作业说明书": "03-Projects/金融与时序/03-量化金融/大作业/量化金融-大作业-Qlib因子研究与成本敏感回测",
    "03-Projects/HW01-CAPM/README": "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-01-CAPM与Alpha检验",
    "03-Projects/Phase2-GARCH/README": "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-06-GARCH波动率与动态VaR",
    "03-Projects/HW06-DynamicVaR/README": "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-06-GARCH波动率与动态VaR",
    "03-Projects/HW05-BSM/README": "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-05-Black-Scholes定价与对冲",
    "开源课程课后习题/README": "03-Projects/金融与时序/03-量化金融/课后作业/MIT-OCW-18S096-来源与作答说明",
}

MOVED_COURSE_PREFIXES = ("00-前置知识/", "01-夯实基础/", "02-量化核心技能/", "04-深入精通/")


def iter_markdown(root: Path) -> list[Path]:
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        dirnames[:] = [name for name in dirnames if name not in SKIP]
        paths.extend(current / name for name in filenames if name.endswith(".md"))
    return paths


ALL_MD = iter_markdown(ROOT)
STEMS: dict[str, list[Path]] = defaultdict(list)
for markdown in ALL_MD:
    STEMS[markdown.stem].append(markdown)


def split_inner(inner: str) -> tuple[str, str, str, str]:
    pipe = re.search(r"\\\||(?<!\\)\|", inner)
    alias = ""
    alias_separator = ""
    if pipe:
        alias_separator = pipe.group(0)
        alias = inner[pipe.end():]
        inner = inner[:pipe.start()]
    if "#" in inner:
        target, anchor = inner.split("#", 1)
        return target.strip(), f"#{anchor}", alias, alias_separator
    return inner.strip(), "", alias, alias_separator


def exists(source: Path, target: str) -> bool:
    candidate = Path(*target.replace("\\", "/").split("/"))
    if candidate.suffix.lower() != ".md":
        candidate = candidate.with_suffix(".md")
    return (source.parent / candidate).exists() or (ROOT / candidate).exists() or (COURSE / candidate).exists()


def target_for(source: Path, target: str) -> str | None:
    key = target.replace("\\", "/").removesuffix(".md")
    if key in MANUAL:
        return MANUAL[key]
    if key.startswith(MOVED_COURSE_PREFIXES):
        candidate = COURSE.joinpath(*key.split("/"))
        if candidate.suffix.lower() != ".md":
            candidate = candidate.with_suffix(".md")
        if candidate.exists():
            return candidate.relative_to(ROOT).with_suffix("").as_posix()
    if exists(source, key):
        return None
    if "/" not in key:
        return None
    if key.startswith(("03-Projects/", "../")):
        return None
    if key.startswith("../"):
        key = key[3:]
    for base in (COURSE, PROJECT):
        candidate = base.joinpath(*key.split("/"))
        if candidate.suffix.lower() != ".md":
            candidate = candidate.with_suffix(".md")
        if candidate.exists():
            return candidate.relative_to(ROOT).with_suffix("").as_posix()
    stem = Path(key).name
    local_matches = [path for path in STEMS.get(stem, []) if COURSE in path.parents or PROJECT in path.parents]
    if len(local_matches) == 1:
        return local_matches[0].relative_to(ROOT).with_suffix("").as_posix()
    return None


def repair(path: Path, text: str) -> tuple[str, int]:
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        target, anchor, alias, alias_separator = split_inner(match.group(1))
        new = target_for(path, target)
        if not new:
            return match.group(0)
        count += 1
        return f"[[{new}{anchor}{alias_separator + alias if alias else ''}]]"

    return WIKILINK_RE.sub(replace, text), count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--print-patch", action="store_true")
    args = parser.parse_args()
    if args.apply and not SNAPSHOT.exists():
        raise SystemExit(f"Missing recovery snapshot: {SNAPSHOT}")
    edits = []
    for root in (COURSE, PROJECT):
        for path in iter_markdown(root):
            old = path.read_text(encoding="utf-8-sig")
            new, count = repair(path, old)
            if new != old:
                edits.append((path, new, count))
    print(f"mode={'apply' if args.apply else 'dry-run'}")
    print(f"files={len(edits)}")
    print(f"replacements={sum(item[2] for item in edits)}")
    for path, _, count in edits:
        print(f"EDIT\t{path.relative_to(ROOT)}\t{count}")
    if args.print_patch:
        print("*** Begin Patch")
        for path, new, _ in edits:
            old = path.read_text(encoding="utf-8-sig")
            print(f"*** Update File: {path}")
            diff = difflib.unified_diff(
                old.splitlines(),
                new.splitlines(),
                fromfile=str(path),
                tofile=str(path),
                lineterm="",
            )
            for line in list(diff)[2:]:
                print("@@" if line.startswith("@@") else line)
        print("*** End Patch")
        return 0
    if not args.apply:
        return 0
    for path, new, _ in edits:
        path.write_text(new, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
