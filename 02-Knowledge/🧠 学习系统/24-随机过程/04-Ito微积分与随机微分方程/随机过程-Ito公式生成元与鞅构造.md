---
type: study
topic: "Ito公式、生成元与鞅构造"
course: "随机过程"
created: 2026-08-08
updated: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段4-Ito微积分与随机微分方程]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: [Ito公式, 生成元, 鞅构造]
prerequisites: [Ito积分, 二次变差, 二阶Taylor展开]
related: [Feynman-Kac, 扩散过程, Black-Scholes]
upstream: ["[[随机过程-Ito积分与Ito等距]]"]
source: "MIT 15.070J Advanced Stochastic Processes, Lectures 14 and 17"
source_url: "https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/"
accessed: 2026-08-08
license: "CC BY-NC-SA 4.0; 本地改写并归因"
tags: [学习, 随机过程, Ito公式, 生成元]
---

# 随机过程｜Itô 公式、生成元与鞅构造

## 1. 为什么普通链式法则失效

对确定性可微路径，二阶 Taylor 项是高阶小量；Brownian 增量的平方却与 $dt$ 同阶，因为 $[W]_t=t$。Itô 公式正是把这个二阶累积项保留下来的随机链式法则。

## 2. 一维 Itô 公式

设过程满足

$$
dX_t=b(t,X_t)dt+\sigma(t,X_t)dW_t,
$$

且 $f\in C^{1,2}$。则

$$
df(t,X_t)
=\left(
f_t+b f_x+\frac12\sigma^2 f_{xx}
\right)dt
+\sigma f_x\,dW_t.
$$

积分形式为

$$
f(t,X_t)=f(0,X_0)
+\int_0^t\left(f_s+b f_x+\frac12\sigma^2f_{xx}\right)ds
+\int_0^t\sigma f_x\,dW_s.
$$

所有导数都在 $(s,X_s)$ 处取值。额外的 $\tfrac12\sigma^2 f_{xx}$ 是与二次变差对应的修正。

## 3. 生成元

对只依赖状态的 $f(x)$，扩散过程生成元为

$$
(\mathcal Lf)(x)=b(x)f'(x)+\frac12\sigma(x)^2f''(x).
$$

Itô 公式可写为

$$
df(X_t)=(\mathcal Lf)(X_t)dt+\sigma(X_t)f'(X_t)dW_t.
$$

生成元描述短时间平均变化：

$$
(\mathcal Lf)(x)=\lim_{h\downarrow0}
\frac{E_x[f(X_h)]-f(x)}h.
$$

## 4. 鞅构造

若 $u(t,x)$ 足够光滑，令

$$
M_t=u(t,X_t)-u(0,X_0)
-\int_0^t(\partial_s+\mathcal L)u(s,X_s)ds.
$$

由 Itô 公式，$M_t$ 只剩 Itô 积分项，因此在可积条件下是鞅。

若满足偏微分方程

$$
(\partial_t+\mathcal L)u=0,
$$

则 $u(t,X_t)$ 本身是鞅。这是扩散过程与 PDE/Feynman-Kac 连接的入口。

## 5. 三个必须会算的例子

### $f(x)=x^2$ 与 Brownian

令 $X_t=W_t$，$b=0,\sigma=1$，$f_x=2x,f_{xx}=2$，得到

$$
d(W_t^2)=2W_t\,dW_t+dt.
$$

因此 $W_t^2-t$ 是鞅，和阶段 3 的补偿平方例子一致。

### Geometric Brownian motion

若 $dS_t=\mu S_tdt+\sigma S_tdW_t$，取 $f(x)=\log x$：

$$
d\log S_t
=\left(\mu-\frac12\sigma^2\right)dt+\sigma dW_t.
$$

少掉 $-\sigma^2/2$ 会导致对数收益均值错误。

### OU 过程

若 $dX_t=\kappa(\theta-X_t)dt+\sigma dW_t$，取 $f(x)=x$ 可得均值方程

$$
\frac d{dt}E[X_t]=\kappa(\theta-E[X_t]).
$$

因此

$$
E[X_t]=\theta+(X_0-\theta)e^{-\kappa t}.
$$

Itô 公式把随机方程转成可检查的矩方程。

## 6. 二维版本的记号

对 $X_t\in\mathbb R^d$、扩散矩阵 $a=\sigma\sigma^\top$，生成元为

$$
(\mathcal Lf)(x)=b(x)^\top\nabla f(x)
+\frac12\operatorname{tr}\left(a(x)\nabla^2f(x)\right).
$$

二阶项是 Hessian 与协方差矩阵的收缩，不是简单把一维 $\sigma^2$ 换成矩阵后省略迹号。

## 7. 证明主线

1. 对 $f(t+\Delta t,X_t+\Delta X_t)$ 作二阶 Taylor 展开。
2. 代入 $\Delta X=b\Delta t+\sigma\Delta W$。
3. 使用 $(\Delta W)^2$ 的累积极限为 $\Delta t$，舍弃 $\Delta t\Delta W$ 和 $(\Delta t)^2$ 的高阶贡献。
4. 对分割求和并取概率/均方极限，得到积分形式。

关键转念是：随机项的一阶量级为 $\sqrt{dt}$，其平方不能按普通高阶项丢掉。

## 8. 常见错误

1. 忘记时间偏导 $f_t$。
2. 忘记二阶项的 $1/2$ 或把 $\sigma$ 写成 $\sigma^2$ 的错误次方。
3. 把生成元当作转移矩阵，忽略它作用在函数上。
4. 看到 Itô 积分均值为零，就忽略状态过程中的漂移项。
5. 多维情形漏掉协方差矩阵的交叉项。

## 9. 闭卷检索练习

1. 完整写出一维 Itô 公式及每项条件。
2. 从公式推导 $W_t^2-t$ 是鞅。
3. 推导 GBM 的对数过程，并解释 $-\sigma^2/2$ 来源。
4. 写出扩散生成元的多维形式。

**通过标准**：三类例子至少两类能闭卷完成；每次都能指出二次变差贡献。

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

- [MIT 15.070J Lecture Notes](https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/)，Lectures 14 and 17；访问 2026-08-08。
