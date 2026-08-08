---
type: study
topic: "Cramer法则"
course: "高等代数"
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: ["Cramer法则", "行列式比值", "解的显式公式"]
stage_moc: "[[🌟 第三阶段：行列式、特征值与对角化]]"
upstream: ["[[行列式的计算]]"]
flow: knowledge
kind: concept
source: "Hefferon Linear Algebra Ch.4 §4.5 + MIT 18.06SC Lec 20；参考高等代数（第5版）"
source_url: "https://hefferon.net/linearalgebra/"
accessed: 2026-08-06
license: "CC BY-SA 4.0（Hefferon）；MIT OCW（18.06SC）"
tags: [高等代数, 线性代数, Cramer法则]
---

# Cramer 法则

> **核心问题**：方阵方程组 $A\mathbf{x}=\mathbf{b}$ 的解，能不能用行列式"一比"就出来？

## 0. 学习边界

| 分类 | 评估 |
|:--|:--|
| 理由 | 证明简洁优美、连接行列式与解；但工程计算必须用消元/LU |
| 投入建议 | 必须能推导并会算 $2\times2$、$3\times3$；记住"理论用、数值不用"的边界 |

## 1. 这个知识点解决什么问题？

阶段 I 用高斯消元求 $A\mathbf{x}=\mathbf{b}$。Cramer 给出**解的显式公式**：$x_j=\det A_j/\det A$——不消元、直接"比值"。它回答"解长什么样"，并给出"解依赖系数如何变化"的解析形式（经济学比较静态、微分方程解公式的基础）。

## 2. 它为什么重要？它有什么用？

- **解的存在唯一**：$\det A\neq0$ ⟺ 唯一解（Cramer 公式直接给出）。
- **理论工具**：证明"解对 $\mathbf{b}$ 线性"、灵敏度分析。
- **比较静态分析**（经济学）：$x_j$ 关于某个系数的偏导 = 行列式之比。
- **应用边界**：$n\ge4$ 时 $n$ 个行列式各需 $O(n^3)$，总 $O(n^4)$——远不如 $O(n^3)$ 的消元。**只用于理论与小规模推导**。

## 3. 学它之前需要哪些前置知识？

1. [[行列式的计算|行列式的计算]]：展开与性质。
2. [[线性方程组与高斯消元法|线性方程组与高斯消元法]]（阶段 I）：解的语义。
3. [[逆矩阵与Gauss-Jordan消元|逆矩阵]]（阶段 I）：$A^{-1}$ 与解的联系。

## 4. 定义复述

### 4.1 公式

$A\mathbf{x}=\mathbf{b}$，$\det A\neq0$，令 $A_j$ 为把 $A$ 第 $j$ 列替换为 $\mathbf{b}$ 后的矩阵，则

$$x_j = \frac{\det A_j}{\det A},\qquad j=1,\dots,n$$

### 4.2 例子（$2\times2$）

$\begin{cases}2x+3y=7\\x-y=1\end{cases}$：$D=\det\begin{bmatrix}2&3\\1&-1\end{bmatrix}=-5$；$D_1=\det\begin{bmatrix}7&3\\1&-1\end{bmatrix}=-10$；$D_2=\det\begin{bmatrix}2&7\\1&1\end{bmatrix}=-5$。
故 $x=D_1/D=2$，$y=D_2/D=1$。检验：$2(2)+3(1)=7$ ✓，$2-1=1$ ✓。

## 5. 直觉与图像

- $x_j$ = "把第 $j$ 列换成 $\mathbf{b}$ 后的体积" ÷ "原体积"——**分量 = 定向体积比**。
- 几何：$\mathbf{b}$ 在第 $j$ 个方向上的"伸展比例"。
- 与 $A^{-1}\mathbf{b}$ 的关系：$A^{-1}=\frac{1}{\det A}\operatorname{adj}A$，第 $j$ 行乘 $\mathbf{b}$ 恰好给出 $\det A_j$（3.5 将展示）。

> **一句话本质**：Cramer 法则 = 解的第 $j$ 分量是"把第 $j$ 列换成 $\mathbf{b}$"的行列式与原行列式之比。

## 6. 定理陈述与证明重建

### 定理：Cramer 法则

**前提**：$A$ 可逆（$\det A\neq0$）；**结论**：$x_j=\det A_j/\det A$。

**证明主线**：
1. 记 $A$ 的列为 $\mathbf{a}_1,\dots,\mathbf{a}_n$，则 $\mathbf{b}=x_1\mathbf{a}_1+\cdots+x_n\mathbf{a}_n$；
2. 在 $D_j=\det(\mathbf{a}_1,\dots,\mathbf{b},\dots,\mathbf{a}_n)$ 中代入 $\mathbf{b}$ 的展开，由**多线性**拆成 $n$ 项；
3. 第 $i\neq j$ 项含重复列 $\mathbf{a}_i$（出现两次）⟹ 行列式 $=0$；
4. 仅剩第 $j$ 项：$D_j=x_j\det(\mathbf{a}_1,\dots,\mathbf{a}_n)=x_jD$。$\square$

**关键"转念"**：多线性 + 交替性（重复列归零）把"解线性组合"变成"筛选出单个分量"。

## 7. 经典反例库

### 反例 1：$\det A=0$ 时公式失效

$A$ 奇异时 $A_j$ 可能非零，但 $x_j=D_j/0$ 无定义——Cramer 不能判定"无解 vs 无穷多解"（那是秩的职责，阶段 I 1.11）。

### 反例 2：$n$ 阶 Cramer 计算量陷阱

$n=20$ 时计算 $20$ 个 $20\times20$ 行列式（各约 $O(20^3)$ 次运算）≈ 远超一次 $O(20^3)$ 的消元——"美貌的代价"。

### 反例 3：Cramer 要求方阵

$m\times n$ 长方形系统没有 $\det$，不能用 Cramer——用秩/最小二乘（阶段 IV）。

## 8. 条件变式

| 变式方向 | 具体变化 | 影响 |
|:--|:--|:--|
| 弱化：$\det A=0$ | 无唯一解 | 交给秩理论 |
| 加强：$\mathbf{b}=0$ | $x_j=0/\det A=0$ | 齐次系统只有零解 |
| 换视角：列替换 | 替换第 $j$ 列 | 公式定义 $A_j$ |
| 换用途：灵敏度 | $dx_j/db_k=\det A_{jk}/\det A$ | 比较静态分析 |

## 9. 相关知识点与 Obsidian 双链建议

- [[行列式的计算|行列式的计算]] — 上游
- [[伴随矩阵与逆矩阵公式|伴随矩阵与逆矩阵公式]] — 下游：$A^{-1}$ 显式公式
- [[线性方程组与高斯消元法|线性方程组与高斯消元法]] — 横向：消元 vs 行列式两条路线
- [[矩阵的秩|矩阵的秩]] — 横向：$\det=0$ 时怎么办

## 10. 闭卷验收（数学模式）

- [ ] **公式默写**：$x_j=\det A_j/\det A$ 及 $A_j$ 定义。
- [ ] **推导**：多线性 + 重复列归零的完整论证。
- [ ] **计算**：$3\times3$ 系统用 Cramer 求解。
- [ ] **边界**：何时不能用；计算复杂度对比。

## 11. 分级习题

| 等级 | 题目 | 来源 |
|:--|:--|:--|
| ★ | 用 Cramer 解 $\begin{cases}3x+2y=1\\x-y=2\end{cases}$ | Hefferon §4.5 |
| ★★★ | 证明：$A$ 可逆 ⟺ $A\mathbf{x}=\mathbf{b}$ 对任意 $\mathbf{b}$ 有唯一解（用 Cramer 必要性） | MIT 18.06 Lec 20 |
| ★★★★ | 比较 $n=10$ 时 Cramer 与 LU 消元的运算量（数量级） | Trefethen & Bau 补充 |

## 12. 我的主动回忆区

> 不看上文：写公式；推导一遍；算 $2\times2$；说明为何数值计算不用它。

## 13. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---
*创建于：2026-08-06 | 来源：Hefferon Ch.4 §4.5 + MIT 18.06SC Lec 20 + 高等代数（第5版）；旧卡（Cramer法则）于 2026-08-06 迁移/重写*

