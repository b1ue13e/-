---
type: study
topic: "SARIMA模型"
course: "时间序列分析"
created: 2026-04-18
updated: 2026-08-02
status: completed
difficulty: advanced
concept: ["季节ARIMA", "季节差分", "季节相关"]
prerequisites: ["ARIMA模型", "差分运算", "自相关函数ACF"]
related: ["AR模型", "MA模型", "模型识别"]
tags: [学习, 时间序列, SARIMA]
flow: knowledge
kind: derivation
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/seasonal-arima.html"
    locator: "Section 9.9: Seasonal ARIMA models, identification, diagnostics and test-set evaluation"
    source_type: "open-textbook"
    license: "截至 2026-08-07 未发现适用于教材正文/题目的开放再分发许可；link-only，仅保留原创释义与章节定位。"
    verified_at: 2026-08-02
stage_moc: "[[🧭 阶段3-经典预测模型]]"
upstream: ["[[L06-SARIMA与季节预测]]"]
---
# SARIMA模型

> [!tip] 这张卡怎么学（60 分钟）
> 1. 先复习 ARIMA，再把相同结构复制到季节滞后 \(m\)。
> 2. 手动展开一个 \((1,1,0)(1,1,0)_{12}\) 模型。
> 3. 用月度数据比较 seasonal naïve 和 SARIMA，而不是只看拟合优度。
>
> **过关问题**：普通差分、季节差分、普通 AR 和季节 AR 各解决什么问题？

SARIMA 在非季节 ARIMA 上增加以季节周期 (m) 为间隔的 AR、差分和 MA 项，记作

$$\operatorname{ARIMA}(p,d,q)(P,D,Q)_m.$$

完整滞后算子形式为

$$
\Phi(B^m)\phi(B)(1-B)^d(1-B^m)^D y_t
=c+\Theta(B^m)\theta(B)\varepsilon_t.
$$

小写参数描述相邻期动态，大写参数描述 (m,2m,ldots) 季节滞后动态。月度序列通常 (m=12)，季度序列通常 (m=4)；但周期必须来自采样频率和业务机制，不能仅由图形猜测。

## 1. 乘法季节结构

以 (\operatorname{ARIMA}(1,1,1)(1,1,1)_4) 为例：

$$
(1-\phi B)(1-\Phi B^4)(1-B)(1-B^4)y_t
=(1+\theta B)(1+\Theta B^4)\varepsilon_t.
$$

季节与非季节多项式相乘会产生交叉滞后。例如两个 AR 因子展开后含 (B^5) 项，因此 SARIMA 不是把两组独立模型简单相加。

季节差分 ((1-B^m)y_t=y_t-y_{t-m}) 消除重复季节水平；若仍有趋势，再考虑普通一阶差分。过度差分会放大噪声并制造额外负相关，所以使用能达到平稳的最少差分。

## 2. 候选识别

- 季节 MA((Q)) 常在 ACF 的季节滞后截尾、PACF 季节滞后拖尾。
- 季节 AR((P)) 常在 PACF 的季节滞后截尾、ACF 季节滞后拖尾。
- 非季节 (p,q) 主要看低阶滞后，季节 (P,Q) 主要看 (m,2m,ldots)。

这些只是生成候选的启发式。应固定 (d,D) 后用 AICc 比较少量候选，并检查参数根和残差。

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

rng = np.random.default_rng(65)
t = np.arange(144)
y = 30 + 0.05 * t + 4 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 0.8, len(t))
train = pd.Series(y, index=pd.date_range("2012-01-01", periods=len(y), freq="MS"))

fit = SARIMAX(
    train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=True, enforce_invertibility=True
).fit(disp=False)
fc = fit.get_forecast(steps=12)
print("converged:", fit.mle_retvals.get("converged"))
print("forecast length:", len(fc.predicted_mean))
```

## 3. 严格验收流程

1. 按时间留出完整季节周期作测试集，不能随机打乱。
2. 比较 seasonal naïve 基线；复杂模型至少应在多个预测步长上稳定胜出。
3. 残差 ACF 和 Ljung–Box 的最大滞后应覆盖季节周期，并扣除已估参数自由度。
4. 同时报告 MAE/RMSE、预测区间覆盖率和区间宽度。
5. 用滚动起点评估，避免单个测试窗口碰巧有利。

## 4. 边界与替代方案

SARIMA 假设季节周期固定且线性结构相对稳定。多重季节性、很长季节周期或平滑变化季节模式会导致参数爆炸，可考虑 Fourier 项加 ARIMA 误差、动态回归或状态空间模型。节假日、促销和制度变化不应硬塞进季节项，应作为外生变量或干预项显式建模。

## 5. 知识连接与验收台账

SARIMA 以[[ARIMA模型]]为骨架，把[[AR模型]]和[[MA模型]]多项式扩展到季节滞后；普通与季节算子统一见[[差分运算]]。残差必须经过覆盖季节周期的[[纯随机性检验]]，最终按[[预测与评估]]协议与 seasonal naïve 比较。

候选台账应明确记录 ((p,d,q)(P,D,Q)_m)、变换、训练区间、AICc、根条件、Ljung–Box 滞后与自由度、逐 horizon 误差和区间覆盖率。若复杂候选只在单个窗口略优，而参数或误差随窗口剧烈变化，应保留更简单稳定的模型。

## 6. 开放教材定位

主线精读 FPP3 §9.9，复现季节差分、候选识别、AICc、残差和测试集评估的完整链路。掌握标准是能展开一个乘法 SARIMA 方程，说明每个阶数的角色，并用 seasonal naïve 基线否定无增益模型。

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §9.9 Seasonal ARIMA models](https://otexts.com/fpp3/seasonal-arima.html)，季节算子、识别、残差和测试集评估。

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






