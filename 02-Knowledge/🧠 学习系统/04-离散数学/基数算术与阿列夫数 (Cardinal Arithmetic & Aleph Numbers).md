---
type: concept
topic: 基数算术与阿列夫数
created: 2026-07-28
status: learning
difficulty: advanced
concept:
- 基数算术
- 阿列夫数
- 连续统基数
- 连续统假设
prerequisites:
- '[[等势]]'
- '[[可数集]]'
- '[[康托定理]]'
related:
- '[[不可数集]]'
- '[[幂集]]'
tags:
- 学习
- 离散数学
- 集合论
- 基数
- 基数算术
- 阿列夫数
- 连续统假设
- 康托定理
title: 基数算术与阿列夫数
date: 2026-07-28
updated: 2026-07-28
kind: concept
flow: knowledge
course: 离散数学
importance: A
upstream:
- '[[等势]]'
- '[[可数集]]'
- '[[不可数集]]'
- '[[康托定理]]'
downstream:
- '[[Zorn勒马与选择公理]]'
- '[[幂集]]'
stage: 📐 第一阶段：基础奠基 (Foundation)
module: 集合论与基数
---

# 基数算术与阿列夫数 (Cardinal Arithmetic & Aleph Numbers)

## 0. 先判断它值不值得深挖

- **分类结果**: **A 类（核心概念，必须深挖）**
- **分类理由**: 基数算术（Cardinal Arithmetic）与阿列夫数（Aleph Numbers）由集合论奠基人格奥尔格·康托尔 (Georg Cantor) 创立。它打破了人类数千年来认为“无穷大只是一个无法达到的极限概念”的认知瓶颈，建立了严密的“超越有限”的**无限大算术阶梯**。它精确定义了可数无穷 $\aleph_0$ 与连续统无穷 $\mathfrak{c}$，给出了无穷集合的加法、乘法与幂运算法则。它是现代实变函数、拓扑学、超限归纳法以及逻辑学连续统假设 (CH) 的基石。

---

## 1. 这个知识点解决什么问题？

**我们遇到了什么麻烦？**

对于有限集合，比较大小非常直观：通过数自然数 $1, 2, 3 \dots$ 即可。然而当面对无限集合时，直觉开始彻底失效：
- 自然数集 $\mathbb{N}$ 和 偶数集 $2\mathbb{N}$ 哪个元素更多？（偶数明明只是自然数的一部分！）
- 正方形内部的点 $(x, y)$ 和 一条线段上的点 $x$ 哪个更多？
- 所有的“无限大”都是一样大的吗？

如果只停留在口头“无限大”的泛泛描述，数学就无法精确度量离散世界与连续空间的维度特征。

为了**形式化度量并计算无限集合的精确“元素个数（势 / 基数）”**，康托尔建立了 **基数算术与阿列夫数系统**。

---

## 2. 为什么它重要？它有什么用？

- **课程大图景位置**: 集合论从有限向无限跨越的理论顶峰，连接双射映射、不可数集与选择公理。
- **后续知识支撑**:
  - [[康托定理]]: 基数意义下的 $2^\kappa > \kappa$ 幂集基数递增定理；
  - [[Zorn勒马与选择公理]]: 超限序数 (Ordinal) 与超限基数 (Cardinal) 的良序化推导；
  - **实变函数与测度论**: 零测集与可数集、连续统集的关系。
- **实战与跨学科应用**:
  - **理论计算机科学**: 证明“可计算的程序总数”是可数无穷 $\aleph_0$，而“所有可能的数学问题/语言总数”是不可数无穷 $2^{\aleph_0} = \mathfrak{c}$！由此从基数角度深刻证明了**绝大多数问题都是绝对不可计算的**。

---

## 3. 学它之前需要哪些前置知识？

- **等势 (Equinumerosity)**: $A \sim B \iff$ 存在从 $A$ 到 $B$ 的双射映射 $f: A \to B$。
- **可数集与不可数集**: 了解 $|\mathbb{N}| = \aleph_0$ 以及实数集 $\mathbb{R}$ 的不可数性。
  - *最小必要背景速补*: **康托尔对角线画法**证明了 $[0, 1]$ 之间的实数无法与自然数建立一一对应，从而揭示了无限存在不同的“层级”。

---

## 4. 用直觉语言解释它

«“基数算术其实就是**无限世界的‘希尔伯特无限客栈’入住法则**。”»

假设希尔伯特开了一家有**无限多个房间**（$\aleph_0$ 个房间）的客栈，且已经全部客满：
1. **加法法则 ($\aleph_0 + 1 = \aleph_0$)**：来了一位新客人。经理让 1 号房搬到 2 号，2 号搬到 3 号……腾出了 1 号房。客人轻松入住！无限加上有限，基数依然是原来的无限；
2. **加法法则 ($\aleph_0 + \aleph_0 = \aleph_0$)**：来了无限多辆公交车，每辆车有无限多个客人。经理让老客人搬到偶数房（$2n$），腾出所有奇数房（$2n-1$）给新客人。所有人全部住下！
3. **乘法法则 ($\aleph_0 \cdot \aleph_0 = \aleph_0$)**：二维网格上的所有点，也可以通过蛇形穿梭一笔画一排开。
4. **指数暴涨法则 ($2^{\aleph_0} = \mathfrak{c} > \aleph_0$)**：给客栈每个房间设置硬币正反面。所有可能的房间状态组合（即幂集）达到了连续统 $\mathfrak{c}$，客栈彻底爆炸，再也装不下了！
- **直觉本质**: 在无穷基数运算中，“极大项”拥有绝对吞噬力 ($\kappa + \lambda = \kappa \cdot \lambda = \max(\kappa, \lambda)$)。

---

## 5. 正式定义、核心公式、符号解释

### 基数的正式定义与阿列夫数

1. **基数 (Cardinality / 势)**:
   每个集合 $A$ 被赋予一个代数标记记作 $|A|$（或 $\text{card}(A)$），满足 $|A| = |B| \iff A \sim B$（存在双射）。
2. **阿列夫数 (Aleph Numbers $\aleph_\alpha$)**:
   采用选择公理 (ZFC) 时，所有无限基数构成一个良序序列：
   $$ \aleph_0 < \aleph_1 < \aleph_2 < \dots < \aleph_\alpha < \dots $$
   - **$\aleph_0$ (阿列夫零)**：最小的无限基数，即自然数集的基数 $|\mathbb{N}| = \aleph_0$；
   - **$\mathfrak{c}$ (连续统基数, Continuum)**：实数集的基数 $|\mathbb{R}| = \mathfrak{c}$。由康托定理可知 $\mathfrak{c} = 2^{\aleph_0}$。

---

### 基数算术三大基本法则

设 $\kappa = |A|, \lambda = |B|$：

#### 1. 基数加法 (Cardinal Addition)
设 $A \cap B = \emptyset$，定义：
$$ \kappa + \lambda = |A \cup B| $$
- **无限加法吸性定理**: 若 $\kappa, \lambda$ 中至少有一个是无限基数，则：
  $$ \kappa + \lambda = \max(\kappa, \lambda) $$
  例如：$\aleph_0 + n = \aleph_0$, $\aleph_0 + \aleph_0 = \aleph_0$, $\mathfrak{c} + \aleph_0 = \mathfrak{c}$。

#### 2. 基数乘法 (Cardinal Multiplication)
定义：
$$ \kappa \cdot \lambda = |A \times B| $$ （笛卡尔积的势）
- **无限乘法吸收定理**: 若 $\kappa, \lambda$ 中至少有一个无限，且均非 0，则：
  $$ \kappa \cdot \lambda = \max(\kappa, \lambda) $$
  例如：$\aleph_0 \cdot \aleph_0 = \aleph_0$, $\mathfrak{c} \cdot \aleph_0 = \mathfrak{c}$, $\mathfrak{c} \cdot \mathfrak{c} = \mathfrak{c}$。

#### 3. 基数幂运算 (Cardinal Exponentiation)
定义 $B^A$ 为从 $A$ 到 $B$ 的所有映射构成的集合，则：
$$ \lambda^\kappa = |B^A| $$
- **常用幂运算恒等式**:
  1. $2^{|A|} = |\mathcal{P}(A)|$ （幂集的势）
  2. $(\lambda^\mu)^\kappa = \lambda^{\mu \cdot \kappa}$
  3. $\lambda^{\kappa_1 + \kappa_2} = \lambda^{\kappa_1} \cdot \lambda^{\kappa_2}$
  4. $(\lambda_1 \cdot \lambda_2)^\kappa = \lambda_1^\kappa \cdot \lambda_2^\kappa$

---

### 连续统假设 (Continuity Hypothesis, CH)

- **连续统假设 (CH)**: 不存在任何基数 $\lambda$ 满足 $\aleph_0 < \lambda < 2^{\aleph_0}$。即：
  $$ 2^{\aleph_0} = \aleph_1 $$
- **独立性结果 (Gödel & Cohen)**:
  - 1938 年哥德尔证明了：在 ZFC 集合论中**无法证明 CH 为假**；
  - 1963 年保罗·科恩 (Paul Cohen) 发明力迫法 (Forcing) 证明了：在 ZFC 中**无法证明 CH 为真**；
  - **结论**: 连续统假设在 ZFC 集合论系统中是**绝对独立（不可判定）**的！

---

### 符号解释表

| 符号 | 含义 | 取值范围/量纲 | 备注 |
|:---:|:---|:---|:---|
| $\aleph_0$ | 阿列夫零 | 可数无穷基数 | $|\mathbb{N}| = |\mathbb{Z}| = |\mathbb{Q}| = \aleph_0$ |
| $\mathfrak{c}$ 或 $2^{\aleph_0}$ | 连续统基数 | 实数集的基数 | $|\mathbb{R}| = |[0,1]| = |\mathbb{R}^n| = \mathfrak{c}$ |
| $\kappa + \lambda$ | 基数加法 | 基数 | 不相交并集之势 |
| $\kappa \cdot \lambda$ | 基数乘法 | 基数 | 笛卡尔积之势 |
| $\lambda^\kappa$ | 基数幂运算 | 基数 | 映射集 $B^A$ 之势 |

---

## 6. 推导思路和思想来源

- **困难与动机**: 传统的有限算术律（如 $a + a = 2a \ne a$）在无穷面前失效。
- **关键转念**: 抛弃数值大小，回归**映射与双射**！只要能构造出双射映射，两个集合的基数就严格相等。
- **核心公式推导主线**:
  1. **推导 $\aleph_0 \cdot \aleph_0 = \aleph_0$**：
     构造正整数对 $(m, n) \in \mathbb{N} \times \mathbb{N}$ 到一维正整数 $\mathbb{N}$ 的 Cantor 派对配对函数：
     $$ f(m, n) = \frac{(m + n - 2)(m + n - 1)}{2} + m $$
     证明该函数为双射，从而证明 $|\mathbb{N} \times \mathbb{N}| = \aleph_0$。
  2. **推导 $|\mathbb{R}| = 2^{\aleph_0}$**：
     - 每个区间 $[0, 1]$ 上的实数可以用二进制小数表示：$0.b_1 b_2 b_3 \dots$ （其中 $b_i \in \{0, 1\}$）；
     - 这天然对应了一个从 $\mathbb{N}$ 到 $\{0, 1\}$ 的特征映射 $f: \mathbb{N} \to \{0, 1\}$（即 $\{0, 1\}^{\mathbb{N}}$ 的元素）；
     - 结合 Cantor-Bernstein 定理处理重复尾数（如 $0.0111\dots = 0.1000\dots$），证明了 $|\mathbb{R}| = |\{0, 1\}^{\mathbb{N}}| = 2^{\aleph_0} = \mathfrak{c}$。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（Hilbert 无限客栈算术）
- **题目**: 计算以下无穷基数的值：
  1. $\aleph_0 + 2026$
  2. $\aleph_0 + \aleph_0$
  3. $\mathfrak{c} + \aleph_0$
  4. $\mathfrak{c} \cdot \mathfrak{c}$
- **解答过程**:
  利用基数吸收定理 $\kappa + \lambda = \kappa \cdot \lambda = \max(\kappa, \lambda)$：
  1. $\aleph_0 + 2026 = \max(\aleph_0, 2026) = \aleph_0$
  2. $\aleph_0 + \aleph_0 = \max(\aleph_0, \aleph_0) = \aleph_0$
  3. $\mathfrak{c} + \aleph_0 = \max(\mathfrak{c}, \aleph_0) = \mathfrak{c}$
  4. $\mathfrak{c} \cdot \mathfrak{c} = \max(\mathfrak{c}, \mathfrak{c}) = \mathfrak{c}$
- **结论解释**: 三维空间 $\mathbb{R}^3$ 中的点数等于一条线段 $\mathbb{R}^1$ 上的点数（均为 $\mathfrak{c} \cdot \mathfrak{c} \cdot \mathfrak{c} = \mathfrak{c}$），这曾让康托尔惊叹：“我看到了它，但我无法相信它！”

---

### 例子 2：中等例子（函数空间的基数计算）
- **题目**: 计算所有从 $\mathbb{R}$ 到 $\mathbb{R}$ 的函数构成的集合 $\mathcal{F} = \{f \mid f: \mathbb{R} \to \mathbb{R}\}$ 的基数 $|\mathcal{F}|$。
- **完整解答过程**:
  1. 根据基数幂运算定义，$|\mathcal{F}| = |\mathbb{R}|^{|\mathbb{R}|} = \mathfrak{c}^{\mathfrak{c}}$；
  2. 将 $\mathfrak{c} = 2^{\aleph_0}$ 代入：
     $$ \mathfrak{c}^{\mathfrak{c}} = (2^{\aleph_0})^{\mathfrak{c}} = 2^{\aleph_0 \cdot \mathfrak{c}} $$
  3. 运用乘法吸收律 $\aleph_0 \cdot \mathfrak{c} = \max(\aleph_0, \mathfrak{c}) = \mathfrak{c}$：
     $$ 2^{\aleph_0 \cdot \mathfrak{c}} = 2^{\mathfrak{c}} $$
  4. 由康托定理可知 $2^{\mathfrak{c}} > \mathfrak{c}$。
- **最终答案**: 全体实函数的基数为 $2^{\mathfrak{c}}$（比连续统 $\mathfrak{c}$ 更高级别的无穷！）。

---

### 例子 3：实际应用例子
- **真实场景**: **图灵机程序总数与不可计算语言总数的基数对比**
  在理论计算机科学中，我们要探讨“计算机的能力极限”。
  - **程序总数计算**:
    任何 C 语言程序、Python 代码或图灵机可以看作是有限字母表 $\Sigma$ 上的有限长字符串。
    所有可能代码构成的集合 $\Sigma^*$ 是一个**可数集**，其基数为 $\aleph_0$。
    这意味着：**人类能编写出的所有程序总数只有 $\aleph_0$ 个**。
  - **问题（语言）总数计算**:
    一个判定问题（语言）是 $\Sigma^*$ 的一个子集。因此所有判定问题的集合是 $\mathcal{P}(\Sigma^*)$（幂集）。
    所有可能问题的总数为 $|\mathcal{P}(\Sigma^*)| = 2^{\aleph_0} = \mathfrak{c}$！
  - **基数对比结论**:
    因为可计算程序总数（$\aleph_0$）远小于存在的问题总数（$\mathfrak{c}$），由鸽巢原理可得：**绝大多数问题在数学上是绝对不存在任何解法程序的（不可计算）**！

---

## 8. 常见误区和易混概念

### 常见误区

#### 误区 1：认为有限算术中的消去律在基数加法中成立
- **错误直觉**: “因为 $\aleph_0 + 5 = \aleph_0 + 10$，两边消去 $\aleph_0$，所以 $5 = 10$。”
- **为什么错**: 无限基数加法**不满足消去律**！当 $\kappa$ 是无限基数时，$\kappa + a = \kappa + b$ 推不出 $a = b$。
- **正确理解**: 基数算术遵从吸收律，一旦引入无限，有限项细节将被完全吞噬。

#### 误区 2：以为多维空间 $\mathbb{R}^n$ 的点数比一维 $\mathbb{R}^1$ 多
- **错误直觉**: “二维平面 $\mathbb{R}^2$ 的点肯定比一维线段 $\mathbb{R}$ 包含更多的点。”
- **为什么错**: 康托尔证明了存在从 $[0, 1]$ 到 $[0, 1] \times [0, 1]$ 的双射映射！
- **正确理解**: $|\mathbb{R}^n| = \mathfrak{c}^n = (2^{\aleph_0})^n = 2^{n \cdot \aleph_0} = 2^{\aleph_0} = \mathfrak{c}$。一维、二维到任意有限 $n$ 维连续空间的基数完全相等，均为连续统 $\mathfrak{c}$！

### 易混概念对比

| 集合 / 符号 | 基数记号 | 具体代表集合 | 典型特征 |
|:---|:---|:---|:---|
| **有限集 (Finite)** | $n \in \mathbb{N}$ | $\{1, 2, \dots, n\}$ | 满足传统有限算术与消去律 |
| **可数无穷 (Countable)** | $\aleph_0$ | $\mathbb{N}, \mathbb{Z}, \mathbb{Q}$, 计算机程序总数 | 能与自然数建立一一对应排序 |
| **连续统 (Continuum)** | $\mathfrak{c} = 2^{\aleph_0}$ | $\mathbb{R}, \mathbb{R}^n, [0, 1]$, 判定问题总数 | 无法被可数穷举，对角线切断 |
| **高阶幂集无穷** | $2^{\mathfrak{c}}$ | 所有实函数集 $\mathcal{F}$, $\mathcal{P}(\mathbb{R})$ | 比连续统更高层级的无穷大 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[等势]]: 基数相等的判定标准依托。
- [[可数集]], [[不可数集]]: 两个最基础的无限基数代表。
- [[康托定理]]: 证明 $2^\kappa > \kappa$ 的基数递增核心定理。

### 下游延伸
- [[Zorn勒马与选择公理]]: 超限基数能进行全序比较（任何两基数必可比 $\kappa \le \lambda \lor \lambda \le \kappa$）依赖选择公理。
- [[幂集]]: 幂集运算导出下一个阿阶基数。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
1. 用一句话说明基数算术打破了什么传统认知。
2. 用“希尔伯特客栈”直觉解释 $\aleph_0 + \aleph_0 = \aleph_0$。
3. 写出无限基数加法与乘法的吸收律公式。
4. 什么是阿列夫零 $\aleph_0$ 与连续统基数 $\mathfrak{c}$？写出两者的关系。
5. 准确写出基数幂运算的 4 个代数恒等式。
6. 简述什么是连续统假设 (CH) 及其在 ZFC 中的独立性含义。
7. 证明全实函数集合的基数为 $2^{\mathfrak{c}}$。
8. 列举关于基数消去律和多维空间点数的两个常见误区。
9. 解释为什么从基数角度看“绝大多数问题都是不可计算的”。
10. 证明三维空间 $\mathbb{R}^3$ 的基数等于 $\mathbb{R}$ 的基数。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
|:---:|:---:|:---:|:---|
| 1 | 概念辨析 | 基础 | 常见集合基数的识别与比较 |
| 2 | 公式运用 | 基础 | 利用吸收律计算基数混合表达式 |
| 3 | 条件判断 | 中等 | 基数幂运算与真子集包含关系 |
| 4 | 变式/综合 | 中等 | 计算有理数序列与实数序列集的基数 |
| 5 | 开放/证明 | 较难 | 利用基数算术证明 $2^{\aleph_0} \cdot 2^{\aleph_0} = 2^{\aleph_0}$ |

### 题目 1
下列集合中，基数为连续统 $\mathfrak{c}$ 的是：
A. 所有有理数构成的集合 $\mathbb{Q}$
B. 所有计算机 C 语言源程序构成的集合
C. 区间 $(0, 1)$ 内的所有实数构成的集合
D. 所有代数数（有理系数多项式的根）构成的集合

> [!question]- 答案解析
> **答案**: C
> **解析**: 实数区间 $(0, 1)$ 与全实数集 $\mathbb{R}$ 等势，基数为连续统 $\mathfrak{c} = 2^{\aleph_0}$。有理数集 $\mathbb{Q}$、C 语言程序集以及代数数集均为可数集（基数均为 $\aleph_0$）。
> **最可能错因**: 误以为代数数或程序集是不可数的。
> **Obsidian 标签**: `#自测题 #基础 #基数`

---

### 题目 2
已知 $\kappa = \aleph_0, \lambda = \mathfrak{c}$，计算基数表达式 $(\kappa + \lambda) \cdot \lambda^{\kappa}$ 的最终简化值。

> [!question]- 答案解析
> **答案**: $\mathfrak{c}$
> **解析**:
> 1. $\kappa + \lambda = \aleph_0 + \mathfrak{c} = \max(\aleph_0, \mathfrak{c}) = \mathfrak{c}$；
> 2. $\lambda^{\kappa} = \mathfrak{c}^{\aleph_0} = (2^{\aleph_0})^{\aleph_0} = 2^{\aleph_0 \cdot \aleph_0} = 2^{\aleph_0} = \mathfrak{c}$；
> 3. 代入乘法：$(\kappa + \lambda) \cdot \lambda^{\kappa} = \mathfrak{c} \cdot \mathfrak{c} = \mathfrak{c}$。
> **Obsidian 标签**: `#自测题 #基础 #基数算术`

---

### 题目 3
判断命题正误：若集合 $A \subset B$ 且 $A \ne B$（即 $A$ 为 $B$ 的真子集），则必有 $|A| < |B|$。

> [!question]- 答案解析
> **答案**: 错误
> **解析**: 这只对有限集成立！对无限集而言，**无限集可以与其真子集等势**（这正是 Dedekind 对无限集的定义）。例如偶数集 $2\mathbb{N}$ 是自然数集 $\mathbb{N}$ 的真子集，但 $|2\mathbb{N}| = |\mathbb{N}| = \aleph_0$。
> **最可能错因**: 用有限集的直觉套用无限集。
> **Obsidian 标签**: `#自测题 #中等 #易错点 #无限集`

---

### 题目 4
求解所有从自然数集 $\mathbb{N}$ 到 $\{0, 1, 2\}$ 的序列集合 $S = \{ (a_0, a_1, a_2, \dots) \mid a_i \in \{0, 1, 2\} \}$ 的基数 $|S|$。

> [!question]- 答案解析
> **答案**: $\mathfrak{c}$
> **解析**:
> 序列集合 $S$ 相当于映射集 $\{0, 1, 2\}^{\mathbb{N}}$。
> 其基数为 $3^{\aleph_0}$。
> 由于 $2 \le 3 \le 2^{\aleph_0}$，由基数夹逼可知：
> $$ 2^{\aleph_0} \le 3^{\aleph_0} \le (2^{\aleph_0})^{\aleph_0} = 2^{\aleph_0 \cdot \aleph_0} = 2^{\aleph_0} $$
> 因此 $3^{\aleph_0} = 2^{\aleph_0} = \mathfrak{c}$。
> **Obsidian 标签**: `#自测题 #中等 #基数计算`

---

### 题目 5
证明：二维实数平面 $\mathbb{R}^2$ 的基数等于一维实数轴 $\mathbb{R}$ 的基数（即证明 $\mathfrak{c} \cdot \mathfrak{c} = \mathfrak{c}$）。

> [!question]- 答案解析
> **答案**: 见下述证明
> **解析**:
> 1. 根据基数乘法定义，$|\mathbb{R}^2| = |\mathbb{R} \times \mathbb{R}| = \mathfrak{c} \cdot \mathfrak{c}$。
> 2. 将 $\mathfrak{c} = 2^{\aleph_0}$ 代入：
>    $$ \mathfrak{c} \cdot \mathfrak{c} = 2^{\aleph_0} \cdot 2^{\aleph_0} $$
> 3. 运用基数幂运算运算法则 $\lambda^{a} \cdot \lambda^{b} = \lambda^{a+b}$：
>    $$ 2^{\aleph_0} \cdot 2^{\aleph_0} = 2^{\aleph_0 + \aleph_0} $$
> 4. 运用无限加法吸收律 $\aleph_0 + \aleph_0 = \aleph_0$：
>    $$ 2^{\aleph_0 + \aleph_0} = 2^{\aleph_0} = \mathfrak{c} $$
> 5. 综上所述，$\mathfrak{c} \cdot \mathfrak{c} = \mathfrak{c}$，得证！二维平面与一维线段的点数完全相同。
> **Obsidian 标签**: `#自测题 #证明 #较难 #连续统`

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

- **归档目录**: `04-离散数学/01-基础奠基/`
- **推荐关联笔记**: [[等势]], [[可数集]], [[不可数集]], [[康托定理]], [[Zorn勒马与选择公理]], [[幂集]]
- **建议标签**: `#学习 #离散数学 #集合论 #基数 #基数算术 #阿列夫数 #连续统假设 #康托定理 #核心概念`
- **拆分建议**: 本篇为集合论最核心的概念主卡（A类）。选择公理与超
