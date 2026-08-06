---
type: study
course: "05-计算机视觉"
topic: "奇异值分解 (SVD)"
created: 2026-08-06
status: planned
difficulty: intermediate
concept: ["SVD", "奇异值", "低秩近似", "图像压缩", "伪逆"]
prerequisites: ["线性代数基础CV", "特征分解CV"]
related: ["傅里叶变换CV", "图像表示"]
upstream: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/线性代数基础CV]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/特征分解CV]]"]
flow: knowledge
stage_moc: "[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/🏗️ 第一阶段：底层基石]]"
kind: concept
source: "《Mathematics for Machine Learning》Ch.4; Szeliski Ch.3"
tags: [学习, 计算机视觉, 线性代数, SVD]
---

# 奇异值分解 (Singular Value Decomposition, SVD)

> 所属模块：[[02-Knowledge/🧠 学习系统/05-计算机视觉/🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/🏗️ 第一阶段：底层基石|第一阶段：底层基石]]
> 建议先看：[[线性代数基础CV]]、[[特征分解CV]]

---

## 0. 类别：A 类核心概念

SVD 是"线性代数的瑞士军刀"——图像压缩、PCA、最小二乘、伪逆、推荐系统、LoRA 微调，全部离不开它。

---

## 1. 直觉：矩阵的"三层分解"

任意矩阵 $\mathbf{A}$ 可拆解为三个部分：

$$\mathbf{A}_{m \times n} = \mathbf{U}_{m \times m} \mathbf{\Sigma}_{m \times n} \mathbf{V}_{n \times n}^T$$

| 矩阵 | 含义 | 可视化 |
|:---|:---|:---|
| $\mathbf{U}$ | **左奇异向量**：$\mathbf{A}\mathbf{A}^T$ 的特征向量（列空间的正交基） | 描述"输出模式" |
| $\mathbf{\Sigma}$ | **奇异值**：$\sqrt{\lambda(\mathbf{A}^T\mathbf{A})}$，非负对角 | 描述"模式强度" |
| $\mathbf{V}^T$ | **右奇异向量**：$\mathbf{A}^T\mathbf{A}$ 的特征向量（行空间的正交基） | 描述"输入模式" |

> **一句话本质**：SVD 把矩阵分解为"输入方向 × 缩放因子 × 输出方向"的加权和。$\mathbf{A} = \sum_{i=1}^r \sigma_i \mathbf{u}_i \mathbf{v}_i^T$（秩-1 矩阵之和）。

---

## 2. 与特征分解的关系

| 特征分解 | SVD |
|:---|:---|
| 仅对方阵 | **任意矩阵**（矩形也行） |
| $\mathbf{A} = \mathbf{V}\mathbf{\Lambda}\mathbf{V}^{-1}$ | $\mathbf{A} = \mathbf{U}\mathbf{\Sigma}\mathbf{V}^T$ |
| 需可对角化 | **始终存在** |
| 特征值可正可负可复数 | 奇异值**始终 ≥ 0** |

实际上，$\mathbf{A}^T\mathbf{A}$ 的特征值 = $\sigma_i^2$，$\mathbf{A}^T\mathbf{A}$ 的特征向量 = $\mathbf{V}$ 的列。

---

## 3. 低秩近似：SVD 的核心威力

取前 $k$ 个最大的奇异值及对应的奇异向量：

$$\mathbf{A}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$

**Eckart-Young 定理**：$\mathbf{A}_k$ 是 $\mathbf{A}$ 在所有秩-$k$ 矩阵中的**最优近似**（Frobenius 范数最小）。

### 图像压缩示例

```python
import numpy as np
import matplotlib.pyplot as plt

def svd_compress(img_gray, k):
    """用前 k 个奇异值压缩灰度图"""
    U, S, Vt = np.linalg.svd(img_gray, full_matrices=False)
    approx = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
    compression_ratio = (img_gray.size) / (k * (U.shape[0] + Vt.shape[1] + 1))
    return np.clip(approx, 0, 255), compression_ratio

# 示例：512×512 图像
# k=10:  压缩比 ~50:1, 可辨认大致轮廓但细节模糊
# k=50:  压缩比 ~10:1, 细节恢复良好
# k=100: 压缩比 ~5:1,  肉眼几乎无差
# 一张图可以被压缩 100 倍而肉眼无差——这就是 SVD 的魔力
```

**典型压缩效果**：

| k | 压缩比 | 视觉效果 |
|:---|:---:|:---|
| 5 | ~100:1 | 仅可见大块色块 |
| 20 | ~25:1 | 轮廓清晰，细节模糊 |
| 50 | ~10:1 | 细节基本恢复 |
| 100 | ~5:1 | 与原图肉眼无差 |

---

## 4. CV 中的典型应用

| 应用 | SVD 角色 | 说明 |
|:---|:---|:---|
| **图像压缩** | 低秩近似 | 保留前 k 个奇异值 |
| **图像去噪** | 低秩近似 | 噪声对应小奇异值，丢弃即可 |
| **PCA** | $\mathbf{V}$ 即主成分 | SVD 是 PCA 的数值稳定实现 |
| **最小二乘** | 伪逆 $\mathbf{A}^+ = \mathbf{V}\mathbf{\Sigma}^+\mathbf{U}^T$ | 过定/欠定方程的通解 |
| **LoRA 微调** | 低秩分解 | 权重更新 $\Delta W = BA$，灵感来自 SVD |
| **相机标定** | DLT 算法 | 最小奇异值对应的右奇异向量是解 |

---

## 5. 条件变式：截断 vs 完整 SVD

| 变体 | 矩阵尺寸 | 用途 |
|:---|:---|:---|
| **完整 SVD** | $\mathbf{U}_{m \times m}, \mathbf{\Sigma}_{m \times n}, \mathbf{V}_{n \times n}$ | 理论分析 |
| **经济 SVD** | $\mathbf{U}_{m \times r}, \mathbf{\Sigma}_{r \times r}, \mathbf{V}_{n \times r}^T$（$r = \min(m,n)$） | 节省内存 |
| **截断 SVD** | 只保留前 $k$ 个奇异值和向量 | 压缩/降维 |
| **随机化 SVD** | 近似计算 | 大规模矩阵 |

---

## 6. 常见误区

- ❌ "SVD 和特征分解是一回事" — SVD 用于任意矩阵，奇异值始终 ≥0
- ❌ "奇异值越多越好" — 噪声对应的小奇异值反而有害
- ❌ "SVD 只是数学工具，深度学习不需要" — LoRA、权重矩阵初始化、模型压缩都用到 SVD

---

## 🧪 自测题

1. **(基础)** SVD 分解得到的三个矩阵 $\mathbf{U}, \mathbf{\Sigma}, \mathbf{V}^T$ 各自的物理含义是什么？
   <details><summary>💡 提示</summary>$\mathbf{U}$=输出空间的正交基，$\mathbf{\Sigma}$=各方向的缩放因子，$\mathbf{V}^T$=输入空间的正交基。等价于把矩阵作用理解为"旋转→缩放→旋转"。</details>

2. **(中等)** 为什么低秩近似能用于图像去噪？
   <details><summary>💡 提示</summary>噪声通常是高频、低能量的，对应小奇异值。低秩近似丢弃小奇异值 = 保留主要结构、丢弃噪声。</details>

3. **(较难)** LoRA 的核心思想是 $\Delta W = BA$（$B \in \mathbb{R}^{d \times r}, A \in \mathbb{R}^{r \times k}, r \ll \min(d,k)$）。为什么这被称为"受 SVD 启发的低秩分解"？
   <details><summary>💡 提示</summary>SVD 表明任何矩阵可表达为秩-1 矩阵的加权和 $\sum \sigma_i \mathbf{u}_i\mathbf{v}_i^T$。LoRA 的 $BA$ 正是只保留前 $r$ 项的低秩近似，$\sigma_i$ 被吸收进 $A$ 或 $B$ 中。</details>

---

## 🧪 学完本节后可完成的作业

- 可直接用 NumPy 实现 SVD 图像压缩实验：对 CIFAR-10 图像做不同 k 值的重建并计算 PSNR
---

## 学完后可以完成

- 完成卡内自测题与闭卷复现（SVD 分解）

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
