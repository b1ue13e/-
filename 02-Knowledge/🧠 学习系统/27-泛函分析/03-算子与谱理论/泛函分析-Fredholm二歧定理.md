---
type: study
topic: "Fredholm二歧定理"
course: "泛函分析"
created: 2026-08-09
updated: 2026-08-09
status: active
stage_moc: "[[🧭 阶段3-算子与谱理论]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["Fredholm算子", "Fredholm二歧定理", "紧摄动", "指标定理", "积分方程求解", "有限维二歧性"]
prerequisites: ["谱理论与紧自伴算子谱定理"]
upstream: ["[[泛函分析-谱理论与紧自伴算子谱定理]]"]
tags: [学习, 数学, 泛函分析, Fredholm, 积分方程, 算子可逆性, 紧摄动]
proof_mode: true
source: "MIT 18.102 Lec 15; Erwin Kreyszig, Chapter 8.4-8.7; Haim Brezis, Chapter 6"
source_url: "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
---

# 泛函分析-Fredholm二歧定理

> 所属阶段：[[🧭 阶段3-算子与谱理论|第三阶段：算子与谱理论]]
> 目标：掌握紧算子摄动方程 $(I - K)u = f$ 的 Fredholm 二歧性定理、核空间与伴随核空间有限维等维性质（$\operatorname{ind}(I-K) = 0$），以及第二类 Fredholm 积分方程的显式求解与相容性条件。

---

## 0. 知识定位与无穷维方程的可解性二歧

### 1. 为什么 Fredholm 理论是无穷维方程的救星？
在有限维线性代数中，对于线性方程组 $(I - A)x = y$：
- **要么**齐次方程 $(I - A)x = 0$ 只有零解，此时矩阵 $I - A$ 可逆，非齐次方程对**任意右端项 $y$ 存在唯一解**；
- **要么**齐次方程有非零解，此时非齐次方程**有解当且仅当 $y$ 正交于伴随齐次方程的解**。
在一般的无穷维空间中，单射不再等价于满射，上述二歧性彻底失效。
**Fredholm 发现：只要算子是恒等算子加上紧算子（紧摄动 $I - K$）**，这种极其优美的有限维二歧可解性**在无穷维中奇迹般地完全复活**！

---

## 1. Fredholm 算子与指标定义

### 1. Fredholm 算子
设 $X, Y$ 为 Banach 空间，$T \in \mathcal{B}(X, Y)$。若满足：
1. $\ker(T)$ 是有限维子空间（$\dim \ker(T) < \infty$）；
2. $\operatorname{Im}(T)$ 是闭子空间，且上核 $\operatorname{coker}(T) = Y / \operatorname{Im}(T)$ 是有限维（$\operatorname{codim} \operatorname{Im}(T) < \infty$）。
则称 $T$ 为 **Fredholm 算子**。其 **Fredholm 指标 (Index)** 定义为：
$$\operatorname{ind}(T) = \dim \ker(T) - \operatorname{codim} \operatorname{Im}(T)$$

### 2. 紧摄动指标不变定理
**定理**：若 $T$ 是 Fredholm 算子，$K \in \mathcal{K}(X, Y)$ 是紧算子，则 $T + K$ 仍是 Fredholm 算子，且指标严格不变：
$$\operatorname{ind}(T + K) = \operatorname{ind}(T)$$
特别地，取 $T = I$（此时 $\ker(I) = \{0\}, \operatorname{Im}(I) = X \implies \operatorname{ind}(I) = 0$），对任意紧算子 $K \in \mathcal{K}(X)$：
$$\operatorname{ind}(I - K) = 0 \iff \dim \ker(I - K) = \operatorname{codim} \operatorname{Im}(I - K)$$

---

## 2. 核心定理：Fredholm 二歧定理 (Fredholm Alternative)

### 1. 定理陈述
设 $H$ 为 Hilbert 空间，$K \in \mathcal{K}(H)$ 为紧算子。考虑方程：
$$(I - K) u = f \quad \text{与伴随方程} \quad (I - K^*) v = g$$
则必定且只必定发生以下两情形之一：
- **情形一 (唯一可解性)**：
  齐次方程 $(I - K)u = 0$ 只有零解 $\iff$ 对任意 $f \in H$，非齐次方程 $(I - K)u = f$ 存在唯一的强解 $u \in H$，且逆算子 $(I - K)^{-1}$ 有界连续。
- **情形二 (相容可解性与共振)**：
  齐次方程 $(I - K)u = 0$ 拥有 $m$ 个线性无关解 $\{u_1, \dots, u_m\}$ ($1 \le m < \infty$)。
  此时伴随齐次方程 $(I - K^*)v = 0$ 也恰好拥有 $m$ 个线性无关解 $\{v_1, \dots, v_m\}$。
  非齐次方程 $(I - K)u = f$ 有解当且仅当 $f$ 满足正交相容性条件：
  $$\langle f, v_j \rangle = 0, \quad \forall j = 1, \dots, m$$

---

## 3. 经典应用：第二类 Fredholm 积分方程求解

考虑区间 $[a, b]$ 上的积分方程：
$$u(x) - \lambda \int_a^b K(x, y) u(y) dy = f(x)$$
1. 若 $\lambda^{-1} \notin \sigma(K)$（不是特征值倒数），方程存在唯一解，解由预解核 (Resolvent Kernel) 显式给出：
   $$u(x) = f(x) + \lambda \int_a^b R(x, y; \lambda) f(y) dy$$
2. 若 $\lambda^{-1} = \lambda_k$ 为特征值，方程有解当且仅当 $\int_a^b f(x) \overline{\psi_k(x)} dx = 0$（其中 $\psi_k$ 为伴随特征函数）。

---

## 4. 闭卷自测与练习

- [ ] 能清楚写出 Fredholm 算子指标的定义，并说明为什么 $\operatorname{ind}(I - K) = 0$。
- [ ] 能陈述 Fredholm 二歧定理的两种互斥情形。
- [ ] 能分析当参数 $\lambda$ 处于共振特征值时积分方程的相容性条件。

---

## 🃏 Anki 卡片

TARGET DECK: 泛函分析::03-算子与谱理论

Q: 叙述 Fredholm 二歧定理 (Fredholm Alternative) 的核心结论。
A: 
设 $K$ 为紧算子。对方程 $(I - K)u = f$：
1. 若齐次方程 $(I-K)u=0$ 只有零解，则对任意 $f$ 存在唯一连续解；
2. 若齐次方程有 $m$ 维非零解空间，则伴随齐次方程 $(I-K^*)v=0$ 亦有 $m$ 维解空间，且非齐次方程有解 $\iff f \perp \ker(I-K^*)$。
<!--ID: 1723180000018-->

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
