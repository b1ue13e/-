#!/usr/bin/env python3
"""Idempotently add topic-specific evidence and verification to K15-K28."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "03-量化金融"
MARKER = "<!-- quant-route-quality-v2 -->"
FENCE = chr(96) * 3

ITEMS = {
"15": (
"03-策略开发与实战/分层回测.md",
"""分层回测的定义是在每个截面按预先冻结的因子排序，把资产分入若干组合并追踪后续收益。机制要固定股票池、分位数边界、权重、调仓和成本，才能把 Top-Bottom 差异解释为排序证据。假设每层有足够资产且可交易；重复值、缺失和小截面会使 qcut 失效。反例是看完结果后改成最有利的分组数。验证应同时报告各层样本数、单调性、换手和净收益。""",
[
"pandas qcut API, Section quantile-based discretization: https://pandas.pydata.org/docs/reference/api/pandas.qcut.html",
"Microsoft Qlib Recorder, Section SignalAnalysisRecord and PortAnaRecord: https://qlib.readthedocs.io/en/stable/component/recorder.html",
"SciPy spearmanr API, Section rank correlation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html",
],
"""scores = [1, 2, 3, 4, 5]
future = [-0.02, -0.01, 0.00, 0.01, 0.03]
assert len(scores) == len(future)
top_bottom = future[-1] - future[0]
assert abs(top_bottom - 0.05) < 1e-12""",
["03-策略开发与实战/因子标准化", "03-策略开发与实战/标签设计", "03-策略开发与实战/因子评价：IC、Rank IC 与 ICIR", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"16": (
"03-策略开发与实战/因子评价：IC、Rank IC 与 ICIR.md",
"""因子评价：IC、Rank IC 与 ICIR的定义单位是“日期内横截面相关，再沿时间汇总”。Pearson IC度量线性相关，Rank IC度量秩单调关系；ICIR是IC均值与其波动的比值，不等于组合信息比率。假设截面样本足够且缺失成对删除。边界包括横截面过小、并列秩过多、IC自相关与结构突变。反例是把所有日期资产堆在一起算一个相关系数。验证应手算一次并与 SciPy 两种相关实现核对。""",
[
"SciPy pearsonr API, Section statistic and p-value: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html",
"SciPy spearmanr API, Section rank correlation and nan_policy: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html",
"Microsoft Qlib Recorder, Section SignalAnalysisRecord IC metrics: https://qlib.readthedocs.io/en/stable/component/recorder.html",
],
"""from scipy.stats import pearsonr, spearmanr
factor = [1, 2, 3, 4]
label = [0.0, 0.2, 0.1, 0.4]
p = pearsonr(factor, label).statistic
s = spearmanr(factor, label).statistic
assert -1 <= p <= 1 and -1 <= s <= 1""",
["03-策略开发与实战/标签设计", "03-策略开发与实战/分层回测", "02-量化核心技能/策略评价指标", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"17": (
"03-策略开发与实战/前视偏差.md",
"""前视偏差的定义是在决策时使用未来才知道的数据或后来修订的历史。机制可能来自负 shift、财报回填、幸存股票池、全样本标准化或不可能的成交价。它与普通过拟合不同：前视偏差违反信息可得性，过拟合是在合法信息内过度选择。成立条件必须用 point-in-time 时间表逐项证明。反例是用 t 日收盘信号按同一收盘价无摩擦成交。验证要保留一个故意泄漏版本作为失败测试。""",
[
"scikit-learn Common pitfalls, Section 11.2 Data leakage: https://scikit-learn.org/stable/common_pitfalls.html",
"Microsoft Qlib Data Layer, Section Dataset time slicing: https://qlib.readthedocs.io/en/stable/component/data.html",
"López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapter 7.",
],
"""feature_known = {"close_t": 16_00, "report_t": 18_30}
decision_time = 16_05
assert feature_known["close_t"] <= decision_time
assert feature_known["report_t"] > decision_time
allowed = [k for k, v in feature_known.items() if v <= decision_time]
assert allowed == ["close_t"]""",
["02-量化核心技能/样本泄漏", "03-策略开发与实战/标签设计", "03-策略开发与实战/生存者偏差", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"18": (
"03-策略开发与实战/特征工程-量化应用.md",
"""特征工程-量化应用的定义是把历史可见原始字段转成稳定、可审计的模型输入。窗口收益、波动、量价关系和横截面排名都必须记录字段、运算符、窗口和最早可得时间。机制上同一表达式在 Qlib DataHandler 中还会经过处理器与数据切片。假设表达式只引用过去并不足够，全样本拟合的处理器仍可泄漏。反例是背诵 Alpha158 名称却说不清其中任意五个特征。验证应抽样追踪表达式到原始行。""",
[
"Microsoft Qlib Data Layer, Section Expression Engine: https://qlib.readthedocs.io/en/stable/component/data.html",
"Qlib official repository, Alpha158 handler configuration: https://github.com/microsoft/qlib/tree/main/qlib/contrib/data",
"scikit-learn Common pitfalls, Section preprocessing leakage: https://scikit-learn.org/stable/common_pitfalls.html",
],
"""close = [10.0, 10.5, 10.2]
ret_1 = [None] + [close[i] / close[i-1] - 1 for i in range(1, len(close))]
assert ret_1[0] is None
assert abs(ret_1[-1] - (10.2 / 10.5 - 1)) < 1e-12""",
["03-策略开发与实战/因子构造", "01-夯实基础/滚动窗口与波动率特征", "02-量化核心技能/树模型基线", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"19": (
"02-量化核心技能/树模型基线.md",
"""树模型基线的定义是在冻结数据、标签和切分后，用有限超参数建立可复现的非线性参照。LightGBM逐步加入树来降低训练目标，但早停只能查看验证集，测试集不能选择迭代轮数。适用假设是表格特征和样本量足以支持树分裂；高维噪声与时间漂移会放大过拟合。反例是在测试期多次调 depth 后仍称其为样本外。验证要记录种子、特征清单、最佳轮数和各时间段指标。""",
[
"LightGBM Parameters, Section Learning Control Parameters: https://lightgbm.readthedocs.io/en/stable/Parameters.html",
"LightGBM early_stopping callback, Section API: https://lightgbm.readthedocs.io/en/stable/pythonapi/lightgbm.early_stopping.html",
"Microsoft Qlib Quick Start, Section LightGBM workflow: https://qlib.readthedocs.io/en/stable/introduction/quick.html",
],
"""train_dates = set(range(1, 101))
valid_dates = set(range(101, 121))
test_dates = set(range(121, 141))
assert train_dates.isdisjoint(valid_dates | test_dates)
best_iteration_selected_on = "validation"
assert best_iteration_selected_on != "test""",
["02-量化核心技能/时间序列验证", "03-策略开发与实战/特征重要性", "03-策略开发与实战/量化预测", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"20": (
"02-量化核心技能/时间序列验证.md",
"""时间序列验证的定义是保持因果顺序的训练、验证和测试协议，而不是随机交叉验证换一个名字。扩展窗、滚动窗、gap、purge 和 embargo 解决的重叠问题不同。假设样本等间隔时 TimeSeriesSplit 的各折指标更可比；标签跨期时仅保留顺序仍可能泄漏。反例是打乱日期后做 KFold。验证必须逐折断言 max(train_time) 小于 min(test_time)，并检查标签区间不跨边界。""",
[
"scikit-learn TimeSeriesSplit, Section ordered folds and gap: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
"scikit-learn Cross-validation guide, Section time series data: https://scikit-learn.org/stable/modules/cross_validation.html#time-series-split",
"López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapter 7.",
],
"""folds = [([1,2,3], [5,6]), ([1,2,3,4,5], [7,8])]
for train, test in folds:
    assert max(train) < min(test)
    assert set(train).isdisjoint(test)
    gap = min(test) - max(train) - 1
    assert gap >= 1""",
["02-量化核心技能/样本泄漏", "03-策略开发与实战/标签设计", "03-策略开发与实战/Purged CV", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"21": (
"03-策略开发与实战/量化预测.md",
"""量化预测的定义是为每个资产—时点生成可保存的分数、概率或条件收益估计。预测层、组合层和执行层必须解耦，因为相同分数可对应完全不同的权重与成本。假设预测分数排序稳定不等于可盈利，容量、换手和基准会改变结果。反例是把模型输出的 score 直接称为收益率。验证要检查 MultiIndex 唯一、缺失比例、每日期排序，并让 E1/E2 共用同一组合规则。""",
[
"Microsoft Qlib Introduction, Section Forecast Model and Decision Generator: https://qlib.readthedocs.io/en/stable/introduction/introduction.html",
"Microsoft Qlib Recorder, Section SignalRecord and portfolio records: https://qlib.readthedocs.io/en/stable/component/recorder.html",
"Qlib Quick Start, Section Auto Quant Research Workflow: https://qlib.readthedocs.io/en/stable/introduction/quick.html",
],
"""pred = {("A", 1): 0.3, ("B", 1): -0.1, ("A", 2): 0.2}
assert len(pred) == len(set(pred))
day1 = {k:v for k,v in pred.items() if k[1] == 1}
ranking = sorted(day1, key=day1.get, reverse=True)
assert ranking[0][0] == "A" """,
["02-量化核心技能/树模型基线", "02-量化核心技能/时间序列验证", "03-策略开发与实战/交易成本", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"22": (
"03-策略开发与实战/特征重要性.md",
"""特征重要性的定义依赖模型、数据集和评分函数，不是特征的永久属性。树分裂重要性可能偏爱高基数变量；置换重要性测量打乱某列后验证性能的下降，但相关特征会互相替代。成立条件是模型本身具有样本外预测力。反例是在训练集上解释过拟合模型并宣布因果关系。验证应在冻结验证集重复置换，报告均值和方差，并做单变量消融确认方向。""",
[
"scikit-learn Permutation feature importance, Section algorithm and caveats: https://scikit-learn.org/stable/modules/permutation_importance.html",
"scikit-learn permutation_importance API, Section scoring and repeats: https://scikit-learn.org/stable/modules/generated/sklearn.inspection.permutation_importance.html",
"Breiman, Random Forests, Machine Learning 45, 2001, DOI 10.1023/A:1010933404324: https://doi.org/10.1023/A:1010933404324",
],
"""baseline_scores = [0.10, 0.11, 0.09]
permuted_scores = [0.06, 0.08, 0.07]
importance = sum(baseline_scores)/3 - sum(permuted_scores)/3
assert importance > 0
assert len(baseline_scores) == len(permuted_scores)""",
["02-量化核心技能/树模型基线", "03-策略开发与实战/量化预测", "03-策略开发与实战/因子评价：IC、Rank IC 与 ICIR", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"23": (
"🚀 Qlib项目执行入口.md",
"""Qlib项目执行入口对应的核心机制是 provider 到 dataset、model、recorder、strategy、executor 与 backtest 的证据链。每一层都应保存配置和产物，避免“qrun 成功”被误当成研究结论。假设官方示例能运行只证明环境与接口基本可用；数据许可、复权、交易日历和样本外设计仍需独立审计。反例是只保存最终图表而丢失预测分数和配置哈希。验证要从回测结果反向定位模型与数据版本。""",
[
"Microsoft Qlib Introduction, Section Framework layers: https://qlib.readthedocs.io/en/stable/introduction/introduction.html",
"Microsoft Qlib Quick Start, Section qrun workflow: https://qlib.readthedocs.io/en/stable/introduction/quick.html",
"Microsoft Qlib Recorder, Section experiment management: https://qlib.readthedocs.io/en/stable/component/recorder.html",
],
"""artifacts = {"config": True, "prediction": True, "metrics": True, "portfolio": True}
assert all(artifacts.values())
pipeline = ["provider", "dataset", "model", "record", "strategy", "backtest"]
assert pipeline.index("dataset") < pipeline.index("model") < pipeline.index("backtest")""",
["03-策略开发与实战/量化预测", "03-策略开发与实战/回测偏差五层审计", "🧩 Qlib 项目知识点—作业—验收路线图", "🚀 Qlib项目执行入口"],
),
"24": (
"03-策略开发与实战/回测偏差五层审计.md",
"""回测偏差五层审计把风险分为数据、股票池、特征、标签和执行。机制是对每层列出可见时间、选择规则、失败测试与证据位置；任何 unknown 都不能自动转为 pass。假设某层无泄漏并不能推出其他层安全。反例是特征完全滞后，却使用今天仍存续的股票重建十年前股票池。验证应故意破坏一层并确认审计测试失败，同时保留失败日志。""",
[
"scikit-learn Common pitfalls, Section Data leakage: https://scikit-learn.org/stable/common_pitfalls.html",
"Microsoft Qlib Recorder, Section experiment artifacts and portfolio analysis: https://qlib.readthedocs.io/en/stable/component/recorder.html",
"López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapters 7 and 11.",
],
"""layers = {"data":"pass", "universe":"unknown", "feature":"pass", "label":"pass", "execution":"fail"}
assert set(layers) == {"data","universe","feature","label","execution"}
formal_pass = all(v == "pass" for v in layers.values())
assert not formal_pass""",
["02-量化核心技能/样本泄漏", "03-策略开发与实战/前视偏差", "03-策略开发与实战/生存者偏差", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"25": (
"03-策略开发与实战/生存者偏差.md",
"""生存者偏差的定义是历史样本只保留后来仍存在或仍被数据库覆盖的资产。机制上，退市、合并和指数成分更替被删除后，历史收益与可交易性会系统性变好。point-in-time 股票池是成立条件；仅有当前代码列表不够。反例是用今天的沪深300成分回测十年前策略。验证应抽查至少三个历史日期的成员、上市日、退市日，并比较动态股票池与当前幸存池。""",
[
"Kenneth French Data Library, Section historical research portfolios: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
"Microsoft Qlib Data Layer, Section Instruments and time-dependent universe: https://qlib.readthedocs.io/en/stable/component/data.html",
"López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapter 11.",
],
"""history = {2019: {"A","B","C"}, 2026: {"A","C","D"}}
current_only = history[2026]
assert "B" in history[2019] and "B" not in current_only
assert history[2019] != current_only""",
["03-策略开发与实战/前视偏差", "03-策略开发与实战/回测偏差五层审计", "01-夯实基础/OHLCV字段清洗与复权", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"26": (
"03-策略开发与实战/Purged CV.md",
"""Purged CV 的定义是在标签跨越多个时点时，从训练折删除与测试标签区间重叠的样本；embargo 则在边界后追加缓冲。两者机制基于标签区间，而不是随意删几天。假设仅使用 TimeSeriesSplit gap 并不总等价于 purge，因为每个样本的标签终点可能不同。反例是标签持有十天却只隔一天。验证应构造明确区间并断言训练标签与测试区间无交集。""",
[
"scikit-learn TimeSeriesSplit, Section gap parameter: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
"López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapter 7.",
"Bailey et al., The Probability of Backtest Overfitting, Journal of Computational Finance 20(4), Section combinatorial validation: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253",
],
"""train_intervals = [(1,3), (4,6)]
test_interval = (7,10)
overlap = lambda a,b: max(a[0],b[0]) <= min(a[1],b[1])
assert not any(overlap(x, test_interval) for x in train_intervals)
embargo_end = test_interval[1] + 2
assert embargo_end == 12""",
["02-量化核心技能/时间序列验证", "03-策略开发与实战/标签设计", "03-策略开发与实战/组合过拟合概率PBO", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"27": (
"03-策略开发与实战/滑点模型.md",
"""滑点模型的定义是订单决策价与实际可成交价之间的差异模型，应与方向、规模、流动性和延迟关联。固定基点、半价差和冲击函数是不同复杂度的假设，不可混称真实成交。机制上买单通常抬高成交价、卖单压低成交价，因此符号测试很重要。反例是成本上升后净收益反而系统性提高且没有再平衡解释。验证要做低中高三档压力表并保持其他配置不变。""",
[
"Microsoft Qlib Recorder, Section backtest deal_price and cost configuration: https://qlib.readthedocs.io/en/stable/component/recorder.html",
"Qlib Strategy and Executor, Section order execution: https://qlib.readthedocs.io/en/stable/component/strategy.html",
"Perold, The Implementation Shortfall, DOI 10.3905/jpm.1988.409150, Section execution shortfall: https://doi.org/10.3905/jpm.1988.409150",
],
"""mid, bps = 100.0, 10
buy_fill = mid * (1 + bps / 10000)
sell_fill = mid * (1 - bps / 10000)
assert buy_fill > mid > sell_fill
assert abs(buy_fill - 100.1) < 1e-12""",
["03-策略开发与实战/交易成本", "03-策略开发与实战/换手率调和收益", "03-策略开发与实战/回测偏差五层审计", "🧩 Qlib 项目知识点—作业—验收路线图"],
),
"28": (
"03-策略开发与实战/组合过拟合概率PBO.md",
"""组合过拟合概率PBO用于估计从多个候选策略中选出的样本内赢家在样本外退化的风险。机制需要足够多候选配置和可交换的时间分块，通过组合对称交叉验证比较样本内、外排名。它不是对少量手工实验随便输出的百分比。假设试验台账完整，否则选择偏差无法计入。反例是只保存最佳结果后声称 PBO 很低。验证应保存所有候选、失败配置、分块和排名映射。""",
[
"Bailey et al., The Probability of Backtest Overfitting, Journal of Computational Finance 20(4), Section PBO: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253",
"Bailey and López de Prado, Deflated Sharpe Ratio, DOI 10.3905/jpm.2014.40.5.094, Section multiple testing: https://doi.org/10.3905/jpm.2014.40.5.094",
"López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapter 11.",
],
"""trial_scores = {"cfg_a":0.2, "cfg_b":0.1, "cfg_c":-0.1, "cfg_d":0.05}
assert len(trial_scores) >= 4
winner = max(trial_scores, key=trial_scores.get)
assert winner == "cfg_a"
assert set(trial_scores) == {"cfg_a","cfg_b","cfg_c","cfg_d"}""",
["03-策略开发与实战/Purged CV", "03-策略开发与实战/回测偏差五层审计", "02-量化核心技能/策略评价指标", "🧩 Qlib 项目知识点—作业—验收路线图"],
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

该最小实验只验证 K{k} 的定义、符号或时间边界，不等价于策略有效。正式结论还必须保存输入版本、期望输出、实际结果和失败案例。

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
        if "updated: 2026-08-01" not in text and text.startswith("---"):
            text = text.replace("\n---\n", "\nupdated: 2026-08-01\n---\n", 1)
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(ROOT))
    print(f"Upgraded {len(changed)} route cards: K15-K28.")

if __name__ == "__main__":
    main()