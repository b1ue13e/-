---
type: study
topic: "前向后向算法与BaumWelch"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段5-隐马尔可夫模型]]"
flow: knowledge
kind: derivation
difficulty: intermediate
upstream: ["[[概率图模型-隐马尔可夫模型HMM]]", "[[概率图模型-EM算法]]"]
concept: ["前向算法", "后向算法", "Baum-Welch", "EM"]
related: ["概率图模型-隐马尔可夫模型HMM", "概率图模型-Viterbi解码"]
tags: [概率图模型, HMM, 前向后向, BaumWelch]
anki_deck: "概率图模型::05-隐马尔可夫模型"
anki_tags: [概率图模型, HMM, 前向后向, BaumWelch]
---

# 概率图模型-前向后向算法与BaumWelch

> 本卡讲解 HMM **三大基本问题中的两个**：评估（前向/后向算法算 $P(O \mid \lambda)$）与学习（Baum-Welch 算法估计参数，它是 EM 在 HMM 上的特例）。维特比解码见 [[概率图模型-Viterbi解码]]。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：HMM 的参数 $\lambda = (A, B, \pi)$ 与观测序列 $O = (o_1, \dots, o_T)$ 已给，如何：
> 1. **评估**：计算观测序列概率 $P(O \mid \lambda)$（模型匹配度）？直接枚举隐状态序列是 $N^T$ 指数级；
> 2. **学习**：只有观测序列，如何估计 $A, B, \pi$（无监督学习）？隐状态未知。
> 前向/后向算法用**动态规划**解决评估；Baum-Welch（EM）用前向-后向量解决学习。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：前向算法是"链式 BP"在 HMM 的实例（见 [[概率图模型-和积算法与消息传递]]）；Baum-Welch 是 EM 的具体化（见 [[概率图模型-EM算法]]）；两者是语音识别、生物序列分析（HMMER）的核心引擎。
- **实际应用场景**：语音识别训练、基因/蛋白质序列家族建模、词性标注（HMM 版）。
- **高频考点**：前向/后向递推公式、Baum-Welch 更新公式、复杂度 $O(N^2T)$。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-隐马尔可夫模型HMM]]**：五元组、三大问题。
2. **[[概率图模型-EM算法]]**：Q 函数、E/M 步。
3. **[[概率图模型-和积算法与消息传递]]**：链上消息递推（前向=消息）。

---

## 4. 定义与核心公式

### 4.1 前向算法（评估 $P(O \mid \lambda)$）

**前向变量**：$\alpha_t(i) = P(o_1, \dots, o_t, q_t = s_i \mid \lambda)$——前 $t$ 个观测且 $t$ 时刻在状态 $s_i$ 的联合概率。

**递推**：
- 初始化：$\alpha_1(i) = \pi_i b_i(o_1)$
- 递推：$$\alpha_{t+1}(j) = b_j(o_{t+1}) \sum_{i=1}^{N} \alpha_t(i) a_{ij}$$
- 终止：$$P(O \mid \lambda) = \sum_{i=1}^{N} \alpha_T(i)$$

**复杂度**：$O(N^2 T)$（每步 $N^2$ 次乘加）。

### 4.2 后向算法

**后向变量**：$\beta_t(i) = P(o_{t+1}, \dots, o_T \mid q_t = s_i, \lambda)$——给定 $t$ 时刻状态，其后观测的概率。

**递推**：
- 初始化：$\beta_T(i) = 1$
- 递推：$$\beta_t(i) = \sum_{j=1}^{N} a_{ij} b_j(o_{t+1}) \beta_{t+1}(j)$$
- 终止：$P(O \mid \lambda) = \sum_i \pi_i b_i(o_1) \beta_1(i)$

### 4.3 Baum-Welch（EM 学习参数）

**定义辅助量**：
- **γ（状态占用）**：$\gamma_t(i) = P(q_t = s_i \mid O, \lambda) = \frac{\alpha_t(i)\beta_t(i)}{P(O\mid\lambda)}$；
- **ξ（转移占用）**：$\xi_t(i,j) = P(q_t = s_i, q_{t+1} = s_j \mid O, \lambda) = \frac{\alpha_t(i) a_{ij} b_j(o_{t+1}) \beta_{t+1}(j)}{P(O\mid\lambda)}$。

**更新公式（M 步）**：
$$\hat\pi_i = \gamma_1(i)$$
$$\hat a_{ij} = \frac{\sum_{t=1}^{T-1}\xi_t(i,j)}{\sum_{t=1}^{T-1}\gamma_t(i)}$$
$$\hat b_j(k) = \frac{\sum_{t: o_t = v_k}\gamma_t(j)}{\sum_{t=1}^{T}\gamma_t(j)}$$

**算法**：初始化 $\lambda$ → 前向-后向算 $\gamma, \xi$（E 步）→ 用上式更新（M 步）→ 迭代至似然收敛。它是 EM 在 HMM 的特例（隐状态 = 缺失数据）。

---

## 5. 关键推导

**推导：前向递推（概率的分解）**。

$\alpha_{t+1}(j) = P(o_{1:t+1}, q_{t+1}=s_j) = P(o_{1:t}, q_{t+1}=s_j) \cdot P(o_{t+1} \mid q_{t+1}=s_j)$（观测独立）
$= b_j(o_{t+1}) \sum_i P(o_{1:t}, q_t=s_i) \cdot P(q_{t+1}=s_j \mid q_t=s_i)$（对前态求和，齐次性）
$= b_j(o_{t+1}) \sum_i \alpha_t(i) a_{ij}$。∎

**推导：Baum-Welch = EM（E 步的 Q 函数）**。

完整数据对数似然 $Q(\lambda \mid \bar\lambda) = \sum_t \sum_i \gamma_t(i)\log\pi_i + \sum_t\sum_{i,j}\xi_t(i,j)\log a_{ij} + \sum_t\sum_i\gamma_t(i)\log b_i(o_t)$。最大化 $Q$（带 $\sum_j a_{ij}=1$ 等约束，拉格朗日）得 M 步更新公式——与 [[概率图模型-EM算法]] 的 GMM 更新同构。∎

**推导：复杂度 $O(N^2T)$**。
每步递推对每个 $j$ 做 $N$ 次求和 → $N^2$；共 $T$ 步 → $O(N^2T)$，远小于枚举 $O(N^T)$。∎

---

## 6. 最小可手算例子

**例（前向算法）**：$N=2$，$\pi = (0.5, 0.5)$，$A = \begin{pmatrix}0.7 & 0.3\\0.4 & 0.6\end{pmatrix}$，$B$（观测 $o \in \{0,1\}$）：$b_1(0)=0.9, b_1(1)=0.1$，$b_2(0)=0.2, b_2(1)=0.8$。观测 $O = (0, 1)$。

**$t=1$**：$\alpha_1(1) = 0.5\times0.9 = 0.45$；$\alpha_1(2) = 0.5\times0.2 = 0.10$。

**$t=2$**：
- $\alpha_2(1) = b_1(1)\sum_i\alpha_1(i)a_{i1} = 0.1\times(0.45\times0.7 + 0.10\times0.4) = 0.1\times0.355 = 0.0355$；
- $\alpha_2(2) = 0.8\times(0.45\times0.3 + 0.10\times0.6) = 0.8\times0.195 = 0.156$。

**$P(O) = 0.0355 + 0.156 = 0.1915$**。

**Baum-Welch 一步**（示意）：算 $\gamma, \xi$ 后用公式更新 $A, B, \pi$；本例仅 2 时刻，实际需长序列。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| 前向算法复杂度 $O(N^T)$ | **错**。动态规划 $O(N^2T)$ |
| Baum-Welch 保证全局最优 | **错**。EM 性质：仅局部最优（似然非凸），依赖初始化 |
| $\beta_T(i) = 0$ | **错**。$\beta_T(i) = 1$（无后续观测，概率为 1） |
| $\gamma$ 与 $\xi$ 相同 | **错**。$\gamma$ 是单时刻状态占用，$\xi$ 是相邻时刻状态对占用；$\gamma_t(i) = \sum_j\xi_t(i,j)$ |
| 前向只能算 $P(O)$ | **错**。$\alpha_t$ 还可用于滤波（在线后验） |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出前向递推公式。
2. Baum-Welch 的三个更新公式分别是什么？

### #自测题/中等
3. 用 §6 数据手算 $P(O{=}(0,1))$ 的完整前向过程。
4. 说明 $\gamma_t(i)$ 与 $\xi_t(i,j)$ 的定义差异。

### #自测题/较难
5. 证明 Baum-Welch 是 EM：写出 E 步的 Q 函数并说明 M 步为何得频率更新。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. $\alpha_{t+1}(j) = b_j(o_{t+1})\sum_i\alpha_t(i)a_{ij}$；$\alpha_1(i) = \pi_i b_i(o_1)$；$P(O) = \sum_i\alpha_T(i)$。
2. $\hat\pi_i = \gamma_1(i)$；$\hat a_{ij} = \sum_t\xi_t(i,j)/\sum_t\gamma_t(i)$；$\hat b_j(k) = \sum_{t:o_t=v_k}\gamma_t(j)/\sum_t\gamma_t(j)$。
3. 见 §6：$P(O) = 0.1915$。
4. $\gamma_t(i)$：$t$ 时刻在 $s_i$ 的边缘后验；$\xi_t(i,j)$：$t,t+1$ 时刻在 $(s_i,s_j)$ 的联合后验。
5. 隐状态是缺失数据；$Q$ 是完整数据对数似然在 $\gamma,\xi$ 下的期望；M 步拉格朗日最大化得频率更新（与 EM 一般形式一致）。
</details>

---

## 9. 通过标准

- [ ] 能**默写**前向/后向递推与 Baum-Welch 更新；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**手算**小 HMM 的前向概率；
- [ ] 能**说明** Baum-Welch 与 EM 的关系。

---

## 10. 来源

- Rabiner (1989). A tutorial on hidden Markov models and selected applications in speech recognition. *Proc. IEEE*.
- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Ch. 23.
- Bishop (2006). *PRML*, Springer. §13.2. 访问日期：2026-08-07。

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

> 直接下游：[[概率图模型-Viterbi解码]]、阶段 6 的 HMM 项目、课程 Capstone。

## 🃏 Anki 卡片

- 前向变量 α_t(i) 的定义::α_t(i) = P(o_1,...,o_t, q_t=s_i | λ)，前 t 个观测且 t 时刻处于状态 i 的联合概率
- 前向递推式::α_{t+1}(j) = b_j(o_{t+1}) · Σ_{i=1}^{N} α_t(i)·a_{ij}
- 后向变量 β_t(i) 的定义::β_t(i) = P(o_{t+1},...,o_T | q_t=s_i, λ)，给定 t 时刻状态后其后观测的概率
- 前向/后向算法的时间复杂度::O(N²T)，N 为状态数、T 为序列长度
