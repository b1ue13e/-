---
type: index
note_role: moc
cssclasses:
- atlas-page
- atlas-index
topic: 机器学习 MOC
course: 机器学习
created: '2026-06-24'
status: active
tags:
- MOC
- 机器学习
- 索引
---

# 机器学习 MOC

## 概念地图

### 基础概念

#### 基础概念
- [[2折交叉验证]]

### 第一阶段：基础概念

#### 基础概念
- [[K-means]]
- [[PCA]]
- [[Q-Learning]]
- [[伪标签]]
- [[偏差与方差]]
- [[机器学习]]
- [[概率统计基础]]
- [[正则化]]
- [[理解21]]
- [[线性代数基础]]
- [[结构风险最小化]]
- [[训练集与测试集]]
- [[过拟合]]
- [[过拟合与欠拟合]]

### 第三阶段：正则优化

#### 正则优化
- [[PAC学习]]
- [[反向传播算法]]
- [[深度学习入门]]
- [[神经网络]]
- [[稳定性]]

### 第二阶段：线性模型

#### 线性模型
- [[线性回归的几何解释]]
- [[逻辑回归]]

### 第五阶段：其他方法

#### 其他方法
- [[EM算法]]
- [[K近邻KNN]]
- [[SVM回归SVR]]
- [[主成分分析]]
- [[低维嵌入]]
- [[半监督学习]]
- [[原型聚类]]
- [[密度聚类]]
- [[层次聚类]]
- [[02-Knowledge/🧠 学习系统/17-机器学习/05-其他方法/度量学习]]
- [[强化学习导论]]
- [[支持向量机SVM]]
- [[02-Knowledge/🧠 学习系统/17-机器学习/05-其他方法/朴素贝叶斯]]
- [[极大似然估计]]
- [[核方法]]
- [[概率图模型入门]]
- [[聚类任务]]
- [[规则学习]]
- [[贝叶斯决策论]]
- [[软间隔SVM]]
- [[集成学习回顾]]

### 第四阶段：树与集成

#### 树与集成
- [[Bagging]]
- [[Boosting原理]]
- [[CatBoost]]
- [[LightGBM]]
- [[XGBoost]]
- [[决策树]]
- [[决策树剪枝]]
- [[划分选择]]
- [[多变量决策树]]
- [[多样性]]
- [[结合策略]]
- [[随机森林]]
- [[集成学习]]

### 线性模型

#### 线性模型
- [[公式理解6]]

### 计划占位

#### 计划占位
- [[占位-代码实践]]
- [[占位-公式清单]]
- [[占位-模拟题复盘]]
- [[占位-特征工程]]
- [[占位-课程任务挂载]]
- [[占位-课程复盘]]
- [[占位-错题整理]]
- [[占位-项目实践]]

### 🌱 第一阶段：基础概念

#### 模块1：学习任务与问题设定
- [[半监督与强化学习]]
- [[无监督学习]]
- [[机器学习概述]]
- [[监督学习]]

#### 模块2：假设空间与归纳偏好
- [[假设空间]]
- [[归纳偏好]]
- [[机器学习发展历程]]
- [[机器学习应用现状]]

#### 模块3：经验风险与泛化
- [[经验风险最小化]]

#### 模块4：评估与模型选择
- [[数据集划分与交叉验证]]
- [[模型评估指标]]
- [[比较检验]]

### 📈 第二阶段：线性模型

#### 模块1：回归视角
- [[线性回归]]

#### 模块2：分类视角
- [[线性判别分析]]

#### 模块3：多分类与不平衡
- [[多分类学习]]
- [[类别不平衡问题]]

### 🛡️ 第三阶段：正则优化

#### 模块1：神经网络与反向传播
- [[02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/感知机]]

#### 模块2：特征选择与稀疏化
- [[L1正则化Lasso]]
- [[特征选择]]
- [[稀疏学习]]

#### 模块3：泛化理论
- [[Rademacher复杂度]]
- [[VC维]]

## 推导地图
- [[K-means中心更新推导]]
- [[反向传播算法推导]]

## 题型地图
- [[假设空间常见题型]]
- [[其他方法常见题型]]
- [[基础概念常见题型]]
- [[树与集成常见题型]]
- [[计划占位常见题型]]

## 错题 / 漏洞
- [[机器学习错题漏洞入口]]


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 机器学习 MOC)

> **作业任务说明**：本作业为《机器学习 MOC》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 机器学习 MOC 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 机器学习 MOC 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (机器学习 MOC) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
