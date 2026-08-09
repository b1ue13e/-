---
type: study
topic: "Euler-Maruyama路径模拟与误差"
course: "随机过程"
created: 2026-08-08
updated: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段4-Ito微积分与随机微分方程]]"
flow: knowledge
kind: problem-type
difficulty: advanced
concept: [Euler-Maruyama方法, 强误差, 弱误差]
prerequisites: [随机微分方程, Brownian增量, 数值Euler法]
related: [Monte Carlo, 路径耦合, 数值稳定性]
upstream: ["[[随机过程-SDE存在唯一性与典型扩散]]"]
source: "Higham 2001, An Algorithmic Introduction to Numerical Simulation of SDEs"
source_url: "https://doi.org/10.1137/S0036144500378302"
accessed: 2026-08-08
license: "© SIAM; link-only；本地推导、代码和任务原创"
tags: [学习, 随机过程, Euler-Maruyama, 数值SDE]
---

# 随机过程｜Euler-Maruyama 路径模拟与误差

## 1. 它解决什么问题

大多数 SDE 没有可直接采样的解析解。Euler-Maruyama（EM）把漂移按 $\Delta t$、扩散按 Brownian 增量离散化，是最小可复现基线。正确实验不仅要生成路径，还要区分路径级强误差、分布/期望级弱误差和数值稳定性。

## 2. 离散格式

对

$$
dX_t=b(t,X_t)dt+\sigma(t,X_t)dW_t,
$$

取网格 $t_n=n\Delta t$，Brownian 增量

$$
\Delta W_n=W_{t_{n+1}}-W_{t_n}
\sim N(0,\Delta t)
$$

且相互独立。EM 更新为

$$
X_{n+1}^{h}=X_n^h
+b(t_n,X_n^h)\Delta t
+\sigma(t_n,X_n^h)\Delta W_n.
$$

扩散项量级是 $\sqrt{\Delta t}$，不能误写成 $\sigma Z\Delta t$。

## 3. 强误差与弱误差

### 强误差

强误差比较同一 Brownian 驱动下的路径，例如

$$
E|X_T-X_T^h|.
$$

在标准全局 Lipschitz 条件下，EM 通常有强阶 $1/2$：

$$
E|X_T-X_T^h|=O(h^{1/2}).
$$

为了估计强误差，不同步长必须使用**耦合增量**：粗网格增量等于对应细网格增量之和。

### 弱误差

弱误差比较测试函数期望：

$$
|E[\varphi(X_T)]-E[\varphi(X_T^h)]|.
$$

在更强光滑条件下，EM 对合适 $\varphi$ 通常有弱阶 1。弱误差实验不要求逐路径对齐，但仍要控制 Monte Carlo 标准误。

## 4. OU 模型上的最小实验

对

$$
dX_t=\kappa(\theta-X_t)dt+\sigma dW_t,
$$

EM 为

$$
X_{n+1}=X_n+\kappa(\theta-X_n)h
+\sigma\sqrt h Z_n,
\qquad Z_n\sim N(0,1).
$$

解析检查量为

$$
m(T)=\theta+(X_0-\theta)e^{-\kappa T},
$$

$$
v(T)=\frac{\sigma^2}{2\kappa}(1-e^{-2\kappa T}).
$$

对多个步长 $h$，报告终点经验均值/方差与解析值差异，同时报告 Monte Carlo 标准误。步长偏差和抽样误差必须分开。

## 5. 耦合增量

若细步长为 $h/2$，生成

$$
\Delta W_{2k}^{f},\ \Delta W_{2k+1}^{f}
\sim N(0,h/2).
$$

粗步长使用

$$
\Delta W_k^c
=\Delta W_{2k}^{f}+\Delta W_{2k+1}^{f}.
$$

这样粗细解共享同一 Brownian 路径，$|X_T^{f}-X_T^c|$ 才近似离散误差。若分别使用独立随机数，差异会被路径随机性主导，无法估计强阶。

## 6. 数值稳定性

对确定性部分 $dX_t=-\kappa X_tdt+\sigma dW_t$，EM 更新系数为 $1-\kappa h$。若 $h$ 过大，绝对值可能大于 1，数值路径会表现出非物理振荡或爆炸，即使真实 OU 过程均值回归。

因此“代码能运行”不是通过标准；必须做步长敏感性和已知矩检查。

## 7. 最小 Python 伪代码

```python
import math
import random

rng = random.Random(42)
x = x0
for _ in range(steps):
    d_w = math.sqrt(dt) * rng.gauss(0.0, 1.0)
    x += kappa * (theta - x) * dt + sigma * d_w
```

课程的可运行实现位于 `03-Projects/24-随机过程/scripts/stochastic_process_lab.py`。学习者不能只提交生成路径的代码，还要提交理论矩、误差表和失败步长。

## 8. 实验设计清单

1. 固定模型参数、$T$、步长序列、路径数和随机种子。
2. 先用解析矩或解析解建立基线。
3. 强误差使用耦合增量；弱误差报告标准误。
4. 至少加入一个过大步长失败案例。
5. 不删除数值爆炸、溢出或异常路径；解释它们来自模型还是算法。
6. 报告计算预算，避免只挑最漂亮的一次随机结果。

## 9. 常见错误

1. 把 $\Delta W$ 写成 $N(0,h^2)$；正确方差是 $h$。
2. 用独立路径比较粗细步长并称为强误差。
3. 只报样本均值，不报 Monte Carlo 标准误。
4. 把弱阶 1 解释为每条路径误差 $O(h)$。
5. 只测试一个步长，无法区分离散偏差与随机波动。

## 10. 闭卷检索练习

1. 写出 EM 更新并解释漂移、扩散的不同量级。
2. 定义强误差和弱误差，说明各自的耦合要求。
3. 为 OU 设计均值、方差和稳定性三项检查。
4. 解释为什么粗增量必须等于两个细增量之和。

**通过标准**：能独立设计至少三个步长的实验；结果同时包含估计、误差、标准误和失败案例。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

## 来源

- [Higham 2001](https://doi.org/10.1137/S0036144500378302)，SIAM Review 43(3), 525–546；link-only，访问 2026-08-08。
- 本地实现、测试和作业规格为课程原创，不复制论文代码或题面。
