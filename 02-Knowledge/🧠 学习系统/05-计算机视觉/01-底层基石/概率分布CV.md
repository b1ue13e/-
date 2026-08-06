---
type: study
course: "05-计算机视觉"
topic: "概率分布与贝叶斯推断"
created: 2026-08-05
status: ongoing
difficulty: beginner
concept: ["概率分布", "贝叶斯定理", "高斯分布", "最大似然", "先验后验"]
prerequisites: ["高中数学"]
related: ["图像分类", "Softmax损失", "生成模型VAE"]
flow: knowledge
stage_moc: "[[🏗️ 第一阶段：底层基石]]"
kind: concept
source: "《Mathematics for Machine Learning》Ch.6"
anki_deck: "05-计算机视觉::01-底层基石"
anki_tags: ["计算机视觉", "概率", "贝叶斯"]
tags: [学习, 计算机视觉, 概率, 贝叶斯]
---

# 概率分布与贝叶斯推断

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：概率与贝叶斯推断是计算机视觉的"底层语言"。从图像去噪（噪声是随机变量）到图像分类（输出是类别后验概率）、从目标检测（边界框回归的不确定性）到生成模型（VAE、Diffusion 本质上都在建模概率分布）——不理解概率，就无法读懂 CV 论文中 80% 的公式。贝叶斯定理更是贯穿整个机器学习：先验 → 似然 → 后验这条链，是理解正则化、不确定性估计、主动学习的钥匙。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 一张数码照片的每个像素值都不"干净"——光子计数的随机波动（泊松噪声）、电路热噪声（高斯噪声）、量化误差（均匀噪声）叠加在一起，让同一个场景每次拍出来都不一样。你拿到训练集里 1000 张「猫」的照片，它们每一张的像素值都是随机变量的一次实现。**如何用数学描述这种"不干净"？如何从有噪声的观测中推断出干净的真相？**
>
> 概率分布描述"数据长什么样"，贝叶斯推断则回答"看到数据后，我对真相有多确定"。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：贝叶斯定理是机器学习中几乎所有损失函数的源头。分类任务最小化交叉熵损失，等价于最大化后验概率的对数；回归任务最小化 MSE，等价于假设噪声服从高斯分布下的最大似然估计。理解这个"损失函数 ← 概率建模"的双向通道，你就不会再死记硬背损失公式。

- **实际应用场景**：
  - **图像去噪**：假设噪声服从 $\mathcal{N}(0,\sigma^2)$，用贝叶斯推断恢复原图（MAP估计 → 正则化最小二乘）
  - **图像分类**：Softmax 输出 $P(y=k|\mathbf{x})$ 就是后验概率，交叉熵损失就是负对数似然
  - **生成模型**：VAE 学习 $P(\mathbf{x}|\mathbf{z})$（似然）和 $P(\mathbf{z}|\mathbf{x})$（后验），Diffusion 逐步学习噪声分布
  - **主动学习**：用后验不确定性决定该标注哪些样本

- **高频题型/任务**：推导 Softmax + 交叉熵的梯度、解释为什么 MSE 损失等价于高斯 MLE、理解 VAE 的 ELBO 推导。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景（各 200 字以内）：

1. **高中数学概率基础**：理解随机事件、条件概率 $P(A|B)$、独立事件 $P(A \cap B)=P(A)P(B)$、期望值和方差的定义。知道"骰子掷出 6 的概率是 1/6"这类基本直觉。

2. **微积分入门**：会求简单函数的导数（$x^n$、$e^x$、$\ln x$），理解"导数为零处可能是极值点"。因为最大似然估计就是"求导 → 令导数为零 → 解出参数"。

3. **Python 基础**：能用 `numpy` 做数组运算、`matplotlib` 画图。本卡中的代码例子需要 `numpy`、`scipy.stats`、`matplotlib`。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

- **直觉类比 — 先验 vs 似然 vs 后验**：
  想象你在一个漆黑的房间里，听到一声猫叫。
  - **先验（Prior）** $P(\text{猫在房间里})$：你进房间之前就知道，"这栋楼养了猫，猫大概有 30% 的概率在房间里"——这是你没有任何观察时的初始信念。
  - **似然（Likelihood）** $P(\text{听到猫叫} | \text{猫在房间里})$：如果猫真的在房间里，你听到猫叫的概率很高（比如 80%）；如果猫不在，也可能是邻居家的猫（比如 5%）。似然衡量"给定真相，观测到当前证据的可能性"。
  - **后验（Posterior）** $P(\text{猫在房间里} | \text{听到猫叫})$：结合先验和似然，更新后的信念——"既然听到了猫叫，猫在房间里的概率大概是多少？"。贝叶斯定理就是把先验和似然揉在一起算出后验的公式。

- **为什么很自然**：人类大脑天生就是贝叶斯推断机器——我们不断用新证据更新旧信念。看到一个模糊轮廓时，你不会说"这有 50% 是猫、50% 是狗"，而是根据"这里有 70% 的概率出现猫"（先验）+ "这个轮廓更像猫"（似然）→ "这很可能是猫"（后验）。

- **一句话直觉本质**：**概率分布是描述世界不确定性的语言，贝叶斯定理是用证据更新信念的规则。**

---

## 5. 正式定义、核心公式、符号解释

### 5.1 高斯分布（正态分布）

一维高斯分布的概率密度函数（PDF）：

$$p(x | \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$

多维高斯分布（$D$ 维）：

$$p(\mathbf{x} | \boldsymbol{\mu}, \boldsymbol{\Sigma}) = \frac{1}{(2\pi)^{D/2} |\boldsymbol{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)$$

**CV 中的噪声建模**：传感器噪声通常被建模为**零均值高斯噪声**：

$$\mathbf{I}_{\text{obs}} = \mathbf{I}_{\text{true}} + \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \sigma^2 \mathbf{I})$$

其中 $\mathbf{I}_{\text{obs}}$ 是观测图像，$\mathbf{I}_{\text{true}}$ 是干净图像，$\boldsymbol{\epsilon}$ 是独立同分布的高斯噪声。这个假设是 Wiener 滤波、BM3D、以及许多深度学习去噪方法的理论基础。

**中心极限定理的直觉**：为什么噪声常被假设为高斯？因为传感器噪声是大量独立微小随机因素（热运动、电路波动……）的叠加，根据中心极限定理，它们的和趋向于高斯分布。

| 噪声类型 | 分布 | CV 中的来源 | 特点 |
|:---|:---|:---|:---|
| **高斯噪声** | $\mathcal{N}(\mu, \sigma^2)$ | 传感器热噪声、电路噪声 | 最常见假设，对称、无界 |
| **泊松噪声** | $\text{Poisson}(\lambda)$ | 光子计数（shot noise） | 低光照下显著，方差=均值 |
| **椒盐噪声** | 伯努利 + 均匀 | 传输错误、坏像素 | 离散脉冲，中值滤波有效 |
| **瑞利噪声** | Rayleigh | 超声/雷达散斑 | 非对称、正值 |

### 5.2 贝叶斯定理

$$\underbrace{P(A | B)}_{\text{后验}} = \frac{\overbrace{P(B | A)}^{\text{似然}} \cdot \overbrace{P(A)}^{\text{先验}}}{\underbrace{P(B)}_{\text{证据/边缘似然}}}$$

**各部分的直觉**：
- **先验 $P(A)$**：看到数据前，对 $A$ 的初始信念。例如"一张随机照片里出现猫的概率是 10%"。
- **似然 $P(B|A)$**：假设 $A$ 为真，观测到数据 $B$ 的可能性。例如"如果图片里真的有猫，分类器输出猫的概率应该很高"。
- **后验 $P(A|B)$**：看到数据 $B$ 后，更新过的信念。分类器的最终输出。
- **证据 $P(B)$**：所有可能性下观测到 $B$ 的总概率，$P(B) = \sum_A P(B|A)P(A)$。它保证后验是一个合法的概率分布（归一化常数）。

**连续版本**（参数推断）：

$$p(\boldsymbol{\theta} | \mathcal{D}) = \frac{p(\mathcal{D} | \boldsymbol{\theta}) \cdot p(\boldsymbol{\theta})}{p(\mathcal{D})}$$

其中 $\boldsymbol{\theta}$ 是模型参数，$\mathcal{D}$ 是训练数据。

### 5.3 最大似然估计（MLE）

给定独立同分布数据 $\mathcal{D} = \{x_1, x_2, \ldots, x_N\}$，MLE 寻找使数据出现概率最大的参数：

$$\hat{\boldsymbol{\theta}}_{\text{MLE}} = \arg\max_{\boldsymbol{\theta}} \; p(\mathcal{D} | \boldsymbol{\theta}) = \arg\max_{\boldsymbol{\theta}} \prod_{i=1}^{N} p(x_i | \boldsymbol{\theta})$$

取对数（对数似然）使乘积变求和，数值更稳定：

$$\hat{\boldsymbol{\theta}}_{\text{MLE}} = \arg\max_{\boldsymbol{\theta}} \sum_{i=1}^{N} \log p(x_i | \boldsymbol{\theta})$$

### 5.4 最大后验估计（MAP）

MAP 在 MLE 的基础上加入先验：

$$\hat{\boldsymbol{\theta}}_{\text{MAP}} = \arg\max_{\boldsymbol{\theta}} \; p(\boldsymbol{\theta} | \mathcal{D}) = \arg\max_{\boldsymbol{\theta}} \; p(\mathcal{D} | \boldsymbol{\theta}) \cdot p(\boldsymbol{\theta})$$

取对数：

$$\hat{\boldsymbol{\theta}}_{\text{MAP}} = \arg\max_{\boldsymbol{\theta}} \left[ \underbrace{\sum_{i=1}^{N} \log p(x_i | \boldsymbol{\theta})}_{\text{对数似然}} + \underbrace{\log p(\boldsymbol{\theta})}_{\text{对数先验}} \right]$$

**关键直觉**：加上先验 $\log p(\boldsymbol{\theta})$ 这一项就是正则化！例如，若先验是高斯分布 $p(\boldsymbol{\theta}) \propto \exp(-\frac{\|\boldsymbol{\theta}\|^2}{2\tau^2})$，则 MAP 等价于 MLE + L2 正则化。

### 5.5 MLE 与交叉熵损失的关系（CV 核心！）

这是理解图像分类损失函数的关键连接。对于 $K$ 类分类任务：

- **模型输出**：Softmax 给出的各类概率 $\hat{y}_k = P(y=k|\mathbf{x}; \boldsymbol{\theta})$
- **似然**：给定标签 $y$（one-hot），观测到的似然是 $P(y|\mathbf{x}; \boldsymbol{\theta}) = \prod_{k=1}^{K} \hat{y}_k^{y_k}$
- **负对数似然（NLL）**：$-\log P(y|\mathbf{x}; \boldsymbol{\theta}) = -\sum_{k=1}^{K} y_k \log \hat{y}_k$
- **交叉熵损失**：正是负对数似然的期望！

$$\mathcal{L}_{\text{CE}} = -\sum_{k=1}^{K} y_k \log \hat{y}_k = -\log P(y|\mathbf{x}; \boldsymbol{\theta})$$

**结论**：最小化交叉熵损失 = 最大化（对数）似然 = MLE！这就是为什么你用交叉熵训练分类器时，实际上在做概率意义上的最大似然估计。

### 5.6 符号说明表

| 符号 | 含义 | 计算/来源 | 备注 |
|:---|:---|:---|:---|
| $P(A\|B)$ | 条件概率 | $P(A \cap B)/P(B)$ | 给定 B 后 A 的概率 |
| $p(x\|\mu,\sigma^2)$ | 高斯 PDF | 公式见 5.1 | $p$ 表示概率密度 |
| $\mathcal{N}(\mu,\sigma^2)$ | 高斯分布记号 | 均值为 $\mu$，方差为 $\sigma^2$ | $\mathcal{N}(0,1)$ 为标准正态 |
| $\boldsymbol{\theta}$ | 模型参数 | 学习得到 | 分类器权重、分布参数等 |
| $\mathcal{D}$ | 训练数据集 | $\{(x_i,y_i)\}_{i=1}^{N}$ | i.i.d. 假设 |
| $\hat{y}_k$ | 预测类别概率 | Softmax 输出 | $\sum_k \hat{y}_k = 1$ |

---

## 6. 推导思路和思想来源

- **最初困难**：面对不确定的观测（有噪声的图像），如何"反向"推断出干净的真相或最优参数？这本质是一个**逆问题（Inverse Problem）**——从果推因。

- **直接方法局限**：如果没有概率框架，你只能猜测。但猜测缺乏量化——你不知道你的推断有多可靠。

- **关键"转念"——贝叶斯定理的视角翻转**：
  $$P(\text{原因}|\text{结果}) = \frac{P(\text{结果}|\text{原因}) \cdot P(\text{原因})}{P(\text{结果})}$$
  贝叶斯定理的巧妙之处在于：它把难以直接计算的"从果推因"（后验），转化为容易建模的"从因推果"（似然）乘以"先验信念"（先验）。在 CV 中，"因"是图像内容（类别、干净像素），"果"是观测（像素值、特征）。

- **推导主线**：
  1. 假设观测模型（例如：像素 = 真实值 + 高斯噪声）→ 写出似然 $p(\text{观测}|\text{真相})$
  2. 加入对真相的先验知识（例如：自然图像像素通常是平滑的）→ 写出先验 $p(\text{真相})$
  3. 用贝叶斯定理组合二者 → 后验 $p(\text{真相}|\text{观测})$
  4. 最大化后验（MAP）或采样后验 → 得到推断结果

- **为什么交叉熵来自 MLE**：
  对于分类问题，真实的 $P_{\text{data}}(y|\mathbf{x})$ 是 one-hot（确定性标签），模型学到的分布是 $P_{\text{model}}(y|\mathbf{x}; \boldsymbol{\theta})$。MLE 最小化两个分布的 KL 散度 → 等价于最小化交叉熵。这是一条优美的推导链：**经验风险最小化 ← KL 散度 ← MLE ← 负对数似然 ← 交叉熵**。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算 — 硬币抛掷的 MLE vs MAP

> **场景**：你抛一枚硬币 10 次，观察到 7 次正面（H）、3 次反面（T）。硬币正面的真实概率 $\theta$ 未知。

**MLE 解**：
似然函数（二项分布）：
$$p(\mathcal{D}|\theta) = \theta^7 (1-\theta)^3$$

对数似然：
$$\log p(\mathcal{D}|\theta) = 7\log\theta + 3\log(1-\theta)$$

求导并令为零：
$$\frac{d}{d\theta} = \frac{7}{\theta} - \frac{3}{1-\theta} = 0 \quad \Rightarrow \quad \hat{\theta}_{\text{MLE}} = \frac{7}{10} = 0.7$$

**直观**：MLE 就是数频率——你看到什么就信什么。

**MAP 解（Beta 先验）**：
假设你对硬币有先验信念：硬币大概率是公平的。用 $\text{Beta}(2,2)$ 作为先验：
$$p(\theta) \propto \theta^{2-1}(1-\theta)^{2-1} = \theta(1-\theta)$$

后验（Beta 是二项分布的共轭先验）：
$$p(\theta|\mathcal{D}) \propto p(\mathcal{D}|\theta) \cdot p(\theta) = \theta^7(1-\theta)^3 \cdot \theta(1-\theta) = \theta^8(1-\theta)^4$$

最大化：$\hat{\theta}_{\text{MAP}} = \frac{8}{8+4} = \frac{2}{3} \approx 0.667$

**对比**：
| 方法 | $\hat{\theta}$ | 直觉 |
|:---|:---|:---|
| MLE | 0.700 | "数据说什么就是什么" |
| MAP (Beta(2,2)先验) | 0.667 | "数据说 0.7，但我先验认为应该接近 0.5，折中到 0.667" |
| MAP (Beta(10,10)先验) | 0.567 | 强先验 → 数据的影响力被压制 |

**关键洞察**：先验相当于"伪计数"（pseudo-count）。Beta(2,2) 相当于你事先"虚拟地"看到了 1 次正面 + 1 次反面。这就是**拉普拉斯平滑**（Laplace Smoothing）的概率视角！

### 例子 2：中等例子 — 高斯噪声下的图像去噪（MAP）

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

# --- 1. 生成一维"干净信号" + 高斯噪声 ---
np.random.seed(42)
N = 200
x_true = np.zeros(N)
x_true[50:80] = 1.0     # 一个矩形脉冲（模拟边缘）
x_true[120:150] = 0.6   # 一个矮脉冲

sigma_noise = 0.3
x_obs = x_true + np.random.randn(N) * sigma_noise

# --- 2. MAP 去噪 = 最小化 (数据保真项 + 正则化项) ---
#   p(x_true|x_obs) ∝ p(x_obs|x_true) · p(x_true)
#   高斯似然: p(x_obs|x_true) ∝ exp(-||x_obs - x_true||² / (2σ²))
#   平滑先验: p(x_true) ∝ exp(-λ·||∇x_true||²)  （鼓励相邻像素相似）
#   MAP:  argmin ||x_obs - x_est||² + λ·||∇x_est||²
#   这就是 Tikhonov 正则化 / 岭回归的一维版本

# 用简单的梯度下降求解 MAP
x_est = x_obs.copy()
lr = 0.1
lam = 2.0  # 正则化系数（先验强度）
for _ in range(500):
    # 数据保真梯度（似然项）
    grad_data = -2 * (x_obs - x_est)
    # 平滑先验梯度（先验项）：二阶差分
    grad_prior = 2 * lam * (2 * x_est - np.roll(x_est, 1) - np.roll(x_est, -1))
    grad_prior[0] = grad_prior[-1] = 0  # 边界忽略
    x_est -= lr * (grad_data + grad_prior)

# --- 3. 绘图对比 ---
fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
axes[0].plot(x_true, 'k-', linewidth=2, label='Ground Truth')
axes[0].set_ylabel('Clean'); axes[0].legend(loc='upper right')
axes[1].plot(x_obs, 'r-', alpha=0.7, linewidth=1, label='Noisy σ=0.3')
axes[1].set_ylabel('Observed'); axes[1].legend(loc='upper right')
axes[2].plot(x_true, 'k-', linewidth=2, alpha=0.5, label='Ground Truth')
axes[2].plot(x_est, 'b-', linewidth=1.5, label=f'MAP (λ={lam})')
axes[2].set_ylabel('MAP Est.'); axes[2].set_xlabel('Pixel index')
axes[2].legend(loc='upper right')
plt.tight_layout(); plt.show()
```

- **易错点**：正则化系数 $\lambda$ 太大 → 过度平滑，边缘模糊；太小 → 噪声残留。$\lambda$ 本质上控制"你有多信任先验"。
- **🤔 追问**：如果噪声不是高斯的（比如椒盐噪声），MAP 框架还适用吗？→ 适用！只需要把似然换成正确的噪声分布（如拉普拉斯 → L1 损失）。

### 例子 3：实际应用例子 — 图像分类后验概率可视化

```python
import numpy as np

def softmax(logits):
    """Softmax: 把 logits 变成概率分布"""
    exps = np.exp(logits - np.max(logits))  # 数值稳定性
    return exps / exps.sum()

# --- 模拟一个 3 类分类器 ---
# 假设模型对一张图片输出 logits（原始分数）
logits = np.array([-0.5, 2.3, 0.8])  # 类别: 猫, 狗, 鸟
classes = ['猫', '狗', '鸟']

# Softmax → 后验概率 P(y|x)
probs = softmax(logits)

print("=== 分类器输出的后验概率 ===")
for cls, p in zip(classes, probs):
    print(f"P(y={cls} | x) = {p:.4f} ({p*100:.1f}%)")

# --- 贝叶斯视角解释 ---
# P(y=k|x) ∝ P(x|y=k) · P(y=k)
# log P(y=k|x) = log P(x|y=k) + log P(y=k) + const
# 如果各类先验相等 P(y=k)=1/3，则后验完全由似然决定
# Softmax 输出的正是归一化后的后验概率！

# --- 交叉熵损失计算 ---
y_true = 1  # 真实标签是「狗」（索引1）
y_onehot = np.eye(3)[y_true]
ce_loss = -np.sum(y_onehot * np.log(probs + 1e-8))
print(f"\n交叉熵损失: {ce_loss:.4f}")
print(f"负对数似然 -log P(y=狗|x): {-np.log(probs[y_true]):.4f}  (两者相等!)")

# --- 加入先验的 MAP 视角 ---
prior = np.array([0.1, 0.6, 0.3])  # 先验：狗最常见，猫最稀有
log_posterior = np.log(probs) + np.log(prior)  # 对数后验（忽略常数项）
map_pred = np.argmax(log_posterior)
print(f"\n加入先验 {prior} 后:")
print(f"  对数后验: {log_posterior}")
print(f"  MAP预测: {classes[map_pred]}")
```

**关键观察**：
- Softmax 输出 = 后验概率的估计
- 交叉熵损失 = 负对数似然 = 训练即 MLE
- 若训练数据各类别不均衡，等于隐式地施加了一个非均匀的"数据先验"

---

## 8. 常见误区和易混概念

### 误区 1：把似然当成概率，忽略归一化

- **错误直觉**："$P(D|\theta) = 0.8$ 说明这个参数有 80% 的概率是正确的。"
- **为什么错**：似然 $P(D|\theta)$ 不是 $\theta$ 的概率分布！它是"固定 $\theta$ 时观测到 $D$ 的概率"，对 $\theta$ 的积分不一定为 1。$\theta$ 的概率分布是后验 $P(\theta|D)$。**似然不是概率，后验才是。**
- **正确理解**：比较不同 $\theta$ 的似然比值有意义（似然比检验），但不能直接把似然当作 $\theta$ 的概率。

### 误区 2："没有先验"就是客观——错！那只是选了均匀先验

- **错误直觉**："我用 MLE，没有加先验，所以我的结论是客观的。"
- **为什么错**：MLE 等价于 MAP with 均匀先验 $p(\theta) \propto 1$。均匀先验是一种特定的先验选择（认为所有 $\theta$ 值等可能），它不比其他先验更"客观"——特别是在 $\theta$ 有自然度量时（比如方差不能为负，均匀先验会导致边界偏差）。
- **正确理解**：MLE 是 MAP 的特例（均匀先验），而非"没有先验"。在数据量大的情况下，MLE 和 MAP 通常收敛到相同结果（先验被数据压倒）。在数据量小时，先验的选择至关重要。

### 误区 3：交叉熵损失就是"一个损失函数"——忘记它的概率根源

- **错误直觉**："交叉熵只是一个衡量概率分布差异的公式，和概率建模没关系。"
- **为什么错**：交叉熵损失 = 负对数似然，最小化它等价于在 Bernoulli/Categorical 似然假设下做 MLE。如果你用 MSE 训练分类器（即假设高斯似然），效果会很差——因为分类标签不是连续高斯变量。
- **正确理解**：选择损失函数 = 选择数据的概率模型。交叉熵 → Categorical 似然；MSE → 高斯似然；MAE → 拉普拉斯似然。

### 概念对比表

| 概念 | 符号 | 对 $\theta$ 的积分 | 核心用途 |
|:---|:---|:---|:---|
| **似然** | $p(D\|\theta)$ | ≠ 1（不是概率分布） | 参数估计（MLE） |
| **后验** | $p(\theta\|D)$ | = 1（是概率分布） | 参数推断（MAP/贝叶斯） |
| **先验** | $p(\theta)$ | = 1（是概率分布） | 编码先验知识 |
| **证据** | $p(D)$ | 归一化常数 | 模型选择（贝叶斯因子） |

| 估计方法 | 优化目标 | 与正则化的关系 |
|:---|:---|:---|
| MLE | $\max_\theta \log p(D\|\theta)$ | 无正则化（= MAP 均匀先验） |
| MAP | $\max_\theta \log p(D\|\theta) + \log p(\theta)$ | $\log p(\theta)$ 就是正则化项 |
| 全贝叶斯 | 不点估计，求整个后验 $p(\theta\|D)$ | 无需显式正则化（边缘化自带 Occam 剃刀） |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- 高中数学：条件概率、期望、方差的基础定义
- [[线性代数基础CV]]：多维高斯分布的协方差矩阵 $\boldsymbol{\Sigma}$ 需要线性代数背景

### 下游延伸
- [[Softmax与SVM损失函数]]：Softmax 输出 = 后验概率，交叉熵损失 = 负对数似然（MLE）
- 生成模型VAE：VAE 的核心——学习 $p(\mathbf{x}|\mathbf{z})$（似然）和 $q(\mathbf{z}|\mathbf{x})$（近似后验）
- 扩散模型DDPM：正向加噪（构造似然）→ 反向去噪（学习后验），全程是概率建模
- 贝叶斯深度学习（如已建）：贝叶斯神经网络用分布替代点估计

### 横向关联
- 梯度下降与优化基础：MLE/MAP 的优化通常用梯度下降求解
- 信息论基础：交叉熵、KL 散度、熵——信息论是概率建模的另一套语言
- 正则化技术：L1/L2 正则化 = 拉普拉斯/高斯先验下的 MAP

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚贝叶斯定理的直觉含义。
- [ ] 2. 用直觉语言解释先验、似然、后验的区别（«"这东西其实就像……"»）。
- [ ] 3. 写出一维高斯分布的概率密度公式，并解释每个符号。
- [ ] 4. 写出贝叶斯定理的公式，标注每部分的名称。
- [ ] 5. 推导：为什么最小化交叉熵损失等价于最大似然估计？
- [ ] 6. 手算：抛硬币 10 次 7 正 3 反，求 $\hat{\theta}_{\text{MLE}}$ 和 Beta(2,2) 先验下的 $\hat{\theta}_{\text{MAP}}$。
- [ ] 7. 解释为什么 MAP 中的对数先验 $\log p(\theta)$ 是正则化项。
- [ ] 8. 说出 CV 中三种常见的噪声分布及其来源。
- [ ] 9. 解释"似然不是概率"的含义。
- [ ] 10. 画出一张图描述 MLE → 负对数似然 → 交叉熵 → KL 散度之间的等价关系链。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
|:---|:---|:---|:---|
| 1 | 概念辨析 | 基础 | 似然 vs 后验 vs 先验的区分 |
| 2 | 公式推导 | 基础 | 二项分布的 MLE 推导 |
| 3 | 计算 | 中等 | 贝叶斯定理在图像分类中的应用 |
| 4 | 综合 | 中等 | 给定数据，手算 MLE 和 MAP |
| 5 | 开放 | 较难 | 为新的噪声模型设计损失函数 |

### 题目与解析

#### 1. 以下哪个说法正确？
A. 似然 $P(D|\theta)$ 是 $\theta$ 的概率分布
B. 后验 $P(\theta|D)$ 是 $\theta$ 的概率分布
C. MLE 等价于 MAP with 高斯先验
D. 交叉熵损失和概率建模无关

> [!question]- 答案解析
> - **答案**：B
> - **解析**：后验对 $\theta$ 积分为 1，是合法的概率分布；似然对 $\theta$ 积分不为 1。MLE 等价于 MAP with **均匀先验**（不是高斯）。交叉熵本质是负对数似然。
> - **易错原因**：初学者常把似然当作参数的概率。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 2. 推导二项分布的 MLE
> 抛硬币 $N$ 次，$k$ 次正面。推导 $\hat{\theta}_{\text{MLE}}$。
> [!question]- 答案解析
> - **推导**：$L(\theta) = \binom{N}{k} \theta^k (1-\theta)^{N-k}$，$\log L = k\log\theta + (N-k)\log(1-\theta) + \text{const}$。求导：$\frac{k}{\theta} - \frac{N-k}{1-\theta} = 0$，解得 $\hat{\theta} = \frac{k}{N}$。
> - **解析**：MLE 就是频率 $\frac{k}{N}$，大道至简。
> - **对应误区**：注意二项系数 $\binom{N}{k}$ 不含 $\theta$，取对数后变常数，求导消掉。

#### 3. 图像分类中的贝叶斯应用
> 一个三类分类器输出后验概率 $P(y|\mathbf{x}) = [0.1, 0.7, 0.2]$。已知各类先验概率为 $P(y) = [0.5, 0.3, 0.2]$。求各类的似然 $P(\mathbf{x}|y)$（忽略归一化常数）。
> [!question]- 答案解析
> - **答案**：$P(\mathbf{x}|y) \propto P(y|\mathbf{x}) / P(y) = [0.1/0.5, 0.7/0.3, 0.2/0.2] = [0.2, 2.33, 1.0]$
> - **解析**：由贝叶斯定理 $P(y|\mathbf{x}) \propto P(\mathbf{x}|y) \cdot P(y)$，所以 $P(\mathbf{x}|y) \propto P(y|\mathbf{x}) / P(y)$。类别 2（狗）的似然最高——即使先验不高，观测证据足够强。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 4. 硬币抛掷的手算 MLE vs MAP
> 抛硬币 5 次，3 次正面 2 次反面。计算：(a) MLE；(b) Beta(3,3) 先验下的 MAP。
> [!question]- 答案解析
> - **答案**：(a) $\hat{\theta}_{\text{MLE}} = 3/5 = 0.6$；(b) Beta(3,3) 先验即 $\alpha=3, \beta=3$，后验 Beta(3+3, 3+2) = Beta(6,5)，$\hat{\theta}_{\text{MAP}} = (6-1)/(6+5-2) = 5/9 \approx 0.556$。或等效地用"伪计数"：先验相当于 2 正 + 2 反，数据 3 正 + 2 反 → 总共 5 正 4 反 → 5/9。
> - **解析**：先验把估计往 0.5 拉——贝叶斯版的"保守估计"。
> - **对应卡内例子**：例子 1。

#### 5. 为椒盐噪声设计 MAP 去噪的损失函数
> 高斯噪声假设下 MAP 去噪的数据项是 $\|\mathbf{I}_{\text{obs}} - \mathbf{I}_{\text{est}}\|_2^2$。如果噪声是椒盐噪声（稀疏脉冲），应该用什么损失？
> [!question]- 答案解析
> - **答案**：使用 **L1 损失**（$\|\mathbf{I}_{\text{obs}} - \mathbf{I}_{\text{est}}\|_1$）或 **Huber 损失**。因为椒盐噪声产生离群值（outlier），L2 损失对离群值过于敏感（平方放大误差），L1 损失更鲁棒。更精确的做法：把噪声建模为拉普拉斯分布 $p(\epsilon) \propto \exp(-|\epsilon|/b)$ → 负对数似然就是 L1。
> - **解析**：这展示了"选择损失函数 = 选择噪声模型"的核心思想。实际应用中，中值滤波就是 L1 思想的极端体现。
> - **Obsidian 标签建议**：`#自测题/较难`

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试推导二项分布的 MLE 和 Beta 先验下的 MAP：

### 我的错误与卡点
-

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/`
- **关联已有笔记**：`[[线性代数基础CV]]` `[[Softmax与SVM损失函数]]` `生成模型VAE` `扩散模型DDPM` `梯度下降与优化基础`
- **建议标签**：`#学习` `#计算机视觉` `#概率` `#贝叶斯` `#数学基础`
- **拆分建议**：本卡内容完整，不拆分。若后续深入学习，可考虑拆分出：
  - 「高斯过程与贝叶斯优化」专题卡（进阶）
  - 「变分推断入门」专题卡（进阶，VAE 的数学基础）
  - 「概率图模型与 MRF」专题卡（与图像分割联动）

---
---

## 学完后可以完成

- 完成卡内自测题与闭卷复现（分布建模）

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
