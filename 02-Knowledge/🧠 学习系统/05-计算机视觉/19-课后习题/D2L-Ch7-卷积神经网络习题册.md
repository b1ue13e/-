---
type: project
topic: "D2L Ch.7 卷积神经网络课后习题"
created: 2026-08-05
status: active
flow: project
kind: problem-type
source: "D2L Chapter 7: Convolutional Neural Networks"
source_url: "https://d2l.ai/chapter_convolutional-neural-networks/index.html"
license: "CC BY-SA 4.0"
tags: [计算机视觉, 课后习题, D2L, CNN]
---

# D2L Ch.7 卷积神经网络课后习题

> **来源改编**：基于 [Dive into Deep Learning (D2L) Ch.7](https://d2l.ai/chapter_convolutional-neural-networks/index.html)（CC BY-SA 4.0）各节 Exercises 重述、扩展与参数替换。涵盖卷积运算、填充步幅、多通道、池化、LeNet 五大模块。

## 对应知识卡

- [[卷积神经网络CNN]]
- [[LeNet]]
- [[图像滤波]]
- [[线性代数基础CV]]

## 作答协议

每题先写「**作答前信心：__/100**」，完成后写「**作答后信心：__/100**」。手算题写出完整推导过程；代码题保留输入、输出和断言（assert）。错题记录错因并在 24h / 72h / 7d 重测。

---

### 题 1（手算题）：卷积层输出尺寸

输入为 $32 \times 32$ 的灰度图（单通道），分别计算以下三种卷积配置下的输出特征图尺寸（假设 dilation=1）：

| 配置 | 卷积核尺寸 $k$ | 填充 $p$ | 步幅 $s$ |
|:---|:---:|:---:|:---:|
| A | 3 | 1 | 1 |
| B | 5 | 0 | 2 |
| C | 3 | 1 | 2 |

要求：
- 写出通用公式 $H_{\text{out}} = \lfloor \frac{H - k + 2p}{s} \rfloor + 1$
- 逐一计算三种配置下的输出尺寸，并判断是否有像素被"丢弃"

> [!hint]- 提示 1
> 配置 A（$k=3, p=1, s=1$）属于 "same" padding 的常见设置。
> [!hint]- 提示 2
> 配置 B 中 $32-5=27$，除以 2 后向下取整。
> [!hint]- 提示 3
> 配置 C 检查 $(32-3+2)/2 = 15.5$，向下取整为 15，$15 \times 2 + 3 = 33 > 32$，说明最右/最下一列未被任何卷积窗口的右/下边缘覆盖。
> [!success]- 答案锚点
> A: $32\times32$；B: $14\times14$；C: $16\times16$（最右/最下各丢弃 1 像素，因为 $15 \times 2 + 3 = 33 > 32$）。

---

### 题 2（概念题）：池化层的梯度传播

考虑一个 $2 \times 2$ 最大池化（Max Pooling, stride=2）和一个 $2 \times 2$ 平均池化（Average Pooling, stride=2），均在 $4 \times 4$ 输入上操作。

- (a) 画出前向传播时两种池化的输出（给定一个示例输入矩阵，含数值）。
- (b) 设上游梯度（池化输出的梯度）为全 1 矩阵，分别写出两种池化的反向传播梯度分配到输入各位置的规则，并给出梯度矩阵。
- (c) 解释为什么 Max Pooling 的梯度是稀疏的，而 Average Pooling 的梯度是均匀的。

> [!hint]- 提示 1
> Max Pooling 的反向传播：梯度仅传递给每个窗口内最大值所在位置，其余位置梯度为零。
> [!hint]- 提示 2
> Average Pooling 的反向传播：每个窗口的梯度均分给窗口内所有元素（除以 $k^2$）。
> [!hint]- 提示 3
> 可以用 $4\times4$ 的简单矩阵如 $\begin{bmatrix}1&2&3&4\\5&6&7&8\\9&10&11&12\\13&14&15&16\end{bmatrix}$ 手算验证。
> [!success]- 答案锚点
> (a) Max Pooling 输出 $2\times2$ 取每窗最大值；Average Pooling 输出每窗均值。(b) Max Pooling 反传时非最大值位置梯度为 0，仅最大值位置获得上游梯度；Average Pooling 每个元素获得上游梯度的 $1/4$。(c) Max 只选一个位置，梯度只流向该位置（稀疏）；Average 所有位置均等参与，梯度均匀分配。

---

### 题 3（手算题）：卷积 vs 全连接参数量

输入图像尺寸为 $28 \times 28$（单通道，MNIST 灰度图），目标输出为 10 类分类结果。

- (a) 若使用**全连接层**直接将 $28 \times 28 = 784$ 个输入映射到 10 个输出，不计偏置，参数量是多少？
- (b) 若使用**单个卷积层**（$5 \times 5$ 卷积核，输入通道 1，输出通道 6，padding=2, stride=1），不计偏置，参数量是多少？
- (c) 若使用卷积层后接一个全连接层（将特征图拉平后接 10 输出），其中卷积后特征图尺寸为 $28 \times 28 \times 6 = 4704$，全连接层参数量是多少？
- (d) 对比 (a) 和 (b)+(c)，说明卷积如何通过**权值共享**和**局部连接**减少参数量。

> [!hint]- 提示 1
> 全连接层参数量 = 输入维度 $\times$ 输出维度。
> [!hint]- 提示 2
> 卷积核参数量 = $c_{\text{in}} \times c_{\text{out}} \times k_h \times k_w$。
> [!hint]- 提示 3
> 权值共享：同一个卷积核在输入的不同位置复用同一组权重；局部连接：每个输出神经元只与 $k^2$ 大小的局部区域连接。
> [!success]- 答案锚点
> (a) $784 \times 10 = 7{,}840$。(b) $1 \times 6 \times 5 \times 5 = 150$。(c) $4704 \times 10 = 47{,}040$。(d) 卷积核参数量仅 150，全连接需 7,840（即使是 28×28 的小图）。但卷积后的全连接层（47,040）反而是瓶颈——这正是现代 CNN 使用全局平均池化替代拉平+FC 的动机之一。

---

### 题 4（推导题）：多通道卷积的维度变换

给定一个卷积层：输入特征图维度为 $(C_{\text{in}}, H, W) = (3, 32, 32)$，卷积核维度为 $(C_{\text{out}}, C_{\text{in}}, k, k) = (16, 3, 3, 3)$，padding=1，stride=1。

- (a) 计算输出特征图的维度 $(C_{\text{out}}, H_{\text{out}}, W_{\text{out}})$。
- (b) 解释"多输入通道"的卷积如何合并信息：写出对位置 $(i,j)$ 和输出通道 $o$ 的数学表达式。
- (c) 如果只有 1 个输入通道，同样的 $16$ 个输出通道，卷积核维度变为 $(16, 1, 3, 3)$，参数量变化多少？

> [!hint]- 提示 1
> 输出通道数 = 卷积核的 $C_{\text{out}}$，即 16。
> [!hint]- 提示 2
> 多通道卷积：对每个输出通道 $o$，先对 $C_{\text{in}}$ 个通道分别与对应的 $k\times k$ 核做互相关，然后求和。
> [!hint]- 提示 3
> 参数量 = $C_{\text{out}} \times C_{\text{in}} \times k \times k$。
> [!success]- 答案锚点
> (a) $(16, 32, 32)$。(b) $Y_{o,i,j} = \sum_{c=0}^{C_{\text{in}}-1} \sum_{u=0}^{k-1} \sum_{v=0}^{k-1} X_{c, i+u, j+v} \cdot W_{o, c, u, v}$。(c) 参数量从 $16 \times 3 \times 3 \times 3 = 432$ 降至 $16 \times 1 \times 3 \times 3 = 144$。

---

### 题 5（架构分析题）：LeNet-5 逐层推导

LeNet-5 原始架构如下：

| 层 | 类型 | 核/窗口 | 输出尺寸 | 参数量 |
|:---|:---|:---|:---|:---:|
| 输入 | — | — | $1 \times 28 \times 28$ | 0 |
| C1 | Conv (6@5×5) | $k=5, s=1, p=2$ | ? | ? |
| S2 | AvgPool (2×2) | $k=2, s=2$ | ? | 0 |
| C3 | Conv (16@5×5) | $k=5, s=1, p=0$ | ? | ? |
| S4 | AvgPool (2×2) | $k=2, s=2$ | ? | 0 |
| C5 | Conv (120@5×5) | $k=5, s=1, p=0$ | ? | ? |
| F6 | FC | — | 84 | ? |
| 输出 | FC | — | 10 | ? |

- (a) 填写表中所有 `?` 的输出尺寸（padding 和 stride 均按表中所给）。
- (b) 计算每个可学习层的参数量（含偏置，偏置数 = 输出通道数/输出维度）。
- (c) 为什么在 C3 层使用 16 个输出通道而非全部连接（LeNet 中 C3 与 S2 的连接是部分连接表）？现代实现通常怎么做？

> [!hint]- 提示 1
> C1 输出：$28 - 5 + 2\times 2 + 1 = 28$，即 $6 \times 28 \times 28$。
> [!hint]- 提示 2
> S2 输出：$28 / 2 = 14$（stride=2, 无重叠）。
> [!hint]- 提示 3
> C5 的输入是 $16 \times 5 \times 5$，$5\times5$ 卷积后变为 $1\times1$，等价于全连接。
> [!hint]- 提示 4
> 参数量含偏置：Conv 层为 $C_{\text{out}} \times C_{\text{in}} \times k^2 + C_{\text{out}}$；FC 层为 $\text{in} \times \text{out} + \text{out}$。
> [!success]- 答案锚点
> (a) C1: $6\times28\times28$; S2: $6\times14\times14$; C3: $16\times10\times10$; S4: $16\times5\times5$; C5: $120\times1\times1$。(b) C1: $6\times1\times25+6=156$; C3: $16\times6\times25+16=2{,}416$（全连接）; C5: $120\times16\times25+120=48{,}120$; F6: $120\times84+84=10{,}164$; 输出: $84\times10+10=850$。(c) 原始 LeNet 为节省计算/参数使用部分连接表；现代实现直接全部连接。

---

### 题 6（性质题）：卷积的平移等变性

- (a) 定义卷积的**平移等变性**（Translation Equivariance）：输入平移 $\Delta$ 像素，输出如何变化？
- (b) 给出一个 $3 \times 3$ 卷积核在一维信号上的简单算例（如输入 `[0,0,1,0,0]` vs `[0,1,0,0,0]`，核为 `[1,2,3]`），验证平移等变性。
- (c) 池化层（Max / Average Pooling）是否也具有平移等变性？为什么？
- (d) 举出一个**不具备**平移等变性的操作，并解释原因。

> [!hint]- 提示 1
> 平移等变性：$f(T_v(x)) = T_v(f(x))$，先平移再卷积 = 先卷积再平移。
> [!hint]- 提示 2
> 一维卷积输出 = 互相关结果。手动计算两个信号的卷积输出，看是否相互平移。
> [!hint]- 提示 3
> 池化操作本质上是局部统计量，平移等变性取决于 stride 与窗口的比率；当 stride=1 且 padding 恰当时成立，stride>1 时可能因边界效应而破坏。
> [!hint]- 提示 4
> 全连接层不具备平移等变性——它把每个空间位置视为独立的输入特征。
> [!success]- 答案锚点
> (a) 输入平移 $\Delta$ → 输出也平移 $\Delta$。公式：$\text{Conv}(T_{\Delta}X) = T_{\Delta}\text{Conv}(X)$。(b) `[0,0,1,0,0]` 的输出为 `[0,1,2,3,0]`；`[0,1,0,0,0]` 的输出为 `[1,2,3,0,0]`，恰好平移 1 位。(c) 当 stride=1 时 Max/Average Pooling 也是平移等变的；stride>1 且不是除尽关系时可能被边界破坏。(d) 全连接层：将空间位置展平为独立特征，位置关系丢失，平移输入会产生完全不同的激活。

---

### 题 7（推理题）：1×1 卷积的作用

- (a) 数学上，$1 \times 1$ 卷积等价于什么操作？写出其数学表达式。
- (b) 假设输入为 $(C_{\text{in}}, H, W) = (64, 32, 32)$，使用 $1 \times 1$ 卷积将通道数降为 32，参数量和计算量（FLOPs，仅乘加）分别是多少？
- (c) 在 NiN（Network in Network）和 ResNet bottleneck 中，$1 \times 1$ 卷积分别起到什么作用？各举一个具体例子。
- (d) $1 \times 1$ 卷积能否改变特征图的空间尺寸？为什么？

> [!hint]- 提示 1
> $1\times1$ 卷积等价于对每个空间位置的通道向量做一次全连接（线性变换）。
> [!hint]- 提示 2
> 参数量 = $C_{\text{in}} \times C_{\text{out}} \times 1 \times 1 = 64 \times 32 = 2{,}048$（不含偏置时）；FLOPs ≈ $2 \times H \times W \times C_{\text{in}} \times C_{\text{out}}$（乘+加）。
> [!hint]- 提示 3
> NiN 用 $1\times1$ 卷积替代全连接层做逐像素的分类；ResNet bottleneck 用 $1\times1$ 降维再升维以节省大卷积核的计算量。
> [!hint]- 提示 4
> $k=1$ 意味着每个输出位置仅依赖于输入的同位置像素，因此不改变空间尺寸（假设 padding=0, stride=1）。
> [!success]- 答案锚点
> (a) $Y_{o,i,j} = \sum_{c} W_{o,c} \cdot X_{c,i,j}$，等价于每个空间位置的逐通道全连接。(b) 参数量 $64 \times 32 = 2{,}048$（无偏置）；FLOPs ≈ $2 \times 32^2 \times 64 \times 32 \approx 4.19 \times 10^6$。(c) NiN：在卷积特征图后接 $1\times1$ 卷积 + 全局平均池化替代 FC；ResNet bottleneck：$1\times1$（降维 256→64）→ $3\times3$（64→64）→ $1\times1$（升维 64→256）。(d) 不能，$k=1$ 时感受野为单像素，无法捕捉空间邻域，输出空间尺寸恒等于输入（s=1, p=0 时）。

---

### 题 8（计算题）：感受野递推

- (a) 定义**感受野**（Receptive Field）：第 $l$ 层特征图上的一个像素能"看到"的原始输入图像区域大小。
- (b) 给定如下网络（均无 padding，stride 均为 1），逐层计算每个特征图像素的感受野大小：

  | 层 | 类型 | 核尺寸 | 步幅 |
  |:---|:---|:---:|:---:|
  | Conv1 | Conv | 3 | 1 |
  | Conv2 | Conv | 3 | 1 |
  | Conv3 | Conv | 3 | 1 |

- (c) 如果将 Conv2 的步幅改为 2（Conv1 和 Conv3 仍为 stride=1），重新计算 Conv3 的感受野。
- (d) 解释感受野公式 $r_n = r_{n-1} + (k_n - 1) \times \prod_{i=1}^{n-1} s_i$ 中累积步幅乘积的含义。

> [!hint]- 提示 1
> 无 stride 时：$r_1 = k_1$，$r_n = r_{n-1} + (k_n - 1)$。
> [!hint]- 提示 2
> 有 stride 时，前面的 stride 会"放大"后面的感受野步进。
> [!hint]- 提示 3
> (c) Conv2 stride=2 意味着 Conv2 输出上相邻两像素在输入上间隔 2 像素；到 Conv3 时该间隔进一步放大。
> [!hint]- 提示 4
> 累积步幅乘积 $\prod s_i$ 代表第 $n-1$ 层输出中相邻像素对应于第 1 层（原始输入）的间隔。
> [!success]- 答案锚点
> (a) 定义见上。(b) Conv1: $r=3$; Conv2: $r=3+(3-1)=5$; Conv3: $r=5+(3-1)=7$。(c) Conv1: $r=3$; Conv2: $r=3+(3-1)\times 1=5$（stride 只影响后续层）；Conv3: $r=5+(3-1)\times (1\times 2)=5+4=9$。(d) $\prod_{i=1}^{n-1} s_i$ 将第 $n$ 层的 kernel 步进映射回原始输入的像素间隔：第 $n$ 层卷积核每移动 1 个位置，在第 $n-1$ 层跨越 $s_{n-1}$ 像素，在原始输入跨越 $\prod s_i$ 像素。

---

## 错因与重测

| 题号 | 错因 | 作答前信心 | 补救页 | 24h | 72h | 7d | 作答后信心 |
|:---|:---|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 2 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 3 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 4 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 5 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 6 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 7 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 8 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |

---

## 外部原题索引

| D2L 节 | 原 Exercises 链接 | 改编题号 |
|:---|:---|:---:|
| 7.1 From Fully Connected Layers to Convolutions | [why-conv.html#exercises](https://d2l.ai/chapter_convolutional-neural-networks/why-conv.html#exercises) | 题3, 题6 |
| 7.2 Convolutions for Images | [conv-layer.html#exercises](https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html#exercises) | 题1, 题8 |
| 7.3 Padding and Stride | [padding-and-strides.html#exercises](https://d2l.ai/chapter_convolutional-neural-networks/padding-and-strides.html#exercises) | 题1 |
| 7.4 Multiple Input and Output Channels | [channels.html#exercises](https://d2l.ai/chapter_convolutional-neural-networks/channels.html#exercises) | 题4, 题7 |
| 7.5 Pooling | [pooling.html#exercises](https://d2l.ai/chapter_convolutional-neural-networks/pooling.html#exercises) | 题2 |
| 7.6 LeNet | [lenet.html#exercises](https://d2l.ai/chapter_convolutional-neural-networks/lenet.html#exercises) | 题5 |
