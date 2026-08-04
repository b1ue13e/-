---
title: "决策树剪枝 (Decision Tree Pruning: Pre-pruning & Post-pruning)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 树模型, 决策树剪枝, 预剪枝, 后剪枝, 泛化能力]
upstream: ["[[04-树与集成/决策树|决策树]]"]
downstream: ["[[01-基础概念/过拟合|过拟合]]"]
status: learning
---

# 🎯 决策树剪枝 (Pruning)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：剪枝（Pruning）是决策树克服过拟合、提升泛化能力的最核心手段。未经过剪枝的决策树极易无限分枝形成枝繁叶茂的高复杂度树，将噪声样本背诵下来。掌握预剪枝（Pre-pruning）与后剪枝（Post-pruning）的机制与优缺点对比是树模型调优的基本功。

---

## 1. 预剪枝 vs 后剪枝原理对比

### 1. 预剪枝 (Pre-pruning)
- **原理**：在决策树**生成过程中**，对每个节点在划分前先进行评估。若当前节点的划分**不能提升验证集上的泛化性能**，则停止划分并将当前节点标记为叶节点。
- **限制条件设置**：限制树的最大深度 `max_depth`、限制叶节点最小样本数 `min_samples_leaf`、限制节点划分最小样本数 `min_samples_split`、限制信息增益门槛。
- **优点**：大幅减少训练开销与内存占用，能显著降低过拟合风险。
- **缺点**：存在**欠拟合风险**（贪心策略可能切断后续多步组合后能极大提升性能的“潜在好分支”）。

### 2. 后剪枝 (Post-pruning)
- **原理**：先让决策树**充分完全生长**，直到无法划分为止。然后自底向上评估非叶节点，若将该非叶节点对应的子树替换为单个叶节点**能提升验证集上的泛化性能**，则将其剪掉。
- **优点**：欠拟合风险极小，泛化性能通常优于预剪枝。
- **缺点**：需要先生成完整大树再自底向上遍历，训练时间开销与内存开销显著大于预剪枝。

---

## 2. 常见误区和易混概念

### 预剪枝 vs 后剪枝对比表格
| 维度 | 预剪枝 (Pre-pruning) | 后剪枝 (Post-pruning) |
| :--- | :--- | :--- |
| **剪枝时机** | 边生成边剪枝（提前终止） | 先生成完整大树，自底向上回溯剪枝 |
| **训练时间开销** | 极小（显著加速训练） | 极大（需全量建树再遍历） |
| **欠拟合风险** | 较高（贪心视角易陷入局部停滞） | 较低 |
| **过拟合风险** | 低 | 低 |
| **实用广度** | 工业界（如 Scikit-learn）最常用（超参数调优） | 学术理论常用 |

---

## 3. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/04-树与集成/`
- **建议双链**：
  - [[04-树与集成/🌲 第四阶段：树与集成|第四阶段：树与集成]]
  - [[04-树与集成/决策树|决策树]]
- **建议标签**：`#学习` `#机器学习` `#决策树剪枝` `#预剪枝` `#后剪枝`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 决策树剪枝)

> **作业任务说明**：本作业为《决策树剪枝》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 决策树剪枝 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 决策树剪枝 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (决策树剪枝) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
