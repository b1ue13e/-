---
type: study
course: "时间序列分析"
lesson: 4
topic: "MA模型与有限冲击"
created: 2026-08-02
updated: 2026-08-05
status: planned
mastery: 0
difficulty: intermediate
flow: knowledge
kind: concept
concept: ["移动平均模型", "有限冲击", "可逆性"]
prerequisites: ["ACF、PACF与白噪声", "创新与预测误差"]
related: ["L03-AR模型与均值回归", "L05-ARMA与ARIMA建模闭环", "MA模型"]
next: ["L05-ARMA与ARIMA建模闭环"]
anki_deck: "时间序列分析::主线课程"
anki_tags: ["时间序列分析", "L04", "MA模型", "可逆性"]
tags: [学习, 时间序列, 教师式课程, MA模型]
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/MA.html"
    locator: "Section 9.4: Moving average models"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
---

# L04｜MA 模型与有限冲击

> **预计用时**：70 分钟　**当前掌握**：0 / 1 / 2 / 3

## 0. 这节课解决什么问题

某些事件只影响很短时间。例如一次物流延误影响今天和明天，却不会像 AR 模型那样通过序列水平持续传递。MA 模型直接描述“当前值由最近几次意外冲击共同构成”。

注意：这里的 MA 是 moving average **model**，不是用于平滑曲线的滑动平均。

## 1. 学习目标

学完后，不看笔记能够：

- 区分创新、残差和普通观测值；
- 追踪一次冲击在 MA(1)、MA(2) 中持续几期；
- 推导 MA(1) 的方差和一阶 ACF；
- 解释可逆性为什么用于保证唯一表示；
- 从 ACF/PACF 提出 MA 候选并使用其他证据验收。

## 2. 课前诊断

> [!question] 先判断
> `rolling(3).mean()` 与 MA(2) 模型都使用三个数，它们是同一件事吗？

> [!answer]- 诊断答案
> 不是。滑动平均平滑对三个已观测值求平均，用来减少历史曲线噪声；MA(2) 使用当前及过去两个不可直接观测的创新来生成随机过程，用来描述和预测序列动态。其系数也不要求相等或和为 1。

## 3. 直觉：冲击只留下有限长度的脚印

MA(2) 为

$$
y_t=c+\varepsilon_t+\theta_1\varepsilon_{t-1}
+\theta_2\varepsilon_{t-2}.
$$

假设只有时点 5 出现大小为 10 的冲击，其他创新为零：

| 时点 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|
| 冲击贡献 | $10$ | $10\theta_1$ | $10\theta_2$ | $0$ |

冲击在两期之后完全消失。这叫有限冲击响应。

## 4. 手算 MA(1)

设

$$y_t=\varepsilon_t+0.5\varepsilon_{t-1},$$

创新依次为 `2, -1, 3, 0`，并令更早创新为零：

| 时点 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| ε | 2 | -1 | 3 | 0 |
| y | 2 | 0 | 2.5 | 1.5 |

例如 $y_3=3+0.5\times(-1)=2.5$。这里无法把普通观测 $y_{t-1}$ 直接当作创新；实际拟合时，创新和参数需要联合恢复。

## 5. 方差与 ACF 推导

对 MA(1)：

$$y_t=\varepsilon_t+\theta\varepsilon_{t-1},
\qquad \operatorname{Var}(\varepsilon_t)=\sigma^2.$$

因为不同时点创新不相关：

$$\operatorname{Var}(y_t)=(1+\theta^2)\sigma^2.$$

相邻两期只有共同的 ε 项产生协方差：

$$\operatorname{Cov}(y_t,y_{t-1})=\theta\sigma^2,$$

所以

$$\rho_1=\frac{\theta}{1+\theta^2},\qquad \rho_k=0\ (k>1).$$

因此理论 MA(1) 的 ACF 在一阶后截尾，而 PACF 通常逐渐衰减。

## 6. 可逆性：为什么参数需要限制

MA(1) 中 $\theta$ 与 $1/\theta$ 会给出相同的一阶自相关。例如 0.5 与 2 都得到 0.4。如果不加限制，同一个相关结构可能对应多个参数表示。

通常要求 MA 特征多项式的根位于单位圆外；MA(1) 对应 $|\theta|<1$。这样创新可以由当前和过去观测的收敛组合表示，模型表示唯一且计算稳定。

## 7. 最小代码实验

运行前预测：增大 θ 会改变一阶 ACF，但二阶以后仍应接近零。

```python
import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
series = ArmaProcess(ma=[1, 0.7]).generate_sample(
    nsample=800, distrvs=rng.normal
)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
plot_acf(series, lags=20, ax=axes[0])
plot_pacf(series, lags=20, ax=axes[1])
plt.tight_layout()
plt.show()
```

## 8. 常见错误

- 把模型中的创新当成已知特征直接回归。
- 把 ACF 一根突出视为 MA(1) 的最终证明。
- 忽略可逆性，得到等价但不唯一或不稳定的参数。
- 用高阶 MA 勉强表示长记忆，而不比较更简洁的 AR/ARMA。

## 9. 当堂练习

1. MA(2) 中一次冲击最多影响几个 $y$？
2. 若 θ=1，MA(1) 的一阶 ACF 是多少？它满足常用可逆限制吗？
3. 为什么 MA(1) 的二阶 ACF 为零，但 $y_t$ 与 $y_{t-2}$ 不一定统计独立？

> [!answer]- 当堂练习答案
> 1. 当前期及后续两期，共三个观测。  
> 2. $1/(1+1)=0.5$，但 $|\theta|=1$ 位于可逆边界，不满足严格限制。  
> 3. ACF 为零只排除线性相关；若创新非高斯或存在其他结构，零相关不自动推出独立。

## 10. 过关标准

- [ ] 能说：区分 MA 模型与移动平均平滑。
- [ ] 能算：由创新手算 MA(1)，推导方差和 ACF。
- [ ] 能做：模拟 MA(1) 并提前预测相关图形。
- [ ] 能判断：解释可逆性，而不是只背 $|\theta|<1$。

## 11. 下一课与作业

- 下一课：[[L05-ARMA与ARIMA建模闭环]]
- 参考卡：[[MA模型]]、[[ARMA模型]]
- 正式作业：[[HW04-MA模型与有限冲击阶梯作业]]
- 课程入口：[[📚 时间序列课程学习面板]]

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §9.4 Moving average models](https://otexts.com/fpp3/MA.html)。

## 🃏 Anki 卡片

- MA(q) 的一次创新最多直接影响多少个观测？::当前期及后续 q 期，共 q+1 个观测
- MA 模型与移动平均平滑的区别？::MA 模型用当前与过去创新生成随机过程；移动平均平滑对已观测值取窗口平均
- MA(1) 为什么常要求 $|\theta|<1$？::保证可逆，使创新能由当前和过去观测的收敛组合表示，并选择唯一稳定的参数表示
