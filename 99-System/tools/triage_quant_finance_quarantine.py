#!/usr/bin/env python3
"""Give every quarantined quant-finance card a concrete canonical destination."""
from __future__ import annotations

import csv
import re
from pathlib import Path


VAULT = Path(__file__).resolve().parents[2]
Q = VAULT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
ARCHIVE = VAULT / ".recovery-hold" / "quarantine" / "量化金融未达标知识卡-2026-08-01"
OUT_DIR = VAULT / "99-System" / "🗄️ 归档" / "知识库审计"
OUT_MD = OUT_DIR / "quant_finance_quarantine_triage_2026-08-01.md"
OUT_CSV = OUT_DIR / "quant_finance_quarantine_triage_2026-08-01.csv"


M = {
    "01-夯实基础/ROE拆解与杜邦分析.md": "ROE 拆解与杜邦分析 (DuPont Analysis)",
    "01-夯实基础/保证金与杠杆.md": "动态下注规模与凯利公式 (Bet Sizing & Kelly Criterion in AFML)",
    "01-夯实基础/订单类型与成交机制.md": "订单类型与交易所连续竞价撮合机制 (Order Types & Continuous Double Auction)",
    "01-夯实基础/利润表与利润质量.md": "Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)",
    "01-夯实基础/利润质量与现金流背离.md": "Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)",
    "01-夯实基础/三大报表关系.md": "三大财务报表钩稽关系 (Interrelationship of Financial Statements)",
    "01-夯实基础/现金流量表与利润背离.md": "三大财务报表钩稽关系 (Interrelationship of Financial Statements)",
    "01-夯实基础/相关系数、协方差与分散化.md": "相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)",
    "01-夯实基础/远期、期货与期权的区别.md": "Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)",
    "01-夯实基础/资产负债表的风险信号.md": "Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)",
    "01-夯实基础/资产类别与交易场所.md": "订单类型与交易所连续竞价撮合机制 (Order Types & Continuous Double Auction)",
    "02-量化核心技能/ACF与PACF.md": "ACF 自相关函数与 PACF 偏自相关函数 (Autocorrelation & Partial Autocorrelation Functions)",
    "02-量化核心技能/ARCH效应.md": "量化金融-GARCH波动率策略",
    "02-量化核心技能/ARIMA模型.md": "量化金融-ARIMA策略应用",
    "02-量化核心技能/Black-Scholes.md": "Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)",
    "02-量化核心技能/GARCH模型.md": "量化金融-GARCH波动率策略",
    "02-量化核心技能/Greeks.md": "高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)",
    "02-量化核心技能/Johansen检验.md": "02-量化核心技能/Johansen检验",
    "02-量化核心技能/Monte Carlo VaR.md": "蒙特卡洛模拟法 VaR (Monte Carlo Simulation VaR)",
    "02-量化核心技能/波动率聚集.md": "量化金融-GARCH波动率策略",
    "02-量化核心技能/参数法VaR.md": "参数法VaR（方差-协方差法）",
    "02-量化核心技能/残差诊断.md": "量化金融-ARIMA策略应用",
    "02-量化核心技能/单位根检验.md": "单位根检验与 ADF 检验 (Unit Root & Augmented Dickey-Fuller Test)",
    "02-量化核心技能/二叉树定价.md": "二叉树期权定价模型 (Binomial Option Pricing Model)",
    "02-量化核心技能/历史模拟VaR.md": "历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)",
    "02-量化核心技能/收益率序列的风格化事实.md": "非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)",
    "02-量化核心技能/特征工程.md": "03-策略开发与实战/特征工程-量化应用",
    "02-量化核心技能/尾部风险.md": "极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)",
    "02-量化核心技能/误差修正模型.md": "量化金融-ECM套利策略",
    "02-量化核心技能/协整.md": "协整关系与 Engle-Granger 两步法 (Cointegration & Engle-Granger Method)",
    "02-量化核心技能/压力测试.md": "CVaR条件风险价值",
    "02-量化核心技能/隐含波动率.md": "隐含波动率与波动率微笑 (Implied Volatility & Volatility Smile)",
    "02-量化核心技能/远期与期货定价.md": "Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)",
    "04-深入精通/订单生命周期.md": "04-深入精通/交易环境设计",
    "04-深入精通/风险约束下的RL.md": "04-深入精通/风险约束下的RL",
    "04-深入精通/奖励函数设计.md": "04-深入精通/风险约束下的RL",
    "04-深入精通/交易环境设计.md": "04-深入精通/交易环境设计",
    "04-深入精通/盘口特征.md": "04-深入精通/盘口特征",
    "04-深入精通/实盘风控.md": "04-深入精通/实盘风控",
    "ML 如何规范地进入金融建模常见题型.md": "🧩 Qlib 项目知识点—作业—验收路线图",
    "Pandas分组聚合与透视表 深度学习笔记.md": "01-夯实基础/Pandas分组聚合与透视表",
    "regression='c' 代表模型A(常数项突变), 't' 代表模型B(趋势突变), 'ct' 代表模型C(双重突变).md": "单位根检验与 ADF 检验 (Unit Root & Augmented Dickey-Fuller Test)",
    "RL 交易实验常见题型.md": "04-深入精通/风险约束下的RL",
    "🧠 马科维茨均值-方差模型 (Markowitz Mean-Variance Model).md": "相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)",
    "🧠 夏普比率 (Sharpe Ratio).md": "02-量化核心技能/策略评价指标",
    "🧠 詹森 Alpha (Jensen's Alpha).md": "CAPM 资本资产定价模型",
    "表格理解.md": "配对交易与统计套利 (Pairs Trading & Statistical Arbitrage)",
    "低延迟系统设计与 C++_FPGA 极致性能优化 (Low-Latency System Design & C++_FPGA Optimization).md": "高频交易系统架构与模块解耦设计 (High-Frequency Trading System Architecture)",
    "订单生命周期 深度学习笔记.md": "04-深入精通/交易环境设计",
    "滑点模型 (Slippage Model) 深度学习笔记.md": "03-策略开发与实战/滑点模型",
    "换手率调和收益 (Turnover-Adjusted Return) 深度学习笔记.md": "03-策略开发与实战/换手率调和收益",
    "奖励函数设计 (Reward Function Design).md": "04-深入精通/风险约束下的RL",
    "理解32.md": "量化金融-ECM套利策略",
    "量化-策略评估与回测.md": "02-量化核心技能/策略评价指标",
    "量化核心技能常见题型 深度学习笔记.md": "🧩 Qlib 项目知识点—作业—验收路线图",
    "期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho).md": "高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)",
    "前视偏差 深度学习笔记.md": "03-策略开发与实战/前视偏差",
    "夏普比率.md": "02-量化核心技能/策略评价指标",
    "信息交易模型推导 (Kyle 1985 经典单期模型).md": "信息交易模型与 VPIN 毒性订单流度量 (Information-Based Models & VPIN)",
    "知识地图/CVaR.md": "CVaR条件风险价值",
}


def add_resolution(pointer: Path, target: str) -> None:
    if not pointer.exists():
        return
    text = pointer.read_text(encoding="utf-8-sig")
    # Rebuilt stage pages are no longer quarantine pointers; do not alter them.
    if "quality_gate: failed" not in text:
        return
    if "triage_decision:" not in text:
        text = text.replace("quality_gate: failed\n", f'quality_gate: failed\ntriage_decision: merged\ncanonical: "[[{target}]]"\n', 1)
    marker = "## 处理结论"
    if marker not in text:
        text = text.rstrip() + f"\n\n{marker}\n\n- 决策：**合并，不重建第二张主卡**。\n- 唯一主卡：[[{target}]]\n- 理由：主题已由内容更完整、路径更清晰的主卡覆盖；继续维护两份会造成检索竞争与重复复习。\n"
    pointer.write_text(text, encoding="utf-8")


def main() -> None:
    originals = sorted(p for p in ARCHIVE.rglob("*.md"))
    actual = {p.relative_to(ARCHIVE).as_posix() for p in originals}
    if actual != set(M):
        raise RuntimeError(f"Triage map mismatch: missing={sorted(actual-set(M))}, extra={sorted(set(M)-actual)}")

    rows = []
    for original in originals:
        rel = original.relative_to(ARCHIVE).as_posix()
        target = M[rel]
        target_file = Q / f"{target}.md"
        if not target_file.exists():
            raise FileNotFoundError(target_file)
        add_resolution(Q / rel, target)
        rows.append({
            "原隔离卡": rel,
            "决策": "合并到唯一主卡",
            "唯一主卡": target,
            "原文归档": str(original),
        })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# 量化金融隔离卡逐张处置清单",
        "",
        "> 日期：2026-08-01。原则：不删除原文、不恢复低质副本；每个概念只指定一张唯一主卡。",
        "",
        f"- 已处置：**{len(rows)} / {len(rows)}**",
        "- 处置方式：全部有明确主卡承接；原始文本继续保存在质量归档，旧路径保留稳定入口。",
        "- 认知负荷治理：学习者只进入主线主卡，隔离卡不再制造第二套定义、第二套作业或第二套复习队列。",
        "",
        "| 原隔离卡 | 决策 | 唯一主卡 |",
        "|:---|:---|:---|",
    ]
    for row in rows:
        lines.append(f"| `{row['原隔离卡']}` | {row['决策']} | [[{row['唯一主卡']}]] |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Triaged {len(rows)} quarantined cards. Manifest: {OUT_MD}")


if __name__ == "__main__":
    main()
