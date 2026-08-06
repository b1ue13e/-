---
type: study
course: "05-计算机视觉"
topic: "线性代数基础（CV视角）"
created: 2026-08-05
status: ongoing
difficulty: beginner
concept: ["线性代数", "矩阵运算", "向量空间", "特征值", "SVD"]
prerequisites: ["高中数学"]
related: ["图像表示", "几何变换CV", "特征分解CV", "梯度下降"]
flow: knowledge
stage_moc: "[[🏗️ 第一阶段：底层基石]]"
kind: concept
source: "《Mathematics for Machine Learning》Ch.2-4"
anki_deck: "05-计算机视觉::01-底层基石"
anki_tags: ["计算机视觉", "线性代数", "数学基础"]
tags: [学习, 计算机视觉, 线性代数, 数学基础]
---

# 线性代数基础（CV视角）

> 所属模块：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 主教材：`《Mathematics for Machine Learning》` Ch.2-4；`《Linear Algebra and Its Applications》` Strang
> 对应阶段：[[🏗️ 第一阶段：底层基石|返回阶段页]]
> 建议先看：[[图像表示]]、NumPy数组CV
> 辅助教材：`3Blue1Brown - Essence of Linear Algebra`（几何直觉）

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：线性代数是计算机视觉的**底层语言**。一张图像是一个矩阵，一个卷积核是一个小矩阵，旋转缩放是矩阵乘法，PCA 降维是特征分解，图像压缩是 SVD 低秩逼近——整个 CV 的数学底座就建在线性代数之上。不理解矩阵乘法的几何含义，你就看不懂卷积层为什么能做边缘检测；不理解特征值，你就无法真正理解 PCA 为什么有效；不理解 SVD，图像压缩对你来说就是黑盒魔法。**这一卡是整门课所有数学推导的共同前序——跳过它，后面每一张卡都会在公式面前卡住。**

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 你打开一张 256×256 的灰度照片，计算机看到的不是"一只猫"，而是一个 $256 \times 256$ 的数字矩阵。然后你告诉计算机："把这个猫旋转 30 度"，"把这个猫压缩到原来的 1/10 大小"，"找出这张猫图里最重要的特征"——这每一件事都不是"看图说话"，而是**大规模矩阵运算**。
>
> 问题来了：
> - 旋转 30 度——对应的矩阵长什么样？它怎么作用在图像矩阵上？
> - 卷积神经网络的第一层 3×3 卷积核——它和矩阵乘法是什么关系？
> - 一张 1000×1000 的图像有 100 万个像素——怎样用区区 1000 个数字近似它？
> - 损失函数 $J(W)$ 对权重矩阵 $W$ 求梯度——矩阵的"导数"长什么样？$\frac{\partial J}{\partial W}$ 的维度是什么？
> - PCA 降维时说的"最大方差方向"——在数学上到底对应矩阵的什么量？
>
> **线性代数基础（CV视角）** 就是对以上所有问题的系统性回答：把抽象的线性代数概念**一一映射到 CV 中你能摸得着的场景**。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：线性代数是 CV 数学底座的"第一支柱"（另外两根是微积分和概率论）。从图像表示的 `(H, W, C)` 张量定义，到 ResNet 中残差连接的矩阵加法，到 ViT 中 384 维 patch embedding 的内积——全都是线性代数运算。可以说，**每一个 CV 模型的 forward pass，本质上就是一系列矩阵乘法和逐元素非线性变换的交替**。
- **实际应用场景**：
  - **图像变换**：旋转、缩放、平移、透视——全部表示为矩阵乘法，GPU 专门为此设计了硬件加速单元（Tensor Cores）。
  - **卷积运算**：3×3 卷积核在图像上滑动——本质上是稀疏 Toeplitz 矩阵与拉直图像向量的乘积（im2col 展开）。
  - **PCA 降维**：对协方差矩阵做特征分解，取前 k 个最大特征值对应的特征向量——这就是"主成分"的数学定义。
  - **图像压缩**：SVD 低秩逼近——一张 1000×1000 的图，保留前 20 个奇异值，数据量从 100 万降到 4 万（压缩 25 倍），肉眼几乎看不出差别。
  - **损失函数求导**：$\frac{\partial}{\partial W} \|XW - Y\|_F^2 = 2X^T(XW - Y)$——矩阵转置和迹恒等式是手推梯度的基本工具。
- **高频题型/任务**：矩阵乘法维度推导、卷积的矩阵乘法理解、PCA 背后的特征分解推导、SVD 图像压缩的手算验证、损失函数对矩阵参数的求导。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景（各 200 字以内）：

1. **高中数学——向量与矩阵基础**：知道向量是有序数组，矩阵是数字的矩形排列。会做矩阵乘法（行×列）、会算 2×2 行列式。如果忘了，回忆一下 $(AB)_{ij} = \sum_k a_{ik}b_{kj}$ 即可——我们会在 §5 正式重述。
2. **基本微积分——偏导数概念**：理解 $\frac{\partial f}{\partial x}$ 衡量函数沿某方向的变化率。矩阵求导会在本卡中从标量求导自然推广到矩阵情况，不需要预知。
3. **图像基本概念**：知道一张灰度图是一个二维数组，彩色图是三维数组（宽×高×通道）。参考 [[图像表示]]。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

- **直觉类比 1——向量是空间中的箭头**：二维向量 $(3, 2)$ 就是从原点出发、水平走 3 步、垂直走 2 步的那个箭头。矩阵 $A$ 作用在这个箭头上，把它**拉伸、旋转、剪切**成另一个箭头。**矩阵 = 空间变换器**。
- **直觉类比 2——特征向量是"不转弯的方向"**：大多数箭头被矩阵 $A$ 作用后会改变方向。但总有那么几个特殊方向——箭头只被拉伸（或压缩），方向不变。这些方向就是**特征向量**，拉伸的倍数就是**特征值**。想象一个椭圆被拉伸：长轴和短轴上的箭头方向不变。
- **直觉类比 3——SVD 是"拆成三层"**：任何矩阵 $A$ 可拆成三块：**旋转 → 拉伸 → 再旋转**。$A = U \Sigma V^T$：$V^T$ 是一个旋转（把图转到"最合适"的方向），$\Sigma$ 沿坐标轴做纯拉伸（奇异值就是拉伸倍数），$U$ 再转回来。这就像你把一张歪的照片先转正、压扁、再转回去——中间"压扁"那步丢掉小的拉伸方向，就实现了压缩。
- **直觉类比 4——矩阵乘法与卷积**：3×3 卷积核在图像上"滑动做内积"，等价于把图像拉成一条长向量，用一个巨大的稀疏带状矩阵去乘它。每个输出像素 = 输入图像中一个 3×3 邻域的加权和——这就是"局部连接"的矩阵表达。
- **一句话直觉本质**：**矩阵是空间的线性变换器；特征向量是变换后方向不变的轴；SVD 把任意变换拆成"转-拉-转"三步；图像就是这些变换作用的对象。**

---

## 5. 正式定义、核心公式、符号解释

### 5.1 向量、矩阵与张量——CV 视角的定义

| 概念 | 数学定义 | CV 中的对应 | 形状示例 |
|:---|:---|:---|:---|
| **标量 (Scalar)** | 单个数字 $s \in \mathbb{R}$ | 单个像素值、学习率 $\eta$ | `255` |
| **向量 (Vector)** | 一维数组 $\mathbf{v} \in \mathbb{R}^n$ | 拉直后的一行/一列像素；RGB 颜色 $(R,G,B)$；特征向量 | `(3,)` 或 `(256,)` |
| **矩阵 (Matrix)** | 二维数组 $A \in \mathbb{R}^{m \times n}$ | 灰度图像 $H \times W$；卷积核 $k \times k$；权重矩阵 $W$ | `(256, 256)` |
| **张量 (Tensor)** | 三维及以上数组 | 彩色图像 $H \times W \times C$；批量图像 $B \times C \times H \times W$ | `(32, 3, 224, 224)` |

> 🧠 **CV 核心约定**：在 NumPy / PyTorch 中，图像的最常见表示是 `(H, W)`（灰度）或 `(H, W, C)`（彩色 HWC）或 `(C, H, W)`（PyTorch CHW）。向量的"方向"在代码中是 shape 的排列顺序——`(3,)` 是一维向量，`(3,1)` 是列矩阵，`(1,3)` 是行矩阵。

### 5.2 矩阵乘法——定义与 CV 本质

**定义**：$C = AB$，其中 $A \in \mathbb{R}^{m \times k}$，$B \in \mathbb{R}^{k \times n}$，则 $C \in \mathbb{R}^{m \times n}$：

$$C_{ij} = \sum_{p=1}^{k} A_{ip} \cdot B_{pj}$$

**维度铁律**：$(m \times \color{red}{k}) \cdot (\color{red}{k} \times n) = (m \times n)$——内维必须相等，外维决定结果形状。

**三种等价视角理解 $C = AB$**：

| 视角 | 公式 | CV 直觉 |
|:---|:---|:---|
| **行×列**（标准定义） | $C_{ij} = \text{row}_i(A) \cdot \text{col}_j(B)$ | 每个输出像素是输入一行与卷积核一列的内积 |
| **列的线性组合** | $C$ 的第 $j$ 列 = $A \times$ ($B$ 的第 $j$ 列) | 输出图像的每一列是输入图像的列的线性组合 |
| **行的线性组合** | $C$ 的第 $i$ 行 = ($A$ 的第 $i$ 行) $\times B$ | 输出图像的每一行是卷积核的行的线性组合 |

**CV 中的关键实例**：

```python
# 图像旋转：每个像素 (x,y) 的新位置由旋转矩阵决定
# [x']   [cosθ  -sinθ] [x]
# [y'] = [sinθ   cosθ] [y]   ← 2×2 矩阵 × 2×1 向量 = 2×1 向量

# 全连接层：输入向量 → 权重矩阵 → 输出向量
# y = W x     其中 W: (out_dim, in_dim), x: (in_dim,), y: (out_dim,)

# 批量线性变换：
# Y = X W^T   其中 X: (B, in_dim), W: (out_dim, in_dim), Y: (B, out_dim)
```

### 5.3 矩阵乘法在卷积中的本质——im2col 展开

这是理解"卷积 = 矩阵乘法"的核心桥梁。设输入图像 $X \in \mathbb{R}^{H \times W}$，卷积核 $K \in \mathbb{R}^{k \times k}$。

**im2col 操作**：把每个 $k \times k$ 滑动窗口拉直成一行，所有窗口叠成矩阵 $X_{\text{col}} \in \mathbb{R}^{(H' \times W') \times k^2}$。同时把卷积核拉直成列向量 $\mathbf{k} \in \mathbb{R}^{k^2}$。

$$\text{Output} = X_{\text{col}} \cdot \mathbf{k}$$

这就是为什么 GPU 能用高度优化的矩阵乘法（GEMM）来加速卷积——**卷积的本质是"展开后的矩阵乘法"**。

```python
import numpy as np

# 5×5 灰度图，单通道
X = np.arange(25).reshape(5, 5)
# 3×3 卷积核（Sobel 水平边缘检测核的简化版）
K = np.array([[-1, 0, 1],
              [-2, 0, 2],
              [-1, 0, 1]])

# 手工 im2col：提取每个 3×3 patch 并拉直
H, W = X.shape
k = K.shape[0]
patches = []
for i in range(H - k + 1):
    for j in range(W - k + 1):
        patch = X[i:i+k, j:j+k].flatten()  # 拉直为 9 维向量
        patches.append(patch)
X_col = np.array(patches)                  # shape: (9, 9) — 9个窗口，每个9维
k_vec = K.flatten()                        # shape: (9,)
output_vec = X_col @ k_vec                  # shape: (9,) — 矩阵乘法！
output = output_vec.reshape(H-k+1, W-k+1)   # 恢复为 3×3 输出

print(f"输入形状: {X.shape}")
print(f"im2col 矩阵形状: {X_col.shape}")
print(f"卷积核拉直: {k_vec.shape}")
print(f"矩阵乘法输出: {output_vec.shape} → 恢复为 {output.shape}")
print(f"卷积结果:\n{output}")
```

- **核心洞察**：$X_{\text{col}}$ 的每一行，就是原图中某个 3×3 邻域的所有像素。与 $\mathbf{k}$ 做内积 = 该邻域的加权和 = 该位置的卷积输出。**"滑动窗口 + 内积"等价于"矩阵乘法"**。
- **为什么重要**：PyTorch 的 `Conv2d` 底层调用 cuDNN，cuDNN 内部就是用 im2col + GEMM（通用矩阵乘）来做的。理解这一点，你才能理解卷积的参数量、计算量（FLOPs）、以及为什么 1×1 卷积就是全连接层。

### 5.4 转置、逆、迹——定义与 CV 应用

| 运算 | 定义 | 符号 | CV 核心应用 |
|:---|:---|:---|:---|
| **转置** | $(A^T)_{ij} = A_{ji}$ | $A^T$ | 梯度传播中"维度翻转"；协方差矩阵 $X^T X$；注意力中 $QK^T$ |
| **逆** | $A A^{-1} = A^{-1}A = I$ | $A^{-1}$ | 相机标定中求解内外参；仿射变换的逆变换；白化 (whitening) |
| **迹** | $\text{tr}(A) = \sum_i A_{ii}$ | $\text{tr}(A)$ | 矩阵求导恒等式；$\text{tr}(AB) = \text{tr}(BA)$ 是推导损失梯度的核心技巧 |
| **Frobenius 范数** | $\|A\|_F = \sqrt{\sum_{i,j} A_{ij}^2}$ | $\|A\|_F$ | 权重衰减正则化；矩阵逼近的误差度量 |

**转置在损失求导中的本质角色**：

考虑最简单的线性回归损失：$J(W) = \frac{1}{2}\|XW - Y\|_F^2$，其中 $X \in \mathbb{R}^{N \times d}$，$W \in \mathbb{R}^{d \times m}$，$Y \in \mathbb{R}^{N \times m}$。

对 $W$ 求梯度——展开损失：

$$J = \frac{1}{2}\text{tr}\big((XW - Y)^T (XW - Y)\big) = \frac{1}{2}\text{tr}\big(W^T X^T X W - 2W^T X^T Y + Y^T Y\big)$$

利用矩阵求导恒等式 $\frac{\partial}{\partial W} \text{tr}(W^T A W) = (A + A^T)W$ 和 $\frac{\partial}{\partial W} \text{tr}(W^T B) = B$，得：

$$\frac{\partial J}{\partial W} = X^T(XW - Y)$$

> 🔑 **关键洞察**：梯度公式中的 $X^T$ 来自链式法则的"维度匹配"——损失对 $XW-Y$ 求导是 $(N \times m)$，但 $W$ 的形状是 $(d \times m)$，中间必须经过 $X^T$（$d \times N$）把 $N$ 维压缩到 $d$ 维。**转置在反向传播中的本质作用是"维度翻转"**。

**迹技巧速查表**（这些恒等式在推导任何矩阵损失函数梯度时都用得到）：

| 恒等式 | 用途 |
|:---|:---|
| $\text{tr}(AB) = \text{tr}(BA)$ | 循环置换——把求导变量移到最右 |
| $\text{tr}(A) = \text{tr}(A^T)$ | 迹不随转置改变 |
| $\frac{\partial}{\partial W} \text{tr}(W^T A) = A$ | 线性项的矩阵求导 |
| $\frac{\partial}{\partial W} \text{tr}(W^T A W) = (A + A^T)W$ | 二次型的矩阵求导 |

### 5.5 特征值与特征向量——几何意义

**定义**：对方阵 $A \in \mathbb{R}^{n \times n}$，若存在非零向量 $\mathbf{v} \in \mathbb{R}^n$ 和标量 $\lambda$ 满足：

$$A\mathbf{v} = \lambda \mathbf{v}$$

则 $\lambda$ 是 $A$ 的**特征值**，$\mathbf{v}$ 是对应的**特征向量**。

**几何直觉**：矩阵 $A$ 作用在大多数向量上会改变其方向。但特征向量是特殊方向——$A$ 作用后只做**纯拉伸**（拉伸倍数为 $\lambda$），方向不变。$\lambda > 1$ 拉伸，$0 < \lambda < 1$ 压缩，$\lambda < 0$ 翻转方向。

**对称矩阵的特殊性**：若 $A = A^T$（如协方差矩阵），则所有特征值都是实数，且不同特征值对应的特征向量互相正交。这为 PCA 提供了数学保证——主成分方向是正交的。

**与 PCA 的直接联系（前置知识）**：

给定数据中心化后的矩阵 $X \in \mathbb{R}^{N \times d}$，协方差矩阵为 $C = \frac{1}{N-1} X^T X \in \mathbb{R}^{d \times d}$。

- **第 1 主成分** = $C$ 的**最大特征值对应的特征向量**——数据方差最大的方向
- **第 k 主成分** = $C$ 的第 k 大特征值对应的特征向量
- **"解释方差比例"** = $\lambda_k / \sum_i \lambda_i$——该方向"承载了多少信息"

> 🧠 **一句话**：PCA 就是"对协方差矩阵做特征分解，取前 k 个最大特征向量作为新的坐标轴"。

```python
import numpy as np

# 生成二维高斯数据，沿 (1, 0.5) 方向方差最大
np.random.seed(42)
X = np.random.randn(200, 2) @ np.array([[3, 1], [0, 1]])  # 200×2

# 中心化
X_centered = X - X.mean(axis=0)

# 协方差矩阵 (2×2)
C = (X_centered.T @ X_centered) / (X.shape[0] - 1)
print(f"协方差矩阵 C:\n{C}")

# 特征分解
eigenvalues, eigenvectors = np.linalg.eigh(C)  # eigh 用于对称矩阵
# 按特征值降序排列
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

print(f"特征值: λ₁={eigenvalues[0]:.4f}, λ₂={eigenvalues[1]:.4f}")
print(f"第一主成分方向: {eigenvectors[:, 0]}")
print(f"第二主成分方向: {eigenvectors[:, 1]}")
print(f"解释方差比例: λ₁={eigenvalues[0]/eigenvalues.sum()*100:.1f}%, "
      f"λ₂={eigenvalues[1]/eigenvalues.sum()*100:.1f}%")
```

### 5.6 SVD（奇异值分解）——形式定义

**定义**：对任意矩阵 $A \in \mathbb{R}^{m \times n}$（不需要是方阵！），存在分解：

$$A = U \Sigma V^T$$

其中：
- $U \in \mathbb{R}^{m \times m}$：**左奇异向量**矩阵，列正交（$U^T U = I$）
- $\Sigma \in \mathbb{R}^{m \times n}$：**对角矩阵**，对角元 $\sigma_1 \geq \sigma_2 \geq \dots \geq \sigma_r > 0$ 称为**奇异值**
- $V \in \mathbb{R}^{n \times n}$：**右奇异向量**矩阵，列正交（$V^T V = I$）
- $r = \text{rank}(A)$：矩阵的秩（非零奇异值的个数）

**与特征分解的关系**：
- $A^T A = V \Sigma^T \Sigma V^T = V \Sigma^2 V^T$ → $V$ 的列是 $A^T A$ 的特征向量，$\sigma_i^2$ 是 $A^T A$ 的特征值
- $A A^T = U \Sigma \Sigma^T U^T = U \Sigma^2 U^T$ → $U$ 的列是 $A A^T$ 的特征向量

**几何直觉（三层分解）**：
$$A = \underbrace{U}_{\text{旋转/反射}} \cdot \underbrace{\Sigma}_{\text{拉伸/压缩}} \cdot \underbrace{V^T}_{\text{旋转/反射}}$$

任意线性变换 $A$ = 先旋转 → 沿坐标轴拉伸 → 再旋转。

**SVD 的秩-k 逼近（Eckart-Young 定理）**：

$$A_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$

$A_k$ 是秩为 $k$ 的矩阵中**最接近 $A$ 的矩阵**（在 Frobenius 范数意义下）。这就是 SVD 图像压缩的数学基础——保留前 $k$ 个最大的奇异值/向量，丢掉小的。

---

## 6. 推导思路和思想来源

- **最初困难**：高维数据难以直观理解和高效存储。一张 256×256 的图有 65536 个数字——它们之间显然有大量冗余（相邻像素相似），如何提取"本质结构"？
- **直接方法局限**：单独看每个像素值是没法发现结构的——就像只看一个单词无法理解一篇文章。需要研究像素之间的**协方差关系**（$X^T X$），这自然引出了矩阵的谱分析。
- **关键"转念"**：
  - **Cayley-Hamilton/谱定理**（19 世纪）：对称矩阵可被正交对角化 $A = Q\Lambda Q^T$——这是 PCA 的理论基石。
  - **Eckart-Young 定理**（1936）：SVD 的秩-k 截断给出最优低秩逼近——这是所有基于 SVD 的压缩/降噪方法的理论保证。
  - **数值线性代数**（20 世纪中后期）：Golub-Reinsch SVD 算法使得大规模矩阵的奇异值分解在计算机上可行——这才让 PCA 和 SVD 从数学定理变成工程工具。
- **推导主线**：图像 = 矩阵 → 矩阵的谱（特征值/奇异值）揭示了其内在结构 → 保留大特征值/奇异值的分量 = 保留主要结构、丢弃噪声 → PCA 降维、SVD 压缩、协方差分析等全部是这条线上的应用。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子——手算 2×2 矩阵的 SVD 分解

> **场景**：对矩阵 $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ 做完整的 SVD 分解。

**Step 1：计算 $A^T A$**

$$A^T A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} = \begin{bmatrix} 5 & 4 \\ 4 & 5 \end{bmatrix}$$

**Step 2：求 $A^T A$ 的特征值和特征向量（得到 $V$ 和 $\Sigma$）**

特征方程：$\det(A^T A - \lambda I) = \begin{vmatrix} 5-\lambda & 4 \\ 4 & 5-\lambda \end{vmatrix} = (5-\lambda)^2 - 16 = \lambda^2 - 10\lambda + 9 = (\lambda - 9)(\lambda - 1) = 0$

→ $\lambda_1 = 9$，$\lambda_2 = 1$

奇异值：$\sigma_1 = \sqrt{9} = 3$，$\sigma_2 = \sqrt{1} = 1$

→ $\Sigma = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}$

求 $\lambda_1 = 9$ 的特征向量：解 $(A^T A - 9I)\mathbf{v} = 0$

$$\begin{bmatrix} -4 & 4 \\ 4 & -4 \end{bmatrix} \begin{bmatrix} v_1 \\ v_2 \end{bmatrix} = 0 \quad \Rightarrow \quad v_1 = v_2$$

归一化：$\mathbf{v}_1 = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix}$

求 $\lambda_2 = 1$ 的特征向量：

$$\begin{bmatrix} 4 & 4 \\ 4 & 4 \end{bmatrix} \begin{bmatrix} v_1 \\ v_2 \end{bmatrix} = 0 \quad \Rightarrow \quad v_1 = -v_2$$

归一化：$\mathbf{v}_2 = \begin{bmatrix} 1/\sqrt{2} \\ -1/\sqrt{2} \end{bmatrix}$

→ $V = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix}$

**Step 3：计算 $U$ 的各列**

$\mathbf{u}_1 = \frac{A\mathbf{v}_1}{\sigma_1} = \frac{1}{3} \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix} = \frac{1}{3} \begin{bmatrix} 3/\sqrt{2} \\ 3/\sqrt{2} \end{bmatrix} = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix}$

$\mathbf{u}_2 = \frac{A\mathbf{v}_2}{\sigma_2} = \frac{1}{1} \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} \\ -1/\sqrt{2} \end{bmatrix} = \begin{bmatrix} 1/\sqrt{2} \\ -1/\sqrt{2} \end{bmatrix}$

→ $U = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix}$（恰好 $U = V$，因为 $A$ 是对称正定矩阵）

**Step 4：验证 $A = U \Sigma V^T$**

$$U \Sigma V^T = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix}$$

$$= \begin{bmatrix} 3/\sqrt{2} & 1/\sqrt{2} \\ 3/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} = \begin{bmatrix} 3/2 + 1/2 & 3/2 - 1/2 \\ 3/2 - 1/2 & 3/2 + 1/2 \end{bmatrix} = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} = A \quad \checkmark$$

> 📝 **观察**：对对称矩阵 $A = A^T$，SVD 退化为特征分解 $A = Q \Lambda Q^T$（$U=V=Q$, $\Sigma=\Lambda$）。对一般非对称矩阵，$U \neq V$。

**秩-1 逼近验证**：

$$A_1 = \sigma_1 \mathbf{u}_1 \mathbf{v}_1^T = 3 \cdot \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \end{bmatrix} = 3 \cdot \begin{bmatrix} 1/2 & 1/2 \\ 1/2 & 1/2 \end{bmatrix} = \begin{bmatrix} 1.5 & 1.5 \\ 1.5 & 1.5 \end{bmatrix}$$

逼近误差：$\|A - A_1\|_F = \sigma_2 = 1$（恰好等于被丢弃的奇异值！）。

### 例子 2：中等例子——NumPy 实现 SVD 图像压缩

```python
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --- 读入灰度图并转为 float64 ---
# 用随机生成的"图像"演示（实际使用时替换为 cv2.imread）
np.random.seed(42)
H, W = 200, 200
# 模拟一张有结构的图：低秩背景 + 噪声
U_true = np.random.randn(H, 5)
V_true = np.random.randn(5, W)
img = U_true @ V_true + 0.02 * np.random.randn(H, W)  # 秩≈5 + 噪声

# --- SVD 分解 ---
U, s, Vt = np.linalg.svd(img, full_matrices=False)
# U: (H, K), s: (K,), Vt: (K, W)  其中 K = min(H, W)

print(f"图像形状: {img.shape}")
print(f"总像素数: {img.size:,}")
print(f"奇异值数量: {len(s)}")
print(f"前10个奇异值: {np.round(s[:10], 3)}")

# --- 秩-k 逼近重建 ---
def svd_compress(U, s, Vt, k):
    """用前 k 个奇异值重建图像"""
    return U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]

# 不同压缩率对比
k_values = [1, 3, 5, 10, 20, 50]
fig, axes = plt.subplots(2, 3, figsize=(14, 9))

for ax, k in zip(axes.flat, k_values):
    recon = svd_compress(U, s, Vt, k)
    storage = k * (H + W + 1)  # U + Σ + V 的参数数
    ratio = img.size / storage
    error = np.linalg.norm(img - recon, 'fro') / np.linalg.norm(img, 'fro')

    ax.imshow(recon, cmap='gray')
    ax.set_title(f'k={k}  压缩比={ratio:.1f}:1  误差={error:.3f}', fontsize=10)
    ax.axis('off')

plt.suptitle('SVD 图像压缩：不同秩-k 逼近的视觉效果', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

# --- 奇异值衰减曲线 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))

ax1.plot(s, 'b-', linewidth=0.8, alpha=0.7)
ax1.set_xlabel('索引 i')
ax1.set_ylabel('奇异值 σᵢ')
ax1.set_title('奇异值衰减（线性坐标）')
ax1.grid(True, alpha=0.3)

ax2.semilogy(s, 'r-', linewidth=0.8, alpha=0.7)
ax2.set_xlabel('索引 i')
ax2.set_ylabel('奇异值 σᵢ (对数坐标)')
ax2.set_title('奇异值衰减（对数坐标）')
ax2.grid(True, alpha=0.3)

plt.suptitle('奇异值谱：快速衰减 → 低秩结构 → 可压缩', fontsize=14)
plt.tight_layout()
plt.show()

print(f"\n--- 存储分析 ---")
print(f"原始存储: {img.size:,} 个数值")
for k in [5, 10, 20, 50]:
    storage_k = k * (H + W + 1)
    print(f"k={k:3d}: {storage_k:,} 个数值 (压缩 {img.size/storage_k:.1f}:1)")
```

> 💡 **关键观察**：奇异值衰减越快 → 图像的低秩性越强 → 压缩效果越好。自然图像通常有较慢的衰减（包含高频纹理），但前 5-10% 的奇异值就已经保留了大部分视觉信息。

### 例子 3：实际应用例子——用迹技巧推导 Softmax 损失对权重矩阵的梯度

> **场景**：多分类线性模型中，损失函数 $J(W) = -\frac{1}{N}\sum_i \log \frac{e^{\mathbf{w}_{y_i}^T \mathbf{x}_i}}{\sum_j e^{\mathbf{w}_j^T \mathbf{x}_i}}$。这里不推导完整 Softmax（那是另一张卡的活），而是展示其中关键的**矩阵/迹求导步骤**。

考虑简化版的平方损失 + 权重衰减：

$$J(W) = \frac{1}{2}\|XW - Y\|_F^2 + \frac{\lambda}{2}\|W\|_F^2$$

其中 $X \in \mathbb{R}^{N \times d}$，$W \in \mathbb{R}^{d \times C}$，$Y \in \mathbb{R}^{N \times C}$。

**用迹技巧求 $\frac{\partial J}{\partial W}$**：

$$\begin{aligned}
J &= \frac{1}{2}\text{tr}\big((XW-Y)^T(XW-Y)\big) + \frac{\lambda}{2}\text{tr}(W^T W) \\
  &= \frac{1}{2}\text{tr}\big(W^T X^T X W - 2W^T X^T Y + Y^T Y\big) + \frac{\lambda}{2}\text{tr}(W^T W)
\end{aligned}$$

对 $W$ 求导（使用 §5.4 的恒等式）：

$$\frac{\partial J}{\partial W} = \frac{1}{2}\big((X^T X + X^T X)W - 2X^T Y\big) + \frac{\lambda}{2}(2W) = X^T X W - X^T Y + \lambda W$$

$$= X^T(XW - Y) + \lambda W$$

**代码验证——数值梯度检查**：

```python
import numpy as np

# --- 随机数据和参数 ---
N, d, C = 50, 10, 3
X = np.random.randn(N, d)
W = np.random.randn(d, C)
Y = np.random.randn(N, C)
lam = 0.01

# --- 解析梯度 ---
def loss_and_grad(W, X, Y, lam):
    diff = X @ W - Y                            # (N, C)
    loss = 0.5 * np.sum(diff**2) + 0.5 * lam * np.sum(W**2)
    grad = X.T @ diff + lam * W                 # (d, C) — 解析梯度
    return loss, grad

loss, grad_analytic = loss_and_grad(W, X, Y, lam)

# --- 数值梯度（有限差分）---
eps = 1e-6
grad_numeric = np.zeros_like(W)
for i in range(d):
    for j in range(C):
        W_plus = W.copy(); W_plus[i, j] += eps
        W_minus = W.copy(); W_minus[i, j] -= eps
        loss_plus, _ = loss_and_grad(W_plus, X, Y, lam)
        loss_minus, _ = loss_and_grad(W_minus, X, Y, lam)
        grad_numeric[i, j] = (loss_plus - loss_minus) / (2 * eps)

# --- 比较 ---
diff = np.abs(grad_analytic - grad_numeric)
print(f"解析梯度 vs 数值梯度:")
print(f"  最大绝对差异: {diff.max():.2e}")
print(f"  平均绝对差异: {diff.mean():.2e}")
print(f"  相对误差:     {diff.max() / (np.abs(grad_analytic).max() + 1e-8):.2e}")
print(f"  ✅ 梯度正确!" if diff.max() < 1e-4 else "  ❌ 梯度有误!")
```

> 🔑 **核心收获**：
> - $X^T$ 的出现是因为链式法则中的"维度翻转"——损失对 $XW-Y$（形状 $N \times C$）求导后，需要乘以 $X^T$（$d \times N$）才能收缩到 $W$ 的形状 $(d \times C)$。
> - 权重衰减项 $\lambda W$ 来自 $\frac{\partial}{\partial W} \frac{\lambda}{2}\|W\|_F^2 = \lambda W$（矩阵版的 $\frac{d}{dx}\frac{\lambda}{2}x^2 = \lambda x$）。
> - 迹技巧让矩阵求导变得像标量求导一样机械——不需要记住复杂的矩阵求导表，只需要展开 $\|\cdot\|_F^2$ 为迹的形式。

---

## 8. 常见误区和易混概念

### 误区 1："矩阵乘法就是行列对应乘加，没什么几何意义"

- **错误直觉**："$(AB)_{ij} = \sum_k a_{ik}b_{kj}$，就是个计算规则。"
- **为什么错**：这个"计算规则"只是表象。矩阵乘法的**本质**是线性变换的复合——$A$ 和 $B$ 各代表一个空间变换，$AB$ 代表"先做 B 再做 A"。不理解这一点，你就无法理解为什么卷积是矩阵乘法、为什么 PCA 的投影矩阵是特征向量拼成的。
- **正确理解**：看到 $C = AB$，脑子里应该出现：**B 的列被 A 重新线性组合**，或者 **A 的行被 B 重新线性组合**。这是 §5.2 "三种等价视角"的几何实质。

### 误区 2："特征值和奇异值是一回事"

- **错误直觉**："SVD 的 σ 不就是特征值开根号嘛，那直接用特征分解不就行了？"
- **为什么错**：特征分解只对方阵有意义，且只有可对角化的方阵才有完整的特征分解。SVD 对**任意矩阵**（矩形！非方！）都成立——这才是它的威力所在。图像的协方差矩阵是方的，但图像本身不是方的（256×256 是方的，但 1920×1080 不是方阵）。
- **正确理解**：$A^T A$ 的特征值 = $\sigma_i^2$，$V$ 的列 = $A^T A$ 的特征向量。但 $A$ 本身的特征值（如果 $A$ 是方阵）和 $\sigma_i$ 没有简单的相等关系。**SVD 是特征分解的"普适推广"——无需方阵假设。**

### 误区 3："$\frac{\partial J}{\partial W}$ 的形状和 $W$ 一样，所以标量求导规则直接套"

- **错误直觉**："既然形状一样，那 $\frac{\partial}{\partial W}\|W\|_F^2 = 2W$ 应该对吧……"
- **为什么错**：这个结果虽然对，但推理过程不扎实。矩阵求导中容易出现维度不匹配的公式——比如想当然写 $\frac{\partial}{\partial W} XW = X$ 而实际是 $\frac{\partial}{\partial W} \mathbf{a}^T W \mathbf{b} = \mathbf{a}\mathbf{b}^T$（外积！不是内积！）。靠谱的做法永远是：展开成迹 → 用迹恒等式 → 匹配维度。
- **正确理解**：矩阵求导 = **标量对矩阵的梯度**，结果形状与矩阵相同。但链式法则中的"中间项"可能带来转置——永远从迹恒等式出发，或者用维度分析（检查输出形状与输入形状是否匹配）。

### 误区 4："SVD 压缩就是扔掉小奇异值，类似于 JPEG 的高频丢弃"

- **错误直觉**："都是丢高频嘛。"
- **为什么错**：JPEG 用的是 DCT（离散余弦变换），在固定分块（8×8）上做，丢掉的是 DCT 高频系数。SVD 是**全局最优低秩逼近**——它找的是整个矩阵层面的最优，不依赖于分块。SVD 在图像压缩中不常用（不是因为它不好，而是因为它需要存储 $U$ 和 $V$ 矩阵，开销比 JPEG 大），但它是很多高级方法（如鲁棒 PCA、矩阵补全）的理论基础。
- **正确理解**：SVD = 全局低秩（整个图的"主题"），DCT/JPEG = 局部频域（8×8 块的高频细节）。两者思路完全不同，不能混为一谈。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | CV 典型场景 |
|:---|:---|:---|:---|
| 特征分解 vs SVD | 方阵的谱分解 vs 任意矩阵的谱分解 | 特征分解需方阵；SVD 无此限制 | 协方差 PCA vs 图像直接压缩 |
| 矩阵乘 vs 逐元素乘 | $(AB)_{ij} = \sum_k A_{ik}B_{kj}$ vs $A \odot B$ | 一个改变空间结构，一个只做像素级缩放 | 全连接层 vs 注意力掩膜 |
| 转置 vs 逆 | $A^T$ 行列互换 vs $A^{-1}$ 乘法逆元 | 转置永远存在；逆不一定存在（需满秩） | 梯度传播 vs 相机标定 |
| 迹 vs 行列式 | 对角元之和 vs 空间体积缩放比 | $\text{tr}(A) = \sum\lambda_i$；$\det(A) = \prod\lambda_i$ | 矩阵求导 vs 坐标变换雅可比 |
| $\|\cdot\|_F$ vs $\|\cdot\|_2$ | 所有元素的平方和开根 vs 最大奇异值 | F 范数对所有元素平等；2 范数只关注最大拉伸 | 权重衰减 vs 谱归一化 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[图像表示]]：图像 = $H \times W \times C$ 张量——这是所有矩阵运算的作用对象。
- 高中数学（向量、矩阵、行列式的基本运算）：本卡在 §5 对核心运算都给了正式定义，但基本熟练度需要前置。

### 下游延伸
- [[特征分解CV]]：本卡的 §5.5-5.6 是前序——特征分解卡将深入 PCA、协方差矩阵分析、特征脸等具体 CV 应用。
- [[几何变换CV]]：旋转/缩放/仿射变换矩阵的定义与应用——本卡的矩阵乘法是基础。
- [[梯度下降CV]]：损失函数对参数的梯度计算——本卡 §5.4 和 §7 例 3 的迹技巧直接用于梯度推导。
- [[卷积神经网络CNN]]：卷积 = im2col + 矩阵乘法——本卡 §5.3 已经给出了这个本质理解。
- [[SVDCV]]：SVD 在 CV 中的完整应用（图像压缩、去噪、背景建模）——本卡 §5.6 是前序。

### 横向关联
- NumPy矩阵CV ↔ 本知识点：NumPy 中矩阵运算的 API 对应（`@`, `np.dot`, `np.linalg.svd`, `np.linalg.eigh` 等）。
- 向量化CV ↔ 本知识点：如何用矩阵运算替换 for 循环，本质就是利用"矩阵乘法 = 批量内积"。
- 线性变换CV ↔ 本知识点：更侧重变换的几何性质（行列式=面积缩放比、特征向量=不变方向的直观动画）。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚矩阵乘法 $C = AB$ 的"三种等价视角"是什么。
- [ ] 2. 用直觉语言解释为什么卷积可以用矩阵乘法（im2col）来实现。
- [ ] 3. 写出 $X^T X W - X^T Y + \lambda W$ 是哪个损失函数的梯度，并标识每一项的来源。
- [ ] 4. 用自己的话讲特征向量的几何定义：$A\mathbf{v} = \lambda \mathbf{v}$ 是什么意思。
- [ ] 5. 解释 PCA"第一主成分"在协方差矩阵的数学结构中对应什么。
- [ ] 6. 写出 SVD 的三层分解 $A = U \Sigma V^T$ 中每个矩阵的几何含义。
- [ ] 7. 默写 2×2 矩阵 $A = \begin{bmatrix}2&1\\1&2\end{bmatrix}$ 的完整 SVD（$\Sigma, U, V$ 的数值）。
- [ ] 8. 解释为什么 SVD 可以用于图像压缩——丢掉小奇异值为什么"视觉损失小"？
- [ ] 9. 写出迹恒等式 $\text{tr}(AB) = \text{tr}(BA)$ 并解释为什么它对矩阵求导至关重要。
- [ ] 10. 用维度分析解释为什么 $\frac{\partial}{\partial W} \frac{1}{2}\|XW-Y\|_F^2 = X^T(XW-Y)$ 中必须有 $X^T$。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
|:---|:---|:---|:---|
| 1 | 概念辨析 | 基础 | 矩阵乘法的维度铁律 |
| 2 | 计算 | 基础 | 2×2 SVD 手算（按步骤给分） |
| 3 | 条件判断 | 中等 | im2col 维度和卷积参数关系 |
| 4 | 综合 | 中等 | SVD 压缩的存储分析 |
| 5 | 开放 | 较难 | 设计使用迹技巧推导一个新损失函数的梯度 |

---
### 题目与解析

#### 题1：设 $X \in \mathbb{R}^{32 \times 784}$，$W \in \mathbb{R}^{784 \times 10}$。$Y = XW$ 的形状是什么？$X^T Y$ 的形状是什么？（单选）
A. $(32, 10)$ 和 $(784, 10)$
B. $(32, 10)$ 和 $(32, 32)$
C. $(10, 32)$ 和 $(784, 10)$
D. $(32, 10)$ 和 $(10, 784)$

> [!question]- 答案A。$XW$: $(32 \times \color{red}{784}) \cdot (\color{red}{784} \times 10) = (32, 10)$。$X^T Y$: $(\color{red}{784} \times 32) \cdot (32 \times 10) = (784, 10)$。维度铁律是 CV 中 debug shape mismatch 的最基础技能。`#自测题/基础`

#### 题2：对矩阵 $A = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}$ 求 SVD 分解。写出 $\Sigma$、$U$、$V$ 并验证 $A = U\Sigma V^T$。

> [!question]- 答案解析
> - $A^T A = A^2 = \begin{bmatrix}9&0\\0&1\end{bmatrix}$，特征值 $\lambda_1=9,\lambda_2=1$ → $\sigma_1=3,\sigma_2=1$ → $\Sigma = \begin{bmatrix}3&0\\0&1\end{bmatrix}$
> - $A^T A$ 特征向量：$\mathbf{v}_1=[1,0]^T$（对应 λ=9），$\mathbf{v}_2=[0,1]^T$（对应 λ=1）→ $V = I$
> - $\mathbf{u}_1 = A\mathbf{v}_1/\sigma_1 = [3,0]^T/3 = [1,0]^T$，$\mathbf{u}_2 = A\mathbf{v}_2/\sigma_2 = [0,1]^T/1 = [0,1]^T$ → $U = I$
> - 验证：$U\Sigma V^T = I \cdot \Sigma \cdot I = \Sigma = A$。对角矩阵的 SVD 就是它自己——非常自然的结论。`#自测题/基础`

#### 题3：输入图像 $64 \times 64$，卷积核 $3 \times 3$，stride=1, padding=0。im2col 展开后的矩阵 $X_{\text{col}}$ 形状是什么？卷积核拉直后长度是多少？

> [!question]- 答案解析
> - 输出尺寸：$(64-3+1) \times (64-3+1) = 62 \times 62 = 3844$ 个滑动窗口
> - 每个窗口 $3 \times 3 = 9$ 个像素
> - $X_{\text{col}}$ 形状：$(3844, 9)$ — 3844 行（每行一个 patch），9 列（patch 内 9 个像素）
> - 卷积核拉直长度：$9$
> - 矩阵乘法 $(3844, 9) \times (9,) = (3844,)$ → reshape → $(62, 62)$
> - **常见错误**：把 $X_{\text{col}}$ 写成 $(9, 3844)$——行数=窗口数，列数=patch 像素数。`#自测题/中等`

#### 题4：一张 $512 \times 512$ 灰度图，用 SVD 保留前 $k$ 个奇异值。推导存储 $U_k \Sigma_k V_k^T$ 所需的数字个数，并计算 $k=50$ 时的压缩比。

> [!question]- 答案解析
> - 全 SVD 参数：$U: (512, 512)$ + $\Sigma$ 对角: $512$ + $V^T: (512, 512)$ = $512^2 + 512 + 512^2 \approx 524,800$
> - 秩-k 截断：$U_k: (512, k)$ + $\Sigma_k$: $k$ + $V_k^T: (k, 512)$ = $512k + k + 512k = 1025k$
> - $k=50$：存储 $1025 \times 50 = 51,250$ 个数字
> - 原始：$512^2 = 262,144$ 个像素
> - 压缩比：$262,144 / 51,250 \approx 5.1:1$
> - **注意**：实际 SVD 压缩因需存储浮点（而非 uint8）和 $U,V$ 矩阵，文件大小可能不比 PNG 小。但**原理上**它揭示了图像的低秩结构——这是鲁棒 PCA、推荐系统中矩阵分解的基础思想。`#自测题/中等`

#### 题5：多标签分类中使用损失函数 $J(W) = \frac{1}{2}\|XW - Y\|_F^2 + \lambda \|W\|_F^2$。请用迹技巧写出从 $J$ 到 $\frac{\partial J}{\partial W}$ 的完整推导，并设计一个数值梯度检查方案。

> [!question]- 答案解析
> - 推导：(1) $J = \frac{1}{2}\text{tr}\big((XW-Y)^T(XW-Y)\big) + \frac{\lambda}{2}\text{tr}(W^T W)$；(2) 展开：$\frac{1}{2}\text{tr}(W^T X^T X W - 2W^T X^T Y + Y^T Y) + \frac{\lambda}{2}\text{tr}(W^T W)$；(3) 逐项求导：$\frac{\partial}{\partial W}\text{tr}(W^T X^T X W) = (X^T X + X^T X)W = 2X^T X W$，$\frac{\partial}{\partial W}\text{tr}(W^T X^T Y) = X^T Y$，$\frac{\partial}{\partial W}\text{tr}(W^T W) = 2W$；(4) 合并：$\frac{\partial J}{\partial W} = X^T X W - X^T Y + \lambda W = X^T(XW-Y) + \lambda W$。
> - 数值检查方案：(a) 随机初始化 $X, W, Y$；(b) 用解析公式算梯度；(c) 对 $W$ 的每个元素做 $\pm \epsilon$ 扰动，用 $\frac{J(W+\epsilon)-J(W-\epsilon)}{2\epsilon}$ 近似偏导；(d) 比较解析和数值梯度的相对误差，$<10^{-6}$ 即通过。`#自测题/较难`

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：



### 我的推导复现
> 不看上文，尝试手算 $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ 的完整 SVD 分解：



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
- **关联已有笔记**：`[[图像表示]]` `[[几何变换CV]]` `[[特征分解CV]]` `[[SVDCV]]` `[[梯度下降CV]]` `NumPy矩阵CV` `向量化CV` `线性变换CV` `[[卷积神经网络CNN]]`
- **建议标签**：`#学习` `#计算机视觉` `#线性代数` `#数学基础` `#矩阵运算` `#SVD` `#特征值`
- **拆分建议**：本卡聚焦线性代数基础概念与 CV 映射关系，内容完整不拆分。若需更深入的纯数学推导（如 Cayley-Hamilton 定理、Jordan 标准型、广义特征值问题），建议新建「矩阵分析进阶」卡——但 CV 视角下本卡覆盖的内容已足够支撑后续全部学习。
- **Anki 导入备注**：anki_deck 已设为 `05-计算机视觉::01-底层基石`，建议将 §10 闭卷复现任务和 §11 自测题转化为 Anki 卡片；每个核心公式（$A = U\Sigma V^T$、$\frac{\partial J}{\partial W} = X^T(XW-Y)$、im2col 维度关系）单独制卡。

---
---

## 学完后可以完成

- 完成卡内自测题与闭卷复现（矩阵运算/特征分解）

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
