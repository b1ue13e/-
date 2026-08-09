---
type: study
topic: "偏自相关函数 PACF"
course: "时间序列分析"
created: 2025-08-11
updated: 2026-08-07
status: ongoing
difficulty: intermediate
flow: knowledge
kind: derivation
aliases: ["PACF（深挖笔记）", "偏自相关函数PACF", "PACF"]
concept: ["偏自相关", "线性投影", "模型识别"]
prerequisites: ["自相关函数", "线性回归", "弱平稳"]
related: ["AR模型", "Yule-Walker方程", "模型识别"]
stage_moc: "[[🧭 阶段2-平稳性与相关结构]]"
upstream: ["[[自相关函数ACF]]"]
sources:
  - title: "Penn State STAT 510"
    url: "https://online.stat.psu.edu/stat510/Lesson02"
    locator: "Lesson 2: autocorrelation and partial autocorrelation"
    source_type: official-course
    license: "link-only；本卡为原创释义。"
    verified_at: 2026-08-07
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/non-seasonal-arima.html"
    locator: "Section 9.2: backshift notation and ARIMA preliminaries"
    source_type: open-textbook
    license: "link-only；本卡不复制教材题目。"
    verified_at: 2026-08-07
tags: [学习, 时间序列分析, PACF, 模型识别]
---

# 偏自相关函数（PACF）

## 它解决什么问题

滞后 $k$ 的 ACF 同时包含直接关联和经由中间滞后传递的间接关联。PACF 回答：

> 在线性控制 $y_{t-1},\ldots,y_{t-k+1}$ 后，$y_{t-k}$ 对 $y_t$ 还提供多少额外线性信息？

因此 PACF 是候选 AR 阶数的证据之一，但不是自动定阶器。

## 正式定义

分别将 $y_t$ 和 $y_{t-k}$ 对中间滞后向量

$$
Z_t=(y_{t-1},\ldots,y_{t-k+1})^\top
$$

做线性投影，得到残差

$$
e_t=y_t-\operatorname{Proj}(y_t\mid Z_t),\qquad
u_{t-k}=y_{t-k}-\operatorname{Proj}(y_{t-k}\mid Z_t).
$$

滞后 $k$ 的偏自相关定义为

$$
\alpha_k=\operatorname{Corr}(e_t,u_{t-k}).
$$

在平稳 $AR(k)$ 线性投影

$$
y_t=\phi_{k1}y_{t-1}+\cdots+\phi_{kk}y_{t-k}+\varepsilon_t
$$

中，最后一个系数 $\phi_{kk}$ 等于 $\alpha_k$。

> [!note] 解释边界
> “直接”指控制中间滞后后的线性投影关系，不等于结构因果或物理直接作用。

## 从 ACF 到 PACF

Yule–Walker 方程给出

$$
\begin{bmatrix}
1 & \rho_1 & \cdots & \rho_{k-1}\\
\rho_1 & 1 & \cdots & \rho_{k-2}\\
\vdots & \vdots & \ddots & \vdots\\
\rho_{k-1} & \rho_{k-2} & \cdots & 1
\end{bmatrix}
\begin{bmatrix}
\phi_{k1}\\
\phi_{k2}\\
\vdots\\
\phi_{kk}
\end{bmatrix}
=
\begin{bmatrix}
\rho_1\\
\rho_2\\
\vdots\\
\rho_k
\end{bmatrix}.
$$

当 $k=1$ 时，

$$
\alpha_1=\phi_{11}=\rho_1.
$$

当 $k=2$ 时，

$$
\alpha_2=\phi_{22}
=\frac{\rho_2-\rho_1^2}{1-\rho_1^2}.
$$

若 $\rho_1=0.8,\rho_2=0.64$，则 $\alpha_2=0$：二阶总相关可完全由一阶关系传递，不需要额外二阶线性项。

## 理论图形与有限样本

- 对因果平稳 $AR(p)$，总体 PACF 在 $p$ 阶后为零。
- 对可逆 $MA(q)$，总体 PACF 通常拖尾。
- 对一般 $ARMA(p,q)$，ACF 和 PACF 通常都拖尾。

样本 PACF 不会精确截尾。参考带只是近似，且同时查看很多滞后会增加偶然越界。正确流程是：

1. 在平稳化口径下计算 ACF/PACF。
2. 用理论形状提出少量候选，不直接宣布模型。
3. 检查参数约束、信息准则和拟合失败。
4. 用残差与滚动样本外误差淘汰候选。

## 最小可运行验证

~~~python
import numpy as np
from statsmodels.tsa.stattools import pacf

rng = np.random.default_rng(7)
n = 800
eps = rng.normal(size=n)
y = np.zeros(n)

for t in range(2, n):
    y[t] = 0.55 * y[t - 1] - 0.25 * y[t - 2] + eps[t]

print(np.round(pacf(y, nlags=8, method="ywm"), 3))
~~~

运行前先预注册预期：lag 1 和 lag 2 可能明显，后续样本 PACF 应围绕零波动，而不是恰好等于零。

## 常见错误

- **PACF 是 ACF 做差**：PACF 来自条件线性关系，不是简单相减。
- **PACF 一定小于 ACF**：没有这种大小关系。
- **数显著柱子就得到 $p$**：样本波动、非平稳、季节性和多重查看都会误导。
- **原序列不平稳也直接定阶**：先固定差分、趋势和季节处理口径。
- **PACF 证明因果**：它只描述受控后的线性关联。

## 闭卷检索

1. 用残差相关写出 PACF 的定义。
2. 从二阶 Yule–Walker 方程推出 $\alpha_2$。
3. 解释为什么 AR(1) 的 ACF 可以多阶非零，而总体 PACF 在一阶后为零。
4. 给出 ACF/PACF 都拖尾时的候选与验证流程。
5. 说明样本 PACF 参考带为什么不能当作唯一裁决线。

**通过标准**：前两题公式正确；后三题必须同时提到“候选生成、有限样本、残差与样本外验证”。

## 相关入口

- 总相关：[[自相关函数ACF]]
- 模型性质：[[AR模型]]
- 计算基础：[[Yule-Walker 方程 (Yule-Walker Equations)]]
- 识别流程：[[L07-模型识别与参数估计]]

## 学完后可以完成

### 下游知识

~~~dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
~~~

### 可完成作业

~~~dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
~~~
