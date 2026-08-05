---
type: study
topic: "自相关函数 ACF"
course: "时间序列分析"
created: 2026-04-18
updated: 2026-08-02
status: completed
difficulty: intermediate
concept: ["自相关函数", "序列相关", "时间序列诊断"]
prerequisites: ["协方差", "平稳性"]
related: ["偏自相关函数PACF", "白噪声", "ARIMA模型"]
tags: [学习, 时间序列, ACF]
flow: knowledge
kind: concept
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/acf.html"
    locator: "Section 2.8: Autocorrelation; sample ACF, trend and seasonality patterns"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/wn.html"
    locator: "Section 2.9: White noise; approximate ACF reference bounds"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
---

# 自相关函数 ACF

自相关函数（autocorrelation function, ACF）描述同一序列在不同时间间隔上的线性相关。它回答的是“当前值与滞后 (k) 期的值是否一起变化”，而不是证明因果关系。对弱平稳过程，滞后 (k) 的总体自相关为

$$
\rho_k=\frac{\gamma_k}{\gamma_0}
=\frac{\operatorname{Cov}(Y_t,Y_{t-k})}{\operatorname{Var}(Y_t)},\qquad -1\le \rho_k\le 1.
$$

给定长度为 (T) 的观测序列，常用样本估计是

$$
r_k=\frac{\sum_{t=k+1}^{T}(y_t-\bar y)(y_{t-k}-\bar y)}
{\sum_{t=1}^{T}(y_t-\bar y)^2}.
$$

分母固定为全样本离差平方和，因此不同滞后的 (r_k) 可放在同一张相关图中比较。

## 1. 如何读 ACF 图

- **短滞后缓慢衰减且长期为正**：常见于含趋势或高度持久的非平稳序列，先检查[[平稳性]]，不要直接据此选择 AR 阶数。
- **在季节周期 (m,2m,3m,ldots) 出现峰值**：提示季节结构；月度数据的 12、24 阶峰值是典型例子。
- **少数低阶显著、随后快速截尾**：可能支持 MA 类结构，但必须结合[[PACF（偏自相关函数）]]、残差诊断和样本外表现判断。
- **残差 ACF 仍有成片结构**：模型遗漏了可预测信息；一个合格的预测模型应使残差接近[[白噪声]]。

白噪声假设下，单个样本自相关常用近似参考带为 (\pm1.96/\sqrt{T})。它只是逐滞后的近似界限：同时查看很多滞后时，偶尔越界并不自动否定白噪声，应配合 Ljung–Box 等联合检验。

## 2. 最小可复现实验

```python
import numpy as np
from statsmodels.tsa.stattools import acf

rng = np.random.default_rng(7)
e = rng.normal(size=500)
y = np.zeros(500)
for t in range(1, len(y)):
    y[t] = 0.7 * y[t-1] + e[t]

rho = acf(y, nlags=10, fft=True)
print(np.round(rho, 3))
```

AR(1) 理论上有 (\rho_k=\phi^k)，所以本例 ACF 应近似按 (0.7^k) 衰减。验收时同时记录样本量、最大滞后、是否去趋势/差分；把原序列与差分后序列的 ACF 并排比较。

## 3. 边界与误区

1. ACF 只捕捉线性依赖；(r_k\approx0) 不等于统计独立。
2. 趋势、季节性和结构突变都会制造“伪相关”，非平稳原序列的 ACF 不能按平稳模型机械解释。
3. ACF 不是选阶按钮。AR/MA/[[ARIMA模型]] 的候选阶数还需用信息准则、残差白噪声和滚动样本外误差验收。
4. 金融价格水平常呈高持久性，而收益率可能近似零自相关；二者的建模对象不能混用。

## 4. 开放教材定位

主线精读 FPP3 §2.8 的定义、趋势与季节图形，再用 §2.9 校准白噪声参考带。掌握标准是：能从公式解释每个滞后的含义，并能说明为何“一个柱越界”不等于序列必然可预测。

## 参考资料

- Hyndman & Athanasopoulos, [Forecasting: Principles and Practice, 3rd ed., §2.8 Autocorrelation](https://otexts.com/fpp3/acf.html)，样本 ACF、趋势与季节模式。
- Hyndman & Athanasopoulos, [§2.9 White noise](https://otexts.com/fpp3/wn.html)，白噪声 ACF 的近似参考界限。
