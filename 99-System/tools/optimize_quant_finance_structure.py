#!/usr/bin/env python3
"""Consolidate duplicate quant-finance cards without deleting any source text.

The script is intentionally narrow: every changed source is copied to a dated
archive first, then the old Obsidian path becomes a stable index redirect.
"""
from __future__ import annotations

import re
from pathlib import Path


VAULT = Path(__file__).resolve().parents[2]
Q = VAULT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
ARCHIVE = VAULT / ".recovery-hold" / "quarantine" / "量化金融合并重复卡-2026-08-01"
TODAY = "2026-08-01"


def backup(path: Path) -> None:
    relative = path.relative_to(Q)
    target = ARCHIVE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(path.read_text(encoding="utf-8-sig"), encoding="utf-8")


def wiki_target(path: Path) -> str:
    return path.relative_to(Q).as_posix()[:-3]


def redirect(source: Path, target: Path, reason: str) -> None:
    backup(source)
    source.write_text(
        f'''---
type: index
topic: "{source.stem}：合并入口"
created: {TODAY}
updated: {TODAY}
status: merged
flow: knowledge
canonical: "[[{wiki_target(target)}]]"
tags: [量化金融, 合并入口, 索引]
---
# ↪ {source.stem}：已合并

> {reason}。为避免重复学习和双向链接失效，旧路径仅保留为稳定入口。

- 唯一主卡：[[{wiki_target(target)}|{target.stem}]]
- 原文归档：`{ARCHIVE / source.relative_to(Q)}`
''',
        encoding="utf-8",
    )


def normalize_identity(text: str, title: str) -> str:
    """Keep the stronger body while making filename, frontmatter and H1 agree."""
    if text.startswith("---"):
        text = re.sub(r"(?m)^title:\s*.*$", f'title: "{title}"', text, count=1)
        text = re.sub(r"(?m)^topic:\s*.*$", f'topic: "{title}"', text, count=1)
    text = re.sub(r"(?m)^#\s+.*$", f"# {title}", text, count=1)
    text = re.sub(r"(?m)^subagent_audit_score:\s*.*\n?", "", text)
    return text


def replace_with_stronger(target: Path, donor: Path, title: str, reason: str) -> None:
    backup(target)
    backup(donor)
    target.write_text(normalize_identity(donor.read_text(encoding="utf-8-sig"), title), encoding="utf-8")
    redirect(donor, target, reason)


def promote_to_stage(source: Path, target: Path, title: str) -> None:
    backup(source)
    backup(target)
    target.write_text(normalize_identity(source.read_text(encoding="utf-8-sig"), title), encoding="utf-8")
    redirect(source, target, "完整正文已迁入纵向阶段目录，并改用清晰主题名")


def append_case(source: Path, target: Path, heading: str) -> None:
    backup(source)
    backup(target)
    source_text = source.read_text(encoding="utf-8-sig")
    body = source_text.split("---", 2)[2].strip() if source_text.startswith("---") else source_text.strip()
    target_text = target.read_text(encoding="utf-8-sig").rstrip()
    marker = f"## {heading}"
    if marker not in target_text:
        target_text += f"\n\n---\n\n{marker}\n\n{body}\n"
        target.write_text(target_text, encoding="utf-8")
    redirect(source, target, "错名算例已并入对应理论主卡")


def reclassify_problem(path: Path) -> None:
    backup(path)
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"(?m)^type:\s*\S+", "type: problem", text, count=1)
    if re.search(r"(?m)^kind:\s*", text):
        text = re.sub(r"(?m)^kind:\s*\S+", "kind: problem-type", text, count=1)
    if re.search(r"(?m)^flow:\s*", text):
        text = re.sub(r"(?m)^flow:\s*\S+", "flow: review", text, count=1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    # Exact semantic duplicates: retain the clearer filename and the stronger body.
    replace_with_stronger(
        Q / "APT套利定价理论.md",
        Q / "🧠 APT 套利定价理论 (Arbitrage Pricing Theory).md",
        "APT 套利定价理论",
        "两张卡讲解同一 APT 模型，已保留内容更完整的版本",
    )
    replace_with_stronger(
        Q / "Fama-French三因子模型.md",
        Q / "🧠 Fama-French 三因子模型 (Fama-French Three-Factor Model).md",
        "Fama-French 三因子模型",
        "两张卡的定义、公式与例子高度重合",
    )
    replace_with_stronger(
        Q / "WACC加权平均资本成本.md",
        Q / "🧠 WACC 加权平均资本成本 (Weighted Average Cost of Capital).md",
        "WACC 加权平均资本成本",
        "两张卡讲解同一资本成本公式，已统一为单一主卡",
    )
    replace_with_stronger(
        Q / "多因子模型.md",
        Q / "多因子模型推导 笔记.md",
        "多因子模型：从暴露到截面回归",
        "推导卡与概念卡应按主题卡粒度合并，避免两套定义和公式并存",
    )

    # Root-level duplicates of canonical K-route cards.
    merge_map = {
        "信息比率 (Information Ratio) 深度学习笔记.md": "02-量化核心技能/策略评价指标.md",
        "分层回测 深度学习笔记.md": "03-策略开发与实战/分层回测.md",
        "标签设计 (Label Design).md": "03-策略开发与实战/标签设计.md",
        "滚动窗口与波动率特征 (Rolling Window & Volatility Characteristics).md": "01-夯实基础/滚动窗口与波动率特征.md",
        "时间序列验证 深度学习笔记.md": "02-量化核心技能/时间序列验证.md",
        "样本泄漏 (Data Leakage _ Look-ahead Bias).md": "02-量化核心技能/样本泄漏.md",
        "树模型基线 (Tree Model Baseline).md": "02-量化核心技能/树模型基线.md",
        "特征重要性 (Feature Importance).md": "03-策略开发与实战/特征重要性.md",
        "交易成本 深度学习笔记.md": "03-策略开发与实战/交易成本.md",
        "生存者偏差 (Survivorship Bias) 深度学习笔记.md": "03-策略开发与实战/生存者偏差.md",
        "收益率与对数收益率 (Simple Return vs Log Return).md": "01-夯实基础/收益率与对数收益率.md",
        "组合过拟合概率 PBO (Probability of Backtest Overfitting & CPCV in AFML).md": "03-策略开发与实战/组合过拟合概率PBO.md",
    }
    for source_name, target_name in merge_map.items():
        redirect(Q / source_name, Q / target_name, "该主题已有纳入 K01–K28 主线的阶段主卡")

    # Advanced cards belong in the vertical phase-4 directory, not in the root.
    for source_name, target_name, title in (
        ("风险约束下的RL 深度学习笔记.md", "04-深入精通/风险约束下的RL.md", "风险约束下的强化学习"),
        ("盘口特征 深度学习笔记.md", "04-深入精通/盘口特征.md", "盘口特征"),
        ("实盘风控 深度学习笔记.md", "04-深入精通/实盘风控.md", "实盘风控"),
        ("交易环境设计 深度学习笔记.md", "04-深入精通/交易环境设计.md", "交易环境设计"),
    ):
        promote_to_stage(Q / source_name, Q / target_name, title)

    # Recover useful material hidden behind meaningless filenames.
    append_case(
        Q / "for example0.md",
        Q / "协整关系与 Engle-Granger 两步法 (Cointegration & Engle-Granger Method).md",
        "完整算例：同行业股票的 Engle-Granger 两步法",
    )
    promote_to_stage(
        Q / "公式理解7.md",
        Q / "02-量化核心技能/Johansen检验.md",
        "Johansen 检验：协整秩、迹统计量与最大特征值统计量",
    )

    # This page is explicitly a problem-type collection, not a concept card.
    reclassify_problem(Q / "夯实基础常见题型 (量化金融基石).md")

    print(f"Structure optimization complete. Backups: {ARCHIVE}")


if __name__ == "__main__":
    main()
