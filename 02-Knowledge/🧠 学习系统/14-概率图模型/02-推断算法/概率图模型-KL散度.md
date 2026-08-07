---
type: study
topic: "KL散度"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-推断算法]]"
flow: knowledge
kind: derivation
difficulty: intermediate
upstream: ["[[概率图模型-贝叶斯规则与条件独立]]", "[[概率图模型-指数族]]"]
concept: ["KL散度", "信息论", "变分推断"]
related: ["概率图模型-变分推断与ELBO", "概率图模型-变分推断算法"]
tags: [概率图模型, KL散度, 信息论]
---

# 概率图模型-KL散度

> KL 散度（Kullback-Leibler divergence）度量"用 $q$ 近似 $p$ 的代价"，是变分推断的**优化目标核心**。本卡给出定义、性质、两种方向（$\text{KL}(q\parallel p)$ vs $\text{KL}(p\parallel q)$）的本质差异，以及它在 ELBO 推导中的角色。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：后验 $p(\mathbf{z} \mid \mathbf{x})$ 往往不可计算（分母难积）。变分推断的思路是：在一个"好算的分布族" $\mathcal{Q}$ 中找 $q^*$ 最接近 $p$。**"接近"怎么度量？** 答案就是 KL 散度——它是信息论意义下"用 $q$ 编码 $p$ 的额外代价"，也是变分推断的优化目标。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：ELBO = $\log p(\mathbf{x}) - \text{KL}(q \parallel p)$（见 [[概率图模型-变分推断与ELBO]]）；KL 的方向选择决定变分推断是"零强制"还是"零避免"。
- **实际应用场景**：变分自编码器（VAE）损失、模型选择、密度估计。
- **高频考点**：KL 定义与性质、$\text{KL}(q\parallel p)$ vs $\text{KL}(p\parallel q)$ 差异、非负性证明、与 ELBO 的关系。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-贝叶斯规则与条件独立]]**：后验、证据。
2. **[[概率图模型-指数族]]**：期望与对数配分函数（KL 在指数族下有闭式）。
3. 信息论基础：熵 $H(p) = -\sum p\log p$。

---

## 4. 定义与核心公式

### 4.1 定义

**定义（KL 散度）**：对离散分布 $p, q$（$q > 0$ 处 $p = 0$）：
$$\text{KL}(q \parallel p) = \sum_{\mathbf{z}} q(\mathbf{z}) \log \frac{q(\mathbf{z})}{p(\mathbf{z})} = \mathbb{E}_q\left[\log\frac{q}{p}\right]$$

连续情形把求和换积分。**注意顺序**：$\text{KL}(q\parallel p)$ 是"以 $q$ 为权重、比较 $q$ 对 $p$"。

### 4.2 关键性质

**非负性**：$\text{KL}(q \parallel p) \ge 0$，等号当且仅当 $q = p$（几乎处处）。

**不对称性**：$\text{KL}(q \parallel p) \ne \text{KL}(p \parallel q)$ 一般成立——KL **不是**距离（不满足对称性与三角不等式）。

**与熵的关系**：$\text{KL}(q \parallel p) = \underbrace{-\mathbb{E}_q[\log p]}_{\text{交叉熵}} - \underbrace{(-\mathbb{E}_q[\log q])}_{H(q)}$。

**分解形式**：$\text{KL}(q \parallel p) = \mathbb{E}_q[\log q] - \mathbb{E}_q[\log p]$。

### 4.3 两种方向的意义（变分推断核心）

设 $q$ 是变分分布（简单），$p$ 是目标后验（复杂）。

**$\text{KL}(q \parallel p)$（反向 KL，变分推断采用）**：
- $q$ 小处若 $p$ 大，$\log(q/p) \to -\infty$ 但被 $q \approx 0$ 加权 → **惩罚 $p$ 有质量而 $q$ 没有**的地方有限；
- 结果：$q$ 倾向于**锁定在 $p$ 的一个峰**（mode-seeking / 零避免，zero-avoiding）；
- 优点：只需求 $\mathbb{E}_q[\log p]$，可计算（不需要 $p$ 归一化）——所以 VI 用它。

**$\text{KL}(p \parallel q)$（正向 KL，期望传播/EP 采用）**：
- $p$ 有质量而 $q$ 没有的地方被大权重惩罚 → **$q$ 覆盖 $p$ 的所有支撑**（mean-seeking / 零强制，zero-forcing）；
- 缺点：需要 $\mathbb{E}_p[\log q]$，涉及对复杂 $p$ 求期望，难算。

---

## 5. 关键推导

**推导：KL 非负性（Jensen 不等式）**。

$\text{KL}(q\parallel p) = -\mathbb{E}_q[\log \frac{p}{q}] \ge -\log \mathbb{E}_q[\frac{p}{q}] = -\log \sum_z q \frac{p}{q} = -\log \sum_z p = 0$（Jensen：$-\log$ 凸，期望换序）。等号当且仅当 $\frac pq$ 为常数即 $p=q$。∎

**推导：ELBO 中的 KL**（连接变分）。

$$\log p(\mathbf{x}) = \log \sum_z p(\mathbf{x},\mathbf{z}) = \log \mathbb{E}_q\left[\frac{p(\mathbf{x},\mathbf{z})}{q(\mathbf{z})}\right] \ge \mathbb{E}_q[\log p(\mathbf{x},\mathbf{z})] - \mathbb{E}_q[\log q(\mathbf{z})] = \text{ELBO}(q)$$
且 $\log p(\mathbf{x}) = \text{ELBO}(q) + \text{KL}(q \parallel p(\mathbf{z}\mid\mathbf{x}))$（把 $p(\mathbf{x},\mathbf{z}) = p(\mathbf{z}\mid\mathbf{x})p(\mathbf{x})$ 代入展开）。最大化 ELBO ⇔ 最小化 $\text{KL}(q\parallel p(\cdot\mid\mathbf{x}))$。∎

**推导：指数族间的 KL**（变分更新用）。

若 $q_\eta$ 与 $p_{\eta'}$ 同指数族：$\text{KL}(q_\eta \parallel p_{\eta'}) = A(\eta') - A(\eta) - \langle \eta' - \eta, \nabla A(\eta)\rangle$（利用 $\mathbb{E}_q[T] = \nabla A(\eta)$）。这给出 MFVI 坐标更新的闭式。∎

---

## 6. 最小可手算例子

**例 1（手算 KL）**：$q = \text{Bernoulli}(0.9)$，$p = \text{Bernoulli}(0.5)$。
$$\text{KL}(q\parallel p) = 0.9\log\frac{0.9}{0.5} + 0.1\log\frac{0.1}{0.5} = 0.9\times0.588 + 0.1\times(-1.609) = 0.529 - 0.161 = 0.368$$

**例 2（方向差异）**：$p$ 是双峰（两个高斯峰），$q$ 是单高斯。
- $\text{KL}(q\parallel p)$：$q$ 会**锁定一个峰**（mode-seeking）——若初始化偏向峰 A，$q$ 覆盖峰 A；
- $\text{KL}(p\parallel q)$：$q$ 会**横跨两峰之间**（mean-seeking）——覆盖两峰，落在低概率谷区。
- 这解释了"VI 低估方差、EP 高估方差"的经典现象。

**例 3（与 ELBO）**：$\log p(\mathbf{x}) = 5$，若 $\text{KL}(q\parallel p) = 0.5$，则 $\text{ELBO}(q) = 4.5$。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| KL 是距离度量 | **错**。不对称、不满足三角不等式；是"散度"不是"距离" |
| $\text{KL}(q\parallel p) = \text{KL}(p\parallel q)$ | **错**。一般不等；方向选择决定 mode-seeking vs mean-seeking |
| KL 可以为负 | **错**。恒非负（Jensen），最小 0 |
| 变分推断用正向 KL | **错**。VI 用反向 KL（$\text{KL}(q\parallel p)$），因为可计算；EP 才用正向 |
| KL 需要 $p$ 归一化 | **错**。$\text{KL}(q\parallel p)$ 中 $p$ 的归一化常数是常数项，优化时可忽略（这正是 VI 可行的关键） |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出 $\text{KL}(q\parallel p)$ 的定义并说明符号含义。
2. KL 非负性用什么不等式证明？

### #自测题/中等
3. 手算 $\text{KL}(\text{Bern}(0.8)\parallel \text{Bern}(0.5))$。
4. 解释 mode-seeking 与 mean-seeking 的差异，各自对应哪种 KL 方向？

### #自测题/较难
5. 推导 $\log p(\mathbf{x}) = \text{ELBO}(q) + \text{KL}(q\parallel p(\mathbf{z}\mid\mathbf{x}))$，并说明"为什么最大化 ELBO 等价于最小化 KL"。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. $\text{KL}(q\parallel p) = \sum_z q(z)\log\frac{q(z)}{p(z)} = \mathbb{E}_q[\log(q/p)]$。
2. Jensen 不等式（$-\log$ 凸）。
3. $0.8\log(0.8/0.5) + 0.2\log(0.2/0.5) = 0.8\times0.47 + 0.2\times(-0.916) = 0.376 - 0.183 = 0.193$。
4. $\text{KL}(q\parallel p)$（反向）mode-seeking，$q$ 锁一峰；$\text{KL}(p\parallel q)$（正向）mean-seeking，$q$ 覆盖全支撑。
5. 见 §5 推导：把 $p(\mathbf{x},\mathbf{z}) = p(\mathbf{z}\mid\mathbf{x})p(\mathbf{x})$ 代入 ELBO 定义并重组；$p(\mathbf{x})$ 与 $q$ 无关故固定，最大化 ELBO = 最小化 KL。
</details>

---

## 9. 通过标准

- [ ] 能**默写** KL 定义、非负性证明、两种方向差异；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**推导** ELBO = log 证据 − KL；
- [ ] 能**解释** VI 用反向 KL 的原因。

---

## 10. 来源

- Kullback & Leibler (1951). On information and sufficiency. *Ann. Math. Statist.*
- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Appendix A / Ch. 8.
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

> 直接下游：[[概率图模型-变分推断与ELBO]]、[[概率图模型-变分推断算法]]、阶段 6 的 [[KL损失]]（VAE）。
