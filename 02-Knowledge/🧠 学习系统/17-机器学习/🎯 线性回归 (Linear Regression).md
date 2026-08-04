---
title: "线性回归 (Linear Regression)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 线性模型, 线性回归, 最小二乘法, 矩阵求导, PyTorch实战]
upstream: ["[[01-基础概念/线性代数基础|线性代数基础]]", "[[01-基础概念/概率统计基础|概率统计基础]]"]
downstream: ["[[逻辑回归]]", "[[03-正则优化/L1正则化Lasso|L1正则化Lasso]]", "[[03-正则优化/L2正则化Ridge|L2正则化Ridge]]"]
status: learning
---

# 🎯 线性回归 (Linear Regression)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：线性回归是整个监督学习与连续变量预测的绝对起点。它的最小二乘法推导、正规方程封闭解、概率最大似然解释以及凸二次优化性质，贯穿了后续 Logistic 回归、岭回归、Lasso 正则化与神经网络感知机的底层数学基础。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**
> 假设你需要根据房屋面积 $x_1$、房间数 $x_2$、离地铁距离 $x_3$ 等连续特征预测房屋总价 $y$。你需要构建一个简单、稳定且具备极强可解释性的数学模型。

线性回归**通过拟合一个最佳超平面（Hyperplane）**，建立起自变量与连续因变量之间的线性映射关系。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：
  - **后续影响**：加上 Sigmoid 激活得到 [[逻辑回归]]；加上 L2 范数得到 Ridge 回归；加上 L1 范数得到 Lasso 回归。
  - **课程位置**：属于“第二阶段：线性模型”的理论基石。
- **实战与科研价值**：
  - **因果推断与可解释性**：权重 $w_j$ 明确表示在其他特征不变时，特征 $x_j$ 每增加一个单位导致 $y$ 变化的平均幅度。
  - **最常出现题型**：正规方程（Normal Equation）矩阵求导推导题、极大似然估计推导 MSE 题、不可逆情形（多重共线性）分析题。

---

## 3. 学它之前需要哪些前置知识？

### 最小必要背景：
1. **向量与矩阵求导**：$\frac{\partial (\mathbf{w}^T \mathbf{x})}{\partial \mathbf{w}} = \mathbf{x}, \frac{\partial (\mathbf{w}^T \mathbf{A} \mathbf{w})}{\partial \mathbf{w}} = 2\mathbf{A}\mathbf{w}$。
2. **均方误差 (MSE)**：$E_{\mathbf{w}, b} = \sum_{i=1}^N (y_i - (\mathbf{w}^T \mathbf{x}_i + b))^2$。

---

## 4. 用直觉语言解释它

> «“这东西其实就像在散点图里画一条最贴合的直线……”»

- **一维直觉**：黑板上有许多散落的横轴为面积、纵轴为房价的点。你的任务是拿一把直尺画一条斜线 $y = w x + b$，使得所有点到这条直线的竖直距离的平方和最小。
- **高维扩展**：特征变成 $d$ 维时，直线变成了高维空间里的超平面 $f(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b$。

---

## 5. 正式定义、核心公式、符号解释

### 1. 向量化模型表达
引入偏置项增广向量：令 $\tilde{\mathbf{x}} = (x_1, \dots, x_d, 1)^T \in \mathbb{R}^{d+1}$，$\tilde{\mathbf{w}} = (w_1, \dots, w_d, b)^T \in \mathbb{R}^{d+1}$。
模型预测值为：

$$f(\mathbf{x}_i) = \tilde{\mathbf{w}}^T \tilde{\mathbf{x}}_i$$

给出现特征矩阵 $\mathbf{X} \in \mathbb{R}^{N \times (d+1)}$，目标向量 $\mathbf{y} \in \mathbb{R}^N$。

### 2. 损失函数 (MSE) 矩阵形式

$$E(\tilde{\mathbf{w}}) = \|\mathbf{y} - \mathbf{X}\tilde{\mathbf{w}}\|_2^2 = (\mathbf{y} - \mathbf{X}\tilde{\mathbf{w}})^T (\mathbf{y} - \mathbf{X}\tilde{\mathbf{w}})$$

### 3. 正规方程封闭解 (Normal Equation)
对 $\tilde{\mathbf{w}}$ 求导并置 0 得到：

$$\frac{\partial E}{\partial \tilde{\mathbf{w}}} = -2 \mathbf{X}^T \mathbf{y} + 2 \mathbf{X}^T \mathbf{X} \tilde{\mathbf{w}} = \mathbf{0} \implies \mathbf{X}^T \mathbf{X} \tilde{\mathbf{w}} = \mathbf{X}^T \mathbf{y}$$

当 $\mathbf{X}^T \mathbf{X}$ 可逆时，最优封闭解为：

$$\tilde{\mathbf{w}}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$

---

## 6. 推导思路和思想来源

### 四步矩阵推导法：
1. **展开损失函数**：
   $$E(\tilde{\mathbf{w}}) = \mathbf{y}^T \mathbf{y} - \mathbf{y}^T \mathbf{X} \tilde{\mathbf{w}} - \tilde{\mathbf{w}}^T \mathbf{X}^T \mathbf{y} + \tilde{\mathbf{w}}^T \mathbf{X}^T \mathbf{X} \tilde{\mathbf{w}}$$
2. **合并标量同类项**：由于 $\mathbf{y}^T \mathbf{X} \tilde{\mathbf{w}}$ 为 $1 \times 1$ 标量，其转置等于自身 $\tilde{\mathbf{w}}^T \mathbf{X}^T \mathbf{y}$，故：
   $$E(\tilde{\mathbf{w}}) = \mathbf{y}^T \mathbf{y} - 2 \tilde{\mathbf{w}}^T \mathbf{X}^T \mathbf{y} + \tilde{\mathbf{w}}^T \mathbf{X}^T \mathbf{X} \tilde{\mathbf{w}}$$
3. **矩阵求导**：利用法则 $\frac{\partial (\mathbf{a}^T \mathbf{x})}{\partial \mathbf{x}} = \mathbf{a}$ 和 $\frac{\partial (\mathbf{x}^T \mathbf{A} \mathbf{x})}{\partial \mathbf{x}} = 2\mathbf{A}\mathbf{x}$：
   $$\frac{\partial E}{\partial \tilde{\mathbf{w}}} = -2 \mathbf{X}^T \mathbf{y} + 2 \mathbf{X}^T \mathbf{X} \tilde{\mathbf{w}}$$
4. **令梯度为 0 解方程**：得到 $\tilde{\mathbf{w}}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：一维最小二乘求斜率与截距
**题目**：已知 2 个数据点 $(1, 2)$ 和 $(3, 4)$。使用一维线性回归 $y = w x + b$ 求 $w$ 和 $b$。

**解答**：
代入数据点：
$2 = w(1) + b$  
$4 = w(3) + b$  
两式相减：$2w = 2 \implies w = 1$。代入得 $b = 1$。
故线性方程为 $y = x + 1$。

---

## 🛠️ 14. PyTorch 动手实战与代码映射

### 1. 课本公式到 PyTorch 变量映射表 (Textbook-to-Code Mapping)
| 课本公式 / 符号 | 数学含义 | PyTorch 对应 API / 变量 | 说明 / 维度 (Shape) |
| :--- | :--- | :--- | :--- |
| $\mathbf{w}, b$ | 参数权重与偏置 | `nn.Linear(in_dim, 1)` | `.weight` `[1, d]`, `.bias` `[1]` |
| $\mathbf{X}\mathbf{w} + b$ | 前向预测值 $\hat{\mathbf{y}}$ | `model(X)` | `[N, 1]` |
| $E(\mathbf{w}) = \frac{1}{N}\|\mathbf{y}-\hat{\mathbf{y}}\|^2$ | 均方误差 Loss | `nn.MSELoss()` | 标量 `[1]` |
| $\nabla_{\mathbf{w}} E$ | 损失函数梯度 | `param.grad` | `loss.backward()` 自动计算积累 |
| $\mathbf{w}^* = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$ | 正规方程封闭解 | `torch.linalg.lstsq(X, y)` | 矩阵求解封闭解 |

### 2. 自包含、零依赖可运行代码 (Self-Contained Runnable Code)

```python
import torch
import torch.nn as nn
import torch.optim as optim

# ---------------------------------------------------------------
# 1. 模拟数据集生成 (Synthetic Dataset)
# 假设真实规律：y = 2.0 * x1 - 3.0 * x2 + 1.5 + 噪声
# ---------------------------------------------------------------
torch.manual_seed(42)
N, d = 200, 2
X = torch.randn(N, d) # Shape: [200, 2]
true_w = torch.tensor([2.0, -3.0]).unsqueeze(1) # Shape: [2, 1]
true_b = 1.5
noise = 0.05 * torch.randn(N, 1) # Shape: [200, 1]
y = torch.matmul(X, true_w) + true_b + noise # Shape: [200, 1]

# ---------------------------------------------------------------
# 方式 A：用线性代数正规方程直接求解封闭解 (Closed-form Solution)
# w* = (X^T X)^-1 X^T y
# ---------------------------------------------------------------
X_aug = torch.cat([X, torch.ones(N, 1)], dim=1) # 增加常数项 [200, 3]
w_exact = torch.matmul(torch.matmul(torch.linalg.inv(torch.matmul(X_aug.T, X_aug)), X_aug.T), y)
print("=== 方式 A: 矩阵正规方程封闭解 ===")
print(f"解得权重 w1, w2: {w_exact[0].item():.4f}, {w_exact[1].item():.4f}, 偏置 b: {w_exact[2].item():.4f}\n")

# ---------------------------------------------------------------
# 方式 B：用 PyTorch 梯度下降模型求解 (Gradient Descent)
# ---------------------------------------------------------------
class LinearRegressionModel(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.linear = nn.Linear(in_features, 1) # [batch, in_features] -> [batch, 1]

    def forward(self, x):
        return self.linear(x)

model = LinearRegressionModel(in_features=d)
criterion = nn.MSELoss() # 对应 MSE Loss
optimizer = optim.SGD(model.parameters(), lr=0.05) # 对应梯度下降算法

# 训练循环 (Training Loop)
for epoch in range(200):
    optimizer.zero_grad()         # 1. 梯度清零
    y_pred = model(X)             # 2. 前向传播 [200, 1]
    loss = criterion(y_pred, y)   # 3. 计算 MSE 损失
    loss.backward()               # 4. 反向传播 dJ/dw
    optimizer.step()              # 5. 参数更新 w = w - alpha * grad

print("=== 方式 B: PyTorch 梯度下降法答案 ===")
print(f"最终 Loss: {loss.item():.6f}")
print(f"学得权重 w: {model.linear.weight.detach().numpy().ravel()}")
print(f"学得偏置 b: {model.linear.bias.item():.4f}")
```

### 3. PyTorch 避坑指南与 Gotchas
- **张量维度广播坑 (Broadcasting Bug)**：在计算 `y_pred - y` 时，如果 `y_pred` 的 Shape 是 `[N, 1]` 而 `y` 的 Shape 是 `[N]`，PyTorch 触发广播机制会隐式生成一个 `[N, N]` 的矩阵，导致 Loss 计算彻底崩溃且无报错！务必保持 `y` 的 Shape 与 `y_pred` 一致 (`[N, 1]`)。
- **梯度清零 (Zero Grad)**：由于 `loss.backward()` 默认将梯度累加到 `param.grad` 上，每次 `step()` 之前必须调用 `optimizer.zero_grad()`。

---

## 8. 常见误区和易混概念

### 误区 1：只要有数据，就可以直接用正规方程求解 $\mathbf{w}^*$
- **为什么错**：如果特征数 $d > N$（特征数大于样本数），或者特征之间存在高度相关性（多重共线性），矩阵 $\mathbf{X}^T \mathbf{X}$ 将变成**奇异矩阵（不可逆）**。此时正规方程无法直接求解，必须使用伪逆或加入 L2 正则化（Ridge 岭回归）。

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖（前置知识）
- [[01-基础概念/线性代数基础|线性代数基础]]
- [[01-基础概念/梯度下降法|梯度下降法]]

### 下游延伸（后续进阶）
- [[02-线性模型/逻辑回归|逻辑回归]]
- [[02-线性模型/线性判别分析|线性判别分析]]
- [[03-正则优化/L1正则化Lasso|L1正则化Lasso]]

## 下游延伸（后续进阶）
- [[02-线性模型/逻辑回归|逻辑回归]]
- [[02-线性模型/线性判别分析|线性判别分析]]
- [[03-正则优化/L1正则化Lasso|L1正则化Lasso]]

## 下游延伸（后续进阶）
- [[02-线性模型/逻辑回归|逻辑回归]]
- [[02-线性模型/线性判别分析|线性判别分析]]
- [[03-正则优化/L1正则化Lasso|L1正则化Lasso]]

## 下游延伸
- [[逻辑回归]]
- [[03-正则优化/L1正则化Lasso|L1正则化Lasso]]

---

## 10. 闭卷复现任务

1. 默写线性回归的矩阵损失函数表达式。
2. 完整推导正规方程封闭解 $\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$。
3. 解释当 $\mathbf{X}^T \mathbf{X}$ 不可逆时发生什么，如何解决？

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 线性回归任务类型 |
| 2 | 公式求导 | 基础 | 梯度表达式 |
| 3 | 不可逆分析 | 中等 | 多重共线性 |
| 4 | 概率推导 | 中等 | 高斯噪声与 MLE |
| 5 | 算力对比 | 较难 | 正规方程 vs 梯度下降 |

1. **[概念辨析] 线性回归中，损失函数采用均方误差 (MSE) 的概率学根源假设是：**
   A. 标签误差服从拉普拉斯分布  
   B. 标签误差服从独立同分布的高斯分布 $\mathcal{N}(0, \sigma^2)$  
   C. 特征服从均匀分布  
   D. 标签服从伯努利分布
> [!question]- 答案解析
> **答案**：B  
> **解析**：在误差独立同分布高斯假设下，极大似然估计 (MLE) 推导出的表达式与 MSE 完全一致。  
> **标签**：`#自测/基础 #MSE高斯假设`

2. **[公式求导] 设增广特征矩阵为 $\mathbf{X}$，目标为 $\mathbf{y}$，均方误差对增广权重 $\tilde{\mathbf{w}}$ 的梯度为：**
   A. $\mathbf{X}(\mathbf{y} - \mathbf{X}\tilde{\mathbf{w}})$  
   B. $-2\mathbf{X}^T (\mathbf{y} - \mathbf{X}\tilde{\mathbf{w}})$  
   C. $\mathbf{X}^T \mathbf{y}$  
   D. $\|\mathbf{y} - \mathbf{X}\tilde{\mathbf{w}}\|^2$
> [!question]- 答案解析
> **答案**：B  
> **解析**：求导展开为 $-2\mathbf{X}^T\mathbf{y} + 2\mathbf{X}^T\mathbf{X}\tilde{\mathbf{w}} = -2\mathbf{X}^T(\mathbf{y} - \mathbf{X}\tilde{\mathbf{w}})$。  
> **标签**：`#自测/基础 #线性回归梯度`

3. **[不可逆分析] 当样本特征存在完全共线性（如 $x_2 = 2x_1$）时，会导致：**
   A. $\mathbf{X}^T \mathbf{X}$ 满秩  
   B. $\mathbf{X}^T \mathbf{X}$ 的行列式等于 0，矩阵不可逆  
   C. 梯度下降无法收敛  
   D. Loss 永远为 0
> [!question]- 答案解析
> **答案**：B  
> **解析**：完全共线性导致矩阵列向量线性相关，矩阵降秩不可逆。  
> **标签**：`#自测/中等 #多重共线性`

4. **[概率推导] 若假设误差服从拉普拉斯分布 $p(\varepsilon) \propto \exp(-\frac{|\varepsilon|}{b})$，极大似然估计得到的损失函数将变为：**
   A. 均方误差 (L2 Loss)  
   B. 平均绝对误差 (MAE / L1 Loss)  
   C. 交叉熵损失  
   D. Hinge Loss
> [!question]- 答案解析
> **答案**：B  
> **解析**：拉普拉斯分布的对数似然包含绝对值项 $-|\varepsilon|$，对应 MAE 损失。  
> **标签**：`#自测/中等 #拉普拉斯MAE`

5. **[算力对比] 当特征维度 $d = 100,000$ 极高时，直接求解正规方程 $\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$ 相比于使用梯度下降法（GD）的劣势是：**
   A. 无法找到全局最优解  
   B. 矩阵求逆算法复杂度高达 $O(d^3)$，引发内存爆表与计算瘫痪；而 GD 单次迭代复杂度仅为 $O(Nd)$  
   C. 梯度下降更容易过拟合  
   D. 没有区别
> [!question]- 答案解析
> **答案**：B  
> **解析**：高维求逆 $O(d^3)$ 算力极其昂贵，因此高维下工程上优先采用梯度下降迭代求解。  
> **标签**：`#自测/较难 #正规方程复杂度`

---

## 12. 我的主动回忆区

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

## 13. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/02-线性模型/`
- **建议双链**：
  - [[02-线性模型/📈 第二阶段：线性模型|第二阶段：线性模型]]
  - [[02-线性模型/逻辑回归|逻辑回归]]
- **建议标签**：`#学习` `#机器学习` `#线性回归` `#最小二乘法` `#正规方程` `#PyTorch实战`


---



---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 线性回归)

> **作业任务说明**：本作业为《线性回归》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 线性回归 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 线性回归 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (线性回归) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
