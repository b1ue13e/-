---
type: study
course: "时间序列分析"
lesson: 5
topic: "ARMA与ARIMA建模闭环"
created: 2026-08-02
updated: 2026-08-05
status: planned
mastery: 0
difficulty: intermediate
flow: knowledge
kind: concept
concept: ["ARIMA", "差分还原", "建模闭环"]
prerequisites: ["平稳性与差分", "AR模型", "MA模型"]
related: ["L04-MA模型与有限冲击", "L06-SARIMA与季节预测", "ARIMA模型"]
next: ["L06-SARIMA与季节预测"]
anki_deck: "时间序列分析::主线课程"
anki_tags: ["时间序列分析", "L05", "ARMA", "ARIMA", "建模闭环"]
tags: [学习, 时间序列, 教师式课程, ARMA, ARIMA]
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/non-seasonal-arima.html"
    locator: "Section 9.5: Non-seasonal ARIMA models"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/arima-r.html"
    locator: "Section 9.7: ARIMA modelling in R"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
---

# L05｜ARMA 与 ARIMA 建模闭环

> **预计用时**：90 分钟　**当前掌握**：0 / 1 / 2 / 3

## 0. 这节课解决什么问题

AR 适合描述持续衰减的记忆，MA 适合描述有限长度的冲击，但真实序列可能同时具有两者；更常见的是，原序列还带趋势而不平稳。

本课把前四课连成一条完整思路：**先用差分处理非平稳，再用 ARMA 描述差分后序列的动态，最后通过残差和样本外预测验收。**

## 1. 学习目标

学完后，不看笔记能够：

- 用自己的话解释 ARMA、ARIMA 以及字母 `I`；
- 把 ARIMA$(p,d,q)$ 写成滞后算子形式；
- 从原序列手算差分，并解释预测如何还原到原尺度；
- 建立少量候选，而不是凭 ACF/PACF 一次定型；
- 用信息准则、残差诊断和滚动预测完成模型验收。

## 2. 课前诊断

> [!question] 先判断
> ARMA(1,1) 与 ARIMA(1,1,1) 只差一个字母，因此它们对同一条数据表达的是近似相同的模型。对吗？

> [!answer]- 诊断答案
> 不对。ARMA(1,1) 直接假设原序列平稳；ARIMA(1,1,1) 先对原序列做一次差分，再让差分序列服从 ARMA(1,1)。一次差分改变了模型对象、长期行为和预测还原方式。

## 3. 从价格到变化量：`I` 到底做了什么

考虑价格序列：

```text
100, 102, 105, 104, 108
```

一阶差分为：

```text
2, 3, -1, 4
```

若价格水平不平稳，但变化量近似平稳，我们不直接给价格硬套 ARMA，而是给变化量建模。`I` 表示 integrated：模型通过累加差分预测回到原水平。

例如最后价格是 108，下一期变化量预测为 2.5，则水平预测为：

$$
\hat y_{T+1|T}=108+2.5=110.5.
$$

## 4. ARMA：把两种冲击传播合在一起

ARMA(1,1) 写作：

$$
y_t=c+\phi y_{t-1}+\varepsilon_t+\theta\varepsilon_{t-1}.
$$

- $\phi y_{t-1}$：过去状态继续传递，形成逐渐衰减的记忆；
- $\theta\varepsilon_{t-1}$：最近的意外直接影响当前期；
- $\varepsilon_t$：当前无法提前知道的新信息。

因此 ARMA 的 ACF 和 PACF 往往都拖尾。相关图不再给出简单“截尾口诀”，只能帮助提出候选。

## 5. ARIMA 的统一表达

用滞后算子 $B y_t=y_{t-1}$，非季节 ARIMA$(p,d,q)$ 可写为：

$$
\phi(B)(1-B)^d y_t=c+\theta(B)\varepsilon_t,
$$

其中：

- $p$：差分后序列的 AR 阶数；
- $d$：差分次数；
- $q$：差分后序列的 MA 阶数。

以 ARIMA(1,1,1) 为例：

$$
(1-\phi B)(1-B)y_t=c+(1+\theta B)\varepsilon_t.
$$

先令 $w_t=(1-B)y_t=y_t-y_{t-1}$，就得到一个针对 $w_t$ 的 ARMA(1,1)。这一步能避免把所有符号同时展开造成的认知负担。

## 6. 常数、均值与漂移

常数项的解释依赖 $d$：

- 当 $d=0$，常数通常与平稳过程的非零均值有关；
- 当 $d=1$，差分方程中的常数会在原尺度形成漂移；
- 当 $d\ge 2$，继续加入多项式趋势很容易产生不合理的远期外推。

所以不能看到软件里的 `const` 或 `trend` 就机械保留；应先说明它在原尺度意味着什么。

## 7. 建模闭环：每一步回答一个问题

| 步骤 | 要回答的问题 | 证据 |
|---|---|---|
| 1. 画图与理解业务 | 异常、趋势、季节和结构变化在哪里？ | 原序列图、领域背景 |
| 2. 变换与差分 | 方差是否稳定？最少需要几次差分？ | Box-Cox/对数、差分图、检验 |
| 3. 提出候选 | 哪几个低阶 $(p,q)$ 值值得试？ | ACF/PACF、简约原则 |
| 4. 参数估计 | 模型是否收敛且满足平稳/可逆约束？ | 估计结果、特征根 |
| 5. 候选比较 | 谁在同一建模目标下更简洁？ | AICc 等信息准则 |
| 6. 残差诊断 | 是否还留下可预测相关性？ | 残差图、ACF、Ljung–Box |
| 7. 样本外验收 | 是否真的优于简单方法？ | rolling-origin、基线、分 horizon 误差 |

> [!important] 三道闸门
> 相关图用于**提名**，AICc 用于**筛选**，残差与样本外评估用于**验收**。任何一个指标都不能单独宣布模型正确。

## 8. 最小代码实验

运行前先写预测：价格序列通常需要一次差分；更复杂模型的训练拟合可能更好，但测试集未必更好。

```python
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

y = np.array([100, 102, 105, 104, 108, 111, 110, 114, 116, 117], dtype=float)
train, test = y[:-2], y[-2:]

candidates = [(1, 1, 0), (0, 1, 1), (1, 1, 1)]
for order in candidates:
    fit = ARIMA(train, order=order, trend="t").fit()
    pred = fit.forecast(steps=len(test))
    mae = np.mean(np.abs(test - pred))
    print(order, "AIC=", round(fit.aic, 2), "test MAE=", round(mae, 2))
```

这只是最小演示，不是正式评估。十个观测太少，且一次固定切分很不稳定；正式作业要使用更长序列和滚动起点。

## 9. 常见错误

- 对原序列和不同差分阶数的模型直接比较 AIC/AICc，并据此选 $d$；它们的似然基准未必可直接比较。
- 把 `auto_arima` 的输出当结论，而不检查差分、根、残差和样本外表现。
- 残差通过白噪声检验就宣称模型有用；它仍可能输给 naïve 基线。
- 为得到更漂亮的 ACF 反复差分，导致过度差分和负一阶相关。
- 忘记逆差分或逆变换，让最终预测失去原业务单位。

## 10. 当堂练习

1. 将 `[20, 23, 25, 24]` 一阶差分；若下一期差分预测为 2，原尺度预测是多少？
2. ARIMA(2,1,0) 实际对哪个序列拟合 AR(2)？
3. 某 ARIMA 残差通过 Ljung–Box，但测试 MAE 高于 naïve。是否应采用？为什么？
4. 为什么不同 $d$ 的候选不应只靠 AICc 决定？

> [!answer]- 当堂练习答案
> 1. 差分为 `[3, 2, -1]`；最后水平 24 加预测变化 2，得到 26。  
> 2. 对一阶差分 $w_t=y_t-y_{t-1}$ 拟合 AR(2)。  
> 3. 通常不应。残差无明显自相关只是必要证据，不能替代样本外价值；还应检查评估设计和预测区间。  
> 4. 不同差分会改变被拟合的数据和似然常数；应结合图形、单位根/差分判断及样本外表现决定 $d$。

## 11. 过关标准

- [ ] 能说：用一句话分别解释 AR、MA、I。
- [ ] 能算：手算差分，并把一步预测还原到原尺度。
- [ ] 能写：写出 ARIMA$(p,d,q)$ 的滞后算子形式。
- [ ] 能做：完成至少三个候选的估计、残差和滚动比较。
- [ ] 能判断：不把自动选模、AICc 或白噪声检验当最终答案。

## 12. 下一课与作业

- 下一课：[[L06-SARIMA与季节预测]]
- 参考卡：[[ARMA模型]]、[[ARIMA模型]]、[[模型识别]]、[[参数估计]]
- 正式作业：[[HW05-ARMA与ARIMA建模闭环阶梯作业]]
- 课程入口：[[📚 时间序列课程学习面板]]

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §9.5 Non-seasonal ARIMA models](https://otexts.com/fpp3/non-seasonal-arima.html)。
- Hyndman & Athanasopoulos, [FPP3 §9.7 ARIMA modelling](https://otexts.com/fpp3/arima-r.html)。

## 🃏 Anki 卡片

- ARIMA$(p,d,q)$ 的三个阶数分别控制什么？::$p$ 控制差分后序列的 AR 记忆，$d$ 控制普通差分次数，$q$ 控制创新的有限 MA 传播
- 不同差分阶数的模型为什么不能机械比较 AICc？::差分改变了拟合对象、有效样本和似然口径，应先依据机制与平稳化证据确定差分方案
- ARIMA 候选的完整验收链是什么？::数据与信息边界、变换/差分、有限候选、估计稳定性、残差诊断、滚动样本外评估、与朴素基线比较
