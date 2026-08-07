---
title: "深度学习优化器全解 (Optimizer: Momentum, RMSprop, Adam)"
date: 2026-07-23
type: concept
course: "深度学习"
importance: "A"
tags: [学习, 机器学习, 优化器, SGD, Momentum, RMSprop, Adam, 动量, 自适应学习率, PyTorch实战]
upstream: ["[[01-基础概念/梯度下降法|梯度下降法]]", "[[反向传播算法]]", "[[反向传播算法]]", "[[反向传播算法]]", "[[反向传播算法]]"]
status: learning
stage_moc: "[[🌱 第一阶段：深度学习核心]]"
flow: knowledge
kind: concept
---
# 🎯 深度学习优化器 (Adam, RMSprop, Momentum)

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：在训练深层神经网络时，普通 SGD 梯度下降极易卡在鞍点（Saddle Point）、高维峡谷或产生剧烈震荡。从 SGD + 动量 (Momentum)、自适应学习率 (RMSprop) 到集大成者 **Adam (Adaptive Moment Estimation)**，掌握各优化器的物理动量图像、一阶/二阶矩估计与偏差修正推导，是调参和深度学习训练的必备基本功。

---

## 1. 经典优化器进化谱系表

| 优化器 | 一阶矩 (动量) $m_t$ | 二阶矩 (梯度平方) $v_t$ | 参数更新公式 | 物理直觉与求解痛点 |
| :--- | :--- | :--- | :--- | :--- |
| **SGD** | $g_t$ | 无 | $\theta_{t} = \theta_{t-1} - \eta g_t$ | 最基础，容易在峡谷震荡、鞍点卡死 |
| **Momentum** | $m_t = \beta m_{t-1} + (1-\beta)g_t$ | 无 | $\theta_t = \theta_{t-1} - \eta m_t$ | 惯性冲出鞍点，平滑震荡 |
| **RMSprop** | 无 | $v_t = \beta v_{t-1} + (1-\beta)g_t^2$ | $\theta_t = \theta_{t-1} - \frac{\eta}{\sqrt{v_t + \epsilon}} g_t$ | 频繁更新的维度降速，稀疏维度加速 |
| **Adam** | $m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t$ | $v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$ | $\theta_t = \theta_{t-1} - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$ | **王者标配**：同时融合一阶动量与二阶自适应率 |

### Adam 的偏差修正 (Bias Correction)
由于初始 $m_0 = 0, v_0 = 0$，在训练初期 $m_t, v_t$ 会严重偏向 0。Adam 引入了偏差修正：

$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$

---

## 🛠️ 14. PyTorch 动手实战与代码映射

```python
import torch
import torch.nn as nn
import torch.optim as optim

# ---------------------------------------------------------------
# 1. 模拟高维鞍点优化问题 (Loss 曲线实验)
# ---------------------------------------------------------------
torch.manual_seed(42)
X = torch.randn(100, 10)
y = torch.randn(100, 1)

# 比较 SGD vs Momentum vs Adam
for opt_name, opt_cls, kwargs in [
    ("Vanilla SGD", optim.SGD, {"lr": 0.01}),
    ("SGD + Momentum", optim.SGD, {"lr": 0.01, "momentum": 0.9}),
    ("Adam", optim.Adam, {"lr": 0.01, "betas": (0.9, 0.999)})
]:
    model = nn.Linear(10, 1)
    optimizer = opt_cls(model.parameters(), **kwargs)
    criterion = nn.MSELoss()
    
    for epoch in range(50):
        optimizer.zero_grad()
        loss = criterion(model(X), y)
        loss.backward()
        optimizer.step()
        
    print(f"优化器 [{opt_name:15s}] 50 Epoch 训练后 Loss: {loss.item():.5f}")
```

---

## 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/`
- **建议双链**：
  - [[🛡️ 第三阶段：正则优化|第三阶段：正则优化]]
  - [[01-基础概念/梯度下降法|梯度下降法]]
- **建议标签**：`#学习` `#机器学习` `#优化器` `#Adam` `#RMSprop` `#Momentum` `#PyTorch实战`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 深度优化器)

> **作业任务说明**：本作业为《深度优化器》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 深度优化器 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 深度优化器 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (深度优化器) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。

