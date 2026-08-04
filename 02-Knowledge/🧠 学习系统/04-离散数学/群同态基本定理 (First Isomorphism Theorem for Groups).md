---
type: concept
topic: 群同态基本定理
created: 2026-07-28
status: learning
difficulty: advanced
concept:
- 群同态基本定理
- 同态核
- 同态像
- 群同构
prerequisites:
- '[[正规子群与商群]]'
- '[[群定义]]'
related:
- '[[理想与商环]]'
tags:
- 学习
- 离散数学
- 代数结构
- 群论
- 同态
- 同构
- 正规子群
- 商群
- 群同态基本定理
title: 群同态基本定理
date: 2026-07-28
updated: 2026-07-28
kind: concept
flow: knowledge
course: 离散数学
importance: A
upstream:
- '[[正规子群与商群]]'
- '[[群定义]]'
- '[[等价类]]'
downstream:
- '[[单群]]'
- '[[理想与商环]]'
- '[[RSA加密]]'
stage: 🌐 第二阶段：核心深化 (Core Deepening)
module: 代数结构
---

# 群同态基本定理 (First Isomorphism Theorem for Groups)

## 0. 先判断它值不值得深挖

- **分类结果**: **A 类（核心概念，必须深挖）**
- **分类理由**: 群同态基本定理（也称群的第一同态定理, First Isomorphism Theorem for Groups）被称为抽象代数中的“微积分基本定理”。它在**群同态映射 (Homomorphism)**、**正规子群 (Normal Subgroup)**、**同态核 (Kernel)** 以及 **商群 (Quotient Group)** 之间建立起了一座极其完美的代数桥梁。它揭示了一个深刻本质：任何群同态的图像（像集），在代数同构的意义下，完全等价于原群关于同态核的商群！

---

## 1. 这个知识点解决什么问题？

**我们遇到了什么麻烦？**

假设我们发现了一个复杂的抽象大群 $G$，并通过某种映射 $\phi$ 将其投射到了一个我们熟悉的简易目标群 $G'$ 上（例如将庞大的矩阵群投射到一维的非零实数乘法上）。

我们迫切想知道：
1. 映射过程丢失了多少结构细节？
2. 映射所保留下来的影子部分（同态像 $\text{Im}(\phi)$），能否用大群 $G$ 自身内部的某种商结构精确再现？

**群同态基本定理**正是为了回答“**同态像到底与原群的什么商结构完全等价**”而诞生的。

---

## 2. 为什么它重要？它有什么用？

- **课程代数大图景位置**: 抽象代数中最核心、最漂亮的定理，将同态与商结构融为一体。
- **后续知识支撑**:
  - **第二/第三同态定理**: 基于第一同态定理延伸的子群格分解定理；
  - [[理想与商环]]: 环论第一同态定理 $R / \ker(\phi) \cong \text{Im}(\phi)$ 的直接原型；
  - [[单群]]: 利用同态核为 $\{\text{id}\}$ 判定单群结构。
- **实战与跨学科应用**:
  - **对称密码学与置换群**: 利用偶置换交错群 $A_n$ 为符号同态 $\text{sgn}$ 的核，精确计算奇偶置换类；
  - **线性代数与行列式**: 将高维可逆矩阵的体积缩放归结为行列式同态的商群；
  - **计算机拓扑与同调论**: 链复形中边缘算子的核与像计算同调群 $H_k = \ker(\partial_k) / \text{Im}(\partial_{k+1})$。

---

## 3. 学它之前需要哪些前置知识？

- **群同态 (Group Homomorphism)**: 映射 $\phi: G \to G'$ 保持运算：对任意 $a, b \in G$，均有 $\phi(a \circ_G b) = \phi(a) \circ_{G'} \phi(b)$。
- **同态核 (Kernel)**: $\ker(\phi) = \{ g \in G \mid \phi(g) = e' \}$ （所有被映射到目标群单位元的元素集合）。
- **同态像 (Image)**: $\text{Im}(\phi) = \{ \phi(g) \mid g \in G \}$。
  - *最小必要背景速补*: 同态核 $\ker(\phi)$ 衡量了映射“压缩消去”的细节数量，而同态像 $\text{Im}(\phi)$ 记录了映射“保留呈现”的结构。

---

## 4. 用直觉语言解释它

«“群同态基本定理其实就像**用皮影戏的灯光把 3D 物体投射成 2D 影子——影子的形状（同态像），完全等于把 3D 物体沿着所有平行光线切块打捆（商群）后的形状！**”»

假设你手里拿了一个 3D 模型（大群 $G$），用平行光垂直照射出墙上的影子（同态像 $\text{Im}(\phi)$）：
- 沿同一条光线落到墙上同一个点上的所有 3D 点，聚在一起形成一条直线（一个陪集）；
- 所有光线穿过的底座盲区，汇聚在原点（同态核 $\ker(\phi)$）；
- 定理告诉我们：只要你把 3D 模型沿着光线方向捆成一个个平行切片（构造商群 $G/\ker(\phi)$），这个切片组合的代数结构，和墙上的影子（像集 $\text{Im}(\phi)$）**在拓扑与代数上是绝对一模一样、完全同构的 ($\cong$)！**
- **直觉本质**: $G / \text{消去的细节}(\ker\phi) \cong \text{保留的影子}(\text{Im}\phi)$。

---

## 5. 正式定义、核心公式、符号解释

### 群同态基本定理 (First Isomorphism Theorem)

设 $\phi: G \to G'$ 是从群 $\langle G, \circ \rangle$ 到群 $\langle G', \ast \rangle$ 的一个**群同态映射**。
则有以下三个核心推论：

1. **核的正规性**:
   同态核 $\ker(\phi)$ 必定是 $G$ 的**正规子群**：
   $$ \ker(\phi) \triangleleft G $$
2. **自然同构映射**:
   定义映射 $\Phi: G / \ker(\phi) \to \text{Im}(\phi)$ 为：
   $$ \Phi(g \cdot \ker(\phi)) = \phi(g) $$
   则 $\Phi$ 是一个**良定义的群同构映射**（即单射、满射且保持运算的双射同态）。
3. **同构核心公式**:
   $$ G / \ker(\phi) \cong \text{Im}(\phi) $$
   若 $\phi$ 是满同态（即 $\text{Im}(\phi) = G'$），则有：
   $$ G / \ker(\phi) \cong G' $$

---

### 交换图表 (Commutative Diagram)

我们可以将同态分解表达为如下可交换图表：

$$\begin{array}{ccc}
G & \xrightarrow{\quad\phi\quad} & G' \\
\pi \downarrow & & \uparrow \iota \\
G/\ker(\phi) & \xrightarrow{\quad\Phi\quad} & \text{Im}(\phi)
\end{array}$$

其中：
- $\pi: G \to G/\ker(\phi)$ 为自然商同态（$\pi(g) = g \cdot \ker(\phi)$）；
- $\Phi$ 为诱导的同构映射；
- $\iota: \text{Im}(\phi) \hookrightarrow G'$ 为包含单射。
即满足关系：$\phi = \iota \circ \Phi \circ \pi$。

---

### 符号解释表

| 符号 | 含义 | 取值范围/量纲 | 备注 |
|:---:|:---|:---|:---|
| $\phi: G \to G'$ | 群同态映射 | 函数 mapping | 满足 $\phi(ab) = \phi(a)\phi(b)$ |
| $\ker(\phi)$ | 同态核 (Kernel) | $G$ 的正规子群 | $\ker(\phi) = \{g \in G \mid \phi(g) = e'\}$ |
| $\text{Im}(\phi)$ | 同态像 (Image) | $G'$ 的子群 | $\text{Im}(\phi) = \{\phi(g) \mid g \in G\}$ |
| $\cong$ | 群同构 (Isomorphism) | 代数等价关系 | 表示两群结构完全一模一样 |

---

## 6. 推导思路和思想来源

- **推导主线（三步验证法）**:
  1. **第一步：证明 $\ker(\phi) \triangleleft G$（核必定是正规子群）**
     - 任取 $k \in \ker(\phi)$ 和 $g \in G$，验证 $g k g^{-1} \in \ker(\phi)$：
       $$ \phi(g k g^{-1}) = \phi(g) \phi(k) \phi(g^{-1}) = \phi(g) \cdot e' \cdot (\phi(g))^{-1} = \phi(g) (\phi(g))^{-1} = e' $$
     - 由正规子群判定条件，$\ker(\phi) \triangleleft G$ 必成立！
  2. **第二步：验证映射 $\Phi(g \cdot \ker(\phi)) = \phi(g)$ 的良定义性 (Well-defined)**
     - 设 $g_1 \cdot \ker(\phi) = g_2 \cdot \ker(\phi)$，则 $g_1^{-1} g_2 \in \ker(\phi)$；
     - 计算 $\phi(g_1^{-1} g_2) = e' \implies (\phi(g_1))^{-1} \phi(g_2) = e' \implies \phi(g_1) = \phi(g_2)$；
     - 故 $\Phi(g_1 \cdot \ker(\phi)) = \Phi(g_2 \cdot \ker(\phi))$，无任何歧义！
  3. **第三步：证明 $\Phi$ 是同构映射**
     - **单射**: $\Phi(g_1 \ker\phi) = \Phi(g_2 \ker\phi) \implies \phi(g_1) = \phi(g_2) \implies \phi(g_1^{-1} g_2) = e' \implies g_1 \ker\phi = g_2 \ker\phi$；
     - **满射**: 对任意 $y \in \text{Im}(\phi)$，必存在 $x \in G$ 使 $\phi(x) = y$，故 $\Phi(x \ker\phi) = y$；
     - **保持运算**: $\Phi( (a \ker\phi) (b \ker\phi) ) = \Phi( (ab) \ker\phi ) = \phi(ab) = \phi(a) \phi(b) = \Phi(a \ker\phi) \Phi(b \ker\phi)$。
  4. 综上，$G / \ker(\phi) \cong \text{Im}(\phi)$ 完美得证！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（模 $n$ 自然商同态）
- **题目**: 考虑整数加法群 $\mathbb{Z}$ 和模 $n$ 加法群 $\mathbb{Z}_n$。定义映射 $\phi: \mathbb{Z} \to \mathbb{Z}_n$ 为 $\phi(m) = m \bmod n$。
  1. 验证 $\phi$ 是满同态；
  2. 求同态核 $\ker(\phi)$；
  3. 利用同态基本定理验证商群。

- **解题分析与过程**:
  1. **同态验证**: $\phi(a + b) = (a + b) \bmod n = (a \bmod n +_n b \bmod n) = \phi(a) +_n \phi(b)$。满同态 ($\text{Im}(\phi) = \mathbb{Z}_n$)；
  2. **求同态核**: $\ker(\phi) = \{ m \in \mathbb{Z} \mid m \bmod n = 0 \} = n\mathbb{Z} = \{\dots, -2n, -n, 0, n, 2n, \dots\}$；
  3. **套用第一同态定理**:
     $$ \mathbb{Z} / \ker(\phi) \cong \text{Im}(\phi) \implies \mathbb{Z} / n\mathbb{Z} \cong \mathbb{Z}_n $$
- **结论**: 模 $n$ 剩余类群 $\mathbb{Z}_n$ 本质上就是整数群 $\mathbb{Z}$ 关于 $n\mathbb{Z}$ 的商群！

---

### 例子 2：中等例子（对称群 $S_n$ 奇偶置换同态）
- **题目**: 设 $S_n$ 为 $n$ 阶置换对称群 ($n \ge 2$)。定义符号映射 $\text{sgn}: S_n \to \{1, -1\}$（偶置换映射为 1，奇置换映射为 -1，目标群运算为实数乘法）。
  1. 求同态核 $\ker(\text{sgn})$；
  2. 应用同态基本定理计算偶置换交错群 $A_n$ 的阶数。

- **解答过程**:
  1. $\text{sgn}$ 是满同态（$\text{Im}(\text{sgn}) = \{1, -1\}$，阶数为 2）；
  2. **同态核**: $\ker(\text{sgn}) = \{ \sigma \in S_n \mid \text{sgn}(\sigma) = 1 \}$，这正是所有**偶置换**构成的子群——**交错群 (Alternating Group $A_n$)**！
  3. 由第一同态定理：$A_n = \ker(\text{sgn}) \triangleleft S_n$，且：
     $$ S_n / A_n \cong \{1, -1\} \cong \mathbb{Z}_2 $$
  4. 计算阶数：$|S_n / A_n| = \frac{|S_n|}{|A_n|} = 2 \implies |A_n| = \frac{|S_n|}{2} = \frac{n!}{2}$。
- **结论**: 偶置换的个数恰好占全置换的一半（$\frac{n!}{2}$），且 $A_n \triangleleft S_n$。

---

### 例子 3：实际应用例子
- **真实场景**: **矩阵行列式与高维体积缩放**
  考虑全体 $n \times n$ 实数可逆矩阵构成的乘法群 $GL_n(\mathbb{R})$。定义行列式映射：
  $$ \det: GL_n(\mathbb{R}) \to \mathbb{R}^* \quad (\det(A B) = \det(A) \det(B)) $$
  - **同态分析**:
    1. $\det$ 是从矩阵乘法群到非零实数乘法群 $\mathbb{R}^*$ 的满同态；
    2. 同态核 $\ker(\det) = \{ A \in GL_n(\mathbb{R}) \mid \det(A) = 1 \} = SL_n(\mathbb{R})$ （特殊线性群）；
    3. 由同态基本定理直接得出：
       $$ GL_n(\mathbb{R}) / SL_n(\mathbb{R}) \cong \mathbb{R}^* $$
  - **物理与几何意义**:
    忽略所有“保持体积不变”的复杂高维剪切与旋转变化（商掉 $SL_n(\mathbb{R})$），庞大的高维矩阵群 $GL_n(\mathbb{R})$ 剩余的代数骨架仅仅是一维空间中的**体积缩放倍率**（同构于非零实数乘法群 $\mathbb{R}^*$）！

---

## 8. 常见误区和易混概念

### 常见误区

#### 误区 1：混淆“群同态 (Homomorphism)”与“群同构 (Isomorphism)”
- **错误直觉**: “同态基本定理证明了 $G$ 和 $G'$ 是完全相同的。”
- **为什么错**: 同态 $\phi$ 可以降维压缩（多对一）；同构 $\Phi$ 才是无损双射（一对一）。
- **正确理解**: 同态基本定理证明的是 $G$ **消去核之后形成的商群 $G/\ker(\phi)$** 与像集 $\text{Im}(\phi)$ 同构，而不是 $G$ 自身与 $G'$ 同构！

#### 误区 2：以为任意子群都能充当某个同态的核
- **错误直觉**: “随便选一个子群 $H \le G$，都能找到一个同态映射使得 $\ker(\phi) = H$。”
- **为什么错**: 第一同态定理证明了**只有正规子群 ($N \triangleleft G$)** 才能充当同态的核！如果是普通非正规子群，没有任何群同态能以它为核。
- **正确规则**: **同态核 $\iff$ 正规子群**（两者互为充要条件）。

### 易混概念对比

| 代数映射概念 | 定义与约束 | 映射类型 | 作用 |
|:---|:---|:---|:---|
| **群同态 (Homomorphism)** | $\phi(ab) = \phi(a)\phi(b)$ | 可单可满可多对一 | 保运算的模糊投影 |
| **同态核 $\ker(\phi)$** | $\{g \in G \mid \phi(g) = e'\}$ | **必为正规子群** | 记录同态中被压碎的细节 |
| **群同构 (Isomorphism)** | 双射同态 | 一对一保持结构的双射 | 两群代数本质完全等价 |
| **第一同态定理** | $G/\ker(\phi) \cong \text{Im}(\phi)$ | 结构定理 | 将投影结果与原群商结构精准挂钩 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[正规子群与商群]]: 同态核必然是正规子群，商群是定理的左半部分。
- [[群定义]]: 群同态映射的作用基础。

### 下游延伸
- [[理想与商环]]: 环论第一同态定理 $R/\ker(\phi) \cong \text{Im}(\phi)$ 的直接衍生。
- [[单群]]: 同态核只有 $\{\text{id}\}$ 和自身的群。

### 横向关联
- [[RSA加密]] ↔ [[群同态基本定理]]: 模 $n$ 剩余类同态与 RSA 同态加密的基础。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
1. 用一句话说明群同态基本定理揭示了什么核心代数规律。
2. 用“皮影戏投射”直觉解释 $G/\ker(\phi) \cong \text{Im}(\phi)$。
3. 准确写出第一同态定理的三大推论。
4. 写出自然商同态与诱导同构映射的表达式。
5. 证明同态核 $\ker(\phi)$ 必定是正规子群。
6. 为什么任意子群不一定能充当某个同态的核？
7. 举例说明符号映射 $\text{sgn}: S_n \to \{1, -1\}$ 应用同态基本定理的过程。
8. 区分“群同态”与“群同构”的区别。
9. 解释矩阵行列式同态 $GL_n(\mathbb{R}) / SL_n(\mathbb{R}) \cong \mathbb{R}^*$ 的几何含义。
10. 画出同态分解的可交换图表。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
|:---:|:---:|:---:|:---|
| 1 | 概念辨析 | 基础 | 同态核的正规性与像集子群性质 |
| 2 | 公式运用 | 基础 | 利用同态基本定理计算商群阶数 |
| 3 | 条件判断 | 中等 | 判定给定子群能否作为某个群同态的核 |
| 4 | 变式/综合 | 中等 | 构造同态证明复数乘法群与旋转群同构 |
| 5 | 开放/证明 | 较难 | 详细证明诱导映射 $\Phi(g \ker\phi) = \phi(g)$ 的单射性与满射性 |

### 题目 1
关于群同态映射 $\phi: G \to G'$，下列说法**错误**的是：
A. 同态像 $\text{Im}(\phi)$ 必定是 $G'$ 的子群
B. 同态核 $\ker(\phi)$ 必定是 $G$ 的正规子群
C. 若 $\ker(\phi) = \{e_G\}$，则 $\phi$ 是单同态
D. 任意子群 $H \le G$ 都能作为某个同态的核

> [!question]- 答案解析
> **答案**: D
> **解析**: 根据群同态基本定理，一个子群能作为某个同态映射的核，当且仅当它是一个**正规子群** ($H \triangleleft G$)。普通非正规子群绝对无法充当同态核（D 错误）。A、B、C 均为正确的代数性质。
> **Obsidian 标签**: `#自测题 #基础 #同态核`

---

### 题目 2
已知 $\phi: G \to G'$ 是一个满同态映射。若 $|G| = 60$，且同态像 $|G'| = 12$，则同态核 $\ker(\phi)$ 的阶数为：
A. 5
B. 12
C. 48
D. 720

> [!question]- 答案解析
> **答案**: A
> **解析**: 由第一同态定理，若 $\phi$ 是满同态，则 $G/\ker(\phi) \cong G'$。
> 结合阶数公式：$|G/\ker(\phi)| = \frac{|G|}{|\ker(\phi)|} = |G'| \implies \frac{60}{|\ker(\phi)|} = 12 \implies |\ker(\phi)| = 5$。
> **Obsidian 标签**: `#自测题 #基础 #阶数计算`

---

### 题目 3
判断命题正误：若同态映射 $\phi: G \to G'$ 的同态核仅包含单位元（即 $\ker(\phi) = \{e_G\}$），则 $G$ 与其像集 $\text{Im}(\phi)$ 完全同构（$G \cong \text{Im}(\phi)$）。

> [!question]- 答案解析
> **答案**: 正确
> **解析**: 当 $\ker(\phi) = \{e_G\}$ 时，商群 $G/\ker(\phi) = G/\{e_G\} \cong G$。由第一同态定理 $G/\ker(\phi) \cong \text{Im}(\phi)$，立刻导出 $G \cong \text{Im}(\phi)$。此时映射 $\phi$ 称为单同态 (Monomorphism) 或同构嵌入。
> **Obsidian 标签**: `#自测题 #中等 #单同态`

---

### 题目 4
定义映射 $\phi: \mathbb{R} \to S^1$（其中 $\mathbb{R}$ 为实数加法群，$S^1$ 为复平面单位圆乘法群 $S^1 = \{e^{i\theta} \mid \theta \in \mathbb{R}\}$）为 $\phi(x) = e^{2\pi i x}$。
1. 证明 $\phi$ 是满同态；
2. 求 $\ker(\phi)$，并利用第一同态定理写出同构式。

> [!question]- 答案解析
> **答案**: 见下述过程
> **解析**:
> 1. **同态**: $\phi(x+y) = e^{2\pi i(x+y)} = e^{2\pi i x} \cdot e^{2\pi i y} = \phi(x) \cdot \phi(y)$。对任意 $e^{i\theta} \in S^1$，取 $x = \frac{\theta}{2\pi} \in \mathbb{R}$，有 $\phi(x) = e^{i\theta}$。故 $\phi$ 为满同态；
> 2. **求核**: $\ker(\phi) = \{ x \in \mathbb{R} \mid e^{2\pi i x} = 1 \} = \{ x \in \mathbb{R} \mid 2\pi x = 2k\pi, k \in \mathbb{Z} \} = \mathbb{Z}$（整数集）；
> 3. **同构式**: 由第一同态定理：
>    $$ \mathbb{R} / \mathbb{Z} \cong S^1 $$
>    （实数线段模掉整数周期后，拓扑与代数上正好封闭成一个单位圆周线！）。
> **Obsidian 标签**: `#自测题 #综合 #复数同态`

---

### 题目 5
详细证明：在群同态基本定理中，诱导映射 $\Phi: G/\ker(\phi) \to \text{Im}(\phi)$ （定义为 $\Phi(g \ker\phi) = \phi(g)$）是一个**单射 (Injective)**。

> [!question]- 答案解析
> **答案**: 见下述证明
> **解析**:
> 1. 设 $g_1 \ker(\phi)$ 和 $g_2 \ker(\phi)$ 为商群 $G/\ker(\phi)$ 中的两个陪集；
> 2. 假设它们的映射值相同，即 $\Phi(g_1 \ker\phi) = \Phi(g_2 \ker\phi)$；
> 3. 根据 $\Phi$ 的定义，有 $\phi(g_1) = \phi(g_2)$；
> 4. 在目标群 $G'$ 中两边右乘 $\phi(g_2)^{-1}$：
>    $$ \phi(g_1) (\phi(g_2))^{-1} = e' \implies \phi(g_1 g_2^{-1}) = e' $$
> 5. 根据同态核的定义，这意味着元素 $g_1 g_2^{-1} \in \ker(\phi)$；
> 6. 由陪集相等的充要条件（$a b^{-1} \in H \iff a H = b H$），可知：
>    $$ g_1 \ker(\phi) = g_2 \ker(\phi) $$
> 7. 结论：假设映射值相同，导出了输入陪集完全相同，故 $\Phi$ 必为单射。得证！
> **Obsidian 标签**: `#自测题 #证明 #较难 #单射证明`

---

## 12. 我的主动回忆区

## 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

## 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

## 我的错误与卡点
- 

## 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **归档目录**: `04-离散数学/02-核心深化/`
- **推荐关联笔记**: [[正规子群与商群]], [[群定义]], [[等价类]], [[商集]], [[理想与商环]]
- **建议标签**: `#学习 #离散数学 #代数结构 #群论 #同态 #同构 #正规子群 #商群 #群同态基本定理 #核心概念`
- **拆分建议**: 本篇为群论第一同态定理核心主卡（A类）。第二、第三同态定理可作为延伸补充，
