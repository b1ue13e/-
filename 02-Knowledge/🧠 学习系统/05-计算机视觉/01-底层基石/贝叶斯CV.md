---
type: study
course: "05-计算机视觉"
topic: "贝叶斯定理 (Bayes' Theorem)"
created: 2026-08-06
status: planned
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

## 🧪 自测题

1. **(基础)** 贝叶斯定理中，先验 $P(\theta)$ 和似然 $P(D|\theta)$ 的区别是什么？
   <details><summary>💡 提示</summary>先验 = 看到数据前对参数的信念（"θ 大概是什么"）；似然 = 给定参数后数据的概率（"这个 θ 能多好地解释数据"）。</details>

2. **(中等)** 如果把先验设为均匀分布 $P(\theta) = \text{const}$，MAP 退化成什么？
   <details><summary>💡 提示</summary>MAP = MLE。因为 $\log P(\theta)$ 是常数，不参与优化。均匀先验 = "我对参数一无所知"。</details>

3. **(较难)** L2 正则化等价于参数的什么先验分布？L1 正则化呢？
   <details><summary>💡 提示</summary>L2 正则 $\|\mathbf{w}\|^2$ 等价于高斯先验 $\mathbf{w} \sim \mathcal{N}(0, \sigma^2)$；L1 正则 $\|\mathbf{w}\|_1$ 等价于拉普拉斯先验 $\mathbf{w} \sim \text{Laplace}(0, b)$。</details>

---

## 🧪 学完本节后可完成的作业

- 理解 [[Softmax与SVM损失函数|Softmax]] 中的概率解释（Softmax 输出 = 后验概率 $P(y|\mathbf{x})$）
---

## 学完后可以完成

- 完成卡内自测题与闭卷复现（贝叶斯推断）

> 该卡无直接课后/阶段作业：以卡内自测题与闭卷复现作为形成性验收；如需综合实践，可挂靠 HW06 开放课程项目或 CAP01。

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
