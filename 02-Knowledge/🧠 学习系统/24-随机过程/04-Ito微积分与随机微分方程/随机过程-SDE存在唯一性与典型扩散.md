---
type: study
topic: "SDE存在唯一性与典型扩散"
course: "随机过程"
created: 2026-08-08
updated: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段4-Ito微积分与随机微分方程]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: [随机微分方程, 强解, 扩散过程]
prerequisites: [Ito积分, Ito公式, Lipschitz连续]
related: [Geometric Brownian motion, Ornstein-Uhlenbeck过程, Fokker-Planck方程]
upstream: ["[[随机过程-Ito公式生成元与鞅构造]]"]
source: "MIT 15.070J Lectures 17 and 19; local SDE bridge"
source_url: "https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/"
accessed: 2026-08-08
license: "CC BY-NC-SA 4.0; 本地桥接内容原创"
tags: [学习, 随机过程, SDE, 扩散过程]
---

# 随机过程｜SDE 存在唯一性与典型扩散

## 1. 它解决什么问题

随机微分方程把确定性漂移和随机扰动合并为动态系统。但写下 $dX_t=b(X_t)dt+\sigma(X_t)dW_t$ 不代表解自动存在、唯一或不会爆炸。必须先给出积分定义和系数条件，再讨论模型与模拟。

## 2. 积分形式与强解

一维 SDE 写作

$$
dX_t=b(t,X_t)dt+\sigma(t,X_t)dW_t,
\qquad X_0=\xi.
$$

其含义是对每个 $t$，

$$
X_t=\xi+\int_0^tb(s,X_s)ds
+\int_0^t\sigma(s,X_s)dW_s.
$$

在给定概率空间、Brownian 运动和初值上构造出的适应过程称为强解。路径唯一性表示：若两个解使用同一 $W$ 与初值，则它们不可区分。

弱解允许连概率空间和 Brownian 运动一起构造；“分布唯一”与“路径唯一”不是同一概念。本课程数值实验使用强解口径。

## 3. 标准存在唯一性条件

若对所有 $t$ 和 $x,y$ 存在常数 $L,C$，使

$$
|b(t,x)-b(t,y)|+|\sigma(t,x)-\sigma(t,y)|
\le L|x-y|
$$

（全局 Lipschitz），并且

$$
|b(t,x)|^2+|\sigma(t,x)|^2
\le C(1+|x|^2)
$$

（线性增长），且 $E|\xi|^2<\infty$，则在有限时间区间上存在唯一强解，并有二阶矩控制。

证明采用 Picard 迭代：

$$
X_t^{(n+1)}=\xi+\int_0^tb(s,X_s^{(n)})ds
+\int_0^t\sigma(s,X_s^{(n)})dW_s.
$$

利用 Cauchy-Schwarz、Itô 等距和 Grönwall 不等式证明迭代 Cauchy，并用同样估计证明路径唯一。

这些条件是常用充分条件，不是所有 SDE 可解的必要条件；局部 Lipschitz 还需配合非爆炸控制。

## 4. Geometric Brownian motion

模型

$$
dS_t=\mu S_tdt+\sigma S_tdW_t,
\qquad S_0>0.
$$

对 $\log S_t$ 使用 Itô 公式：

$$
d\log S_t=\left(\mu-\frac12\sigma^2\right)dt+\sigma dW_t.
$$

积分得到

$$
S_t=S_0\exp\left[
\left(\mu-\frac12\sigma^2\right)t+\sigma W_t
\right].
$$

因此 $S_t>0$，

$$
E[S_t]=S_0e^{\mu t}.
$$

解析解为数值方法提供强误差基准，但 GBM 的金融解释还需要风险中性测度等额外结构，本课程不展开。

## 5. Ornstein-Uhlenbeck 过程

模型

$$
dX_t=\kappa(\theta-X_t)dt+\sigma dW_t,
\qquad \kappa>0.
$$

乘积分因子 $e^{\kappa t}$，得到

$$
X_t=\theta+(X_0-\theta)e^{-\kappa t}
+\sigma\int_0^te^{-\kappa(t-s)}dW_s.
$$

因此

$$
E[X_t]=\theta+(X_0-\theta)e^{-\kappa t},
$$

$$
\operatorname{Var}(X_t)=\frac{\sigma^2}{2\kappa}
\left(1-e^{-2\kappa t}\right).
$$

当 $t\to\infty$，分布趋向

$$
N\left(\theta,\frac{\sigma^2}{2\kappa}\right).
$$

OU 既有均值回归，又有显式矩，是检查模拟器的理想基准。

## 6. 生成元与矩方程

一维扩散的生成元

$$
\mathcal Lf=b f'+\frac12\sigma^2f''
$$

给出

$$
\frac d{dt}E[f(X_t)]=E[(\mathcal Lf)(X_t)]
$$

在可交换微分与期望的条件下成立。取 $f(x)=x,x^2$ 可推导均值和二阶矩方程，用于解析—模拟对照。

## 7. 边界与失败模式

- 系数不满足全局 Lipschitz 时仍可能有唯一解，但需要专门定理。
- 超线性漂移可能爆炸，Euler-Maruyama 也可能数值发散。
- 扩散系数在边界退化时，解是否保持非负需要额外分析。
- 参数可解释性不等于统计可识别性；单条短路径未必能可靠估计漂移与扩散。

## 8. 常见错误

1. 把微分记号当成 $dW_t/dt$ 存在。
2. 写 SDE 不写初值、滤过和解的口径。
3. 只检查 Lipschitz，不检查增长或爆炸。
4. 在 GBM 对数解中漏掉 $-\sigma^2/2$。
5. 把 OU 的长期方差写成 $\sigma^2/(2\theta)$；分母是均值回归速率 $\kappa$。

## 9. 闭卷检索练习

1. 写出 SDE 的积分形式和强解定义。
2. 陈述全局 Lipschitz、线性增长与存在唯一性结论。
3. 推导 GBM 解析解和 OU 的均值、方差。
4. 给出一个“写得出方程但需额外非爆炸分析”的失败模式。

**通过标准**：解的口径、系数条件和模型公式都完整；能用解析矩设计数值验收。

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

- [MIT 15.070J Lecture Notes](https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/)，Lectures 17 and 19；访问 2026-08-08。
