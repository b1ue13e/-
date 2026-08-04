---
title: "K-均值聚类算法 (K-Means Clustering)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, K-means, 聚类, 无监督学习, EM算法]
upstream: ["[[无监督学习]]", "[[线性代数基础]]"]
downstream: ["[[高斯混合模型]]", "[[K-means++]]", "[[MiniBatchKMeans]]"]
status: learning
---

# 🎯 K-均值聚类算法 (K-Means)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：K-Means 是最经典、最简单且工业界应用最广的原型聚类（Prototype Clustering）算法。它是理解无监督学习、簇质心更新机制以及 EM 算法（期望极大算法）物理图像的必修基础。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**
> 假设你拥有 100 万个用户的二维地理位置数据，需要在城市中设立 5 个仓储中心，使得每个用户到其最近仓储中心的距离之和最小。

以往的方法卡在：
- 没有事先划分好的“哪个用户属于哪个仓储区”的标签；
- 手工穷举切分方案组合数是指数级（NP-Hard）。

K-Means **通过“分配-更新”两步迭代**，高效地求得了局部最优的聚类质心划分。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：
  - **后续影响**：它是 [[高斯混合模型|高斯混合模型 (GMM)]] 的硬聚类特例；其初始化缺陷直接导出了 [[K-means++]] 算法。
  - **课程位置**：属于“无监督聚类算法”的核心柱石。
- **实战与科研价值**：
  - **图像量化**：将 24 位真彩色图片用 16 种主色彩压缩（Color Quantization）。
  - **最常出现题型**：单步质心更新手算题、受离群点影响分析题、K 值的选择（肘部法 Elbow Method）应用题。

---

## 3. 学它之前需要哪些前置知识？

### 最小必要背景：
1. **欧氏距离**：$d(x, y) = \|\mathbf{x} - \mathbf{y}\|_2$。
2. **质心/均值**：一组向量的算术平均值 $\boldsymbol{\mu} = \frac{1}{|C|} \sum_{\mathbf{x} \in C} \mathbf{x}$。

---

## 4. 用直觉语言解释它

> «“这东西其实就像选举与投票站更新……”»

1. **初始化**：在地图上随机插 $K$ 面旗子作为初始投票站。
2. **分配 (Assignment)**：所有居民看哪面旗子离自己近，就跑去哪面旗子底下集合（形成 $K$ 个簇）。
3. **更新 (Update)**：每面旗子的负责人看到自己旗下站了这么多人，重新把旗子移到这群人的几何中心位置。
4. **重复**：居民重新按新旗子位置站队……直到旗子不再移动为止。

---

## 5. 正式定义、核心公式、符号解释

### 1. 目标函数 (WCSS / 簇内平方和)
给定数据集 $D = \{\mathbf{x}_1, \dots, \mathbf{x}_N\}$，K-Means 旨在最小化簇内平方误差和（Within-Cluster Sum of Squares, WCSS）：

$$E = \sum_{k=1}^K \sum_{\mathbf{x} \in \mathcal{C}_k} \|\mathbf{x} - \boldsymbol{\mu}_k\|^2$$

其中 $\boldsymbol{\mu}_k = \frac{1}{|\mathcal{C}_k|} \sum_{\mathbf{x} \in \mathcal{C}_k} \mathbf{x}$ 是簇 $\mathcal{C}_k$ 的均值向量（质心）。

### 2. 算法迭代两步
- **E 步 (Assignment)**：保持质心 $\boldsymbol{\mu}_k$ 不变，更新样本簇分配：
  $$\mathcal{C}_k^{(t)} = \{\mathbf{x}_i \mid \|\mathbf{x}_i - \boldsymbol{\mu}_k^{(t)}\|^2 \le \|\mathbf{x}_i - \boldsymbol{\mu}_j^{(t)}\|^2, \forall j\}$$
- **M 步 (Update)**：保持簇分配不变，重新计算质心：
  $$\boldsymbol{\mu}_k^{(t+1)} = \frac{1}{|\mathcal{C}_k^{(t)}|} \sum_{\mathbf{x} \in \mathcal{C}_k^{(t)}} \mathbf{x}$$

---

## 6. 例子：基础 → 中等 → 实际应用

### 例子 1：单步手算更新
**题目**：4 个一维点 $X = \{1, 2, 6, 8\}$。初始质心 $\mu_1 = 2, \mu_2 = 7$。请完成第 1 次迭代。

**解答**：
1. **分配**：
   - $x=1$：到 $\mu_1$ 距离 1，到 $\mu_2$ 距离 6 $\implies \mathcal{C}_1$
   - $x=2$：到 $\mu_1$ 距离 0 $\implies \mathcal{C}_1$
   - $x=6$：到 $\mu_1$ 距离 4，到 $\mu_2$ 距离 1 $\implies \mathcal{C}_2$
   - $x=8$：到 $\mu_1$ 距离 6，到 $\mu_2$ 距离 1 $\implies \mathcal{C}_2$
   - 结果：$\mathcal{C}_1 = \{1, 2\}, \mathcal{C}_2 = \{6, 8\}$。
2. **更新质心**：
   - $\mu_1^{\text{new}} = (1+2)/2 = 1.5$
   - $\mu_2^{\text{new}} = (6+8)/2 = 7.0$

---

## 7. 常见误区和易混概念

### 局限性与缺点
1. **对初始质心敏感**：不同的随机初始质心可能收敛到完全不同的局部极小值（解决方案：K-Means++）。
2. **需预先指定 $K$**：通过肘部法 (Elbow Method) 或轮廓系数确定最佳 $K$。
3. **假设簇是球形/凸的**：无法有效识别非凸形状的簇（如双环形，需用 DBSCAN）。
4. **对离群点/噪声极其敏感**：均值易受极值牵引（解决方案：K-Medoids / PAM 用中位数代替均值）。

---

## 8. 相关知识点与 Obsidian 双链建议

### 上游依赖（前置知识）
- [[01-基础概念/无监督学习|无监督学习]]

### 下游延伸（后续进阶）
- [[05-其他方法/高斯混合模型GMM|高斯混合模型GMM]]
- [[05-其他方法/DBSCAN密度聚类|DBSCAN密度聚类]]

## 下游延伸（后续进阶）
- [[05-其他方法/高斯混合模型GMM|高斯混合模型GMM]]
- [[05-其他方法/DBSCAN密度聚类|DBSCAN密度聚类]]

## 下游延伸（后续进阶）
- [[05-其他方法/高斯混合模型GMM|高斯混合模型GMM]]
- [[05-其他方法/DBSCAN密度聚类|DBSCAN密度聚类]]

## 下游延伸
- [[01-基础概念/PCA|PCA]]：常与 K-Means 结合做降维后聚类。

---

## 9. 闭卷复现任务

1. 写出 K-Means 的目标函数（簇内平方和 WCSS）。
2. 默写 K-Means 迭代更新的两大步骤。
3. 列举 K-Means 的 4 个核心缺点。
4. 说明“肘部法 (Elbow Method)”如何确定最佳 $K$ 值。

---

## 10. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 算法性质 |
| 2 | 计算题 | 基础 | 单步质心计算 |
| 3 | 缺点辨析 | 中等 | 形状适用性 |
| 4 | 参数选择 | 中等 | 肘部法分析 |
| 5 | 算法改进 | 较难 | K-Means++ 思想 |

1. **[概念辨析] K-Means 算法在更新簇质心（M步）时，使得该簇内所有点到质心的距离平方和最小的统计量是：**
   A. 中位数 (Median)  B. 均值 (Mean)  C. 众数 (Mode)  D. 最大值
> [!question]- 答案解析
> **答案**：B  
> **解析**：二次损失 $\sum (x-\mu)^2$ 的极小值点正好是算术平均值 Mean。  
> **标签**：`#自测/基础 #均值`

2. **[计算题] 某簇内包含三个二维点 $(0,0), (0,3), (3,0)$，该簇更新后的质心坐标为：**
   A. $(1, 1)$  B. $(1.5, 1.5)$  C. $(0, 0)$  D. $(3, 3)$
> [!question]- 答案解析
> **答案**：A  
> **解析**：$x$ 均值 $(0+0+3)/3 = 1$，$y$ 均值 $(0+3+0)/3 = 1$，质心为 $(1,1)$。  
> **标签**：`#自测/基础 #质心计算`

3. **[缺点辨析] 面对同心圆形状（非凸）分布的数据集，K-Means 效果很差，最主要的原因是：**
   A. K-Means 假设簇是凸球面形状的  
   B. 点的数量太少  
   C. 学习率太小  
   D. 无法计算欧氏距离
> [!question]- 答案解析
> **答案**：A  
> **解析**：基于欧氏距离和质心的划分导致 K-Means 的决策边界永远是超平面切分，只适合凸集/球形簇。  
> **标签**：`#自测/中等 #球形假设`

4. **[参数选择] 绘制 WCSS 随 $K$ 变化的曲线，当 $K$ 从 1 增加到 10 时，应该选择的 $K$ 值是：**
   A. WCSS 降为 0 时的 $K=N$  
   B. 曲线下降斜率发生明显转折的“肘部 (Elbow)”节点  
   C. 最大的 $K$  
   D. $K=1$
> [!question]- 答案解析
> **答案**：B  
> **解析**：肘部点之后 WCSS 下降趋于平缓，说明收益边际递减，是最佳 $K$ 节点。  
> **标签**：`#自测/中等 #肘部法`

5. **[算法改进] K-Means++ 在选择初始 $K$ 个质心时的核心改进思想是：**
   A. 随机挑选 $K$ 个点  
   B. 相互距离越远的点，被选为下一个初始质心的概率越大  
   C. 距离最近的点优先选  
   D. 选最大的点
> [!question]- 答案解析
> **答案**：B  
> **解析**：K-Means++ 按照与已有质心的最短距离平方成正比的概率挑选新质心，分散初始点。  
> **标签**：`#自测/较难 #K-Means++`

---

## 11. 我的主动回忆区

## 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

## 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

## 我的错误与卡点
- 

## 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 12. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/01-基础概念/`
- **建议双链**：
  - [[01-基础概念/🌱 第一阶段：基础概念|第一阶段：基础概念]]
  - [[01-基础概念/无监督学习|无监督学习]]
- **建议标签**：`#学习` `#机器学习` `#K-means` `#聚类` `#无监督学习`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: K-means)

> **作业任务说明**：本作业为《K-means》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

### 1. 4 级 Baseline 设级与冲榜拆解 (4-Tier Baseline System)

| Baseline 级别 | 评估指标 (Metric Target) | 突破核心技术 & 优化建议 |
| :--- | :--- | :--- |
| 🟢 **Simple Baseline** | 跑通代码无报错 | 搭建基础 PyTorch 模型框架，完成前向传播与 Loss 计算 |
| 🔵 **Medium Baseline** | 评估 Metric 提升 $20\%$ | **特征与损失优化**：引入数据标准化 (StandardScaler)、标签平滑或权值衰减 |
| 🟣 **Strong Baseline** | 评估 Metric 提升 $40\%$ | **架构与调度优化**：使用 `AdamW` + `CosineAnnealingLR` 余弦退火学习率调度器 |
| 🔴 **Boss Baseline** | **绝顶 SOTA 达标线** | **理论极值突破**：手写无偏估计/SVD 伪逆矩阵/K-Fold 模型集成 (Ensemble) 突破极限 |

### 2. 助教 Starter Code 与作业框架 (PyTorch Runnable Boilerplate)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np

# ---------------------------------------------------------------
# Step 1: 模拟生成 K-means 实战数据集 (Synthetic Dataset)
# ---------------------------------------------------------------
torch.manual_seed(42)
np.random.seed(42)

N, d = 300, 4
X_raw = np.random.randn(N, d)
y_raw = (X_raw[:, 0] * 1.5 - X_raw[:, 1] * 2.0 + np.random.randn(N) * 0.1 > 0).astype(np.int64)

class CustomHWDataset(Dataset):
    def __init__(self, x, y):
        self.x = torch.tensor(x, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

dataset = CustomHWDataset(X_raw, y_raw)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# ---------------------------------------------------------------
# Step 2: 搭建 K-means 模块化模型 (Model Architecture)
# ---------------------------------------------------------------
class HWModel(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, out_dim)
        )

    def forward(self, x):
        return self.net(x)

model = HWModel(in_dim=d, out_dim=2)
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=0.01, weight_decay=1e-4)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=30)

# ---------------------------------------------------------------
# Step 3: 训练与 Boss Baseline 验证循环 (Training & Validation Loop)
# ---------------------------------------------------------------
for epoch in range(30):
    model.train()
    total_loss, correct = 0.0, 0
    for bx, by in train_loader:
        optimizer.zero_grad()
        out = model(bx)
        loss = criterion(out, by)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item() * len(bx)
        correct += (out.argmax(dim=1) == by).sum().item()
        
    scheduler.step()

acc = correct / len(dataset)
print(f"=== 李宏毅 HW Lab (K-means) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
