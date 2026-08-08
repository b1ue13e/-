---
type: study
topic: "BN参数学习"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-学习算法]]"
flow: knowledge
kind: derivation
difficulty: intermediate
upstream: ["[[概率图模型-贝叶斯网络]]", "[[概率图模型-指数族]]", "[[概率图模型-优化初步]]"]
concept: ["极大似然估计", "贝叶斯估计", "Dirichlet先验", "共轭先验"]
related: ["概率图模型-贝叶斯网络", "概率图模型-MRF参数学习"]
tags: [概率图模型, 参数学习, MLE, 贝叶斯估计]
anki_deck: "概率图模型::03-学习算法"
anki_tags: [概率图模型, 参数学习, MLE, Dirichlet]
---

# 概率图模型-BN参数学习

> 本卡讲解**完全数据**下贝叶斯网络参数的两种估计：极大似然估计（MLE，频率计数）与贝叶斯估计（Dirichlet 先验平滑）。两者都有**闭式解**（CPT 的计数/伪计数），是阶段 3 的第一块基石。MRF 的参数学习（无闭式）见 [[概率图模型-MRF参数学习]]。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：给定数据集 $\mathcal{D}$（$N$ 个完整样本）和固定的 BN 结构（DAG），如何估计每个 CPT $P(X_i \mid \text{Pa}(X_i))$ 的参数？完全数据下这很简单：**数数**。但小样本时需要平滑（贝叶斯估计）、要处理未观测组合，且要理解为什么"数数"就是最优。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：参数学习是 BN 应用的"填表"步骤；MLE 的因子分解性质（每张 CPT 独立估计）是 BN 相对一般模型的效率来源；贝叶斯估计的平滑直接支撑结构学习的 BDeu 评分。
- **实际应用场景**：从病历数据学诊断网络 CPT、从点击数据学推荐模型。
- **高频考点**：MLE 闭式推导、CPT 独立估计、伪计数（Dirichlet 平滑）、贝叶斯估计与 MLE 的关系。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-贝叶斯网络]]**：CPT 分解 $P(\mathbf{X}) = \prod_i P(X_i \mid \text{Pa}(X_i))$。
2. **[[概率图模型-指数族]]**：多项分布、共轭（Dirichlet 是多项的共轭先验）。
3. **[[概率图模型-优化初步]]**：拉格朗日求解带约束最大化。

---

## 4. 定义与核心公式

### 4.1 极大似然估计（MLE）

**目标**：$\hat\theta = \arg\max_\theta \log P(\mathcal{D} \mid \theta)$。

**BN 分解**（完全数据）：对数似然分解为各 CPT 之和：
$$\log P(\mathcal{D}\mid\theta) = \sum_i \sum_{\text{样本}} \log P(x_i^{(t)} \mid \text{pa}_i^{(t)}, \theta_i) = \sum_i \ell_i(\theta_i)$$
**每个 $\theta_i$ 独立最大化**。

**CPT 的 MLE 闭式**（多项式/伯努利）：
$$\hat P(X_i = x \mid \text{Pa}(X_i) = \mathbf{p}) = \frac{\text{count}(X_i = x, \text{Pa}_i = \mathbf{p})}{\text{count}(\text{Pa}_i = \mathbf{p})}$$

即**条件频率计数**。**证明**：用拉格朗日（$\sum_x \hat\theta_{x\mid p} = 1$）对每行 CPT 单独求解，得频率解（见 [[概率图模型-优化初步]] 推导 3 的推广）。

### 4.2 贝叶斯估计与 Dirichlet 先验

**问题**：小样本时频率估计不可靠（如某组合从未出现 → 概率 0）。

**Dirichlet 先验**：对每行 CPT，取 $\theta_{\cdot \mid \mathbf{p}} \sim \text{Dirichlet}(\alpha_{x \mid \mathbf{p}})$（参数即**伪计数**）。它是多项分布的共轭先验。

**后验**：$\text{Dirichlet}(\alpha_{x\mid\mathbf{p}} + \text{count}(x, \mathbf{p}))$——**后验仍为 Dirichlet**，期望估计为：

$$\hat P(X_i = x \mid \text{Pa}_i = \mathbf{p}) = \frac{\alpha_{x\mid\mathbf{p}} + \text{count}(x, \mathbf{p})}{\sum_{x'}(\alpha_{x'\mid\mathbf{p}} + \text{count}(x', \mathbf{p}))}$$

**常见的等价先验**：
- **BDeu 先验**：$\alpha_{x\mid p} = \alpha / (\text{取值数} \times |\text{Pa}_i \text{ 组合数}|)$（等效样本量 $\alpha$ 均匀分配）；
- **Laplace 平滑**：$\alpha = 1$ 均匀。

**性质**：贝叶斯估计 = MLE + 伪计数；$N \to \infty$ 时收敛到 MLE；小样本时避免零概率。

---

## 5. 关键推导

**推导：对数似然按 CPT 分解（独立性）**。

$\log P(\mathcal{D}\mid\theta) = \sum_t \log\prod_i P(x_i^{(t)}\mid pa_i^{(t)},\theta_i) = \sum_i \sum_t \log P(x_i^{(t)}\mid pa_i^{(t)},\theta_i)$——求和可交换，每项只含 $\theta_i$，故各 $\theta_i$ 独立优化。∎

**推导：CPT 单行 MLE = 频率**。

固定 $\text{Pa}_i = \mathbf{p}$，该行参数 $\theta_{\cdot}$ 是多项分布，观测计数 $n_x$。最大化 $\sum_x n_x \log\theta_x$ 受 $\sum_x\theta_x = 1$：拉格朗日 $\sum_x n_x\log\theta_x + \lambda(\sum_x\theta_x - 1)$，求导 $\frac{n_x}{\theta_x} + \lambda = 0 \Rightarrow \theta_x \propto n_x$，归一化 $\theta_x = n_x / \sum n_x$。∎

**推导：Dirichlet 共轭**。

$P(\theta\mid \mathcal{D}) \propto P(\mathcal{D}\mid\theta)\text{Dir}(\theta;\alpha) \propto \prod_x \theta_x^{n_x} \prod_x \theta_x^{\alpha_x - 1} = \prod_x \theta_x^{\alpha_x + n_x - 1}$——正是 $\text{Dirichlet}(\alpha + n)$ 的核。∎

---

## 6. 最小可手算例子

**例**：BN $A \to B$，$A, B$ 二值。数据 5 条：$(1,1), (1,0), (1,1), (0,1), (0,0)$。

**MLE**：
- $P(A{=}1) = 3/5 = 0.6$；
- $P(B{=}1\mid A{=}1) = 2/3 \approx 0.667$；$P(B{=}1\mid A{=}0) = 1/2 = 0.5$。

**贝叶斯（Laplace $\alpha = 1$）**：
- $P(A{=}1) = (3+1)/(5+2) = 4/7 \approx 0.571$；
- $P(B{=}1\mid A{=}1) = (2+1)/(3+2) = 3/5 = 0.6$；$P(B{=}1\mid A{=}0) = (1+1)/(2+2) = 0.5$。

**对比**：平滑把极端值拉向均匀，小样本更稳健。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| BN 参数学习要联合优化所有参数 | **错**。完全数据下每张 CPT 独立估计（似然可分解） |
| 未观测组合的 CPT 概率应为 0 | **错**。频率 0 是估计偏差；贝叶斯平滑/伪计数避免零概率（否则推断时乘 0 全盘崩溃） |
| Dirichlet 先验只用于 BN | **错**。任何多项参数（主题模型、朴素贝叶斯）都可用 |
| MLE 在小样本下也好 | **错**。小样本 MLE 高方差/过拟合；贝叶斯估计更稳健 |
| 先验越大越好 | **不精确**。先验强度 $\alpha$ 大 = 数据影响小；需与数据量匹配（BDeu 用等效样本量） |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出 CPT 的 MLE 闭式公式。
2. Dirichlet 先验在 BN 参数学习中起什么作用？

### #自测题/中等
3. 用上例数据完成 MLE 与 Laplace 平滑估计，对比结果。
4. 证明"对数似然可分解为各 CPT 之和"。

### #自测题/较难
5. 为什么贝叶斯估计收敛到 MLE？给出直觉与数学说明（$N \to \infty$）。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. $\hat P(x\mid p) = \frac{count(x,p)}{count(p)}$。
2. 提供伪计数平滑，避免零概率；作为多项共轭先验使后验闭式。
3. 见 §6。
4. $\log P = \sum_t \log\prod_i P(x_i\mid pa_i)$，交换求和顺序即得每项只含 $\theta_i$。
5. 后验 = $\text{Dirichlet}(\alpha + n)$，其均值 = $\frac{\alpha + n}{N + \sum\alpha} \to \frac{n}{N}$（频率），即 MLE。
</details>

---

## 9. 通过标准

- [ ] 能**默写** MLE 与贝叶斯估计公式；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**推导** CPT MLE 闭式与 Dirichlet 共轭；
- [ ] 能**说明**平滑对推断鲁棒性的作用。

---

## 10. 来源

- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Chapter 17.
- Stanford CS228 Notes, Lecture 7 (Learning). https://ermongroup.github.io/cs228-notes/
- Heckerman (1998). A tutorial on learning with Bayesian networks. 访问日期：2026-08-07。

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

> 直接下游：[[概率图模型-BN结构学习]]（BDeu 评分）、阶段 4 的 [[概率图模型-BN工程实践]]、课程 Capstone（参数学习部分）。

## 🃏 Anki 卡片

- 完全数据下 BN 的 CPT MLE 闭式::条件频率计数 P̂(X=x|Pa=p) = count(x,p) / count(p)
- Dirichlet 先验的参数含义::α_{x|p} 即伪计数，是多项分布的共轭先验，可避免零频率
- 为什么 BN 参数可逐 CPT 独立最大化::对数似然分解为各 CPT 对数之和（Σ_i ℓ_i(θ_i)），参数互不共享
