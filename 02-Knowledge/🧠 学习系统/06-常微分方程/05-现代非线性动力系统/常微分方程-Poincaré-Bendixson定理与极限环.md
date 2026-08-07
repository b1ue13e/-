---
type: study
topic: "Poincaré-Bendixson定理与极限环"
course: "常微分方程"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段5-现代非线性动力系统]]"
upstream:
  - "[[常微分方程-相平面与方向场基础]]"
  - "[[常微分方程-渐近稳定]]"
flow: knowledge
kind: concept
difficulty: advanced
tags:
  - 学习
  - 常微分方程
  - 动力系统
  - 极限环
---

# 🔄 常微分方程：Poincaré-Bendixson 定理与极限环 (Limit Cycles)

> **所属阶段**：[[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统|阶段5-现代非线性动力系统]]  
> **前置知识**：[[常微分方程-相平面与方向场基础]]、[[常微分方程-渐近稳定]]  

---

## 1. 💡 动机与直觉 (Intuition & Motivation)

在非线性二维系统（平面动力系统）中，除了孤立的平衡点外，还可能存在自我维持的非平凡周期运动——**极限环 (Limit Cycle)**。极限环是相平面上一条**孤立的封闭轨道**，附近的相轨线会随着时间推移逐渐向其靠拢（稳定极限环）或排斥（不稳定极限环）。

例如心脏的自发跳动、钟表的摆动、Van der Pol 振荡电路等，都是典型的极限环系统。**Poincaré-Bendixson 定理**是二维动力学中最强大的定理之一，它给出了二维平面上确定闭轨线/极限环存在性的充要或充分条件，彻底证明了二维自治系统**不可能存在混沌**。

---

## 2. 📐 正式定义与 Poincaré-Bendixson 定理

### 2.1 极限环的定义
考虑二维自治微分方程组：
$$\begin{cases} \frac{dx}{dt} = f(x, y) \\ \frac{dy}{dt} = g(x, y) \end{cases}$$

若 $\gamma$ 是相平面上的一条闭轨线，且存在 $\gamma$ 的一个邻域 $U$，使得 $U \setminus \gamma$ 内的所有轨迹在 $t \to +\infty$（或 $t \to -\infty$）时均渐近趋近于 $\gamma$，则称 $\gamma$ 为**极限环 (Limit Cycle)**。

### 2.2 Poincaré-Bendixson 定理 (定理表述)
设 $R$ 是相平面上一个闭合有界的区域（即紧集），满足：
1. **正不变性 (Positively Invariant)**：从 $R$ 内任意初始点出发的轨迹 $\mathcal{C}^+$ 在 $t \ge 0$ 时永远留在 $R$ 内部。
2. **无奇异点 (No Equilibrium Points)**：区域 $R$ 内部不包含任何奇点（平衡点）。

**结论**：轨线 $\mathcal{C}^+$ 在 $R$ 内必收敛于一条**封闭的周期轨道（极限环）**，或者本身就是一条闭轨线。

---

## 3. 💡 典型代数与数值计算实例 (Example)

### 实例 1：应用 Poincaré-Bendixson 捕获箱法 (Trapping Region) 证明极限环存在
**题目**：考虑极坐标下的系统：
$$\begin{cases} \frac{dr}{dt} = r(1 - r^2) + \mu r \cos\theta \\ \frac{d\theta}{dt} = 1 \end{cases}$$
当 $\mu = 0$ 时，证明系统存在唯一稳定极限环。

**详细证明**：
1. 当 $\mu = 0$ 时，径向方程化为：
   $$\frac{dr}{dt} = r(1 - r^2)$$
2. 构造环形捕获区域 $R = \{(r, \theta) \mid 0.5 \le r \le 1.5\}$。
   - 在内边界 $r = 0.5$ 处：$\frac{dr}{dt} = 0.5(1 - 0.25) = 0.375 > 0$，向量场指向 $R$ 内部；
   - 在外边界 $r = 1.5$ 处：$\frac{dr}{dt} = 1.5(1 - 2.25) = -1.875 < 0$，向量场指向 $R$ 内部。
3. 环形区域 $R$ 内没有奇点（奇点仅在原点 $r=0$，不在 $R$ 内）。
4. 根据 Poincaré-Bendixson 定理，环形区域 $R$ 内必存在至少一条稳定极限环（此处即为圆周 $r=1$）。

---

## 4. ⚠️ 常见误区与陷阱 (Pitfalls)

1. ❌ **误区 1**：认为三维或高维系统也适用 Poincaré-Bendixson 定理。
   - **纠正**：Poincaré-Bendixson 定理**仅适用于二维平面/球面**。三维及以上系统由于轨线可以相交避开，允许存在混沌吸引子（如 Lorenz 系统）。
2. ❌ **误区 2**：忽略了捕获区域内“无奇点”的条件。
   - **纠正**：如果区域内包含不稳定的焦点或鞍点，轨迹可能收敛于奇点而非闭轨线。

---

## 5. 🔍 检索练习与自测 (Self-Check)

1. [ ] **概念自测**：说明稳定极限环与中心点（Center）族轨道在扰动下的本质区别。
2. [ ] **证明自测**：使用 Bendixson 准则（$\nabla \cdot \vec{f} \ne 0$ 不变号）证明系统 $\frac{dx}{dt} = y, \frac{dy}{dt} = -x - y + x^3$ 在整个平面上不存在闭轨线。

---

## 6. 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
