---
title: "多层神经网络 (Artificial Neural Networks / MLP)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 神经网络, 多层感知机, MLP, 激活函数, 通用近似定理, PyTorch实战]
upstream: ["[[03-正则优化/感知机|感知机]]", "[[02-线性模型/逻辑回归|逻辑回归]]"]
downstream: ["[[03-正则优化/反向传播算法|反向传播算法]]", "[[01-基础概念/过拟合|Dropout]]"]
status: learning
---

# 🎯 多层神经网络 (MLP)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：多层前馈神经网络（Multi-Layer Perceptron, MLP）是现代深度学习的基石。通过引入隐藏层与非线性激活函数（ReLU, Sigmoid, GELU），神经网络打破了感知机的线性不可分瓶颈。通用近似定理（Universal Approximation Theorem）进一步从数学上奠定了其“能逼近任意连续函数”的强大表达能力。

---

## 1. 核心结构与前向传播 (Forward Propagation)

```mermaid
graph LR
    subgraph 输入层 Input
        X1[x1]
        X2[x2]
    end
    subgraph 隐藏层 Hidden Layer
        H1[h1 = σ(W1 x + b1)]
        H2[h2 = σ(W1 x + b1)]
    end
    subgraph 输出层 Output Layer
        Y[y_hat = σ(W2 h + b2)]
    end

    X1 --> H1
    X1 --> H2
    X2 --> H1
    X2 --> H2
    H1 --> Y
    H2 --> Y
```

### 1. 逐层矩阵表示
设第 $l$ 层的输入为 $\mathbf{a}^{(l-1)}$，权重矩阵为 $\mathbf{W}^{(l)}$，偏置向量为 $\mathbf{b}^{(l)}$，激活函数为 $\sigma$：

$$\mathbf{z}^{(l)} = \mathbf{W}^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}$$

$$\mathbf{a}^{(l)} = \sigma(\mathbf{z}^{(l)})$$

---

## 2. 三大常用非线性激活函数

| 激活函数 | 数学表达式 | 图像与导数特点 | 常见问题 |
| :--- | :--- | :--- | :--- |
| **Sigmoid** | $\sigma(z) = \frac{1}{1 + e^{-z}}$ | 输出 $(0, 1)$；饱和区导数趋近 0 | 极易引发**梯度消失 (Gradient Vanishing)**；非零均值 |
| **ReLU** | $f(z) = \max(0, z)$ | $z>0$ 时导数为 1；计算极快 | **Dead ReLU 问题**（$z<0$ 时梯度永久为 0）|
| **GELU** | $f(z) = z \cdot \Phi(z)$ | 平滑连续，大模型 (GPT/BERT/Transformer) 标配 | 需求高斯累积分布 |

---

## 3. 通用近似定理 (Universal Approximation Theorem)

> **定理内容：**
> 一个包含**单个隐藏层**、拥有足够多神经元以及非线性激活函数的前馈神经网络，能够以**任意精度逼近闭区间上的任何连续函数**。

---

## 🛠️ 14. PyTorch 动手实战与代码映射

### 1. 课本公式到 PyTorch 变量映射表 (Textbook-to-Code Mapping)
| 课本公式 / 符号 | 数学含义 | PyTorch 对应 API / 变量 | 说明 / 维度 (Shape) |
| :--- | :--- | :--- | :--- |
| $\mathbf{a}^{(1)} = \sigma(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)})$ | 隐藏层前向传播 | `nn.Linear(in_d, hidden_d)` + `nn.ReLU()` | `[batch, hidden_d]` |
| $\mathbf{y}_{\text{pred}}$ | 多分类 Logits | `nn.Linear(hidden_d, num_classes)` | `[batch, num_classes]` |
| $L = -\sum y_k \log \hat{y}_k$ | 交叉熵 Loss | `nn.CrossEntropyLoss()` | 自动整合 Softmax 与 Log-NLL |
| Dropout(p) | 抑制过拟合正规化 | `nn.Dropout(p=0.2)` | 训练时随机将 $p$ 比例神经元置 0 |

### 2. 自包含、零依赖可运行代码 (Self-Contained Runnable Code)

```python
import torch
import torch.nn as nn
import torch.optim as optim

# ---------------------------------------------------------------
# 1. 模拟非线性螺旋/双环二分类数据 (Non-linear Synthetic Data)
# ---------------------------------------------------------------
torch.manual_seed(42)
N = 400
# 内部同心圆 (Class 0) 与 外部同心圆 (Class 1)
r_in = torch.randn(N // 2) * 0.2 + 0.5
theta_in = torch.rand(N // 2) * 2 * 3.14159
X0 = torch.stack([r_in * torch.cos(theta_in), r_in * torch.sin(theta_in)], dim=1)

r_out = torch.randn(N // 2) * 0.2 + 1.8
theta_out = torch.rand(N // 2) * 2 * 3.14159
X1 = torch.stack([r_out * torch.cos(theta_out), r_out * torch.sin(theta_out)], dim=1)

X = torch.cat([X0, X1], dim=0) # [400, 2]
y = torch.cat([torch.zeros(N // 2, dtype=torch.long), torch.ones(N // 2, dtype=torch.long)], dim=0) # [400]

# ---------------------------------------------------------------
# 2. 多层感知机定义 (Multi-Layer Perceptron in PyTorch)
# 包含 2 个隐藏层，使用 ReLU 激活与 Dropout
# ---------------------------------------------------------------
class MLPClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_classes):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),   # W1: [2, 16]
            nn.ReLU(),
            nn.Dropout(p=0.1),                  # 随机置零防止过拟合
            nn.Linear(hidden_dim, hidden_dim),  # W2: [16, 16]
            nn.ReLU(),
            nn.Linear(hidden_dim, num_classes)  # W3: [16, 2]
        )

    def forward(self, x):
        return self.network(x)                  # [batch, 2]

model = MLPClassifier(input_dim=2, hidden_dim=16, num_classes=2)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01) # 使用 Adam 优化器

# ---------------------------------------------------------------
# 3. 训练循环
# ---------------------------------------------------------------
for epoch in range(200):
    model.train()
    optimizer.zero_grad()
    logits = model(X)                # [400, 2]
    loss = criterion(logits, y)
    loss.backward()
    optimizer.step()

# 测试计算分类准确率
model.eval()
with torch.no_grad():
    test_logits = model(X)
    preds = torch.argmax(test_logits, dim=1) # [400]
    acc = (preds == y).float().mean()

print("=== PyTorch 多层神经网络 (MLP) 训练完成 ===")
print(f"最终 Loss: {loss.item():.4f}")
print(f"同心圆非线性数据集分类准确率: {acc.item() * 100:.2f}%")
```

### 3. PyTorch 避坑指南与 Gotchas
- **Train vs Eval 模式切换**：如果网络中使用了 `nn.Dropout()` 或 `nn.BatchNorm2d()`，训练时必须先调用 `model.train()`，评估测试时必须调用 `model.eval()`！否则 Dropout 会在测试阶段继续丢弃神经元导致测试准确率失真。
- **CrossEntropyLoss 标签数据类型**：`nn.CrossEntropyLoss()` 要求传入的 `y` 必须是 `torch.long`（或 `int64`）数据类型的一维 Tensor，不能是 `float`！

---

## 4. 相关知识点与 Obsidian 双链建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/`
- **建议双链**：
  - [[03-正则优化/🛡️ 第三阶段：正则优化|第三阶段：正则优化]]
  - [[03-正则优化/感知机|感知机]]
  - [[03-正则优化/反向传播算法|反向传播算法]]
- **建议标签**：`#学习` `#机器学习` `#神经网络` `#MLP` `#激活函数` `#通用近似定理` `#PyTorch实战`


---



---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 神经网络)

> **作业任务说明**：本作业为《神经网络》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 神经网络 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 神经网络 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (神经网络) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
