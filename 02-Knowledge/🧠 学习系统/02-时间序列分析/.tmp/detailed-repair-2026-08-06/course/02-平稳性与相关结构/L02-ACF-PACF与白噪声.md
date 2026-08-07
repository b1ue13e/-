---
type: study
course: "时间序列分析"
lesson: 2
topic: "ACF、PACF与白噪声"
created: 2026-08-02
updated: 2026-08-05
status: planned
mastery: 0
difficulty: intermediate
flow: knowledge
kind: concept
concept: ["自相关函数", "偏自相关函数", "白噪声"]
prerequisites: ["平稳性与差分", "协方差", "相关系数"]
related: ["L01-平稳性与差分", "L03-AR模型与均值回归", "L04-MA模型与有限冲击"]
anki_deck: "时间序列分析::主线课程"
anki_tags: ["时间序列分析", "L02", "ACF", "PACF", "白噪声"]
tags: [学习, 时间序列, 教师式课程, ACF, PACF]
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/acf.html"
    locator: "Section 2.8: Autocorrelation"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/wn.html"
    locator: "Section 2.9: White noise"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
stage_moc: "[[🧭 阶段2-平稳性与相关结构]]"
upstream: ["[[随机游走（深挖笔记）]]"]
---
# L02｜ACF、PACF 与白噪声

> **预计用时**：70 分钟　**当前掌握**：0 / 1 / 2 / 3

## 0. 这节课解决什么问题

两条序列可能有相同均值和方差，却有完全不同的时间结构：一条今天上涨后明天仍倾向上涨，另一条每期都像重新掷骰子。仅看直方图分不出来，我们需要衡量“相隔 (k) 期的值是否一起变化”。

ACF 用来描述总的滞后相关；PACF 尝试剔除中间滞后的间接影响；白噪声则是“线性结构已经用尽”的基准。

## 1. 学习目标

学完后，不看笔记能够：

- 解释滞后 (k) 的自相关在比较什么；
- 手算一个短序列的一阶样本 ACF；
- 用“直接关系与间接关系”区分 ACF 和 PACF；
- 判断 ACF 图中的单根越界是否足以否定白噪声；
- 用代码比较白噪声、AR(1) 和 MA(1) 的相关图形。

## 2. 课前诊断

> [!question] 先判断
> 若某序列的一阶自相关为 0，能否断言相邻两期独立？

> [!answer]- 诊断答案
> 不能。相关系数只检测线性关系。例如令 $Y_t=X_t^2$，即使某些情况下 $X_t$ 与 $Y_t$ 相关为零，二者仍有确定关系。ACF 接近零只表示没有检测到对应滞后的线性相关。

## 3. 直觉：把序列与自己的“延迟副本”对齐

对序列 `10, 12, 15, 14, 18`，滞后 1 时比较：

| 当前值 | 12 | 15 | 14 | 18 |
|---|---:|---:|---:|---:|
| 前一期 | 10 | 12 | 15 | 14 |

滞后 2 时比较：

| 当前值 | 15 | 14 | 18 |
|---|---:|---:|---:|
| 前两期 | 10 | 12 | 15 |

ACF 就是在每个滞后上计算这种线性共同变化。它不是把时间当普通特征，而是在问序列记忆能持续多远。

## 4. 从手算到样本 ACF

取序列 `1, 2, 3, 4`，均值为 2.5，离差为 `-1.5, -0.5, 0.5, 1.5`。

滞后 1 的分子为

$$
(-0.5)(-1.5)+(0.5)(-0.5)+(1.5)(0.5)=1.25.
$$

分母为

$$(-1.5)^2+(-0.5)^2+(0.5)^2+(1.5)^2=5.$$

因此采用 FPP3 定义时 $r_1=1.25/5=0.25$。一般形式为

$$
r_k=\frac{\sum_{t=k+1}^{T}(y_t-\bar y)(y_{t-k}-\bar y)}
{\sum_{t=1}^{T}(y_t-\bar y)^2}.
$$

样本非常短，所以 `0.25` 不能被过度解释。手算的目的只是理解“对齐—去均值—乘积—标准化”。

## 5. PACF：排除中间人的间接作用

若 $Y_t$ 依赖 $Y_{t-1}$，而 $Y_{t-1}$ 又依赖 $Y_{t-2}$，那么 $Y_t$ 与 $Y_{t-2}$ 会相关，即使 $Y_{t-2}$ 没有额外直接贡献。

二阶 PACF 的问题是：**已经知道 $Y_{t-1}$ 后，$Y_{t-2}$ 还能为 $Y_t$ 增加多少线性信息？**

因此：

- ACF：直接和间接关系都包含；
- PACF：控制中间滞后后的新增关系。

这也是 AR 模型常用 PACF 生成候选阶数的原因，但有限样本中不能机械地按柱子数定阶。

## 6. 白噪声与显著性边界

白噪声要求均值为零、方差恒定、不同期之间不相关。样本 ACF 不会恰好全为零。常见的单滞后近似参考带是

$$\pm\frac{1.96}{\sqrt T}.$$

若同时观察 20 个滞后，即使真实序列是白噪声，也可能偶然有一根柱越界。因此：

1. 单根越界只是警报，不是最终判决；
2. 应观察是否出现成片、衰减或季节模式；
3. 再使用 Ljung–Box 等联合检验；
4. 检验通过也不等于统计独立或不存在非线性结构。

## 7. 最小代码实验

运行前先预测：

- 白噪声 ACF 大多在参考带内；
- AR(1) ACF 逐步衰减；
- MA(1) ACF 主要在一阶突出。

```python
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

rng = np.random.default_rng(7)
n = 500
eps = rng.normal(size=n)

ar = np.zeros(n)
for t in range(1, n):
    ar[t] = 0.75 * ar[t-1] + eps[t]

ma = eps.copy()
ma[1:] += 0.75 * eps[:-1]

fig, axes = plt.subplots(3, 2, figsize=(10, 9))
for row, (name, series) in enumerate([
    ("White noise", eps), ("AR(1)", ar), ("MA(1)", ma)
]):
    plot_acf(series, lags=20, ax=axes[row, 0], title=f"{name} ACF")
    plot_pacf(series, lags=20, ax=axes[row, 1], title=f"{name} PACF")
plt.tight_layout()
plt.show()
```

## 8. 常见错误

- 在带趋势的原序列上直接用 ACF 定 AR 阶数；趋势会产生缓慢衰减的伪相关。
- 把相关解释为因果。
- 把 ACF/PACF 图当成唯一选阶器，忽略残差和样本外预测。
- 认为白噪声等于正态分布；正态性不是白噪声定义的必要条件。

## 9. 当堂练习

1. 用自己的话说明滞后 3 的 ACF 在比较什么。
2. 为什么 AR(1) 即使只直接依赖上一期，也可能在 ACF 中出现很多非零滞后？
3. 一张 ACF 图有 20 根柱，只有第 17 阶略微越界。你会立即否定白噪声吗？

> [!answer]- 当堂练习答案
> 1. 比较当前值与前三期值之间的线性共同变化。  
> 2. 上一期依赖上上期，影响会沿时间链间接传播。  
> 3. 不会。需要结合整体图形、预先选择的滞后范围和联合检验；单根偶然越界可能来自多重查看。

## 10. 过关标准

- [ ] 能说：不用公式解释 ACF 与 PACF 的区别。
- [ ] 能算：手算一个短序列的一阶 ACF。
- [ ] 能做：模拟三类序列并提前预测图形。
- [ ] 能判断：不会凭单根柱或口诀宣布模型阶数。

## 11. 下一课与作业

- 下一课：[[L03-AR模型与均值回归]]
- 参考卡：[[自相关函数ACF]]、[[PACF（深挖笔记）]]、[[白噪声]]
- 正式作业：[[时间序列分析-课后作业-02-ACF-PACF与白噪声]]
- 课程入口：[[🗺️ 时间序列分析学习路径]]

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §2.8 Autocorrelation](https://otexts.com/fpp3/acf.html)。
- Hyndman & Athanasopoulos, [FPP3 §2.9 White noise](https://otexts.com/fpp3/wn.html)。

## 🃏 Anki 卡片

- ACF 与 PACF 分别回答什么？::ACF 衡量相隔 k 期的总线性相关；PACF 控制中间滞后后衡量 lag k 的额外直接线性关系
- ACF 为零为什么不等于独立？::零自相关只排除线性关系；除高斯等附加条件外，仍可能存在非线性依赖
- 白噪声通过 Ljung-Box 检验是否证明模型正确？::不能；大 p 值只是未发现所检验滞后内的线性自相关，还需检查方差、分布、样本外预测和信息边界

## 派生视图

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

