---
type: study
topic: "Jordan标准形"
course: "高等代数"
created: 2026-08-06
status: ongoing
difficulty: advanced
concept: ["Jordan块", "Jordan标准形", "特征向量链", "广义特征向量", "矩阵指数"]
stage_moc: "[[🌟 第三阶段：行列式、特征值与对角化]]"
upstream: ["[[相似对角化条件与判定]]"]
flow: knowledge
kind: concept
source: "Hefferon Linear Algebra Ch.5 §5.5（延伸）+ MIT 18.06SC Lec 28；参考高等代数（第5版）"
source_url: "https://hefferon.net/linearalgebra/"
accessed: 2026-08-06
license: "CC BY-SA 4.0（Hefferon）；MIT OCW（18.06SC）"
tags: [高等代数, 线性代数, Jordan标准形]
---

# Jordan 标准形

> **核心问题**：不能对角化的矩阵，最简能简化到什么程度？——Jordan 标准形。

## 0. 学习边界

| 分类 | 评估 |
|:--|:--|
| 价值等级 | **A** — 任意复矩阵相似标准形的综合答案；$\operatorname{gm}<\operatorname{am}$ 时的补救 |
| 理由 | 微分方程 $e^{At}$、矩阵幂、系统理论都靠 Jordan 形兜底；是"相似分类"的完备解答 |
| 投入建议 | 必须理解 Jordan 块结构、会构造特征向量链、能写出简单缺陷矩阵的 Jordan 形 |

## 1. 这个知识点解决什么问题？

3.8 说可对角化 ⟺ 特征向量铺满空间。但缺陷矩阵（$\operatorname{gm}<\operatorname{am}$，如 $\begin{bmatrix}2&1\\0&2\end{bmatrix}$）特征向量不够用——最简形式是什么？**Jordan 标准形**：分块对角，每块是 Jordan 块（对角元是特征值，上对角线是 1）。它"尽量接近对角"，并在**相似意义下唯一**（不计分块顺序）。

## 2. 它为什么重要？它有什么用？

- **相似分类完备化**：任意复矩阵相似于唯一 Jordan 形（不计分块顺序）——3.11 给出判定工具。
- **矩阵幂**：$J^k$ 的块结构给出 $A^k$ 的显式公式（含 $\binom{k}{t}\lambda^{k-t}$ 项）。
- **矩阵指数**：$e^{Jt}=e^{\lambda t}(I+Nt+\frac{N^2t^2}{2!}+\cdots)$——常微分方程组的通解。
- **系统理论**：可控性/稳定性分析（复特征值、约当块的代数结构）。

## 3. 学它之前需要哪些前置知识？

1. [[相似对角化条件与判定|相似对角化条件与判定]]：可对角化判据与缺陷概念。
2. [[特征多项式与特征值性质|特征多项式与特征值性质]]：代数/几何重数、极小多项式。
3. [[核与像|核与像]]（阶段 II）：$\ker(A-\lambda I)^k$ 的递推。

## 4. 定义复述

### 4.1 Jordan 块

$m\times m$ **Jordan 块** $J_m(\lambda)=\lambda I+N$，$N$ 为上对角线全 1、其余 0：

$$J_m(\lambda)=\begin{bmatrix}\lambda&1&&\\&\lambda&\ddots&\\&&\ddots&1\\&&&\lambda\end{bmatrix}$$

### 4.2 Jordan 标准形

$J=\operatorname{diag}(J_{m_1}(\lambda_1),\dots,J_{m_r}(\lambda_r))$（分块对角）。

### 4.3 Jordan 标准形定理

任意 $A\in\mathbb{C}^{n\times n}$ 相似于 Jordan 标准形，且在**分块顺序意义下唯一**。

- 每个 Jordan 块对应一条**特征向量链**：$(A-\lambda I)\mathbf{v}_m=\mathbf{v}_{m-1},\dots,(A-\lambda I)\mathbf{v}_1=\mathbf{0}$（$\mathbf{v}_1$ 是特征向量，$\mathbf{v}_k$ 是**广义特征向量**）。
- 同一 $\lambda$ 的 Jordan 块个数 = $\operatorname{gm}(\lambda)$；块总大小 = $\operatorname{am}(\lambda)$。

### 4.4 与可对角化的关系

$A$ 可对角化 ⟺ 所有 Jordan 块都是 $1\times1$ ⟺ $\operatorname{gm}=\operatorname{am}$ 对所有特征值。

## 5. 直觉与图像

- 缺陷 = "剪切"：特征方向不够时，矩阵还"斜推"了一下（Jordan 块的上对角线 1）。
- Jordan 块 = "旋转已拆掉，只剩拉伸 + 单方向剪切"的最小积木。
- 特征向量链 = "广义特征向量的阶梯"：$\mathbf{v}_1$（真特征向量）→ $(A-\lambda I)$ 一层层"上台阶"。

> **一句话本质**：Jordan 形 = 把任意矩阵拆成"拉伸块（对角）＋最小剪切块（Jordan 块）"的综合标准形。

## 6. 定理陈述与证明重建

### 定理：Jordan 块的结构（$N$ 的幂）

$J_m(\lambda)=\lambda I+N$，$N$ 为上移位矩阵。则 $N^k$ 是把 1 移到第 $k$ 条上对角线，$N^m=0$（幂零指数 $=m$）。故

$$J_m(\lambda)^k=\sum_{t=0}^{m-1}\binom{k}{t}\lambda^{k-t}N^t$$

**证明主线**：$J^k=(\lambda I+N)^k$ 用二项式定理展开（$\lambda I$ 与 $N$ 可交换），$N^m=0$ 截断。$\square$

**关键"转念"**：把 Jordan 块写成"数乘 + 幂零"两半，幂零部分有限步归零，展开可截断。

### 定理：$e^{J_m(\lambda)t}=e^{\lambda t}\sum_{t'=0}^{m-1}\frac{N^{t'}t^{t'}}{t'!}$

**证明主线**：$e^{At}=e^{\lambda It}e^{Nt}$（可交换故指数分离），$e^{Nt}=\sum N^{t'}t^{t'}/t'!$ 截断于 $N^m=0$。$\square$

### 定理：$J$ 的幂零结构唯一（Jordan 形唯一性）

**证明主线**（要点）：$\dim\ker(A-\lambda I)^k$ 的阶梯（$k=1,2,\dots$）完全决定 $\lambda$ 的 Jordan 块大小序列；而 $\dim\ker(A-\lambda I)^k$ 是相似不变量 ⟹ 块大小序列唯一。$\square$（完整论证用 3.11 不变因子。）

## 7. 经典反例库

### 反例 1：$A=\begin{bmatrix}2&1\\0&2\end{bmatrix}$ 的 Jordan 形

$\operatorname{am}(2)=2$，$\operatorname{gm}(2)=1$ ⟹ 一个 $2\times2$ Jordan 块 $J_2(2)$——不可对角化。

### 反例 2：特征值相同但 Jordan 块大小不同 ⟹ 不相似

$\begin{bmatrix}2&1&0\\0&2&0\\0&0&2\end{bmatrix}$（$J_2(2)\oplus J_1(2)$）与 $2I_3$（$J_1\oplus J_1\oplus J_1$）：特征多项式都是 $(\lambda-2)^3$，但 $\dim\ker(A-2I)$ 分别是 2 和 3，不相似——**几何重数区分**。

### 反例 3：$\mathbb{R}$ 上不存在的 Jordan 形

$R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ 在 $\mathbb{R}$ 上无 Jordan 形（复特征值 $\pm i$）；在 $\mathbb{C}$ 上 $R\sim\operatorname{diag}(i,-i)$。Jordan 定理默认复数域。

## 8. 条件变式

| 变式方向 | 具体变化 | 影响 |
|:--|:--|:--|
| 弱化：实矩阵 | 复 Jordan 形需 $\mathbb{C}$ | 实 Jordan 形用旋转块替代 |
| 加强：可对角化 | 全 $1\times1$ 块 | 退化到 3.8 |
| 换对象：幂零矩阵 | 特征值全 0 | Jordan 块即幂零块 $N$ |
| 换视角：极小多项式 | $m_A$ 的幂次 = 最大块大小 | Jordan 结构速查 |
| 应用：$e^{At}$ | 每块独立求 | 常微分方程组通解 |

## 9. 相关知识点与 Obsidian 双链建议

- [[相似对角化条件与判定|相似对角化条件与判定]] — 上游
- [[λ-矩阵与不变因子|λ-矩阵与不变因子]] — 下游：Jordan 形的计算与唯一性工具
- [[相似矩阵与相似不变量|相似矩阵与相似不变量]] — 横向：Jordan 形是相似类代表元
- [[矩阵函数|矩阵函数]]（阶段 IV）— 横向：$f(J)$ 的块运算
- [[特征值计算|特征值计算]]（阶段 IV）— 横向：数值方法

## 10. 闭卷验收（数学模式）

- [ ] **定义默写**：Jordan 块、Jordan 形、特征向量链、广义特征向量。
- [ ] **定理陈述**：Jordan 标准形定理（存在 + 唯一）。
- [ ] **证明**：$J^k$ 的二项式展开；$e^{Jt}$ 公式。
- [ ] **计算**：给 $4\times4$ 缺陷矩阵写 Jordan 形（含块大小判定）。
- [ ] **反例**：同特征多项式不同 Jordan 结构不相似。

## 11. 分级习题

| 等级 | 题目 | 来源 |
|:--|:--|:--|
| ★ | 写出 $\begin{bmatrix}3&1&0\\0&3&1\\0&0&3\end{bmatrix}$ 的 Jordan 形 | Hefferon §5.5 |
| ★★ | 计算 $J_2(\lambda)^k$ 与 $e^{J_2(\lambda)t}$ | MIT 18.06 Lec 28 |
| ★★★ | 证明：$A$ 可对角化 ⟺ 每个 Jordan 块为 $1\times1$ | 高等代数（第5版） |
| ★★★★ | 用 $\dim\ker(A-\lambda I)^k$ 判定 $A=\begin{bmatrix}2&1&0\\0&2&1\\0&0&2\end{bmatrix}$ 的 Jordan 形并验证唯一性 | 高等代数（第5版） |

## 12. 我的主动回忆区

> 不看上文：写 Jordan 块定义；$J^k$ 展开；$e^{Jt}$ 公式；构造 $J_2(2)$ 的特征向量链。

## 13. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---
*创建于：2026-08-06 | 来源：Hefferon Ch.5 §5.5 延伸 + MIT 18.06SC Lec 28 + 高等代数（第5版）；旧空壳（Jordan块、Jordan标准形定理、Jordan形的应用）于 2026-08-06 合并/重写*

