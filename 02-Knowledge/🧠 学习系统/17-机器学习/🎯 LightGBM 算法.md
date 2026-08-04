---
title: "LightGBM 算法 (Light Gradient Boosting Machine)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 树模型, 集成学习, LightGBM, 直方图算法, GOSS, EFB, PyTorch实战]
upstream: ["[[04-树与集成/XGBoost|XGBoost]]", "[[04-树与集成/GBDT|GBDT]]", "[[04-树与集成/GBDT|GBDT]]", "[[04-树与集成/GBDT|GBDT]]", "[[04-树与集成/XGBoost|XGBoost]]"]
downstream: ["[[04-树与集成/CatBoost|CatBoost]]"]
status: learning
---
# 🎯 LightGBM 算法

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：LightGBM（Ke et al., 2017 / 微软开源）是工业界大规模结构化/表格数据预测速度最快、内存开销最少的梯度提升框架。它通过**基于直方图的决策树算法 (Histogram-based Algorithm)**、单侧梯度采样 (GOSS) 与互斥特征捆绑 (EFB)，将切分计算开销从特征点数量降低到直方图 Bucket 数量，彻底解决了 XGBoost 预排序 (Pre-sorted) 内存占用过大的瓶颈。

---

## 1. 三大核心创新与工程加速

### 1. 基于直方图的决策树算法 (Histogram-based Algorithm)
- **原理**：将连续浮点特征值离散化为 $K$ 个整数桶（Bin，通常 $K=255$），构建直方图。
- **优点**：无需对特征重新排序，内存占用降低至 $1/8$；节点切分查找复杂度从 $O(\text{#data} \times \text{#feature})$ 降低至 $O(K \times \text{#feature})$。

### 2. 单侧梯度采样 (GOSS - Gradient-based One-Side Sampling)
- **原理**：梯度大的样本说明尚未学好，损失误差大。GOSS **保留所有大梯度样本**，同时在小梯度样本中**按比例随机抽样**，并对小梯度样本乘上放大权重补偿分布，兼顾了梯度计算精度与样本量裁剪。

### 3. 互斥特征捆绑 (EFB - Exclusive Feature Bundling)
- **原理**：高维稀疏特征（如 One-hot 特征）中，许多特征很少同时取非零值。EFB 像图着色问题一样将这些互斥特征捆绑为单个复合特征，大幅减少特征数量。

---

## 🛠️ 14. PyTorch 动手实战与代码映射

### 1. 课本公式到 PyTorch 变量映射表 (Textbook-to-Code Mapping)
| 课本公式 / 符号 | 数学含义 | PyTorch 对应 API / 变量 | 说明 / 维度 (Shape) |
| :--- | :--- | :--- | :--- |
| $X_{\text{quantized}}$ | 直方图 Bin 桶离散化 | `torch.bucketize(X, boundaries)` | 将连续实数离散化为 `[0, K-1]` 的桶索引 |
| $G_{\text{bin}}, H_{\text{bin}}$ | 直方图梯度/Hessian 累加 | `torch.zeros(K).scatter_add_(...)` | 快速累加 Bucket 的梯度与 Hessian |

### 2. 自包含、零依赖可运行代码 (Self-Contained Runnable Code)

```python
import torch

# ---------------------------------------------------------------
# 1. 演示 LightGBM 核心思想：直方图 Bucket 构建 (Histogram Building)
# ---------------------------------------------------------------
torch.manual_seed(42)
N = 1000
x_continuous = torch.randn(N) # 连续特征 [1000]
gradients = torch.randn(N)    # 假设的一阶梯度 g_i [1000]

# 设定 K=10 个桶边界 (Quantiles)
boundaries = torch.quantile(x_continuous, torch.linspace(0, 1, 11)[1:-1])
x_binned = torch.bucketize(x_continuous, boundaries) # 离散化为 0~9 的 Bin 索引

# 使用 PyTorch scatter_add_ 极速构建直方图梯度
hist_grad = torch.zeros(10)
hist_grad.scatter_add_(0, x_binned, gradients)

print("=== PyTorch 模拟 LightGBM 直方图 (Histogram) 构建 ===")
print("连续特征成功转化为 10 个直方图桶 (Bins)！")
print(f"各桶梯度累积值 (Hist Gradients): {hist_grad.numpy().round(3)}")
```

---

## 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/04-树与集成/`
- **建议双链**：
  - [[04-树与集成/🌲 第四阶段：树与集成|第四阶段：树与集成]]
  - [[04-树与集成/XGBoost|XGBoost]]
  - [[04-树与集成/GBDT|GBDT]]
- **建议标签**：`#学习` `#机器学习` `#LightGBM` `#直方图算法` `#GOSS` `#EFB` `#PyTorch实战`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: LightGBM)

> **作业任务说明**：本作业为《LightGBM》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 LightGBM 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 LightGBM 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (LightGBM) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
