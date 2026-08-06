---
type: study
course: "05-计算机视觉"
topic: "相机标定与对极几何 (Epipolar Geometry)"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept:
  - 相机标定
  - 对极几何
  - 本质矩阵
  - 基础矩阵
  - 多视图几何
prerequisites:
  - 线性代数
  - 投影变换
related:
  - NeRF
  - 立体视觉
  - SLAM
flow: knowledge
upstream: ["[[线性代数基础CV]]", "[[几何变换CV]]"]
stage_moc: "[[🏭 第五阶段：专业深化与工程落地]]"
kind: concept
source: "Szeliski Ch.6; MVG Ch.6-7"
anki_deck: "05-计算机视觉::05-专业深化与工程落地"
anki_tags:
  - 学习
  - 计算机视觉
  - 3D视觉
  - 相机标定
  - 对极几何
  - 本质矩阵
  - 基础矩阵
tags:
  - 学习
  - 计算机视觉
  - 3D视觉
  - 相机标定
  - 对极几何
  - 本质矩阵
  - 基础矩阵
---

# 🎯 相机标定与对极几何 (Epipolar Geometry)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：相机标定（Camera Calibration）与对极几何（Epipolar Geometry）是连接 **2D 图像平面**与**真实 3D 物理世界**的几何桥梁，也是 Hartley & Zisserman 经典巨著《Multiple View Geometry》的绝对灵魂。无论是自动驾驶感知、机器人 SLAM 定位、三维重建（SfM），还是当下的 NeRF 与 3D Gaussian Splatting，都必须建立在相机内参外参矩阵以及两视角对极约束（本质矩阵 $\mathbf{E}$ 与基础矩阵 $\mathbf{F}$）之上。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (我们遇到了什么麻烦)**：
> 摄像机拍摄的照片只是三维世界在二维平面上的**降维投影**（丢弃了深度信息 $Z$）。
> 1. 我们不知道图像上的像素坐标 $(u, v)$ 对应空间中具体哪条三维射线（不知道相机的焦距 $f$、主点 $c_x, c_y$ 和畸变系数）；
> 2. 当两台相机从不同角度拍摄同一个物体时，如果已知左图的一个像素点 $p_1$，我们**不可能在右图整个二维平面上做盲目全图匹配**，计算量极大且极易错匹配。
> 我们需要一种几何约束，把 2D 图像点还原为 3D 空间射线，并将两视角的点匹配搜索范围降维到**一条线（对极线 Epipolar Line）上**！

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是所有 3D 计算机视觉的起点。从双目立体视觉测距，到 Structure from Motion (SfM) 恢复三维点云，再到自动驾驶多相机融合，对极约束 $\mathbf{x}_2^T \mathbf{F} \mathbf{x}_1 = 0$ 是唯一的物理守恒法则。
- **实际应用场景**：双目深度估计、视觉 SLAM 追踪与建图（ORB-SLAM）、AR 增强现实相机追踪、NeRF / 3DGS 数据预处理 (COLMAP)。
- **高频考点/任务**：针孔相机内参矩阵 $\mathbf{K}$ 的结构推导、外参矩阵 $[\mathbf{R} \mid \mathbf{t}]$ 转换、本质矩阵 $\mathbf{E} = [\mathbf{t}]_{\times} \mathbf{R}$ 推出过程、基础矩阵 $\mathbf{F}$ 的八点算法 (Eight-Point Algorithm) 手推、对极线计算。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[齐次坐标|齐次坐标 (Homogeneous Coordinates)]]**：将 $n$ 维向量用 $n+1$ 维表示（如 2D 点 $(x, y) \to (x, y, 1)^T$），从而可以用矩阵乘法统一表达平移与透视投影。
2. **[[齐次变换矩阵|向量叉积的反对称矩阵]]**：$\mathbf{a} \times \mathbf{b} = [\mathbf{a}]_{\times} \mathbf{b}$，其中 $[\mathbf{a}]_{\times} = \begin{pmatrix} 0 & -a_z & a_y \\ a_z & 0 & -a_x \\ -a_y & a_x & 0 \end{pmatrix}$。

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：
  - **相机标定**：就像**给相机的近视眼配度数眼镜**。测出焦距 $f$、中心偏离 $(c_x, c_y)$，把扭曲的图像纠正成完美的理想透视图。
  - **对极几何**：就像**两个人从不同角度看同一根电线杆**：
    - 左边的人用手指指向电线杆顶端（视线射线）；
    - 右边的人看左边人的眼睛和手指，这两点在右边人的视野里连成了一条直线（**对极线**）；
    - 右边的人**只需要在这条线上寻找电线杆顶端**即可！从全图搜寻降维到了沿着一条线拉窗帘搜寻！
- **为什么很自然**：两个相机光心 $O_1, O_2$ 与三维空间点 $P$ 构成了同一个**对极平面 (Epipolar Plane)**！平面与两个图像相交形成的交线就是对极线。
- **一句话直觉本质**：用内参标定还原透视射线，用三点共面约束将二维匹配简化为一维对极线搜寻。

---

## 5. 正式定义、核心公式、符号解释

### 1. 针孔相机投影与内参矩阵 $\mathbf{K}$
三维相机坐标系下点 $\mathbf{P}_c = (X_c, Y_c, Z_c)^T$ 投影到像素坐标 $\mathbf{p} = (u, v, 1)^T$：
$$Z_c \begin{pmatrix} u \\ v \\ 1 \end{pmatrix} = \mathbf{K} \mathbf{P}_c = \begin{pmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} X_c \\ Y_c \\ Z_c \end{pmatrix}$$

### 2. 跨视角位姿与外参 $[\mathbf{R} \mid \mathbf{t}]$
三维世界坐标 $\mathbf{P}_w$ 到相机坐标 $\mathbf{P}_c$ 的刚体变换：
$$\mathbf{P}_c = \mathbf{R} \mathbf{P}_w + \mathbf{t}$$

### 3. 本质矩阵 $\mathbf{E}$ 与 基础矩阵 $\mathbf{F}$ 的约束方程
设归一化相机坐标为 $\mathbf{x}_1 = \mathbf{K}_1^{-1} \mathbf{p}_1, \mathbf{x}_2 = \mathbf{K}_2^{-1} \mathbf{p}_2$：
- **本质矩阵约束 (Essential Matrix)**（对应归一化平面坐标）：
  $$\mathbf{x}_2^T \mathbf{E} \mathbf{x}_1 = 0 \quad \text{其中 } \mathbf{E} = [\mathbf{t}]_{\times} \mathbf{R}$$
- **基础矩阵约束 (Fundamental Matrix)**（直接对应像素坐标）：
  $$\mathbf{p}_2^T \mathbf{F} \mathbf{p}_1 = 0 \quad \text{其中 } \mathbf{F} = \mathbf{K}_2^{-T} \mathbf{E} \mathbf{K}_1^{-1}$$

### 4. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathbf{K}$ | 相机内参矩阵 (Intrinsic Matrix) | $3 \times 3$ 上三角矩阵 | $f_x, f_y$ 焦距, $c_x, c_y$ 主点 |
| $\mathbf{R}, \mathbf{t}$ | 旋转矩阵与平移向量 (Extrinsics) | $\mathbf{R} \in SO(3), \mathbf{t} \in \mathbb{R}^3$ | 相机的世界位姿 |
| $\mathbf{E}$ | 本质矩阵 (Essential Matrix) | $3 \times 3$，秩为 2 | 仅依赖于两相机的相对位姿 $\mathbf{R}, \mathbf{t}$ |
| $\mathbf{F}$ | 基础矩阵 (Fundamental Matrix) | $3 \times 3$，秩为 2 | 融合了内参和相对位姿 |
| $[\mathbf{t}]_{\times}$ | 向量 $\mathbf{t}$ 的反对称矩阵 | $3 \times 3$ 反对称 | 将叉积转写为矩阵乘法 |

---

## 6. 推导思路和思想来源

- **最初困难**：已知左图点 $p_1$ 和右图点 $p_2$，如何证明它们来自同一个三维点 $P$？
- **关键转念 1（利用三向量共面）**：
  在相机的归一化坐标系中：
  - 左相机光心到点的向量为 $\mathbf{x}_1$；
  - 右相机光心到点的向量（在左系下表达）为 $\mathbf{R}^T \mathbf{x}_2$；
  - 两个光心之间的连线平移向量为 $\mathbf{t}$。
  这三个向量都在同一个对极平面上！根据向量混合积，**三向量共面等价于混合积为 0**：
  $$\mathbf{t} \cdot (\mathbf{x}_2 \times (\mathbf{R} \mathbf{x}_1 + \mathbf{t})) = 0 \implies \mathbf{x}_2^T [\mathbf{t}]_{\times} \mathbf{R} \mathbf{x}_1 = 0$$
  完美导出本质矩阵 $\mathbf{E} = [\mathbf{t}]_{\times} \mathbf{R}$！
- **关键转念 2（解算八点算法）**：
  $\mathbf{p}_2^T \mathbf{F} \mathbf{p}_1 = 0$ 是一个关于 $\mathbf{F}$ 中 9 个元素的线性齐次方程。
  因为齐次性（相差比例因子），只有 8 个自由度。**只要找到 8 对匹配点，就可以写出线性方程组 $\mathbf{A} \mathbf{f} = 0$，通过 SVD 分解直接求解出基础矩阵 $\mathbf{F}$！**

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（反对称矩阵与叉积手算）
- **题目**：已知平移向量 $\mathbf{t} = (1, 2, 3)^T$，旋转矩阵 $\mathbf{R} = \mathbf{I}_{3\times 3}$（无旋转）。求本质矩阵 $\mathbf{E}$。
- **解答过程**：
  1. 写出 $\mathbf{t}$ 的反对称矩阵：
     $$[\mathbf{t}]_{\times} = \begin{pmatrix} 0 & -3 & 2 \\ 3 & 0 & -1 \\ -2 & 1 & 0 \end{pmatrix}$$
  2. 计算 $\mathbf{E} = [\mathbf{t}]_{\times} \mathbf{R} = [\mathbf{t}]_{\times} \mathbf{I} = \begin{pmatrix} 0 & -3 & 2 \\ 3 & 0 & -1 \\ -2 & 1 & 0 \end{pmatrix}$。
- **🤔 追问**：本质矩阵 $\mathbf{E}$ 的奇异值有什么特殊性质？
  - *答*：$\mathbf{E}$ 的两个非零奇异值必然相等（形如 $(\sigma, \sigma, 0)$），这是由于旋转矩阵的正交性决定的！

### 例子 2：中等例子（给定点与 $\mathbf{F}$ 矩阵计算对极线）
已知基础矩阵 $\mathbf{F}$，以及左图像素点 $\mathbf{p}_1 = (100, 200, 1)^T$。求该点在右图上对应的对极线方程 $\mathbf{l}_2$。
- **计算**：
  根据对极约束 $\mathbf{p}_2^T \mathbf{F} \mathbf{p}_1 = 0$，令 $\mathbf{l}_2 = \mathbf{F} \mathbf{p}_1 = (A, B, C)^T$。
  则右图上的匹配点 $\mathbf{p}_2 = (u_2, v_2, 1)^T$ 必须满足直线方程：
  $$A u_2 + B v_2 + C = 0$$
  右图搜寻匹配点时，只需在直线 $A x + B y + C = 0$ 上进行一维滑动搜索！

### 例子 3：实际应用（OpenCV + Python 实现基础矩阵求解与对极线绘制）

```python
import cv2
import numpy as np

def estimate_fundamental_matrix(pts1, pts2):
    """
    使用 RANSAC + 八点算法从匹配点计算基础矩阵 F
    pts1, pts2: Nx2 的像素匹配点
    """
    # 1. 使用 RANSAC 鲁棒估计基础矩阵 F
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC, 1.0, 0.99)
    
    # 选出内点 (Inliers)
    inliers1 = pts1[mask.ravel() == 1]
    inliers2 = pts2[mask.ravel() == 1]
    
    # 2. 计算左图点在右图对应的对极线 l2 = F * p1
    lines2 = cv2.computeCorrespondEpilines(inliers1.reshape(-1, 1, 2), 1, F)
    lines2 = lines2.reshape(-1, 3) # [A, B, C]
    
    return F, inliers1, inliers2, lines2

# 示例驱动代码
np.random.seed(42)
pts1 = np.random.uniform(100, 500, (20, 2))
pts2 = pts1 + np.random.normal(0, 5, (20, 2)) # 模拟微小平移
F, in1, in2, lines2 = estimate_fundamental_matrix(pts1, pts2)
print("估计得到的基础矩阵 F:\n", F)
print("基础矩阵的秩为:", np.linalg.matrix_rank(F)) # 严格为 2
```

---

## 8. 常见误区和易混概念

### 误区 1：基础矩阵 $\mathbf{F}$ 的秩为 3
- **错误直觉**：“$\mathbf{F}$ 是一个 $3 \times 3$ 矩阵，一般矩阵都是满秩 3 的。”
- **为什么错**：反对称矩阵 $[\mathbf{t}]_{\times}$ 的行列式等于 0（秩为 2）。因为 $\mathbf{E} = [\mathbf{t}]_{\times} \mathbf{R}$，乘上正交矩阵不改变秩，所以**本质矩阵 $\mathbf{E}$ 和基础矩阵 $\mathbf{F}$ 的秩严格等于 2**（行列式 $\det(\mathbf{F}) = 0$）！在八点算法计算出 $\mathbf{F}$ 后，必须通过 SVD 强制将最小奇异值设为 0。

### 概念对比表

| 矩阵 | 计算输入 | 自由度 (DoF) | 奇异值约束 | 依赖因素 |
| :--- | :--- | :--- | :--- | :--- |
| **本质矩阵 (Essential Matrix E)** | 归一化平面坐标 $\mathbf{x}$ | **5** (3 旋转 + 2 平移方向) | $(\sigma, \sigma, 0)$ | 仅依赖两相机的相对位姿 $\mathbf{R}, \mathbf{t}$ |
| **基础矩阵 (Fundamental Matrix F)**| 原始像素坐标 $\mathbf{p}$ | **7** (8个参数去标量) | $(\sigma_1, \sigma_2, 0)$ | 依赖相对位姿 $\mathbf{R}, \mathbf{t}$ + 相机内参 $\mathbf{K}_1, \mathbf{K}_2$ |
| **单应性矩阵 (Homography H)** | 纯旋转或共面三维点 | **8** | 无限制 | 仅适用于场景共面或相机纯旋转 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[齐次坐标|齐次坐标与投影变换]]：透视投影与三维到二维投影的矩阵表达。
- [[边缘检测|特征匹配]]：提供八点算法所需的像素对应对 $(p_1, p_2)$。

### 下游延伸
- [[🎯 NeRF 神经辐射场 (Neural Radiance Fields)]]：必须利用 COLMAP（基于相机标定与对极几何）算出图像的相机位姿 $\mathbf{R}, \mathbf{t}$。
- [[SLAM基础|SLAM]]：前端视觉里程计（VO）利用本质矩阵恢复相机运动。

### 横向关联
- 单应性矩阵 H ↔ 对极几何 F：当场景点全部在同一平面上时，对极约束退化，必须改用单应性矩阵 $\mathbf{H}$ 求解。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚对极几何解决什么问题（将 2D 全图特征匹配降维到 1D 对极线上）。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像给近视眼配眼镜和两个人看电线杆……”»）。
- [ ] 3. 写出相机内参矩阵 $\mathbf{K}$ 的 $3 \times 3$ 结构与各个符号含义。
- [ ] 4. 写出本质矩阵 $\mathbf{E} = [\mathbf{t}]_{\times} \mathbf{R}$ 和基础矩阵 $\mathbf{F} = \mathbf{K}_2^{-T} \mathbf{E} \mathbf{K}_1^{-1}$ 公式。
- [ ] 5. 写出对极约束方程 $\mathbf{p}_2^T \mathbf{F} \mathbf{p}_1 = 0$。
- [ ] 6. 推导为什么三向量共面能导出本质矩阵。
- [ ] 7. 解释八点算法为什么需要至少 8 对点，以及为什么最后要用 SVD 强制设最小奇异值为 0。
- [ ] 8. 对比本质矩阵 $\mathbf{E}$ 与基础矩阵 $\mathbf{F}$ 的区别。
- [ ] 9. 手算给定向量 $\mathbf{t}$ 的反对称矩阵。
- [ ] 10. 说明 COLMAP 在 NeRF / 3DGS 中充当的角色。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 基础矩阵 $\mathbf{F}$ 的秩大小 |
| 2 | 公式计算 | 基础 | 反对称矩阵与乘法手算 |
| 3 | 条件判断 | 中等 | 对极几何退化条件（纯旋转） |
| 4 | 变式/综合 | 中等 | 八点算法为何要做坐标归一化（Normalized 8-Point） |
| 5 | 开放/证明 | 较难 | 证明左图点 $p_1$ 在右图对应的对极线方程为 $\mathbf{l}_2 = \mathbf{F} \mathbf{p}_1$ |

### 题目与解析

#### 1. 关于基础矩阵 $\mathbf{F}$ 的性质，下列说法正确的是？
- A. 基础矩阵是满秩的，即 $\text{rank}(\mathbf{F}) = 3$
- B. 基础矩阵的行列式不等于 0
- C. 基础矩阵的秩为 2，且 $\det(\mathbf{F}) = 0$
- D. 基础矩阵只取决于相机的内参，与相机的旋转平移无关

> [!question]- 答案解析
> - **答案**：C
> - **解析**：由于平移向量的反对称矩阵 $[\mathbf{t}]_{\times}$ 的秩为 2，决定了本质矩阵与基础矩阵的秩严格为 2，行列式必为 0。
> - **对应误区**：误区 1。

#### 2. 当相机发生纯旋转（平移向量 $\mathbf{t} = \mathbf{0}$）时，对极几何会发生什么？我们应该改用什么矩阵表达？
> [!question]- 答案解析
> - **答案**：对极约束退化（因为 $\mathbf{E} = [\mathbf{0}]_{\times} \mathbf{R} = \mathbf{0}$，无法计算对极线）；必须改用单应性矩阵 (Homography Matrix $\mathbf{H}$)！
> - **解析**：当 $\mathbf{t}=0$ 时，所有三维点与两个光心共线，对极平面不复存在。此时图像坐标满足纯线性射影变换 $\mathbf{p}_2 = \mathbf{H} \mathbf{p}_1 = \mathbf{K}_2 \mathbf{R} \mathbf{K}_1^{-1} \mathbf{p}_1$。

#### 3. 为什么 Hartley 提出在运行八点算法求解 $\mathbf{F}$ 之前，必须对像素坐标进行归一化预处理 (Normalized 8-Point Algorithm)？
> [!question]- 答案解析
> - **答案**：防止系数矩阵 $\mathbf{A}$ 条件数过大导致数值计算极其不稳定。
> - **解析**：未归一化的像素坐标形如 $(1000, 2000, 1)$，在方程中构建项 $u_1 u_2 \approx 10^6$，而常数项为 1，数量级相差 6 个数量级！导致矩阵奇异值相差巨大，微小噪声会导致解出的 $\mathbf{F}$ 产生巨大偏差。归一化将其缩放到原点附近且方差为 1，数值极其稳定。

#### 4. 已知左相机内参 $\mathbf{K}_1$、右相机内参 $\mathbf{K}_2$，以及解算出的本质矩阵 $\mathbf{E}$。如何求基础矩阵 $\mathbf{F}$？
> [!question]- 答案解析
> - **答案**：$\mathbf{F} = \mathbf{K}_2^{-T} \mathbf{E} \mathbf{K}_1^{-1}$。
> - **解析**：由归一化坐标 $\mathbf{x}_1 = \mathbf{K}_1^{-1} \mathbf{p}_1 \implies \mathbf{x}_2^T \mathbf{E} \mathbf{x}_1 = (\mathbf{K}_2^{-1} \mathbf{p}_2)^T \mathbf{E} (\mathbf{K}_1^{-1} \mathbf{p}_1) = \mathbf{p}_2^T (\mathbf{K}_2^{-T} \mathbf{E} \mathbf{K}_1^{-1}) \mathbf{p}_1 = 0$。

#### 5. 【证明】证明已知右图对极线方程为 $\mathbf{l}_2 = \mathbf{F} \mathbf{p}_1$，且极点 $e_2$ 必在对极线 $\mathbf{l}_2$ 上。
> [!question]- 答案解析
> - **证明**：
>   极点 $e_2$ 是左相机光心 $O_1$ 在右图上的投影。
>   因为左光心 $O_1$ 在所有对极平面上，故所有对极线必须相交于极点 $e_2$，即 $e_2^T \mathbf{l}_2 = 0$。
>   由基础矩阵定义，左光心对应的投影满足 $\mathbf{F}^T \mathbf{e}_2 = \mathbf{0} \implies \mathbf{e}_2^T \mathbf{F} = \mathbf{0}$。
>   因此：$\mathbf{e}_2^T \mathbf{l}_2 = \mathbf{e}_2^T (\mathbf{F} \mathbf{p}_1) = (\mathbf{e}_2^T \mathbf{F}) \mathbf{p}_1 = \mathbf{0} \cdot \mathbf{p}_1 = 0$！
>   证明极点 $e_2$ 恒在对极线 $\mathbf{l}_2$ 上！

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
  - [[齐次坐标]]
  - [[🎯 NeRF 神经辐射场 (Neural Radiance Fields)]]
  - [[SLAM基础|SLAM]]
- **建议标签**：`#学习` `#计算机视觉` `#3D视觉` `#相机标定` `#对极几何` `#本质矩阵` `#基础矩阵`

---
---

## 学完后可以完成

- 可作为 HW06 开放项目『多视图几何』选题

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
