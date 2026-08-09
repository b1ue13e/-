---
title: "实变函数-Cantor集与零测集"
topic: "实变函数-Cantor集与零测集"
date: "2026-08-03"
updated: 2026-08-09
type: study
course: "实变函数"
importance: "A"
tags: [学习, 实变函数]
stage_moc: "[[🧭 阶段2-Lebesgue理论]]"
flow: knowledge
kind: concept
upstream: ["[[实变函数-外测度]]"]
status: completed
learn_status: not_started
difficulty: intermediate
concept: ["Cantor 集", "零测集"]
prerequisites: ["Lebesgue 测度", "外测度", "点集拓扑"]
related: ["[[实变函数-稠密与可分]]", "[[实变函数-可测函数]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.1"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
created: 2026-08-03
---

# 实变函数-Cantor集与零测集

## 为什么学

Cantor 集是实变里第一个"反直觉"对象:它非空、完全(每点都是聚点)、无处稠密,却长度为 0。它同时演示了两件事:(1) 零测集可以"很大"(不可数);(2) "长度=0" 与 "可数" 不是一回事。这是测度论构造反例的母矿,也预告了"单调函数导数积分不一定还原"的怪现象。

## 核心定义

- **零测集**:$E\subset\mathbb{R}$ 零测,若 $\mu^*(E)=0$,即对任意 $\varepsilon>0$ 存在可数开区间覆盖使总长 $<\varepsilon$。
- **Cantor 集构造**:从 $C_0=[0,1]$ 删去中间开区间 $(1/3,2/3)$,得 $C_1=[0,1/3]\cup[2/3,1]$;第 $n$ 步保留 $2^n$ 个长度 $3^{-n}$ 的闭区间。$C=\bigcap_{n=0}^{\infty}C_n$。

## 证明主线(逐步展开)

### 1. $\mu(C)=0$

$C_n$ 是 $2^n$ 个长度 $3^{-n}$ 闭区间之并,故 $\mu(C_n)\le 2^n\cdot 3^{-n}=(2/3)^n\to 0$。$C\subset C_n$ 对所有 $n$,故 $\mu(C)\le (2/3)^n$ 任意小,取极限得 $\mu(C)=0$。

### 2. $C$ 不可数(与 $[0,1]$ 等势)

用三进制展开:$x\in C$ 当且仅当它的三进制展开 $x=\sum a_k 3^{-k}$ 中各位 $a_k\in\{0,2\}$("选 1" 的那位恰好落在被删开区间内)。把数字 0↔0、2↔1 映射为二进制
$$f(x)=\sum_{k=1}^\infty \frac{a_k}{2}\cdot 2^{-k}\in[0,1].$$
这是 $C\to[0,1]$ 的满射(每个二进制数都来自某个 $x\in C$),故 $|C|\ge\mathfrak c$,即 $C$ 不可数。

### 3. $C$ 完全且无处稠密

- **完全**($C$ 闭且无孤立点):$C$ 是闭集之交,故闭;任意 $x\in C$ 的任意邻域都含 $C$ 中其他点,因为构造保留的区间可任意小。
- **无处稠密**:$C$ 的闭包内部为空。$C_n$ 各步删去的中间开区间之并稠密,故 $C$ 无内点。

## 最小例子

- 可数集零测($\mu^*(\mathbb{Q})=0$,见 [[实变函数-外测度]])。Cantor 集是**不可数零测集**的代表——直接打破"零测=可数"的错觉。
- **Cantor 函数( devil's staircase )**:在 $C$ 的补集的每个构成区间上取常数、在 $C$ 上单调连续增到 1,满足导数 a.e. 为 0 却把 $[0,1]$ 映到 $[0,1]$。它预告:仅"单调连续"不足以让"导数积分还原函数"——需要绝对连续(见 [[实变函数-绝对连续与微积分基本定理]])。

## 常见误区

- 以为零测 = 可数。$C$ 是不可数零测集的反例。
- 以为 $C$ 是离散点集。$C$ 没有任何孤立点。
- 三进制判定中"选 1"的点恰好是被删开区间的端点,端点有双重三进制展开,需小心处理。

## 与实变函数的连接

- 是外测度/测度的第一批"惊人"对象([[实变函数-外测度]])。
- 预告依测度收敛与 a.e. 收敛的差异([[实变函数-收敛关系]])。
- 与 Cantor 函数一起说明 FTC 需要绝对连续而非仅单调连续([[实变函数-绝对连续与微积分基本定理]])。

## 最小自测

- [ ] 闭卷证明 $\mu(C)=0$
- [ ] 用三进制构造证明 $C$ 不可数
- [ ] 陈述 $C$ 的三个反直觉性质(零测 / 不可数 / 完全且无处稠密)

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-可测函数]]。
