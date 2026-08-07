---
type: study
topic: "EM算法"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-学习算法]]"
flow: knowledge
kind: derivation
difficulty: intermediate
upstream: ["[[概率图模型-BN参数学习]]", "[[概率图模型-变分推断与ELBO]]", "[[概率图模型-优化初步]]"]
concept: ["EM算法", "Q函数", "隐变量", "GEM"]
related: ["概率图模型-变分推断算法", "概率图模型-变分EM"]
tags: [概率图模型, EM算法, 隐变量]
---

# 概率图模型-EM算法

> **EM（Expectation-Maximization）** 是含隐变量模型（GMM、HMM、混合 BN）参数学习的**通用框架**：E 步推断隐变量后验，M 步最大化完整数据对数似然的期望。本卡覆盖动机、Q 函数、标准 EM、收敛性（单调性 + 局部最优），以及 GEM/随机 EM 等变体。HMM 的 Baum-Welch 是 EM 的链式特例（阶段 5）。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：模型含隐变量 $\mathbf{Z}$（如 GMM 的簇标签、HMM 的隐状态），观测数据 $\mathcal{D} = \{\mathbf{x}\}$ 的对数似然 $\ell(\theta) = \sum_t \log P(\mathbf{x}^{(t)}\mid\theta) = \sum_t \log\sum_{\mathbf{z}} P(\mathbf{x}^{(t)},\mathbf{z}\mid\theta)$ 中，**对隐变量求和使 log 无法进入和号**，MLE 无闭式解、直接梯度也麻烦。EM 通过"E 步填缺失、M 步更新"迭代逼近 MLE。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：EM 是隐变量模型的"瑞士军刀"——GMM、HMM（Baum-Welch）、LDA（变分 EM）、带缺失数据的 BN 都用它；它是"推断-学习交替"范式的原型（与变分 EM 衔接）。
- **实际应用场景**：聚类（GMM）、语音识别（HMM 训练）、推荐系统的隐因子模型。
- **高频考点**：Q 函数定义、E 步/M 步推导、单调性证明、局部最优问题、GMM 的 EM 更新。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-BN参数学习]]**：完全数据 MLE 的闭式。
2. **[[概率图模型-变分推断与ELBO]]**：ELBO/下界思想（EM 的单调性证明用它）。
3. **[[概率图模型-贝叶斯规则与条件独立]]**：后验推断。

---

## 4. 定义与核心公式

### 4.1 不完全数据问题

**完整数据** $(\mathbf{x}, \mathbf{z})$：似然可分解（BN 可逐 CPT 计数）。**观测数据** $\mathbf{x}$：隐变量被求和掉，$\ell(\theta) = \sum_t \log \sum_z P(\mathbf{x}^{(t)}, z\mid\theta)$——不可分解、难优化。

### 4.2 Q 函数

**定义**：E 步计算"完整数据对数似然在隐变量后验下的期望"：

$$Q(\theta \mid \theta^{\text{old}}) = \mathbb{E}_{P(\mathbf{Z}\mid\mathbf{X},\theta^{\text{old}})}[\log P(\mathbf{X}, \mathbf{Z}\mid\theta)]$$

### 4.3 EM 算法

**算法**（重复直到收敛）：
- **E 步**：用当前参数 $\theta^{\text{old}}$ 计算隐变量后验 $P(\mathbf{Z}\mid\mathbf{X},\theta^{\text{old}})$，构造 $Q(\theta\mid\theta^{\text{old}})$；
- **M 步**：$\theta^{\text{new}} = \arg\max_\theta Q(\theta\mid\theta^{\text{old}})$。

**GMM 的 EM 更新**（$K$ 个高斯，$N$ 样本）：
- E 步：责任 $\gamma_{tk} = P(z_t = k\mid x_t, \theta^{\text{old}}) = \frac{\pi_k \mathcal{N}(x_t;\mu_k,\Sigma_k)}{\sum_j \pi_j \mathcal{N}(x_t;\mu_j,\Sigma_j)}$；
- M 步：$\pi_k = \frac{N_k}{N}$，$\mu_k = \frac{\sum_t \gamma_{tk}x_t}{N_k}$，$\Sigma_k = \frac{\sum_t \gamma_{tk}(x_t-\mu_k)(x_t-\mu_k)^\top}{N_k}$（$N_k = \sum_t\gamma_{tk}$）。

### 4.4 收敛性

**单调性定理**：$\ell(\theta^{\text{new}}) \ge \ell(\theta^{\text{old}})$（对数似然单调不降）。

**证明思路**（用 ELBO 视角）：$\log P(\mathbf{x}\mid\theta) = \mathcal{L}(q,\theta) + \text{KL}(q \parallel P(\cdot\mid\mathbf{x},\theta))$，其中 $\mathcal{L}(q,\theta) = \mathbb{E}_q[\log P(\mathbf{x},\mathbf{z}\mid\theta)] - \mathbb{E}_q[\log q(\mathbf{z})]$。
- E 步：$q = P(\cdot\mid\mathbf{x},\theta^{\text{old}})$ 使 KL = 0，$\mathcal{L} = \ell(\theta^{\text{old}})$；
- M 步：最大化 $Q$（= $\mathcal{L}$ 去掉与 $\theta$ 无关的熵项），$\mathcal{L}(\theta^{\text{new}}) \ge \mathcal{L}(\theta^{\text{old}}) = \ell(\theta^{\text{old}})$；
- 因 $\mathcal{L}(\theta^{\text{new}}) \le \ell(\theta^{\text{new}})$，得 $\ell(\theta^{\text{new}}) \ge \ell(\theta^{\text{old}})$。∎

**局限**：似然非凸时 EM 只保证收敛到**局部最优**（依赖初始化）；且收敛可能很慢（E 步对病态后验代价高）。

### 4.5 变体

| 变体 | 改进 | 场景 |
|:---|:---|:---|
| **GEM（广义 EM）** | M 步只提高 $Q$ 而不必全局最大 | M 步无闭式/昂贵 |
| **随机 EM** | E 步用小批量近似后验 | 大规模数据 |
| **变分 EM** | E 步用变分近似后验（后验不可解时） | 复杂后验（LDA） |

---

## 5. 关键推导

**推导：GMM 的 E 步（责任）**。

$P(z_t = k\mid x_t,\theta) = \frac{P(x_t\mid z_t=k)P(z_t=k)}{\sum_j P(x_t\mid z_t=j)P(z_t=j)} = \frac{\pi_k\mathcal{N}(x_t;\mu_k,\Sigma_k)}{\sum_j\pi_j\mathcal{N}(x_t;\mu_j,\Sigma_j)}$——贝叶斯规则直接代入。∎

**推导：GMM 的 M 步（均值）**。

$Q = \sum_t\sum_k\gamma_{tk}\left[\log\pi_k + \log\mathcal{N}(x_t;\mu_k,\Sigma_k)\right]$。对 $\mu_k$ 求导置零：$\sum_t\gamma_{tk}\Sigma_k^{-1}(x_t - \mu_k) = 0 \Rightarrow \mu_k = \frac{\sum_t\gamma_{tk}x_t}{\sum_t\gamma_{tk}}$。∎

**推导：EM 单调性（完整版）**。

设 $q = P(\mathbf{z}\mid\mathbf{x},\theta^{\text{old}})$。E 步后 $\mathcal{L}(q,\theta^{\text{old}}) = \ell(\theta^{\text{old}})$。M 步使 $Q(\theta^{\text{new}}\mid\theta^{\text{old}}) \ge Q(\theta^{\text{old}}\mid\theta^{\text{old}})$，而 $Q = \mathcal{L} + \mathbb{E}_q[\log q]$（熵项与 $\theta$ 无关），故 $\mathcal{L}(q,\theta^{\text{new}}) \ge \ell(\theta^{\text{old}})$。又 $\ell(\theta) \ge \mathcal{L}(q,\theta)$（KL ≥ 0）对任意 $\theta$ 成立，故 $\ell(\theta^{\text{new}}) \ge \mathcal{L}(q,\theta^{\text{new}}) \ge \ell(\theta^{\text{old}})$。∎

---

## 6. 最小可手算例子

**例（二分量 GMM，一步 EM）**：$K=2$，数据 $\{x\} = \{0, 10\}$，初始 $\pi = (0.5, 0.5)$，$\mu = (0, 5)$，$\Sigma = (1, 1)$。

**E 步**：
- $\gamma_{11} = \frac{0.5\mathcal{N}(0;0,1)}{0.5\mathcal{N}(0;0,1)+0.5\mathcal{N}(0;5,1)} = \frac{0.199}{0.199+1.35\times10^{-6}} \approx 1.0$（$x=0$ 几乎全属簇 1）；
- $\gamma_{22} \approx 1.0$（$x=10$ 几乎全属簇 2）。

**M 步**：$\mu_1 \approx 0$，$\mu_2 \approx 10$，$\pi = (0.5,0.5)$——一步后均值大幅移向数据点，继续迭代收敛。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| EM 保证全局最优 | **错**。仅局部最优（似然非凸）；依赖初始化，需多起点 |
| E 步要计算完整后验分布 | **一般对**。需要后验的充分统计量；变分 EM 在不可解时近似 |
| EM 只能用于聚类 | **错**。任何含隐变量模型（HMM、缺失数据、混合模型）都可用 |
| $\ell$ 单调上升 = 已收敛 | **近似对**。还需检查参数/似然变化量小于阈值；EM 后期可能极慢 |
| M 步必须闭式 | **错**。GEM 允许部分优化；数值优化亦可（EM 梯度变体） |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出 Q 函数定义。
2. EM 的 E 步和 M 步各做什么？

### #自测题/中等
3. 推导 GMM 的责任公式与均值更新。
4. 用 ELBO 视角证明 EM 单调性。

### #自测题/较难
5. 为什么 EM 只收敛到局部最优？给出一个可能失败的例子（如 GMM 分量坍缩）。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. $Q(\theta\mid\theta^{old}) = \mathbb{E}_{P(Z\mid X,\theta^{old})}[\log P(X,Z\mid\theta)]$。
2. E 步：计算隐变量后验并构造 Q；M 步：最大化 Q 更新参数。
3. 见 §5 推导。
4. 见 §5 推导（$\ell \ge \mathcal{L}$，KL ≥ 0）。
5. 目标非凸：EM 沿"当前后验下的下界"上升，不同初始后验导向不同局部最优；GMM 可能收敛到分量坍缩（某分量方差 → 0 的退化解），需正则/重初始化。
</details>

---

## 9. 通过标准

- [ ] 能**默写** Q 函数、EM 算法与 GMM 更新；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**证明** EM 单调性（ELBO 视角）；
- [ ] 能**说明** EM 的局部最优与变体取舍。

---

## 10. 来源

- Dempster, Laird & Rubin (1977). Maximum likelihood from incomplete data via the EM algorithm. *JRSS-B*.
- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Chapter 19.
- Bishop (2006). *PRML*, Springer. §9. 访问日期：2026-08-07。

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

> 直接下游：[[概率图模型-变分EM]]、阶段 5 的 [[BW重估计]]（HMM 的 EM）、阶段 6 的 [[LDA推断]]、课程 Capstone（EM 部分）。
