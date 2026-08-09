---
type: study
topic: "M/M/1排队与Little律"
course: "随机过程"
created: 2026-08-08
updated: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段2-马尔可夫泊松与排队]]"
flow: knowledge
kind: problem-type
difficulty: intermediate
concept: [出生死亡链, 排队稳态, Little律]
prerequisites: [Poisson过程, 连续时间Markov链, 级数]
related: [负载率, 稳态分布, PASTA]
upstream: ["[[随机过程-泊松过程指数等待与更新]]", "[[随机过程-连续时间马尔可夫链与生成元]]"]
source: "MIT 6.262 Chapters 2 and 6; local original queueing task"
source_url: "https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/pages/course-notes/"
accessed: 2026-08-08
license: "CC BY-NC-SA 4.0; 本地任务与解释原创"
tags: [学习, 随机过程, 排队, M-M-1]
---

# 随机过程｜M/M/1 排队与 Little 律

## 1. 它解决什么问题

排队模型把随机到达、服务时间和拥堵结果放在同一系统里。M/M/1 的两个 M 表示 Poisson 到达和指数服务，1 表示一个服务台；它不是“随便一个排队队列”的简称。最重要的边界是：负载率小于 1 才存在常规稳态。

## 2. 模型与状态

令 $N(t)\in\{0,1,2,\ldots\}$ 为系统内人数，包括服务中的顾客。到达率为 $\lambda$，服务率为 $\mu$：

- $n\to n+1$ 的速率恒为 $\lambda$；
- $n\to n-1$ 的速率为 $\mu$（$n\ge1$）；
- 状态 0 没有服务完成跳转。

因此它是出生—死亡 CTMC，负载率

$$
\rho=\frac\lambda\mu.
$$

指数服务的无记忆性使“当前人数”成为足够状态；一般服务分布需要扩充剩余服务时间或放弃 Markov 表示。

## 3. 稳态分布推导

稳态流量平衡为

$$
\pi_0\lambda=\pi_1\mu,
\qquad
\pi_n\lambda=\pi_{n+1}\mu.
$$

所以

$$
\pi_n=\pi_0\rho^n.
$$

若 $\rho<1$，归一化几何级数

$$
1=\sum_{n=0}^{\infty}\pi_n
=\pi_0\sum_{n=0}^{\infty}\rho^n
=\frac{\pi_0}{1-\rho}
$$

给出

$$
\boxed{\pi_n=(1-\rho)\rho^n}.
$$

若 $\rho\ge1$，级数不可归一化，不能报告一个“稳态平均队长”。有限仿真中的暂时平均不改变这个结论。

## 4. 长期指标

系统内平均人数

$$
L=E_\pi[N]=\sum_{n=0}^{\infty}n(1-\rho)\rho^n
=\frac\rho{1-\rho}.
$$

到达前平均排队人数（不含服务中）为

$$
L_q=L-\rho=\frac{\rho^2}{1-\rho}.
$$

有效离开率为 $\lambda$（稳定时），一个到达者在系统内平均逗留时间为

$$
W=\frac L\lambda=\frac1{\mu-\lambda},
$$

排队等待时间为

$$
W_q=\frac{L_q}{\lambda}=\frac{\rho}{\mu-\lambda}.
$$

这里使用 Little 律 $L=\lambda W$；它是流量守恒和时间平均恒等式，不是只适用于 M/M/1 的神奇公式。

## 5. 一个参数例子

若 $\lambda=2$、$\mu=3$，则 $\rho=2/3$，

$$
\pi_0=1/3,\quad
L=2,\quad
W=1\text{ 小时},\quad
L_q=4/3.
$$

若把服务率误写成 2.5，结论会变化；报告必须记录参数、单位和是否包含服务中顾客。

## 6. 模拟协议

事件驱动模拟维护当前时间 $t$、队长 $n$ 和下一次到达/服务完成时间：

1. 到达事件：$n\leftarrow n+1$，重新抽下一次到达时间；
2. 服务完成：$n\leftarrow n-1$，仅在 $n>0$ 时安排服务完成；
3. 使用时间加权平均估计 $L$，不能只平均离散观测点；
4. 预先丢弃 burn-in，记录总时长和随机种子；
5. 同时运行 $\rho<1$ 与 $\rho\ge1$，后者必须触发不稳定诊断而非返回稳态。

代码入口为 `scripts/stochastic_process_lab.py mm1`，测试会检查事件时间单调和不稳定拒绝。

## 7. PASTA 的适用边界

Poisson 到达具有“到达时刻看到的时间平均状态等于任意时刻看到的状态平均”的性质（PASTA）。它依赖 Poisson 到达与非预见系统状态；对按系统状态主动择时的到达过程不能直接套用。

## 8. 常见错误

1. 把 $\rho\ge1$ 的有限样本平均当作稳态。
2. 把 $L$ 与 $L_q$、$W$ 与 $W_q$ 混在一起。
3. 只统计顾客到达时的队长，却声称得到时间平均。
4. 服务台空闲时仍生成服务完成事件。
5. 忽略 burn-in、事件同刻处理顺序和单位。

## 9. 闭卷检索练习

1. 从出生—死亡平衡推导 $\pi_n$。
2. 说明为什么 $\rho\ge1$ 时不能归一化。
3. 用 Little 律从 $L$ 推出 $W$ 与 $W_q$。
4. 写出事件驱动模拟的状态变量与两个失败条件。

**通过标准**：能完整推导稳定条件和四个指标；代码结果必须同时包含稳定和不稳定案例。

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

- [MIT 6.262 Course Notes](https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/pages/course-notes/)，Chapters 2 and 6；访问 2026-08-08。
- `scripts/stochastic_process_lab.py` 为本课程原创实验工具，不代表官方实现。
