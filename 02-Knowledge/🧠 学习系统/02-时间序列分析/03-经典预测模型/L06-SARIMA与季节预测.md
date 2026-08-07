---
type: study
course: "时间序列分析"
lesson: 6
topic: "SARIMA与季节预测"
created: 2026-08-02
updated: 2026-08-05
status: planned
mastery: 0
difficulty: advanced
flow: knowledge
kind: concept
concept: ["SARIMA", "季节差分", "季节基线"]
prerequisites: ["ARMA与ARIMA建模闭环", "差分运算", "季节性"]
related: ["L05-ARMA与ARIMA建模闭环", "L07-模型识别与参数估计", "季节性与STL分解"]
anki_deck: "时间序列分析::主线课程"
anki_tags: ["时间序列分析", "L06", "SARIMA", "季节差分"]
tags: [学习, 时间序列, 教师式课程, SARIMA, 季节预测]
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/seasonal-arima.html"
    locator: "Section 9.9: Seasonal ARIMA models"
    source_type: "open-textbook"
    license: "截至 2026-08-07 未发现适用于教材正文/题目的开放再分发许可；link-only，仅保留原创释义与章节定位。"
    verified_at: 2026-08-02
stage_moc: "[[🧭 阶段3-经典预测模型]]"
upstream: ["[[ARIMA建模流程-识别-估计-诊断]]"]
---
# L06｜SARIMA 与季节预测

> **预计用时**：90 分钟　**当前掌握**：0 / 1 / 2 / 3

## 0. 这节课解决什么问题

月度销量、季度用电量和每周客流常出现“与上一个季节同位置相似”的规律。普通 ARIMA 主要描述相邻期动态；SARIMA 再加入相隔一个季节周期的关系。

本课不是教你背七个阶数，而是回答三个问题：

1. 季节周期 $m$ 从哪里来？
2. 普通差分和季节差分分别消除什么？
3. 复杂 SARIMA 是否真的优于 seasonal naïve？

## 1. 学习目标

学完后，不看笔记能够：

- 从采样频率与业务机制确定 $m$，而不是只凭图形猜；
- 手算季节差分，并区分 $d$ 与 $D$；
- 解释 $(p,d,q)$ 与 $(P,D,Q)_m$ 各自负责什么；
- 展开一个乘法季节模型并指出交叉滞后；
- 用完整季节测试窗和 seasonal naïve 验收模型。

## 2. 课前诊断

> [!question] 先判断
> 月度数据的季节周期一定是 12；只要设置 `m=12`，模型就能学到季节性。对吗？

> [!answer]- 诊断答案
> 不对。月度采样让 12 成为一个候选周期，但真实机制可能没有年度季节性，也可能受半年、节假日或结构变化影响。周期应由业务机制、时间图和相关结构共同支持；设置 `m=12` 不会自动创造稳定规律。

## 3. 从一组季度数据理解季节差分

假设两年的季度销量为：

| 季度 | Y1-Q1 | Y1-Q2 | Y1-Q3 | Y1-Q4 | Y2-Q1 | Y2-Q2 | Y2-Q3 | Y2-Q4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 销量 | 10 | 14 | 18 | 22 | 12 | 16 | 21 | 25 |

季度周期 $m=4$。季节差分比较同一季度跨年的变化：

$$
\nabla_4 y_t=(1-B^4)y_t=y_t-y_{t-4}.
$$

因此第二年的季节差分是：

```text
2, 2, 3, 3
```

季节差分消除了四个季度反复出现的水平差异，同时保留了“今年比去年同期多多少”。它与普通一阶差分 $y_t-y_{t-1}$ 回答的不是同一个问题。

## 4. 七个符号其实只有两组角色

SARIMA 记作：

$$
\operatorname{ARIMA}(p,d,q)(P,D,Q)_m.
$$

| 参数 | 作用范围 | 含义 |
|---|---|---|
| $p,d,q$ | 相邻滞后 $1,2,\ldots$ | 普通 AR、差分、MA |
| $P,D,Q$ | 季节滞后 $m,2m,\ldots$ | 季节 AR、差分、MA |
| $m$ | 一个季节的观测数 | 月度年度周期常为 12，季度常为 4 |

完整形式是：

$$
\Phi(B^m)\phi(B)(1-B)^d(1-B^m)^D y_t
=c+\Theta(B^m)\theta(B)\varepsilon_t.
$$

学习时先分块读：普通部分、季节部分、差分部分，最后再相乘。

## 5. 为什么叫“乘法”季节模型

考虑没有差分和 MA 项的 ARIMA$(1,0,0)(1,0,0)_4$：

$$
(1-\phi B)(1-\Phi B^4)y_t=\varepsilon_t.
$$

展开：

$$
y_t=\phi y_{t-1}+\Phi y_{t-4}-\phi\Phi y_{t-5}+\varepsilon_t.
$$

模型不仅包含滞后 1 和滞后 4，还自然出现交叉滞后 5。SARIMA 不是把两个模型简单相加；普通动态和季节动态会相互作用。

若同时进行一次普通差分和一次季节差分：

$$
(1-B)(1-B^4)y_t=y_t-y_{t-1}-y_{t-4}+y_{t-5}.
$$

这也解释了为什么过度差分会迅速损失信息并放大噪声。

## 6. 从相关图提出候选，而不是套口诀

差分后观察：

- 低阶滞后主要帮助提出 $p,q$；
- $m,2m,\ldots$ 附近的峰值帮助提出 $P,Q$；
- 季节 ACF 在少数季节滞后截尾，可能提示季节 MA；
- 季节 PACF 在少数季节滞后截尾，可能提示季节 AR。

“可能提示”不等于识别完成。有限样本、混合 ARMA、异常值和错误差分都会破坏理想图形，最终仍需候选比较与残差检验。

## 7. 最强基线：seasonal naïve

seasonal naïve 直接使用上一个季节同位置的观测：

$$
\hat y_{T+h|T}=y_{T+h-m(k+1)},
$$

其中索引选择最近一个可用的同季节观测。直观地说：预测明年 3 月，就先用今年 3 月。

它简单，却已经捕获主要季节模式。SARIMA 若不能在滚动测试中稳定胜过它，复杂度就没有得到证明。

## 8. 建模与代码实验

运行前先预测：季节差分后，滞后 12 的相关峰应明显减弱；SARIMA 的训练拟合可能更好，但测试误差未必优于 seasonal naïve。

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

# 生成可复现的月度序列，再按时间切分；真实项目替换这里的数据即可
rng = np.random.default_rng(42)
n = 156
t = np.arange(n)
y = 20 + 0.08 * t + 3 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 0.7, n)
series = pd.Series(y, index=pd.date_range("2010-01-01", periods=n, freq="MS"))
train, test = series.iloc[:-24], series.iloc[-24:]

fit = SARIMAX(
    train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=True,
    enforce_invertibility=True,
).fit(disp=False)

sarima_pred = fit.get_forecast(steps=len(test)).predicted_mean
seasonal_naive = np.resize(np.asarray(train[-12:]), len(test))

sarima_mae = np.mean(np.abs(np.asarray(test) - sarima_pred))
naive_mae = np.mean(np.abs(np.asarray(test) - seasonal_naive))
print({"SARIMA": sarima_mae, "seasonal_naive": naive_mae})
# 输出示例：两个非负 MAE；具体数值随 statsmodels 版本可能略有差异
```

`np.resize` 只适合连续、无缺期、预测起点恰接训练末尾的教学示例。真实项目应保留时间索引并按具体季节位置对齐。

## 9. 诊断与评估的季节要求

1. 测试集至少覆盖一个完整季节，最好多个季节。
2. 残差 ACF 和 Ljung–Box 滞后要覆盖 $m$ 及其倍数。
3. 除总 MAE/RMSE 外，检查不同月份或季度是否系统偏差。
4. 滚动起点应覆盖不同季节位置，避免只在旺季或淡季验证。
5. 同时比较预测区间覆盖率与宽度；窄但经常漏掉真实值不是好区间。

## 10. 常见错误

- 看到月度数据便机械设置 $m=12$，没有说明季节机制。
- 同时取很大的 $p,q,P,Q$，导致参数过多、收敛失败或不稳定。
- 为消除所有相关峰同时增加 $d$ 和 $D$，造成过度差分。
- 只与普通 naïve 比较，不与 seasonal naïve 比较。
- 随机划分训练集和测试集，泄漏未来季节信息。
- 固定季节性明显变化后仍坚持 SARIMA，不考虑 Fourier、动态回归或状态空间方法。

## 11. 当堂练习

1. 月度序列 `[10, 12, 15, 20, 13, 14, 18, 24]` 假设 $m=4$，计算季节差分。
2. 展开 $(1-B)(1-B^4)y_t$。
3. ARIMA$(0,1,1)(1,1,0)_{12}$ 中，哪些参数处理相邻期，哪些处理年度季节关系？
4. 某 SARIMA 的 AICc 更低，但滚动 MAE 与 seasonal naïve 相同且区间更差，应该如何决策？

> [!answer]- 当堂练习答案
> 1. `[3, 2, 3, 4]`。  
> 2. $y_t-y_{t-1}-y_{t-4}+y_{t-5}$。  
> 3. 普通差分 $d=1$ 和普通 MA $q=1$ 处理相邻期；季节 AR $P=1$、季节差分 $D=1$ 与 $m=12$ 处理年度关系。  
> 4. 优先保留更简单的 seasonal naïve，除非 SARIMA 在其他重要目标或稳定性上有明确收益；训练期 AICc 不能替代样本外验收。

## 12. 过关标准

- [ ] 能说：解释七个符号，但不靠死记顺序。
- [ ] 能算：手算季节差分和普通—季节交叉差分。
- [ ] 能写：展开一个乘法 SARIMA 并指出交叉滞后。
- [ ] 能做：按时间拟合 SARIMA 并与 seasonal naïve 比较。
- [ ] 能判断：发现过度差分、错误周期和无价值复杂度。

## 13. 下一课与作业

- 下一课：[[L07-模型识别与参数估计]]
- 参考卡：[[SARIMA模型]]、[[差分运算]]、[[季节性与STL分解]]
- 正式作业：[[时间序列分析-课后作业-05-SARIMA与季节预测]]
- 课程入口：[[🗺️ 时间序列分析学习路径]]

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §9.9 Seasonal ARIMA models](https://otexts.com/fpp3/seasonal-arima.html)。

## 🃏 Anki 卡片

- SARIMA 的普通阶与季节阶分别处理什么？::$p,d,q$ 处理相邻期动态与普通差分；$P,D,Q$ 在周期 $m$ 的倍数滞后上处理季节动态与季节差分
- 季节差分公式是什么？::$\Delta_m y_t=y_t-y_{t-m}$，比较当前观测与上一个相同季节位置
- 为什么 SARIMA 必须与 seasonal naïve 比较？::复杂模型只有在相同滚动协议下优于“使用上个季节同位置”的简单基线，才证明额外结构有预测价值

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






