---
type: study
topic: "ARIMA模型"
tags: [学习, 时间序列, ARIMA, 预测]
created: 2026-04-16
updated: 2026-08-02
status: completed
difficulty: intermediate
concept: ["ARIMA", "差分", "自相关建模"]
prerequisites: ["平稳时间序列", "差分运算", "白噪声"]
related: ["ARMA模型", "SARIMA模型", "残差诊断"]
flow: knowledge
kind: concept
sources:
  - title: "Forecasting: Principles and Practice (3e)"
    url: "https://otexts.com/fpp3/arima.html"
    locator: "Chapter 9, especially Sections 9.1 and 9.5-9.9"
    source_type: "official-free-textbook"
    license: "official-free online"
    verified_at: 2026-08-02
---

# ARIMA 模型

ARIMA（AutoRegressive Integrated Moving Average）通过差分把非平稳序列转成近似平稳序列，再用 ARMA 结构描述其自相关。ARIMA$(p,d,q)$ 中，$p$ 是自回归阶数，$d$ 是差分次数，$q$ 是移动平均阶数。

## 1. 模型形式

令滞后算子 $By_t=y_{t-1}$，差分后序列为

$$
w_t=(1-B)^d y_t.
$$

非季节 ARIMA 可写成

$$
\phi(B)(1-B)^d y_t=c+\theta(B)\varepsilon_t,
$$

其中

$$
\phi(B)=1-\phi_1B-\cdots-\phi_pB^p,
\qquad
\theta(B)=1+\theta_1B+\cdots+\theta_qB^q.
$$

$\varepsilon_t$ 应近似零均值、不相关且方差稳定。不同教材对 MA 项正负号可能采用不同约定，比较参数时必须先确认定义。

## 2. 为什么差分

ARMA 部分要求建模对象近似弱平稳。一次差分 $\Delta y_t=y_t-y_{t-1}$ 可消除随机趋势；二次差分是对一次差分再差分。$d$ 不是越大越好：过度差分会放大噪声，并常在 ACF 中出现强负的一阶相关。

常见特例：

- ARIMA$(p,0,0)$ 是 AR$(p)$；
- ARIMA$(0,0,q)$ 是 MA$(q)$；
- ARIMA$(0,1,0)$ 无漂移时是随机游走；
- 存在稳定季节周期时考虑[[02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/SARIMA模型|SARIMA]]，而不是盲目提高 $p,q$。

## 3. 建模流程

1. 画时序图，识别趋势、季节性、异常点和结构突变。
2. 必要时做 Box–Cox 等方差稳定变换。
3. 结合领域判断、单位根检验和差分后图形选择 $d$。
4. 用 ACF/PACF 提出若干 $p,q$ 候选，而非机械套用截尾口诀。
5. 用极大似然估计参数，以 AICc 等准则比较候选。
6. 检查残差 ACF 和 Ljung–Box 检验；残差应近似白噪声。
7. 在按时间留出的测试区间做滚动预测验证，并报告预测区间。

## 4. 最小可运行例子

```python
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

rng = np.random.default_rng(7)
y = np.cumsum(rng.normal(size=160))  # 随机游走
train, test = y[:140], y[140:]

fit = ARIMA(train, order=(0, 1, 0), trend="n").fit()
forecast = fit.get_forecast(steps=len(test))
mean = forecast.predicted_mean
interval = forecast.conf_int(alpha=0.05)

assert len(mean) == len(test)
assert interval.shape == (len(test), 2)
```

该例只验证接口和维度，不证明 ARIMA$(0,1,0)$ 适用于任意真实数据。真实建模还必须做残差诊断并与季节朴素预测等基线比较。

## 5. 预测与不确定性

多步预测把未来误差的条件期望置为零，并递归使用先前预测值。预测区间通常随预测步长扩大。若残差相关、重尾、异方差或存在结构突变，标准区间可能过窄；这时应重新建模、采用自助法区间或显式处理波动性。

## 6. 失效边界

- ARIMA 主要利用单变量线性自相关，不能自动吸收促销、政策等外生信息；需要时使用动态回归/ARIMAX。
- 周期随时间变化、强非线性或多重季节性可能需要其他模型。
- 随机划分训练测试集会泄露未来信息，时间序列必须保持时间顺序。
- 仅凭训练集 AIC 最小不能保证测试期预测最好。

## 知识连接

- 前置：[[平稳性|平稳时间序列]]、[[02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/差分运算|差分运算]]。
- 相邻：[[02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/ARMA模型|ARMA 模型]]、[[02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/SARIMA模型|SARIMA 模型]]。

## 🌐 开放教材定位

> 以下条目是本卡的知识主线与定位依据；算法 API 和软件文档只作实现对照。

- [Forecasting: Principles and Practice (3e)](https://otexts.com/fpp3/arima.html) — `Chapter 9, especially Sections 9.1 and 9.5-9.9`；官方免费访问，不推定再分发权。

引用时继续保留 `locator`，不把教材首页或搜索摘要当作具体论据。

## 参考资料

- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed., Chapter 9：https://otexts.com/fpp3/arima.html
- Hyndman & Athanasopoulos, “Non-seasonal ARIMA models”：https://otexts.com/fpp3/non-seasonal-arima.html

