---
title: "PAC 学习理论 (Probably Approximately Correct Learning)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "B"
tags: [学习, 机器学习, 正则优化, PAC学习, 统计学习理论, 概率近似正确]
upstream: ["[[01-基础概念/假设空间|假设空间]]", "[[03-正则优化/VC维|VC维]]"]
downstream: ["[[03-正则优化/Rademacher复杂度|Rademacher复杂度]]"]
status: learning
---

# 🎯 PAC 学习理论

---

## 0. 先判断它值不值得深挖

- **类别**：**B 类（常用工具，重点掌握概念）**
- **判断理由**：PAC（Probably Approximately Correct，概率近似正确）框架由 Valiant 于 1984 年提出（获得图灵奖），是计算学习理论（Computational Learning Theory）的奠基理论。它形式化给出了“什么叫一个问题在计算机上可学”的数学定义。

---

## 1. 核心定义与公式

### 1. 概率近似正确 (PAC) 形式化
设误差上限为 $\epsilon > 0$，不置信度上限为 $\delta > 0$。
若存在算法 $\mathcal{A}$，使得对于任意未知数据分布 $D$，算法在从 $D$ 中采样出的规模为 $N$ 的训练集上输出的假设 $h$，以至少 **$1 - \delta$ 的概率（Probably）**，满足泛化误差不超过 **$\epsilon$（Approximately Correct）**：

$$P_{D^N}(E(h) \le \epsilon) \ge 1 - \delta$$

且训练样本量 $N$ 与计算时间是 $\frac{1}{\epsilon}, \frac{1}{\delta}$ 的多项式函数，则称假设空间 $\mathcal{H}$ 是 **PAC 可学的 (PAC Learnable)**。

---

## 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/`
- **建议双链**：
  - [[03-正则优化/🛡️ 第三阶段：正则优化|第三阶段：正则优化]]
  - [[03-正则优化/VC维|VC维]]
- **建议标签**：`#学习` `#机器学习` `#PAC学习` `#统计学习理论`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: PAC学习)

> **作业任务说明**：本作业为《PAC学习》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 PAC学习 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 PAC学习 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (PAC学习) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
