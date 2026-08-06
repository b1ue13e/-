---
type: study
course: "05-计算机视觉"
topic: "ResNet (残差网络)"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept:
  - 残差网络
  - ResNet
  - 残差连接
  - 恒等映射
  - 梯度消失
  - 深层网络
prerequisites:
  - VGGNet
  - 梯度流问题
  - BatchNorm
related:
  - DenseNet
  - Transformer注意力
  - MobileNet
flow: knowledge
upstream: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/VGGNet]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/梯度流问题]]"]
stage_moc: "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/🧠 第二阶段：深度学习内核]]"
kind: concept
source: "D2L Ch.8; CS231n A2"
anki_deck: "05-计算机视觉::02-深度学习内核"
anki_tags:
  - 学习
  - 深度学习
  - 计算机视觉
  - ResNet
  - 残差连接
  - 恒等映射
  - 梯度消失
tags:
  - 学习
  - 深度学习
  - 计算机视觉
  - ResNet
  - 残差连接
  - 恒等映射
  - 梯度消失
---

# 🎯 ResNet (残差网络)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：ResNet（Residual Network，残差网络）由 Kaiming He（何恺明）团队于 2015 年提出，斩获 CVPR 2016 最佳论文，是深度学习发展史上最伟大的里程碑之一。它提出的**快捷连接 (Shortcut Connection / Skip Connection)** 和**残差学习 (Residual Learning)** 思想，彻底打破了深层神经网络层数增加导致的“网络退化危机”（Degradation Problem），成功将网络深度从几十层推向上百甚至上千层（ResNet-152 / ResNet-1001）。如今残差连接已成为 Transformer、ConvNeXt、Diffusion Model 等几乎所有 SOTA 模型的必备基础设施。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (我们遇到了什么麻烦)**：
> 在 ResNet 之前，人们普遍相信“网络越深，表达能力越强，准确率应该越高”。然而在实验中人们震惊地发现：当网络从 20 层简单堆叠到 56 层时，**训练集上的 Error 和测试集上的 Error 居然同时变大**（56 层网络的训练错误率反而高于 20 层）！
> 这不是过拟合（过拟合会导致训练集误差极小、测试集误差很大），而是深层网络**根本无法被有效优化**，这种现象被称为**网络退化问题 (Degradation Problem)**。由于链式法则连乘效应，深层梯度的流动受到极严重阻碍，深层模型甚至无法学出与浅层模型相同的恒等变换（Identity Mapping）。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：ResNet 是梯度流设计（Gradient Flow Engineering）的巅峰之作。它证明了：通过改造网络拓扑结构（增加跨层恒等通道），可以让上百层的深层网络像浅层网络一样容易训练。Transformer 中的 Add & Norm 模块也是这一思想在 NLP 领域直接延续。
- **实际应用场景**：ResNet-18/34/50/101/152 是计算机视觉领域最标准的 Backbone 特征抽取器，广泛应用于图像分类、目标检测（Faster R-CNN, YOLO）、语义分割（Mask R-CNN）及迁移学习微调。
- **高频考点/任务**：网络退化现象 vs 过拟合对比、残差块 $H(x) = F(x) + x$ 数学表达式、手推残差块梯度流动 $1 + \frac{\partial F}{\partial x}$ 为什么不会发生梯度消失、BasicBlock vs BottleneckBlock 结构设计、PyTorch 手写 ResNet 模块。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/VGGNet|VGGNet 与卷积神经网络]]**：利用 $3 \times 3$ 卷积层简单顺序堆叠的经典直筒架构。
2. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/梯度流问题|梯度消失与反向传播]]**：深层网络反向传播时，连续乘上小于 1 的权重或导数会导致靠近输入层的梯度迅速衰减至零。

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：残差连接就像在复杂的立交桥下加了一条**直通高速专用车道（Express Lane）**：
  - 原本每辆车（信号/梯度）必须依次挤过几十个拥堵的收费站（卷积层）；收费站多挤几次，信号就全磨损丢掉了（梯度消失）；
  - 现在增加了一条跨越收费站的直通车道（Shortcut $x$）。信号既可以走卷积车道做加工（残差 $F(x)$），也可以直接走直通车道无损飞跃；
  - 哪怕卷积车道啥都没学到（$F(x)=0$），有了保底的直通车道，整个大车道最差也能原封不动传过去（$H(x) = x$，保底不亏）！
- **为什么很自然**：让网络去学习**“拟合目标与输入的差值（残差 $F(x) = H(x) - x$）”**，比直接去拟合未知的复杂全量函数 $H(x)$ 要容易得多！若恒等映射是最优的，把残差权重推向 0 远比把多层卷积学成恒等变换容易。
- **一句话直觉本质**：给信号和梯度建立一条无损直通公路，让网络学会“只学增量，保底不亏”。

---

## 5. 正式定义、核心公式、符号解释

### 1. 核心定义
设残差块的输入为 $\mathbf{x}$，期望拟合的底层映射为 $\mathcal{H}(\mathbf{x})$。残差网络将其拆解为恒等映射与残差映射之和：
$$\mathcal{H}(\mathbf{x}) = \mathcal{F}(\mathbf{x}, \{\mathbf{W}_i\}) + \mathbf{x}$$
其中 $\mathcal{F}(\mathbf{x}, \{\mathbf{W}_i\})$ 为待学习的残差映射（通常包含 2 至 3 层卷积与 ReLU）。

### 2. 梯度流动公式（为何消除梯度消失）
考虑递归展开到第 $L$ 层与第 $l$ 层之间的关系（忽视 BatchNorm）：
$$\mathbf{x}_L = \mathbf{x}_l + \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, \mathbf{W}_i)$$
损失函数 $\mathcal{E}$ 对浅层输入 $\mathbf{x}_l$ 的偏导数为：
$$\frac{\partial \mathcal{E}}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{E}}{\partial \mathbf{x}_L} \frac{\partial \mathbf{x}_L}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{E}}{\partial \mathbf{x}_L} \left( \mathbf{I} + \frac{\partial}{\partial \mathbf{x}_l} \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, \mathbf{W}_i) \right)$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathbf{x}_l$ | 第 $l$ 残差块的输入特征图 | $\mathbb{R}^{C \times H \times W}$ | 上游特征 |
| $\mathcal{F}$ | 残差映射函数 (Residual Mapping) | 与 $\mathbf{x}_l$ 维度相同 | 由卷积+激活构成的分支 |
| $\mathcal{H}$ | 残差块目标输出 | 与 $\mathbf{x}_l$ 维度相同 | $\mathcal{H}(\mathbf{x}) = \mathcal{F}(\mathbf{x}) + \mathbf{x}$ |
| $\mathbf{I}$ | 单位矩阵 (Identity Matrix) | 与特征维度同阶 | **保证梯度流顺畅的关键 $+1$ 项** |
| $\mathbf{W}_s$ | 维度匹配卷积 (1x1 卷积) | $\mathbb{R}^{C_{out} \times C_{in} \times 1 \times 1}$ | 当通道/尺寸改变时使用 |

---

## 6. 推导思路和思想来源

- **最初困难**：直接训练 100 层普通直筒网络（Plain Net）时，由于梯度消失，深层参数无法被更新，训练误差反而上升。
- **关键转念**：假设有一个 20 层的优秀浅层网络，我们强行在后面拼接 30 层“什么都不做的恒等映射层”（$y=x$），这 50 层新网络的性能**绝对不应该比 20 层更差**。然而普通卷积层很难自动学会恒等映射 $y=x$。何恺明转念一想：**与其让卷积硬学 $y=x$，不如把网络改写成 $y = F(x) + x$，让卷积只学 $F(x) = 0$！**
- **数学优雅性推导**：
  在反向传播偏导公式中：
  $$\frac{\partial \mathcal{E}}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{E}}{\partial \mathbf{x}_L} \left( \mathbf{I} + \sum \frac{\partial \mathcal{F}}{\partial \mathbf{x}_l} \right)$$
  括号内包含了常数项 $\mathbf{I}$！这意味着哪怕中间卷积层的偏导数 $\frac{\partial \mathcal{F}}{\partial \mathbf{x}_l}$ 极其微小甚至趋近于 0，整体梯度保留项也不会为 0，深层梯度 $\frac{\partial \mathcal{E}}{\partial \mathbf{x}_L}$ 可以**无损直接传递给最浅层 $\mathbf{x}_l$**！彻底解决了梯度消失。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（BasicBlock vs BottleneckBlock 结构对比）
- **BasicBlock (用于 ResNet-18 / 34)**：
  - 结构：`3x3 Conv` $\to$ `BN` $\to$ `ReLU` $\to$ `3x3 Conv` $\to$ `BN` $+$ `Shortcut` $\to$ `ReLU`。
  - 参数量：由两个 $3 \times 3$ 卷积组成。
- **BottleneckBlock (瓶颈结构，用于 ResNet-50 / 101 / 152)**：
  - 目的：当通道数较大（如 256/1024）时，直接用 $3 \times 3$ 卷积计算量极大。
  - 结构：
    1. $1 \times 1$ 卷积降维（如 $256 \to 64$）；
    2. $3 \times 3$ 卷积抽取空间特征（$64 \to 64$）；
    3. $1 \times 1$ 卷积升维恢复（$64 \to 256$）＋ `Shortcut`。
- **🤔 追问**：为什么瓶颈结构要用 $1 \times 1$ 卷积？
  - *答*：$1 \times 1$ 卷积可以跨通道整合信息并灵活压缩/扩展通道数，大幅降低 $3 \times 3$ 卷积的计算复杂度（FLOPs）。

### 例子 2：中等例子（当尺寸与通道改变时的 1x1 卷积 Shortcut）
当特征图下采样（Stride=2）或通道数扩增（$C_{in} \neq C_{out}$）时，直接按位相加 $\mathcal{F}(\mathbf{x}) + \mathbf{x}$ 维度不匹配。
解决方法：在 Shortcut 分支上增加一个 $1 \times 1$ 卷积做线性投影：
$$\mathbf{y} = \mathcal{F}(\mathbf{x}, \{\mathbf{W}_i\}) + \mathbf{W}_s \mathbf{x}$$
其中 $\mathbf{W}_s$ 采用步长 Stride=2 且卷积核为 $1 \times 1$，精确对齐特征图长宽与通道数。

### 例子 3：实际应用（PyTorch 手写可运行 ResNet BasicBlock）

```python
import torch
import torch.nn as nn

class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super().__init__()
        # 卷积分支
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)

        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        # 维度对齐 Shortcut 分支
        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes)
            )

    def forward(self, x):
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        # 核心：残差相加 F(x) + x
        out += self.shortcut(x)
        out = self.relu(out)
        return out

# 验证代码
x = torch.randn(2, 64, 32, 32)
block = BasicBlock(in_planes=64, planes=128, stride=2)
out = block(x)
print("输入维度:", x.shape)    # [2, 64, 32, 32]
print("输出维度:", out.shape)  # [2, 128, 16, 16] (降采样且通道扩展成功)
```

---

## 8. 常见误区和易混概念

### 误区 1：网络退化现象（Degradation）就是过拟合（Overfitting）
- **错误直觉**：“56 层网络比 20 层效果差，肯定是过拟合了，加点 Dropout 就能好。”
- **为什么错**：过拟合的特征是“训练集准确率极高，测试集准确率很低”；而网络退化现象是**训练集误差和测试集误差同时升高**！这说明网络连训练集都学不动，是优化能力不足，加 Dropout 只会雪上加霜。
- **正确理解**：退化是“学不会”，过拟合是“学太死”。

### 概念对比表

| 概念 | 核心加法/连接结构 | 梯度流动机制 | 典型代表 |
| :--- | :--- | :--- | :--- |
| **ResNet** | 按位加法 (Element-wise Addition): $y = F(x) + x$ | 梯度沿 Shortcut 无损加和流回浅层 | ResNet-50, ConvNeXt |
| **DenseNet** | 通道拼接 (Concatenation): $y = [x, F(x)]$ | 每层与后续所有层建立直接连接，特征复用率极高 | DenseNet-121 |
| **Transformer Block** | 残差加法与归一化: $y = \text{LayerNorm}(x + \text{SelfAttn}(x))$ | 保证注意力机制与 FFN 层在百层 LLM 中稳定训练 | GPT-4, LLaMA |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/VGGNet|VGGNet]]：经典直筒卷积网络的代表，ResNet 解决其深度瓶颈。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/梯度流问题|梯度流问题]]：梯度消失的具体表现，ResNet 求解的目标。

### 下游延伸
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/DenseNet|DenseNet]]：将残差“相加”升级为特征“拼接”的演进架构。
- [[02-Knowledge/🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/08-NLP全栈-Transformer架构|Transformer注意力]]：残差连接在 Transformer 架构中的继承应用。

### 横向关联
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/批归一化BatchNorm|BatchNorm]] ↔ ResNet：BatchNorm 与残差连接共同保障了深层网络的稳定训练。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚 ResNet 解决什么问题（网络退化危机与梯度消失）。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像给梯度建立无损直通高速车道……”»）。
- [ ] 3. 区分网络退化现象与过拟合现象的区别。
- [ ] 4. 写出残差块的数学定义式 $\mathcal{H}(x) = \mathcal{F}(x) + x$。
- [ ] 5. 写出残差网络反向传播梯度流公式，并解释常数项 $\mathbf{I}$ 的数学含义。
- [ ] 6. 对比 BasicBlock 与 BottleneckBlock 的结构与适用网络深度。
- [ ] 7. 解释当 $C_{in} \neq C_{out}$ 时 Shortcut 分支如何用 $1 \times 1$ 卷积处理。
- [ ] 8. 说出为什么残差网络学习 $F(x)=0$ 比硬学恒等变换 $H(x)=x$ 容易得多。
- [ ] 9. 手写包含 Shortcut 和相加的 PyTorch BasicBlock 代码。
- [ ] 10. 说出残差连接思想在现代大语言模型 Transformer 中的应用。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 退化现象与过拟合的区别 |
| 2 | 结构计算 | 基础 | Bottleneck 中 $1 \times 1$ 卷积参数量节省 |
| 3 | 维度推理 | 中等 | Shortcut 维度不匹配时的处理 |
| 4 | 公式推导 | 中等 | 梯度公式中单位阵 $\mathbf{I}$ 对消灭梯度消失的作用 |
| 5 | 开放/迁移 | 较难 | 为什么 Transformer 采用 LayerNorm 结合残差而不是 BatchNorm？ |

### 题目与解析

#### 1. 关于 ResNet 中“网络退化现象”的说法，正确的是？
- A. 随着网络加深，训练集误差变小，但测试集误差变大
- B. 随着网络加深，训练集误差和测试集误差同时增大
- C. 网络退化现象可以通过增加 L2 正则化完全解决
- D. 退化现象只发生在训练样本极少的小数据集上

> [!question]- 答案解析
> - **答案**：B
> - **解析**：退化现象表现为深层网络训练错误率与测试错误率同时高于浅层网络，说明深层直筒网络优化陷入停滞，加正则化无法解决。
> - **对应误区**：误区 1。

#### 2. 在 ResNet-50 的 Bottleneck 模块中，已知输入通道数为 256，结构顺序为：1x1卷积(通道64) $\to$ 3x3卷积(通道64) $\to$ 1x1卷积(通道256)。求这三个卷积的总权重参数量（不含偏置）。
> [!question]- 答案解析
> - **答案**：$256 \times 64 \times 1 \times 1 + 64 \times 64 \times 3 \times 3 + 64 \times 256 \times 1 \times 1 = 16,384 + 36,864 + 16,384 = 69,632$。
> - **解析**：如果不使用 Bottleneck，直接用两个 $3 \times 3$ 卷积处理 256 通道，参数量为 $2 \times (256 \times 256 \times 3 \times 3) = 1,179,648$！Bottleneck 节省了超过 94% 的参数量与计算开销！

#### 3. 为什么在残差块的相加点 `out += shortcut(x)` 之后才执行最后一个 `ReLU` 激活函数？
> [!question]- 答案解析
> - **答案**：为了保持 Shortcut 恒等通路无损无截断。
> - **解析**：如果在相加前对 Shortcut 执行 ReLU，负数特征会被截断为 0，破坏纯粹的恒等变换通道 $\mathbf{x}$；在相加之后执行 ReLU，可以确保 Shortcut 上的信号完全无损传递到加法点。

#### 4. 【推导】证明当残差块中 $\mathcal{F}(\mathbf{x}_i, \mathbf{W}_i) = \mathbf{0}$ 时，任意浅层 $\mathbf{x}_l$ 与深层 $\mathbf{x}_L$ 满足恒等映射。
> [!question]- 答案解析
> - **答案**：由展开公式 $\mathbf{x}_L = \mathbf{x}_l + \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, \mathbf{W}_i)$。
> - **解析**：若所有中间残差项 $\mathcal{F} = \mathbf{0}$，则 $\mathbf{x}_L = \mathbf{x}_l + 0 = \mathbf{x}_l$，即深层特征与浅层特征完全一致，梯度 $\frac{\partial \mathbf{x}_L}{\partial \mathbf{x}_l} = \mathbf{I}$ 100% 无损流动。

#### 5. 【开放/迁移】残差连接也是 Transformer 的核心组成部分，请简述 Transformer 中 Pre-LN 与 Post-LN 在残差梯度流动上的差异。
> [!question]- 答案解析
> - **答案**：Pre-LN 的残差主干路径不经过 LayerNorm 截断，梯度可直接顺畅传递；Post-LN 的残差路径在相加后经过 LayerNorm，会轻微衰减梯度。
> - **解析**：Pre-LN 架构 $x + \text{SubLayer}(\text{LN}(x))$ 保持了主干上真正的无损恒等通道，使得几百层的超大语言模型（如 GPT-3/4）无需复杂的温和预热（Warmup）即可稳定训练；而 Post-LN 需要严格控制初始学习率。

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

- **归档目录**：`02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/`
- **建议双链**：
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/🧠 第二阶段：深度学习内核|第二阶段：深度学习内核]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/VGGNet|VGGNet]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/梯度流问题|梯度流问题]]
  - [[02-Knowledge/🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/08-NLP全栈-Transformer架构|Transformer注意力]]
- **建议标签**：`#学习` `#深度学习` `#计算机视觉` `#ResNet` `#残差网络` `#恒等映射` `#何恺明`

---
---

## 学完后可以完成

- 结合 HW03 理解残差连接；完成卡内自测与复现

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
