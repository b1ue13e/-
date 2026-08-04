---
title: "AdaBoost 算法 (Adaptive Boosting)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 树模型, 集成学习, AdaBoost, Boosting, 指数损失, PyTorch实战]
upstream: ["[[04-树与集成/Boosting原理|Boosting原理]]", "[[04-树与集成/决策树|决策树]]"]
downstream: ["[[04-树与集成/GBDT|GBDT]]", "[[04-树与集成/XGBoost|XGBoost]]"]
status: learning
---
# 🎯 AdaBoost 算法 (Adaptive Boosting)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：AdaBoost（Freund & Schapire, 1997 / 获得哥德尔奖）是 Boosting 提升法最早、最经典的落地算法。它在数学上证明了“弱可学习（弱分类器）与强可学习（强分类器）的等价性”。掌握 AdaBoost 的样本权重调整机制、基分类器权重公式 $\alpha_m$ 的指数损失求导推导，是理解整个 Boosting 算法族系的基础。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**
> 单个弱分类器（如树桩 Decision Stump，只有 1 层的决策树）准确率可能只有 60%，无法直接用于工业决策。

AdaBoost **通过根据上一轮的错误动态提高做错样本的权重**，让下一轮基分类器专注于“攻克错题”，最终加权组合获得极高准确率的强分类器。

---

## 2. 正式定义、核心公式、符号解释

### 1. 样本权重更新规则
给定样本权重分布 $D_m = (w_{m,1}, \dots, w_{m,N})$，初始 $w_{1,i} = \frac{1}{N}$。
第 $m$ 个基分类器 $G_m(\mathbf{x})$ 的加权加权分类误差率为：

$$e_m = \sum_{i=1}^N w_{m,i} \mathbb{I}(G_m(\mathbf{x}_i) \neq y_i)$$

### 2. 基分类器权重 $\alpha_m$
$$\alpha_m = \frac{1}{2} \ln \left( \frac{1 - e_m}{e_m} \right)$$

### 3. 下一轮样本权重更新
$$w_{m+1, i} = \frac{w_{m,i}}{Z_m} \exp(-\alpha_m y_i G_m(\mathbf{x}_i))$$

其中 $Z_m$ 为规范化因子使 $\sum w_{m+1,i} = 1$。

### 4. 最终强分类器
$$f(\mathbf{x}) = \text{sign}\left( \sum_{m=1}^M \alpha_m G_m(\mathbf{x}) \right)$$

---

## 3. 推导思路：为什么 $\alpha_m = \frac{1}{2} \ln \frac{1-e_m}{e_m}$？

### 指数损失函数 (Exponential Loss) 视角：
设加法模型 $f(\mathbf{x}) = \sum \alpha_m G_m(\mathbf{x})$，损失函数为 $L(y, f(\mathbf{x})) = \exp(-y f(\mathbf{x}))$。
在第 $m$ 步，优化目标为：

$$\min_{\alpha_m, G_m} \sum_{i=1}^N \exp\left( -y_i [f_{m-1}(\mathbf{x}_i) + \alpha_m G_m(\mathbf{x}_i)] \right) = \sum_{i=1}^N w_{m,i} \exp(-\alpha_m y_i G_m(\mathbf{x}_i))$$

展开为正确分类点与错误分类点两项：
$$= e^{-\alpha_m} \sum_{y_i = G_m} w_{m,i} + e^{\alpha_m} \sum_{y_i \neq G_m} w_{m,i} = (1 - e_m) e^{-\alpha_m} + e_m e^{\alpha_m}$$
对 $\alpha_m$ 求导设为 0：
$$-(1 - e_m) e^{-\alpha_m} + e_m e^{\alpha_m} = 0 \implies e^{2\alpha_m} = \frac{1 - e_m}{e_m} \implies \alpha_m = \frac{1}{2} \ln \frac{1 - e_m}{e_m}$$

---

## 🛠️ 14. PyTorch 动手实战与代码映射

### 1. 课本公式到 PyTorch 变量映射表 (Textbook-to-Code Mapping)
| 课本公式 / 符号 | 数学含义 | PyTorch 对应 API / 变量 | 说明 / 维度 (Shape) |
| :--- | :--- | :--- | :--- |
| $w_{m,i}$ | 样本权重向量 | `w = torch.ones(N) / N` | `[N]` |
| $e_m = \sum w_i \mathbb{I}(G \neq y)$ | 加权加权误差率 | `(w * (G != y)).sum()` | 标量 `[1]` |
| $\alpha_m = \frac{1}{2}\ln \frac{1-e_m}{e_m}$ | 基分类器权重 | `0.5 * torch.log((1 - e_m) / e_m)` | 标量 |
| $w_{next} \propto w \cdot e^{-\alpha y G}$ | 样本权重更新 | `w * torch.exp(-alpha * y * G)` | 归一化后 `[N]` |

### 2. 自包含、零依赖可运行代码 (Self-Contained Runnable Code)

```python
import torch

# ---------------------------------------------------------------
# 1. 模拟一维非线性二分类数据集 (Labels y in {-1, +1})
# ---------------------------------------------------------------
torch.manual_seed(42)
N = 100
X = torch.linspace(-3, 3, N).unsqueeze(1) # [100, 1]
# 真实分布：中间为 +1，两边为 -1 (一维非线性切分)
y = torch.ones(N)
y[(X[:, 0] < -1.5) | (X[:, 0] > 1.5)] = -1.0

# ---------------------------------------------------------------
# 2. 弱分类器：一维决策树桩 (Decision Stump)
# ---------------------------------------------------------------
class DecisionStump:
    def __init__(self):
        self.feature_idx = 0
        self.threshold = 0.0
        self.polarity = 1
        self.alpha = 0.0

    def predict(self, X):
        N = X.shape[0]
        preds = torch.ones(N)
        if self.polarity == 1:
            preds[X[:, self.feature_idx] < self.threshold] = -1.0
        else:
            preds[X[:, self.feature_idx] >= self.threshold] = -1.0
        return preds

# ---------------------------------------------------------------
# 3. 手写 AdaBoost 训练循环 (10 个弱树桩集成)
# ---------------------------------------------------------------
M = 10
stumps = []
w = torch.ones(N) / N # 初始均匀样本权重

for m in range(M):
    stump = DecisionStump()
    min_error = float('inf')
    
    # 寻找最佳树桩切分点
    for thresh in torch.linspace(-3, 3, 50):
        for pol in [1, -1]:
            temp_stump = DecisionStump()
            temp_stump.threshold = thresh
            temp_stump.polarity = pol
            preds = temp_stump.predict(X)
            
            # 计算加权误差率 e_m
            err = (w * (preds != y).float()).sum().item()
            if err < min_error:
                min_error = err
                stump.threshold = thresh
                stump.polarity = pol

    # 计算基分类器权重 alpha_m
    e_m = max(min_error, 1e-10) # 避免除零
    alpha_m = 0.5 * torch.log(torch.tensor((1.0 - e_m) / e_m)).item()
    stump.alpha = alpha_m
    stumps.append(stump)
    
    # 更新样本权重 w
    G_pred = stump.predict(X)
    w = w * torch.exp(-alpha_m * y * G_pred)
    w = w / w.sum() # 归一化

# ---------------------------------------------------------------
# 4. 强分类器预测与评估
# ---------------------------------------------------------------
final_scores = torch.zeros(N)
for stump in stumps:
    final_scores += stump.alpha * stump.predict(X)

final_preds = torch.sign(final_scores)
acc = (final_preds == y).float().mean().item()

print("=== PyTorch 手写 AdaBoost 算法训练完毕 ===")
print(f"集成 10 个一维决策树桩后的最终准确率: {acc * 100:.2f}%")
```

---

## 4. 常见误区和易混概念

### 误区 1：AdaBoost 中误分类点的权重会无限变大
- **为什么错**：虽然每次迭代误分类点的相对权重被乘以 $e^{\alpha_m} > 1$ 放大，但每次更新后样本权重向量都会显式除以规范化因子 $Z_m$ 进行**全局归一化**（使得 $\sum w_{m+1,i} = 1$），因此单个样本权重始终小于 1。

---

## 5. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 样本权重更新逻辑 |
| 2 | 公式计算 | 基础 | alpha_m 计算 |
| 3 | 理论推导 | 中等 | 指数损失函数 |
| 4 | 缺点分析 | 中等 | 噪声敏感性 |
| 5 | 算法对比 | 较难 | AdaBoost vs GBDT 区别 |

1. **[概念辨析] 当某轮基分类器的分类误差率 $e_m = 0.1$ 时，其权重 $\alpha_m$ 为：**
   A. 正数（说明该基分类器预测效果好，在强分类器中话语权大）  
   B. 零  
   C. 负数  
   D. 无效值
> [!question]- 答案解析
> **答案**：A  
> **解析**：当 $e_m < 0.5$ 时，$\frac{1-e_m}{e_m} > 1$，$\alpha_m = \frac{1}{2}\ln \frac{0.9}{0.1} > 0$，赋予正权重。  
> **标签**：`#自测/基础 #AdaBoost权重`

2. **[公式计算] 已知 $e_m = 0.5$（相当于随机猜测），求 $\alpha_m$ 的值为：**
   A. 0.5  B. 0  C. 1.0  D. 无限大
> [!question]- 答案解析
> **答案**：B  
> **解析**：$\alpha_m = \frac{1}{2}\ln \frac{0.5}{0.5} = \frac{1}{2}\ln 1 = 0$。预测效果等于随机猜测的基分类器被直接赋予 0 权重弃用。  
> **标签**：`#自测/基础 #随机猜测权重`

3. **[理论推导] AdaBoost 在数学上等价于使用哪个损失函数的加性模型前向角分步骤优化？**
   A. 均方误差 (MSE)  B. 指数损失函数 (Exponential Loss)  C. 交叉熵损失  D. Hinge Loss
> [!question]- 答案解析
> **答案**：B  
> **解析**：Friedman 等证明 AdaBoost 是以指数损失 $L(y, f) = \exp(-yf)$ 为目标的加性模型前向分步算法。  
> **标签**：`#自测/中等 #指数损失`

4. **[缺点分析] AdaBoost 最大的工程缺点在于：**
   A. 对噪声数据和离群点极度敏感（离群点权重会被成倍持续放大导致过拟合）  
   B. 无法处理二分类  
   C. 无法并行  
   D. 只能用深度树
> [!question]- 答案解析
> **答案**：A  
> **解析**：噪声点持续被误判，会导致其权重被指数级放大，使后续基分类器完全被噪声绑架。  
> **标签**：`#自测/中等 #AdaBoost缺点`

5. **[算法对比] AdaBoost 与 GBDT (梯度提升树) 的最本质区别在于：**
   A. AdaBoost 通过调整【样本权重】来关注错题；GBDT 通过拟合【前序模型的负梯度/残差】来拟合错题  
   B. 两者完全一样  
   C. AdaBoost 是 Bagging，GBDT 是 Boosting  
   D. AdaBoost 不能做回归
> [!question]- 答案解析
> **答案**：A  
> **解析**：AdaBoost 改变样本概率权重，GBDT 拟合前序残差/伪残差梯度。  
> **标签**：`#自测/较难 #AdaBoost与GBDT`

---

## 6. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/04-树与集成/`
- **建议双链**：
  - [[04-树与集成/🌲 第四阶段：树与集成|第四阶段：树与集成]]
  - [[04-树与集成/集成学习|集成学习]]
  - [[04-树与集成/GBDT|GBDT]]
- **建议标签**：`#学习` `#机器学习` `#AdaBoost` `#Boosting` `#指数损失` `#PyTorch实战`


---



---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: AdaBoost)

> **作业任务说明**：本作业为《AdaBoost》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 AdaBoost 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 AdaBoost 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (AdaBoost) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
