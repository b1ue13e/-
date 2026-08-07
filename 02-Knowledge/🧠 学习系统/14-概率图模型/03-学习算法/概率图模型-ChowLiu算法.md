---
type: study
topic: "ChowLiu算法"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-学习算法]]"
flow: knowledge
kind: derivation
difficulty: intermediate
upstream: ["[[概率图模型-BN结构学习]]", "[[概率图模型-条件独立与d分隔]]"]
concept: ["Chow-Liu", "互信息", "最大生成树", "TAN"]
related: ["概率图模型-BN结构学习", "概率图模型-贝叶斯网络"]
tags: [概率图模型, ChowLiu, 树模型]
---

# 概率图模型-ChowLiu算法

> **Chow-Liu 算法**是结构学习的最优雅特例：当结构限制为**树**时，最优结构可由**互信息 + 最大生成树**闭式求出（$O(n^2)$ 复杂度）。本卡覆盖互信息、最大生成树、定根定向，以及扩展 TAN（树增强朴素贝叶斯）与森林模型。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：一般 DAG 结构学习是 NP-hard、需启发式搜索。但如果假设结构是**树**（每变量最多一个父节点），问题退化为可精确求解：最优树 = 使互信息之和最大的树 = 互信息最大生成树。这给出一个**有理论保证**的结构学习基线。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：Chow-Liu 是"限制结构换闭式解"的范式例子；树模型是复杂模型的简化代理（诊断、分类、概率密度估计）。
- **实际应用场景**：从数据学朴素贝叶斯的树增强（TAN 分类器）、高维密度估计、作为复杂学习的热启动。
- **高频考点**：互信息定义、KL 分解证明最优树、最大生成树（Prim/Kruskal）、树定向。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-BN结构学习]]**：评分-搜索框架。
2. **[[概率图模型-条件独立与d分隔]]**：树上的条件独立。
3. **[[概率图模型-图论基础]]**：树、生成树。

---

## 4. 定义与核心公式

### 4.1 互信息（Mutual Information）

**定义**：$I(X_i; X_j) = \sum_{x_i,x_j} P(x_i,x_j)\log\frac{P(x_i,x_j)}{P(x_i)P(x_j)} = \text{KL}(P(x_i,x_j) \parallel P(x_i)P(x_j)) \ge 0$。

**含义**：度量两个变量共享的信息量（$I = 0$ ⇔ 独立）。从数据估计：用频率计算（经验互信息）。

### 4.2 Chow-Liu 定理

**定理**：在所有以树为结构的 BN 中，使**对数似然最大**的树由**互信息最大生成树**给出。

**推导**：树结构 $T$ 的对数似然（MLE 下）：
$$\ell(T) = N\sum_{i,j\in T} I(X_i; X_j) - N\sum_i H(X_i) + \text{const}$$
（$H$ 为熵，与结构无关）。故最大化 $\ell$ ⇔ 最大化树边上的互信息和 ⇔ **最大生成树**（以 $I$ 为边权）。∎

### 4.3 算法步骤

1. **估计互信息**：对每对变量计算 $I(X_i; X_j)$（$O(n^2)$ 对）；
2. **最大生成树**：以 $I$ 为边权，用 Kruskal（贪心加最大权边、避免环）或 Prim 求最大生成树；
3. **定根定向**：任选根节点，沿树方向定向得 DAG（树的方向不影响独立性/似然，只影响表示）。

**复杂度**：$O(n^2 \cdot d^2)$（$d$ 取值数）+ $O(n^2\log n)$ 建树。

### 4.4 扩展

**TAN（树增强朴素贝叶斯）**：保留类变量 $C$ 到所有特征的边，特征之间用 Chow-Liu（**条件互信息** $I(X_i;X_j\mid C)$ 作权）学树。比朴素贝叶斯更灵活（允许特征间依赖）。

**森林模型（Forest）**：不要求连通，取互信息图的最大权森林（去掉最弱边）——稀疏化、可解释。

---

## 5. 关键推导

**推导：树似然的分解（Chow-Liu 定理核心）**。

树的 BN：$P_T(\mathbf{x}) = \prod_{i=1}^n P(x_{i}\mid x_{\text{pa}(i)})$，每变量恰一父（根无父）。取对数并按 MLE 代入，利用 $P(x_i,x_j) = P(x_i)P(x_j\mid x_i)$ 重组可得 $\ell(T) = N\sum_{(i,j)\in T} I(X_i;X_j) - N\sum_i H(X_i)$。熵项与 $T$ 无关，故最大化似然 = 最大化 $\sum_T I$。∎

**推导：TAN 用条件互信息的原因**。
TAN 的似然（给定类 $C$）：$\log P(\mathbf{x}, c) = \log P(c) + \log P(\mathbf{x}\mid c)$。特征树部分的似然展开为条件互信息和 $\sum I(X_i;X_j\mid C)$——条件于类，故特征间依赖权用条件互信息。∎

---

## 6. 最小可手算例子

**例（4 变量最大生成树）**：$n=4$，互信息矩阵（对称）：
- $I(A,B)=0.8$，$I(A,C)=0.3$，$I(A,D)=0.1$，$I(B,C)=0.6$，$I(B,D)=0.2$，$I(C,D)=0.4$。

**Kruskal**：按权降序加边、避免环：
1. 加 $A\text{-}B$（0.8）；
2. 加 $B\text{-}C$（0.6）；
3. 加 $C\text{-}D$（0.4）——完成连通 4 节点（3 条边），总和 $0.8+0.6+0.4 = 1.8$；
4. 其余边会成环，跳过。

**输出**：链 $A\text{-}B\text{-}C\text{-}D$，任选根（如 $A$）定向：$A \to B \to C \to D$。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| Chow-Liu 能找到一般 DAG | **错**。只限树结构；真实结构含环/多父时树近似有偏 |
| 最大生成树 = 全连接图 | **错**。MST 是 $n-1$ 条边的最优树，不是全连接 |
| 树方向影响结果 | **错**。同骨架的树方向变化不改变独立性/似然（等价类） |
| 互信息越大边越"因果" | **不精确**。互信息是相关性度量，无方向/因果含义 |
| TAN 就是朴素贝叶斯 | **错**。TAN 允许特征间条件依赖（树），NB 假设特征条件独立 |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出互信息定义。
2. Chow-Liu 分几步？复杂度如何？

### #自测题/中等
3. 用 §6 矩阵手算最大生成树（Kruskal）。
4. 推导：树似然 = $N\sum_T I - N\sum H$（给出主要步骤）。

### #自测题/较难
5. TAN 为什么用条件互信息 $I(X_i;X_j\mid C)$？与 Chow-Liu 的 $I(X_i;X_j)$ 区别何在？

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. $I(X;Y) = \sum P(x,y)\log\frac{P(x,y)}{P(x)P(y)}$。
2. 估计 MI → 最大生成树 → 定向；$O(n^2d^2 + n^2\log n)$。
3. 见 §6：$A\text{-}B\text{-}C\text{-}D$，和 1.8。
4. 树联合分解代入 MLE，重组为边互信息和 + 节点熵项；熵与结构无关。
5. 分类目标条件于类 $C$，特征间依赖度需在给定 $C$ 下衡量（否则类变量已解释的依赖被重复计数）。
</details>

---

## 9. 通过标准

- [ ] 能**默写**互信息、Chow-Liu 步骤与复杂度；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**手算**小规模最大生成树；
- [ ] 能**说明** TAN/森林与 Chow-Liu 的关系。

---

## 10. 来源

- Chow & Liu (1968). Approximating discrete probability distributions with dependence trees. *IEEE Trans. IT*.
- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Chapter 18.4.
- Friedman, Geiger & Goldszmidt (1997). Bayesian network classifiers. *Machine Learning*. 访问日期：2026-08-07。

---

## 11. 学完后可以完成

```dataview
LIST
FROM "03-Projects/14-概率图模型"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/14-概率图模型"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

> 直接下游：阶段 4 的 [[朴素贝叶斯]]/[[NB变体]]（树视角）、课程 Capstone（结构学习部分）。
