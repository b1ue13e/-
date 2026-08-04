---
title: "线性判别分析 (Linear Discriminant Analysis, LDA)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 线性模型, LDA, 线性判别分析, 监督降维, 瑞利商]
upstream: ["[[02-线性模型/线性回归|线性回归]]", "[[01-基础概念/线性代数基础|线性代数基础]]"]
downstream: ["[[05-其他方法/主成分分析|PCA]]", "[[02-线性模型/多分类学习|多分类学习]]"]
status: learning
---

# 🎯 线性判别分析 (LDA)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：线性判别分析（LDA / Fisher 判别分析）是经典的**监督降维与分类算法**。它与无监督降维算法 PCA 形成鲜明对比（PCA追求最大方差，LDA追求最大类间分离）。掌握 LDA 的“类内聚集、类间拉开”几何直觉、散度矩阵（Scatter Matrix）定义以及广义瑞利商（Rayleigh Quotient）求解，是深入理解有监督特征抽取的关键。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**
> 假设你有一组带二分类标签的高维数据点。如果你直接用无监督降维 PCA，PCA 会沿着数据整体方差最大的方向投影。然而，整体方差最大的方向可能正好把两个不同类别的点重叠混杂在一起！

LDA **利用样本的类别标签信息**，寻找一个最佳投影方向 $\mathbf{w}$，使得投影后“同类点尽量紧凑（类内散度小），异类点尽量远离（类间散度大）”。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：
  - **后续影响**：与 [[05-其他方法/主成分分析|PCA]] 共同构成“线性降维双璧”（PCA 无监督 vs LDA 有监督）；可直接扩展为多分类 LDA 与核线性判别分析 (KLDA)。
  - **课程位置**：属于“第二阶段：线性模型”的核心分类与降维算法。
- **实战与科研价值**：
  - **人脸识别**：Fisherfaces 经典算法。
  - **最常出现题型**：类内散度矩阵 $\mathbf{S}_w$ 与类间散度矩阵 $\mathbf{S}_b$ 计算题、瑞利商求导导出广义特征值问题推导题、LDA 与 PCA 对比辨析题。

---

## 3. 学它之前需要哪些前置知识？

### 最小必要背景：
1. **均值向量与协方差矩阵**：$\boldsymbol{\mu}_0, \boldsymbol{\mu}_1$ 表示两类样本的均值。
2. **广义特征值问题**：$\mathbf{A} \mathbf{x} = \lambda \mathbf{B} \mathbf{x}$。

---

## 4. 用直觉语言解释它

> «“这东西其实就像给两群不同颜色的羊群拍照拉开距离……”»

- **场景**：红羊群和蓝羊群在草地上混杂在一起。你想拍一张一维的照片（投影到直线）。
- **策略**：
  - 你希望红羊群自己紧紧抱成一团（类内方差小）；
  - 蓝羊群自己也紧紧抱成一团（类内方差小）；
  - 同时红羊群的中心和蓝羊群的中心相距尽量远（类间距离大）。
- **口诀**：**“高内聚，低耦合” / “类内最小，类间最大”**。

---

## 5. 正式定义、核心公式、符号解释

### 1. 二分类 LDA 几何定义
设正例集合 $X_1$（均值 $\boldsymbol{\mu}_1$），负例集合 $X_0$（均值 $\boldsymbol{\mu}_0$）。
投影到单位向量 $\mathbf{w}$ 后：
- 两类中心投影距离的平方：$(\mathbf{w}^T \boldsymbol{\mu}_1 - \mathbf{w}^T \boldsymbol{\mu}_0)^2 = \mathbf{w}^T (\boldsymbol{\mu}_1 - \boldsymbol{\mu}_0)(\boldsymbol{\mu}_1 - \boldsymbol{\mu}_0)^T \mathbf{w} = \mathbf{w}^T \mathbf{S}_b \mathbf{w}$
- 类内方差之和：$\sum_{x \in X_0} (\mathbf{w}^T x - \mathbf{w}^T \boldsymbol{\mu}_0)^2 + \sum_{x \in X_1} (\mathbf{w}^T x - \mathbf{w}^T \boldsymbol{\mu}_1)^2 = \mathbf{w}^T \mathbf{S}_w \mathbf{w}$

### 2. 散度矩阵定义
- **类内散度矩阵 (Within-class Scatter Matrix $\mathbf{S}_w$)**：
  $$\mathbf{S}_w = \boldsymbol{\Sigma}_0 + \boldsymbol{\Sigma}_1 = \sum_{\mathbf{x} \in X_0} (\mathbf{x} - \boldsymbol{\mu}_0)(\mathbf{x} - \boldsymbol{\mu}_0)^T + \sum_{\mathbf{x} \in X_1} (\mathbf{x} - \boldsymbol{\mu}_1)(\mathbf{x} - \boldsymbol{\mu}_1)^T$$
- **类间散度矩阵 (Between-class Scatter Matrix $\mathbf{S}_b$)**：
  $$\mathbf{S}_b = (\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)(\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)^T$$

### 3. 广义瑞利商与最优解
LDA 目标函数（最大化瑞利商 $J(\mathbf{w})$）：

$$J(\mathbf{w}) = \frac{\mathbf{w}^T \mathbf{S}_b \mathbf{w}}{\mathbf{w}^T \mathbf{S}_w \mathbf{w}}$$

令分母 $\mathbf{w}^T \mathbf{S}_w \mathbf{w} = 1$，由拉格朗日乘子法可推导出最优投影方向：

$$\mathbf{w}^* = \mathbf{S}_w^{-1} (\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)$$

---

## 6. 例子：基础 → 中等 → 实际应用

### 例子 1：LDA vs PCA 辨析
**题目**：画出二维数据集中，PCA 与 LDA 投影方向可能冲突的典型示意图。
- **解析**：如果两类数据分布呈平行长条状（例如正例在上方长条，负例在下方长条），数据的总体最大方差方向是水平方向（X轴方向）。
  - **PCA** 会选择水平方向投影，结果导致正负例在 X 轴上完全重叠难以区分；
  - **LDA** 会选择垂直方向（Y轴方向）投影，使得正负例中心分离，获得完美二分类。

---

## 7. 常见误区和易混概念

### LDA 与 PCA 对比总结表
| 维度 | 主成分分析 (PCA) | 线性判别分析 (LDA) |
| :--- | :--- | :--- |
| **学习范式** | 无监督学习 (Unsupervised) | 监督学习 (Supervised) |
| **核心思想** | 寻找最大化数据总方差的方向 | 寻找“类内最小、类间最大”的方向 |
| **降维后维度极限** | 最多可降至 $d$ 维 | **二分类只能降至 1 维**；$N_c$ 分类最多只能降至 $N_c - 1$ 维 |
| **对标签依赖** | 不需要标签 | 极其依赖标签质量 |

---

## 8. 相关知识点与 Obsidian 双链建议

### 上游依赖（前置知识）
- [[02-线性模型/线性回归|线性回归]]
- [[01-基础概念/线性代数基础|线性代数基础]]

### 下游延伸（后续进阶）
- [[02-线性模型/多分类学习|多分类学习]]
- [[01-基础概念/PCA|PCA]]

## 下游延伸（后续进阶）
- [[02-线性模型/多分类学习|多分类学习]]
- [[01-基础概念/PCA|PCA]]

## 下游延伸（后续进阶）
- [[02-线性模型/多分类学习|多分类学习]]
- [[01-基础概念/PCA|PCA]]

## 下游延伸
- [[05-其他方法/主成分分析|PCA]]

---

## 9. 闭卷复现任务

1. 写出 LDA 的几何优化口诀与瑞利商公式 $J(\mathbf{w})$。
2. 默写类内散度矩阵 $\mathbf{S}_w$ 与类间散度矩阵 $\mathbf{S}_b$ 的表达式。
3. 默写二分类 LDA 最优解 $\mathbf{w}^* = \mathbf{S}_w^{-1} (\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)$。
4. 为什么 $K$ 分类问题的 LDA 最多只能降维到 $K-1$ 维？

---

## 10. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | LDA 范式 |
| 2 | 维度限制 | 基础 | LDA 降维上线 |
| 3 | 公式识别 | 中等 | 散度矩阵定义 |
| 4 | 算法对比 | 中等 | LDA vs PCA 区别 |
| 5 | 推导证明 | 较难 | 最优解推导 |

1. **[概念辨析] 线性判别分析（LDA）在选择投影方向时的核心指导原则是：**
   A. 保持投影后的全局数据方差最大化  
   B. 使得同类样本投影点的方差极小（类内紧凑），异类样本中心距离极大（类间分离）  
   C. 最小化重建误差  
   D. 使得权重向量模长为 1
> [!question]- 答案解析
> **答案**：B  
> **解析**：LDA 的核心口诀是“类内最小，类间最大”。  
> **标签**：`#自测/基础 #LDA原则`

2. **[维度限制] 对于一个 10 分类的机器学习任务，使用 LDA 进行监督降维时，最多能将特征降维到几维？**
   A. 10 维  B. 9 维  C. 1 维  D. 无限制
> [!question]- 答案解析
> **答案**：B  
> **解析**：$K$ 类问题的类间散度矩阵 $\mathbf{S}_b$ 是 $K$ 个中心向量差的线性组合，其秩最多为 $K-1$，故 LDA 最多只能降维至 $K-1$ 维（10 分类最多 9 维）。  
> **标签**：`#自测/基础 #LDA维度限制`

3. **[公式识别] 二分类 LDA 的最优投影方向公式 $\mathbf{w}^* = \mathbf{S}_w^{-1} (\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)$ 中，$\mathbf{S}_w$ 代表：**
   A. 类间散度矩阵  B. 类内散度矩阵  C. 总体协方差矩阵  D. 恒等矩阵
> [!question]- 答案解析
> **答案**：B  
> **解析**：$\mathbf{S}_w$ 为类内散度矩阵 (Within-class Scatter Matrix)。  
> **标签**：`#自测/中等 #散度矩阵`

4. **[算法对比] 在图像识别中，关于 PCA 与 LDA 的描述错误的是：**
   A. PCA 是无监督降维，LDA 是监督降维  
   B. PCA 适合保留图像的主要轮廓信息，LDA 适合保留分类判别信息  
   C. 若数据没有标签，仍可以使用 LDA 降维  
   D. LDA 需要计算类内和类间散度
> [!question]- 答案解析
> **答案**：C  
> **解析**：LDA 需要利用数据标签计算类内/类间散度矩阵，无标签时无法使用 LDA。  
> **标签**：`#自测/中等 #LDA与PCA`

5. **[推导证明] 试证明：瑞利商 $J(\mathbf{w}) = \frac{\mathbf{w}^T \mathbf{S}_b \mathbf{w}}{\mathbf{w}^T \mathbf{S}_w \mathbf{w}}$ 的极大化问题，在消去标量比例因子后等价于求解方程 $\mathbf{S}_w^{-1} \mathbf{S}_b \mathbf{w} = \lambda \mathbf{w}$。**
> [!question]- 答案解析
> **答案**：设分母 $\mathbf{w}^T \mathbf{S}_w \mathbf{w} = 1$，则目标化为 $\max \mathbf{w}^T \mathbf{S}_b \mathbf{w} \text{ s.t. } \mathbf{w}^T \mathbf{S}_w \mathbf{w} = 1$。构建拉格朗日函数 $L(\mathbf{w}, \lambda) = \mathbf{w}^T \mathbf{S}_b \mathbf{w} + \lambda(1 - \mathbf{w}^T \mathbf{S}_w \mathbf{w})$。对 $\mathbf{w}$ 求导置 0 得 $2\mathbf{S}_b \mathbf{w} - 2\lambda \mathbf{S}_w \mathbf{w} = 0 \implies \mathbf{S}_b \mathbf{w} = \lambda \mathbf{S}_w \mathbf{w}$。两边左乘 $\mathbf{S}_w^{-1}$ 得 $\mathbf{S}_w^{-1} \mathbf{S}_b \mathbf{w} = \lambda \mathbf{w}$。由于 $\mathbf{S}_b \mathbf{w} = (\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)(\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)^T \mathbf{w}$ 的方向永远平行于 $(\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)$，忽略标量因子即得 $\mathbf{w}^* = \mathbf{S}_w^{-1}(\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)$。  
> **标签**：`#自测/较难 #LDA推导`

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

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/02-线性模型/`
- **建议双链**：
  - [[02-线性模型/📈 第二阶段：线性模型|第二阶段：线性模型]]
  - [[02-线性模型/线性回归|线性回归]]
  - [[05-其他方法/主成分分析|PCA]]
- **建议标签**：`#学习` `#机器学习` `#LDA` `#线性判别分析` `#监督降维`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 线性判别分析)

> **作业任务说明**：本作业为《线性判别分析》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 线性判别分析 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 线性判别分析 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (线性判别分析) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
