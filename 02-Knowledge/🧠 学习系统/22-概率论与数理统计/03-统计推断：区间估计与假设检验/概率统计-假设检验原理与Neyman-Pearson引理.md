---
type: study
topic: "概率统计-假设检验原理与Neyman-Pearson引理"
course: "22-概率论与数理统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段3-统计推断：区间估计与假设检验]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["假设检验", "原假设与备择假设", "第一类错误", "第二类错误", "功效函数", "显著性水平", "Neyman-Pearson引理", "似然比检验"]
upstream: ["[[概率统计-参数区间估计与枢轴量法]]"]
related: ["[[概率统计-经典参数假设检验：Z检验、t检验、卡方与F检验]]", "[[概率统计-似然比检验与拟合优度检验]]"]
tags: [学习, 概率论与数理统计, 假设检验, 两类错误, 功效函数, NP引理]
---

# 概率统计-假设检验原理与Neyman-Pearson引理

---

## 1. 核心数学定义

### 1. 原假设与备择假设
设总体分布依赖未知参数 $\theta \in \Theta$。将参数空间划分为两个不相交子集 $\Theta_0$ 与 $\Theta_1$（$\Theta_0 \cap \Theta_1 = \emptyset$）：
- **原假设（Null Hypothesis, $H_0$）**：$H_0: \theta \in \Theta_0$（通常代表无效应、无差异、现状）；
- **备择假设（Alternative Hypothesis, $H_1$）**：$H_1: \theta \in \Theta_1$（代表研究者希望通过证据证实的效应）。

### 2. 检验规则与拒绝域（Critical Region）
一个检验规则对应于样本空间 $\mathcal{X}$ 中的一个子集 $W \subseteq \mathcal{X}$，称为**拒绝域**：
- 当样本 $\mathbf{X} \in W$ 时，**拒绝 $H_0$**（接受 $H_1$）；
- 当样本 $\mathbf{X} \notin W$ 时，**不拒绝 / 接受 $H_0$**。

### 3. 两类错误对照表

| 真实状态 \ 统计决策 | 接受 $H_0$ ($\mathbf{X} \notin W$) | 拒绝 $H_0$ ($\mathbf{X} \in W$) |
| :---: | :---: | :---: |
| **$H_0$ 为真 ($\theta \in \Theta_0$)** | 正确决策（概率 $1-\alpha$） | **第一类错误（弃真 / 假阳性 Type I Error）**<br>概率 $\alpha = P_{\theta}(\mathbf{X} \in W)$ |
| **$H_1$ 为真 ($\theta \in \Theta_1$)** | **第二类错误（取伪 / 假阴性 Type II Error）**<br>概率 $\beta = P_{\theta}(\mathbf{X} \notin W)$ | 正确决策 / 检验功效（Power）<br>概率 $1-\beta = P_{\theta}(\mathbf{X} \in W)$ |

### 4. 功效函数（Power Function）
定义对任意 $\theta \in \Theta$，拒绝原假设的概率为**功效函数**：
$$\beta(\theta) = P_\theta(\mathbf{X} \in W)$$
- 当 $\theta \in \Theta_0$ 时，$\beta(\theta) \le \alpha$（犯第一类错误的概率）；
- 当 $\theta \in \Theta_1$ 时，$\beta(\theta) = 1 - \beta$（正确拒绝错误原假设的概率，即 **检验功效 Power**）。

---

## 2. 奈曼-皮尔逊基本引理（Neyman-Pearson Lemma）

### 定理陈述（简单假设对简单假设的最优检验）
考虑简单假设检验问题：
$$H_0: \theta = \theta_0 \quad \text{vs} \quad H_1: \theta = \theta_1$$
设样本 $\mathbf{X}$ 在两假设下的联合似然函数分别为 $L(\theta_0; \mathbf{x})$ 和 $L(\theta_1; \mathbf{x})$。
定义**似然比检验拒绝域**：
$$W^* = \left\{\mathbf{x} : \frac{L(\theta_1; \mathbf{x})}{L(\theta_0; \mathbf{x})} \ge k\right\}$$
其中阈值 $k \ge 0$ 选取使得显著性水平刚好为 $\alpha$，即 $P_{\theta_0}(\mathbf{X} \in W^*) = \alpha$。

**结论**：在所有显著性水平满足 $P_{\theta_0}(\mathbf{X} \in W) \le \alpha$ 的检验中，$W^*$ 具有**最大的检验功效**，即对任意其他拒绝域 $W$：
$$P_{\theta_1}(\mathbf{X} \in W^*) \ge P_{\theta_1}(\mathbf{X} \in W)$$
该检验称为**一致最优势检验（Most Powerful Test, MP 检验）**。

---

## 3. Neyman-Pearson 引理严格数学证明

**证明**：
设 $W$ 为任意满足 $P_{\theta_0}(\mathbf{X} \in W) \le \alpha$ 的拒绝域。我们需证明 $\int_{W^*} L(\theta_1) d\mathbf{x} - \int_W L(\theta_1) d\mathbf{x} \ge 0$。
1. 将积分区间拆解为交集与差集：
   $$\int_{W^*} L(\theta_1) d\mathbf{x} - \int_W L(\theta_1) d\mathbf{x} = \int_{W^* \setminus W} L(\theta_1) d\mathbf{x} - \int_{W \setminus W^*} L(\theta_1) d\mathbf{x}$$
2. 由拒绝域 $W^*$ 的定义：
   - 当 $\mathbf{x} \in W^* \setminus W \subseteq W^*$ 时，有 $L(\theta_1; \mathbf{x}) \ge k L(\theta_0; \mathbf{x})$；
   - 当 $\mathbf{x} \in W \setminus W^* \subseteq (W^*)^c$ 时，有 $L(\theta_1; \mathbf{x}) < k L(\theta_0; \mathbf{x})$。
3. 放大缩小不等式：
   $$\int_{W^* \setminus W} L(\theta_1) d\mathbf{x} \ge k \int_{W^* \setminus W} L(\theta_0) d\mathbf{x}$$
   $$\int_{W \setminus W^*} L(\theta_1) d\mathbf{x} \le k \int_{W \setminus W^*} L(\theta_0) d\mathbf{x}$$
4. 代入差式：
   $$\int_{W^*} L(\theta_1) d\mathbf{x} - \int_W L(\theta_1) d\mathbf{x} \ge k \left( \int_{W^* \setminus W} L(\theta_0) d\mathbf{x} - \int_{W \setminus W^*} L(\theta_0) d\mathbf{x} \right) = k \left( \int_{W^*} L(\theta_0) d\mathbf{x} - \int_W L(\theta_0) d\mathbf{x} \right)$$
5. 因为 $\int_{W^*} L(\theta_0) d\mathbf{x} = \alpha$，而 $\int_W L(\theta_0) d\mathbf{x} \le \alpha$，故括号内 $\alpha - P_{\theta_0}(W) \ge 0$。
   由于 $k \ge 0$，整体差值 $\ge 0$。
   即 $P_{\theta_1}(\mathbf{X} \in W^*) \ge P_{\theta_1}(\mathbf{X} \in W)$。 $\blacksquare$

---

## 4. Python 功效曲线模拟

```python
import numpy as np
import scipy.stats as stats

# 正态均值单边检验: H0: mu = 0 vs H1: mu > 0 (已知 sigma=1, n=25, alpha=0.05)
n = 25
sigma = 1.0
se = sigma / np.sqrt(n) # 0.2
z_crit = stats.norm.ppf(0.95) # 1.6449
c = 0 + z_crit * se # 拒绝域: X_bar > 0.32898

# 计算真实 mu 从 -0.5 到 1.0 的理论功效函数与模拟功效
mu_range = np.linspace(-0.5, 1.0, 50)
theory_power = 1 - stats.norm.cdf((c - mu_range) / se)

# 蒙特卡洛模拟验证
sim_power = []
for mu in mu_range:
    samples = np.random.normal(mu, sigma, size=(10_000, n))
    x_bars = samples.mean(axis=1)
    rejections = (x_bars > c).mean()
    sim_power.append(rejections)

# 当 mu=0 时，功效必须恰为 alpha=0.05
alpha_sim = sim_power[np.argmin(np.abs(mu_range - 0.0))]
print(f"mu=0 处的实际假阳性率 (alpha): {alpha_sim:.4f} (理论 0.0500)")
assert abs(alpha_sim - 0.05) < 0.008, "第一类错误控制检验失败！"
```

---

## 5. 闭卷自测

- [ ] 写出第一类错误 $\alpha$ 与第二类错误 $\beta$ 的条件概率定义；
- [ ] 默写 Neyman-Pearson 基本引理陈述；
- [ ] 独立写出 NP 引理利用拆分积分证明最优势性的五步主线。

---

## 6. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
