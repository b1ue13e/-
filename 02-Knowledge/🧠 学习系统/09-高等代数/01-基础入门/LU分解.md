---
type: study
topic: "LU分解"
course: "高等代数"
created: 2026-08-06
status: completed
difficulty: intermediate
concept: ["LU分解", "三角分解", "PA=LU", "消元乘子"]
stage_moc: "[[📐 第一阶段：线性方程组与矩阵]]"
upstream: ["[[线性方程组与高斯消元法]]", "[[矩阵运算]]"]
flow: knowledge
kind: concept
source: "Hefferon Linear Algebra Ch.1 + MIT 18.06SC Lec 4；数值细节参考 Trefethen & Bau Lecture 20-21"
source_url: "https://hefferon.net/linearalgebra/"
accessed: 2026-08-06
license: "CC BY-SA 4.0（Hefferon）；MIT OCW（18.06SC）"
tags: [高等代数, 线性代数, LU分解]
---

# LU分解

> **核心问题**：高斯消元的每一步"乘子"能否保存下来，把整个消元过程打包成一个可复用的分解 $A = LU$？

## 0. 学习边界

| 分类 | 评估 |
|:--|:--|
| 理由 | $A=LU$ 使"解一次方程 $O(n^3)$、解多个右端 $O(n^2)$"成为可能，是所有数值线性代数的起点 |
| 投入建议 | 必须能手算 3×3 的 LU 分解并说明乘子 $l_{ij}$ 的来历 |

## 1. 这个知识点解决什么问题？

高斯消元把 $A$ 变成上三角 $U$，等价于左乘一串初等矩阵 $E_k\cdots E_1 A = U$。把这些"消元记录"移到等式右边：$A = (E_k\cdots E_1)^{-1}U$。奇迹在于 $(E_k\cdots E_1)^{-1}$ 恰是一个**单位下三角矩阵** $L$，且 $L$ 的条目就是消元时使用的乘子。于是消元过程浓缩为恒等式 $A = LU$。

## 2. 它为什么重要？它有什么用？

- **解方程组**：$A\mathbf{x}=\mathbf{b}$ 变成 $L\mathbf{y}=\mathbf{b}$（前代）再 $U\mathbf{x}=\mathbf{y}$（回代），两步都是 $O(n^2)$。
- **多右端**：同一个 $A$ 配多个 $\mathbf{b}$ 时只分解一次（$O(n^3)$），每次求解 $O(n^2)$——这就是工程上不写 `inv(A)` 的原因。
- **行列式**：$\det A = \det U = u_{11}u_{22}\cdots u_{nn}$（无行交换时）。
- **矩阵逆**：$A^{-1} = U^{-1}L^{-1}$（三角矩阵求逆便宜）。
- **铺垫**：$A^TA$ 的 Cholesky 分解（阶段 IV）、QR/SVD 都是"分解思想"的延续。

## 3. 学它之前需要哪些前置知识？

1. [[线性方程组与高斯消元法|线性方程组与高斯消元法]]：消元步骤与初等矩阵（变换 = 左乘 $E$）。
2. [[矩阵运算|矩阵运算]]：矩阵乘法（结合律）与单位矩阵。

## 4. 定义复述

### 4.1 LU 分解的定义

对 $n\times n$ 矩阵 $A$（各阶顺序主子式非零，即消元过程中主元全不为零），存在唯一的**单位下三角矩阵** $L$（对角元全为 1）与**上三角矩阵** $U$，使

$$A = LU$$

### 4.2 算法：Doolittle（乘子记录法）

对 $A$ 做高斯消元，把第 $k$ 步"用第 $i$ 行消第 $j$ 行（$j>k$）"的乘子 $l_{jk} = \dfrac{a^{(k)}_{jk}}{a^{(k)}_{kk}}$ 记入 $L$ 的 $(j,k)$ 位置，$U$ 就是消元结果。

例：

$$A = \begin{bmatrix} 2 & 1 & 1 \\ 4 & 3 & 3 \\ 8 & 7 & 9 \end{bmatrix} \xrightarrow{r_2-2r_1,\ r_3-4r_1} \begin{bmatrix} 2 & 1 & 1 \\ 0 & 1 & 1 \\ 0 & 3 & 5 \end{bmatrix} \xrightarrow{r_3-3r_2} \begin{bmatrix} 2 & 1 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 2 \end{bmatrix} = U$$

乘子为 $l_{21}=2, l_{31}=4, l_{32}=3$，故

$$L = \begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ 4 & 3 & 1 \end{bmatrix},\qquad A = LU$$

**验证**：$LU$ 的第 $(2,1)$ 元 $= 2\cdot 2 + 1\cdot 0 + 0 = 4$ ✓；第 $(3,2)$ 元 $= 4\cdot 1 + 3\cdot 1 + 1\cdot 0 = 7$ ✓。

### 4.3 带行交换：$PA = LU$

若消元中出现零主元，用**置换矩阵** $P$ 记录换行：$PA = LU$（$P$ 是单位矩阵的行置换，满足 $P^{-1}=P^T$）。例：$A=\begin{bmatrix}0&1\\1&1\end{bmatrix}$ 第一主元为 0，交换得 $P=\begin{bmatrix}0&1\\1&0\end{bmatrix}$，$PA=\begin{bmatrix}1&1\\0&1\end{bmatrix}=LU$。

### 4.4 LDU 变体

$U$ 再提取对角元 $D$：$A = LDU'$（$L$ 单位下三角、$D$ 对角、$U'$ 单位上三角）。对称正定矩阵的 $LDL^T$ 分解是 Cholesky 的变体（阶段 IV）。

## 5. 直觉与图像

- $L$ 是"消元的流水账"：$l_{ij}$ 记录第 $j$ 个方程被第 $i$ 行消掉时的倍数。
- $U$ 是"消元后的成品"：上三角系统可直接回代。
- 一句话：**LU 分解 = 把高斯消元的内存保存下来，供所有右端复用。**

> **一句话本质**：$A=LU$ 是"高斯消元作为矩阵恒等式"——算法即分解。

## 6. 定理陈述与证明重建

### 定理：无行交换时 $A=LU$ 分解唯一（Hefferon/MIT 18.06）

**前提**：$A$ 的消元主元全非零。

**结论**：存在唯一单位下三角 $L$ 与上三角 $U$ 使 $A=LU$。

**证明主线（存在性）**：消元得 $E_k\cdots E_1 A = U$，其中 $E_i$ 是单位下三角初等矩阵；$L = (E_k\cdots E_1)^{-1} = E_1^{-1}\cdots E_k^{-1}$。初等矩阵之逆仍是单位下三角，乘积仍为单位下三角（归纳验证）。$\square$

**证明主线（唯一性）**：设 $A=L_1U_1=L_2U_2$。则 $L_2^{-1}L_1 = U_2U_1^{-1}$。左边是单位下三角，右边是上三角，故两者都是对角阵；又左边对角元全为 1，故 $L_2^{-1}L_1=I$，即 $L_1=L_2$，进而 $U_1=U_2$。$\square$

**关键"转念"**："下三角 = 上三角"两边夹 → 对角阵，这个"形状论证"在矩阵分解理论中反复出现。

## 7. 经典反例库

### 反例 1：主元为零必须行交换

$A = \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix}$：无行交换无法 LU 分解（第一主元为 0），但 $PA=LU$ 存在。更一般地：任意可逆矩阵都有 $PA=LU$。

### 反例 2：不可逆矩阵也有 LU

$A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$：可分解为 $L=\begin{bmatrix}1&0\\2&1\end{bmatrix}, U=\begin{bmatrix}1&2\\0&0\end{bmatrix}$——LU 分解不要求 $A$ 可逆，只要求主元非零。

### 反例 3：数值稳定性——小主元污染 $L$

$A = \begin{bmatrix} \varepsilon & 1 \\ 1 & 1 \end{bmatrix}$（$\varepsilon$ 很小）：$l_{21}=1/\varepsilon$ 巨大，$U$ 与 $L$ 条目量级失衡，浮点误差被放大。列主元 $PA=LU$ 通过换行缓解（Trefethen & Bau Lec 21）。

## 8. 条件变式

| 变式方向 | 具体变化 | 影响 |
|:--|:--|:--|
| 弱化：非方阵 $m\times n$ | $L$ 为 $m\times m$，$U$ 为 $m\times n$ | 分解仍成立（行数 ≤ 列数时） |
| 加强：对称正定 | $A = LL^T$（Cholesky） | 计算量减半，数值稳定（阶段 IV） |
| 换结构：对称不定 | $A = LDL^T$ | 避免开方，用于二次型（阶段 IV） |
| 换目标：三对角矩阵 | 追赶法（Thomas 算法） | $O(n)$ 而非 $O(n^3)$ |

## 9. 相关知识点与 Obsidian 双链建议

- [[线性方程组与高斯消元法|线性方程组与高斯消元法]]、[[矩阵运算|矩阵运算]] — 上游
- [[逆矩阵与Gauss-Jordan消元|逆矩阵与 Gauss-Jordan 消元]] — 下游：$A^{-1}=U^{-1}L^{-1}$，工程上用 LU 求解不显式求逆
- [[矩阵的秩|矩阵的秩]] — 横向：$U$ 的非零行数即秩
- [[矩阵运算|矩阵运算]] — 上游：舒尔补与分块 LDU 推导（1.3 进阶）
- 阶段 IV：[[正定矩阵与二次型|Cholesky 分解]]、[[QR分解|QR 分解]]

## 10. 闭卷验收（数学模式）

- [ ] **定义默写**：LU 分解定义与唯一性条件；$PA=LU$ 的 $P$ 是什么。
- [ ] **算法执行**：手算 3×3 矩阵的 LU 分解并验证 $A=LU$。
- [ ] **定理证明**：证明唯一性（"下三角=上三角 ⇒ 对角阵"论证）。
- [ ] **应用**：用 LU 解 $A\mathbf{x}=\mathbf{b}$ 两步流程；说明为何多右端时 LU 优于 Gauss-Jordan。

## 11. 分级习题

| 等级 | 题目 | 来源 |
|:--|:--|:--|
| ★ | 求 $\begin{bmatrix}2&4\\1&3\end{bmatrix}$ 的 LU 分解 | MIT 18.06 Lec 4 |
| ★★ | 用 LU 分解解 $A\mathbf{x}=\mathbf{b}$，$A=\begin{bmatrix}2&1\\1&1\end{bmatrix}$，$\mathbf{b}=(3,2)^T$ | Hefferon §1.4 |
| ★★★ | 证明：$\det A = u_{11}u_{22}\cdots u_{nn}$（无行交换时） | MIT 18.06 PS3 |
| ★★★★ | 对 $A=\begin{bmatrix}\varepsilon&1\\1&1\end{bmatrix}$ 分析列主元 LU 与朴素 LU 的稳定性差异 | Trefethen & Bau Lec 21 |

## 12. 我的主动回忆区

<details>
<summary>🔄 核对要点（先默写，再展开比对）</summary>


- [ ] **定义默写**：LU 分解定义与唯一性条件；$PA=LU$ 的 $P$ 是什么。
- [ ] **算法执行**：手算 3×3 矩阵的 LU 分解并验证 $A=LU$。
- [ ] **定理证明**：证明唯一性（"下三角=上三角 ⇒ 对角阵"论证）。
- [ ] **应用**：用 LU 解 $A\mathbf{x}=\mathbf{b}$ 两步流程；说明为何多右端时 LU 优于 Gauss-Jordan。

</details>

> 不看上文：写出 Doolittle 算法；手算 3×3 LU；证明唯一性；解释 $PA=LU$ 中 $P$ 的来历。

## 13. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---
*创建于：2026-08-06 | 来源：Hefferon Ch.1 + MIT 18.06SC Lec 4 + Trefethen & Bau Lec 20-21（数值补充）*

