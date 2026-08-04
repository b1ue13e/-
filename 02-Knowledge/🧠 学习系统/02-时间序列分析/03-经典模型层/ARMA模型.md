---
type: study
topic: "ARMA模型"
created: 2026-04-18
updated: 2026-08-02
status: completed
difficulty: intermediate
concept: ["ARMA", "自回归", "移动平均"]
prerequisites: ["平稳时间序列", "白噪声", "自相关函数ACF"]
related: ["ARIMA模型", "AR模型", "MA模型"]
tags: [学习, 时间序列, ARMA]
flow: knowledge
kind: derivation
sources:
  - title: "Forecasting: Principles and Practice (3e)"
    url: "https://otexts.com/fpp3/arima.html"
    locator: "Chapter 9, Sections 9.2-9.4: backshift notation, AR and MA models"
    source_type: "official-free-textbook"
    license: "official-free online"
    verified_at: 2026-08-02
---

# ARMA 模型

ARMA$(p,q)$ 用过去观测值的线性组合与过去创新项的线性组合描述平稳时间序列。AR 部分提供递归记忆，MA 部分描述冲击在有限滞后内的传播。

## 1. 模型定义

对均值已处理的序列 $y_t$：

$$
y_t=\phi_1y_{t-1}+\cdots+\phi_py_{t-p}
+\varepsilon_t+\theta_1\varepsilon_{t-1}+\cdots+\theta_q\varepsilon_{t-q},
$$

其中 $\varepsilon_t$ 是方差为 $\sigma^2$ 的[[02-Knowledge/🧠 学习系统/02-时间序列分析/02-统计基础层/白噪声|白噪声]]。用滞后算子 $B$ 可写为

$$
\phi(B)y_t=\theta(B)\varepsilon_t,
$$

$$
\phi(B)=1-\sum_{i=1}^p\phi_iB^i,
\qquad
\theta(B)=1+\sum_{j=1}^q\theta_jB^j.
$$

MA 多项式的正负号在不同软件和教材中可能不同，解释参数前必须确认约定。

## 2. 平稳性与可逆性

AR 多项式 $\phi(z)=0$ 的根都在单位圆外，是因果平稳 ARMA 的常用条件。MA 多项式 $\theta(z)=0$ 的根都在单位圆外，对应可逆性，使创新项可由当前和过去观测唯一表示。

若原序列需要差分才能平稳，应使用[[02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/ARIMA模型|ARIMA$(p,d,q)$]]，而不是直接对非平稳水平序列套 ARMA。

## 3. ACF/PACF 识别只是候选生成

- 纯 AR$(p)$：PACF 理论上在 $p$ 阶后截尾，ACF 拖尾。
- 纯 MA$(q)$：ACF 理论上在 $q$ 阶后截尾，PACF 拖尾。
- ARMA：ACF 与 PACF 通常都拖尾。

有限样本、接近相消的 AR/MA 参数和异常值都会模糊这些模式。因此应结合[[02-Knowledge/🧠 学习系统/02-时间序列分析/02-统计基础层/自相关函数ACF|ACF]]、信息准则、残差诊断和时间外验证，而不是只凭图形定阶。

## 4. 最小模拟与拟合

```python
import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima.model import ARIMA

rng = np.random.default_rng(5)
process = ArmaProcess(ar=[1, -0.6], ma=[1, 0.3])
y = process.generate_sample(600, distrvs=rng.normal)
fit = ARIMA(y, order=(1, 0, 1), trend="n").fit()

assert fit.nobs == 600
assert np.isfinite(fit.aic)
```

一次拟合得到有限 AIC 不等于模型正确。还需检查残差 ACF、Ljung–Box 检验、参数稳定性以及留出区间预测误差。

## 5. 一步预测直觉

对 ARMA$(1,1)$：

$$
y_t=\phi y_{t-1}+\varepsilon_t+\theta\varepsilon_{t-1}.
$$

在时刻 $t$ 已知信息下，一步预测为

$$
\hat y_{t+1|t}=\phi y_t+\theta\hat\varepsilon_t,
$$

因为未来创新 $\varepsilon_{t+1}$ 的条件期望为零。多步预测时，未知未来创新都置为零并递归代入预测值。

## 6. 边界与误区

1. ARMA 主要描述线性条件均值相关，不能自动处理波动聚集和结构突变。
2. 阶数越高不一定越好；高阶模型更易过拟合且参数难解释。
3. 残差通过白噪声检验只是必要诊断之一，不证明模型为真实生成机制。
4. 同一序列可能有多个近似等价模型，应比较预测性能与简洁性。
5. 季节性需要显式季节结构或预处理，不能只靠增加普通滞后阶数。

## 🌐 开放教材定位

> 以下条目是本卡的知识主线与定位依据；算法 API 和软件文档只作实现对照。

- [Forecasting: Principles and Practice (3e)](https://otexts.com/fpp3/arima.html) — `Chapter 9, Sections 9.2-9.4: backshift notation, AR and MA models`；官方免费访问，不推定再分发权。

引用时继续保留 `locator`，不把教材首页或搜索摘要当作具体论据。

## 参考资料

- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, Chapter 9：https://otexts.com/fpp3/arima.html
- statsmodels, `ARIMA` 官方文档：https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html

