---
type: study
topic: "MRF参数学习"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-学习算法]]"
flow: knowledge
kind: derivation
difficulty: advanced
upstream: ["[[概率图模型-马尔可夫随机场]]", "[[概率图模型-优化初步]]", "[[概率图模型-Gibbs与MH采样]]"]
concept: ["配分函数", "对比散度", "伪似然", "极大似然"]
related: ["概率图模型-BN参数学习", "概率图模型-马尔可夫随机场"]
tags: [概率图模型, 参数学习, MRF]
---

# 概率图模型-MRF参数学习

> 与 BN 的"数数即得"不同，MRF 参数学习**没有闭式解**：似然含配分函数 $Z(\theta)$，其梯度涉及对模型的期望。本卡讲解问题的本质（似然梯度 = 数据期望 − 模型期望）、精确梯度不可行性，以及两条实用路线：**对比散度（CD）**与**伪似然（PL）**。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：MRF 的联合分布 $P_\theta(\mathbf{x}) = \frac{1}{Z(\theta)}\prod_C\psi_C(\mathbf{x}_C)$，其中 $Z(\theta)$ 对全部状态求和。最大似然的目标梯度包含"模型期望"项，而模型期望无法精确计算（$Z$ 不可得）——所以 MRF 学习是"没有免费午餐"的推断-学习耦合问题。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：MRF 学习是深度能量模型（EBM）、CRF 学习的原型；CD 是 RBM/深度玻尔兹曼机训练的核心；伪似然是结构简单但稳定的基线。
- **实际应用场景**：图像去噪模型训练（Ising 参数）、CRF 势函数学习、能量模型拟合。
- **高频考点**：似然梯度分解、为什么模型期望难算、CD-k 的近似逻辑、伪似然目标。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-马尔可夫随机场]]**：势函数、$Z$、能量形式。
2. **[[概率图模型-Gibbs与MH采样]]**：从模型分布采样的方法（CD 需要）。
3. **[[概率图模型-优化初步]]**：梯度下降。

---

## 4. 定义与核心公式

### 4.1 对数似然梯度（核心公式）

设 $\psi_C(\mathbf{x}_C) = \exp(\theta_C \cdot f_C(\mathbf{x}_C))$（特征函数线性参数化），则

$$\log P_\theta(\mathbf{x}) = \sum_C \theta_C \cdot f_C(\mathbf{x}_C) - \log Z(\theta)$$

**梯度**：

$$\nabla_{\theta_C} \log P_\theta(\mathbf{x}) = f_C(\mathbf{x}_C) - \mathbb{E}_{P_\theta}[f_C(\mathbf{X}_C)]$$

对数据 $\mathcal{D}$：$\nabla \ell(\theta) = \frac{1}{N}\sum_t f_C(\mathbf{x}_C^{(t)}) - \mathbb{E}_{P_\theta}[f_C(\mathbf{X}_C)]$

**解读**：**数据期望 − 模型期望**。第一项（数据侧）可从样本统计；第二项（模型侧）需要对 $P_\theta$ 求期望——**这就是难点**（$Z$ 不可算）。

### 4.2 为什么模型期望难算

$\mathbb{E}_{P_\theta}[f_C] = \sum_\mathbf{x} f_C(\mathbf{x}_C) P_\theta(\mathbf{x})$：对全部状态求和，指数级；无闭式（除非树/特殊结构）。必须**近似**——这正是 MCMC/CD 的用武之地。

### 4.3 对比散度（Contrastive Divergence, CD-k）

**思想**：不用收敛的 MCMC（太慢），而是**从数据点出发**跑 $k$ 步 Gibbs（$k$ 通常 1），用得到的"近似模型样本"替代模型期望：

$$\nabla_{\theta_C} \ell \approx \frac{1}{N}\sum_t f_C(\mathbf{x}_C^{(t)}) - \frac{1}{N}\sum_t f_C(\hat{\mathbf{x}}_C^{(t)})$$

其中 $\hat{\mathbf{x}}^{(t)}$ 从 $\mathbf{x}^{(t)}$ 出发跑 $k$ 步 Gibbs 采样。

**直觉**：$k$ 步 Gibbs 从数据邻域出发，很快到达模型分布"附近"——用局部近似代替全局期望，偏差小、方差可控。CD-1 是最常用形式。

**局限**：CD 是**有偏**的（不是真梯度）；$k$ 增大偏差减小但计算增加；对多峰模型 CD 可能漏掉模式。

### 4.4 伪似然（Pseudo-Likelihood, PL）

**思想**：用条件分布乘积近似联合似然（避免 $Z$）：

$$\ell_{\text{PL}}(\theta) = \sum_{t} \sum_i \log P_\theta(x_i^{(t)} \mid \mathbf{x}_{-i}^{(t)})$$

**关键**：每项 $P_\theta(x_i \mid \mathbf{x}_{-i})$ 的分母只对 $x_i$ 求和（$|x_i|$ 项），**无需全局 $Z$**——可精确计算。

**性质**：PL 是**一致**估计（$N\to\infty$ 收敛到真参数），但**有偏**（低估依赖强度）；实现简单、稳定，是 MRF 学习的实用基线。

---

## 5. 关键推导

**推导：似然梯度公式**。

$\frac{\partial}{\partial\theta_C}\log P_\theta(\mathbf{x}) = f_C(\mathbf{x}_C) - \frac{1}{Z}\frac{\partial Z}{\partial\theta_C}$，而 $\frac{\partial Z}{\partial\theta_C} = \sum_\mathbf{x} f_C(\mathbf{x}_C) e^{\sum\theta f} = Z \cdot \mathbb{E}_{P_\theta}[f_C]$。代入即得。∎

**推导：伪似然避免 $Z$**。

$P_\theta(x_i\mid\mathbf{x}_{-i}) = \frac{P_\theta(\mathbf{x})}{\sum_{x_i}P_\theta(\mathbf{x})}$。分子分母共享因子 $\exp(\sum_{C: i\notin C}\theta_C f_C)$（不含 $x_i$ 的项），约掉后只剩含 $x_i$ 的团的项，分母对 $x_i$ 求和（$|x_i|$ 项）。∎

**推导：PL 一致性直觉**。
PL 最大化的是条件分布的乘积，其期望梯度为 0 的解满足"每个条件分布都匹配数据的条件分布"——在一般位置下这些条件分布唯一确定联合分布（正分布情形），故一致。∎

---

## 6. 最小可手算例子

**例（Ising 单边参数）**：2 变量 $X_1, X_2$，$P_\theta(x_1,x_2) \propto \exp(\theta \cdot \mathbb{1}[x_1=x_2])$。数据：$(1,1),(1,1),(1,0)$。

**数据期望**：$\frac{1}{3}(1+1+0) = 2/3$。

**模型期望**（精确，本例可算）：$Z = e^\theta + e^\theta + 1 + 1 = 2e^\theta + 2$；$\mathbb{E}[f] = \frac{2e^\theta}{2e^\theta+2} = \frac{e^\theta}{e^\theta+1}$。

**梯度方程**：$\frac{2}{3} - \frac{e^\theta}{e^\theta+1} = 0 \Rightarrow e^\theta = 2 \Rightarrow \theta = \ln 2 \approx 0.693$。

**CD-1 对比**：若从数据点跑 1 步 Gibbs 得近似模型样本 $\hat x$（此处略），用 $\frac{1}{3}\sum f(\hat x)$ 近似模型期望。

**伪似然**：$\ell_{PL} = \log P(x_1\mid x_2) + \log P(x_2\mid x_1)$ 各项只含局部归一化，可直接梯度上升。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| MRF 参数学习有闭式解 | **错**。模型期望含 $Z$，无闭式（树结构除外） |
| CD-1 是精确梯度 | **错**。CD 是有偏近似；$k$ 步 Gibbs 未收敛，只是低方差近似 |
| 伪似然 = 联合似然 | **错**。PL 是条件分布乘积近似，有偏（低估依赖）；但一致 |
| 模型期望可以忽略 | **错**。忽略模型期望 = 只增数据项 = 似然发散（退化为最大化特征均值） |
| Gibbs 采样必须收敛才能用 | **部分错**。CD 故意用短链（$k=1$）作低方差近似；真 MLE 才需收敛采样 |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出 MRF 对数似然梯度公式并解释两项含义。
2. 为什么模型期望难计算？

### #自测题/中等
3. 说明 CD-k 的近似逻辑与偏差来源。
4. 伪似然如何避免计算 $Z$？

### #自测题/较难
5. 对比 CD 与 PL 的偏差特性与适用场景。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. $\nabla\ell = \frac1N\sum_t f_C(x^{(t)}_C) - \mathbb{E}_{P_\theta}[f_C]$：数据期望（统计量）− 模型期望（难算）。
2. $\mathbb{E}_{P_\theta}[f_C] = \sum_\mathbf{x} f_C P_\theta(\mathbf{x})$，对全部状态指数级求和，$Z$ 不可得。
3. 从数据点跑 $k$ 步 Gibbs 得到模型"邻域样本"，用样本平均近似模型期望；偏差来自链未收敛。
4. 用条件分布 $P_\theta(x_i\mid x_{-i})$ 乘积，分母只对 $x_i$ 求和，无全局 $Z$。
5. CD：低偏差（$k$ 大时接近真梯度）但需采样、对多峰不稳；PL：无采样、稳定、实现简单，但偏差大（低估依赖）。大数据简单模型用 PL，精确拟合用 CD/MCMC-MLE。
</details>

---

## 9. 通过标准

- [ ] 能**默写**似然梯度、CD 更新、伪似然目标；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**推导**梯度公式与 PL 无 $Z$ 的原因；
- [ ] 能**选择** MRF 学习的实用方法并说明取舍。

---

## 10. 来源

- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Chapter 20.
- Hinton (2002). Training products of experts by minimizing contrastive divergence. *Neural Computation*.
- Besag (1975). Statistical analysis of non-lattice data. *JRSS-B*. 访问日期：2026-08-07。

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

> 直接下游：阶段 5 的 [[CRF学习]]、阶段 6 的能量模型/扩散模型训练、课程 Capstone。
