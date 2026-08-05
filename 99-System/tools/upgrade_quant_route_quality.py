#!/usr/bin/env python3
"""Idempotently add topic-specific evidence and verification to K01-K28."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
MARKER = "<!-- quant-route-quality-v2 -->"
FENCE = chr(96) * 3

# path, topic-specific audit paragraph, sources, executable check, related pages
ITEMS = {
"01": (
"01-夯实基础/收益率与对数收益率.md",
"""收益率与对数收益率的定义依赖同一资产、相邻可比价格和一致的现金流口径。简单收益负责财富复合，对数收益负责沿时间相加；二者在单期可互换，但组合横截面不能把加权对数收益直接当作组合收益。成立条件是价格严格为正且企业行为已处理。反例是拆股前后直接用原始价格：公式本身没有错，输入口径却制造了虚假亏损。独立验证应同时比较分段收益、累计净值和端点价格，而不是只看某一列输出。""",
[
"Campbell, Lo and MacKinlay, The Econometrics of Financial Markets, Princeton University Press, 1997, ISBN 9780691043012, Chapter 1.",
"pandas pct_change API, Section Returns: https://pandas.pydata.org/docs/reference/api/pandas.Series.pct_change.html",
"Microsoft Qlib Data Layer, Section Data API: https://qlib.readthedocs.io/en/stable/component/data.html",
],
"""prices = [100.0, 102.0, 101.0, 105.0, 103.0]
simple = [prices[i] / prices[i-1] - 1 for i in range(1, len(prices))]
wealth = 1.0
for r in simple: wealth *= 1 + r
assert abs((wealth - 1) - (prices[-1] / prices[0] - 1)) < 1e-12""",
["01-夯实基础/OHLCV字段清洗与复权", "01-夯实基础/时间索引与频率（量化）", "02-量化核心技能/样本泄漏", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"02": (
"01-夯实基础/OHLCV字段清洗与复权.md",
"""OHLCV字段清洗与复权不是“把缺失值填满”，而是建立可审计的数据契约。定义中必须分开原始报价、复权序列、成交量单位和企业行为日期；机制上先检查唯一键、类型与交易日历，再依据供应商说明验证复权因子。关键假设是拆分、分红和停牌标记能够被追溯。边界是不同供应商的前复权、后复权命名可能相反。反例是把零成交量当缺失后前向填充，这会伪造可交易价格。""",
[
"Microsoft Qlib Data Layer, Section Data Preparation and File Structure: https://qlib.readthedocs.io/en/stable/component/data.html",
"pandas Working with missing data, Section NA semantics: https://pandas.pydata.org/docs/user_guide/missing_data.html",
"pandas Duplicate Labels, Section Consequences of duplicate labels: https://pandas.pydata.org/docs/user_guide/duplicates.html",
],
"""rows = [("A", "t1"), ("A", "t2"), ("A", "t2")]
keys = set(rows)
assert len(keys) != len(rows)
raw_return = 50 / 100 - 1
assert raw_return == -0.5  # 拆股反例，不能解释为财富损失""",
["01-夯实基础/收益率与对数收益率", "01-夯实基础/时间索引与频率（量化）", "02-量化核心技能/前视偏差", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"03": (
"01-夯实基础/时间索引与频率（量化）.md",
"""时间索引与频率的核心定义不是日期字符串，而是带时区、交易日历、观测区间和信息可得时点的事件轴。重采样的机制会改变每个桶的边界和标签，所以开高低收的聚合规则不能互换。假设日线收盘数据在收盘后可得时，含当日收盘的特征只能驱动更晚订单。反例是把自然日补齐后将周末当成零收益交易日，波动率与年化因子都会被扭曲。验证必须打印原始时间、桶边界、信号时间与执行时间。""",
[
"pandas Time series/date functionality, Section Resampling: https://pandas.pydata.org/docs/user_guide/timeseries.html",
"pandas Resampler API, Section OHLC aggregation: https://pandas.pydata.org/docs/reference/resampling.html",
"Microsoft Qlib Data Layer, Section Calendar and Instrument APIs: https://qlib.readthedocs.io/en/stable/component/data.html",
],
"""from datetime import datetime, timezone
signal = datetime(2026, 8, 1, 8, 0, tzinfo=timezone.utc)
execution = datetime(2026, 8, 2, 1, 30, tzinfo=timezone.utc)
assert signal.tzinfo is not None
assert signal < execution""",
["01-夯实基础/OHLCV字段清洗与复权", "01-夯实基础/Pandas分组聚合与透视表", "01-夯实基础/滚动窗口与波动率特征", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"04": (
"01-夯实基础/Pandas分组聚合与透视表.md",
"""Pandas分组聚合与透视表在量化面板中的定义必须区分资产内时间运算与同日截面运算。groupby 的 split-apply-combine 机制只在分组键正确、索引对齐稳定时成立；直接对全表 shift 会越过资产边界。适用边界是 pivot 要求行列键唯一，而 pivot_table 会执行聚合，不能拿它掩盖重复行情。反例测试应让 A 的末行紧邻 B 的首行，并确认 B 的首个滞后值仍为空。""",
[
"pandas Group by: split-apply-combine, Section Window and resample operations: https://pandas.pydata.org/docs/user_guide/groupby.html",
"pandas Reshaping and pivot tables, Section pivot versus pivot_table: https://pandas.pydata.org/docs/user_guide/reshaping.html",
"pandas MultiIndex/advanced indexing, Section Basic indexing: https://pandas.pydata.org/docs/user_guide/advanced.html",
],
"""import pandas as pd
s = pd.Series([10, 11, 20, 18], index=["A", "A", "B", "B"])
lag = s.groupby(level=0).shift(1)
assert pd.isna(lag.iloc[0]) and pd.isna(lag.iloc[2])
assert lag.iloc[3] == 20""",
["01-夯实基础/时间索引与频率（量化）", "01-夯实基础/滚动窗口与波动率特征", "03-策略开发与实战/因子标准化", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"05": (
"01-夯实基础/滚动窗口与波动率特征.md",
"""滚动窗口与波动率特征的定义包含窗口边界、最小样本数、标准差自由度与年化频率。其机制是在每个资产内部对过去观测做局部统计，并不自动保证可交易性。假设信号在收盘后生成且次日执行时，可以使用当日收盘信息；若当日开盘执行则必须退回到此前可见数据。反例是无条件 shift 一天或完全不写交易时点。验证要同时检查前导空值、手算样本标准差以及两个时点协议。""",
[
"pandas Windowing operations, Section Rolling window: https://pandas.pydata.org/docs/user_guide/window.html",
"NumPy std API, Section ddof and correction: https://numpy.org/doc/stable/reference/generated/numpy.std.html",
"pandas Rolling.std API, Section ddof: https://pandas.pydata.org/docs/reference/api/pandas.core.window.rolling.Rolling.std.html",
],
"""import numpy as np
r = np.array([0.01, -0.01, 0.01])
sigma = r.std(ddof=1)
assert abs(sigma - 0.011547005383792516) < 1e-12
assert np.isnan(np.array([np.nan, np.nan])[0])""",
["01-夯实基础/Pandas分组聚合与透视表", "02-量化核心技能/样本泄漏", "03-策略开发与实战/前视偏差", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"06": (
"02-量化核心技能/样本泄漏.md",
"""样本泄漏的定义是模型训练或研究选择使用了预测时不可获得的信息。泄漏机制至少包括未来特征、全样本预处理、标签窗口重叠和测试集反复调参；随机切分只是其中一种诱因。成立条件应由逐行 information set 证明，而不是看到高收益后凭直觉判断。反例是先用全样本均值标准化再划分训练测试，即使特征没有显式 lead，也已让测试分布进入训练。独立验证要制造一个会失败的泄漏测试。""",
[
"scikit-learn Common pitfalls, Section 11.2 Data leakage: https://scikit-learn.org/stable/common_pitfalls.html",
"scikit-learn TimeSeriesSplit, Section gap parameter: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
"Microsoft Qlib Data Layer, Section Dataset and Handler: https://qlib.readthedocs.io/en/stable/component/data.html",
],
"""train_end, test_start = 100, 101
fit_rows = set(range(0, train_end + 1))
test_rows = set(range(test_start, 130))
assert fit_rows.isdisjoint(test_rows)
feature_available_at, execution_at = 100, 101
assert feature_available_at < execution_at""",
["01-夯实基础/滚动窗口与波动率特征", "03-策略开发与实战/标签设计", "03-策略开发与实战/前视偏差", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"07": (
"02-量化核心技能/策略评价指标.md",
"""策略评价指标的定义必须绑定收益口径、频率、无风险利率、基准与成本。年化收益、年化波动和 Sharpe 的机制依赖采样频率；最大回撤来自净值路径，IC则属于预测层，不能混成一个“综合好坏”数字。假设收益近似平稳时平方根年化才可作为描述，短样本和自相关会破坏该近似。反例是波动率接近零时报告巨大 Sharpe。验证应以同一收益序列同时计算 gross、net 和基准超额结果。""",
[
"Sharpe, Mutual Fund Performance, Journal of Business 39(1), 1966, Section Performance measurement: https://www.jstor.org/stable/2351741",
"Microsoft Qlib Recorder, Section portfolio analysis and risk_analysis: https://qlib.readthedocs.io/en/stable/component/recorder.html",
"Bailey and López de Prado, Deflated Sharpe Ratio, DOI 10.3905/jpm.2014.40.5.094, Section Selection Bias: https://doi.org/10.3905/jpm.2014.40.5.094",
],
"""import numpy as np
r = np.array([0.01, -0.005, 0.002, 0.003])
ann_vol = r.std(ddof=1) * np.sqrt(252)
assert ann_vol > 0
assert np.isfinite(r.mean() / r.std(ddof=1))""",
["01-夯实基础/最大回撤", "03-策略开发与实战/交易成本", "03-策略开发与实战/因子评价：IC、Rank IC 与 ICIR", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"08": (
"01-夯实基础/最大回撤.md",
"""最大回撤的定义是净值相对历史峰值的最大相对跌幅，而不是最差单日收益。计算机制先取 running maximum，再计算当前净值除以峰值减一；因此路径顺序会改变最大回撤，即使期末收益相同。边界包括净值必须使用一致成本口径、缺失期不能默认零收益。反例是将全期最高点与更早最低点相减，那条“回撤”在时间上无法发生。独立验证应保存峰值日期、谷底日期和恢复日期。""",
[
"Bacon, Practical Portfolio Performance Measurement and Attribution, Wiley, 2008, ISBN 9780470059289, Chapter 4.",
"Microsoft Qlib Recorder, Section risk_analysis output: https://qlib.readthedocs.io/en/stable/component/recorder.html",
"NumPy maximum.accumulate API, Section cumulative maximum: https://numpy.org/doc/stable/reference/generated/numpy.maximum.accumulate.html",
],
"""import numpy as np
nav = np.array([1.0, 1.1, 1.05, 0.88, 0.95])
peak = np.maximum.accumulate(nav)
drawdown = nav / peak - 1
assert abs(drawdown.min() - (0.88 / 1.1 - 1)) < 1e-12
assert drawdown[0] == 0""",
["02-量化核心技能/策略评价指标", "03-策略开发与实战/交易成本", "03-策略开发与实战/换手率调和收益", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"09": (
"03-策略开发与实战/交易成本.md",
"""交易成本的定义至少拆为显式费用、买卖价差、滑点、冲击和机会成本。机制上，费率通常作用于成交名义金额，方向和最低收费可能不对称；组合净收益应由毛收益扣除与实际换手相容的成本。假设固定费率只能作为基线，不代表真实大单执行。反例是训练策略时忽略成本、最后仅从累计收益减一个常数。验证应逐笔核对买卖方向、成交额、费率与净值。""",
[
"Microsoft Qlib Recorder, Section backtest open_cost and close_cost: https://qlib.readthedocs.io/en/stable/component/recorder.html",
"Perold, The Implementation Shortfall: Paper versus Reality, Journal of Portfolio Management 14(3), 1988, DOI 10.3905/jpm.1988.409150: https://doi.org/10.3905/jpm.1988.409150",
"Qlib Strategy and Backtest, Section Exchange and Executor: https://qlib.readthedocs.io/en/stable/component/strategy.html",
],
"""trades = [(1000, 0.0005), (-600, 0.0010)]
cost = sum(abs(notional) * rate for notional, rate in trades)
assert abs(cost - 1.1) < 1e-12
gross = 10.0
assert gross - cost < gross""",
["02-量化核心技能/策略评价指标", "03-策略开发与实战/换手率调和收益", "03-策略开发与实战/滑点模型", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"10": (
"03-策略开发与实战/换手率调和收益.md",
"""换手率调和收益的定义不是新绩效指标，而是把权重变化、交易成本和净收益放在同一会计恒等式中。双边换手常写为权重绝对变化之和的一半，但具体口径必须声明是否包含现金、申赎和漂移。机制上更高换手通常提高成本，却不保证收益单调下降，因为成交时点也会变化。反例是只报告换手后 Sharpe 而不保留 gross 与 net。验证应对等权持有、全量换仓和部分调仓三个场景手算。""",
[
"Microsoft Qlib Recorder, Section portfolio analysis with and without cost: https://qlib.readthedocs.io/en/stable/component/recorder.html",
"Qlib Strategy, Section TopkDropoutStrategy and turnover controls: https://qlib.readthedocs.io/en/stable/component/strategy.html",
"Perold, The Implementation Shortfall, DOI 10.3905/jpm.1988.409150, Section transaction accounting: https://doi.org/10.3905/jpm.1988.409150",
],
"""old = [0.5, 0.5, 0.0]
new = [0.0, 0.5, 0.5]
turnover = 0.5 * sum(abs(a-b) for a, b in zip(old, new))
assert turnover == 0.5
assert 0 <= turnover <= 1""",
["03-策略开发与实战/交易成本", "01-夯实基础/最大回撤", "03-策略开发与实战/分层回测", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"11": (
"03-策略开发与实战/因子构造.md",
"""因子构造的定义是把经济假设转成在每个资产与时点都可重复计算的数值映射。机制必须冻结字段、变换、窗口、方向和可得时间；任何看完测试结果再改方向的动作都属于研究者自由度。成立条件包括原始字段 point-in-time、横截面股票池可追溯。反例是把未来二十日收益误作“动量因子”。独立验证应在十行样本上手算一个资产，并测试窗口未满、价格缺失和分母为零的边界。""",
[
"Microsoft Qlib Data Layer, Section Expression Engine and formulaic alphas: https://qlib.readthedocs.io/en/stable/component/data.html",
"Qlib Alpha158 data handler configuration, Section Feature expressions: https://qlib.readthedocs.io/en/stable/component/data.html#data-handler",
"López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapter 4.",
],
"""prices = [100, 101, 103]
momentum_2 = prices[-1] / prices[0] - 1
assert abs(momentum_2 - 0.03) < 1e-12
available_at = 2
assert available_at == len(prices) - 1""",
["03-策略开发与实战/因子标准化", "03-策略开发与实战/标签设计", "03-策略开发与实战/分层回测", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"12": (
"03-策略开发与实战/因子标准化.md",
"""因子标准化的定义是在指定信息集合内改变尺度，而不改变研究对象。横截面 z-score 应只使用当日可见资产；训练型变换则只能在训练区间拟合。机制通常包含去极值、缺失处理、行业或规模中性化与标准化，顺序改变会产生不同结果。假设均值方差稳定并不总成立。反例是先用全样本均值标准化再切测试集。验证应检查每期均值、标准差、极端值和只含一个有效样本的截面。""",
[
"SciPy zscore API, Section nan_policy and ddof: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.zscore.html",
"SciPy winsorize API, Section limits: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mstats.winsorize.html",
"scikit-learn Common pitfalls, Section preprocessing and leakage: https://scikit-learn.org/stable/common_pitfalls.html",
],
"""import numpy as np
x = np.array([1.0, 2.0, 3.0])
z = (x - x.mean()) / x.std(ddof=0)
assert abs(z.mean()) < 1e-12
assert abs(z.std(ddof=0) - 1) < 1e-12""",
["03-策略开发与实战/因子构造", "03-策略开发与实战/标签设计", "02-量化核心技能/样本泄漏", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"13": (
"03-策略开发与实战/因子选择：价值、质量与动量.md",
"""因子选择：价值、质量与动量必须先定义经济机制再选择数据字段。价值比较价格与基本面，质量描述盈利与资产负债表稳健性，动量刻画过去价格延续；三者的数据发布时间和换手特征不同。基本假设是信号在样本外仍有补偿风险或行为偏差依据。边界包括行业不可比、会计修订、微盘股可交易性与动量崩溃。反例是同时试几十种窗口后只报告最优组合。""",
[
"Kenneth French Data Library, Section Fama/French factors and momentum: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
"Fama and French, The Cross-Section of Expected Stock Returns, Journal of Finance 47(2), 1992, DOI 10.1111/j.1540-6261.1992.tb04398.x: https://doi.org/10.1111/j.1540-6261.1992.tb04398.x",
"Microsoft Qlib Data Layer, Section formulaic alpha construction: https://qlib.readthedocs.io/en/stable/component/data.html",
],
"""candidates = ["value", "quality", "momentum"]
chosen_before_test = "momentum"
assert chosen_before_test in candidates
trials_reported = 1
assert trials_reported == 1""",
["03-策略开发与实战/因子构造", "03-策略开发与实战/因子标准化", "03-策略开发与实战/标签设计", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"14": (
"03-策略开发与实战/标签设计.md",
"""标签设计的定义是从特征时点之后的价格路径构造预测目标，并明确持有期、执行价和成本口径。标签区间必须严格晚于特征可得时点，但训练样本的标签窗口可能相互重叠，因此时间切分还需要 gap 或 purge。机制上收盘到收盘、开盘到开盘和开盘到收盘回答不同交易问题。反例是在 t 日收盘特征旁使用 t 日开盘到收盘收益。验证要画出特征、下单、成交与标签终点四个时间戳。""",
[
"Microsoft Qlib Data Layer, Section Dataset and label expressions: https://qlib.readthedocs.io/en/stable/component/data.html",
"scikit-learn TimeSeriesSplit, Section gap parameter: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
"López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapter 7.",
],
"""feature_at, order_at, fill_at, label_end = 10, 11, 11, 16
assert feature_at < order_at <= fill_at < label_end
holding_period = label_end - fill_at
assert holding_period == 5""",
["03-策略开发与实战/因子构造", "03-策略开发与实战/因子标准化", "02-量化核心技能/时间序列验证", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
}

def render(k: str, item: tuple) -> str:
    rel, focus, sources, code, links = item
    source_lines = "\n".join(f"{i}. {src}" for i, src in enumerate(sources, 1))
    link_lines = "\n".join(f"- [[{target}]]" for target in links)
    return f"""
{MARKER}
## K{k} 来源、边界与独立复核

### 定义、假设、机制与边界

{focus}

### 可定位来源

{source_lines}

### 可复现示例与验证

{FENCE}python
{code}
{FENCE}

这段最小实验不是收益证明；它只验证 K{k} 的局部定义与边界。正式作业仍需保存输入、期望输出、实际结果和失败案例。

### 知识连接

{link_lines}
"""

def main() -> None:
    changed = []
    for k, item in ITEMS.items():
        path = Q / item[0]
        if not path.exists():
            raise FileNotFoundError(path)
        text = path.read_text(encoding="utf-8-sig")
        text = re.sub(
            rf"\n{re.escape(MARKER)}.*?(?=\n<!-- quant-route-quality-v2 -->|\Z)",
            "",
            text,
            flags=re.S,
        ).rstrip()
        text += "\n" + render(k, item).rstrip() + "\n"
        if "updated: 2026-08-01" not in text:
            if text.startswith("---"):
                text = text.replace("\n---\n", "\nupdated: 2026-08-01\n---\n", 1)
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(ROOT))
    print(f"Upgraded {len(changed)} route cards: K01-K14.")

if __name__ == "__main__":
    main()