---
title: "实变函数-Lebesgue积分与可积函数"
topic: "实变函数-Lebesgue积分与可积函数"
date: "2026-08-03"
updated: 2026-08-09
type: study
course: "实变函数"
importance: "A"
tags: [学习, 实变函数]
stage_moc: "[[🧭 阶段2-Lebesgue理论]]"
flow: knowledge
kind: concept
upstream: ["[[实变函数-简单函数]]", "[[实变函数-三大收敛定理]]"]
status: completed
learn_status: not_started
difficulty: advanced
concept: ["Lebesgue 积分", "可积函数", "绝对连续积分"]
prerequisites: ["可测函数", "简单函数", "单调收敛定理"]
related: ["[[实变函数-三大收敛定理]]", "[[实变函数-Lp空间与不等式]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.2"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
created: 2026-08-03
---

# 实变函数-Lebesgue积分与可积函数

## 为什么学

Riemann 积分在"几乎连续"的函数上工作良好,但对 $\mathbf 1_{\mathbb Q}$、振荡剧烈的函数或无界域上的极限无能为力。Lebesgue 积分改为"按函数值切片",因而能积分更多函数、并与极限自由交换(三大收敛定理)。本卡给出定义、基本性质,并点明"可积"的精确含义。

## 核心定义

- 对非负可测 $f$,$\int_E f=\sup\{\int_E\varphi:0\le\varphi\le f,\ \varphi\text{ 简单}\}$。
- 一般可测 $f=f^+-f^-$,定义 $\int_E f=\int_E f^+-\int_E f^-$,当两边不都 $=+\infty$ 时成立。
- **可积**:$\int |f|<\infty$(即 $f\in L^1(E)$)。可积必积分存在且绝对收敛。
- 当且仅当 $f$ 可积时,$\int_E f$ 有限且 $\int_E f=\int_{E\cap\{f\ge0\}}f-\int_{E\cap\{f<0\}}|f|$。

## 证明主线(逐步展开)

### 1. 线性与单调性

对可积函数,线性由简单函数层传递:取 $f_n,g_n$ 为简单函数逼近,则 $\int(\alpha f+\beta g)=\lim\int(\alpha f_n+\beta g_n)=\alpha\int f+\beta\int g$。单调性 $f\le g\Rightarrow\int f\le\int g$ 同理。

### 2. 与 Riemann 积分的关系

若 $f$ 在 $[a,b]$ 上 Riemann 可积,则它几乎处处连续( Lebesgue 定理),故 Lebesgue 可测且两积分相等。反之 Lebesgue 可积不蕴含 Riemann 可积(如 $\mathbf 1_{\mathbb Q}$ 的 Lebesgue 积分为 0,但 Riemann 不可积)。

### 3. 积分的绝对连续性(关键性质)

若 $f\in L^1$,则对任意 $\varepsilon>0$,存在 $\delta>0$ 使任意可测 $A$ 满足 $\mu(A)<\delta$ 时 $\int_A|f|<\varepsilon$。
**证明**:取截断 $f_N=|f|\chi_{\{|f|\le N\}}$,则 $\int|f-f_N|\to0$。对 $\mu(A)<\delta$,$\int_A|f|\le\int_A f_N+N\mu(A)\le\int|f-f_N|+N\delta$,先取 $N$ 使第一项 $<\varepsilon/2$,再取 $\delta=\varepsilon/(2N)$。

### 4. 可积性的判别

- 有界可测函数在有限测度集上必可积($\int_E|f|\le M\mu(E)<\infty$)。
- 无界情形看尾巴衰减:如 $\int_1^\infty x^{-p}$ 当且仅当 $p>1$ 可积。

## 最小例子

- $\int_{[0,1]}\mathbf 1_{\mathbb Q}=0$:因 $\mathbf 1_{\mathbb Q}=0$ a.e.,而"积分只认 a.e."(若两函数 a.e. 相等则积分相等)。
- $f(x)=1/\sqrt{x}$ 在 $(0,1]$ 上 Lebesgue 可积($\int_0^1x^{-1/2}=2$),尽管无界。

## 常见误区

- 以为"积分存在" = "可积"。错:可积要求 $\int|f|<\infty$;仅 $\int f$ 有限(一边无穷抵消)不算可积。
- 以为 Lebesgue 积分需要函数连续。错:只要求可测。
- 忽略绝对连续性——它是后面 FTC 与 Vitali 收敛定理的枢纽。

## 与实变函数的连接

- 定义在简单函数之上([[实变函数-简单函数]])。
- 三大收敛定理给出极限交换条件([[实变函数-三大收敛定理]])。
- 绝对连续性升级为"绝对连续函数"才还原 FTC([[实变函数-绝对连续与微积分基本定理]])。

## 最小自测

- [ ] 陈述 $f\in L^1$ 的定义,并区分"积分存在"与"可积"
- [ ] 证明积分的绝对连续性
- [ ] 说明 $\mathbf 1_{\mathbb Q}$ 在 $[0,1]$ 的 Lebesgue 积分,并对比其 Riemann 不可积

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-三大收敛定理]]。
