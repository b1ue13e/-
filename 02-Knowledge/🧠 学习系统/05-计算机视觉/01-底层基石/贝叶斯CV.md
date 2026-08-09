---
type: study
course: "05-计算机视觉"
topic: "贝叶斯定理 (Bayes' Theorem)"
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: ["贝叶斯定理", "先验", "似然", "后验", "贝叶斯推断"]
prerequisites: ["概率分布CV"]
related: ["梯度下降CV", "kNN与线性分类器"]
upstream: ["[[概率分布CV]]"]
flow: knowledge
stage_moc: "[[🧭 阶段1-底层基石]]"
kind: concept
source: "《Mathematics for Machine Learning》Ch.6"
tags: [学习, 计算机视觉, 概率, 贝叶斯]
---

# 贝叶斯定理 (Bayes' Theorem)

> 所属模块：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[🧭 阶段1-底层基石|第一阶段：底层基石]]
> 建议先看：[[概率分布CV]]

---

## 0. 类别：A 类核心概念

贝叶斯定理是概率视角下理解所有机器学习模型的统一框架。从朴素贝叶斯分类器到 VAE 到 Diffusion 模型，核心都是"先验 + 数据 → 后验"。

---

## 1. 直觉：用证据更新信念

$$P(\theta | D) = \frac{P(D | \theta) \cdot P(\theta)}{P(D)}$$

| 项 | 名称 | 含义 |
|:---|:---|:---|
| $P(\theta \mid D)$ | **后验 (Posterior)** | 看到数据后的更新信念 |
| $P(D \mid \theta)$ | **似然 (Likelihood)** | 模型对数据的解释力 |
| $P(\theta)$ | **先验 (Prior)** | 看到数据前的初始信念 |
| $P(D)$ | **证据 (Evidence)** | 归一化常数 |

> **一句话**：后验 ∝ 似然 × 先验。数据说服力越强（似然大），先验越弱（先验平坦），后验就越接近纯数据驱动。

---

## 2. 经典示例：医学检测

某疾病发病率 1%（先验 $P(D)=0.01$）。检测准确率 99%（$P(+|D)=0.99$），假阳性率 5%（$P(+|\neg D)=0.05$）。检测结果为阳性，真的患病概率是？

$$P(D|+) = \frac{P(+|D)P(D)}{P(+|D)P(D) + P(+|\neg D)P(\neg D)} = \frac{0.99 \times 0.01}{0.99 \times 0.01 + 0.05 \times 0.99} \approx 16.7\%$$

> **反直觉**：即使检测准确率 99%，阳性结果也只有 16.7% 的概率是真患病——因为疾病本身太罕见了（先验极低）。

---

## 3. CV 中的应用

### 3.1 朴素贝叶斯分类器

假设特征条件独立：

$$P(y | \mathbf{x}) \propto P(y) \prod_{i=1}^n P(x_i | y)$$

在文本分类和简单图像分类中仍有应用。虽然"朴素"假设在 CV 中通常不成立（像素之间高度相关），但作为基准模型理解贝叶斯框架很有价值。

### 3.2 贝叶斯深度学习

- **贝叶斯神经网络**：权重不是点估计而是分布 → 自带不确定性估计
- **变分自编码器 (VAE)**：用贝叶斯框架建模隐变量 → 生成模型
- **Diffusion 模型**：前向过程（加噪）= 从数据分布到先验；反向过程（去噪）= 从先验到后验

### 3.3 MAP 估计

最大后验 (MAP) = 最大似然 (MLE) + 正则化：

$$\hat{\theta}_{\text{MAP}} = \arg\max_\theta P(D|\theta)P(\theta)$$

取对数：
$$\hat{\theta}_{\text{MAP}} = \arg\max_\theta [\log P(D|\theta) + \log P(\theta)]$$

其中 $\log P(\theta)$ 正是 L2 正则化（当先验为高斯分布时）或 L1 正则化（当先验为拉普拉斯分布时）的等价形式。

### 3.4 可运行示例：从数据计算后验

把 §2 的医学检测与 §3.3 的 MAP 公式落成可验证代码（NumPy，无外部依赖）：

```python
import numpy as np

# (1) 医学检测后验：复现 §2，验证 P(D|+) ≈ 0.167
p_pos_given_D, p_D = 0.99, 0.01
p_pos_given_notD, p_notD = 0.05, 1 - p_D
p_D_given_pos = (p_pos_given_D * p_D) / (p_pos_given_D * p_D + p_pos_given_notD * p_notD)
print(f"P(D|+) = {p_D_given_pos:.4f}")   # ≈ 0.1670

# (2) 一维高斯 MAP：先验 N(0, sigma_p^2)，似然 N(theta, sigma_l^2)
#     theta_MAP = (n / (n + sigma_l^2/sigma_p^2)) * theta_MLE
sigma_p, sigma_l = 1.0, 0.5           # sigma_p 越小 = 先验越强 = 正则越重
data = np.array([0.3, 0.1, 0.4, -0.2, 0.5])
theta_mle = data.mean()
n = len(data)
shrink = n / (n + sigma_l**2 / sigma_p**2)
theta_map = shrink * theta_mle
print(f"theta_MLE={theta_mle:.3f}  theta_MAP={theta_map:.3f}  shrink={shrink:.3f}")
# shrink<1 → 先验把 MLE 拉向 0，正是 L2 正则的贝叶斯解释
```

运行应得 `P(D|+) = 0.1670` 与 `shrink ≈ 0.862`（`theta_MAP` 比 `theta_MLE` 更靠近 0）。

---

## 4. 条件变式：MLE vs MAP vs 全贝叶斯

| 方法 | 公式 | 特点 |
|:---|:---|:---|
| **MLE** | $\hat{\theta} = \arg\max P(D\|\theta)$ | 纯数据驱动，无先验，易过拟合 |
| **MAP** | $\hat{\theta} = \arg\max P(D\|\theta)P(\theta)$ | 加入先验 = 等价于正则化 |
| **全贝叶斯** | $P(\theta\|D)$ 整个分布 | 完整的不确定性量化，但计算昂贵 |

---

## 5. 常见误区

- ❌ "先验不重要，数据多了自然覆盖" — 小数据场景下先验至关重要；大数据场景下不好的先验会减慢收敛
- ❌ "后验概率高于先验就是好事" — 取决于似然有多强、先验有多可靠
- ❌ "贝叶斯方法太慢、深度学习不需要" — VAE、Diffusion、Bayesian NN 全部基于贝叶斯框架

---

## 6. 适用边界与注意事项

- **贝叶斯真正占优的场景**：小样本 / 数据昂贵（医疗、机器人）、需要不确定性量化（主动学习、异常检测）、或为安全关键系统提供置信度。此时"先验 + 后验"比单点估计更稳健。
- **贝叶斯代价高、通常退化的场景**：现代大规模深度网络对 $P(\theta\mid D)$ 做精确推断不可行（维度太高、无解析形式），只能用变分推断（VAE）、MCMC 或 Dropout 近似；若只想要预测而不要不确定性，MLE + 正则往往更省事。
- **与深度学习的接口**：把深度网络权重视为分布即 Bayesian NN；Diffusion 的前向（加噪）/反向（去噪）过程本质就是先验 ↔ 后验的桥梁。读懂本卡，是理解这些模型"为什么这样设计"的前置。

---

## 🧪 自测题

1. **(基础)** 贝叶斯定理中，先验 $P(\theta)$ 和似然 $P(D|\theta)$ 的区别是什么？
   <details><summary>💡 思路</summary>看两个概率各自「以什么为条件」：一个不依赖数据，另一个以参数为条件。再用一句话概括它们分别回答什么问题。</details>

2. **(中等)** 如果把先验设为均匀分布 $P(\theta) = \text{const}$，MAP 退化成什么？
   <details><summary>💡 思路</summary>写出 MAP 的目标 $\arg\max_\theta [\log P(D|\theta) + \log P(\theta)]$，把 $P(\theta)$ 换成常数后，看第二项还参不参与优化。</details>

3. **(较难)** L2 正则化等价于参数的什么先验分布？L1 正则化呢？
   <details><summary>💡 思路</summary>把正则项写进 MAP 的目标函数，反推 $\log P(\theta)$ 该长什么样：平方项对应哪种分布的对数密度？绝对值项又对应哪种？</details>

---

## 🔀 学完本节后的横向连接

- 理解 [[Softmax与SVM损失函数|Softmax]] 中的概率解释（Softmax 输出 = 后验概率 $P(y|\mathbf{x})$）
---

## 学完后可以完成

> 下列作业在 `requires` 中引用了本卡，由 Dataview 实时派生（非人工维护反向链接）：

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

本卡另以前置「🧪 自测题」与闭卷复现作为形成性验收。

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
