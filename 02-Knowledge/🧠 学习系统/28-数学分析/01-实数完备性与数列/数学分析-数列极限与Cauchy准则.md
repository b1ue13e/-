---
type: study
topic: "数列极限与Cauchy准则"
course: "28-数学分析"
created: 2026-08-09
status: planned
stage_moc: "[[🧭 阶段1-实数完备性与数列]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: [数列极限, Cauchy数列, 子列]
upstream: ["[[数学分析-实数完备性与确界]]"]
source: "Jiří Lebl, Basic Analysis I, v6.3, Sections 2.1-2.4"
source_url: "https://www.jirka.org/ra/html/seq_chapter.html"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0 / CC BY-SA 4.0"
tags: [学习, 数学分析, 数列]
---

# 数学分析-数列极限与Cauchy准则

## 定义与量词

数列 $(a_n)$ 收敛到 $L$，记 $a_n\to L$，若
$$\forall\varepsilon>0\ \exists N\in\mathbb N\ \forall n\ge N: |a_n-L|<\varepsilon.$$

数列是 Cauchy 数列，若
$$\forall\varepsilon>0\ \exists N\ \forall m,n\ge N: |a_m-a_n|<\varepsilon.$$

收敛定义需要知道候选 $L$；Cauchy 定义只比较尾部项，因此能在未知极限时判断“是否应当有极限”。

子列 $(a_{n_k})$ 要求 $n_1<n_2<\cdots$。聚点是某个收敛子列的极限，不等于原数列极限。

## 核心定理链

1. 极限唯一。
2. 收敛数列有界，且每个子列收敛到同一极限。
3. 收敛数列必为 Cauchy。
4. 在 $\mathbb R$ 中，Cauchy 数列必收敛。
5. 每个有界实数数列都有收敛子列（Bolzano-Weierstrass）。

### 极限唯一的证明骨架

若 $a_n\to L$ 且 $a_n\to M$，假设 $L\ne M$，取 $\varepsilon=|L-M|/3$。当 $n$ 同时足够大时，
$$|L-M|\le |L-a_n|+|a_n-M|<2|L-M|/3,$$
矛盾。

### Cauchy 完备性的证明接口

Cauchy 数列先证明有界；由 Bolzano-Weierstrass 取收敛子列 $a_{n_k}\to L$；再用 Cauchy 性把任意尾项 $a_n$ 与某个足够后的子列项 $a_{n_k}$ 拉近，得到 $a_n\to L$。真正使用实数完备性的地方藏在 Bolzano-Weierstrass。

## Worked example：$a_n=n/(n+1)$

目标是证明 $a_n\to1$。给定 $\varepsilon>0$，
$$|a_n-1|=\frac1{n+1}.$$
只需选 $N>1/\varepsilon$，则 $n\ge N$ 时 $1/(n+1)<\varepsilon$。写证明时必须说明 $N$ 如何依赖 ε，不能只写“当 $n$ 很大”。

## Completion problem：收敛推出 Cauchy

已知 $a_n\to L$。给定 ε，选择 $N$ 使 $n\ge N$ 时 $|a_n-L|<\underline{\qquad}$。对 $m,n\ge N$，用三角不等式补全
$$|a_m-a_n|\le \underline{\qquad}+\underline{\qquad}<\varepsilon.$$

答案应使用 $\varepsilon/2$，而不是另外猜一个界。

## 反例与辨析

- $(-1)^n$ 有界但不收敛；它有两个不同聚点。
- $a_n=n$ 没有收敛子列，说明 BW 的有界条件不能省。
- 在 $\mathbb Q$ 中可构造趋近 $\sqrt2$ 的有理 Cauchy 数列，但它在 $\mathbb Q$ 内不收敛。
- $a_{n+1}-a_n\to0$ 不推出 Cauchy，例如调和部分和。

## 闭卷检索与通过标准

1. 写出收敛和 Cauchy 的定义与否定。
2. 完整证明极限唯一。
3. 说明“有界 → 有收敛子列”和“有界 → 收敛”的差别。
4. 从 Cauchy + 收敛子列推出原数列收敛。

定义无量词错误、两条证明闭卷可重建，才通过。

## 下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/28-数学分析"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/28-数学分析"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

