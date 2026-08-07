---
type: study
topic: "BN结构学习"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-学习算法]]"
flow: knowledge
kind: derivation
difficulty: advanced
upstream: ["[[概率图模型-BN参数学习]]", "[[概率图模型-条件独立与d分隔]]", "[[概率图模型-优化初步]]"]
concept: ["结构学习", "评分函数", "BIC", "BDeu", "搜索算法"]
related: ["概率图模型-因果发现", "概率图模型-ChowLiu算法"]
tags: [概率图模型, 结构学习, BIC, BDeu]
---

# 概率图模型-BN结构学习

> 结构学习回答：**从数据中发现 BN 的 DAG 结构**。本卡聚焦**基于评分**的方法：评分函数（BIC/AIC/BDeu）权衡拟合与复杂度，搜索算法（K2/爬山/禁忌/遗传）在结构空间中寻优。约束方法（PC 等）见 [[概率图模型-因果发现]]。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：给定数据，不知道变量间的依赖方向/结构。穷举所有 DAG 是超指数级（$n$ 节点 DAG 数 ~ $n!\,2^{\Theta(n^2)}$）。结构学习需要：①一个**评分函数**量化"结构 $G$ 有多好"；②一个**搜索策略**在巨大的结构空间中找到好结构。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：结构学习是"从数据学模型"的综合目标（不只是填 CPT）；评分-搜索范式也是网络结构推断（GNN 结构搜索）的原型。
- **实际应用场景**：从基因表达数据发现调控网络、从问卷数据学贝叶斯网。
- **高频考点**：BIC 公式与渐进一致性、BDeu 与先验、搜索空间的爆炸、K2 的节点序假设。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-BN参数学习]]**：参数似然与 Dirichlet 先验（BDeu 依赖）。
2. **[[概率图模型-优化初步]]**：正则化/复杂度权衡。
3. **[[概率图模型-贝叶斯网络]]**：DAG 语义。

---

## 4. 定义与核心公式

### 4.1 评分函数

**目标**：$\hat G = \arg\max_G \text{score}(G : \mathcal{D})$。

**BIC（贝叶斯信息准则，渐进一致）**：
$$\text{BIC}(G) = \log P(\mathcal{D}\mid\hat\theta_G) - \frac{d_G}{2}\log N$$
- 第一项：拟合（MLE 对数似然）；第二项：复杂度惩罚（$d_G$ 为自由参数数）；
- **性质**：$N\to\infty$ 时以概率 1 选择真实结构（若在搜索空间内）——渐进一致。

**AIC（赤池信息准则，预测导向）**：
$$\text{AIC}(G) = \log P(\mathcal{D}\mid\hat\theta_G) - d_G$$
- 惩罚更轻（$\log N/2$ vs 1）；偏向更复杂模型；预测误差更优但非一致。

**BDeu（贝叶斯 Dirichlet 评分，精确贝叶斯）**：
$$\text{BDeu}(G) = \log P(G) + \sum_i \sum_{\mathbf{p}} \left[\log\frac{\Gamma(\alpha_{i\mathbf{p}})}{\Gamma(\alpha_{i\mathbf{p}} + n_{i\mathbf{p}})} + \sum_x \log\frac{\Gamma(\alpha_{ix\mathbf{p}} + n_{ix\mathbf{p}})}{\Gamma(\alpha_{ix\mathbf{p}})}\right]$$
（$n$ 为计数，$\alpha$ 为 BDeu 等效先验。）它是**边际似然** $P(\mathcal{D}\mid G)$（对参数积分），在 Dirichlet 先验下闭式，满足**局部性**（每变量独立计分）。

### 4.2 搜索算法

| 算法 | 策略 | 特点 |
|:---|:---|:---|
| **K2** | 给定节点序，贪心逐节点选父集 | 高效，但需拓扑序先验 |
| **爬山法** | 局部搜索：加边/删边/转边，取评分提升最大者 | 简单，易局部最优 |
| **禁忌搜索** | 记录近期操作，禁止回退 | 逃离局部最优 |
| **遗传算法** | 群体进化（交叉/变异/选择） | 全局搜索，慢 |

**搜索空间**：$n=10$ 时 DAG 数约 $10^{18}$——必须启发式；**评分可分解**（BIC/BDeu 都是 $\sum_i \text{score}_i$）使局部操作（改一条边）只影响局部评分，是高效搜索的关键。

---

## 5. 关键推导

**推导：BIC 来自贝叶斯因子近似**。

边际似然 $P(\mathcal{D}\mid G) = \int P(\mathcal{D}\mid\theta,G)P(\theta\mid G)d\theta$，Laplace 近似得 $\log P(\mathcal{D}\mid G) \approx \log P(\mathcal{D}\mid\hat\theta) - \frac{d}{2}\log N + O(1)$——即 BIC。∎

**推导：BIC 为什么一致**。

真结构 $G^*$ 下，$\log P(\mathcal{D}\mid\hat\theta_{G^*})/N \to \mathbb{E}[\log P]$（KL 到真分布），且惩罚项 $d\log N/(2N) \to 0$；对错误结构，拟合项严格小于真结构（KL > 0）且不随 $N$ 消失，故 $N$ 大时 BIC 选真结构。∎

**推导：评分可分解性**。

BIC/BDeu 的得分 $= \sum_i \text{score}(X_i \mid \text{Pa}(X_i))$（因对数似然与先验均按变量分解）。修改 $X_i$ 的父集只改变第 $i$ 项——局部搜索只需重算局部评分。∎

---

## 6. 最小可手算例子

**例（BIC 权衡）**：$N=100$，模型 1（独立，$d=2$）$\ell_1 = -150$；模型 2（$A\to B$，$d=4$）$\ell_2 = -130$。
- BIC$_1 = -150 - \frac{2}{2}\log100 = -150 - 4.6 = -154.6$；
- BIC$_2 = -130 - \frac{4}{2}\log100 = -130 - 9.2 = -139.2$；
- **BIC$_2$ > BIC$_1$** → 选 $A\to B$（拟合提升 20 值得额外 2 参数）。

**例（K2 直觉）**：节点序 $(A, B, C)$。贪心：先为 $B$ 选父（从 $A$ 开始试加，评分提升则保留），再为 $C$ 选父（试 $A,B$）——只需在给定序下做局部贪心。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| 结构学习能找到"因果" | **不精确**。评分方法学的是"统计依赖结构"；同一马尔可夫等价类（如 $A\to B$ 与 $B\to A$）不可区分 |
| AIC 与 BIC 行为相同 | **错**。AIC 惩罚轻、预测导向、非一致；BIC 惩罚重、一致、模型选择导向 |
| 搜索总能找到全局最优 | **错**。超指数空间下启发式只能局部最优；K2 还需节点序先验 |
| BDeu 不需要先验 | **错**。BDeu 依赖等效样本量 $\alpha$ 与结构先验 $P(G)$ |
| 评分越高越好，不看数据量 | **不精确**。小样本下复杂评分过拟合；评分需与数据量匹配（BIC 自动平衡） |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出 BIC 与 AIC 公式并说明差异。
2. 为什么 DAG 搜索空间爆炸？

### #自测题/中等
3. 解释"评分可分解性"为什么是高效搜索的关键。
4. 用 §6 数据判断：若 $\ell_2 - \ell_1 = 5$（而非 20），BIC 会怎么选？

### #自测题/较难
5. 为什么评分方法无法区分马尔可夫等价类（如 $A\to B$ vs $B\to A$）？这对"因果发现"意味着什么？

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. BIC $= \ell - \frac d2\log N$；AIC $= \ell - d$。AIC 惩罚轻、非一致；BIC 一致。
2. $n$ 节点 DAG 数超指数（~$n!2^{\Theta(n^2)}$）。
3. 分解使局部边操作只影响局部评分，无需全图重算。
4. BIC$_1 = -150 - 4.6 = -154.6$；BIC$_2 = -145 - 9.2 = -154.2$——仍选模型 2 但差距很小；若 $d$ 更大则模型 1 胜。
5. $A\to B$ 与 $B\to A$ 蕴含相同条件独立集（无 V 型时），似然相同 → 评分相同。结构学习只能确定**马尔可夫等价类**；因果方向需干预/额外假设（见 [[概率图模型-因果发现]]）。
</details>

---

## 9. 通过标准

- [ ] 能**默写** BIC/AIC/BDeu 与主要搜索算法；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**手算** BIC 权衡并选择结构；
- [ ] 能**说明**结构学习与因果发现的边界。

---

## 10. 来源

- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Chapter 18.
- Schwarz (1978). Estimating the dimension of a model. *Ann. Statist.*
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

> 直接下游：[[概率图模型-因果发现]]（PC/IC/FCI）、[[概率图模型-ChowLiu算法]]（树结构特例）、阶段 4 的 BN 建模、课程 Capstone。

