---
type: study
topic: "AR模型"
course: "时间序列分析"
created: 2026-04-18
updated: 2026-08-02
status: completed
difficulty: intermediate
concept: ["自回归模型", "平稳性", "冲击衰减"]
prerequisites: ["平稳时间序列", "白噪声", "自相关函数ACF"]
related: ["MA模型", "ARMA模型", "PACF（偏自相关函数）"]
tags: [学习, 时间序列, AR模型]
flow: knowledge
kind: derivation
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/AR.html"
    locator: "Section 9.3: Autoregressive models, examples and stationarity restrictions"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
---

# AR模型

> [!tip] 这张卡怎么学（60 分钟）
> 1. 只看 AR(1)，分别代入 \(\phi=0.7\)、\(-0.7\)、1。
> 2. 手算一次冲击后第 1、2、3 期的影响，再读均值、方差和 ACF。
> 3. 最后运行模拟，确认衰减、振荡或永久保留是否符合预期。
>
> **过关问题**：为什么 \(|\phi|<1\) 是均值回归的关键？

自回归模型用序列自己的过去值解释当前值。AR((p)) 写成

$$
y_t=c+\phi_1y_{t-1}+\cdots+\phi_py_{t-p}+\varepsilon_t,
\qquad \varepsilon_t\sim WN(0,\sigma^2).
$$

它不是把普通回归直接套到任意时间序列：平稳性、创新白噪声以及时间顺序决定了估计和推断是否可靠。使用滞后算子 (B)，可写为 (\phi(B)y_t=c+\varepsilon_t)，其中 (\phi(B)=1-\phi_1B-\cdots-\phi_pB^p)。平稳条件是特征多项式 (\phi(z)=0) 的根都在单位圆之外。

## 1. AR(1) 的核心性质

对

$$y_t=c+\phi y_{t-1}+\varepsilon_t,$$

若 (|\phi|<1)，无条件均值和方差为

$$
\mu=\frac{c}{1-\phi},\qquad
\operatorname{Var}(y_t)=\frac{\sigma^2}{1-\phi^2},
$$

自相关函数为 (\rho_k=\phi^k)。因此正 (\phi) 产生同方向缓慢衰减，负 (\phi) 产生正负交替衰减；(\phi=1) 退化为带单位根的随机游走。冲击 (\varepsilon_t) 对 (h) 期后的影响是 (\phi^h)，平稳模型中最终消失。

## 2. 识别与预测

理想 AR((p)) 的 ACF 拖尾，而 PACF 在 (p) 阶后截尾；有限样本中这种图形只是候选生成规则。最终阶数应结合 AICc、参数稳定性、[[纯随机性检验]]和滚动样本外误差。

AR(1) 的 (h) 步条件均值为

$$
\hat y_{t+h|t}=\mu+\phi^h(y_t-\mu).
$$

预测逐步回归长期均值；预测区间随步长扩大，最终接近无条件方差。

```python
from statsmodels.tsa.ar_model import AutoReg

fit = AutoReg(train, lags=2, trend="c", old_names=False).fit()
forecast = fit.predict(start=len(train), end=len(train)+11)
print(fit.params)
```

## 3. 验收流程

1. 先证明建模序列近似平稳；价格水平等单位根序列不能直接拟合平稳 AR。
2. 用 ACF/PACF 提出少量候选阶数，避免搜索到很高阶。
3. 检查特征根、系数不确定性和残差白噪声；显著系数不保证整体模型合格。
4. 与均值、朴素预测及[[ARMA模型]]在相同滚动窗口比较。
5. 报告点预测之外的区间覆盖率，并检查结构突变前后参数稳定性。

## 4. 易错边界

- PACF “截尾”不是精确阶数判决器，季节性、测量误差和短样本都会扭曲图形。
- 高阶 AR 能逼近很多相关结构，但参数多、共线性强，可能只是在样本内记忆噪声。
- 含确定趋势的序列与随机趋势不同：前者可去趋势，后者通常需要差分。
- AR 描述条件均值的线性动态；残差无相关不代表方差恒定或尾部风险已建模。

## 5. 开放教材定位

主线精读 FPP3 §9.3，先掌握 AR(1) 的平稳限制、均值回归和 ACF，再扩展到 AR((p)) 的根条件。验收是能从系数解释冲击持续性，并用残差和样本外预测否定不合格候选。

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §9.3 Autoregressive models](https://otexts.com/fpp3/AR.html)，AR((p)) 定义、参数图形与平稳限制。
