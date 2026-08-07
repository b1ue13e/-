---
type: study
topic: "变分EM"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-学习算法]]"
flow: knowledge
kind: derivation
difficulty: advanced
upstream: ["[[概率图模型-EM算法]]", "[[概率图模型-变分推断算法]]", "[[概率图模型-变分推断与ELBO]]"]
concept: ["变分EM", "变分E步", "LDA", "随机变分EM"]
related: ["概率图模型-EM算法", "概率图模型-变分推断算法"]
tags: [概率图模型, 变分EM, LDA]
---

# 概率图模型-变分EM

> 当隐变量后验**不可精确计算**时，标准 EM 的 E 步无法执行。**变分 EM** 用变分推断近似 E 步：交替更新变分参数（变分 E 步）与模型参数（M 步）。这是 LDA 主题模型、大规模隐变量模型的**标准求解方法**。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：EM 的 E 步需要精确后验 $P(\mathbf{Z}\mid\mathbf{X},\theta)$。但复杂模型（LDA、深度潜变量模型）的隐变量后验**无闭式**（变量间相互依赖、嵌套）。变分 EM 的答案：E 步不精确计算后验，而是用变分分布 $q$ 近似，交替优化 $q$ 与 $\theta$。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：变分 EM 把"推断（E）"与"学习（M）"解耦为双优化循环；它是 LDA（Blei 2003 的原始求解）、变分自编码器的前身思想。
- **实际应用场景**：LDA 主题建模、大规模 GMM/贝叶斯混合模型、隐变量 BN 学习。
- **高频考点**：变分 EM 的目标、变分 E 步与标准 E 步的区别、LDA 的变分更新、与 VAE 的联系。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-EM算法]]**：标准 EM 的 E/M 步与单调性。
2. **[[概率图模型-变分推断算法]]**：CAVI、ELBO 优化。
3. **[[概率图模型-变分推断与ELBO]]**：ELBO 定义。

---

## 4. 定义与核心公式

### 4.1 目标与结构

**完整数据对数似然**：$\ell(\theta) = \sum_t \log P(\mathbf{x}^{(t)}\mid\theta)$。

**变分 EM 目标**：在参数 $\theta$ 与变分分布 $q$ 上联合优化 ELBO 下界：

$$\mathcal{L}(q, \theta) = \mathbb{E}_q[\log P(\mathbf{X},\mathbf{Z}\mid\theta)] - \mathbb{E}_q[\log q(\mathbf{Z})] \le \ell(\theta)$$

**循环**：
- **变分 E 步**：固定 $\theta$，优化 $q$ 最大化 $\mathcal{L}$（即最小化 $\text{KL}(q \parallel P(\mathbf{Z}\mid\mathbf{X},\theta))$）——用变分推断（如 CAVI/平均场）；
- **M 步**：固定 $q$，优化 $\theta$ 最大化 $\mathcal{L}$（此时 $\mathbb{E}_q[\log P(\mathbf{X},\mathbf{Z}\mid\theta)]$ 可用 $q$ 的充分统计量计算，类似标准 EM 的 M 步）。

### 4.2 与标准 EM 的关系

- 标准 EM：E 步取 $q = P(\mathbf{Z}\mid\mathbf{X},\theta^{\text{old}})$（精确）；
- 变分 EM：$q$ 限制在变分族（平均场等），$\text{KL} > 0$，ELBO 是**更松的下界**；
- 两者都单调不降 $\mathcal{L}$；变分 EM 的 $\ell$ 也单调不降（因 $\mathcal{L}$ 上升且 $\ell \ge \mathcal{L}$，需 $\theta$ 更新不破坏下界）。

### 4.3 LDA 的变分 EM（例子）

LDA：文档-主题分布 $\theta_d$、主题-词分布 $\beta_k$、每词主题 $z_{dn}$（隐变量）。
- **变分 E 步**：对每个文档，用平均场 $q(z_{dn}, \theta_d) = q(\theta_d)\prod_n q(z_{dn})$ 近似后验，CAVI 更新 $\phi_{dn}$（词的主题分布）与 $\gamma_d$（文档主题参数）；
- **M 步**：更新全局 $\beta_k$（主题-词分布），公式与"用变分计数统计词-主题频数"同构。

---

## 5. 关键推导

**推导：变分 E 步的更新（平均场）**。

固定 $\theta$，对 $q(\mathbf{Z}) = \prod_i q_i(Z_i)$ 用 CAVI：$q_i^*(z_i) \propto \exp(\mathbb{E}_{q_{-i}}[\log P(\mathbf{x},\mathbf{z}\mid\theta)])$。这与 [[概率图模型-变分推断算法]] 的 CAVI 完全相同——E 步就是一个变分推断子问题。∎

**推导：M 步用充分统计量**。

$\mathcal{L} = \mathbb{E}_q[\log P(\mathbf{X},\mathbf{Z}\mid\theta)] + \text{const}$（熵项与 $\theta$ 无关）。对指数族完整模型，$\mathbb{E}_q[\log P] = \theta^\top \sum_t \mathbb{E}_q[T(\mathbf{x}^{(t)},\mathbf{z}^{(t)})] - N A(\theta)$，只需 $q$ 下的充分统计量期望（E 步已算出）即可最大化——与标准 EM 的 M 步同构。∎

**推导：为什么比精确 EM 慢但可行**。
变分 E 步每次要迭代优化 $q$（内层循环），计算量大于单次精确后验；但在后验无闭式时这是**唯一可行**的 E 步近似，且随数据规模可扩展（SVI 再加速）。∎

---

## 6. 最小可手算例子

**例（混合模型 + 变分 E 步直觉）**：GMM 但后验近似（如高维）。变分 E 步用平均场 $q(z) = \prod_k q(z_k)$ 近似后验责任，M 步用 $\mathbb{E}_q$ 的软计数更新 $\mu,\Sigma$——当后验恰为可分解时退化为标准 EM。

**例（LDA 变分计数）**：M 步更新主题-词 $\beta_{kv} \propto \sum_d \sum_n \phi_{dnk}\mathbb{1}[w_{dn}=v]$——用变分责任 $\phi$ 代替硬指派，即"软计数"。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| 变分 EM = 标准 EM 加近似 | **对**。但 E 步是迭代变分优化，不是单次计算 |
| 变分 EM 保证全局最优 | **错**。双非凸目标（$q$ 与 $\theta$），只局部最优 |
| 变分 E 步和 M 步必须严格交替到收敛 | **不必须**。实践常每轮各做一步/几步（广义变分 EM） |
| LDA 只能变分 EM | **错**。也可 MCMC（Gibbs 采样）求解；变分 EM 更快、可扩展 |
| 变分 EM 只用于文本 | **错**。任何后验不可解的大规模隐变量模型都适用 |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 变分 EM 与标准 EM 的 E 步有何区别？
2. 变分 EM 交替优化哪两组变量？

### #自测题/中等
3. 说明为什么变分 EM 的 $\ell$ 单调不降。
4. LDA 的变分 E 步与 M 步各更新什么？

### #自测题/较难
5. 对比变分 EM 与 VAE 的训练目标结构（两者都最大化 ELBO 下界，区别在哪？）。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. 标准 EM 取精确后验；变分 EM 在变分族内近似（KL > 0）。
2. 变分参数 $q$（变分 E 步）与模型参数 $\theta$（M 步）。
3. 变分 E 步提高 $\mathcal{L}(q,\theta)$，M 步也提高 $\mathcal{L}$；$\ell \ge \mathcal{L}$ 且（θ 固定时）E 步使 $\mathcal{L}$ 逼近 $\ell$，故 $\ell$ 单调不降（在 E 步精确最优时）。
4. E 步：文档-主题 $\gamma_d$ 与词-主题 $\phi_{dn}$；M 步：主题-词 $\beta_k$。
5. VAE 把"隐变量生成 + 编码器 $q(z\mid x)$"端到端用梯度下降优化（重参数化）；变分 EM 显式交替 E/M 两循环，$q$ 是每样本的推断而非共享网络。VAE 是变分 EM 的"摊销（amortized）"版本。
</details>

---

## 9. 通过标准

- [ ] 能**默写**变分 EM 目标与两阶段；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**说明**变分 EM 与标准 EM、VAE 的关系；
- [ ] 能**解释** LDA 的变分 EM 求解流程。

---

## 10. 来源

- Blei, Ng & Jordan (2003). Latent Dirichlet allocation. *JMLR*.
- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Chapter 19.5.
- Blei et al. (2017). *Variational Inference: A Review for Statisticians*. 访问日期：2026-08-07。

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

> 直接下游：阶段 6 的 [[LDA推断]]/[[LDA生成]]、课程 Capstone（EM/VI 部分）。
