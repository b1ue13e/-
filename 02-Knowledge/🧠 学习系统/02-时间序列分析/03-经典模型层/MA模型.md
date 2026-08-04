---
type: study
topic: "MA模型"
course: "时间序列分析"
created: 2026-04-18
updated: 2026-08-02
status: completed
difficulty: intermediate
concept: ["移动平均模型", "有限冲击响应", "可逆性"]
prerequisites: ["白噪声", "自相关函数ACF", "滞后算子"]
related: ["AR模型", "ARMA模型", "模型识别"]
tags: [学习, 时间序列, MA模型]
flow: knowledge
kind: derivation
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/MA.html"
    locator: "Section 9.4: Moving average models and invertibility"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
---

# MA模型

> [!tip] 这张卡怎么学（60 分钟）
> 1. 先追踪一个创新在 MA(1)、MA(2) 中分别影响几期。
> 2. 再推导 MA(1) 的方差和一阶 ACF。
> 3. 最后比较 MA 模型与滑动平均平滑，写出两者建模对象的区别。
>
> **过关问题**：为什么 MA 的冲击有限，但还要满足可逆性？

移动平均模型 MA((q)) 把当前值写成当前及过去有限个创新冲击的线性组合：

$$
y_t=c+\varepsilon_t+\theta_1\varepsilon_{t-1}+\cdots+
\theta_q\varepsilon_{t-q},\qquad \varepsilon_t\sim WN(0,\sigma^2).
$$

这里的“移动平均”不是用于平滑趋势的滑动窗口均值。模型中的 (\varepsilon_t) 是不可直接观测的一步预测创新，参数通过整个序列联合估计。用滞后算子可写为 (y_t=c+\theta(B)\varepsilon_t)。

## 1. MA(1) 的性质

对 (y_t=c+\varepsilon_t+\theta\varepsilon_{t-1})，有

$$
\operatorname{Var}(y_t)=(1+\theta^2)\sigma^2,
\qquad
\rho_1=\frac{\theta}{1+\theta^2},
\qquad \rho_k=0\ (k>1).
$$

一次冲击只影响当前和下一期，因此 MA((q)) 的冲击响应在 (q) 期后严格归零。其理论 ACF 在 (q) 阶后截尾，PACF 通常拖尾。这与平稳 AR 模型的无限衰减冲击响应形成对照。

## 2. 可逆性为什么必要

不同 (\theta) 可能产生相同自相关结构。例如 MA(1) 的 (\theta) 与 (1/\theta) 给出相同 (\rho_1)。为获得唯一且稳定的创新表示，通常要求 (\theta(z)=0) 的根在单位圆之外；MA(1) 即 (|\theta|<1)。可逆性允许把创新写成当前和过去观测的收敛组合，便于估计与预测。

```python
from statsmodels.tsa.arima.model import ARIMA

fit = ARIMA(train, order=(0, 0, 2), trend="c").fit()
print(fit.summary())
pred = fit.get_forecast(steps=12)
interval = pred.conf_int(alpha=0.05)
```

## 3. 识别与验收

1. 确保序列已近似平稳；MA 部分不能替代必要的差分或趋势建模。
2. 用 ACF 的低阶截尾提出候选 (q)，但不要仅凭肉眼定阶。
3. 用最大似然估计后检查可逆根、参数标准误和残差[[纯随机性检验]]。
4. 用 AICc 在**相同差分阶数**的候选中比较，再用滚动样本外误差最终验收。
5. 报告创新方差和预测区间；只报告系数显著性不能证明预测有效。

## 4. 预测直觉与边界

已估计的最近创新会进入短期预测；当预测步长超过 (q) 后，未知未来创新的条件期望为零，点预测回到长期均值。MA 适合描述短暂冲击，但对长持续性往往需要较高阶，此时低阶[[AR模型]]或[[ARMA模型]]更简洁。异常值会被误认为大创新并影响邻近期，结构突变也会破坏固定参数假设。

## 5. 开放教材定位

主线精读 FPP3 §9.4，重点区分 MA 模型和移动平均平滑，推导 MA(1) 方差与 ACF，并解释可逆性。验收标准是能从 ACF 提出候选、检查可逆根，并证明残差不再保留线性结构。

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §9.4 Moving average models](https://otexts.com/fpp3/MA.html)，MA((q)) 定义、冲击表示与可逆性。
