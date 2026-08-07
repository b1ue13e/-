---
type: study
topic: "Gibbs与MH采样"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-推断算法]]"
flow: knowledge
kind: derivation
difficulty: intermediate
upstream: ["[[概率图模型-基本采样方法]]", "[[概率图模型-马尔可夫随机场]]"]
concept: ["MCMC", "Gibbs采样", "Metropolis-Hastings", "马尔可夫链"]
related: ["概率图模型-MCMC收敛与诊断", "概率图模型-基本采样方法"]
tags: [概率图模型, MCMC, Gibbs采样, MH采样]
---

# 概率图模型-Gibbs与MH采样

> 本卡是 **MCMC 家族的核心**：Metropolis-Hastings（MH）给出通用的"提议-接受"框架，Gibbs 采样是它在"按条件分布逐坐标更新"下的特例。两者都通过构造以目标分布为平稳分布的马尔可夫链来采样，克服了拒绝采样在高维下失效的问题。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：拒绝采样/似然加权在维数升高或证据复杂时效率崩溃（接受率指数级下降）。MCMC 的思路是：**不独立采样**，而是构造一条马尔可夫链，让它的**平稳分布 = 目标分布** $p(\mathbf{x})$；从链的后期样本近似 $p$。因为每步只做局部更新，高维下仍然可行。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：MCMC 是贝叶斯推断的主力（PyMC/Stan 的采样引擎）；Gibbs 是 MRF/CRF/主题模型的标准工具；HMC/NUTS（阶段 2 后续卡）是 MH 的连续空间改进。
- **实际应用场景**：贝叶斯后验采样、图像去噪（Ising 模型 Gibbs）、LDA 主题模型、生物 HMM 参数估计。
- **高频考点**：MH 接受率推导、详细平衡条件、Gibbs 是 MH 特例的证明、链的收敛判断。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-基本采样方法]]**：采样推断的动机与局限。
2. **[[概率图模型-马尔可夫随机场]]**：无向图/势函数（Gibbs 常用于 MRF）。
3. 概率基础：条件分布、马尔可夫链、平稳分布（可看 [[24-随机过程]] 的马尔可夫链部分）。

---

## 4. 定义与核心公式

### 4.1 Metropolis-Hastings（MH）

**目标**：从 $p(\mathbf{x})$ 采样（只需知道未归一化形式 $\tilde p(\mathbf{x}) \propto p(\mathbf{x})$）。

**算法**：
1. 初始化 $\mathbf{x}^{(0)}$；
2. 对 $t = 0, 1, 2, \dots$：
   - 从提议分布 $q(\mathbf{x}' \mid \mathbf{x}^{(t)})$ 提议 $\mathbf{x}'$；
   - 计算接受率：$$\alpha = \min\left(1, \frac{\tilde p(\mathbf{x}') q(\mathbf{x}^{(t)} \mid \mathbf{x}')}{\tilde p(\mathbf{x}^{(t)}) q(\mathbf{x}' \mid \mathbf{x}^{(t)})}\right)$$
   - 以概率 $\alpha$ 接受：$\mathbf{x}^{(t+1)} = \mathbf{x}'$；否则 $\mathbf{x}^{(t+1)} = \mathbf{x}^{(t)}$；
3. 丢弃前 $B$ 个样本（burn-in），用剩余样本估计。

**关键性质（详细平衡）**：转移核 $T$ 满足 $\tilde p(\mathbf{x})T(\mathbf{x} \to \mathbf{x}') = \tilde p(\mathbf{x}')T(\mathbf{x}' \to \mathbf{x})$，故 $\tilde p$（归一化即 $p$）是链的**平稳分布**。

### 4.2 Gibbs 采样（Gibbs Sampling）

**目标**：从联合分布 $p(\mathbf{x}_1, \dots, \mathbf{x}_n)$ 采样，已知所有**满条件分布** $p(x_i \mid \mathbf{x}_{-i})$。

**算法**（系统扫描）：
1. 初始化 $\mathbf{x}^{(0)}$；
2. 对 $t$，依次对 $i = 1, \dots, n$：
   - 从 $p(x_i \mid x_1^{(t+1)}, \dots, x_{i-1}^{(t+1)}, x_{i+1}^{(t)}, \dots, x_n^{(t)})$ 采样更新 $x_i$；
3. 完整扫一遍得样本 $\mathbf{x}^{(t+1)}$。

**图模型中的满条件**：在 MRF 中，$p(x_i \mid \mathbf{x}_{-i})$ 只依赖 $x_i$ 的**马尔可夫毯**（邻居及其共享因子）——所以每步更新只需局部信息，非常高效。

### 4.3 Gibbs 是 MH 的特例

对单坐标 $x_i$，Gibbs 的更新等价于 MH：提议 $q(x_i' \mid \mathbf{x}_{-i}) = p(x_i' \mid \mathbf{x}_{-i})$（满条件），接受率恒为 1：

$$\alpha = \min\left(1, \frac{p(x_i' \mid \mathbf{x}_{-i}) p(x_i \mid \mathbf{x}_{-i})}{p(x_i \mid \mathbf{x}_{-i}) p(x_i' \mid \mathbf{x}_{-i})}\right) = 1$$

**结论**：Gibbs 是**永远接受**的 MH，无调参但要求能直接从满条件采样。

---

## 5. 关键推导

**推导：MH 满足详细平衡**。

设 $\alpha(\mathbf{x} \to \mathbf{x}') = \min(1, \frac{\tilde p(\mathbf{x}')q(\mathbf{x}\mid\mathbf{x}')}{\tilde p(\mathbf{x})q(\mathbf{x}'\mid\mathbf{x})})$。转移核 $T(\mathbf{x}\to\mathbf{x}') = q(\mathbf{x}'\mid\mathbf{x})\alpha(\mathbf{x}\to\mathbf{x}')$（$\mathbf{x}\ne\mathbf{x}'$）。分情况验证：若 $\tilde p(\mathbf{x})q(\mathbf{x}'\mid\mathbf{x}) \le \tilde p(\mathbf{x}')q(\mathbf{x}\mid\mathbf{x}')$，则 $\alpha(\mathbf{x}\to\mathbf{x}')=1$，$\alpha(\mathbf{x}'\to\mathbf{x}) = \frac{\tilde p(\mathbf{x})q(\mathbf{x}'\mid\mathbf{x})}{\tilde p(\mathbf{x}')q(\mathbf{x}\mid\mathbf{x}')}$，于是 $\tilde p(\mathbf{x})q\alpha_1 = \tilde p(\mathbf{x}')q'\alpha_2$ 成立。对称情形同理。∎

**推导：Gibbs 采样保留目标分布为平稳分布**。

Gibbs 每次用满条件 $p(x_i\mid \mathbf{x}_{-i})$ 更新，该更新满足详细平衡（$\alpha=1$ 情形）；整轮扫描是多个满足详细平衡的更新的复合，故目标 $p$ 是平稳分布。∎

---

## 6. 最小可手算例子

**例（二维高斯 Gibbs）**：$p(x,y)$ 为二元正态，均值 0，相关 $\rho = 0.5$。满条件：
$$x \mid y \sim \mathcal{N}(\rho y, 1-\rho^2),\quad y \mid x \sim \mathcal{N}(\rho x, 1-\rho^2)$$

采样序列：$x^{(0)}=0 \to y^{(1)} \sim \mathcal{N}(0, 0.75) \to x^{(1)} \sim \mathcal{N}(0.5y^{(1)}, 0.75) \to \dots$。链逐步进入 $\mathcal{N}(0, \Sigma)$ 的平稳分布。

**例（MH 手算接受率）**：$p \propto e^{-x^2/2}$（标准正态），提议 $q(x'\mid x) = \mathcal{N}(x, 1)$。从 $x=0$ 提议 $x'=1.5$：
$$\alpha = \min\left(1, \frac{e^{-1.125}}{e^0}\right) = e^{-1.125} \approx 0.325$$
（对称提议下 $q$ 比值为 1。）以 32.5% 概率接受 $1.5$，否则停留 $0$。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| 初始样本可以直接用 | **错**。链未收敛（burn-in 期）的样本不来自目标分布，必须丢弃 |
| 相邻样本相互独立 | **错**。MCMC 样本**强相关**（自相关），有效样本量远小于样本数 |
| Gibbs 比 MH 更"准" | **不精确**。两者都渐近精确；Gibbs 无拒绝但要求可采样满条件，且高相关变量收敛慢 |
| MH 的提议必须对称 | **错**。非对称提议用完整比值（含 $q$ 项）修正偏置 |
| 运行越久越好，无需诊断 | **错**。必须做收敛诊断（见 [[概率图模型-MCMC收敛与诊断]]）；不收敛时再久也无用 |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出 MH 接受率公式。
2. Gibbs 采样每步从什么分布采样？

### #自测题/中等
3. 证明 Gibbs 是接受率恒为 1 的 MH。
4. 为什么 MRF 上的 Gibbs 更新只需局部信息？

### #自测题/较难
5. 说明"burn-in 丢弃"和"自相关"如何影响 MCMC 估计的偏差与方差；给出缓解手段。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. $\alpha = \min(1, \frac{\tilde p(x')q(x\mid x')}{\tilde p(x)q(x'\mid x)})$。
2. 满条件分布 $p(x_i \mid \mathbf{x}_{-i})$。
3. 提议 = 满条件，比值分子分母相同 → $\alpha=1$。
4. 满条件只含 $x_i$ 的马尔可夫毯（邻居及共享因子），其余因子视为常数消去。
5. burn-in 样本来自未收敛链 → 引入偏差；自相关使有效样本量 $< N$ → 方差高于独立样本。缓解：丢弃 burn-in、减薄（thinning）、多链、计算 $\hat R$。
</details>

---

## 9. 通过标准

- [ ] 能**默写** MH 与 Gibbs 算法；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**推导** MH 详细平衡与 Gibbs=MH 特例；
- [ ] 能**实现**小模型（如 Ising）的 Gibbs 采样器并做基本诊断。

---

## 10. 来源

- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Chapter 12.3–12.4.
- Stanford CS228 Notes, Lecture 6. https://ermongroup.github.io/cs228-notes/
- Robert & Casella (2004). *Monte Carlo Statistical Methods*. 访问日期：2026-08-07。

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

> 直接下游：[[概率图模型-MCMC收敛与诊断]]、[[概率图模型-高级MCMC]]、阶段 5 的 HMM 采样、课程 Capstone（采样一致性审计）。
