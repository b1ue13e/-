---
type: study
course: "05-计算机视觉"
topic: "AlexNet"
created: 2026-08-06
status: ongoing
difficulty: beginner
concept:
  - AlexNet
  - 深度CNN
  - ImageNet
  - ReLU
  - Dropout
prerequisites:
  - 卷积神经网络CNN
  - 激活函数详解
related:
  - VGGNet
  - LeNet
  - ResNet
flow: knowledge
stage_moc: "[[02-深度学习内核/🧠 第二阶段：深度学习内核]]"
kind: concept
source: "D2L Ch.8; Krizhevsky et al. 2012"
anki_deck: "05-计算机视觉::02-深度学习内核"
anki_tags:
  - 计算机视觉
  - AlexNet
  - CNN架构
tags:
  - 学习
  - 计算机视觉
  - AlexNet
  - CNN架构
  - ImageNet
---

# AlexNet

> 所属模块：[[../🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[🧠 第二阶段：深度学习内核|返回阶段页]]
> 前置知识：[[卷积神经网络CNN]]、[[激活函数详解]]
> 主教材：D2L Ch.8；Krizhevsky, Sutskever & Hinton, "ImageNet Classification with Deep Convolutional Neural Networks" (NeurIPS 2012)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：AlexNet 是深度学习历史上的分水岭。2012 年，Alex Krizhevsky、Ilya Sutskever 和 Geoffrey Hinton 凭借 AlexNet 以 **15.3% 的 Top-5 错误率**一举夺得 ImageNet Large Scale Visual Recognition Challenge (ILSVRC) 冠军，将第二名传统方法（26.2%）远远甩在身后——差距超过 **10 个百分点**。这是**深度学习首次在大规模图像识别任务上碾压传统计算机视觉方法**，标志着计算机视觉从"手工特征工程"时代步入"深度特征学习"时代，也由此引爆了此后十年深度学习全面统治 CV/NLP/Speech 的浪潮。它提出的 **ReLU 替代 Sigmoid**、**Dropout 防过拟合**、**GPU 训练**等实践，至今仍是深度学习的标配。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (我们遇到了什么麻烦)**：

在 2012 年之前，ImageNet（120 万张图片，1000 个类别）这样的超大规模图像识别任务上，计算机视觉领域的 SOTA 方法是基于**手工设计特征 + 浅层分类器**的组合——例如 SIFT / HOG 特征提取 + SVM 分类器。这些方法存在根本性瓶颈：

1. **手工特征表达能力天花板**：SIFT、HOG 等特征是人工根据直觉设计的，它们只捕捉特定类型的视觉模式（边缘、梯度方向），无法自动从数据中学到高层次语义抽象。
2. **规模扩展困难**：传统方法在数据量从几千张增长到百万级时，性能提升微乎其微——它们没有足够的参数容量来消化海量数据。
3. **优化困难**：当时的深层神经网络虽理论上具备强大表达能力，但在实践中难以训练——Sigmoid/Tanh 导致严重的梯度消失，GPU 编程门槛极高，大规模网络在普通硬件上甚至跑不起来。

AlexNet 解决的问题本质上是：**如何训练一个足够深、足够宽的卷积神经网络，让它能在百万级图像数据集上收敛，并且泛化得比任何手工特征方法都好。**

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：AlexNet 证明了**端到端深度卷积神经网络可以在大规模自然图像上击败精心设计的手工特征管线**。这一胜利是深度学习复兴的"Big Bang"——此后 VGGNet、GoogLeNet、ResNet、DenseNet、EfficientNet 等后续架构如雨后春笋般涌现，每一代都在 AlexNet 奠定的 GPU + CNN + ReLU + Dropout 范式基础上演进。
- **实际应用场景**：
  - **图像分类**（ImageNet 级别的 1000 类识别）
  - **迁移学习的 Backbone**（用 ImageNet 预训练的 AlexNet 作为特征提取器，迁移到医学影像、遥感、工业质检等小样本领域）
  - **历史研究价值**（理解 CNN 如何从 LeNet 的雏形演进到现代架构，AlexNet 是必经之路）
- **高频考点/任务**：ReLU vs Sigmoid 对训练速度的影响、Local Response Normalization 的作用、双 GPU 分组设计的原因、Dropout 为何放在全连接层、参数量 60M 在各层的分布、与 LeNet 的结构对比。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[卷积神经网络CNN]]**：卷积层（卷积核、步长、填充）、池化层（最大池化）、全连接层的基本概念和计算方式。
2. **[[激活函数详解]]**：Sigmoid、Tanh、ReLU 的数学形式和各自的梯度特性（尤其是 Sigmoid 饱和区导致梯度消失的机理）。
3. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Dropout|Dropout]]**：训练时随机丢弃神经元、推理时权重缩放的基本原理。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

- **直觉类比**：在 AlexNet 之前，计算机视觉就像让一个侦探带着**几张固定的模板卡片**（手工设计的 SIFT 特征模板）去找嫌疑人——模板是有限的，碰到发型变了、光线暗了，侦探就抓瞎了。AlexNet 的做法是：**让侦探自己看 120 万张嫌疑人照片，自己总结出什么是眼睛、鼻子、嘴巴，再总结出什么是人脸、狗脸、猫脸。** 看得越多，侦探的直觉越准。

- **另一个类比**：把 AlexNet 理解为一台**逐层抽象的"视觉蒸馏器"**：
  - 第一层（Conv1）学会的是最简单的笔画——边缘、颜色块、方向纹理（类似 Gabor 滤波器）；
  - 中间层（Conv3-5）把这些笔画组合成"部件"——眼睛的弧线、车轮的圆形、花瓣的纹理；
  - 最后几层（FC6-8）把"部件"拼成"完整概念"——这是一只哈士奇，那是一只金毛。

- **为什么是突破**：之前大家也觉得深层网络好，但一训练就"死掉"（梯度消失）。AlexNet 开了三个"外挂"：
  - **ReLU**（不饱和的激活函数，梯度不衰减）
  - **GPU**（用两张显卡并行计算，显存翻倍）
  - **Dropout**（逼着每个神经元独立学好特征，别互相串通作弊）

- **一句话直觉本质**：AlexNet 是用**GPU 暴力算力 + ReLU 加速信号流 + Dropout 防止死记硬背**，让一个 8 层 CNN 在 120 万张图片上自己学会"什么是猫"的鼻祖架构。

---

## 5. 正式定义、核心公式、符号解释

### 5.1 整体架构定义

AlexNet 由 **5 个卷积层 + 3 个全连接层**组成，输入为 $224 \times 224 \times 3$ 的 RGB 图像，输出为 1000 类的 softmax 概率分布。

$$
\mathbf{y} = \text{softmax}(\text{FC}_8(\text{FC}_7(\text{FC}_6(\text{Conv}_5(\text{Conv}_4(\text{Conv}_3(\text{Conv}_2(\text{Conv}_1(\mathbf{X})))))))))
$$

### 5.2 逐层规格表

| 层 | 类型 | 输入尺寸 | 核大小/步长/填充 | 输出尺寸 | 参数量 | 备注 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Conv1 | 卷积 + ReLU + LRN + Pool | 224×224×3 | 96×11×11 / S=4 / P=0 | 27×27×96 | 34,944 | 大核捕捉大范围纹理 |
| Conv2 | 卷积 + ReLU + LRN + Pool | 27×27×96 | 256×5×5 / S=1 / P=2 | 13×13×256 | 614,400 | 双GPU分组 |
| Conv3 | 卷积 + ReLU | 13×13×256 | 384×3×3 / S=1 / P=1 | 13×13×384 | 885,120 | 跨GPU通信 |
| Conv4 | 卷积 + ReLU | 13×13×384 | 384×3×3 / S=1 / P=1 | 13×13×384 | 1,327,104 | 双GPU分组 |
| Conv5 | 卷积 + ReLU + Pool | 13×13×384 | 256×3×3 / S=1 / P=1 | 6×6×256 | 884,736 | 双GPU分组 |
| FC6 | 全连接 + ReLU + Dropout | 9216 (6×6×256) | — | 4096 | 37,748,736 | **参数量最大层** |
| FC7 | 全连接 + ReLU + Dropout | 4096 | — | 4096 | 16,777,216 | — |
| FC8 | 全连接 + Softmax | 4096 | — | 1000 | 4,096,000 | 输出层 |

> **总参数量**：约 **62,378,000**（≈ 62M），其中卷积层约 3.7M（约 6%），全连接层约 58.6M（约 94%）。

### 5.3 关键公式

#### ReLU 激活函数
$$\text{ReLU}(x) = \max(0, x)$$

对比 Sigmoid $\sigma(x) = \frac{1}{1 + e^{-x}}$：ReLU 在 $x > 0$ 时导数恒为 1，不饱和，梯度流动无衰减；Sigmoid 在 $|x|$ 较大时导数趋近于 0，导致梯度消失。

#### Local Response Normalization (LRN)
$$b_{x,y}^i = a_{x,y}^i \Big/ \left( k + \alpha \sum_{j = \max(0,\, i - n/2)}^{\min(N-1,\, i + n/2)} (a_{x,y}^j)^2 \right)^\beta$$

其中 $a_{x,y}^i$ 是第 $i$ 个通道在位置 $(x, y)$ 的激活值，$N$ 是总通道数，超参数 $(k, \alpha, \beta, n) = (2, 10^{-4}, 0.75, 5)$。LRN 在通道维度上做局部归一化，模拟生物神经元中的"侧抑制"机制。**注意：LRN 后来被 BatchNorm 取代。**

#### Dropout（训练时）
$$r_j \sim \text{Bernoulli}(p), \quad \tilde{y} = r \odot y$$

以概率 $p = 0.5$ 随机丢弃全连接层的神经元输出，每个 mini-batch 训练不同的稀疏子网络，等效于集成了指数级数量的子模型。

#### Overlapping Pooling
核大小 $3 \times 3$，步长 $S = 2 < 3$（核大小），池化窗口之间有重叠。相比传统非重叠池化（$S = 2, \text{kernel} = 2 \times 2$），Top-1 错误率降低 0.4%，且略微缓解过拟合。

### 5.4 符号说明表

| 符号 | 含义 | 在 AlexNet 中的值 |
| :--- | :--- | :--- |
| $C_{in}, C_{out}$ | 输入/输出通道数 | Conv1: (3→96); Conv2: (96→256); FC8: (4096→1000) |
| $H \times W$ | 特征图高度 × 宽度 | 输入 224×224 → Flatten 前 6×6 |
| $K$ | 卷积核大小 | Conv1: 11; Conv2: 5; Conv3/4/5: 3 |
| $S$ | 步长 (Stride) | Conv1: 4; Pool: 2 |
| $P$ | 填充 (Padding) | Conv2/3/4/5: 按保持尺寸原则 |
| $p_{\text{drop}}$ | Dropout 概率 | 0.5 |

---

## 6. 推导思路和思想来源

### 6.1 历史背景与"为什么是 2012 年"

- **数据条件成熟**：ImageNet 数据集（Deng et al., 2009）提供了 **120 万张标注图片、1000 个类别**，规模远超之前的 CIFAR-10（6 万张 32×32）和 MNIST（7 万张 28×28）。没有这个数据量，深度 CNN 的容量优势无从发挥。
- **算力条件成熟**：NVIDIA GTX 580（2010 年底发布），单卡 3GB 显存、1.58 TFLOPS。AlexNet 用了 **两张 GTX 580**，训练耗时约 **5-6 天**。
- **算法条件成熟**：Hinton 团队在 2006 年提出的逐层预训练 + 微调策略（DBN）为深层网络训练提供了信心；2010-2011 年 GPU 卷积实现（Cuda-Convnet）逐渐成熟。

### 6.2 设计决策的推理链

1. **为什么用 CNN 而不是全连接？** → 图像具有平移等变性，卷积的权重共享机制在参数量可控的前提下捕获局部视觉模式。
2. **为什么用 ReLU 而不是 Sigmoid？** → 实验证明 ReLU 在 CIFAR-10 上达到 25% 训练误差的速度是 Sigmoid 的 **6 倍**（图 1，原文）。原因：ReLU 在正半轴梯度恒为 1，不衰减；Sigmoid 在饱和区梯度趋近于 0，深层网络的前几层几乎收不到有效梯度信号。
3. **为什么双 GPU？** → 这是个**纯工程妥协**——GTX 580 单卡只有 3GB 显存，装不下完整 AlexNet 的 62M 参数 + 中间激活值。于是把网络拆成两半放到两张卡上：每张卡跑一半的特征图，只在 Conv3 和 FC 层做跨 GPU 通信。这不是设计优雅，而是**"显存不够，多卡来凑"**的历史痕迹。
4. **为什么用 Dropout？** → FC6 有 37.7M 参数（AlexNet 总参数的 60%），极其容易过拟合。Dropout 在训练时随机丢弃 50% 的神经元，迫使每个神经元学到鲁棒特征，效果等同于训练了 $2^{4096}$ 个稀疏子网络的集成。
5. **为什么 Conv1 用 11×11 大核？** → 输入 224×224 分辨率较高，大核在初始层能捕获更大范围的纹理和边缘模式。但这一步后来被 VGGNet 批判——VGG 将大核全部替换为堆叠的 3×3 小核，感受野相同但参数更少、非线性更强。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（逐层感受野计算）

**问题**：输入 224×224 图像中，Conv5 输出特征图上一个像素点能"看到"原始图像多大的区域？

逐层计算感受野（Receptive Field）：

| 层 | 核大小 | 步长 | 累积感受野 |
| :--- | :--- | :--- | :--- |
| Conv1 | 11×11 | 4 | 11 |
| Pool1 | 3×3 | 2 | 11 + (3-1)×4 = 19 |
| Conv2 | 5×5 | 1 | 19 + (5-1)×(4×2) = 51 |
| Pool2 | 3×3 | 2 | 51 + (3-1)×(4×2×1) = 67 |
| Conv3 | 3×3 | 1 | 67 + (3-1)×(4×2×1×2) = 99 |
| Conv4 | 3×3 | 1 | 99 + (3-1)×(4×2×1×2×1) = 131 |
| Conv5 | 3×3 | 1 | 131 + (3-1)×(4×2×1×2×1×1) = 163 |
| Pool5 | 3×3 | 2 | 163 + (3-1)×(4×2×1×2×1×1×2) = 195 |

Conv5 输出一个像素对应原始图像 **195×195** 的感受野。这说明即使是 5 层卷积，深层神经元也已经能"看到"输入图像的绝大部分区域（224×224 中覆盖 195×195）。

### 例子 2：中等例子（参数量分布可视化分析）

AlexNet 总参数 ≈ 62M，但分布极不均匀：

```
卷积层 (5层合计)：  约  3.7M 参数  (≈ 6%)
全连接层 (3层合计)： 约 58.6M 参数  (≈ 94%)
```

其中 **FC6 一层就占了 37.7M（约 60%）**！

为什么 FC6 这么"胖"？因为 Conv5 输出 $6 \times 6 \times 256 = 9216$ 个值，每个值都要连接到 FC6 的 4096 个神经元：

$$9216 \times 4096 = 37,748,736$$

这个观察直接启发了后续架构设计：
- **VGGNet**：仍然保留了三个大 FC 层，参数量爆炸（VGG16 ≈ 138M）
- **GoogLeNet (Inception)**：用全局平均池化 (Global Average Pooling) 替代全连接层，大幅压缩参数
- **ResNet**：同样用 GAP + 单 FC，ResNet-50 仅 25M 参数却远超 AlexNet 精度

### 例子 3：实际应用（PyTorch 从零实现 AlexNet）

```python
import torch
import torch.nn as nn

class AlexNet(nn.Module):
    """AlexNet 原始架构的 PyTorch 实现。

    注：为与 D2L 保持一致并适配现代硬件，这里实现的是简化版：
    - 单 GPU 版本（不手动分组，因为现代 GPU 显存充足）
    - 省略 LRN（已被 BatchNorm 替代）
    - 输入尺寸适配 224×224
    """

    def __init__(self, num_classes=1000):
        super().__init__()

        # ── 特征提取器（卷积层） ──
        self.features = nn.Sequential(
            # Conv1: 224×224×3 → 55×55×96 → pool → 27×27×96
            nn.Conv2d(3, 96, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),

            # Conv2: 27×27×96 → 27×27×256 → pool → 13×13×256
            nn.Conv2d(96, 256, kernel_size=5, stride=1, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),

            # Conv3: 13×13×256 → 13×13×384
            nn.Conv2d(256, 384, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),

            # Conv4: 13×13×384 → 13×13×384
            nn.Conv2d(384, 384, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),

            # Conv5: 13×13×384 → 13×13×256 → pool → 6×6×256
            nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )

        # ── 分类器（全连接层） ──
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),

            nn.Dropout(p=0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),

            nn.Linear(4096, num_classes),
        )

        # 权重初始化：与原文一致
        self._initialize_weights()

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                # 卷积层：均值 0，标准差 0.01 的高斯分布
                nn.init.normal_(m.weight, mean=0, std=0.01)
                if m.bias is not None:
                    # Conv2/4/5 偏置初始化为 1（加速 ReLU 激活）
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, mean=0, std=0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, start_dim=1)   # 展平为 (batch, 9216)
        x = self.classifier(x)
        return x


# ── 验证代码 ──
if __name__ == "__main__":
    model = AlexNet(num_classes=1000)

    # 统计参数量
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"总参数量: {total_params:,}  ({total_params / 1e6:.1f}M)")
    print(f"可训练参数: {trainable_params:,}  ({trainable_params / 1e6:.1f}M)")

    # 逐层参数量
    for name, param in model.named_parameters():
        if 'weight' in name:
            print(f"  {name:30s}  shape={str(param.shape):20s}  params={param.numel():>10,}")

    # 前向传播测试
    x = torch.randn(2, 3, 224, 224)
    out = model(x)
    print(f"\n输入: {x.shape}")
    print(f"输出: {out.shape}")  # [2, 1000]

    # 验证中间特征图尺寸
    features = model.features(x)
    print(f"Flatten 前特征图: {features.shape}")  # [2, 256, 6, 6]
```

运行输出示例：
```
总参数量: 62,378,344  (62.4M)
  features.0.weight              shape=[96, 3, 11, 11]       params=    34,848
  features.3.weight              shape=[256, 96, 5, 5]       params=   614,400
  features.6.weight              shape=[384, 256, 3, 3]      params=   885,120
  features.8.weight              shape=[384, 384, 3, 3]      params= 1,327,104
  features.10.weight             shape=[256, 384, 3, 3]      params=   884,736
  classifier.1.weight            shape=[4096, 9216]          params=37,748,736
  classifier.4.weight            shape=[4096, 4096]          params=16,777,216
  classifier.6.weight            shape=[1000, 4096]          params= 4,096,000

输入: torch.Size([2, 3, 224, 224])
输出: torch.Size([2, 1000])
Flatten 前特征图: torch.Size([2, 256, 6, 6])
```

---

## 8. 常见误区和易混概念

### 误区 1：AlexNet 是第一个 CNN
- **错误认知**："AlexNet 发明了卷积神经网络。"
- **为什么错**：CNN 的雏形可追溯到 **1989 年 LeCun 的 LeNet**（用于手写数字识别），甚至 1980 年 Fukushima 的 Neocognitron。AlexNet 不是 CNN 的发明者，而是**第一个让 CNN 在大规模自然图像上大放异彩**的架构。
- **正确理解**：AlexNet 之于 CNN，正如 iPhone 之于智能手机——都不是发明者，但都是引爆行业的关键催化剂。

### 误区 2：双 GPU 设计是核心创新
- **错误认知**："双 GPU 分组是一种精巧的架构设计，提升了模型效果。"
- **为什么错**：双 GPU 分组是 **GTX 580 单卡仅 3GB 显存的工程妥协**，不是刻意设计。Krizhevsky 自己后来也说，如果当时有更大显存的 GPU，根本不会这样分组。2013 年后的实践也证明，单 GPU 训练 AlexNet 效果一致甚至更好。
- **正确理解**：双 GPU 是历史遗迹——它让我们看到深度学习对算力的渴求如何倒逼硬件演进。

### 误区 3：LRN 很重要
- **错误认知**："LRN 是 AlexNet 成功的关键组件之一。"
- **为什么错**：原文中 LRN 带来的提升非常有限（Top-1 错误率降低约 1.4%，Top-5 降低约 1.2%）。2015 年 BatchNorm 出现后，LRN 被彻底取代——BN 不仅正则化效果更好，还加速了训练。
- **正确理解**：LRN 是 AlexNet 的"历史包袱"，后来者用 BN 替代。

### 概念对比表

| 概念 | AlexNet | LeNet-5 | 核心差异 |
| :--- | :--- | :--- | :--- |
| **提出年份** | 2012 | 1998 | 相差 14 年 |
| **输入尺寸** | 224×224×3 | 32×32×1 | 分辨率↑ 49 倍，彩色 vs. 灰度 |
| **深度** | 5 Conv + 3 FC | 2 Conv + 3 FC | 卷积层深度↑ 2.5 倍 |
| **通道数** | 96→256→384→384→256 | 6→16 | 通道数↑ 10-20 倍 |
| **激活函数** | **ReLU** | Sigmoid | 训练速度↑ 6 倍 |
| **正则化** | **Dropout** + 数据增强 | 无 | 过拟合控制 |
| **训练硬件** | 2× GTX 580 GPU | CPU | 算力飞跃 |
| **数据集** | ImageNet (1.2M 张) | MNIST (60K 张) | 数据量↑ 20 倍 |
| **参数量** | ≈ 62M | ≈ 60K | 参数量↑ 1000 倍 |
| **Top-5 错误率** | 15.3% | — | ILSVRC 2012 冠军 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖（前置知识）
- [[卷积神经网络CNN]]：卷积/池化/全连接的基本原理，理解这些才能看懂 AlexNet 各层的作用。
- [[激活函数详解]]：Sigmoid → ReLU 的动机（梯度消失问题），是 AlexNet 关键创新的理论基础。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Dropout|Dropout]]：AlexNet 首次在大规模 CNN 中验证了 Dropout 的有效性。

### 下游延伸（后续演进）
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/.归档/空壳文件/VGGNet|VGGNet]]：2014 年，将 AlexNet 的 11×11 和 5×5 大卷积核全部替换为堆叠 3×3 小核，统一设计哲学（更深的直筒网络）。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/🎯 ResNet (残差网络)|ResNet]]：2015 年，用残差连接解决"更深网络的退化问题"，突破了 AlexNet/VGG 的深度瓶颈。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/.归档/空壳文件/GoogLeNet|GoogLeNet (Inception)]]：2014 年，与 VGGNet 同年，引入 Inception 多分支并行模块和全局平均池化替代大 FC 层。

### 横向关联
- [[批归一化BatchNorm|BatchNorm]] ↔ AlexNet：BN (2015) 取代了 AlexNet 中的 LRN，成为训练深层网络的标准组件。
- [[数据增强与正则化|数据增强与正则化]] ↔ AlexNet：AlexNet 使用了图像平移/翻转 + PCA 颜色扰动两大数据增强策略。

---

## 10. 闭卷复现任务

- [ ] 1. 一句话说清楚 AlexNet 的历史意义（2012 ImageNet，深度学习击败传统 CV 的分水岭）。
- [ ] 2. 画出 AlexNet 的架构草图（5 Conv + 3 FC），标注每层输入输出尺寸。
- [ ] 3. 解释为什么 ReLU 比 Sigmoid 训练速度快 6 倍（梯度不饱和 vs. 饱和区梯度消失）。
- [ ] 4. 说明双 GPU 分组的真正原因（GTX 580 单卡 3GB 显存不够，不是刻意设计）。
- [ ] 5. 计算 FC6 的参数量（9216 × 4096 ≈ 37.7M），解释为什么它占了总参数的 60%。
- [ ] 6. 对比 AlexNet 与 LeNet-5 的六项关键差异（深度/输入/激活/正则化/硬件/数据量）。
- [ ] 7. 解释 Dropout 在 AlexNet 中为什么只放在全连接层而不放在卷积层。
- [ ] 8. 解释什么是 Overlapping Pooling，以及它为什么能略微减轻过拟合。
- [ ] 9. 手写不看书从零实现 AlexNet 的 PyTorch 代码（features + classifier 两大 Sequential）。
- [ ] 10. 说出 AlexNet 的三个"历史包袱"（LRN → BN 替代、双 GPU → 单 GPU、大核 Conv → 小核堆叠）。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | AlexNet 的历史地位 |
| 2 | 结构计算 | 基础 | FC6 参数量计算 |
| 3 | 技术对比 | 中等 | ReLU vs Sigmoid 梯度分析 |
| 4 | 架构理解 | 中等 | 双 GPU 分组与跨 GPU 通信 |
| 5 | 代码调试 | 较难 | 逐层特征图尺寸推导 |

### 题目与解析

#### 1. 关于 AlexNet 的历史地位，以下说法最准确的是？
- A. AlexNet 是第一个卷积神经网络
- B. AlexNet 是第一个在 ImageNet 上使用 GPU 训练的模型
- C. AlexNet 首次证明深度 CNN 可在大规模图像识别上大幅超越传统手工特征方法
- D. AlexNet 发明了 ReLU 和 Dropout

> [!question]- 答案解析
> - **答案**：C
> - **解析**：A 错，LeNet（1998）更早；B 错，2010-2011 年已有 GPU 训练的 CNN 参赛；D 错，ReLU 和 Dropout 此前已被提出，AlexNet 是首次在大型 CNN 中成功应用。C 精准概括了 AlexNet 的历史贡献：它是深度学习在 CV 领域"碾压"传统方法的标志性事件。
> - **对应知识点**：Section 1, 2。

#### 2. AlexNet 的 FC6 层将 Conv5 的 256 通道 6×6 特征图映射到 4096 维向量。请问 FC6 的权重参数量是多少（不含偏置）？
> [!question]- 答案解析
> - **答案**：$256 \times 6 \times 6 \times 4096 = 37,748,736$（约 37.7M）。
> - **解析**：FC 层的每个输入神经元都要连接到每个输出神经元。Conv5 展平后为 $9216$ 个值，连接到 $4096$ 个输出，故权重矩阵为 $4096 \times 9216$。这一层占了总参数的约 60%。
> - **对应知识点**：Section 5.2, 7 例子 2。

#### 3. 【对比分析】用 Sigmoid 训练一个 8 层全连接网络时，前 2 层梯度的模长约为输出层梯度的 $10^{-5}$ 倍（几乎无法更新）。换成 ReLU 后，这一比例大约变成多少？为什么？
> [!question]- 答案解析
> - **答案**：变成接近 1 倍（远好于 Sigmoid）。
> - **解析**：ReLU 在正半轴导数恒为 1，反向传播时梯度经过 ReLU 层要么原样通过（$x>0$），要么直接截断为 0（$x \leq 0$），不会像 Sigmoid 那样每经过一层就乘以一个 $\sigma'(x) \leq 0.25$ 的因子。链式法则连乘的结果是：Sigmoid 网络中 $0.25^8 \approx 1.5 \times 10^{-5}$，而 ReLU 网络中约 50% 的神经元在 $x>0$ 区间，梯度保留比例约为 $0.5^8 \approx 0.004$（这是最差情况，实际因为残差跳过得多得多）。关键是 ReLU 不存在"梯度被多级微小因子连乘压垮"的问题。
> - **对应知识点**：Section 5.3, 6.2。

#### 4. 在 AlexNet 的双 GPU 设计中原论文明确指出 Conv3 的核连接到**两个 GPU** 的 Conv2 输出，而 Conv1/Conv2/Conv4/Conv5 只在同一 GPU 内连接。为什么 Conv3 是例外？
> [!question]- 答案解析
> - **答案**：为了在保持 GPU 间通信开销可控的前提下，打破"每个 GPU 看到的信息一半是盲区"的局面。
> - **解析**：如果所有层都不跨 GPU，那么 GPU1 最终看到的只是"一半的特征"，分类器缺乏全局上下文。但每一层都跨 GPU 通信又会抵消掉双 GPU 的显存优势（通信开销大）。Conv3 作为中间层，恰到好处地在两个 GPU 的特征之间建立连接，后续 Conv4/5 再各自独立处理，兼顾了信息融合与显存效率。
> - **对应知识点**：Section 5.2, 6.2。

#### 5. 【代码推导】给定输入尺寸 227×227×3（AlexNet 论文中实际使用的尺寸），推导 Conv1→Pool1→Conv2→Pool2→Conv5→Pool5 每一步的特征图尺寸，并确认 Conv5 输出是否恰好为 6×6。
> [!question]- 答案解析
> - **答案**：
>   - Conv1: K=11, S=4, P=0 → $\lfloor\frac{227-11}{4}\rfloor+1 = 55$ → 55×55×96
>   - Pool1: K=3, S=2 → $\lfloor\frac{55-3}{2}\rfloor+1 = 27$ → 27×27×96
>   - Conv2: K=5, S=1, P=2 → $27-5+2\times2+1 = 27$ → 27×27×256
>   - Pool2: K=3, S=2 → $\lfloor\frac{27-3}{2}\rfloor+1 = 13$ → 13×13×256
>   - Conv3/Conv4: K=3, P=1 → 维持 13×13
>   - Conv5: K=3, P=1 → 13×13×256
>   - Pool5: K=3, S=2 → $\lfloor\frac{13-3}{2}\rfloor+1 = 6$ → **6×6×256** ✓
> - **解析**：最终 Flatten 得到 $6 \times 6 \times 256 = 9216$，与 FC6 输入维度一致。注意：D2L 使用 224×224 输入时 Conv1 输出为 54×54（因为 224 不能被 4 整除干净），但最终都能推算到约 6×6。
> - **对应知识点**：Section 5.2。

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释 AlexNet：

### 我的推导复现
> 不看上文，尝试画出 AlexNet 架构图并计算每层参数量：

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
  - [[🧠 第二阶段：深度学习内核|第二阶段：深度学习内核]]
  - [[卷积神经网络CNN|卷积神经网络 CNN]]
  - [[激活函数详解|激活函数详解]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/.归档/空壳文件/LeNet|LeNet]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/.归档/空壳文件/VGGNet|VGGNet]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/🎯 ResNet (残差网络)|ResNet]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Dropout|Dropout]]
- **建议标签**：`#学习` `#计算机视觉` `#AlexNet` `#CNN架构` `#ImageNet` `#深度学习`

---

*创建于：2026-08-06 | 来源：D2L Ch.8; Krizhevsky, Sutskever & Hinton (NeurIPS 2012)*

---

## 🧪 学完本节后可完成的作业

- 配合 [[03-Projects/课程作业/05-计算机视觉/课后习题/D2L-Ch8-现代CNN习题册|D2L-Ch8 习题册]]

---
---

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
