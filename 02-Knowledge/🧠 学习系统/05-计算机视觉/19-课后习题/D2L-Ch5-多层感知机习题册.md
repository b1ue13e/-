---
type: project
topic: "D2L Ch.5 多层感知机课后习题"
created: 2026-08-05
status: active
flow: project
tags: [计算机视觉, 课后习题, D2L, MLP, 反向传播]
---

# 🧠 D2L Ch.5 多层感知机（Multilayer Perceptrons）课后习题册

> 基于 [Dive into Deep Learning (D2L)](https://d2l.ai/chapter_multilayer-perceptrons/index.html) 第5章（CC BY-SA 4.0），共8道习题。
> 覆盖：前向传播矩阵推导、激活函数对比、反向传播手算、权重衰减、Dropout、数值稳定性、从零实现、MLP vs 线性模型。
> 每道题标注考查知识点与对应知识卡，形成「学→练→测」闭环。

---

## 🗺️ 知识地图

| 题号 | 题目 | 考查知识点 | 对应知识卡 | 难度 |
|:---:|:---|:---|:---|:---:|
| 1 | MLP前向传播矩阵推导 | 矩阵乘法、广播、逐层表示 | [[前向传播]]、[[线性代数基础CV]] | ⭐⭐ |
| 2 | 激活函数选择：ReLU vs Sigmoid vs Tanh | 梯度饱和、非饱和、死亡ReLU | [[激活函数CV]]、[[反向传播与计算图]] | ⭐⭐ |
| 3 | 反向传播梯度推导（含手算小题） | 链式法则、本地梯度、上游梯度 | [[反向传播与计算图]]、[[链式法则]] | ⭐⭐⭐ |
| 4 | 权重衰减（L2正则化）的梯度形式 | 正则化原理、梯度项分解、超参数λ | [[权重正则化]]、[[梯度计算]] | ⭐⭐ |
| 5 | Dropout的训练/测试差异 | 缩放因子、集成解释、方差偏移 | [[Dropout]]、[[数据增强与正则化]] | ⭐⭐ |
| 6 | 数值稳定性与梯度消失/爆炸 | Xavier初始化、sigmoid饱和、log-sum-exp | [[梯度流问题]]、[[批归一化BatchNorm]] | ⭐⭐⭐ |
| 7 | MLP从零实现思路 | 模块化设计、前向/反向分离、梯度检查 | [[MLP]]、[[前向传播]]、[[反向传播与计算图]] | ⭐⭐⭐ |
| 8 | MLP与线性模型的根本区别 | 非线性变换、表示学习、万能逼近 | [[感知机]]、[[MLP]] | ⭐ |

---

## 习题

---

### 习题 1 · MLP前向传播矩阵推导

> 📘 **考查**：前向传播的矩阵表示 | 🏷️ **对应卡**：[[前向传播]] [[线性代数基础CV]]

**题目**：考虑一个包含一个隐藏层的MLP，结构为：输入维度 $d=3$，隐藏层宽度 $h=4$，输出类别数 $k=2$。

已知：
- 输入样本（batch size = 1）：$\mathbf{x} = [1.0, \; 2.0, \; 3.0]^\top \in \mathbb{R}^{3}$
- 第一层权重：$\mathbf{W}^{(1)} = \begin{bmatrix} 0.1 & 0.2 & 0.3 \\ 0.4 & 0.5 & 0.6 \\ 0.7 & 0.8 & 0.9 \\ 1.0 & 1.1 & 1.2 \end{bmatrix} \in \mathbb{R}^{4 \times 3}$
- 第一层偏置：$\mathbf{b}^{(1)} = [0.1, \; 0.2, \; 0.3, \; 0.4]^\top \in \mathbb{R}^{4}$
- 第二层权重：$\mathbf{W}^{(2)} = \begin{bmatrix} 0.5 & -0.3 & 0.2 & 0.1 \\ -0.1 & 0.4 & -0.2 & 0.3 \end{bmatrix} \in \mathbb{R}^{2 \times 4}$
- 第二层偏置：$\mathbf{b}^{(2)} = [0.0, \; 0.0]^\top \in \mathbb{R}^{2}$
- 隐藏层激活函数：ReLU（$\text{ReLU}(z) = \max(0, z)$）
- 输出层不使用激活函数（即线性输出，用于回归/后续接Softmax）

**(a)** 写出MLP两层前向传播的矩阵公式（通用形式，包含激活函数）。

**(b)** 用给定数值计算隐藏层预激活 $\mathbf{z}^{(1)} = \mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}$，再计算隐藏层激活 $\mathbf{h} = \text{ReLU}(\mathbf{z}^{(1)})$。

**(c)** 用 $\mathbf{h}$ 继续计算输出层 $\mathbf{o} = \mathbf{W}^{(2)}\mathbf{h} + \mathbf{b}^{(2)}$。

**(d)** 如果输入改为 mini-batch $\mathbf{X} \in \mathbb{R}^{m \times 3}$（$m$ 个样本），上述矩阵公式需要如何修改？写出矩阵形状变化。

---

<details>
<summary><b>📝 参考答案</b></summary>

**(a)** 通用形式：
$$\mathbf{z}^{(1)} = \mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}, \quad \mathbf{h} = \sigma(\mathbf{z}^{(1)})$$
$$\mathbf{o} = \mathbf{W}^{(2)}\mathbf{h} + \mathbf{b}^{(2)}$$
其中 $\sigma$ 为激活函数（此处为ReLU）。若需输出概率，可再经Softmax：$\hat{\mathbf{y}} = \text{softmax}(\mathbf{o})$。

**(b)** 计算 $\mathbf{z}^{(1)}$：

$$\mathbf{z}^{(1)} = \begin{bmatrix} 0.1 & 0.2 & 0.3 \\ 0.4 & 0.5 & 0.6 \\ 0.7 & 0.8 & 0.9 \\ 1.0 & 1.1 & 1.2 \end{bmatrix} \begin{bmatrix} 1.0 \\ 2.0 \\ 3.0 \end{bmatrix} + \begin{bmatrix} 0.1 \\ 0.2 \\ 0.3 \\ 0.4 \end{bmatrix}$$

- 第1行：$0.1 \times 1.0 + 0.2 \times 2.0 + 0.3 \times 3.0 = 0.1 + 0.4 + 0.9 = 1.4$，加偏置得 $1.5$
- 第2行：$0.4 + 1.0 + 1.8 = 3.2$，加偏置得 $3.4$
- 第3行：$0.7 + 1.6 + 2.7 = 5.0$，加偏置得 $5.3$
- 第4行：$1.0 + 2.2 + 3.6 = 6.8$，加偏置得 $7.2$

$$\mathbf{z}^{(1)} = [1.5, \; 3.4, \; 5.3, \; 7.2]^\top$$

ReLU激活：$\mathbf{h} = \max(0, \mathbf{z}^{(1)}) = [1.5, \; 3.4, \; 5.3, \; 7.2]^\top$（全部为正，无变化）

**(c)** 输出层：
$$\mathbf{o} = \begin{bmatrix} 0.5 & -0.3 & 0.2 & 0.1 \\ -0.1 & 0.4 & -0.2 & 0.3 \end{bmatrix} \begin{bmatrix} 1.5 \\ 3.4 \\ 5.3 \\ 7.2 \end{bmatrix}$$

- 第1行：$0.5 \times 1.5 + (-0.3) \times 3.4 + 0.2 \times 5.3 + 0.1 \times 7.2 = 0.75 - 1.02 + 1.06 + 0.72 = 1.51$
- 第2行：$(-0.1) \times 1.5 + 0.4 \times 3.4 + (-0.2) \times 5.3 + 0.3 \times 7.2 = -0.15 + 1.36 - 1.06 + 2.16 = 2.31$

$$\mathbf{o} = [1.51, \; 2.31]^\top$$

**(d)** Mini-batch修改：

$$\mathbf{Z}^{(1)} = \mathbf{X}\mathbf{W}^{(1)\top} + \mathbf{b}^{(1)} \quad \text{或} \quad \mathbf{Z}^{(1)} = \mathbf{X} \in \mathbb{R}^{m \times 3} \cdot (\mathbf{W}^{(1)})^\top \in \mathbb{R}^{3 \times 4}$$

形状变化链：$\mathbf{X}(m \times 3) \to \mathbf{Z}^{(1)}(m \times 4) \to \mathbf{H}(m \times 4) \to \mathbf{O}(m \times 2)$。

偏置 $\mathbf{b}^{(1)}$ 通过广播机制加到每一行。

> 注意：不同框架中 $\mathbf{W}$ 的形状约定不同。此处 $\mathbf{W}^{(1)} \in \mathbb{R}^{h \times d}$，则 $\mathbf{z} = \mathbf{W}\mathbf{x} + \mathbf{b}$。若定义为 $\mathbf{W} \in \mathbb{R}^{d \times h}$，则为 $\mathbf{z} = \mathbf{x}^\top \mathbf{W} + \mathbf{b}$。两种约定等价，关键是保持一致。

</details>

---

### 习题 2 · 激活函数选择：ReLU vs Sigmoid vs Tanh

> 📘 **考查**：激活函数的梯度特性与选择依据 | 🏷️ **对应卡**：[[激活函数CV]] [[反向传播与计算图]]

**题目**：深度网络训练中，激活函数的选择直接影响梯度流。

**(a)** 写出 Sigmoid、Tanh、ReLU 三者的数学表达式及其导数的表达式。指出每种激活函数的输出值域和导数值域。

**(b)** 什么是"梯度饱和"（gradient saturation）？请以 Sigmoid 为例解释：当输入 $x \to +\infty$ 和 $x \to -\infty$ 时梯度分别趋近于什么值？这对深层网络训练有何危害？

**(c)** ReLU 在 $x > 0$ 和 $x \le 0$ 时梯度分别为多少？什么是"死亡ReLU"（dying ReLU）问题？有哪些缓解方案（至少列出两种）？

**(d)** 假设有一个 $L$ 层的MLP，所有隐藏层统一使用 Sigmoid 激活，权重初始化均用 $\mathcal{N}(0, 0.01)$。请解释为什么这种配置极可能导致梯度消失——从反向传播链式法则的角度，写出第 $l$ 层梯度与后面各层的关系。

---

<details>
<summary><b>📝 参考答案</b></summary>

**(a)** 三者对比：

|  | Sigmoid | Tanh | ReLU |
|:---|:---|:---|:---|
| 表达式 | $\sigma(x) = \frac{1}{1+e^{-x}}$ | $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$ | $\text{ReLU}(x) = \max(0, x)$ |
| 导数 | $\sigma(x)(1 - \sigma(x))$ | $1 - \tanh^2(x)$ | $\mathbb{1}_{x>0}$ |
| 输出值域 | $(0, 1)$ | $(-1, 1)$ | $[0, +\infty)$ |
| 导数值域 | $(0, 0.25]$ | $(0, 1]$ | $\{0, 1\}$ |

> 关键差异：Sigmoid的最大梯度仅0.25，Tanh最大为1，ReLU在正区梯度始终为1（无衰减）。

**(b)** **梯度饱和**：当输入绝对值很大时，激活函数的导数趋近于零，导致反向传播时梯度几乎为零。

以 Sigmoid 为例：
- $x \to +\infty$：$\sigma(x) \to 1$，$\sigma'(x) = \sigma(1-\sigma) \to 1 \times 0 = 0$
- $x \to -\infty$：$\sigma(x) \to 0$，$\sigma'(x) \to 0 \times 1 = 0$

**危害**：在深层网络中，每一层Sigmoid的梯度 $\le 0.25$，$L$ 层后梯度按 $(0.25)^L$ 衰减——指数级消失，浅层参数几乎无法更新。

**(c)** ReLU梯度：
- $x > 0$：梯度 = 1（不衰减！）
- $x \le 0$：梯度 = 0（完全截断）

**死亡ReLU**：当某个神经元的所有输入都 $\le 0$ 时，梯度永为0，该神经元永久失活，不再对任何样本有响应。

**缓解方案**（任答两种即可）：
1. **Leaky ReLU**：$f(x) = \max(\alpha x, x)$，其中 $\alpha$ 是小正数（如0.01），使负区也有非零梯度
2. **ELU**：$f(x) = \begin{cases} x & x>0 \\ \alpha(e^x - 1) & x \le 0 \end{cases}$，负区平滑且输出均值接近0
3. **合理初始化**：使用He初始化（$\mathcal{N}(0, 2/n_{\text{in}})$），避免大量神经元在初始化时就死亡
4. **适当的学习率**：过大的学习率可能将神经元推到死亡区

**(d)** 梯度消失分析：

设第 $l$ 层激活 $\mathbf{h}^{(l)} = \sigma(\mathbf{W}^{(l)}\mathbf{h}^{(l-1)} + \mathbf{b}^{(l)})$，损失对第 $l$ 层权重的梯度：

$$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \frac{\partial \mathcal{L}}{\partial \mathbf{h}^{(L)}} \cdot \prod_{k=l+1}^{L} \left( \mathbf{W}^{(k)\top} \cdot \text{diag}(\sigma'(\mathbf{z}^{(k)})) \right) \cdot \text{diag}(\sigma'(\mathbf{z}^{(l)})) \cdot \mathbf{h}^{(l-1)\top}$$

关键因子 $\sigma'(\mathbf{z}^{(k)}) \le 0.25$（Sigmoid）。$L-l$ 层叠乘后，梯度被因子 $(0.25)^{L-l}$ 压缩。再加上权重 $\mathbf{W}^{(k)} \sim \mathcal{N}(0, 0.01)$ 的每个元素都很小，乘积累进一步缩小 → **梯度消失**。

> 这是为什么现代网络几乎总是用 ReLU 或其变体作为隐藏层激活函数。

</details>

---

### 习题 3 · 反向传播梯度推导（含手算小题）

> 📘 **考查**：链式法则 + 计算图上的梯度手算 | 🏷️ **对应卡**：[[反向传播与计算图]] [[链式法则]]

**题目**：给定一个简化的两层网络（标量版），用于二分类：只有一个隐藏神经元。

- 输入：$x = 2$（标量）
- 标签：$y = 1$
- 参数：$w_1 = 0.5, \; b_1 = 0.0, \; w_2 = 1.0, \; b_2 = 0.0$
- 前向传播：
  $$z_1 = w_1 x + b_1 \quad \to \quad h = \text{sigmoid}(z_1)$$
  $$z_2 = w_2 h + b_2 \quad \to \quad \hat{y} = \text{sigmoid}(z_2)$$
- 损失：二分类交叉熵 $\mathcal{L} = -[y \log \hat{y} + (1-y) \log(1-\hat{y})]$

**(a)** 画出计算图，标注每个节点的值和前向传播的中间结果（保留3位小数）。

**(b)** 写出交叉熵损失对 $\hat{y}$ 的梯度 $\frac{\partial \mathcal{L}}{\partial \hat{y}}$（这是反向传播的起点）。

**(c)** 从 $\hat{y}$ 开始向回传播，手算 $\frac{\partial \mathcal{L}}{\partial w_2}$、$\frac{\partial \mathcal{L}}{\partial b_2}$、$\frac{\partial \mathcal{L}}{\partial w_1}$、$\frac{\partial \mathcal{L}}{\partial b_1}$。请写出每一步的链式法则分解。

**(d)** 验证：若 $w_1$ 微小增加 $\Delta = 0.001$，用你算出的梯度预测损失变化量 $\Delta \mathcal{L} \approx \frac{\partial \mathcal{L}}{\partial w_1} \times \Delta$，再用前向传播计算实际损失变化量，说明两者接近。

---

<details>
<summary><b>📝 参考答案</b></summary>

**(a)** 前向传播计算：

$z_1 = 0.5 \times 2 + 0 = 1.0$
$h = \sigma(1.0) = \frac{1}{1+e^{-1}} = 0.731$
$z_2 = 1.0 \times 0.731 + 0 = 0.731$
$\hat{y} = \sigma(0.731) = \frac{1}{1+e^{-0.731}} = 0.675$

$\mathcal{L} = -[1 \times \log(0.675) + 0 \times \log(0.325)] = -\log(0.675) = 0.393$

计算图：
```
x=2 ──→ [×:w₁=0.5] ──→ [+:b₁=0] ──→ z₁=1.0 ──→ [σ] ──→ h=0.731
                                                              │
                                                              ↓
                                       ŷ=0.675 ←── [σ] ←── z₂=0.731 ←── [+:b₂=0] ←── [×:w₂=1.0]
                                                                                            ↑
                                                                                   h=0.731 ─┘
```

**(b)** 交叉熵对 $\hat{y}$ 的梯度（起点）：
$$\frac{\partial \mathcal{L}}{\partial \hat{y}} = -\frac{y}{\hat{y}} + \frac{1-y}{1-\hat{y}} = -\frac{1}{0.675} + \frac{0}{0.325} = -1.481$$

**(c)** 逐步反向传播：

> **第1步**：$\frac{\partial \mathcal{L}}{\partial z_2} = \frac{\partial \mathcal{L}}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z_2}$

Sigmoid导数：$\sigma'(z_2) = \hat{y}(1 - \hat{y}) = 0.675 \times 0.325 = 0.219$

$$\frac{\partial \mathcal{L}}{\partial z_2} = (-1.481) \times 0.219 = -0.325$$

> 验证：对于二分类交叉熵 + sigmoid 输出，$\frac{\partial \mathcal{L}}{\partial z_2} = \hat{y} - y = 0.675 - 1 = -0.325$ ✓

> **第2步**：$\frac{\partial \mathcal{L}}{\partial w_2} = \frac{\partial \mathcal{L}}{\partial z_2} \cdot \frac{\partial z_2}{\partial w_2}$

$\frac{\partial z_2}{\partial w_2} = h = 0.731$

$$\frac{\partial \mathcal{L}}{\partial w_2} = -0.325 \times 0.731 = -0.238$$

> **第3步**：$\frac{\partial \mathcal{L}}{\partial b_2} = \frac{\partial \mathcal{L}}{\partial z_2} \cdot \frac{\partial z_2}{\partial b_2} = -0.325 \times 1 = -0.325$

> **第4步**：$\frac{\partial \mathcal{L}}{\partial h} = \frac{\partial \mathcal{L}}{\partial z_2} \cdot \frac{\partial z_2}{\partial h}$

$\frac{\partial z_2}{\partial h} = w_2 = 1.0$

$$\frac{\partial \mathcal{L}}{\partial h} = -0.325 \times 1.0 = -0.325$$

> **第5步**：$\frac{\partial \mathcal{L}}{\partial z_1} = \frac{\partial \mathcal{L}}{\partial h} \cdot \frac{\partial h}{\partial z_1}$

$\sigma'(z_1) = h(1-h) = 0.731 \times 0.269 = 0.197$

$$\frac{\partial \mathcal{L}}{\partial z_1} = -0.325 \times 0.197 = -0.064$$

> **第6步**：$\frac{\partial \mathcal{L}}{\partial w_1} = \frac{\partial \mathcal{L}}{\partial z_1} \cdot \frac{\partial z_1}{\partial w_1}$

$\frac{\partial z_1}{\partial w_1} = x = 2$

$$\frac{\partial \mathcal{L}}{\partial w_1} = -0.064 \times 2 = -0.128$$

> **第7步**：$\frac{\partial \mathcal{L}}{\partial b_1} = \frac{\partial \mathcal{L}}{\partial z_1} \cdot 1 = -0.064$

**汇总**：

| 参数 | 梯度 |
|:---|:---|
| $w_1$ | $-0.128$ |
| $b_1$ | $-0.064$ |
| $w_2$ | $-0.238$ |
| $b_2$ | $-0.325$ |

**(d)** 验证：

令 $w_1' = 0.501$，重新前向：
- $z_1' = 0.501 \times 2 = 1.002$
- $h' = \sigma(1.002) = 0.7314$
- $z_2' = 1.0 \times 0.7314 = 0.7314$
- $\hat{y}' = \sigma(0.7314) = 0.6752$
- $\mathcal{L}' = -\log(0.6752) = 0.3926$

实际损失变化：$\Delta \mathcal{L}_{\text{actual}} = 0.3926 - 0.3929 = -0.00037$

梯度预测：$\Delta \mathcal{L}_{\text{pred}} = -0.128 \times 0.001 = -0.000128$

两者同号且量级接近（$\Delta$ 越小越精确），说明梯度计算基本正确。

</details>

---

### 习题 4 · 权重衰减（L2正则化）的梯度形式

> 📘 **考查**：L2正则化的数学形式和梯度含义 | 🏷️ **对应卡**：[[权重正则化]] [[梯度计算]]

**题目**：L2正则化（权重衰减）是防止过拟合的基本技术。

**(a)** 写出带L2正则化的损失函数：
$$\mathcal{L}_{\text{total}}(\mathbf{W}, b) = \mathcal{L}_{\text{data}}(\mathbf{W}, b) + \frac{\lambda}{2}\|\mathbf{W}\|_2^2$$
请解释为什么通常只对权重 $\mathbf{W}$ 施加正则化，而不对偏置 $b$ 施加正则化？

**(b)** 对权重 $\mathbf{W}$ 求梯度，证明：
$$\frac{\partial \mathcal{L}_{\text{total}}}{\partial \mathbf{W}} = \frac{\partial \mathcal{L}_{\text{data}}}{\partial \mathbf{W}} + \lambda \mathbf{W}$$

**(c)** 将上述梯度代入SGD更新公式 $\mathbf{W} \leftarrow \mathbf{W} - \eta \frac{\partial \mathcal{L}_{\text{total}}}{\partial \mathbf{W}}$，推导出更新规则的等价形式：
$$\mathbf{W} \leftarrow (1 - \eta\lambda)\mathbf{W} - \eta \frac{\partial \mathcal{L}_{\text{data}}}{\partial \mathbf{W}}$$
并解释为什么L2正则化被称为"权重衰减"（weight decay）。

**(d)** L1正则化 $\lambda\|\mathbf{W}\|_1$ 与L2正则化有什么不同的效果（从梯度形式和稀疏性角度分析）？

---

<details>
<summary><b>📝 参考答案</b></summary>

**(a)** 不对偏置正则化的原因：

1. **偏置参数量极少**：偏置仅 $O(h)$ 量级，而权重是 $O(d \times h)$ 量级。偏置过拟合的风险远小于权重。
2. **偏置控制的是决策边界的平移**：正则化偏置可能导致模型欠拟合（无法灵活调整激活阈值）。
3. **经验结论**：实践中正则化偏置几乎不改善泛化，反而可能降低模型容量。

> 一句话：正则化主要针对"自由度大"的参数。偏置自由度太小，不值得也不应该正则化。

**(b)** 求导：

$$\frac{\partial}{\partial \mathbf{W}}\left(\frac{\lambda}{2}\|\mathbf{W}\|_2^2\right) = \frac{\partial}{\partial \mathbf{W}}\left(\frac{\lambda}{2} \sum_{i,j} W_{ij}^2\right) = \lambda \mathbf{W}$$

因此：
$$\frac{\partial \mathcal{L}_{\text{total}}}{\partial \mathbf{W}} = \frac{\partial \mathcal{L}_{\text{data}}}{\partial \mathbf{W}} + \lambda \mathbf{W}$$

**(c)** SGD更新：

$$\begin{aligned}
\mathbf{W} &\leftarrow \mathbf{W} - \eta\left(\frac{\partial \mathcal{L}_{\text{data}}}{\partial \mathbf{W}} + \lambda \mathbf{W}\right) \\
&= \mathbf{W} - \eta\lambda\mathbf{W} - \eta\frac{\partial \mathcal{L}_{\text{data}}}{\partial \mathbf{W}} \\
&= (1 - \eta\lambda)\mathbf{W} - \eta\frac{\partial \mathcal{L}_{\text{data}}}{\partial \mathbf{W}}
\end{aligned}$$

**"权重衰减"的含义**：每一步更新中，权重先被因子 $(1-\eta\lambda)$ 缩小（"衰减"），再按数据梯度方向更新。$\eta\lambda$ 通常很小（如 $\eta=0.01, \lambda=0.0005$，则 $1-\eta\lambda=0.999995$），但累积多步后效果显著。

> ⚠️ 注意：对于带动量的优化器（如Adam），L2正则化与真正的"解耦权重衰减"（decoupled weight decay，如AdamW）并不等价。AdamW将权重衰减从自适应学习率中解耦出来，效果更好。

**(d)** L1 vs L2：

| | L2正则化 $\lambda\|\mathbf{W}\|_2^2$ | L1正则化 $\lambda\|\mathbf{W}\|_1$ |
|:---|:---|:---|
| 梯度贡献 | $\lambda \mathbf{W}$（与权重成正比） | $\lambda \cdot \text{sign}(\mathbf{W})$（固定步长） |
| 更新行为 | 所有权重均匀缩小 | 所有权重向零移动相同距离 |
| 稀疏性 | 产生小但不为零的权重 | **产生稀疏解**（许多权重精确为0） |
| 几何解释 | 约束在L2球内 | 约束在L1菱形内，角点对应稀疏解 |
| 典型应用 | 通用正则化（大多数情况） | 特征选择、可解释性要求高的场景 |

> 直觉：L1给所有权重相同的"推力"推向零，小权重先被推成零；L2对大权重的惩罚更强，对小权重惩罚更弱，因此小权重趋于变小但不归零。

</details>

---

### 习题 5 · Dropout的训练/测试差异

> 📘 **考查**：Dropout的机制与训练-推理行为差异 | 🏷️ **对应卡**：[[Dropout]] [[数据增强与正则化]]

**题目**：Dropout是一种在训练时随机丢弃神经元的技术。

**(a)** 描述Dropout在**训练时**的具体操作：设丢弃概率为 $p$（如 $p=0.5$），写出每个神经元输出 $h_i$ 经过Dropout后的数学表达式，并解释"inverted dropout"（反向Dropout）的缩放策略。

**(b)** 在**测试/推理时**，Dropout的行为是什么？为什么测试时不能随机丢弃？如果不做任何调整，训练时的期望输出和测试时的期望输出有什么差异？

**(c)** 从"集成学习"（ensemble）的角度解释Dropout为什么能正则化：一个含 $n$ 个神经元的隐藏层，训练时采样了多少种可能的子网络？测试时等价于什么操作？

**(d)** 一句话回答：Dropout和权重衰减（L2正则化）的正则化机理有什么本质不同？

---

<details>
<summary><b>📝 参考答案</b></summary>

**(a)** 训练时操作（Inverted Dropout）：

以丢弃概率 $p$（保留概率 $1-p$）为例：

$$\tilde{h}_i = \begin{cases} 0 & \text{以概率 } p \\ \frac{h_i}{1-p} & \text{以概率 } 1-p \end{cases}$$

等价写法：$\tilde{h}_i = h_i \cdot \frac{m_i}{1-p}$，其中 $m_i \sim \text{Bernoulli}(1-p)$。

**Inverted Dropout** 的核心：训练时对保留的神经元**除以 $(1-p)$** 进行放大，使得训练时的期望输出 $\mathbb{E}[\tilde{h}_i] = h_i$，与测试时一致。这样测试时无需任何缩放，直接使用原始输出即可。

> 对比"vanilla dropout"（非反向）：训练时不缩放、测试时乘 $(1-p)$。Inverted Dropout 在现代框架中为标准做法，因为它让推理零开销。

**(b)** 测试时行为：

测试时**不丢弃任何神经元**，直接输出 $h_i$（不做任何缩放）。

**不用随机丢弃的原因**：
1. 测试需要确定性输出（相同输入 → 相同输出）
2. 随机丢弃引入噪声，降低测试性能
3. 训练时已通过除以 $(1-p)$ 缩放，使训练期望 = 测试输出

**不调整时的差异**：如果训练时使用"保留/丢弃"但不缩放，训练时每个神经元的期望输出 = $(1-p) \cdot h_i$（被压低了），而测试时输出 = $h_i$（完整值）→ 训练和测试的激活分布不匹配，测试时输出会系统性地大于训练期望。

**(c)** 集成视角：

含 $n$ 个神经元的隐藏层，每个神经元有"保留/丢弃"两种状态 → 共有 $2^n$ 种可能的子网络结构。

- **训练时**：每个mini-batch采样一个子网络，等效于在 $2^n$ 个不同网络上进行随机训练
- **测试时**：使用完整网络，但每个神经元权重隐式地被"平均"了 —— 等效于对 $2^n$ 个子网络的预测做**几何平均近似**（模型组合/ensemble）

> Dropout ≈ 以极低成本训练了一个 $2^n$ 规模的隐式集成模型。每个子网络共享参数，训练时互相正则化。

**(d)** 本质区别：

- **权重衰减（L2）**：对参数值直接施加约束，防止任何单个权重过大 → 属于**参数范数惩罚**
- **Dropout**：在特征层面注入噪声，迫使每个神经元不能依赖特定同伴的存在 → 属于**特征层面的扰动正则化**，打破神经元间的"共适应"（co-adaptation）

> 一句总结：L2惩罚"权重不能太大"；Dropout惩罚"神经元不能太依赖彼此"。

</details>

---

### 习题 6 · 数值稳定性与梯度消失/爆炸

> 📘 **考查**：深度网络训练中的数值问题 | 🏷️ **对应卡**：[[梯度流问题]] [[批归一化BatchNorm]]

**题目**：训练深层MLP时，数值稳定性是影响收敛的关键因素。

**(a)** **梯度消失**和**梯度爆炸**分别指什么现象？从反向传播链式法则的角度，写出第 $l$ 层梯度 $\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}}$ 中包含的连乘因子，并说明什么情况下会导致消失、什么情况下会导致爆炸。

**(b)** **Xavier初始化**（Glorot初始化）的核心思想是什么？写出其推荐的权重方差：$\text{Var}(W) = \frac{2}{n_{\text{in}} + n_{\text{out}}}$（Xavier）和 $\text{Var}(W) = \frac{2}{n_{\text{in}}}$（He/何恺明初始化），并解释为什么He初始化更适合ReLU网络。

**(c)** 计算 Softmax 时，直接计算 $\frac{e^{z_i}}{\sum_j e^{z_j}}$ 可能产生数值问题。请举例说明当 $z_i$ 很大时会发生什么，并给出稳定计算方案（log-sum-exp技巧）。

**(d)** 你正在训练一个20层MLP，发现训练刚开始几轮后损失变成NaN。请列出至少三种可能的原因及对应的排查/修复方法。

---

<details>
<summary><b>📝 参考答案</b></summary>

**(a)** 梯度消失与爆炸：

第 $l$ 层梯度的连乘形式（忽略激活函数的细节）：

$$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} \propto \prod_{k=l+1}^{L} \left( \mathbf{W}^{(k)\top} \cdot \text{diag}(\sigma'(\mathbf{z}^{(k)})) \right)$$

- **梯度消失**：当 $|\sigma'(\mathbf{z}^{(k)})| < 1$ 且 $\|\mathbf{W}^{(k)}\| < 1$ 时，连乘因子指数级趋近于0。典型场景：Sigmoid/Tanh激活 + 小权重初始化 → 浅层梯度 $\approx 0$。
- **梯度爆炸**：当 $\|\mathbf{W}^{(k)}\| > 1$ 且激活函数导数不衰减时，连乘因子指数级增长。典型场景：大权重初始化 + ReLU激活（正区梯度=1） → 梯度溢出为NaN。

> 两种现象都随网络深度 $L$ 指数级恶化。本质是连乘结构的**不稳定性放大**。

**(b)** 初始化策略：

**核心思想**：让每层输出的方差 = 每层输入的方差，使信号在前向和反向传播中方差保持一致，不衰减也不放大。

- **Xavier（Glorot）初始化**：$W \sim \mathcal{N}\left(0, \frac{2}{n_{\text{in}} + n_{\text{out}}}\right)$ 或 $\mathcal{U}\left[-\frac{\sqrt{6}}{\sqrt{n_{\text{in}} + n_{\text{out}}}}, \frac{\sqrt{6}}{\sqrt{n_{\text{in}} + n_{\text{out}}}}\right]$
  - 推导假设：激活函数是线性的（或Tanh，在零附近近似线性）
  
- **He初始化**：$W \sim \mathcal{N}\left(0, \frac{2}{n_{\text{in}}}\right)$ 或 $\mathcal{U}\left[-\frac{\sqrt{6}}{\sqrt{n_{\text{in}}}}, \frac{\sqrt{6}}{\sqrt{n_{\text{in}}}}\right]$
  - 推导假设：激活函数是ReLU（负半区输出为零，方差减半）

**为什么He更适合ReLU**：ReLU将负半区的输出截断为0，导致输出方差变为输入方差的一半。He通过 $\frac{2}{n_{\text{in}}}$（比Xavier多一个因子2）补偿这一减半效应，使ReLU网络各层方差保持一致。

**(c)** Softmax数值稳定性：

**问题**：当 $z_i = 1000$ 时，$e^{1000} \approx \infty$（float32溢出），直接计算产生 `inf/nan`。

**稳定方案（log-sum-exp）**：

令 $M = \max_j z_j$（每行取最大），则：

$$\text{softmax}(z_i) = \frac{e^{z_i - M}}{\sum_j e^{z_j - M}}$$

因为分子分母同除以 $e^M$，数学上恒等。但数值上 $z_i - M \le 0$，$e^{\le 0} \in (0, 1]$，完全避免溢出。

```python
def stable_softmax(z):
    z_max = z.max(axis=-1, keepdims=True)
    exp_z = np.exp(z - z_max)
    return exp_z / exp_z.sum(axis=-1, keepdims=True)
```

同理，计算 $\log\text{softmax}$ 时直接使用：
$$\log\text{softmax}(z_i) = z_i - M - \log\sum_j e^{z_j - M}$$

**(d)** Loss变NaN的排查：

| 可能原因 | 排查方法 | 修复方案 |
|:---|:---|:---|
| 学习率过大 | 逐步降低lr（如除以10），观察是否消失 | 使用warmup、更小的lr、或自适应优化器 |
| 权重初始化不当 | 检查各层输出的均值和方差 | 使用Xavier/He初始化 |
| 梯度爆炸 | 打印梯度范数，观察是否随时间指数增长 | 梯度裁剪（`clip_grad_norm_`）、BatchNorm |
| 数据中有NaN/Inf | 检查输入数据的 `np.isnan().any()` | 清洗数据，添加数据预处理断言 |
| Softmax上溢（如上题） | 检查logits的值域 | 使用log-sum-exp稳定计算 |
| $\log(0)$ 或除零 | 检查损失函数中是否出现 $-\log(0)$ | 添加 $\epsilon$ 平滑（如 `log(x + 1e-8)`） |

</details>

---

### 习题 7 · MLP从零实现思路

> 📘 **考查**：模块化设计、前向/反向分离、梯度检查 | 🏷️ **对应卡**：[[MLP]] [[前向传播]] [[反向传播与计算图]]

**题目**：设计一个从零实现的MLP训练框架（仅用NumPy），不使用PyTorch/TensorFlow等自动求导框架。

**(a)** 写出需要实现的**核心模块**清单（至少5个模块），并说明每个模块的职责。提示：从数据流和训练循环两个维度来思考。

**(b)** 以**线性层（全连接层）**为例，写出 `forward` 和 `backward` 的伪代码或NumPy实现。`forward` 必须显式缓存反向传播所需的中间值。

**(c)** 训练循环的伪代码应包括哪些关键步骤？写出一个 epoch 的执行流程（含梯度清零、前向、反向、参数更新、loss记录）。

**(d)** 你如何验证反向传播的实现是否正确？描述梯度检查（gradient check）的原理和步骤，并写出核心代码逻辑。

---

<details>
<summary><b>📝 参考答案</b></summary>

**(a)** 核心模块清单：

| 模块 | 职责 |
|:---|:---|
| `Linear`（全连接层） | 封装 $\mathbf{W}, \mathbf{b}$，提供 `forward` 和 `backward` |
| `ReLU` / `Sigmoid`（激活函数） | 逐元素非线性变换 + 反向传播 |
| `Dropout`（可选正则化） | 训练时随机掩码 + 缩放；测试时恒等映射 |
| `Sequential`（层容器） | 按顺序组合多个层，自动串联 forward/backward |
| `CrossEntropyLoss`（损失函数） | 计算损失值 + 提供反向传播起点梯度 |
| `SGD` / `Adam`（优化器） | 接收梯度，更新参数 |
| `DataLoader`（数据迭代器） | Mini-batch采样、shuffle |

> 也可以把 Softmax 和 CrossEntropy 合并为一个 `SoftmaxCrossEntropy` 模块以获得数值稳定性。

**(b)** 线性层的 forward/backward：

```python
import numpy as np

class Linear:
    def __init__(self, in_features, out_features):
        # He初始化
        self.W = np.random.randn(in_features, out_features) * np.sqrt(2.0 / in_features)
        self.b = np.zeros((1, out_features))
        self.cache = {}  # 缓存前向中间值

    def forward(self, x):
        # x: (N, in_features)
        self.cache['x'] = x          # 缓存输入，反向时计算 dW
        out = x @ self.W + self.b    # (N, out_features)
        return out

    def backward(self, dout):
        # dout: (N, out_features) — 上游梯度
        x = self.cache['x']
        self.dW = x.T @ dout          # (in_features, out_features)
        self.db = dout.sum(axis=0, keepdims=True)  # (1, out_features)
        dx = dout @ self.W.T          # (N, in_features) — 传给前一层
        return dx
```

> 关键：`cache['x']` 存储输入，因为 $\frac{\partial z}{\partial \mathbf{W}} = \mathbf{x}^\top$，反向传播必须用到前向时的 $\mathbf{x}$ 值。

**(c)** 一个 epoch 的训练循环：

```python
def train_epoch(model, dataloader, loss_fn, optimizer):
    total_loss = 0.0
    for x_batch, y_batch in dataloader:
        # ─── 1. 前向传播 ───
        logits = model.forward(x_batch)          # 逐层前向
        loss = loss_fn.forward(logits, y_batch)  # 计算损失
        total_loss += loss

        # ─── 2. 反向传播 ───
        dout = loss_fn.backward()                # 损失层的梯度（起点）
        model.backward(dout)                     # 逐层反向，累积到各层 dW/db

        # ─── 3. 参数更新 ───
        optimizer.step(model.parameters())       # W -= lr * dW
        optimizer.zero_grad(model.parameters())  # 清零梯度（防止累积）
    
    return total_loss / len(dataloader)
```

> 关键细节：`zero_grad()` 必须在每个batch开始前（而不是结束后）调用。通常放在循环最开头或 `step()` 之后。

**(d)** 梯度检查：

**原理**：用数值梯度（有限差分）逼近解析梯度，两者相对误差应 $< 10^{-7}$（float64）。

**步骤**：
1. 用极小随机输入做一次前向+反向，获得解析梯度
2. 对每个参数，用中心差分计算数值梯度：$\frac{\partial L}{\partial \theta} \approx \frac{L(\theta+\epsilon) - L(\theta-\epsilon)}{2\epsilon}$
3. 比较相对误差

```python
def gradient_check(model, loss_fn, x, y, eps=1e-5):
    # 1. 解析梯度
    logits = model.forward(x)
    loss = loss_fn.forward(logits, y)
    dout = loss_fn.backward()
    model.backward(dout)

    for layer in model.layers:
        for param_name in ['W', 'b']:
            param = getattr(layer, param_name)
            grad_analytic = getattr(layer, f'd{param_name}')
            grad_numerical = np.zeros_like(param)

            # 2. 对每个元素做中心差分
            it = np.nditer(param, flags=['multi_index'])
            while not it.finished:
                idx = it.multi_index
                old_val = param[idx]

                param[idx] = old_val + eps
                loss_plus = loss_fn.forward(model.forward(x), y)

                param[idx] = old_val - eps
                loss_minus = loss_fn.forward(model.forward(x), y)

                grad_numerical[idx] = (loss_plus - loss_minus) / (2 * eps)
                param[idx] = old_val  # 恢复
                it.iternext()

            # 3. 相对误差
            diff = np.abs(grad_analytic - grad_numerical)
            denom = np.abs(grad_analytic) + np.abs(grad_numerical) + 1e-8
            rel_error = diff.max() / denom.max()
            
            if rel_error > 1e-4:
                print(f"❌ {param_name} gradient check FAILED: {rel_error:.2e}")
            else:
                print(f"✅ {param_name} gradient check passed: {rel_error:.2e}")
```

> 实践经验：先用 `float64` 做梯度检查（误差 $< 10^{-7}$），通过后再切回 `float32` 训练。梯度检查只在小规模设置下进行（参数量大会极慢）。

</details>

---

### 习题 8 · MLP与线性模型的根本区别

> 📘 **考查**：非线性变换与表示学习 | 🏷️ **对应卡**：[[感知机]] [[MLP]]

**题目**：

**(a)** 如果MLP中所有隐藏层的激活函数都换成**恒等函数** $f(x) = x$（即不使用激活函数），证明该MLP等价于一个单层线性模型。要求用矩阵乘法进行推导（以两层隐藏层为例）。

**(b)** 由此出发，用一句话总结：激活函数（非线性）在MLP中扮演的**不可替代**的角色是什么？

**(c)** 什么是**万能逼近定理**（Universal Approximation Theorem）？它的核心结论是什么？它有什么**局限性**（在实际应用中的约束）？

**(d)** 对于如下二分类数据集，为什么线性模型（感知机）无法完美分类，而带一个隐藏层的MLP可以？请用几何直觉解释。

```
类别A的点（○）：(0,0), (0,1), (1,0), (1,1) 中位于 x₁+x₂ > 1 的点
类别B的点（×）：(0,0), (0,1), (1,0), (1,1) 中位于 x₁+x₂ ≤ 1 的点
```
即：这是一个包含4个点的平面，请画出点的分布，判断它是否线性可分。

---

<details>
<summary><b>📝 参考答案</b></summary>

**(a)** 证明：

设两层隐藏层的MLP（无激活函数）：

$$\begin{aligned}
\mathbf{h}^{(1)} &= \mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)} \\
\mathbf{h}^{(2)} &= \mathbf{W}^{(2)}\mathbf{h}^{(1)} + \mathbf{b}^{(2)} \\
\mathbf{o} &= \mathbf{W}^{(3)}\mathbf{h}^{(2)} + \mathbf{b}^{(3)}
\end{aligned}$$

代入展开：
$$\begin{aligned}
\mathbf{o} &= \mathbf{W}^{(3)}(\mathbf{W}^{(2)}(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}) + \mathbf{b}^{(2)}) + \mathbf{b}^{(3)} \\
&= \mathbf{W}^{(3)}\mathbf{W}^{(2)}\mathbf{W}^{(1)}\mathbf{x} + \mathbf{W}^{(3)}\mathbf{W}^{(2)}\mathbf{b}^{(1)} + \mathbf{W}^{(3)}\mathbf{b}^{(2)} + \mathbf{b}^{(3)}
\end{aligned}$$

令 $\tilde{\mathbf{W}} = \mathbf{W}^{(3)}\mathbf{W}^{(2)}\mathbf{W}^{(1)}$，$\tilde{\mathbf{b}} = \mathbf{W}^{(3)}\mathbf{W}^{(2)}\mathbf{b}^{(1)} + \mathbf{W}^{(3)}\mathbf{b}^{(2)} + \mathbf{b}^{(3)}$

则 $\mathbf{o} = \tilde{\mathbf{W}}\mathbf{x} + \tilde{\mathbf{b}}$ —— 这正是单层线性模型的形式。

> 结论：任意多层线性变换的复合仍然是线性变换。没有非线性激活函数，无论堆叠多少层，模型的表达能力都不会超过单层线性模型。

**(b)** 一句话：

**激活函数是MLP从"线性变换的堆叠（仍然线性）"跃升为"非线性函数逼近器"的唯一要素。没有非线性，深度就没有意义。**

**(c)** 万能逼近定理：

**核心结论**：具有单个隐藏层、包含足够多神经元、使用Sigmoid类（非多项式）激活函数的前馈网络，可以在任意精度下逼近任何定义在紧致子集上的连续函数。

即：$\forall \epsilon > 0, \forall f \in C(K)$（$K \subset \mathbb{R}^n$ 紧致），$\exists$ 单隐层网络 $g$ 使得 $\sup_{x \in K} |f(x) - g(x)| < \epsilon$。

**局限性**：
1. **没说需要多少神经元**：理论上可能需要指数级数量的隐藏神经元才能逼近某些函数
2. **没说如何找到参数**：定理只保证存在性，不保证SGD能学到。实际训练可能收敛到局部最优
3. **深度 > 宽度**：实践中，深层窄网络通常比浅层宽网络更高效（参数效率更高）——这是深度学习的核心经验
4. **紧致集假设**：函数定义域必须是有界闭集，不适用于无界域

> 万能逼近定理是MLP的"理论下限"——它告诉我们单隐层就足够"表达"任何函数，但没说"学到"需要多少层/神经元/数据。

**(d)** 几何分析：

四个点的分布：

| $(x_1, x_2)$ | $x_1 + x_2$ | 类别 |
|:---|:---|:---|
| (0,0) | 0 | B（×） |
| (0,1) | 1 | B（×） |
| (1,0) | 1 | B（×） |
| (1,1) | 2 | A（○） |

画出平面：
```
 x₂
 1 │  ×           ○
   │
 0 │  ×           ×
   └────────────────────
      0           1     x₁
```

- B类：(0,0), (0,1), (1,0) 三个点
- A类：(1,1) 一个点

**线性不可分**：不存在一条直线能将 A（○）和 B（×）分开，因为B类三个点已经包围了A类。任何直线划分都会至少混入一个错误类别。

**MLP可解**：一个隐藏层（含至少2个ReLU神经元）可以学到如下变换：
- 神经元1：$\text{ReLU}(x_1 + x_2 - 1.5)$ → 只在(1,1)时为正
- 神经元2：$\text{ReLU}(-x_1 - x_2 + 0.5)$ → 仅在(0,0)时为正

两个隐藏特征将原始空间映射到一个新的2D空间中，使得在新空间中数据变得线性可分。这正是MLP相对于线性模型的本质优势：**通过非线性变换将不可分的数据映射到可分空间**。

</details>

---

## 🔗 习题→知识卡映射速查

| 习题 | 对应知识卡 |
|:---|:---|
| 习题1：前向传播矩阵推导 | [[前向传播]] [[线性代数基础CV]] |
| 习题2：激活函数选择 | [[激活函数CV]] [[反向传播与计算图]] |
| 习题3：反向传播手算 | [[反向传播与计算图]] [[链式法则]] |
| 习题4：权重衰减梯度 | [[权重正则化]] [[梯度计算]] |
| 习题5：Dropout训练/测试 | [[Dropout]] [[数据增强与正则化]] |
| 习题6：数值稳定性 | [[梯度流问题]] [[批归一化BatchNorm]] |
| 习题7：MLP从零实现 | [[MLP]] [[前向传播]] [[反向传播与计算图]] |
| 习题8：MLP vs 线性模型 | [[感知机]] [[MLP]] |

---

## 📐 使用建议

1. **最小完成路径**：习题 1 → 3 → 8 覆盖MLP核心理解（前向、反向、非线性本质）
2. **强化数学推导**：习题 3 + 4 逐层手算梯度，是面试和考试的高频题型
3. **工程实战辅助**：习题 7 建议配合 [[../18-实战作业说明书/🎓 HW02 - 两层网络与反向传播正确性验证正式作业说明书\|HW02]] 一起完成
4. **查漏补缺**：习题 2 + 5 + 6 覆盖训练中常见的"为什么训不动/训崩了"的排查知识

---

*基于 D2L Ch.5（CC BY-SA 4.0）编写 | 最后更新 2026-08-05*
