---
title: "反向传播算法 (Backpropagation)"
date: 2026-07-27
type: concept
course: "深度学习 / 机器学习"
importance: "A"
tags: [学习, 深度学习, 机器学习, 反向传播, BP, 自动求导, 链式法则]
upstream: ["[[02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/神经网络|神经网络]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/计算图|计算图]]"]
downstream: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/PyTorchOptimizer|PyTorchOptimizer]]", "[[17-机器学习/03-正则优化/深度优化器|深度优化器]]"]
status: learning
---

# 🎯 反向传播算法 (Backpropagation)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：反向传播（BP）算法是整个深度学习训练的“心脏”。它巧妙利用多元微积分的**链式法则（Chain Rule）**，通过由输出层向输入层反向高效传递误差梯度 $\delta^{(l)}$，避免了大量的重复计算，将深层神经网络所有参数求导的计算复杂度从指数级 $O(2^L)$ 降低至与前向传播同阶的线性复杂度 $O(|E|)$。如果不搞懂 BP，后续的自动求导、梯度爆炸/消失、神经网络调优均无法真正理解。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 在 1980 年代以前，人们知道多层感知机（MLP）理论上能表达非线性函数，但**根本不知道该如何训练它**。深层网络包含成千上万甚至数十亿个权重参数 $W$，当最终输出产生错误（Loss 大）时，我们只知道整个网络错了，却不知道“具体是哪一层、哪一个神经元的哪根权重调大或调小了多少”。
> 如果对每个权重用数值微分（给 $w_{ij}$ 加个微小变化 $\epsilon$ 跑一遍前向传播计算导数），对于百万级参数的网络，计算一次梯度就需要跑百万遍前向传播，计算量浩瀚无穷，网络训练彻底卡死。BP 算法正是在这个背景下诞生，只用**一次前向传播 + 一次反向传递**，就能求出所有权重的精确梯度！

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：BP 是连接“模型定义/损失函数”与“优化器参数更新（SGD/Adam）”之间的桥梁。不理解 BP，就无法明白为什么深层网络会发生梯度消失/爆炸，也无法理解 ResNet 残差连接和 Transformer 架构的设计动机。
- **实际应用场景**：所有现代深度学习框架（PyTorch、TensorFlow、JAX）的底层自动求导引擎（Autograd）都是反向传播算法的工程实现。
- **高频考点/任务**：手写两层神经网络 BP 推导（笔试高频）、 PyTorch `loss.backward()` 原理解析、梯度检查（Gradient Checking）代码实现。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/链式法则|多元复合函数链式法则]]**：若 $z = f(u, v)$ 且 $u = g(x), v = h(x)$，则 $\frac{d z}{d x} = \frac{\partial z}{\partial u} \frac{d u}{d x} + \frac{\partial z}{\partial v} \frac{d v}{d x}$。BP 的核心思想就是沿着计算图逆向累加链式偏导。
2. **[[02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/神经网络|前向传播与矩阵乘法]]**：网络第 $l$ 层净输入为 $\mathbf{z}^{(l)} = \mathbf{W}^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}$，激活输出为 $\mathbf{a}^{(l)} = \sigma(\mathbf{z}^{(l)})$。

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：想象一个大型工厂接力流水线（输入层 $\to$ 隐藏层 $\to$ 输出层）。最后出来的产品质量不合格（Loss 大），总厂长要求追究责任：
  - **前向传播**：原料一层层加工成产品；
  - **反向传播**：质检员从最后一级（输出层）倒回去问：“终检组差了多少？倒数第二组贡献了多少偏差？第一组原料切削差了多少？”每一层把分配到的责任（误差信号 $\delta$）按权重比例反向分发给上一层工序。每个工人（权重 $W$）根据自己分配到的责任大小，微调自己的操作。
- **为什么很自然**：因为靠后层的偏导数在计算靠前层偏导数时必然会被反复用到，逆向计算可以**复用中间结果**。
- **一句话直觉本质**：用链式法则逆向复用计算结果，把最终误差“按劳分配”回每个权重。

---

## 5. 正式定义、核心公式、符号解释

### 1. 核心定义
定义第 $l$ 层第 $j$ 个神经元在激活前净输入 $z_j^{(l)}$ 上的偏导数为**节点误差信号 (Error Signal)**：
$$\delta_j^{(l)} = \frac{\partial J}{\partial z_j^{(l)}}$$

### 2. 核心四大公式 (BP 核心矩阵形式)

1. **输出层误差**（以 MSE 损失 $J = \frac{1}{2}\|\mathbf{a}^{(L)} - \mathbf{y}\|^2$ 为例）：
   $$\boldsymbol{\delta}^{(L)} = (\mathbf{a}^{(L)} - \mathbf{y}) \odot \sigma'(\mathbf{z}^{(L)})$$
2. **隐藏层误差递推（反向传递）**：
   $$\boldsymbol{\delta}^{(l)} = \left( (\mathbf{W}^{(l+1)})^T \boldsymbol{\delta}^{(l+1)} \right) \odot \sigma'(\mathbf{z}^{(l)})$$
3. **权重参数梯度**：
   $$\frac{\partial J}{\partial \mathbf{W}^{(l)}} = \boldsymbol{\delta}^{(l)} (\mathbf{a}^{(l-1)})^T$$
4. **偏置参数梯度**：
   $$\frac{\partial J}{\partial \mathbf{b}^{(l)}} = \boldsymbol{\delta}^{(l)}$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $J$ | 标量损失值 (Loss) | $[0, +\infty)$ | 全局标量标靶 |
| $\mathbf{z}^{(l)}$ | 第 $l$ 层神经元净输入 (Pre-activation) | $\mathbb{R}^{n_l}$ | 未通过激活函数的向量 |
| $\mathbf{a}^{(l)}$ | 第 $l$ 层激活输出 (Post-activation) | $\mathbb{R}^{n_l}$ | $\mathbf{a}^{(0)}=\mathbf{x}$ 为输入 |
| $\mathbf{W}^{(l)}$ | 第 $l-1$ 层到第 $l$ 层的权重矩阵 | $\mathbb{R}^{n_l \times n_{l-1}}$ | 待优化的主参数 |
| $\boldsymbol{\delta}^{(l)}$ | 第 $l$ 层的节点误差向量 | $\mathbb{R}^{n_l}$ | 反向传递的递推介质 |
| $\odot$ | Hadamard 积 (Element-wise product) | N/A | 逐元素按位相乘 |

---

## 6. 推导思路和思想来源

- **最初困难**：直接对深层权值 $w_{ij}^{(l)}$ 求解 $\frac{\partial J}{\partial w_{ij}^{(l)}}$ 时，表达式极其冗长且包含大量重叠项。
- **关键转念**：引入中间变量 $\mathbf{z}^{(l)}$！利用链式法则拆解为：
  $$\frac{\partial J}{\partial w_{ij}^{(l)}} = \frac{\partial J}{\partial z_i^{(l)}} \cdot \frac{\partial z_i^{(l)}}{\partial w_{ij}^{(l)}}$$
  观察两部分：第二部分 $\frac{\partial z_i^{(l)}}{\partial w_{ij}^{(l)}} = a_j^{(l-1)}$（即上一层输入，前向已算好）；第一部分正是误差信号 $\delta_i^{(l)}$。
- **推导主线**：
  1. 求解 $\delta_i^{(l)}$ 时，利用全微分定理，前一层 $z_i^{(l)}$ 的改变会通过影响下一层所有神经元 $z_k^{(l+1)}$ 进而影响 Loss。
  2. 因此：$\delta_i^{(l)} = \frac{\partial J}{\partial z_i^{(l)}} = \sum_{k} \frac{\partial J}{\partial z_k^{(l+1)}} \cdot \frac{\partial z_k^{(l+1)}}{\partial z_i^{(l)}} = \sum_{k} \delta_k^{(l+1)} \cdot (w_{ki}^{(l+1)} \sigma'(z_i^{(l)}))$。
  3. 提公因式 $\sigma'(z_i^{(l)})$，转写为矩阵乘法即得到：$\boldsymbol{\delta}^{(l)} = \left( (\mathbf{W}^{(l+1)})^T \boldsymbol{\delta}^{(l+1)} \right) \odot \sigma'(\mathbf{z}^{(l)})$。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（单神经元链条可手算）
- **题目**：设单输入单隐藏层网络：$x = 2$, $w_1 = 0.5, b_1 = 0$, 激活函数 $\sigma(z) = z$（恒等），$w_2 = 1.5, b_2 = 0$，真实目标 $y = 5$。损失函数 $J = \frac{1}{2}(a_2 - y)^2$。求 $\frac{\partial J}{\partial w_1}$。
- **解题思路**：
  1. 前向计算：$z_1 = 2 \times 0.5 = 1 \implies a_1 = 1$；$z_2 = 1 \times 1.5 = 1.5 \implies a_2 = 1.5$。
  2. 计算 Loss：$J = \frac{1}{2}(1.5 - 5)^2 = 6.125$。
  3. 反向计算：
     - 输出误差 $\delta_2 = \frac{\partial J}{\partial a_2} \cdot \sigma'(z_2) = (1.5 - 5) \times 1 = -3.5$。
     - 隐藏误差 $\delta_1 = \delta_2 \cdot w_2 \cdot \sigma'(z_1) = -3.5 \times 1.5 \times 1 = -5.25$。
     - 参数梯度 $\frac{\partial J}{\partial w_1} = \delta_1 \cdot x = -5.25 \times 2 = -10.5$。
- **🤔 追问**：若激活函数换为 Sigmoid $\sigma(z) = \frac{1}{1+e^{-z}}$，求出的梯度会变大还是变小？
  - *答*：变小！因为 Sigmoid 导数 $\sigma'(1) = \sigma(1)(1-\sigma(1)) \approx 0.731 \times 0.269 \approx 0.196 < 1$，导数相乘导致误差信号被衰减。

### 例子 2：中等例子（矩阵形式两层 MLP）
考虑输入 $d=2$、隐藏层 $m=2$、输出 $k=1$ 的网络，推导并写出批次大小为 $B$ 时的矩阵求导维度对应关系。
- **维度确认**：$\mathbf{X} \in \mathbb{R}^{B \times 2}$，$\mathbf{W}^{(1)} \in \mathbb{R}^{2 \times 2}$，$\mathbf{Z}^{(1)} = \mathbf{X} \mathbf{W}^{(1)} \in \mathbb{R}^{B \times 2}$，$\mathbf{W}^{(2)} \in \mathbb{R}^{2 \times 1}$，$\boldsymbol{\Delta}^{(2)} \in \mathbb{R}^{B \times 1}$。
- **矩阵梯度公式**：$\frac{\partial J}{\partial \mathbf{W}^{(1)}} = \mathbf{X}^T \boldsymbol{\Delta}^{(1)}$，维度为 $(2 \times B) \times (B \times 2) = (2 \times 2)$，与 $\mathbf{W}^{(1)}$ 维度完全一致。

### 例子 3：实际应用（PyTorch 手写 Autograd 算子）
在实际深度学习框架中，每个自定义算子必须实现 `forward` 与 `backward` 静态方法：

```python
import torch

class CustomLinearFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, weight, bias=None):
        # 缓存前向中间结果用于反向传播
        ctx.save_for_backward(input, weight, bias)
        output = input.mm(weight.t())
        if bias is not None:
            output += bias.unsqueeze(0)
        return output

    @staticmethod
    def backward(ctx, grad_output):
        # grad_output 即上游传下来的 𝛿
        input, weight, bias = ctx.saved_tensors
        grad_input = grad_weight = grad_bias = None

        if ctx.needs_input_grad[0]:
            grad_input = grad_output.mm(weight) # 𝛿^(l) = 𝛿^(l+1) W^(l+1)
        if ctx.needs_input_grad[1]:
            grad_weight = grad_output.t().mm(input) # 𝛿^(l) (a^(l-1))^T
        if bias is not None and ctx.needs_input_grad[2]:
            grad_bias = grad_output.sum(0)

        return grad_input, grad_weight, grad_bias
```

---

## 8. 常见误区和易混概念

### 误区 1：反向传播就是梯度下降算法 (SGD)
- **错误直觉**：“我运行了反向传播，模型的参数就被更新了。”
- **为什么错**：反向传播仅负责**计算**所有参数对损失函数的偏导数（梯度 $\nabla_{\theta} J$）；真正拿着梯度去修改参数（例如 $\theta \leftarrow \theta - \eta \nabla_{\theta} J$）的是优化器（SGD/Adam）。
- **正确理解**：BP 是“测量测绘仪”（算梯度），SGD 是“施工队”（改参数）。

### 误区 2：反向传播中权重更新是同时发生的
- **错误直觉**：前一层权重先更新，更新后的权重再参与后一层的梯度计算。
- **为什么错**：在一次反向传播迭代中，所有梯度都是基于**当前前向传播那一刻保存的模型参数**一次性求出的，计算完成后由优化器统一全网同步更新。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| **反向传播 (BP)** | 计算梯度的算法 | 基于计算图的逆向自动求导，计算复杂度 $O(N)$ | 神经网络训练求导 |
| **数值微分** | 计算梯度的近似 | 用 $\frac{f(x+\epsilon)-f(x)}{\epsilon}$，复杂度 $O(N^2)$ | 梯度检查 (Gradient Check) |
| **梯度下降 (SGD)** | 参数更新优化策略 | 利用求得的梯度迭代更新权重 $\theta$ | 参数学习与优化 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/神经网络|神经网络]]：了解 MLP 的前向传播结构与激活函数。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/链式法则|链式法则]]：微积分基础，BP 的核心推导工具。

### 下游延伸
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/梯度流问题|梯度流问题]]：BP 链式连乘导致梯度消失与梯度爆炸的原因分析。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/PyTorchOptimizer|PyTorchOptimizer]]：接收 BP 计算出的梯度并更新参数。

### 横向关联
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/计算图|计算图]] ↔ [[02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/反向传播算法|反向传播算法]]：计算图是 BP 的图形化与通用计算表达。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚它解决什么问题。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像……”»）。
- [ ] 3. 写出正式定义（误差信号 $\delta^{(l)}$ 的定义）。
- [ ] 4. 写出核心四个矩阵公式。
- [ ] 5. 解释公式里每个符号的含义与矩阵维度。
- [ ] 6. 讲出推导主线与引入中间变量 $z^{(l)}$ 的关键转念。
- [ ] 7. 手算做出单神经元基础例子。
- [ ] 8. 说出 BP 与 SGD 的区别（误区 1）。
- [ ] 9. 说出它与计算图和梯度消失的关系。
- [ ] 10. 说出 PyTorch 中 `backward()` 的对应原理。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | BP 与优化器的区别 |
| 2 | 公式运用 | 基础 | 简单单神经元梯度手算 |
| 3 | 条件判断 | 中等 | 激活函数导数对 BP 的影响 |
| 4 | 变式/综合 | 中等 | 深度递推下的梯度消失条件 |
| 5 | 开放/建模 | 较难 | 为什么反向求导比正向求导快？ |

### 题目与解析

#### 1. 关于反向传播算法（BP）与梯度下降（SGD）关系的说法，正确的是？
- A. BP 算法包含了参数更新过程
- B. BP 算法的核心是高效计算偏导数，参数更新由优化器完成
- C. 只要使用了 BP 算法，网络就一定会收敛到全局最优
- D. BP 算法计算梯度的时间复杂度随着网络层数呈指数增长

> [!question]- 答案解析
> - **答案**：B
> - **解析**：BP 只负责利用链式法则高效计算梯度，参数更新由 SGD/Adam 等优化器执行。BP 复杂度为线性 $O(|E|)$。
> - **易错原因**：混淆了“求导”与“更新”。
> - **对应误区**：误区 1。
> - **Obsidian 标签建议**：`#自测题/概念`

#### 2. 在 Sigmoid 激活函数 $\sigma(z) = \frac{1}{1+e^{-z}}$ 下，当某层 $z=10$ 时，该层反向传递的误差信号 $\delta$ 会发生什么？
- A. 放大
- B. 保持不变
- C. 严重衰减为接近 0
- D. 变为负数

> [!question]- 答案解析
> - **答案**：C
> - **解析**：Sigmoid 导数为 $\sigma'(z) = \sigma(z)(1-\sigma(z))$。当 $z=10$ 时，$\sigma(10) \approx 1$，导数 $\sigma'(10) \approx 1 \times 0 = 0$。根据递推公式 $\boldsymbol{\delta}^{(l)} = \dots \odot \sigma'(\mathbf{z}^{(l)})$，乘上接近 0 的数会导致误差信号严重衰减（饱和区梯度消失）。

#### 3. 为什么在深度神经网络中，逆向计算梯度（反向传播）比正向计算梯度（前向模式自动求导）效率高得多？
> [!question]- 答案解析
> - **答案**：因为深度神经网络通常是“高维输入（百万参数）、标量输出（单 Loss）”。
> - **解析**：对于标量函数 $J: \mathbb{R}^N \to \mathbb{R}$，前向模式自动求导每次只能求出损失对 1 个输入的偏导，求出全部 $N$ 个参数的梯度需要运行 $N$ 次；而反向模式（BP）从标量 Loss 倒推，只需要运行 **1 次**反向传播就能同时得到全部 $N$ 个参数的梯度。

#### 4. 在反向传播中，已知上一层误差向量 $\boldsymbol{\delta}^{(l+1)} \in \mathbb{R}^{4 \times 1}$，权重矩阵 $\mathbf{W}^{(l+1)} \in \mathbb{R}^{4 \times 3}$，求传给当前层的误差向量维度。
> [!question]- 答案解析
> - **答案**：$\mathbb{R}^{3 \times 1}$。
> - **解析**：根据递推公式 $(\mathbf{W}^{(l+1)})^T \boldsymbol{\delta}^{(l+1)}$，转置矩阵维度为 $3 \times 4$，乘以 $4 \times 1$ 的向量，结果维度为 $3 \times 1$，精确对应当前层 3 个神经元的误差信号。

#### 5. 【证明/推导】请推导 Sigmoid 激活函数在 Cross-Entropy 损失函数下，输出层误差 $\delta^{(L)}$ 的精简形式。
> [!question]- 答案解析
> - **答案**：$\boldsymbol{\delta}^{(L)} = \mathbf{a}^{(L)} - \mathbf{y}$。
> - **解析**：二分类交叉熵 $J = - y \ln a - (1-y) \ln (1-a)$，其中 $a = \sigma(z)$。
>   $\frac{\partial J}{\partial a} = -\frac{y}{a} + \frac{1-y}{1-a} = \frac{a - y}{a(1-a)}$。
>   因为 $\sigma'(z) = a(1-a)$，由链式法则 $\delta^{(L)} = \frac{\partial J}{\partial z} = \frac{\partial J}{\partial a} \cdot \frac{\partial a}{\partial z} = \frac{a - y}{a(1-a)} \cdot a(1-a) = a - y$。
>   该抵消特性使 Cross-Entropy 结合 Sigmoid 时不会在输出层产生梯度饱和！

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/`
- **建议双链**：
  - [[02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/🛡️ 第三阶段：正则优化|第三阶段：正则优化]]
  - [[02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/神经网络|神经网络]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/计算图|计算图]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/梯度流问题|梯度流问题]]
- **建议标签**：`#学习` `#深度学习` `#机器学习` `#反向传播` `#BP` `#链式法则` `#自动求导`
- **拆分建议**：属于 A 类核心概念主体卡，无需拆分，已包含直觉、公式、推导、例题与自测。
