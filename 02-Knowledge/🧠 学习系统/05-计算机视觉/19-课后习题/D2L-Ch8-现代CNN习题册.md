---
type: project
topic: "D2L Ch.8 现代CNN课后习题"
created: 2026-08-05
status: active
flow: project
kind: problem-type
source: "D2L Chapter 8: Modern Convolutional Neural Networks"
source_url: "https://d2l.ai/chapter_convolutional-modern/index.html"
license: "CC BY-SA 4.0"
tags: [计算机视觉, 课后习题, D2L, ResNet, AlexNet, VGG, GoogLeNet, DenseNet, BatchNorm]
---

# D2L Ch.8 现代CNN课后习题

> **来源改编**：基于 [Dive into Deep Learning (D2L) Ch.8](https://d2l.ai/chapter_convolutional-modern/index.html)（CC BY-SA 4.0）各节 Exercises 重述、扩展与参数替换。涵盖 AlexNet、VGG、NiN、GoogLeNet、BatchNorm、ResNet、DenseNet 七大模块。

## 对应知识卡

- [[🎯 ResNet (残差网络)]]
- [[卷积神经网络CNN]]
- [[批归一化BatchNorm]]
- [[GoogLeNet与Inception]]
- [[VGG与更深网络]]
- [[DenseNet与特征复用]]

## 作答协议

每题先写「**作答前信心：__/100**」，完成后写「**作答后信心：__/100**」。手算题写出完整推导过程；代码题保留输入、输出和断言（assert）。错题记录错因并在 24h / 72h / 7d 重测。

---

### 题 1（架构分析题）：AlexNet 与 LeNet 的架构差异

AlexNet（2012）常被视为 LeNet 的"放大版"，但它在多个关键设计点上做出了根本性的创新。请回答：

- (a) 列出 AlexNet 与 LeNet-5 在以下维度的具体差异：网络深度（层数）、卷积核尺寸、激活函数、池化方式、正则化手段。
- (b) AlexNet 为何在第一层使用 $11 \times 11$ 大卷积核，而后续层改为 $5 \times 5$ 和 $3 \times 3$？这与 VGG 后来"全部用 $3 \times 3$"的理念有何不同？
- (c) AlexNet 使用双 GPU 训练，通道被分成两组（每组各一半），且 Conv2/Conv4/Conv5 只在同组内连接（如 Conv2 的输入只来自同组 Conv1 的输出）。这种设计与现代分组卷积（Group Convolution）有何异同？为什么后续架构（如 VGG）逐渐放弃了这种分组策略？
- (d) 如果去除 AlexNet 所有的 Dropout 和局部响应归一化（LRN），在 ImageNet 上预期会发生什么？解释其原因。

> [!hint]- 提示 1
> AlexNet 的关键创新点：ReLU 激活函数（解决 Sigmoid 梯度饱和）、Dropout（缓解过拟合）、重叠池化（overlapping pooling，kernel=3, stride=2）、LRN（已被 BatchNorm 取代）。
> [!hint]- 提示 2
> 大卷积核在第一层捕捉大范围低级特征（边缘、纹理），但参数量大；小卷积核堆叠可达到相同感受野且参数更少——这是 VGG 的核心论据。
> [!hint]- 提示 3
> AlexNet 的分组卷积本质上是硬件限制（GTX 580 3GB 显存放不下整个模型），而非设计选择；现代分组卷积（如 ResNeXt）则是为了提高计算效率（FLOPs/参数比）。
> [!hint]- 提示 4
> 去掉 Dropout 会导致严重的过拟合（AlexNet 有 ~60M 参数，ImageNet 仅 1.2M 训练图）；去掉 LRN 对现在的模型影响很小——它已被证明并非关键组件。
> [!success]- 答案锚点
> (a) **深度**：LeNet 仅 2 卷积 + 3 全连接；AlexNet 有 5 卷积（或 5+3=8 层可学习层）。**卷积核**：LeNet 全部 $5\times5$；AlexNet 用 $11\times11$/$5\times5$/$3\times3$ 混合。**激活**：LeNet 用 Sigmoid/Tanh；AlexNet 用 ReLU（训练速度快 6 倍且缓解梯度消失）。**池化**：LeNet 用 $2\times2$ 平均池化；AlexNet 用 $3\times3$ 最大池化（stride=2，重叠）。**正则化**：LeNet 无（早期无需求）；AlexNet 用 Dropout（FC 层 p=0.5）+ 数据增强（裁剪、翻转、颜色扰动）+ LRN。(b) 第一层 $11\times11$ 是为了快速覆盖大感受野（ImageNet 图像 224×224 比 MNIST 大得多）；后续用小卷积核减少参数。VGG 证明 $3\times3$ 堆叠可达到任意感受野且参数更少——两个 $3\times3$ 的感受野等同于一个 $5\times5$，三个 $3\times3$ 等同 $7\times7$。(c) AlexNet 每 GPU 各管一半通道，同组内全连接、跨组隔离——这是"channel-wise 分组卷积"（groups=2），但动机是硬件限制。现代 Group Conv（groups=g）将 $C_{\text{in}}$ 等分成 g 组各自独立卷积再拼接，参数量降为 $1/g$，动机是效率。后者用 $1\times1$ 卷积混合跨组信息，而 AlexNet 仅在 FC 层才混合。(d) 去掉 Dropout 会严重过拟合（训练精度高但测试精度大幅下降）；去掉 LRN 影响很小——现代实验证明 LRN 对最终精度几乎无贡献，BatchNorm 已完全替代它。
> 
> ---
>
> ### 题 2（设计分析题）：VGG 的 $3 \times 3$ 卷积堆叠思想

VGG 网络的核心设计原则是"全部使用 $3 \times 3$ 卷积核，通过堆叠增加深度"。请回答：

- (a) 证明：两个堆叠的 $3 \times 3$ 卷积层（stride=1, padding=1）与单个 $5 \times 5$ 卷积层具有相同的感受野。推广：$n$ 个 $3 \times 3$ 卷积堆叠的感受野是多少？
- (b) 比较参数量：假设输入输出通道数均为 $C$，计算两个 $3 \times 3$ 卷积层与单个 $5 \times 5$ 卷积层的参数量之比。当 $C=64$ 和 $C=512$ 时，分别节省了多少参数？
- (c) VGG 架构中为什么在每次池化（spatial 尺寸减半）后将通道数翻倍？这种设计背后的直觉是什么？
- (d) VGG 的主要缺陷是什么？从参数量、计算量和内存占用的角度分析。

> [!hint]- 提示 1
> 感受野递推公式：$r_n = r_{n-1} + (k_n - 1) \times \prod_{i=1}^{n-1} s_i$。无 stride 时直接 $r_n = r_{n-1} + (k_n - 1)$。
> [!hint]- 提示 2
> 两个 $3\times3$ 卷积：参数 = $2 \times (C \times C \times 3 \times 3) = 18C^2$；单个 $5\times5$：参数 = $C \times C \times 5 \times 5 = 25C^2$。节省了 $7C^2$ 即 28%。
> [!hint]- 提示 3
> 空间尺寸减半 → 丢失了 75% 的空间信息；翻倍通道数 → 增加特征维度以"补偿"信息容量损失，保持每一层的总信息量（≈ 空间 × 通道）大致恒定。
> [!hint]- 提示 4
> VGG-16 有 ~138M 参数，其中约 90% 集中在最后的全连接层（FC-4096→4096→1000）；且特征图在浅层占用大量显存（224×224×64 ≈ 12.5MB per sample）。
> [!success]- 答案锚点
> (a) 第一个 $3\times3$：$r=3$。第二个 $3\times3$：$r = 3 + (3-1) = 5$（与 $5\times5$ 相同）。推广：$n$ 个 $3\times3$ 堆叠的感受野 = $1 + 2n$（$n=1 \to 3$, $n=2 \to 5$, $n=3 \to 7$…）。(b) 比值 = $18C^2 / 25C^2 = 0.72$，即节省 28%。$C=64$：节省 $7\times 64^2 = 28{,}672$；$C=512$：节省 $7\times 512^2 \approx 1.84 \times 10^6$。(c) 直觉：每层的信息量 ≈ 空间尺寸 × 通道数。池化将空间尺寸缩小为 $1/4$，通道翻倍后信息量变为 $(1/4) \times 2 = 1/2$，虽然仍下降但避免了信息瓶颈；若通道不变则信息量直接降为 $1/4$，下一层卷积可提取的信息大幅减少。(d) 主要缺陷：① 参数巨大（VGG-16 ~138M，大部分在 FC 层）；② 计算量大（~15.5 GFLOPs）；③ 显存占用高（大量中间特征图需存储用于反向传播）；④ 训练慢、部署难。
>
> ---
>
> ### 题 3（推理题）：NiN 的全局平均池化替代 FC 层

Network in Network（NiN）提出了两个重要创新：$1 \times 1$ 卷积的 mlpconv 层和全局平均池化（Global Average Pooling, GAP）替代全连接层。请回答：

- (a) 写出 GAP 的数学表达式：给定输入特征图 $X \in \mathbb{R}^{C \times H \times W}$，GAP 输出向量 $\mathbf{y} \in \mathbb{R}^C$ 的每个分量 $y_c$ 如何计算？
- (b) GAP 相比传统的"Flatten + FC"有哪三个主要优势？请从参数量、过拟合风险、空间信息保留三个角度分析。
- (c) 为什么 GAP 之后可以直接接 softmax 做分类，而传统的 Flatten 之后通常需要多个 FC 层？GAP 的"先验"是什么？
- (d) 假设最后一个卷积层输出为 $(C, H, W) = (1024, 7, 7)$，分类数为 1000。比较以下两种方案的参数量（不含偏置）：方案 A：Flatten → FC(1024×7×7, 4096) → FC(4096, 4096) → FC(4096, 1000)；方案 B：GAP → FC(1024, 1000)。并说明 ResNet 等现代架构采用了哪种方案。

> [!hint]- 提示 1
> GAP 对每个通道独立求均值：$y_c = \frac{1}{H \times W} \sum_{i=1}^{H} \sum_{j=1}^{W} X_{c,i,j}$。
> [!hint]- 提示 2
> Flatten + FC 将空间位置视为独立特征，参数量巨大且丢失了"位置无关性"先验；GAP 则强制每个通道只产生一个全局统计量，极大减少了参数。
> [!hint]- 提示 3
> GAP 的隐含假设：卷积特征图每个通道已经编码了某一类高级语义概念（如"猫脸"、"狗耳"），该概念在图中任意位置出现都应贡献相同的分类分数——即平移不变的分类。
> [!hint]- 提示 4
> 方案 A 参数量 ≈ $50176 \times 4096 + 4096 \times 4096 + 4096 \times 1000 \approx 205.5\text{M} + 16.8\text{M} + 4.1\text{M} \approx 226.4\text{M}$；方案 B 参数量 = $1024 \times 1000 \approx 1.02\text{M}$。
> [!success]- 答案锚点
> (a) $y_c = \frac{1}{H \times W} \sum_{i=1}^{H} \sum_{j=1}^{W} X_{c,i,j}$，即对每个通道求空间均值。(b) ① **参数量**：GAP 无参数，直接消除 FC 层的百万级参数（NiN 将参数量从 AlexNet 的 ~60M 降至 ~7.5M）。② **过拟合风险**：无 FC 意味着无需 Dropout 等强正则化，天然正则化。③ **空间信息保留**：GAP 前的卷积特征图保留了空间对应关系（可用于 CAM 等可视化），而 Flatten 直接丢弃了空间结构。(c) GAP 隐含先验是"每个通道对应一个类别置信度图"——卷积层学到的通道已经语义对齐了类别，GAP 只是做"空间投票"取均值。而 Flatten 后的向量没有这种语义对齐，需要 FC 层做复杂的非线性映射来发现跨空间位置的关系。(d) 方案 A 参数量 ≈ 226.4M；方案 B 参数量 ≈ 1.02M（仅为 A 的 0.45%）。ResNet、DenseNet、ResNeXt 等现代架构均采用方案 B（GAP → FC），这正是 NiN 范式被广泛采纳的证明。
>
> ---
>
> ### 题 4（结构分析题）：GoogLeNet 的 Inception 模块多分支设计

GoogLeNet（Inception v1）的 Inception 模块在同一层并行使用 $1 \times 1$、$3 \times 3$、$5 \times 5$ 卷积和一个 $3 \times 3$ 最大池化分支，并将输出沿通道维拼接。

- (a) 画出 Inception 模块的完整结构框图，标注每个分支的卷积核尺寸、stride 和 padding（使用"same" padding 保持空间尺寸不变）。
- (b) 为什么在每个 $3 \times 3$ 和 $5 \times 5$ 卷积前插入一个 $1 \times 1$ 卷积（bottleneck）？假设输入为 $(C_{\text{in}}, H, W) = (256, 28, 28)$，$3 \times 3$ 分支输出 128 通道，$5 \times 5$ 分支输出 32 通道，分别计算有/无 $1 \times 1$ bottleneck（降至原通道的 $1/4$）时的参数量变化。
- (c) Inception 模块的多分支设计体现了什么核心思想？与 VGG 的"单一通路逐层加深"相比有何优劣？
- (d) GoogLeNet 在中间层插入两个辅助分类器（auxiliary classifiers）。解释其目的和训练/推理时的不同处理方式。这种方式解决了什么训练难题？

> [!hint]- 提示 1
> Inception 的核心思想：让网络自己"学习"在每个位置该用多大的卷积核（$1\times1$ for 细节 / $3\times3$ for 中等 / $5\times5$ for 大范围），而非人工指定。
> [!hint]- 提示 2
> Bottleneck $1\times1$ 的作用：降维——先压缩通道再做大卷积核卷积，再恢复到目标通道数（或只做前半段降维）。这大幅减少了大卷积核的计算量。
> [!hint]- 提示 3
> 对于 $3\times3$ 分支：无 bottleneck = $256 \times 128 \times 3^2 = 294{,}912$；有 bottleneck（$256 \to 64 \to 128$）= $256 \times 64 + 64 \times 128 \times 9 = 16{,}384 + 73{,}728 = 90{,}112$，节省约 69%。
> [!hint]- 提示 4
> 辅助分类器解决深层网络的梯度消失问题——在中间层注入监督信号，"迫使"前面的层学习有判别力的特征；训练时加权（通常权重 0.3）参与总 loss，推理时丢弃。
> [!success]- 答案锚点
> (a) 四个并行分支：① $1\times1$ 卷积（直接）。② $1\times1$ → $3\times3$ 卷积（same padding）。③ $1\times1$ → $5\times5$ 卷积（same padding）。④ $3\times3$ 最大池化（same padding）→ $1\times1$ 卷积。四个分支输出沿 channel 维拼接。(b) **$3\times3$ 分支**：无 bottleneck $= 256 \times 128 \times 9 = 294{,}912$；有 bottleneck（$256 \xrightarrow{1\times1} 64 \xrightarrow{3\times3} 128$）$= 256 \times 64 + 64 \times 128 \times 9 = 90{,}112$，节省 69.4%。**$5\times5$ 分支**：无 bottleneck $= 256 \times 32 \times 25 = 204{,}800$；有 bottleneck（$256 \xrightarrow{1\times1} 64 \xrightarrow{5\times5} 32$）$= 256 \times 64 + 64 \times 32 \times 25 = 67{,}584$，节省 67.0%。(c) 核心思想：**多尺度并行处理**——让网络在每个位置同时用不同大小的感受野提取特征，增加"宽度"而非单纯加深。VGG 是"窄而深"的单一通路，设计简单但参数集中在末端 FC；Inception 是"宽而深"的多通路，设计复杂但参数效率更高（GoogLeNet ~6.8M vs VGG-16 ~138M）。(d) 目的：① 缓解深层网络的梯度消失——中间注入监督信号提供额外的梯度路径；② 起到正则化作用。训练时：辅助分类器的 loss 乘以权重（0.3）加入总 loss 共同反向传播。推理时：辅助分类器完全丢弃，只用最终分类器。解决了 22 层深度的梯度衰减问题，在当时没有 BatchNorm 和 ResNet 的背景下是有效的训练技巧。
>
> ---
>
> ### 题 5（推导题）：ResNet 残差连接与梯度流分析

ResNet 的核心创新是残差连接（skip connection）。对于一个残差块 $\mathbf{y} = \mathcal{F}(\mathbf{x}, \{W_i\}) + \mathbf{x}$：

- (a) 写出残差块的反向传播梯度表达式：设上游梯度为 $\frac{\partial L}{\partial \mathbf{y}}$，推导 $\frac{\partial L}{\partial \mathbf{x}}$ 的表达式，并指出它由哪两项相加组成。
- (b) 解释为何残差连接可以"天然地"缓解梯度消失：即使 $\mathcal{F}$ 的权重任意小，梯度仍然可以通过恒等映射路径回传。与普通网络的梯度链式乘法做对比。
- (c) 假设残差函数 $\mathcal{F}$ 由两层 $3 \times 3$ 卷积（带 BN 和 ReLU）组成，$\mathbf{x}$ 和 $\mathcal{F}(\mathbf{x})$ 维度相同（使用恒等 shortcut）。如果 $\mathbf{x}$ 的维度与 $\mathcal{F}(\mathbf{x})$ 不同（如通道数从 64 变为 128，空间尺寸减半），ResNet 如何处理 shortcut？至少给出两种方案。
- (d) 从优化的角度，解释"残差学习"（learning residual）相比"直接学习"（learning direct mapping）的优势。为什么让网络学习 $\mathcal{F}(\mathbf{x}) \approx 0$ 比学习 $\mathcal{H}(\mathbf{x})$ 更容易优化？

> [!hint]- 提示 1
> 链式法则：$\frac{\partial L}{\partial \mathbf{x}} = \frac{\partial L}{\partial \mathbf{y}} \cdot \frac{\partial \mathbf{y}}{\partial \mathbf{x}} = \frac{\partial L}{\partial \mathbf{y}} \cdot \left( \frac{\partial \mathcal{F}}{\partial \mathbf{x}} + \mathbf{I} \right) = \frac{\partial L}{\partial \mathbf{y}} \cdot \frac{\partial \mathcal{F}}{\partial \mathbf{x}} + \frac{\partial L}{\partial \mathbf{y}}$。
> [!hint]- 提示 2
> 普通网络：$\mathbf{x}_L = f_L \circ \cdots \circ f_1(\mathbf{x}_0)$，梯度 = $\prod_{i} f_i'$，每项 $<1$ 时乘积指数衰减 → 梯度消失。ResNet：$\mathbf{x}_{l+1} = \mathbf{x}_l + \mathcal{F}_l(\mathbf{x}_l)$，梯度展开后始终含 $+\frac{\partial L}{\partial \mathbf{x}_L}$ 项，即使 $\mathcal{F}_l'$ 任意小也不会完全"消失"。
> [!hint]- 提示 3
> 维度不匹配时的 shortcut 方案：① **零填充**（zero-padding）——对新增通道填 0，空间尺寸变化用 stride=2；② **$1\times1$ 卷积投影**（projection shortcut）——用 $1\times1$ 卷积匹配维度和空间尺寸（stride=2）。
> [!hint]- 提示 4
> 如果最优映射接近恒等映射（深层网络中，恒等映射是合理的默认假设），学习 $\mathcal{F}(\mathbf{x}) = \mathcal{H}(\mathbf{x}) - \mathbf{x} \approx 0$ 比直接学习 $\mathcal{H}(\mathbf{x})$ 更容易——因为网络只需将残差分支的权重推向 0（训练初期 BN 后的输出本身接近零均值），恒等映射提供了"不退化"的保证。
> [!success]- 答案锚点
> (a) $\frac{\partial L}{\partial \mathbf{x}} = \frac{\partial L}{\partial \mathbf{y}} \cdot \frac{\partial \mathbf{y}}{\partial \mathbf{x}} = \frac{\partial L}{\partial \mathbf{y}} \cdot \left( \mathbf{I} + \frac{\partial \mathcal{F}(\mathbf{x})}{\partial \mathbf{x}} \right) = \frac{\partial L}{\partial \mathbf{y}} + \frac{\partial L}{\partial \mathbf{y}} \cdot \frac{\partial \mathcal{F}(\mathbf{x})}{\partial \mathbf{x}}$。两项相加：第一项 $\frac{\partial L}{\partial \mathbf{y}}$ 直接将上游梯度"无损"地传回 $\mathbf{x}$（恒等路径），第二项经过残差分支的变换。(b) 普通网络的反向传播是纯乘性的：$\frac{\partial L}{\partial \mathbf{x}_1} = \frac{\partial L}{\partial \mathbf{x}_L} \prod_{l=2}^{L} \frac{\partial \mathbf{x}_l}{\partial \mathbf{x}_{l-1}}$，当每层梯度 $<1$ 时指数衰减。ResNet 中每层梯度 = 恒等项 + 残差项的梯度之和：$\frac{\partial L}{\partial \mathbf{x}_l} = \frac{\partial L}{\partial \mathbf{x}_L} \left( \mathbf{I} + \sum_{i=l}^{L-1} \prod_{j=i}^{L-1} \frac{\partial \mathcal{F}_j}{\partial \mathbf{x}_j} \right)$，展开后始终包含不衰减的"直达项" $\frac{\partial L}{\partial \mathbf{x}_L}$。因此即使残差分支的梯度很小，$\frac{\partial L}{\partial \mathbf{x}_l}$ 也至少 ≈ $\frac{\partial L}{\partial \mathbf{x}_L}$，不会趋零。(c) 方案一：**恒等 shortcut + 零填充**——保持恒等映射，对新增的通道维度补零，空间降采样通过 shortcut 分支上的 stride=2 和 $1\times1$ 平均池化或直接对 $\mathbf{x}$ 做 stride=2 下采样。方案二：**投影 shortcut**（$1\times1$ 卷积）——用 stride=2 的 $1\times1$ 卷积同时匹配通道数和空间尺寸。(d) 残差学习将目标函数分解为 $\mathcal{H}(\mathbf{x}) = \mathbf{x} + \mathcal{F}(\mathbf{x})$。若深层的最优映射接近恒等（即继续加深不应伤害性能），那么 $\mathcal{F}$ 只需趋近于零。网络通过权重衰减和 BN 自然倾向将 $\mathcal{F}$ 推向小值——这比学习任意的 $\mathcal{H}$ 更简单。反之，普通网络必须精确学习恒等映射 $\mathcal{H}(\mathbf{x}) = \mathbf{x}$，这在非线性层堆叠中是极其困难的。实验证明：深层普通网络甚至无法拟合恒等映射（训练误差反升），而 ResNet 通过"默认恒等 + 残差修正"优雅地解决了退化问题。
>
> ---
>
> ### 题 6（概念+计算题）：DenseNet 的稠密连接与特征复用

DenseNet 中，第 $l$ 层的输入是所有前面层的特征图的拼接：$\mathbf{x}_l = H_l([\mathbf{x}_0, \mathbf{x}_1, \dots, \mathbf{x}_{l-1}])$。

- (a) 设初始输入通道数为 $k_0=64$，每层的增长率（growth rate）为 $k=32$（即每层 $H_l$ 输出 $k$ 个新特征图）。写出第 $l$ 层输入的总通道数 $C_l^{\text{in}}$ 的公式，并计算 $l=1, 2, 3, 4, 12$ 时的值。
- (b) DenseNet 为什么能用很小的增长率（如 $k=12$ 或 $k=32$）就能达到很好的性能？解释"特征复用"（feature reuse）的含义。
- (c) DenseNet 的稠密连接与 ResNet 的残差连接在数学形式上有什么关键区别？（写公式对比）。哪种连接方式更有利于特征复用？哪种更有利于梯度流动？
- (d) 假设一个 DenseNet block 有 $L=6$ 层，$k_0=64$，$k=32$。不包含 transition layer 的情况下，该 block 的总参数量相比一个同样深度、每层固定 128 输出通道的 ResNet block，谁更大？说明原因。（两网络均使用 $3\times3$ 卷积，每层 $H_l$ 的 bottleneck 为 BN-ReLU-$1\times1$ 卷积（输出 $4k$ 通道）→ BN-ReLU-$3\times3$ 卷积（输出 $k$ 通道））

> [!hint]- 提示 1
> 通道数公式：$C_l^{\text{in}} = k_0 + (l-1) \times k$。呈线性增长，而非指数增长——因为拼接的只是"增量"而非递归复合。
> [!hint]- 提示 2
> 特征复用：DenseNet 中每层直接"看到"所有浅层特征，浅层的低级特征（边缘、纹理）可以直接被深层利用，不需要通过很多中间层传递。这类似于"集体知识"——每层都在前面所有层的"知识库"上构建。
> [!hint]- 提示 3
> ResNet: $\mathbf{x}_l = H_l(\mathbf{x}_{l-1}) + \mathbf{x}_{l-1}$（加法，假设维度匹配）。DenseNet: $\mathbf{x}_l = H_l([\mathbf{x}_0, ..., \mathbf{x}_{l-1}])$（拼接）。加法和拼接在信息传递上有本质区别：加法是"修正"，拼接是"累积"。
> [!hint]- 提示 4
> DenseNet 的 bottleneck 设计：$1\times1$ 卷积先降维到 $4k$ 通道（控制计算量），再 $3\times3$ 卷积输出 $k$ 通道。即使如此，随 $l$ 增长，$C_l^{\text{in}}$ 线性增大，$1\times1$ 卷积的参数量也随之增长。
> [!success]- 答案锚点
> (a) $C_l^{\text{in}} = k_0 + (l-1) \times k$。$l=1$: $64$；$l=2$: $96$；$l=3$: $128$；$l=4$: $160$；$l=12$: $64 + 11\times 32 = 416$。呈线性增长。(b) 因为每层不需要像传统 CNN 那样输出大量"冗余"特征来保留信息——它可以直接访问前面所有层的特征。增长率 $k$ 仅仅代表"每层新增多少新知识"，已有的特征通过拼接自动复用。这就是"特征复用"：浅层提取的基础特征（如边缘）无需在深层被重新学习，深层只需"增量"地学习对当前任务有用的补充特征。(c) ResNet: $\mathbf{x}_l = H_l(\mathbf{x}_{l-1}) + \mathbf{x}_{l-1}$，通过**加法**实现残差修正，梯度有恒等通道；DenseNet: $\mathbf{x}_l = H_l([\mathbf{x}_0, ..., \mathbf{x}_{l-1}])$，通过**通道拼接**实现特征累积。ResNet 的加法更适合梯度流动（恒等路径直达），DenseNet 的拼接更适合特征复用（所有层直接访问所有浅层特征）。DenseNet 在参数效率（用小增长率达到高性能）上更优，ResNet 在极深网络（>100层）的梯度稳定性上更优。(d) DenseNet 参数量更大。虽然 DenseNet 单层输出通道少（$k$=32 vs ResNet's 128），但**输入通道数随层数线性增长**导致 bottleneck $1\times1$ 卷积的参数量快速增长。以第6层为例：DenseNet 第6层输入 $64+5\times32=224$ 通道，$1\times1$ 卷积参数 = $224 \times 128 = 28{,}672$；ResNet 每层输入始终为 128 通道，$3\times3$ 卷积参数 = $128 \times 128 \times 9 = 147{,}456$。然而 DenseNet 每层有两个卷积（$1\times1 + 3\times3$），且输入通道递增，综合计算：DenseNet block 总参数 ≈ $\sum_{l=1}^{6} [ (k_0+(l-1)k) \times 4k + 4k \times k \times 9 ]$ ≈ $\sum_{l=1}^{6} [C_{l}^{\text{in}} \times 128 + 128 \times 32 \times 9]$，逐步计算后 DenseNet block 总计约 0.59M 参数；同等 ResNet block（6层，每层 $128\to128$ 两个 $3\times3$）约 $6 \times 2 \times 128^2 \times 9 = 1.77$M。注意：这个结论取决于具体配置，DenseNet 的参数量实际通常更小（因为 $k$ 小且用了 bottleneck），但在某些配置下由于输入通道的线性增长，后期层的参数量确实可能超过对应 ResNet 层。关键辩证：DenseNet 的**总参数效率**优于 ResNet（在相同精度下参数更少），但单层输入通道的线性增长是其主要内存瓶颈。
>
> ---
>
> ### 题 7（计算对比题）：ResNet-50 与 DenseNet-121 参数量与计算量对比

下表给出了 ResNet-50 和 DenseNet-121 的架构概要：

| 阶段 | 输出尺寸 | ResNet-50 | DenseNet-121 |
|:---|:---:|:---|:---|
| conv1 | 112×112 | $7\times7$, 64, stride 2 | $7\times7$, 64, stride 2 |
| pool1 | 56×56 | $3\times3$ max pool, stride 2 | $3\times3$ max pool, stride 2 |
| stage2 | 56×56 | $\begin{bmatrix}1\times1, 64 \\ 3\times3, 64 \\ 1\times1, 256\end{bmatrix} \times 3$ | $\begin{bmatrix}1\times1, 128 \\ 3\times3, 32\end{bmatrix} \times 6$ |
| stage3 | 28×28 | $\begin{bmatrix}1\times1, 128 \\ 3\times3, 128 \\ 1\times1, 512\end{bmatrix} \times 4$ | $\begin{bmatrix}1\times1, 128 \\ 3\times3, 32\end{bmatrix} \times 12$ |
| stage4 | 14×14 | $\begin{bmatrix}1\times1, 256 \\ 3\times3, 256 \\ 1\times1, 1024\end{bmatrix} \times 6$ | $\begin{bmatrix}1\times1, 128 \\ 3\times3, 32\end{bmatrix} \times 24$ |
| stage5 | 7×7 | $\begin{bmatrix}1\times1, 512 \\ 3\times3, 512 \\ 1\times1, 2048\end{bmatrix} \times 3$ | $\begin{bmatrix}1\times1, 128 \\ 3\times3, 32\end{bmatrix} \times 16$ |
| 分类 | 1×1 | GAP + FC 1000 | GAP + FC 1000 |

- (a) 解释 ResNet bottleneck 结构 $[1\times1 \to 3\times3 \to 1\times1]$ 中三个卷积各自的作用。为什么先降维再升维？
- (b) 计算 ResNet-50 stage2 中一个 bottleneck block 的参数量（含 BN，BN 的 $\gamma$ 和 $\beta$ 各等于对应通道数）。DenseNet-121 stag2 中一个 dense layer 的输入通道数按 $C_{l}^{\text{in}} = 64 + (l-1) \times 32$ 计算，增长率 $k=32$，bottleneck 为 $1\times1$ 输出 $4k=128$ → $3\times3$ 输出 $k=32$。计算 $l=1$ 和 $l=6$ 的参数量。
- (c) ResNet-50 总参数量约 25.6M，DenseNet-121 约 8.0M。为什么 DenseNet 参数更少但在训练时 GPU 显存占用却通常更高？从特征图存储的角度分析。
- (d) 如果要将 DenseNet 的增长率从 $k=32$ 提高到 $k=64$，参数量的增长趋势是怎么样的？提示：分析 $C_l^{\text{in}}$ 和 $1\times1$ bottleneck 的参数量变化。

> [!hint]- 提示 1
> ResNet bottleneck 三阶段：$1\times1$ 降维（压缩通道，减小 $3\times3$ 卷积计算量）→ $3\times3$ 空间特征提取 → $1\times1$ 升维（恢复通道数，匹配 shortcut）。
> [!hint]- 提示 2
> ResNet-50 stage2 bottleneck 参数：conv1 ($1\times1$, 256→64) = $256 \times 64$；conv2 ($3\times3$, 64→64) = $64 \times 64 \times 9$；conv3 ($1\times1$, 64→256) = $64 \times 256$。BN 参数：4 个 BN 层（conv1前1个 + conv1/conv2/conv3 后各1个），每层 $2 \times$ 通道数。
> [!hint]- 提示 3
> 显存占用的主要贡献：① 模型参数（DenseNet 更少 ✓）；② 中间特征图（反向传播需全部保留）——DenseNet 因为稠密拼接，每层输入通道数线性增大，产生的中间特征图数量远超 ResNet；③ 优化器状态（Adam 的 momentum/variance，参数量的 2-3 倍）。
> [!hint]- 提示 4
> $k$ 翻倍后，$C_l^{\text{in}}$ 的线性增长斜率翻倍，且 $1\times1$ bottleneck 输出通道翻倍（$4k \to 8k$），导致 bottleneck 参数量 ≈ $C_l^{\text{in}} \times 4k$ 中的两个因子同时增大。
> [!success]- 答案锚点
> (a) **第一个 $1\times1$**：降维，将通道数压缩为原来的 $1/4$（如 256→64），大幅减小后续 $3\times3$ 卷积的计算量。**$3\times3$**：在压缩后的低维空间做空间特征提取（核心计算，但通道数已大幅缩小）。**第二个 $1\times1$**：升维恢复原始通道数，使 shortcut（恒等）可以直接相加。整体效果：与直接做两个 $3\times3$ 卷积相比，FLOPs 降低约 $(1/4 + 1/16) \approx 31\%$。(b) **ResNet-50 stage2 bottleneck**：conv1($1\times1$, 256→64) = $256 \times 64 = 16{,}384$；conv2($3\times3$, 64→64) = $64 \times 64 \times 9 = 36{,}864$；conv3($1\times1$, 64→256) = $64 \times 256 = 16{,}384$。BN 参数：4 个 BN × 2($\gamma$+$\beta$) × 各自通道数 = $2 \times (256 + 64 + 64 + 256) = 1{,}280$。bottleneck 总计 = $70{,}912$。**DenseNet stage2**：$l=1$ 时 $C_1^{\text{in}}=64$，bottleneck：$1\times1$(64→128) = $8{,}192$；$3\times3$(128→32) = $128 \times 32 \times 9 = 36{,}864$；BN 参数 = $2\times(64+128+32)=448$；总计 = $45{,}504$。$l=6$ 时 $C_6^{\text{in}}=64+5\times32=224$，bottleneck：$1\times1$(224→128) = $28{,}672$；$3\times3$(128→32) = $36{,}864$；BN 参数 = $2\times(224+128+32)=768$；总计 = $66{,}304$。(c) DenseNet 显存更高的核心原因：**梯度计算需要存储所有中间特征图**。DenseNet 的稠密拼接意味着每层的输入是前面所有层的拼接，这些拼接后的特征图（尺寸 $C_l^{\text{in}} \times H \times W$）必须全部保留在显存中用于反向传播 $H_l$ 的内部梯度。例如 stage3 第 12 层的输入通道数 $= 256 + 11\times 32 = 608$，其 $28\times28\times608$ 特征图 ≈ 1.91MB（fp32），12 层累计 ≈ 15MB（仅 stage3 的特征图输入）。而 ResNet 每层只保留固定的 256/512 通道，特征图总存储显著更少。此外 DenseNet 的拼接操作产生大量中间张量副本。实践中，DenseNet-121 在训练时显存占用约为 ResNet-50 的 1.5-2 倍，尽管参数仅为其 1/3。(d) $k=32 \to 64$ 后，① $C_l^{\text{in}}$ 增长斜率翻倍（每层输入通道增量从 32 → 64）；② bottleneck $1\times1$ 的输出通道从 $4k=128$ 翻倍至 256。瓶颈卷积参数量 $C_l^{\text{in}} \times 4k$ 中两个因子都增大，导致后期层的参数量增长接近 4 倍。整体参数增长约 3-4 倍（略低于 $2\times2=4$，因为浅层 $C_l^{\text{in}}$ 还受初始 $k_0$ 影响）。这也是 DenseNet 实际使用时 $k$ 通常取 12 或 32 的原因。
>
> ---
>
> ### 题 8（架构分析题）：BatchNorm 在 ResNet 中的位置——Pre-activation vs Post-activation

Batch Normalization 在 ResNet 中的放置位置经历了从"post-activation"到"pre-activation"的演变。

- (a) 分别画出"Post-activation ResNet block"和"Pre-activation ResNet block"的结构框图：标注 Conv、BN、ReLU 的顺序，以及 shortcut（skip connection）的起止位置。
- (b) 在 post-activation 设计中，残差块的公式为 $\mathbf{y} = \text{ReLU}(\text{BN}(\text{Conv}(\text{ReLU}(\text{BN}(\text{Conv}(\mathbf{x})))))) + \mathbf{x}$；在 pre-activation 设计中，公式为 $\mathbf{y} = \text{Conv}(\text{ReLU}(\text{BN}(\text{Conv}(\text{ReLU}(\text{BN}(\mathbf{x})))))) + \mathbf{x}$。分析两种设计下，shortcut 路径上的信号经历了哪些变换。哪一种设计的 shortcut 是"纯恒等"（pure identity）路径？
- (c) 解释为什么 pre-activation 设计能进一步提升梯度流动和信息传播（相对于 post-activation）。提示：考虑 shortcut 路径上的 BN 和 ReLU 是否"阻塞"了信号。
- (d) 实验表明 pre-activation ResNet 在 CIFAR-10 上训练 1001 层时明显优于 post-activation。结合 (b)(c) 的分析，解释极深网络中对 shortcut 路径"纯净度"的需求。

> [!hint]- 提示 1
> Post-activation：Conv → BN → ReLU → Conv → BN → **加法** → ReLU（ReLU 在加法之后）。Pre-activation：BN → ReLU → Conv → BN → ReLU → Conv → **加法**（加法后无 ReLU）。
> [!hint]- 提示 2
> Post-activation 中 shortcut 路径为 $\mathbf{x}$ 直接加到最后——看似恒等，但加法后还要经过 ReLU，这会截断负值信号，使 shortcut 并非"完全恒等"。
> [!hint]- 提示 3
> Pre-activation 中 shortcut 路径直接加到最后输出，无任何非线性——真正纯粹的恒等映射。且 BN 和 ReLU 移到卷积权重之前，使卷积总是"看到"归一化后的激活，训练更稳定。
> [!hint]- 提示 4
> 原论文（He et al., "Identity Mappings in Deep Residual Networks", ECCV 2016）证明：当 shortcut 是纯恒等映射且 after-addition 无 ReLU 时，前向/反向信号可以在任意两层之间直接传播，使 1001 层 ResNet 也能收敛。
> [!success]- 答案锚点
> (a) **Post-activation**（原始设计）：输入 → Conv → BN → ReLU → Conv → BN → **与 shortcut $\mathbf{x}$ 相加** → ReLU → 输出。shortcut 起于输入，止于第二个 BN 之后、最后的 ReLU 之前。**Pre-activation**（改进设计）：输入 → BN → ReLU → Conv → BN → ReLU → Conv → **与 shortcut $\mathbf{x}$ 相加** → 输出。shortcut 起于输入，直接止于最终输出（无中间变换）。(b) **Post-activation**：shortcut $\mathbf{x}$ 经加法后共同通过 ReLU——虽看似恒等，但 ReLU 会将负的残差信号截断为 0。当 $\mathcal{F}(\mathbf{x})$ 为负值时，$\mathcal{F}(\mathbf{x})+\mathbf{x}$ 可能 <0 被清零，导致 shortcut 路径也被"污染"。**Pre-activation**：shortcut $\mathbf{x}$ 直接抵达最终输出，不经过任何 BN/ReLU/Conv——真正的"纯恒等"（pure identity）路径。信号从输入到输出有一条完全无阻碍的高速公路。(c) Pre-activation 优势：① shortcut 路径无 BN 和 ReLU 阻塞——前向信号直接传递，反向梯度直接流动；② BN 和 ReLU 移到卷积权重层之前，使卷积层始终接收归一化后的激活（正则化效果更好），且权重层的梯度计算不受 BN 在加法后引入的分布偏移影响。(d) 在极深网络（1001层）中，即使 ResNet 有残差连接，如果 shortcut 路径上有 ReLU（post-activation），每 2 层信号就经过一次 ReLU 截断。虽然梯度可以通过 ReLU（正值时导数为 1），但前向信号会逐渐被"修剪"——负值信号无法通过 shortcut 传递。在 1001 层中这种累积效应导致信息丢失。Pre-activation 使 shortcut 为完全的线性恒等，信号和梯度在任意深度都可无衰减直达，使 1001 层甚至更深的 ResNet 都能以极低的训练误差收敛。
>
> ---

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
| 8.1 Deep Convolutional Neural Networks (AlexNet) | [alexnet.html#exercises](https://d2l.ai/chapter_convolutional-modern/alexnet.html#exercises) | 题1 |
| 8.2 Networks Using Blocks (VGG) | [vgg.html#exercises](https://d2l.ai/chapter_convolutional-modern/vgg.html#exercises) | 题2 |
| 8.3 Network in Network (NiN) | [nin.html#exercises](https://d2l.ai/chapter_convolutional-modern/nin.html#exercises) | 题3 |
| 8.4 Multi-Branch Networks (GoogLeNet) | [googlenet.html#exercises](https://d2l.ai/chapter_convolutional-modern/googlenet.html#exercises) | 题4 |
| 8.5 Batch Normalization | [batch-norm.html#exercises](https://d2l.ai/chapter_convolutional-modern/batch-norm.html#exercises) | 题8 |
| 8.6 Residual Networks (ResNet) | [resnet.html#exercises](https://d2l.ai/chapter_convolutional-modern/resnet.html#exercises) | 题5, 题7, 题8 |
| 8.7 Densely Connected Networks (DenseNet) | [densenet.html#exercises](https://d2l.ai/chapter_convolutional-modern/densenet.html#exercises) | 题6, 题7 |
