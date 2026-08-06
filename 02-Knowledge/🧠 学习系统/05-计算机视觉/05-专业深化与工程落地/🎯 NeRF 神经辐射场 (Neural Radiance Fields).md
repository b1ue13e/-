---
type: study
course: "05-计算机视觉"
topic: "NeRF 神经辐射场 (Neural Radiance Fields)"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept:
  - NeRF
  - 神经辐射场
  - 体渲染
  - 3D重建
  - 位置编码
prerequisites:
  - 相机标定
  - 多层感知机
related:
  - GaussianSplatting
  - 立体视觉
  - 点云处理
flow: knowledge
upstream: ["[[🎯 相机标定与对极几何 (Epipolar Geometry)]]", "[[MLP]]"]
stage_moc: "[[🏭 第五阶段：专业深化与工程落地]]"
kind: concept
source: "论文补充; CS231n A3"
anki_deck: "05-计算机视觉::05-专业深化与工程落地"
anki_tags:
  - 学习
  - 深度学习
  - 计算机视觉
  - 3D视觉
  - NeRF
  - 神经辐射场
  - 体渲染
tags:
  - 学习
  - 深度学习
  - 计算机视觉
  - 3D视觉
  - NeRF
  - 神经辐射场
  - 体渲染
---

# 🎯 NeRF 神经辐射场 (Neural Radiance Fields)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：NeRF 由 Ben Mildenhall 等人于 ECCV 2020 提出（获最佳论文提名），是**3D 计算机视觉与神经渲染（Neural Rendering）领域的革命性里程碑**。它首次提出用一个简单的多层感知机（MLP）网络去隐式表达整个 3D 场景的连续辐射场，并结合经典**体渲染（Volume Rendering）**，实现了极其惊艳的**新视角合成（Novel View Synthesis）**。NeRF 开创了隐式三维表示的新纪元，直接孕育了后来的 Instant-NGP、3D Gaussian Splatting 及 3D 神经网络生成。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (我们遇到了什么麻烦)**：
> 在 NeRF 之前，三维重建主要依靠显式几何表达（如三角网格 Mesh、体素 Voxel、点云 Point Cloud）：
> - **网格 Mesh**：难以表达各向异性的光泽、透明物体或烟雾；
> - **体素 Voxel**：显存随分辨率呈现 $O(N^3)$ 爆炸增长（分辨率到 512×512×512 显存就彻底报废）；
> - **点云 Point Cloud**：离散不连续，渲染新视角时充斥着空洞斑块。
> 我们迫切需要一种**占用极小显存（仅几 MB 的网络权重）、能够表达连续无限分辨率、且能完美渲染光影反射与透明物体的全新 3D 场景表达**。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：NeRF 完美融合了深度学习（MLP）、经典几何（相机光线采样）与经典物理（体渲染累积透明度）。它是理解现代神经隐式场 (Implicit Neural Representations, INR)、可微渲染以及 3D AIGC（如 Text-to-3D DreamFusion）的核心理论基石。
- **实际应用场景**：影视级虚拟场景搭建、AR/VR 沉浸式新视角漫游、数字人三维重建、Google Maps 3D 街景渲染。
- **高频考点/任务**：5D 辐射场输入输出定义 $(x,y,z, \theta, \phi) \to (c, \sigma)$、体渲染离散积分公式推导、透射率 $T_i$ 物理含义、高频位置编码 (Positional Encoding) 解决 MLP 频谱偏置 (Spectral Bias) 的必要性、PyTorch 手写光线采样与体渲染。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[🎯 相机标定与对极几何 (Epipolar Geometry)|相机内参与光线生成]]**：根据相机内参 $\mathbf{K}$ 与外参 $[\mathbf{R} \mid \mathbf{t}]$，计算穿过每个像素点 $(u, v)$ 的 3D 光线方程 $\mathbf{r}(t) = \mathbf{o} + t \mathbf{d}$。
2. **[[MLP|多层感知机 (MLP)]]**：拟合连续多元非线性函数的基石网络。

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：NeRF 就像一个**记忆力超群的 3D 全息记忆库**：
  - 你给这个记忆库输入空间中任意一个点的坐标 $(x,y,z)$ 和你看这个点的视角方向 $(\theta, \phi)$；
  - 记忆库（MLP 网络）立刻回答你：“这个点有多密（透明度 $\sigma$）？以及从这个视角看过去它是什么颜色（RGB $\mathbf{c}$）？”
  - 渲染新视角时，你从眼睛出发射出成千上万条视线（光线 Rays）。每条视线穿越记忆库，把沿途采样的“密度 $\sigma$”和“颜色 $\mathbf{c}$”**像穿糖葫芦一样按透明度累加起来**，就画出了一张逼真无比的新视角照片！
- **为什么很自然**：用神经网络的参数去“记忆”整个空间，把 3D 几何存储变为了模型权重；用光线积分把 3D 空间投射回 2D 屏幕，全程可微可以端到端求导！
- **一句话直觉本质**：用 MLP 隐式记忆 5D 辐射场，沿相机光线应用可微体渲染积分积算像素颜色。

---

## 5. 正式定义、核心公式、符号解释

### 1. 5D 辐射场映射函数 (5D Neural Radiance Field)
NeRF 将三维场景表达为一个连续函数 $f_{\Theta}$：
$$f_{\Theta}: (\mathbf{x}, \mathbf{d}) \to (\mathbf{c}, \sigma)$$
- **输入**：3D 空间位置 $\mathbf{x} = (x, y, z)$ 与 2D 观察视角方向 $\mathbf{d} = (\theta, \phi)$（通常用单位方向向量 $\mathbf{d} \in \mathbb{S}^2$）；
- **输出**：发光颜色 $\mathbf{c} = (r, g, b)$ 与体密度 $\sigma$（体积密度 $\sigma$ 仅依赖位置 $\mathbf{x}$，保证几何一致性）。

### 2. 连续体渲染方程 (Continuous Volume Rendering)
对于通过相机的某条光线 $\mathbf{r}(t) = \mathbf{o} + t \mathbf{d}$，近端为 $t_n$，远端为 $t_f$，其渲染出的颜色 $C(\mathbf{r})$ 为：
$$C(\mathbf{r}) = \int_{t_n}^{t_f} T(t) \sigma(\mathbf{r}(t)) \mathbf{c}(\mathbf{r}(t), \mathbf{d}) dt$$
其中**透明度/累积透射率 (Accumulated Transmittance)** $T(t)$ 定义为光线沿途未碰撞到任何微粒的概率：
$$T(t) = \exp \left( -\int_{t_n}^t \sigma(\mathbf{r}(s)) ds \right)$$

### 3. 离散数值积分公式 (Quadrature / Discrete Rendering)
为了在计算机中计算，将光线区间 $[t_n, t_f]$ 划分成 $N$ 个微小采样区间：
$$\hat{C}(\mathbf{r}) = \sum_{i=1}^N T_i \left( 1 - \exp(-\sigma_i \delta_i) \right) \mathbf{c}_i$$
其中 $T_i = \exp \left( -\sum_{j=1}^{i-1} \sigma_j \delta_j \right)$，$\delta_i = t_{i+1} - t_i$ 为相邻采样点间的距离。

### 4. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathbf{o}$ | 光线起始原点 (Camera Origin) | $\mathbb{R}^3$ | 相机光心坐标 |
| $\mathbf{d}$ | 光线方向单位向量 (Ray Direction) | $\mathbb{R}^3, \|\mathbf{d}\|=1$ | 穿过像素的视角方向 |
| $\sigma$ | 体密度 (Volume Density) | $[0, +\infty)$ | 越大越不透明，只由位置 $\mathbf{x}$ 决定 |
| $\mathbf{c}$ | 辐射 RGB 颜色 (Radiance Color) | $[0, 1]^3$ | 由位置 $\mathbf{x}$ 和视角 $\mathbf{d}$ 共同决定 |
| $T_i$ | 累积透射率 (Transmittance) | $[0, 1]$ | $T_i \to 0$ 说明前面已被遮挡 |
| $w_i$ | 采样点合成权重 | $[0, 1]$ | $w_i = T_i (1 - e^{-\sigma_i \delta_i})$ |

---

## 6. 推导思路和思想来源

- **最初困难**：普通 MLP 拟合低维坐标到 RGB 的映射时，生成的图像**极其模糊，失去了所有高频纹理细节**。
- **关键转念 1 (正弦位置编码解决频谱偏置)**：
  根据神经切线核 (NTK) 理论，标准 MLP 倾向于先学习低频平滑函数（Spectral Bias）。
  **解决思想**：在将坐标 $(x,y,z)$ 喂入 MLP 之前，用高频正弦/余弦函数做高维映射：
  $$\gamma(p) = \left( \sin(2^0 \pi p), \cos(2^0 \pi p), \dots, \sin(2^{L-1} \pi p), \cos(2^{L-1} \pi p) \right)$$
  将 3D 坐标维度从 3 提升到 $3 \times 2L = 60$，迫使 MLP 拟合高频细节！
- **关键转念 2 (分层次分级采样 Hierarchical Sampling)**：
  一条光线上大部分区域是空气（$\sigma=0$），均匀采样浪费了大量计算。
  **解决思想**：训练粗糙网络 (Coarse Net) 与精细网络 (Fine Net)。先用粗网络算出的权重 $w_i$ 作为概率密度函数 (PDF)，在概率大的区域（物体表面附近）实施**逆变换采样 (Inverse Transform Sampling)** 密集布置二次采样点，大幅提升渲染效率！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（单光线两点体渲染手算）
- **题目**：某光线上有两个采样点，步长 $\delta = 1$。
  - 点 1：$\sigma_1 = 0.693$ ($\implies e^{-\sigma_1 \delta} = 0.5$)，颜色 $\mathbf{c}_1 = (1, 0, 0)$（纯红）；
  - 点 2：$\sigma_2 = 1.386$ ($\implies e^{-\sigma_2 \delta} = 0.25$)，颜色 $\mathbf{c}_2 = (0, 1, 0)$（纯绿）。
  求该光线合成的 RGB 颜色。
- **解答过程**：
  1. 计算点 1：
     - $T_1 = 1.0$ (起点无遮挡)；
     - 权重 $w_1 = T_1 (1 - e^{-\sigma_1 \delta}) = 1.0 \times (1 - 0.5) = 0.5$。
  2. 计算点 2：
     - $T_2 = T_1 \times e^{-\sigma_1 \delta} = 1.0 \times 0.5 = 0.5$；
     - 权重 $w_2 = T_2 (1 - e^{-\sigma_2 \delta}) = 0.5 \times (1 - 0.25) = 0.5 \times 0.75 = 0.375$。
  3. 合成颜色：
     $$\hat{C} = w_1 \mathbf{c}_1 + w_2 \mathbf{c}_2 = 0.5 \times (1, 0, 0) + 0.375 \times (0, 1, 0) = (0.5, 0.375, 0)$$
- **🤔 追问**：为什么 $w_1 + w_2 = 0.875$ 而不是 1？
  - *答*：因为两点之后仍有 $T_3 = 0.5 \times 0.25 = 0.125$ 的光线穿透到了无穷远处（背景色）。

### 例子 2：中等例子（NeRF MLP 架构细节解构）
NeRF 的 MLP 架构包含 8 层全连接层（每层 256 个神经元，帶残差 Skip Connection）：
- 位置编码 $\gamma(\mathbf{x})$（60 维）输入前 8 层，输出体密度 $\sigma$ 和一个 256 维中间特征向量；
- 视角编码 $\gamma(\mathbf{d})$（24 维）与 256 维特征向量拼接，输入最后 1 层全连接层输出颜色 $\mathbf{c}$。
- **为什么这样设计**：保证**几何体密度 $\sigma$ 完全独立于观察视角**，而只有视觉颜色 $\mathbf{c}$ 允许受视角影响（完美建模高光与反射效果）！

### 例子 3：实际应用（PyTorch 手写纯函数体渲染核心算子）

```python
import torch

def raw2outputs(raw_pred, z_vals, rays_d):
    """
    NeRF 可微体渲染核心算子 (Pure PyTorch Implementation)
    raw_pred: [Num_Rays, Num_Samples, 4] (前3维为RGB, 第4维为Density \sigma)
    z_vals:   [Num_Rays, Num_Samples] (采样深度值)
    rays_d:   [Num_Rays, 3] (光线方向向量)
    """
    # 1. 计算相邻采样点间距 \delta
    dists = z_vals[..., 1:] - z_vals[..., :-1]
    # 最后一点补无限大
    dists = torch.cat([dists, torch.tensor([1e10], device=z_vals.device).expand(dists[..., :1].shape)], dim=-1)
    
    # 乘上光线方向向量的模长得到真实物理距离
    dists = dists * torch.norm(rays_d[..., None, :], dim=-1)
    
    # 2. 提取 RGB 与 \sigma
    rgb = torch.sigmoid(raw_pred[..., :3]) # [Rays, Samples, 3]
    sigma = torch.relu(raw_pred[..., 3])    # [Rays, Samples]
    
    # 3. 计算离散不透明度 alpha = 1 - exp(-\sigma * \delta)
    alpha = 1.0 - torch.exp(-sigma * dists)
    
    # 4. 计算累积透射率 T_i = cumprod(1 - alpha)
    # torch.cumprod 需向前错一位，设置 T_1 = 1
    T = torch.cumprod(torch.cat([torch.ones_like(alpha[..., :1]), 1.0 - alpha + 1e-10], dim=-1), dim=-1)[..., :-1]
    
    # 5. 计算合成权重 w_i = T_i * alpha_i
    weights = T * alpha # [Rays, Samples]
    
    # 6. 加权求和得到最终像素 RGB
    rgb_map = torch.sum(weights[..., None] * rgb, dim=-2)
    depth_map = torch.sum(weights * z_vals, dim=-1)
    
    return rgb_map, depth_map, weights
```

---

## 8. 常见误区和易混概念

### 误区 1：NeRF 的输入必须包含 3D 点云或深度网格 (Mesh)
- **错误直觉**：“NeRF 既然是 3D 重建，输入肯定需要像 Kinect 一样提供深度点云。”
- **为什么错**：NeRF **完全不需要任何 3D 几何输入**！它的训练输入**仅仅是多视角 2D 图像 + 对应相机的内外参位姿**。几何（体密度 $\sigma$）完全是在端到端体渲染梯度反向传播过程中自动隐式学出来的。

### 概念对比表

| 3D 表达范式 | 表达形式 | 渲染速度 (FPS) | 显存/内存占用 | 代表算法 |
| :--- | :--- | :--- | :--- | :--- |
| **经典显式网格** | 顶点 + 三角面片 (Mesh) | **极快 (100+ FPS)** | 取决于网格面数 | OpenGL / Unity |
| **NeRF (隐式辐射场)** | 连续 MLP 神经网络权重 | **较慢 (0.1 - 5 FPS)**| **极小 (仅几 MB 参数)** | Vanilla NeRF, Mip-NeRF |
| **3DGS (显式高斯体)** | 数十万离散 3D 高斯椭球 | **极快 (100+ FPS)** | 中等 (数百 MB) | 3D Gaussian Splatting |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[🎯 相机标定与对极几何 (Epipolar Geometry)]]：COLMAP 位姿估计为 NeRF 提供相机的内外参。
- [[MLP]]：NeRF 的隐式函数载体。

### 下游延伸
- 3D Gaussian Splatting：解决 NeRF 渲染速度慢的显式高斯替代方案。

### 横向关联
- [[🎯 Diffusion 扩散模型 (DDPM)]] ↔ NeRF：结合形成 3D 生成模型（如 DreamFusion, Zero123）。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚 NeRF 解决什么问题（无需显式几何的连续 3D 新视角合成）。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像给空间建立 3D 全息记忆库……”»）。
- [ ] 3. 写出 5D 辐射场的输入输出映射公式 $f_{\Theta}(\mathbf{x}, \mathbf{d}) \to (\mathbf{c}, \sigma)$。
- [ ] 4. 写出离散体渲染颜色合成公式与透射率 $T_i$ 公式。
- [ ] 5. 解释为什么 $\sigma$ 只能由位置 $\mathbf{x}$ 决定，而 $\mathbf{c}$ 由位置 $\mathbf{x}$ 和视角 $\mathbf{d}$ 共同决定。
- [ ] 6. 说明正弦位置编码 (Positional Encoding) 解决 MLP 频谱偏置的原理。
- [ ] 7. 手算单光线两采样点体渲染输出。
- [ ] 8. 解释分层采样（Coarse & Fine Network）的设计动机。
- [ ] 9. 手写包含 `cumprod` 累积透射率计算的 PyTorch 体渲染算子。
- [ ] 10. 说明 3D Gaussian Splatting 相比 NeRF 的最大优势。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 体密度 $\sigma$ 的物理依赖性 |
| 2 | 公式计算 | 基础 | 离散体渲染权重计算 |
| 3 | 条件判断 | 中等 | 位置编码对细节渲染的影响 |
| 4 | 变式/综合 | 中等 | 为什么纯 NeRF 渲染一个像素非常耗时？ |
| 5 | 开放/推导 | 较难 | 从连续体渲染积分导出离散数值合成公式 |

### 题目与解析

#### 1. 关于 NeRF 中的体密度 $\sigma(\mathbf{x})$，说法正确的是？
- A. $\sigma$ 随观察角度 $(\theta, \phi)$ 的变化而变化
- B. $\sigma$ 仅仅是空间三维坐标 $(x, y, z)$ 的函数，与观察角度无关
- C. $\sigma$ 可以取负数表示负不透明度
- D. $\sigma$ 是由相机内参数决定的

> [!question]- 答案解析
> - **答案**：B
> - **解析**：一个物体的三维几何形状（体密度 $\sigma$）无论从什么角度看都是客观固定不变的，因此 $\sigma$ 仅依赖于空间位置 $\mathbf{x}$；只有表面高光/反射颜色 $\mathbf{c}$ 随视角 $\mathbf{d}$ 改变。
> - **对应误区**：误区 1。

#### 2. 在 NeRF 中，为什么渲染一个 $800 \times 800$ 分辨率的图像需要跑数百万次 MLP 前向传播？
> [!question]- 答案解析
> - **答案**：因为每个像素对应的光线上包含几十到上百个采样点。
> - **解析**：全图有 $800 \times 800 = 640,000$ 条光线。若每条光线采样 128 个点，渲染一张图就需要对 5D 输入调用 $640,000 \times 128 \approx 8.19 \times 10^7$ 次 MLP 前向推理！这就是原始 NeRF 渲染极慢的根源。

#### 3. 如果在 NeRF 中移除了正弦位置编码（Positional Encoding），渲染出来的图像会发生什么变化？
> [!question]- 答案解析
> - **答案**：图像会变得极其平滑和模糊，丢失所有高频纹理与边缘细节。
> - **解析**：标准 MLP 具有“低频偏置”，直接拟合低维坐标容易陷入低频平滑解。高频正弦位置编码强行将坐标投影到高维正弦空间，使网络能够学习高频傅里叶分量。

#### 4. 在体渲染中，如果某个采样点 $i$ 的体密度 $\sigma_i \to \infty$（绝对不透明的实心物体），它之后的所有采样点 $j > i$ 的合成权重 $w_j$ 会变成多少？
> [!question]- 答案解析
> - **答案**：严格等于 0。
> - **解析**：当 $\sigma_i \to \infty$ 时，$e^{-\sigma_i \delta_i} \to 0$，该点的透射项变为 0。后续所有点的累积透射率 $T_j = \prod_{k=1}^{j-1} e^{-\sigma_k \delta_k}$ 中包含了该 0 项，导致 $T_j = 0 \implies w_j = 0$。这完美符合物理上的光线遮挡！

#### 5. 【开放/推导】简述 3D Gaussian Splatting (3DGS) 是如何摆脱 NeRF 的光线采样与 MLP 推理瓶颈，实现 100+ FPS 实时渲染的。
> [!question]- 答案解析
> - **答案**：用显式可微的 3D 高斯椭球替代隐式 MLP，用 GPU 硬件级 Alpha-blending 栅格化替代逐点光线采样。
> - **解析**：3DGS 不再用 MLP 记忆空间，而是直接用数百万个显式 3D 高斯点（包含位置、协方差椭球、颜色和不透明度）表达场景；渲染时将 3D 高斯直接投影到 2D 屏幕，采用快速 Tile-based 排序与 Alpha 合成，完全避开了逐点调用神经网络的巨大开销。

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
  - [[🎯 相机标定与对极几何 (Epipolar Geometry)]]
  - [[MLP]]
  - [[05-计算机视觉/02-深度学习内核/3DGS|3D Gaussian

---

## 学完后可以完成

- 可作为 HW06 开放项目『3D/NeRF』选题

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
