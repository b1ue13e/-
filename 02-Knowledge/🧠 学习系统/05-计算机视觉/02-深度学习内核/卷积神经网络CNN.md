---
type: study
course: "05-计算机视觉"
topic: "卷积神经网络 CNN (Convolutional Neural Network)"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept:
  - 卷积神经网络
  - CNN
  - 卷积核
  - 感受野
  - 池化
  - 权值共享
prerequisites:
  - "前向传播"
  - "梯度计算"
  - "图像表示"
related:
  - "ResNet"
  - "VGGNet"
  - "池化层"
  - "全连接网络"
flow: knowledge
stage_moc: "[[02-深度学习内核/🧠 第二阶段：深度学习内核]]"
kind: concept
source: "CS231n A2; D2L Ch.7"
anki_deck: "05-计算机视觉::02-深度学习内核"
anki_tags:
  - "CNN"
  - "卷积神经网络"
  - "卷积核"
  - "感受野"
  - "池化"
tags: [学习, 计算机视觉, CNN, 卷积, 图像处理, 特征提取]
---

# 卷积神经网络 CNN (Convolutional Neural Network)

> 所属路径：[[../🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 所属阶段：[[🧠 第二阶段：深度学习内核|🧠 第二阶段：深度学习内核（模型本质）]]
> 教材入口：[[../📚 教材挂载索引|教材挂载索引]]
> 核心源：CS231n Assignment 2; 《动手学深度学习》Ch.7

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：卷积神经网络（CNN）是过去十年计算机视觉领域最核心的架构范式。从 LeNet-5（1998）到手写数字识别，到 AlexNet（2012）引爆 ImageNet 竞赛的深度学习革命，再到 VGG、ResNet、EfficientNet 等 SOTA 分类网络的骨干——一切现代视觉系统的特征提取器都以卷积层为基本单元。即便在 Vision Transformer（ViT）崛起的今天，**卷积的局部感受野与权值共享两大归纳偏置**仍是理解视觉模型设计的起点。CS231n 将 CNN 列为 Assignment 2 的核心实现任务，要求从零手写卷积前向/反向传播；《动手学深度学习》以整个第 7 章展开现代 CNN 架构。**不理解卷积层的数学本质和计算特性，就无法真正理解任何视觉 backbone。**

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem（我们遇到了什么麻烦）**：

全连接网络（Fully-Connected Network, FC）处理图像时面临**维数灾难**与**语义错配**两大根本困境：

- **维数灾难**：一张 $224 \times 224 \times 3$ 的 RGB 图像展平后是一个 150,528 维的向量。若第一层隐藏层有 4096 个神经元，仅这一层的权重矩阵就达到 $150{,}528 \times 4096 \approx 6.17 \times 10^8$ 个参数（约 **2.3 GB / FP32**）。参数量爆炸导致无法训练、极易过拟合。
- **语义错配**：FC 层将图像的每个像素视为独立输入，完全忽略了像素之间的**空间邻接关系**——左上角像素和右下角像素在 FC 眼中没有任何区别。然而一只猫的耳朵是由相邻像素组成的局部纹理，与远处的背景像素毫无关系。FC 层天生"看不见"这种局部结构。

CNN 通过**局部感受野 + 权值共享 + 池化**三大机制，一举将参数量压缩数个数量级，同时天然编码了"邻近像素相关、远处像素独立"的空间先验。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：CNN 是计算机视觉从"手工特征工程（SIFT/HOG/LBP）"跃迁到"端到端可学习特征"的分水岭。卷积层自动学习从边缘→纹理→部件→物体的层级化特征表示，与人类视觉皮层（Hubel & Wiesel, 1962）的层级感受野机制惊人一致。
- **实际应用场景**：
  - **图像分类**：ResNet、EfficientNet 等 CNN backbone 是 ImageNet 分类的标准方案；
  - **目标检测**：Faster R-CNN、YOLO、SSD 均以 CNN 为骨干提取多尺度特征图；
  - **语义/实例分割**：FCN、U-Net、Mask R-CNN 使用全卷积结构输出像素级预测；
  - **医疗影像**：CNN 在 CT/MRI 病灶检测、病理切片分析中广泛部署；
  - **边缘端推理**：MobileNet、ShuffleNet 等轻量 CNN 在手机、IoT 设备上实时运行。
- **高频考点/任务**：
  - 卷积层输出尺寸公式推导（给定 $H_{in}, K, P, S, D$ 求 $H_{out}$）；
  - 卷积层参数量和 FLOPs 的手算；
  - 堆叠多层卷积的感受野递推公式 $RF_k = RF_{k-1} + (K_k - 1) \times \prod_{i=1}^{k-1} S_i$；
  - 对比 CNN vs FC vs ViT 的归纳偏置差异；
  - 手写 conv2d 前向传播（含 im2col 向量化实现）。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/图像滤波|图像滤波与互相关]]**：理解"滑动窗口 + 加权求和"的二维互相关（Cross-Correlation）运算——卷积层本质上就是一组可学习的滤波器。
2. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/感知机|感知机与全连接层]]**：理解神经元 $y = \sigma(\mathbf{w}^T \mathbf{x} + b)$ 的计算模式，CNN 的卷积核相当于在局部 patch 上的全连接权重。
3. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/前向传播|前向传播]]**：理解层间数据流动和参数与输入之间的计算图关系。
4. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/NumPy矩阵CV|NumPy 矩阵运算]]**：广播 (broadcasting)、reshape、einsum 等——是实现高效 conv2d 向量化的必备技能。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

- **直觉类比 1 — 手电筒扫描**：想象你手持一支手电筒在黑屋子里扫描一幅壁画——手电筒的光圈（卷积核 / Kernel）一次只能照亮一小块区域（局部感受野），你把光圈里看到的内容做个加权记录（内积），然后向右滑动一格（stride）继续看，逐行扫描直到覆盖整幅壁画。**同一个光圈**在整个过程中保持不变（权值共享），这就是卷积！

- **直觉类比 2 — 侦探识人**：侦探识别一个人时不会直接看整张脸，而是先找局部特征：额头纹路→眼角弧度→鼻梁轮廓→嘴角形状。低层卷积检测"边缘和颜色块"（相当于看局部皮肤纹理），中层卷积组合成"眼睛/鼻子/嘴巴"（相当于五官），高层卷积拼出"整张脸"（全局语义）。**逐层抽象，这正是卷积网络层级化特征学习的精髓。**

- **池化直觉 — 看地图的缩放**：当你把地图从 1:100 缩小到 1:10000 时，你不再关心每条小巷的精确位置，只保留关键地标（Max Pooling 取最显著特征）或区域概况（Average Pooling 取平均值）。池化就是在"降分辨率、保留核心信息、增强平移容忍度"。

- **一句话直觉本质**：卷积 = 用同一套"问题模板"（卷积核）扫过图像每一处，问"这里像不像我要找的东西？"——局部扫描节省参数，模板复用赋予平移不变性。

---

## 5. 正式定义、核心公式、符号解释

### 5.1 二维卷积（互相关）的数学定义

严格来说，深度学习中的"卷积"实际上是**互相关（Cross-Correlation）**——不翻转卷积核。给定输入张量 $\mathbf{X} \in \mathbb{R}^{C_{in} \times H_{in} \times W_{in}}$ 和卷积核 $\mathbf{W} \in \mathbb{R}^{C_{out} \times C_{in} \times K_h \times K_w}$，偏置 $\mathbf{b} \in \mathbb{R}^{C_{out}}$，输出特征图 $\mathbf{Y} \in \mathbb{R}^{C_{out} \times H_{out} \times W_{out}}$ 的第 $c_{out}$ 个通道、空间位置 $(i, j)$ 的值为：

$$\mathbf{Y}[c_{out}, i, j] = \sum_{c_{in}=0}^{C_{in}-1} \sum_{p=0}^{K_h-1} \sum_{q=0}^{K_w-1} \mathbf{W}[c_{out}, c_{in}, p, q] \cdot \mathbf{X}[c_{in}, i \cdot S + p, j \cdot S + q] + \mathbf{b}[c_{out}]$$

其中 $S$ 为步长（stride）。当使用 dilation $D$ 时，实际采样位置变为 $i \cdot S + p \cdot D$。

### 5.2 输出尺寸公式

$$H_{out} = \left\lfloor \frac{H_{in} + 2P_h - D_h(K_h - 1) - 1}{S_h} \right\rfloor + 1$$

$$W_{out} = \left\lfloor \frac{W_{in} + 2P_w - D_w(K_w - 1) - 1}{S_w} \right\rfloor + 1$$

**特殊情况速查表**：

| 配置 | 条件 | 输出尺寸 |
| :--- | :--- | :--- |
| Same Padding | $P = \lfloor K/2 \rfloor,\ S=1$ | $H_{out} = H_{in}$ |
| Valid Padding | $P = 0$ | $H_{out} = H_{in} - K + 1$ |
| 全尺寸降采样 | $S = 2$ | $H_{out} \approx H_{in} / 2$ |
| 空洞卷积 | $D > 1$ | 有效感受野扩大为 $K + (K-1)(D-1)$ |

### 5.3 参数量与 FLOPs 精确计算

**参数量（不含偏置）**：
$$\text{Params} = C_{out} \times C_{in} \times K_h \times K_w$$

**含偏置的参数量**：
$$\text{Params}_{\text{+bias}} = C_{out} \times (C_{in} \times K_h \times K_w + 1)$$

**FLOPs（浮点运算次数）**：每个输出位置执行 $C_{in} \times K_h \times K_w$ 次乘法和同样多次加法（共 $2 \times C_{in} \times K_h \times K_w$ 次浮点运算）：

$$\text{FLOPs} = 2 \times H_{out} \times W_{out} \times C_{out} \times C_{in} \times K_h \times K_w$$

**MACs（乘加次数）**：一次乘加 = 一次乘法 + 一次加法，因此：
$$\text{MACs} = H_{out} \times W_{out} \times C_{out} \times C_{in} \times K_h \times K_w$$

> **典例速算**：输入 $(1, 3, 224, 224)$，64 个 $7 \times 7$ 卷积核，stride=2, padding=3。
> $H_{out} = \lfloor (224 + 6 - 6) / 2 \rfloor + 1 = 112$，参数量 $= 64 \times 3 \times 7 \times 7 = 9{,}408$，FLOPs $\approx 2 \times 112 \times 112 \times 64 \times 3 \times 7 \times 7 \approx 2.36 \times 10^8$（约 0.24 GFLOPs）。

### 5.4 符号说明表

| 符号 | 含义 | 典型取值范围 |
| :--- | :--- | :--- |
| $H_{in}, W_{in}$ | 输入特征图的高和宽 | 32（CIFAR）~ 640（检测） |
| $C_{in}, C_{out}$ | 输入/输出通道数 | 3（RGB）→ 64 → 128 → 256 → 512 |
| $K_h, K_w$ | 卷积核空间尺寸 | $1, 3, 5, 7$（最常用 $3 \times 3$） |
| $S_h, S_w$ | 步长 (Stride) | 通常 1 或 2 |
| $P_h, P_w$ | 填充量 (Padding) | $\lfloor K/2 \rfloor$ 实现 same padding |
| $D_h, D_w$ | 膨胀率 (Dilation) | 1（标准卷积）或 >1（空洞卷积） |
| $N$ | 批大小 (Batch Size) | 32, 64, 128 |
| $RF_k$ | 第 $k$ 层的感受野 | 逐层递推 |

---

## 6. 推导思路和思想来源

### 6.1 从全连接到局部连接：生物学启发

1959-1962 年，Hubel 和 Wiesel 通过猫的视觉皮层实验发现：视觉皮层中存在**简单细胞（Simple Cells）**和**复杂细胞（Complex Cells）**。简单细胞仅对视野中特定位置、特定方向的条形刺激作出响应——这就是"局部感受野"的生物学原型；复杂细胞对更大范围内的刺激方向敏感但对精确位置不敏感——这正是"池化带来局部平移不变性"的灵感来源。

### 6.2 权值共享的数学动机

在没有权值共享的情况下，一个 $K \times K$ 卷积核对每个空间位置都使用不同参数，参数量为 $C_{out} \times C_{in} \times K_h \times K_w \times H_{out} \times W_{out}$——这几乎与全连接层一样庞大。

**关键转念**：如果某个特征（比如"45° 边缘"）在图像的左上角有意义，那它在右下角也应该同样有意义。**同一个特征检测器应该在所有空间位置共享参数。** 这不仅将参数量骤降为 $C_{out} \times C_{in} \times K_h \times K_w$（与输入分辨率完全解耦！），还天然赋予卷积层**平移等变性 (Translation Equivariance)**：输入平移会导致输出特征图相应平移。

### 6.3 感受野递推公式推导

第 $k$ 层的感受野 $RF_k$（即输出特征图上一点在原始输入图像上"看到"的区域大小）由以下递推公式给出：

$$RF_k = RF_{k-1} + (K_k - 1) \times \prod_{i=1}^{k-1} S_i$$

其中 $RF_0 = 1$（输入层每个像素感受野为自己）。**直观理解**：每加一层卷积，感受野扩大 $(K_k - 1)$ 倍——但这个扩大发生在"上一层特征图的分辨率尺度"下，所以还要乘以之前所有层的累积步长。

**经典结论**：两层 $3 \times 3$ 卷积（无池化）的感受野 = $1 + (3-1) + (3-1) \times 1 = 5$，等价于一个 $5 \times 5$ 卷积核——但参数量仅为 $2 \times C \times 3 \times 3 = 18C$，而一个 $5 \times 5$ 卷积核为 $25C$。**用小卷积核堆叠代替大卷积核，参数更少、非线性更多、感受野相同！**（这也是 VGG 全部使用 $3 \times 3$ 卷积的设计哲学。）

### 6.4 im2col：卷积到矩阵乘法的优雅转化

卷积运算本质上是**局部 patch 的加权求和**。im2col 算法的核心思路是将滑窗操作展开为矩阵乘法：

1. 将输入图像的每个 $K_h \times K_w \times C_{in}$ 的滑动窗口 patch 拉伸为一列向量；
2. 将所有 $H_{out} \times W_{out}$ 个位置的 patch 列堆叠成矩阵 $\mathbf{X}_{col} \in \mathbb{R}^{(C_{in} K_h K_w) \times (H_{out} W_{out})}$；
3. 将卷积核权重重塑为矩阵 $\mathbf{W}_{row} \in \mathbb{R}^{C_{out} \times (C_{in} K_h K_w)}$；
4. 卷积转化为高效矩阵乘法：$\mathbf{Y} = \mathbf{W}_{row} \cdot \mathbf{X}_{col}$，再 reshape 回 $(C_{out}, H_{out}, W_{out})$。

这不仅是 NumPy 向量化实现的基础，更是 cuDNN 中 `implicit_gemm` 算法的核心思想。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础 — 单通道 $3 \times 3$ 卷积手算

假设输入为 $5 \times 5$ 单通道图像 $\mathbf{X}$，一个 $3 \times 3$ 卷积核 $\mathbf{K}$（sobel 垂直边缘检测器）：

$$\mathbf{X} = \begin{bmatrix}
1 & 2 & 0 & 1 & 0 \\
0 & 1 & 2 & 1 & 2 \\
1 & 0 & 2 & 0 & 1 \\
2 & 2 & 1 & 0 & 0 \\
0 & 3 & 1 & 2 & 1
\end{bmatrix}, \quad
\mathbf{K} = \begin{bmatrix}
-1 & 0 & 1 \\
-2 & 0 & 2 \\
-1 & 0 & 1
\end{bmatrix}$$

对输入左上角 $3 \times 3$ 区域计算 $S=1, P=0$：
$$\mathbf{Y}[0,0] = (1)(-1) + (2)(0) + (0)(1) + (0)(-2) + (1)(0) + (2)(2) + (1)(-1) + (0)(0) + (2)(1) = -1+0+0+0+0+4-1+0+2 = 4$$

输出尺寸 = $5-3+1 = 3$，即 $3 \times 3$ 特征图，其中正值表示"从左暗到右亮"的垂直边缘。

### 例子 2：中等 — PyTorch 风格 conv2d 前向传播（含 for 循环的直观版）

```python
import numpy as np

def conv2d_forward_naive(x: np.ndarray, weight: np.ndarray, bias: np.ndarray,
                         stride: int = 1, padding: int = 0) -> np.ndarray:
    """
    手动实现 2D 卷积层前向传播（显式 for 循环版本，便于理解）。
    x:      (N, C_in, H_in, W_in)
    weight: (C_out, C_in, K_h, K_w)
    bias:   (C_out,)
    返回:   (N, C_out, H_out, W_out)
    """
    N, C_in, H_in, W_in = x.shape
    C_out, _, K_h, K_w = weight.shape

    H_out = (H_in + 2 * padding - K_h) // stride + 1
    W_out = (W_in + 2 * padding - K_w) // stride + 1

    # 零填充
    x_padded = np.pad(
        x,
        ((0, 0), (0, 0), (padding, padding), (padding, padding)),
        mode='constant'
    )
    out = np.zeros((N, C_out, H_out, W_out), dtype=np.float32)

    for n in range(N):
        for c_out in range(C_out):
            for h in range(H_out):
                for w in range(W_out):
                    h_start = h * stride
                    w_start = w * stride
                    patch = x_padded[n, :,
                                     h_start:h_start + K_h,
                                     w_start:w_start + K_w]
                    out[n, c_out, h, w] = (
                        np.sum(patch * weight[c_out]) + bias[c_out]
                    )
    return out


if __name__ == "__main__":
    np.random.seed(42)
    x = np.random.randn(1, 3, 5, 5).astype(np.float32)
    weight = np.random.randn(2, 3, 3, 3).astype(np.float32)
    bias = np.array([0.1, -0.2], dtype=np.float32)

    out = conv2d_forward_naive(x, weight, bias, stride=1, padding=0)
    assert out.shape == (1, 2, 3, 3), f"输出尺寸异常: {out.shape}"

    out_pad = conv2d_forward_naive(x, weight, bias, stride=1, padding=1)
    assert out_pad.shape == (1, 2, 5, 5), "Same padding 应保持空间尺寸不变"

    print("✓ naive conv2d 所有断言通过")
    print(f"  无 padding 输出 shape: {out.shape}")
    print(f"  Same padding 输出 shape: {out_pad.shape}")
```

### 例子 3：实际应用 — im2col 向量化高效 conv2d（**不含 for 循环**）

这是 CS231n Assignment 2 的核心实现要求，也是现代深度学习框架底层（cuDNN/im2col+GEMM）的真实计算方式。

```python
import numpy as np

def im2col(x: np.ndarray, K_h: int, K_w: int,
           stride: int, padding: int) -> np.ndarray:
    """
    将图像滑动窗口 patch 展开为列矩阵 —— 卷积向量化的关键步骤。

    参数:
        x: 输入张量 (N, C_in, H_in, W_in)
        K_h, K_w: 卷积核空间尺寸
        stride: 步长
        padding: 填充量
    返回:
        col: (N, C_in * K_h * K_w, H_out * W_out)
             每一列 = 一个滑动窗口内所有像素的展平向量
    """
    N, C_in, H_in, W_in = x.shape
    H_out = (H_in + 2 * padding - K_h) // stride + 1
    W_out = (W_in + 2 * padding - K_w) // stride + 1

    # 零填充
    x_padded = np.pad(
        x,
        ((0, 0), (0, 0), (padding, padding), (padding, padding)),
        mode='constant'
    )

    # ------------------------------
    #  核心技巧：使用 stride_tricks 而非 for 循环提取所有 patch
    # ------------------------------
    # 构造一个视图，使得 x_padded 的内存被"看作"一个 6 维张量：
    #   (N, C_in, H_out, W_out, K_h, K_w)
    # 其中 H_out 和 W_out 维度通过 stride 跳跃实现
    shape = (N, C_in, H_out, W_out, K_h, K_w)
    strides = (
        x_padded.strides[0],                          # N 维度步长
        x_padded.strides[1],                          # C_in 维度步长
        x_padded.strides[2] * stride,                 # 以 stride 步长在 H 上滑动
        x_padded.strides[3] * stride,                 # 以 stride 步长在 W 上滑动
        x_padded.strides[2],                          # patch 内 H 连续读取
        x_padded.strides[3],                          # patch 内 W 连续读取
    )

    # as_strided 创建零拷贝视图（注意：这不会分配新内存！）
    patches = np.lib.stride_tricks.as_strided(
        x_padded, shape=shape, strides=strides
    )

    # 重排为 (N, H_out, W_out, C_in, K_h, K_w) → 展平每个 patch 为一列
    # → (N, H_out, W_out, C_in * K_h * K_w) → transpose → (N, C_in*K_h*K_w, H_out*W_out)
    col = (patches
           .transpose(0, 2, 3, 1, 4, 5)          # (N, H_out, W_out, C_in, K_h, K_w)
           .reshape(N, H_out * W_out, -1)         # (N, H_out*W_out, C_in*K_h*K_w)
           .transpose(0, 2, 1))                   # (N, C_in*K_h*K_w, H_out*W_out)

    return col


def conv2d_forward_vectorized(x: np.ndarray, weight: np.ndarray,
                               bias: np.ndarray,
                               stride: int = 1,
                               padding: int = 0) -> np.ndarray:
    """
    纯 NumPy 向量化 2D 卷积前向传播 —— 不含任何 Python for 循环。

    核心思路：im2col 展开 + 矩阵乘法 (GEMM)

    x:      (N, C_in, H_in, W_in)
    weight: (C_out, C_in, K_h, K_w)
    bias:   (C_out,)
    返回:   (N, C_out, H_out, W_out)
    """
    N, C_in, H_in, W_in = x.shape
    C_out, _, K_h, K_w = weight.shape

    H_out = (H_in + 2 * padding - K_h) // stride + 1
    W_out = (W_in + 2 * padding - K_w) // stride + 1

    # Step 1: im2col — 将输入展开为列矩阵
    #   x_col: (N, C_in*K_h*K_w, H_out*W_out)
    x_col = im2col(x, K_h, K_w, stride, padding)

    # Step 2: 将卷积核重塑为矩阵
    #   w_row: (C_out, C_in*K_h*K_w)
    w_row = weight.reshape(C_out, -1)

    # Step 3: 矩阵乘法 — 批量 GEMM
    #   out_col: (N, C_out, H_out*W_out)
    #   np.matmul 自动处理 batch 维度广播：(N, a, b) @ (N, b, c) 不可行
    #   改用 einsum 显式指定维度收缩
    out_col = np.einsum('ncp,oc->nop', x_col, w_row)  # (N, C_out, H_out*W_out)

    # Step 4: reshape 回特征图形状 + 加偏置
    out = out_col.reshape(N, C_out, H_out, W_out)
    out += bias.reshape(1, C_out, 1, 1)  # 广播加法

    return out


# ═══════════════════════════════════════════
#  验证：与 naive 版本对比正确性
# ═══════════════════════════════════════════
if __name__ == "__main__":
    np.random.seed(42)

    # 测试 1: 基本正确性
    N, C_in, H_in, W_in = 2, 3, 32, 32
    C_out, K = 16, 3
    x = np.random.randn(N, C_in, H_in, W_in).astype(np.float32)
    weight = np.random.randn(C_out, C_in, K, K).astype(np.float32)
    bias = np.random.randn(C_out).astype(np.float32)

    out_naive = conv2d_forward_naive(x, weight, bias, stride=1, padding=1)
    out_vec = conv2d_forward_vectorized(x, weight, bias, stride=1, padding=1)

    diff = np.max(np.abs(out_naive - out_vec))
    print(f"测试 1 — 正确性验证: max|naive - vectorized| = {diff:.2e}")
    assert diff < 1e-4, f"向量化结果与 naive 不一致！diff = {diff}"
    print("  ✓ 通过")

    # 测试 2: stride=2 降采样
    out_naive_s2 = conv2d_forward_naive(x, weight, bias, stride=2, padding=1)
    out_vec_s2 = conv2d_forward_vectorized(x, weight, bias, stride=2, padding=1)
    H_out_s2 = (32 + 2 - 3) // 2 + 1  # = 16
    assert out_vec_s2.shape == (N, C_out, H_out_s2, H_out_s2)
    diff_s2 = np.max(np.abs(out_naive_s2 - out_vec_s2))
    print(f"测试 2 — stride=2: shape={out_vec_s2.shape}, diff={diff_s2:.2e}")
    assert diff_s2 < 1e-4
    print("  ✓ 通过")

    # 测试 3: 大 batch + 多通道 + 大特征图性能对比
    x_large = np.random.randn(8, 64, 56, 56).astype(np.float32)
    w_large = np.random.randn(128, 64, 3, 3).astype(np.float32)
    b_large = np.random.randn(128).astype(np.float32)

    import time
    t0 = time.time()
    _ = conv2d_forward_vectorized(x_large, w_large, b_large, stride=1, padding=1)
    t_vec = time.time() - t0
    print(f"测试 3 — 性能: (8,64,56,56) → (8,128,56,56), "
          f"向量化耗时 {t_vec*1000:.1f} ms")

    # 测试 4: 输出尺寸公式验证
    # Same padding: P = floor(K/2) = 1, S=1 → H_out = H_in
    out_same = conv2d_forward_vectorized(x, weight, bias, stride=1, padding=1)
    assert out_same.shape[2:] == (32, 32), "Same padding 应保持尺寸不变"
    print("测试 4 — Same padding 尺寸验证: ✓ 通过")

    # 测试 5: 感受野计算
    # 两层 3x3(无池化): RF = 1 + (3-1) + (3-1)*1 = 5, 等价于一个 5x5 卷积
    rf = 1 + (3 - 1) + (3 - 1) * 1
    assert rf == 5, f"两层 3×3 感受野应为 5，实际 {rf}"
    print(f"测试 5 — 感受野: 两层 3×3 → RF = {rf} (等价 5×5 卷积) ✓")

    print("\n🎉 所有测试通过！向量化 conv2d 实现正确。")
```

**关键说明 — `np.lib.stride_tricks.as_strided`**：
- 这是 NumPy 中**零拷贝视图**机制，它不分配新内存，仅改变对同一块内存的"观察方式"；
- `shape` 参数告诉 NumPy"将这块内存视为什么形状"，`strides` 参数告诉它"每个维度跳多少字节"；
- `strides[2] * stride` 让 H_out 维度以 stride 步长跳跃，天然实现了滑动窗口采样；
- **注意**：`as_strided` 不检查内存边界，如果参数错误可能导致读取越界数据（无声错误）；本实现中 `shape` 和 `strides` 的计算已保证安全。

---

## 8. 常见误区和易混概念

### 误区 1："卷积"就是数学上的卷积运算

- **错误理解**：深度学习中的卷积是信号处理中定义的卷积 $ (f * g)(t) = \int f(\tau) g(t - \tau) d\tau $（核翻转 180°）。
- **为什么错**：CNN 中实际执行的是**互相关（Cross-Correlation）**，核不翻转。两者在数学上等价（学到的核只是翻转了），但实现和推导时混用会造成符号混乱。
- **正确表述**：CNN 的"卷积" = 互相关 = 滑动窗口 + 逐元素乘积 + 求和。

### 误区 2：参数量与输入分辨率有关

- **错误直觉**："224×224 的图像比 32×32 的图像需要更多卷积参数。"
- **为什么错**：卷积核参数仅由 $C_{in}, C_{out}, K_h, K_w$ 决定，与输入空间尺寸**完全无关**。这也是 CNN 可以处理任意分辨率图像的根本原因。输入分辨率影响的是**计算量（FLOPs）** 和**显存占用（Activations）**，而非参数量。
- **对比全连接层**：FC 层的权重矩阵形状直接绑定输入维度，输入大小一变网络结构就得改。

### 误区 3：池化层可有可无

- **错误直觉**："现在都用 stride=2 的卷积替代池化了，池化层已经过时。"
- **辩证分析**：stride=2 卷积确实可以降采样且可学习（如 ResNet 的 downsampling block），但池化有以下不可替代的特性：
  - **Max Pooling 提供局部平移不变性**：即使特征在小范围内偏移，最大值仍然被保留；
  - **无参数、不过拟合**：池化层零参数，是天然的正则化器；
  - **感受野快速扩张**：$2 \times 2$ 池化将有效感受野翻倍，比堆卷积更高效。
- **正确理解**：现代架构（如 ConvNeXt）趋向于减少池化、多用 stride 卷积，但这不是"池化无用"的证明，而是设计偏好的变迁。

### 误区 4：$1 \times 1$ 卷积没什么用

- **错误直觉**："$1 \times 1$ 卷积只是乘一个标量，能有什么用？"
- **纠正**：$1 \times 1$ 卷积不混合空间信息，但它**跨通道进行线性组合**——相当于在通道维度做全连接。作用是：
  - 通道升降维（bottleneck 结构核心技术）；
  - 增加非线性（配合 ReLU 在不改变空间尺寸的情况下增强表达能力）；
  - 融合多通道信息（Network in Network, 2013）。

### 概念对比表

| 维度 | 卷积层 (Conv) | 全连接层 (FC) | Vision Transformer (ViT) |
| :--- | :--- | :--- | :--- |
| **归纳偏置** | **强**（局部性 + 平移等变性） | 无 | **弱**（需海量数据/强增强预训练） |
| **参数复杂度** | $O(K^2 \cdot C_{in} C_{out})$，与分辨率无关 | $O(HWC_{in} \cdot N_{hidden})$ | $O(C^2 \cdot L)$（$L$ 为层数） |
| **计算复杂度** | $O(K^2 \cdot HW \cdot C_{in} C_{out})$ | $O(N_{in} N_{out})$ | $O((HW)^2 \cdot C)$（全局自注意力） |
| **小样本泛化** | **强**（内置空间先验，少量数据即可收敛） | 极差 | 中等偏弱 |
| **长距离依赖** | 需深层堆叠/空洞卷积才能捕获 | 天然全连接 | **单层全局感受野** |
| **输入灵活性** | 接受任意分辨率 | 固定输入尺寸 | 固定 patch 数（可插值位置编码） |
| **平移处理** | **等变性**（输入平移 → 输出同平移） | 无特殊处理 | 需位置编码辅助 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/图像滤波|图像滤波]]**：互相关运算的根本来源，Sobel/Canny/高斯滤波都是固定核卷积。
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/感知机|感知机与全连接层]]**：CNN 神经元是 FC 神经元在局部 patch 上的特例。
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/前向传播|前向传播]]**：卷积层的前向传播 = 滑窗内积 + 偏置 + 激活。

### 下游延伸
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/ResNet残差网络|ResNet]]**：以 $3 \times 3$ 卷积为基本单元的残差结构，CNN 架构的巅峰进化。
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/VGGNet|VGGNet]]**：证明"小卷积核堆叠 > 大卷积核"的设计哲学。
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/感受野|感受野]]**：深入递推公式、有效感受野（ERF）、扩张卷积的感受野计算。

### 横向关联
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/BatchNorm|BatchNorm]]** ↔ CNN：BN 使深层 CNN 训练稳定，是 ResNet 成功的另一半。
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/ViT|ViT]]** ↔ CNN：CNN 的归纳偏置 vs Transformer 的全局注意力——"局部先验"和"数据驱动全局性"的根本哲学分歧。
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/ConvNeXt|ConvNeXt]]**："CNN 现代化"的代表作，将 Transformer 的训练/结构技巧反哺 CNN。
- **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/参数量计算|参数量计算]]**：系统化的 CNN 各层参数量/FLOPs 计算方法。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚 CNN 相比全连接网络的两大根本优势（参数效率 + 空间先验）。
- [ ] 2. 用直觉语言解释三大核心机制：局部感受野、权值共享、池化（«"这东西其实就像……"»）。
- [ ] 3. 写出卷积层输出尺寸的完整公式（含 dilation），并手算一个具体例子（如输入 32×32，K=3, P=1, S=2 → H_out=?）。
- [ ] 4. 写出卷积层的参数量公式和 FLOPs 公式，并计算 Conv2d(3→64, K=7, S=2, P=3, 输入 224×224) 的参数量。
- [ ] 5. 推导两层 $3 \times 3$ 卷积（S=1, 无池化）的感受野，验证其等价于一个 $5 \times 5$ 卷积。
- [ ] 6. 默写 im2col + 矩阵乘法的向量化 conv2d 伪代码/核心步骤。
- [ ] 7. 解释 im2col 中 `as_strided` 的 shape 和 strides 参数的作用。
- [ ] 8. 对比 CNN vs FC vs ViT 的归纳偏置强弱与计算复杂度。
- [ ] 9. 区分"卷积"和"互相关"在 CNN 语境下的实际含义。
- [ ] 10. 解释为什么 CNN 可以接受任意尺寸输入而全连接网络不行。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 卷积 vs 互相关 |
| 2 | 公式计算 | 基础 | 输出尺寸 + 参数量 + FLOPs 手算 |
| 3 | 结构理解 | 中等 | 感受野递推 + 小卷积核堆叠优势 |
| 4 | 维度推理 | 中等 | 1×1 卷积的作用与 bottleneck 原理 |
| 5 | 开放/迁移 | 较难 | CNN 归纳偏置 vs ViT 全局自注意力 |

### 题目与解析

#### 1. 以下关于 CNN 中"卷积"运算的说法，正确的是？
- A. CNN 的卷积等价于数学中的卷积运算（核翻转 180°）
- B. CNN 实际执行的是互相关（Cross-Correlation），核不翻转
- C. 卷积和互相关在 CNN 中会产生完全不同的特征图，不可互换
- D. 卷积核在每次前向传播时会自动翻转

> [!question]- 答案解析
> - **答案**：B
> - **解析**：深度学习框架中的"卷积"实际实现的是互相关（核不翻转）。数学上两者等价——如果网络需要翻转核，学习算法自会学到翻转版本的权重。A 错在把"名称"当"定义"；C 错在两者通过权重对称性可互换；D 完全是编造的。
> - **对应误区**：误区 1。

#### 2. 输入张量形状为 $(1, 3, 224, 224)$，使用 64 个 $7 \times 7$ 卷积核，stride=2, padding=3, dilation=1。求：输出形状、卷积层参数量（含 bias）、近似 FLOPs。
> [!question]- 答案解析
> - **输出尺寸**：$H_{out} = \lfloor (224 + 2\times 3 - 1\times(7-1) - 1) / 2 \rfloor + 1 = \lfloor (224+6-6-1)/2 \rfloor + 1 = \lfloor 223/2 \rfloor + 1 = 111 + 1 = 112$。输出形状 = $(1, 64, 112, 112)$。
> - **参数量**：$64 \times (3 \times 7 \times 7 + 1) = 64 \times (147 + 1) = 64 \times 148 = 9{,}472$。
> - **FLOPs**：$2 \times 112 \times 112 \times 64 \times 3 \times 7 \times 7 = 2 \times 112^2 \times 64 \times 147 = 2 \times 12{,}544 \times 9{,}408 \approx 2.36 \times 10^8$（约 0.236 GFLOPs）。
> - **要点**：注意区分 Params（与分辨率无关）和 FLOPs（与分辨率成正比）。

#### 3. 在 VGG 的设计哲学中，为什么使用两个 $3 \times 3$ 卷积堆叠而非一个 $5 \times 5$ 卷积？
> [!question]- 答案解析
> - **答案**：两者感受野相同（都是 $5 \times 5$），但：
>   1. **参数更少**：两个 $3 \times 3$ 参数 = $2 \times C \times C \times 9 = 18C^2$；一个 $5 \times 5$ = $C \times C \times 25 = 25C^2$，节省约 28%。
>   2. **非线性更多**：两个卷积之间多插入一次 ReLU，增强模型表达能力。
>   3. **正则化效果**：分解为更小的卷积核相当于施加了低秩正则化约束。
> - **对应知识点**：6.3 感受野递推。

#### 4. 在 ResNet 的 Bottleneck 结构中（1×1→3×3→1×1），中间的 $3 \times 3$ 卷积通道数很小（如 64）。如果去掉两端的 $1 \times 1$ 卷积，直接对 256 通道做 $3 \times 3$ 卷积，参数量会发生什么变化？
> [!question]- 答案解析
> - **答案**：Bottleneck 总参数 = $256\times 64\times 1\times 1 + 64\times 64\times 3\times 3 + 64\times 256\times 1\times 1 = 16{,}384 + 36{,}864 + 16{,}384 = 69{,}632$。直接 $3 \times 3$ 卷积参数 = $256 \times 256 \times 3 \times 3 = 589{,}824$。**Bottleneck 节省了 88.2% 的参数量！**
> - **直观理解**：$1 \times 1$ 卷积先将高维通道"压缩"到低维瓶颈，让昂贵的 $3 \times 3$ 空间卷积在低维空间进行，最后再"解压"回去——信息流过窄瓶颈但不丢失关键特征。

#### 5. 【开放/迁移】ViT 将图像切割为 16×16 的 patch，每个 patch 通过线性投影变为 token，然后用全局自注意力处理。相比之下，CNN 用局部卷积逐层扩大感受野。请分析两种方式各自的根本优势和劣势。
> [!question]- 答案解析
> - **答案要点**：
>   - **CNN 优势**：局部感受野 + 权值共享是强归纳偏置，小数据集上泛化好、训练快；层级化特征（边缘→纹理→物体）天然符合视觉规律。
>   - **CNN 劣势**：浅层感受野有限，捕获长距离依赖需要堆很多层或用大卷积核；对全局上下文建模"间接"。
>   - **ViT 优势**：自注意力单层即可全局感受野，长距离依赖一步到位；缺少硬编码空间偏置，在大数据（JFT-300M, 数亿张）预训练下可以学到更灵活的空间关系。
>   - **ViT 劣势**：缺少归纳偏置意味着小数据集上极易过拟合，需要海量数据或强数据增强（如 RandAugment）；注意力 $O(N^2)$ 复杂度限制了高分辨率输入。
>   - **趋势**：ConvNeXt、CoAtNet 等混合架构正在融合两者优势——卷积捕获局部底层特征、注意力建模高层全局关系。

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
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/图像滤波|图像滤波]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/感知机|感知机]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/ResNet残差网络|ResNet]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/感受野|感受野]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/参数量计算|参数量计算]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/ViT|ViT]]
- **建议标签**：`#学习` `#深度学习` `#计算机视觉` `#CNN` `#卷积` `#感受野` `#池化` `#权值共享`
- **复习节奏**：首次学习后 1/3/7/14 天间隔复习，配合 Section 10 闭卷复现任务自查。

---

## 🧪 学完本节后可完成的作业

- 可直接完成 [[03-Projects/课程作业/05-计算机视觉/课后作业/🎓 HW03 - 小型 CNN 与训练工程正式作业说明书|HW03]]
- 配合 [[03-Projects/课程作业/05-计算机视觉/课后习题/D2L-Ch7-卷积神经网络习题册|D2L-Ch7 习题册]]

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
