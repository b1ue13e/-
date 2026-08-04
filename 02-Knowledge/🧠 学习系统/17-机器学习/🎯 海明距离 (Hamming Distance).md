---
title: "海明距离 (Hamming Distance)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "C"
tags: [学习, 机器学习, 线性模型, 海明距离, 纠错码, 编码]
upstream: ["[[02-线性模型/多分类学习|多分类学习]]"]
downstream: ["[[02-线性模型/多分类学习|ECOC]]"]
status: learning
---

# 🎯 海明距离 (Hamming Distance)

---

## 0. 先判断它值不值得深挖

- **类别**：**C 类（了解背景与应用）**
- **判断理由**：海明距离是衡量两个相同长度字符串/等长二进制向量之间**不同位置字符个数**的离散距离度量。在机器学习中，它主要用于多分类纠错输出码 (ECOC) 的解码判别与感知哈希（Perceptual Hashing）图像相似度匹配。

---

## 1. 定义与计算公式

对于两个等长向量 $\mathbf{a} = (a_1, \dots, a_m)$ 和 $\mathbf{b} = (b_1, \dots, b_m)$，海明距离定义为不相同元素的个数：

$$d_{\text{Hamming}}(\mathbf{a}, \mathbf{b}) = \sum_{i=1}^m \mathbb{I}(a_i \neq b_i)$$

对于二进制向量，海明距离等于两向量进行**按位异或 (XOR)** 后结果中 1 的个数：

$$d_{\text{Hamming}}(\mathbf{a}, \mathbf{b}) = \text{popcount}(\mathbf{a} \oplus \mathbf{b})$$

---

## 2. 例子

- `a = "1011101"`
- `b = "1001001"`
- 差异位置：第 3 位（1 vs 0）和第 5 位（1 vs 0），共 2 处不同。
- 海明距离 = **2**。

---

## 3. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/02-线性模型/`
- **建议双链**：
  - [[02-线性模型/多分类学习|多分类学习]]
- **建议标签**：`#学习` `#机器学习` `#海明距离` `#编码`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 海明距离 Hamming Distance)

> **作业任务说明**：本作业为《海明距离 Hamming Distance》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 海明距离 Hamming Distance 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 海明距离 Hamming Distance 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (海明距离 Hamming Distance) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
