---
type: study
course: "时间序列分析"
lesson: 3
topic: "AR模型与均值回归"
status: planned
mastery: 0
difficulty: intermediate
flow: knowledge
kind: concept
prerequisites: ["ACF、PACF与白噪声", "等比数列"]
next: ["MA模型", "ARMA模型"]
tags: [学习, 时间序列, 教师式课程, AR模型]
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/AR.html"
    locator: "Section 9.3: Autoregressive models"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
---

# L03｜AR 模型与均值回归

> **预计用时**：75 分钟　**当前掌握**：0 / 1 / 2 / 3

## 0. 这节课解决什么问题

室温、利率偏差或设备状态往往具有惯性：本期偏高，下一期通常仍偏高，但偏离不会永久保持。AR 模型用过去的序列值描述这种“有记忆、会衰减”的动态。

本课不先背 AR((p))，而是从 AR(1) 学会三件事：冲击怎样传播、为什么会回到均值、怎样产生多步预测。

## 1. 学习目标

学完后，不看笔记能够：

- 从递推式解释 AR(1) 的记忆；
- 推导长期均值与冲击响应；
- 判断正、负和单位根参数产生的不同图形；
- 手算两步、三步预测；
- 用 ACF/PACF、残差和样本外结果检验候选 AR 模型。

## 2. 课前诊断

> [!question] 心算
> 若 (y_t=0.5y_{t-1}+\varepsilon_t\)，今天发生大小为 8 的额外冲击，忽略后续新冲击，它在未来三期分别留下多大影响？

> [!answer]- 诊断答案
> 下一期 4，下两期 2，下三期 1。影响按 (8\times0.5^h) 衰减。这就是 AR(1) 均值回归的核心。

## 3. 直觉：带阻尼的记忆

AR(1) 写成

$$y_t=c+\phi y_{t-1}+\varepsilon_t.$$

- (\phi=0)：没有上一期记忆，只剩白噪声和常数；
- (0<\phi<1)：同方向延续，但逐渐衰减；
- (-1<\phi<0)：影响正负交替并衰减；
- (\phi=1)：冲击永久保留，成为随机游走；
- (|\phi|>1)：偏离通常被放大，过程不稳定。

## 4. 从递推到长期均值

若过程平稳，(E(y_t)=E(y_{t-1})=\mu)。对模型取期望：

$$\mu=c+\phi\mu,$$

因此

$$\mu=\frac{c}{1-\phi}.$$

把模型围绕均值重写：

$$y_t-\mu=\phi(y_{t-1}-\mu)+\varepsilon_t.$$

忽略之后的新冲击，当前偏离 (d) 在 (h) 期后变为 (\phi^h d)。当 (|\phi|<1) 时，(\phi^h\to0)，所以过程回到均值。

## 5. ACF 为什么是几何衰减

AR(1) 的理论自相关满足

$$\rho_k=\phi^k.$$

若 (\phi=0.7)，前三阶为 `0.7, 0.49, 0.343`；若 (\phi=-0.7)，则为 `-0.7, 0.49, -0.343`。这不是需要死记的口诀，而是同一个冲击沿递推链传播的结果。

PACF 在一阶后理论上为零，因为控制 (y_{t-1}) 后，更早滞后不再提供额外直接线性信息。

## 6. 手算多步预测

设

$$y_t=2+0.6y_{t-1}+\varepsilon_t,$$

当前 (y_t=8)，未来创新条件期望为零：

$$
\hat y_{t+1|t}=2+0.6\times8=6.8,
$$

$$
\hat y_{t+2|t}=2+0.6\times6.8=6.08.
$$

长期均值是 (2/(1-0.6)=5)，预测会从 8 逐步靠近 5，而不是无限直线外推。

## 7. 最小代码实验

运行前画出预期：

- (\phi=0.8)：缓慢同向变化；
- (\phi=-0.8)：围绕均值交替振荡；
- (\phi=1)：水平漂移且没有固定均值。

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

def simulate_ar1(phi, n=300):
    eps = rng.normal(size=n)
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = phi * y[t-1] + eps[t]
    return y

fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
for ax, phi in zip(axes, [0.8, -0.8, 1.0]):
    ax.plot(simulate_ar1(phi))
    ax.set_title(f"AR(1), phi={phi}")
plt.tight_layout()
plt.show()
```

## 8. 从 AR(1) 扩展到 AR(p)

AR((p)) 为

$$
y_t=c+\phi_1y_{t-1}+\cdots+\phi_py_{t-p}+\varepsilon_t.
$$

此时不能把每个系数单独要求小于 1 就宣布平稳；一般要检查 AR 特征多项式的根。ACF/PACF 只负责提出低阶候选，最终还要检查估计稳定性、残差白噪声和滚动预测。

## 9. 常见错误

- 把高自相关解释成因果或可交易收益；趋势也会制造高自相关。
- 认为 (c) 就是长期均值；均值实际是 (c/(1-\phi))。
- 只看训练拟合，不检查参数是否靠近单位根。
- PACF 有几根越界就无条件选择几阶 AR。

## 10. 当堂练习

1. 对 (y_t=3+0.75y_{t-1}+\varepsilon_t)，计算长期均值。
2. 当前值比均值高 16，忽略新冲击，三期后预期偏离多少？
3. (\phi=-0.5) 时，为什么序列会在均值两侧交替？

> [!answer]- 当堂练习答案
> 1. (3/(1-0.75)=12)。  
> 2. (16\times0.75^3=6.75)。  
> 3. 每次递推都乘一个负数，因此偏离符号交替；绝对值小于 1 又使幅度衰减。

## 11. 过关标准

- [ ] 能说：从冲击传播解释均值回归。
- [ ] 能算：长期均值、三期冲击响应和多步预测。
- [ ] 能做：模拟三种参数并预判图形。
- [ ] 能判断：不把 PACF 截尾当唯一选阶证据。

## 12. 下一课与作业

- 下一课：[[MA模型]]
- 参考卡：[[AR模型]]、[[自相关函数ACF]]
- 正式作业：[[HW03-AR模型与均值回归阶梯作业]]
- 课程入口：[[🧑‍🏫 时间序列教师版学习入口]]

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §9.3 Autoregressive models](https://otexts.com/fpp3/AR.html)。
- 延伸练习：[FPP3 Chapter 9 Exercises](https://otexts.com/fpp3/arima-exercises.html)。
