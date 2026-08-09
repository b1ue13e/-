---
type: study
topic: "Ito积分与Ito等距"
course: "随机过程"
created: 2026-08-08
updated: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段4-Ito微积分与随机微分方程]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: [Ito积分, 简单适应过程, Ito等距]
prerequisites: [Brownian运动, L2空间, 适应过程]
related: [随机积分, 鞅, 二次变差]
upstream: ["[[随机过程-布朗运动反射原理与二次变差]]", "[[随机过程-鞅停时与可选停止]]", "[[随机过程-L2空间与收敛模式]]"]
source: "MIT 15.070J Advanced Stochastic Processes, Lectures 14–16"
source_url: "https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/"
accessed: 2026-08-08
license: "CC BY-NC-SA 4.0; 本地改写并归因"
tags: [学习, 随机过程, Ito积分, Ito等距]
---

# 随机过程｜Itô 积分与 Itô 等距

## 1. 为什么不能直接用普通积分

Brownian 路径几乎处处无限总变差且不可微，$\int H_t\,dW_t$ 不能一般按 Riemann-Stieltjes 积分定义。Itô 的办法是先对“每段开始时已经知道的”简单过程定义随机和，再用 $L^2$ 等距把定义延拓到平方可积适应过程。

## 2. 简单适应过程

在分割

$$
0=t_0<t_1<\cdots<t_n=T
$$

上，令

$$
H_t=\sum_{k=0}^{n-1}\xi_k\mathbf 1_{(t_k,t_{k+1}]}(t),
$$

其中 $\xi_k$ 是 $\mathcal F_{t_k}$-可测且平方可积。定义

$$
\int_0^T H_t\,dW_t
:=\sum_{k=0}^{n-1}\xi_k(W_{t_{k+1}}-W_{t_k}).
$$

$\xi_k$ 只能使用区间开始时的信息。若改用 $W_{t_{k+1}}$ 等未来量，得到的极限可能是其他积分或产生额外漂移。

## 3. 均值为零

由于 $\xi_k$ 对 $\mathcal F_{t_k}$ 可测，而增量 $\Delta W_k$ 与 $\mathcal F_{t_k}$ 独立且均值为 0，

$$
E[\xi_k\Delta W_k]
=E[\xi_kE(\Delta W_k\mid\mathcal F_{t_k})]=0.
$$

所以

$$
E\left[\int_0^T H_t\,dW_t\right]=0.
$$

更一般地，积分过程 $M_t=\int_0^tH_s\,dW_s$ 在平方可积条件下是鞅。

## 4. Itô 等距

展开平方：

$$
E\left[\left(\sum_k\xi_k\Delta W_k\right)^2\right].
$$

交叉项因增量正交和适应性消失，对角项满足

$$
E[\xi_k^2(\Delta W_k)^2]
=E[\xi_k^2]\Delta t_k.
$$

因此

$$
\boxed{
E\left[\left(\int_0^T H_t\,dW_t\right)^2\right]
=E\left[\int_0^T H_t^2\,dt\right]
}.
$$

这就是 Itô 等距。它表明从被积过程到随机积分是一个 $L^2$ 等距映射。

## 5. 用完备性延拓

对平方可积适应过程 $H$，满足

$$
E\int_0^T H_t^2dt<\infty,
$$

取简单适应过程 $H^{(n)}$ 使

$$
E\int_0^T|H_t^{(n)}-H_t|^2dt\to0.
$$

由 Itô 等距，积分序列在 $L^2(\Omega)$ 中 Cauchy：

$$
E\left|\int H^{(n)}dW-\int H^{(m)}dW\right|^2
=E\int|H^{(n)}-H^{(m)}|^2dt.
$$

$L^2$ 完备性保证极限存在，并定义 $\int H\,dW$。等距还保证定义不依赖所选逼近序列。

## 6. 确定被积函数例子

令 $H_t=t$，则

$$
E\left[\int_0^T t\,dW_t\right]=0,
$$

且

$$
\operatorname{Var}\left(\int_0^T t\,dW_t\right)
=\int_0^Tt^2dt=\frac{T^3}{3}.
$$

因为被积函数确定且积分是 Gaussian 增量的线性极限，所以

$$
\int_0^Tt\,dW_t\sim N\left(0,\frac{T^3}{3}\right).
$$

## 7. 随机被积函数例子

取 $H_t=W_t$。Itô 公式稍后将给出

$$
\int_0^T W_t\,dW_t=\frac12(W_T^2-T).
$$

右侧不是普通微积分猜测的 $W_T^2/2$，额外的 $-T/2$ 来自 Brownian 二次变差。用等距检查二阶矩：

$$
E\left[\left(\int_0^TW_t\,dW_t\right)^2\right]
=\int_0^TE[W_t^2]dt
=\frac{T^2}{2}.
$$

## 8. 常见错误

1. 用右端点或未来信息构造被积过程，却仍称为 Itô 积分。
2. 把随机积分当普通路径积分逐点计算。
3. 忘记平方可积条件，或只检查每个固定 $t$ 的二阶矩。
4. 把 Itô 等距误写成逐样本路径等式；它是期望层等式。
5. 从“均值为零”推出积分几乎处处为零。

## 9. 闭卷检索练习

1. 写出简单适应过程和对应 Itô 和式。
2. 逐步说明交叉项为什么消失，推导 Itô 等距。
3. 解释 $L^2$ 完备性如何产生一般积分。
4. 计算 $\int_0^Tt\,dW_t$ 的均值和方差。

**通过标准**：能写清适应性、平方可积和极限三层条件；不把等距当路径等式。

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

- [MIT 15.070J Lecture Notes](https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/)，Lectures 14–16；访问 2026-08-08。
