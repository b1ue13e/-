---
type: study
topic: "单位根检验：ADF 与 KPSS"
course: "时间序列分析"
created: 2026-08-03
updated: 2026-08-07
status: ongoing
difficulty: intermediate
flow: knowledge
kind: concept
aliases: [单位根检验, ADF-KPSS]
concept: [单位根, 平稳性检验, 差分]
prerequisites: [弱平稳, 随机游走, 假设检验]
related: [差分, ARIMA, 协整, 结构突变]
stage_moc: "[[🧭 阶段2-平稳性与相关结构]]"
upstream: ["[[平稳性]]", "[[随机游走（深挖笔记）]]"]
sources:
  - title: "Forecasting: Principles and Practice (3e)"
    url: "https://otexts.com/fpp3/stationarity.html"
    locator: "Section 9.1: Stationarity and differencing"
    source_type: open-textbook
    license: "截至 2026-08-07 未发现适用于教材正文/题目的开放再分发许可；link-only，仅保留原创释义与章节定位。"
    verified_at: 2026-08-07
  - title: "statsmodels: adfuller and kpss"
    url: "https://www.statsmodels.org/stable/tsa.html#stationarity-and-detrending-adf-kpss"
    locator: "Stationarity and detrending"
    source_type: official-documentation
    license: "link-only"
    verified_at: 2026-08-07
anki_deck: "时间序列分析::单位根检验"
anki_tags: [时间序列分析, 单位根, ADF, KPSS]
tags: [学习, 时间序列分析, 单位根]
---

# 单位根检验：ADF 与 KPSS

## 1. 这张卡解决什么问题

图形、ACF 和滚动统计量可以提示非平稳，却不能单独区分确定性趋势、随机趋势、结构突变与短样本波动。单位根检验把其中一个问题形式化：**历史冲击是否像随机游走那样永久累积**。

它不是“自动决定差分阶数”的按钮。课程中的决策链是：数据生成机制与图形证据 → 确定性项和检验规格 → ADF/KPSS → 最少差分 → 差分后诊断 → 滚动样本外比较。

## 2. 从 AR(1) 到单位根

以 AR(1) 为入口：

$$
y_t=c+\phi y_{t-1}+\varepsilon_t.
$$

当 $\lvert\phi\rvert<1$ 时，冲击按几何速度衰减；当 $\phi=1$ 时，

$$
y_t=y_{t-1}+\varepsilon_t,
$$

序列成为随机游走。若 $y_0=0$ 且 $\varepsilon_t\sim WN(0,\sigma^2)$，则

$$
y_t=\sum_{i=1}^{t}\varepsilon_i,
\qquad
\operatorname{Var}(y_t)=t\sigma^2.
$$

方差依赖 $t$，所以不满足弱平稳。对随机游走做一阶差分得到 $\Delta y_t=\varepsilon_t$，但这不意味着任何 ADF 未拒绝结果都应立刻差分。

## 3. ADF 检验

把 AR(1) 两边减去 $y_{t-1}$：

$$
\Delta y_t=(\phi-1)y_{t-1}+\varepsilon_t
=\gamma y_{t-1}+\varepsilon_t.
$$

ADF 在此基础上加入确定性项和滞后差分：

$$
\Delta y_t
=\alpha+\beta t+\gamma y_{t-1}
+\sum_{i=1}^{p}\delta_i\Delta y_{t-i}+u_t.
$$

- $H_0:\gamma=0$：存在单位根。
- $H_1:\gamma<0$：在所选确定性项下平稳。
- $p$ 用于吸收残差自相关；过小会破坏检验尺度，过大则降低功效。
- 单位根边界下统计量不服从普通 t 分布，必须使用 Dickey–Fuller 临界值。

**拒绝 $H_0$** 是反对单位根的证据；**未拒绝 $H_0$** 只表示证据不足，不能写成“已经证明存在单位根”。

## 4. KPSS 检验

KPSS 反过来把水平平稳或趋势平稳作为原假设。可将序列写成确定性部分、随机游走部分和短期误差之和：

$$
y_t=d_t+r_t+\varepsilon_t,
\qquad
r_t=r_{t-1}+u_t.
$$

KPSS 的原假设相当于随机游走创新方差为零；小 p 值表示反对所选的平稳性口径。`regression="c"` 检查水平平稳，`regression="ct"` 检查趋势平稳。确定性项必须根据机制和图形在看结果前冻结，不能为了得到期望结论来回切换。

## 5. 联合解释矩阵

| ADF | KPSS | 可接受的解释 | 下一步 |
| :--- | :--- | :--- | :--- |
| 拒绝单位根 | 不拒绝平稳 | 两类证据与所选平稳口径一致 | 检查结构稳定性与样本外预测 |
| 不拒绝单位根 | 拒绝平稳 | 随机趋势或其他非平稳证据较强 | 比较去趋势、普通/季节差分等候选 |
| 两者都拒绝 | 证据冲突 | 可能有结构突变、非线性、异方差或规格错误 | 检查断点、确定性项和样本区间 |
| 两者都不拒绝 | 证据不足 | 短样本、低功效或接近单位根 | 报告不确定性，不强行定性 |

这张表不是新的自动决策器。显著性水平、样本区间、频率、确定性项、ADF 滞后和 KPSS 带宽都必须随结果一起记录。

## 6. 可运行最小例子

```python
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss

rng = np.random.default_rng(61)
noise = rng.normal(size=400)

stationary = np.empty(400)
stationary[0] = noise[0]
for t in range(1, len(stationary)):
    stationary[t] = 0.65 * stationary[t - 1] + noise[t]

random_walk = np.cumsum(noise)

def diagnose(values):
    adf_p = adfuller(values, regression="c", autolag="AIC")[1]
    kpss_p = kpss(values, regression="c", nlags="auto")[1]
    return {"adf_p": adf_p, "kpss_p": kpss_p}

print("stationary", diagnose(stationary))
print("random_walk", diagnose(random_walk))
```

本例应呈现方向性差异：平稳 AR(1) 通常拒绝 ADF 的单位根原假设且不拒绝 KPSS 的水平平稳原假设；随机游走通常相反。具体 p 值依赖样本，不应抄成固定答案。

## 7. 建模协议

1. 只在训练窗口上画原序列、季节图、滚动统计和 ACF；记录异常值、缺期与结构事件。
2. 在看 p 值前选择无常数、常数或常数加趋势的规格，并说明选择理由。
3. 冻结 ADF 滞后规则、KPSS 带宽、显著性水平和季节处理顺序。
4. 联合解释 ADF、KPSS、图形和机制，不把“未拒绝”写成“接受并证明”。
5. 只尝试最少必要的去趋势或差分；每次变换后重查 ACF、方差和可解释性。
6. 在[[ARIMA模型]]或其他候选中，用相同滚动原点比较样本外误差；最终测试段不参与差分阶数调参。

## 8. 失效边界与常见错误

- **结构突变**：一次均值或趋势断裂可能让 ADF 功效显著下降；先查事件和断点，不要机械差分。
- **季节单位根**：普通 ADF/KPSS 不能替代季节结构诊断；结合季节图、季节差分和专门检验。
- **接近单位根与短样本**：$\phi$ 接近 1 时，两种检验都可能证据不足。
- **长记忆、异方差和非线性**：经典检验的尺寸与功效可能失真，应报告边界并使用更匹配的方法。
- **p 值追逐**：反复修改趋势项、样本起点或滞后直到显著，会制造选择偏差。
- **过度差分**：可能制造强负 lag-1 自相关、放大噪声并恶化区间；差分不是免费操作。
- **错误结论**：价格水平存在单位根不等于市场有效，也不等于差分后具有可预测性。

## 9. 检索练习与通过标准

闭卷完成以下任务：

1. 从 AR(1) 推到 DF 形式，并说明为何不能使用普通 t 临界值。
2. 写出 ADF 与 KPSS 的原假设，解释同一个“小 p 值”为何方向相反。
3. 对联合解释矩阵的四种组合各给一个谨慎结论，不使用“证明”“一定差分”。
4. 给定一个有明显断点的短序列，写出检验前必须冻结的规格和补充证据。
5. 解释为什么最终仍需用滚动样本外预测比较差分方案。

**通过标准**：公式、原假设方向和确定性项无误；能够区分“拒绝”“未拒绝”和“接受”；至少指出结构突变、低功效、季节单位根和过度差分中的两个边界；代码只访问预测原点之前的数据。

## 🃏 Anki 卡片

- ADF 的原假设是什么？::$H_0$ 为存在单位根；拒绝它提供反对单位根的证据，未拒绝不等于证明单位根存在。
- KPSS 与 ADF 为什么互补？::KPSS 以水平/趋势平稳为原假设，ADF 以单位根为原假设；相反方向有助于暴露冲突和低功效。
- ADF 中确定性项与滞后阶为什么必须预先冻结？::结果对截距、趋势和滞后敏感；看结果后反复换规格会产生选择偏差。
- 为什么单位根检验不能单独决定差分阶数？::检验可能受断点、短样本、季节性等影响；还需机制、图形、差分后诊断和滚动样本外比较。

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §9.1 Stationarity and differencing](https://otexts.com/fpp3/stationarity.html)。
- statsmodels, [Stationarity and detrending: ADF and KPSS](https://www.statsmodels.org/stable/tsa.html#stationarity-and-detrending-adf-kpss)。

## 学完后可以完成

完成本卡后，使用下面的派生视图定位下游知识和可执行验收入口；作业关系只维护在作业的 `requires` 字段。

### 派生视图

### 下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

### 可完成作业

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
