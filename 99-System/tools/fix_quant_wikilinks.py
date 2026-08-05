#!/usr/bin/env python3
"""Rewrite stale quant-finance wikilinks to canonical existing notes."""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
QUANT = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
CODE_BLOCK_RE = re.compile(r"```.*?```", re.S)
WIKILINK_RE = re.compile(r"(!?)\[\[(.*?)\]\]")


ALIASES: dict[str, str] = {}


def aliases(canonical: str, *names: str) -> None:
    for name in names:
        ALIASES[name] = canonical


aliases(
    "🗺️ 量化金融学习路径",
    "🗺️ 学习路径",
)
aliases("00-课程说明与先修诊断", "投资学基础")
aliases(
    "00-每周学习执行卡",
    "🧑‍🏫 量化金融老师视角教学设计与作业节奏",
)
aliases(
    "03-Projects/Capstone-统一标的贯穿实战项目",
    "🧩 Qlib 项目知识点—作业—验收路线图",
)
aliases("📚 教材挂载索引", "📗 第二阶段：量化核心技能")
aliases(
    "00-零基础补救-数学统计与Python",
    "微积分",
    "概率论与数理统计",
    "线性代数",
    "Python数据分析",
    "Statsmodels与Pandas基础",
    "时间序列分析基础",
)
aliases(
    "收益率与对数收益率",
    "资产收益率计算",
    "期望收益与方差",
    "收益率分布与厚尾",
)
aliases(
    "相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)",
    "协方差矩阵运算",
)
aliases(
    "CAPM 资本资产定价模型",
    "CAPM资本资产定价模型",
    "CAPM",
    "CAPM与APT模型",
    "纯Alpha对冲策略",
    "统计套利与Beta中性",
)
aliases(
    "🧠 夏普比率 (Sharpe Ratio)",
    "夏普比率",
    "夏普比率与信息比率",
)
aliases(
    "马科维茨有效前沿",
    "马科维茨组合优化与有效前沿",
    "马科维茨投资组合理论",
    "马科维茨优化",
    "投资组合优化进阶",
    "量化母基金FOF资产配置",
    "期望收益与方差",
)
aliases(
    "量化金融-资产定价-多因子模型",
    "APT套利定价理论",
    "多因子模型",
    "CAPM与APT模型",
    "多因子风险模型",
    "多因子选股模型",
    "多因子组合构建",
    "量化因子评价体系",
)
aliases(
    "Fama-French三因子模型",
    "因子模型与Fama-French三因子",
)
aliases(
    "Fama-MacBeth 两步回归法 (Fama-MacBeth Two-Step Regression)",
    "Fama-MacBeth两步回归",
    "面板数据分析",
    "Newey-West调整",
    "Newey-West标准误调整",
)
aliases(
    "因子预处理：去极值、中性化与标准化 (Factor Preprocessing_ Winsorization, Neutralization & Z-Score)",
    "因子标准化",
    "03-策略开发与实战/因子构造",
)
aliases(
    "价值因子与 HML 账面市值比溢价 (Value Factor & HML)",
    "价值因子",
)
aliases(
    "质量因子与 QMJ 盈利能力溢价 (Quality Factor & QMJ - Quality Minus Junk)",
    "质量因子",
)
aliases(
    "趋势跟踪策略框架与 CTA 交易哲学 (Trend-Following Framework & CTA Trading)",
    "动量因子",
    "趋势跟踪框架",
    "均线与突破",
)
aliases(
    "均值回归策略 (Mean-Reversion Trading Strategy)",
    "均值回归策略",
    "ZScore信号",
    "半衰期",
    "ACF与PACF",
)
aliases(
    "配对交易与统计套利 (Pairs Trading & Statistical Arbitrage)",
    "配对交易",
    "配对交易与统计套利",
    "统计套利与对冲",
)
aliases(
    "动态下注规模与凯利公式 (Bet Sizing & Kelly Criterion in AFML)",
    "下注规模",
    "Kelly下注规模",
    "Kelly公式(凯利公式)",
)
aliases(
    "动态止损机制与风险平价仓位管理 (Stop-Loss Mechanisms & Risk-Parity Position Sizing)",
    "止损与仓位",
    "风险平价策略(Risk Parity)",
)
aliases(
    "回测框架与无泄漏实验",
    "分层回测",
    "事件驱动回测",
    "量化回测框架",
    "量化回测框架开发",
    "量化-策略评估与回测",
    "组合风险管理",
    "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/回测偏差五层审计",
)
aliases(
    "策略回测前视偏差与生存者偏差防范审计 (Look-Ahead & Survivorship Bias Audit)",
    "前视偏差",
    "生存者偏差",
    "过度拟合与多重检验",
)
aliases("样本泄漏", "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/标签设计")
aliases(
    "时间序列验证",
    "交叉验证",
    "Walk-Forward Optimization (WFO)",
    "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/Purged CV",
)
aliases(
    "PBO回测过拟合概率与Deflated Sharpe Ratio (Probability of Backtest Overfitting)",
    "组合过拟合概率PBO",
    "CPCV组合净化交叉验证",
    "多重测试困境",
    "Deflated Sharpe Ratio",
)
aliases("Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)", "Purged CV")
aliases(
    "滚动窗口与波动率特征",
    "金融时间序列特征",
    "时间序列特征工程",
    "特征工程-量化应用",
    "特征工程实战",
    "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/特征工程-量化应用",
    "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/特征重要性",
    "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/量化预测",
)
aliases(
    "单位根检验与 ADF 检验 (Unit Root & Augmented Dickey-Fuller Test)",
    "时间序列平稳性检验",
)
aliases("协整关系与 Engle-Granger 两步法 (Cointegration & Engle-Granger Method)", "协整关系与Engle-Granger两步法", "公式理解7")
aliases("极大似然估计", "极大似然估计MLE")
aliases(
    "量化金融-波动率-GARCH家族模型",
    "GARCH族波动率模型",
    "GARCH模型实战",
    "量化金融-GARCH波动率策略",
)
aliases(
    "非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)",
    "非对称GARCH",
    "EGARCH与非对称波动率",
)
aliases(
    "参数法VaR（方差-协方差法）",
    "VaR风险价值回测",
    "VaR的回测检验(Kupiec)",
)
aliases(
    "历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)",
    "历史模拟法VaR",
)
aliases(
    "量化金融-风险管理-期望损失分解与ES理论",
    "CVaR条件风险价值",
    "Expected_Shortfall_ES",
    "VaR与CVaR基础",
)
aliases(
    "极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)",
    "肥尾分布",
    "尾部风险对冲策略",
    "压力测试与情景分析",
)
aliases(
    "Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)",
    "Black-Scholes期权定价模型",
    "Black-Scholes微分方程",
)
aliases(
    "隐含波动率与波动率微笑 (Implied Volatility & Volatility Smile)",
    "波动率微笑",
    "隐含波动率微笑",
    "Implied Volatility",
    "期权隐含波动率偏斜",
    "期权定价与波动率微笑",
    "期权定价与隐含波动率微笑",
)
aliases(
    "期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho)",
    "Delta对冲",
    "Gamma Hedging",
)
aliases("高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)", "高级希腊字母对冲")
aliases("量化金融-衍生品-蒙特卡洛期权定价与方差缩减", "Monte Carlo Simulation")
aliases("量化金融-随机过程-伊藤引理与随机微分方程", "布朗运动基础", "几何布朗运动", "Ito引理", "布朗运动与维纳过程", "Risk-Neutral Measure")
aliases(
    "三大财务报表钩稽关系 (Interrelationship of Financial Statements)",
    "三大报表关系",
    "财务报表分析",
    "财报三表科目映射",
)
aliases("Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)", "Altman Z-Score破产模型")
aliases("Pandas分组聚合与透视表", "Pandas数据处理", "Pandas向量化运算")
aliases("OHLCV字段清洗与复权", "数据清洗与预处理", "数据清洗基础")
aliases("Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)", "Meta-labeling", "标签设计")
aliases(
    "Volume Bars与Dollar Bars信息驱动采样 (Information-Driven Bars)",
    "采样引擎",
    "高频数据清洗",
    "微观不平衡指标(VIB)",
    "流式数据处理",
    "Tick Data",
    "Fractional Differentiation (分数阶差分)",
)
aliases(
    "买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)",
    "市场微观结构与买卖价差",
    "微观市场结构",
)
aliases(
    "限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)",
    "订单簿与L2微观结构",
    "限价指令簿LOB",
    "订单簿机制(LOB)",
    "金融数据结构",
    "LOB数据",
    "逐笔数据处理(Level-3)",
)
aliases(
    "盘口特征",
    "强化学习的订单簿状态表示",
    "DeepLOB预测模型",
    "DeepLOB盘口预测",
)
aliases("订单流不平衡 (Order Flow Imbalance, OFI)", "微观不平衡指标(VIB)")
aliases(
    "Almgren-Chriss最优拆单",
    "最优执行-Almgren-Chriss",
    "AC最优拆单",
    "基于强化学习的拆单(RL Execution)",
)
aliases(
    "Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型",
    "Implementation Shortfall",
    "滑点模型",
    "交易成本分析TCA",
    "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/交易成本",
)
aliases("市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)", "市场冲击模型")
aliases("TWAP 时间加权平均价格 (Time-Weighted Average Price)", "TWAP与VWAP算法", "算法交易VWAP/TWAP", "VWAP与TWAP算法")
aliases("VWAP 成交量加权平均价格 (Volume-Weighted Average Price)", "VWAP算法实现")
aliases(
    "量化金融-执行策略-暗池撮合与SOR智能路由",
    "暗池交易与智能订单路由 SOR (Dark Pools & Smart Order Routing)",
    "暗池与ATS",
    "订单流支付PFOF",
)
aliases(
    "跨市场排队优先权与挂单成交概率 (Queue Position & Fill Probability in High-Frequency Trading)",
    "高频交易执行算法",
    "回测系统撮合引擎",
)
aliases(
    "高频交易系统架构与模块解耦设计 (High-Frequency Trading System Architecture)",
    "高频交易(HFT)基础",
)
aliases(
    "低延迟系统设计与 C++_FPGA 极致性能优化 (Low-Latency System Design & C++_FPGA Optimization)",
    "金融网络延迟与微波架构",
)
aliases(
    "金融MDP设计与奖励函数工程 (Financial MDP & Reward Engineering)",
    "强化学习在量化的应用",
    "强化学习基础",
    "PPO在量化中的应用",
    "Reward奖励设计",
    "强化学习在最优执行中的应用",
    "马尔可夫决策过程(MDP)",
    "Stable-Baselines3实战",
    "VecEnv向量化环境",
)
aliases("奖励函数设计 (Reward Function Design)", "差分夏普比率(DSR)")
aliases(
    "实盘风控",
    "量化风控系统级部署",
    "风控系统开发",
    "实盘策略风控模块",
    "实盘策略上架规范",
    "实盘交易系统",
)
aliases(
    "做市商库存模型与 Avellaneda-Stoikov 框架 (Inventory Models & Avellaneda-Stoikov Framework)",
    "高频做市商(MM)策略",
    "做市商策略(Market Making)",
    "期权做市策略",
)
aliases("协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)", "RMT去噪", "高级协方差缩减(Shrinkage)")
aliases("HRP分层风险平价", "HRP")
aliases("策略评价指标", "量化回测评价指标", "策略归因分析", "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/因子评价：IC、Rank IC 与 ICIR")
aliases("最大回撤", "02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/换手率调和收益")
aliases("Qlib回测工作流(Qlib Workflow)", "机器学习在金融中的应用", "Financial Machine Learning")
aliases("量化金融-动态最优化-3-Merton最优消费问题应用", "效用函数与均值方差分析")
aliases("03-Projects/开源课程课后习题/README", "开源课程课后习题/README")
aliases(
    "单位根检验与 ADF 检验 (Unit Root & Augmented Dickey-Fuller Test)",
    "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/单位根检验",
)
aliases(
    "03-Projects/Capstone-统一标的贯穿实战项目",
    "A01-数据协议与无泄漏审计",
)
aliases(
    "量化金融-平稳性与单位根检验实战",
    "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/ARIMA模型",
)
aliases(
    "量化金融-波动率-GARCH家族模型",
    "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/GARCH模型",
)
aliases("量化金融-动态最优化-1-贝尔曼方程直觉与离散推导", "MDP与贝尔曼方程")
aliases("金融MDP设计与奖励函数工程 (Financial MDP & Reward Engineering)", "PPO近端策略优化")
aliases(
    "🧭 开源作业体系-量化金融",
    "03-Projects/33门课程作业来源审计总表",
    "03-Projects/projects-quant/量化金融_4Tier阶梯作业全景规范说明书",
)
aliases("Qlib回测工作流(Qlib Workflow)", "A04-E2-Qlib-LightGBM")
aliases("PS04-组合与因子模型", "主成分分析PCA", "PCA主成分分析")
aliases(
    "📚 教材挂载索引",
    "02-Knowledge/MOC/开放教材主线注册表",
    "02-Knowledge/MOC/权威课程与作业来源白名单",
)
aliases(
    "02-Knowledge/🧠 学习系统/02-时间序列分析/🗺️ 时间序列分析学习路径",
    "02-时间序列分析/🗺️ 时间序列分析学习路径",
)
aliases(
    "协整关系与 Engle-Granger 两步法 (Cointegration & Engle-Granger Method)",
    "02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/误差修正模型",
)
aliases(
    "量化金融-风险管理-期望损失分解与ES理论",
    "风险管理与定价",
    "压力测试 (Stress Testing)",
)
aliases("00-零基础补救-数学统计与Python", "02-Knowledge/🧠 学习系统/09-高等代数/🗺️ 高等代数学习路径")


def normalize(value: str) -> str:
    return re.sub(r"[\W_]+", "", value, flags=re.UNICODE).lower()


def stem_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for path in QUANT.rglob("*.md"):
        index.setdefault(normalize(path.stem), []).append(path.stem)
    return index


def canonical_for(target: str, stems: dict[str, list[str]]) -> str | None:
    if target in ALIASES:
        return ALIASES[target]
    normalized = normalize(Path(target).name)
    exact = stems.get(normalized, [])
    if len(exact) == 1:
        return exact[0]
    candidates = [
        stem
        for key, values in stems.items()
        if normalized and (normalized in key or key in normalized)
        for stem in values
    ]
    candidates = sorted(set(candidates), key=lambda item: (len(normalize(item)), item))
    if len(candidates) == 1:
        return candidates[0]
    return None


def global_stem_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    skip = {".git", ".obsidian", ".recovery-hold", ".tmp", "__pycache__", "site-packages"}
    for path in ROOT.rglob("*.md"):
        if any(part in skip for part in path.parts):
            continue
        index.setdefault(path.stem, []).append(path)
    return index


def resolves_link(source: Path, target: str, global_stems: dict[str, list[Path]]) -> bool:
    target = target.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    if not target or "{{" in target:
        return True
    candidate = Path(*target.split("/"))
    if candidate.suffix.lower() not in {".md", ".pdf", ".py", ".csv", ".json"}:
        candidate = candidate.with_suffix(".md")
    if (source.parent / candidate).exists() or (ROOT / candidate).exists() or (QUANT / candidate).exists():
        return True
    if "/" in target:
        return False
    return bool(global_stems.get(Path(target).name.removesuffix(".md")))


def rewrite_visible(
    text: str,
    source: Path,
    stems: dict[str, list[str]],
    global_stems: dict[str, list[Path]],
    changes: Counter[tuple[str, str]],
    unknown: Counter[str],
) -> str:
    def replace(match: re.Match[str]) -> str:
        embed, body = match.groups()
        target_and_heading, separator, display = body.partition("|")
        target, heading_mark, heading = target_and_heading.partition("#")
        target = target.strip().replace("\\", "/")
        if resolves_link(source, target, global_stems):
            return match.group(0)
        canonical = canonical_for(target, stems)
        if canonical is None:
            unknown[target] += 1
            return match.group(0)
        visible = display.strip() if separator else Path(target).name
        new_target = canonical + (f"#{heading}" if heading_mark else "")
        replacement = f"{embed}[[{new_target}|{visible}]]"
        changes[(target, canonical)] += 1
        return replacement

    return WIKILINK_RE.sub(replace, text)


def rewrite_document(
    text: str,
    source: Path,
    stems: dict[str, list[str]],
    global_stems: dict[str, list[Path]],
    changes: Counter[tuple[str, str]],
    unknown: Counter[str],
) -> str:
    parts: list[str] = []
    cursor = 0
    for block in CODE_BLOCK_RE.finditer(text):
        parts.append(rewrite_visible(text[cursor:block.start()], source, stems, global_stems, changes, unknown))
        parts.append(block.group(0))
        cursor = block.end()
    parts.append(rewrite_visible(text[cursor:], source, stems, global_stems, changes, unknown))
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write reviewed replacements")
    args = parser.parse_args()
    stems = stem_index()
    global_stems = global_stem_index()
    changes: Counter[tuple[str, str]] = Counter()
    unknown: Counter[str] = Counter()
    pending: dict[Path, str] = {}
    for path in QUANT.rglob("*.md"):
        original = path.read_text(encoding="utf-8-sig")
        rewritten = rewrite_document(original, path, stems, global_stems, changes, unknown)
        if rewritten != original:
            pending[path] = rewritten
    print(f"mapped occurrences: {sum(changes.values())}; files: {len(pending)}")
    for (source, target), count in changes.most_common():
        print(f"MAP {count:3d} {source} -> {target}")
    if unknown:
        print(f"unknown occurrences: {sum(unknown.values())}; unique: {len(unknown)}")
        for target, count in unknown.most_common():
            print(f"UNKNOWN {count:3d} {target}")
        return 1
    if args.apply:
        for path, rewritten in pending.items():
            path.write_text(rewritten, encoding="utf-8")
        print(f"applied to {len(pending)} file(s)")
    else:
        print("dry run only; use --apply after reviewing the map")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
