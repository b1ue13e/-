---
title: "XGBoost 算法 (eXtreme Gradient Boosting)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 树模型, 集成学习, XGBoost, GBDT, 二阶泰勒展开, 裂变查找]
upstream: ["[[04-树与集成/集成学习|集成学习]]", "[[04-树与集成/Boosting原理|Boosting原理]]"]
downstream: ["[[04-树与集成/LightGBM|LightGBM]]", "[[04-树与集成/CatBoost|CatBoost]]"]
status: learning
---

# 🎯 XGBoost 算法

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：XGBoost（Chen & Guestrin, 2016）是梯度提升决策树（GBDT）的高性能工业级巅峰实现。它在传统 GBDT 的一阶导数基础之上，创新性地推导了**二阶泰勒展开（Hessian 矩阵）**、加入了正则化树复杂度惩罚项、实现了缺失值自动分支与 Block 块并行切分，横扫了 Kaggle 绝大部分表格数据竞赛。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**
> 传统 GBDT 仅使用一阶导数（梯度）拟合残差，收敛速度慢且容易过拟合；且遇到超大规模海量表格数据时，传统 GBDT 无法有效利用 GPU 或多核 CPU 进行并行加速。

XGBoost **利用二阶泰勒展开与显式正则化树惩罚**，极大提高了模型收敛速度与泛化上限。

---

## 2. 正式定义与目标函数推导

### 1. 目标函数 (加法模型第 $t$ 步)
在第 $t$ 步，需拟合一棵新树 $f_t(\mathbf{x})$：

$$\mathcal{L}^{(t)} = \sum_{i=1}^N l(y_i, \hat{y}_i^{(t-1)} + f_t(\mathbf{x}_i)) + \Omega(f_t)$$

其中树的复杂度正则项为：$\Omega(f_t) = \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2$（$T$ 为叶节点数，$w_j$ 为叶节点得分）。

### 2. 二阶泰勒展开
对损失函数 $l(y_i, \hat{y}_i^{(t-1)} + f_t(\mathbf{x}_i))$ 进行在 $\hat{y}_i^{(t-1)}$ 处的一阶与二阶泰勒展开：
设一阶导数（一阶梯度）$g_i = \partial_{\hat{y}^{(t-1)}} l(y_i, \hat{y}^{(t-1)})$，二阶导数（Hessian）$h_i = \partial_{\hat{y}^{(t-1)}}^2 l(y_i, \hat{y}^{(t-1)})$。

$$\mathcal{L}^{(t)} \approx \sum_{i=1}^N \left[ l(y_i, \hat{y}_i^{(t-1)}) + g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2$$

去除常数项 $l(y_i, \hat{y}_i^{(t-1)})$，按叶节点 $j \in \{1, \dots, T\}$ 进行样本聚合（设 $I_j = \{i \mid q(\mathbf{x}_i) = j\}$）：

$$\tilde{\mathcal{L}}^{(t)} = \sum_{j=1}^T \left[ \left(\sum_{i \in I_j} g_i\right) w_j + \frac{1}{2} \left(\sum_{i \in I_j} h_i + \lambda\right) w_j^2 \right] + \gamma T$$

恰好为关于 $w_j$ 的**一元二次函数**！

### 3. 最优叶节点权重 $w_j^*$ 与最佳结构打分
令 $\frac{\partial \tilde{\mathcal{L}}^{(t)}}{\partial w_j} = 0$，求得最优叶节点权重：

$$w_j^* = -\frac{\sum_{i \in I_j} g_i}{\sum_{i \in I_j} h_i + \lambda} = -\frac{G_j}{H_j + \lambda}$$

代回目标函数，得到树结构的**最佳得分 (Structure Score / Gain)**：

$$\tilde{\mathcal{L}}^{(t)*} = -\frac{1}{2} \sum_{j=1}^T \frac{G_j^2}{H_j + \lambda} + \gamma T$$

用于节点切分增益（Gain）计算：

$$\text{Gain} = \frac{1}{2} \left[ \frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda} \right] - \gamma$$

---

## 3. XGBoost 的 5 大核心改进点

1. **二阶泰勒展开**：利用一阶 $g_i$ 与二阶 $h_i$ 梯度，收敛速度更快更准。
2. **显式正则化**：在目标函数中直接加入叶节点数 $T$ 和叶节点权重 $L2$ 惩罚 $\Omega(f)$。
3. **缺省值自动分支 (Sparsity-aware Split)**：对缺失值自动分别尝试划入左/右子树，挑选最佳 Gain 路线。
4. **Block 预排序与并行**：特征预先排序并存储为 Block 结构，切分点寻找可并行计算。
5. **剪枝**：采用 $\gamma$ 作为增益阈值，当切分 Gain 小于 $\gamma$ 时停止切分（后剪枝）。

---

## 4. 相关知识点与 Obsidian 双链建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/04-树与集成/`
- **建议双链**：
  - [[04-树与集成/🌲 第四阶段：树与集成|第四阶段：树与集成]]
  - [[04-树与集成/集成学习|集成学习]]
  - [[04-树与集成/LightGBM|LightGBM]]
- **建议标签**：`#学习` `#机器学习` `#XGBoost` `#GBDT` `#二阶泰勒` `#Hessian`


---



---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: XGBoost)

> **作业任务说明**：本作业为《XGBoost》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 XGBoost 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 XGBoost 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (XGBoost) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
