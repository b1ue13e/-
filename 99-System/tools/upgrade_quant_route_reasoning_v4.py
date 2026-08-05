#!/usr/bin/env python3
"""Add a compact, card-specific definition→derivation→contrast chain."""
from __future__ import annotations

from pathlib import Path


VAULT = Path(__file__).resolve().parents[2]
Q = VAULT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
MARKER = "<!-- quant-route-reasoning-v4 -->"


ITEMS = {
    "01-夯实基础/OHLCV字段清洗与复权.md": ("OHLCV字段清洗与复权", "原始成交价、复权价格和总回报序列的区别决定了收益能否守恒；从公司行动现金流推导调整因子，而不是对跳空做经验平滑"),
    "01-夯实基础/Pandas分组聚合与透视表.md": ("Pandas分组聚合与透视表", "`transform` 保持行粒度而 `agg` 改变粒度；从键的函数依赖推导输出行数，并与 `pivot` 不允许重复键的定义对比"),
    "01-夯实基础/滚动窗口与波动率特征.md": ("滚动窗口与波动率特征", "从信息集 $\mathcal F_t$ 推导窗口右端约束，并对比扩展窗口与固定窗口在估计方差和制度漂移下的取舍"),
    "02-量化核心技能/树模型基线.md": ("树模型基线", "从节点纯度下降推导分裂收益，再对比训练误差持续下降与 walk-forward 误差反弹，从而识别容量过拟合"),
    "02-量化核心技能/样本泄漏.md": ("样本泄漏", "用信息集包含关系定义泄漏：训练步骤读到部署时不可得变量；再与合法的历史滞后特征对比，边界由 `available_at` 判定"),
    "03-策略开发与实战/分层回测.md": ("分层回测", "从当期横截面排序推导组别，再对比分层单调性与单个多空组合收益，避免把一个极端组的偶然收益当稳定排序能力"),
    "03-策略开发与实战/交易成本.md": ("交易成本", "从决策价到最终持仓价值逐项推导 implementation shortfall，并对比显性费用、价差、冲击和机会成本的不同规模律"),
    "03-策略开发与实战/滑点模型.md": ("滑点模型", "从可成交盘口而非中间价定义成交基准，再对比固定基点与参与率冲击模型，从而暴露大单和薄盘口的非线性成本"),
    "03-策略开发与实战/特征工程-量化应用.md": ("特征工程-量化应用", "从原始字段的可得时点推导特征信息集，并对比同一公式在公告日、停牌日与普通交易日的不同经济含义"),
    "03-策略开发与实战/特征重要性.md": ("特征重要性", "从置换后损失增量定义模型依赖，再与分裂增益和因果效应对比；相关特征会分摊贡献，因此必须成组消融"),
    "03-策略开发与实战/因子标准化.md": ("因子标准化", "从当日可比集合定义中心与尺度，再对比 z-score、MAD 和秩变换对尾部信息的保留程度"),
    "03-策略开发与实战/因子评价：IC、Rank IC 与 ICIR.md": ("因子评价：IC、Rank IC 与 ICIR", "从逐期截面相关推导 IC 时间序列，再对比 Pearson IC 与 Rank IC 的线性和单调性假设；ICIR 还需修正自相关"),
    "03-策略开发与实战/因子选择：价值、质量与动量.md": ("因子选择：价值、质量与动量", "从三类因子的经济机制推导预期暴露，再对比独立显著与组合增量；共同微盘或行业暴露不构成互补性"),
}


def main() -> None:
    changed = 0
    for relative, (topic, chain) in ITEMS.items():
        path = Q / relative
        text = path.read_text(encoding="utf-8-sig")
        if MARKER in text:
            continue
        block = f'''\n\n{MARKER}\n### 定义—推导—对比复核\n\n**{topic}** 的定义必须能落到数据列和时点，而不能只停留在术语。{chain}。因此，对 **{topic}** 的误区检查要同时保留正例、破坏条件后的反例和样本外结果；只要三者不能形成同一因果链，就暂不判定掌握。\n'''
        path.write_text(text.rstrip() + block, encoding="utf-8")
        changed += 1
    print(f"Added reasoning chains to {changed} route cards.")


if __name__ == "__main__":
    main()
