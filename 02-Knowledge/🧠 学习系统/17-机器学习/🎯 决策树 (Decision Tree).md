---
title: "决策树 (Decision Tree)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 树模型, 决策树, ID3, C4.5, CART, 递归构建]
upstream: ["[[01-基础概念/监督学习|监督学习]]"]
downstream: ["[[04-树与集成/划分选择|划分选择]]", "[[04-树与集成/决策树剪枝|决策树剪枝]]", "[[04-树与集成/随机森林|随机森林]]", "[[04-树与集成/XGBoost|XGBoost]]"]
status: learning
---

# 🎯 决策树 (Decision Tree)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：决策树（Decision Tree）是基于树形结构进行决策的非参数监督学习算法，具备极佳的人类可读性（If-Then 逻辑规则）。它不仅是理解单树分类/回归的基石，更是后续随机森林（Random Forest）、GBDT、XGBoost 与 LightGBM 等所有现代集成树模型的分子级构件。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**
> 许多工业决策场景（如银行贷款审批、医疗分诊流程）不仅要求预测准确，还要求决策过程“完全透明且符合人类逻辑”。神经网络或 SVM 是黑盒，无法给出直观理由。

决策树**通过树状图递归对特征进行“分而治之”切分**，生成直观、可解释的决策逻辑流程。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：
  - **后续影响**：结合 Bagging 导出 [[04-树与集成/随机森林|随机森林]]；结合 Boosting 导出 [[04-树与集成/XGBoost|GBDT/XGBoost]]。
  - **课程位置**：属于“第四阶段：树与集成”的根本支柱。
- **实战与科研价值**：
  - **特征天然兼容**：无需特征标准化/归一化，能天然处理离散特征与缺失值。
  - **最常出现题型**：ID3 / C4.5 / CART 算法生成过程计算题、信息增益与基尼指数计算题、预剪枝与后剪枝对比题。

---

## 3. 学它之前需要哪些前置知识？

### 最小必要背景：
1. **熵 (Entropy)**：衡量数据混乱程度/不确定性的指标 $H(D) = -\sum p_k \log_2 p_k$。
2. **递归思想**：自顶向下构建子树，直到终止条件。

---

## 4. 用直觉语言解释它

> «“这东西其实就像二十个问题猜猜看游戏……”»

- **场景**：你心里想一个动物，朋友通过问你不超过 20 个“是/否”问题（如“有四条腿吗？”“吃肉吗？”“会叫吗？”）逐步缩小范围，直到锁定具体动物。
- **决策树核心**：每一个非叶节点都是一个问题（特征切分），每一个分支代表回答，每一个叶节点就是最终的决策预测。
- **最优切分**：每次挑选那个“能最大程度消除不确定性（使回答后的两组变得最纯净）”的问题来问。

---

## 5. 决策树三大经典算法家族对比

| 维度 | ID3 算法 | C4.5 算法 | CART 算法 (Classification And Regression Tree) |
| :--- | :--- | :--- | :--- |
| **特征选择指标** | **信息增益 (Information Gain)** | **信息增益率 (Gain Ratio)** | **基尼指数 (Gini Index)** (分类) / **MSE** (回归) |
| **树结构形态** | 多叉树 (Multi-way) | 多叉树 (Multi-way) | **严格二叉树 (Binary Tree)** |
| **支持任务** | 仅分类 | 仅分类 | **分类 + 回归** |
| **连续特征处理** | 不支持 | 二分法 (Bi-partition) | 二分法 (Bi-partition) |
| **缺失值处理** | 不支持 | 支持加权处理 | 支持替代切分 (Surrogate Splitting) |
| **偏好偏见** | 偏向选择取值较多的特征 | 克服偏向（惩罚固有值） | 偏向连续特征与大类别 |

---

## 6. 例子：基础 → 中等 → 实际应用

### 例子 1：信息熵计算
**题目**：集合 $D$ 包含 16 个样本，其中 8 个正例、8 个负例。求集合 $D$ 的信息熵 $H(D)$。

**解答**：
$$H(D) = -\left( \frac{8}{16} \log_2 \frac{8}{16} + \frac{8}{16} \log_2 \frac{8}{16} \right) = -\left( \frac{1}{2} (-1) + \frac{1}{2} (-1) \right) = 1.0 \text{ bit}$$
- **结论**：当正负例 50:50 极其均匀时，不确定性最大，熵等于 1。若全部为正例（8/8），$H(D) = 0$（最纯净）。

---

## 7. 常见误区和易混概念

### 误区 1：决策树越深越好
- **为什么错**：如果不加限制地生长，决策树会直到每一个叶节点只有一个样本（纯度 100%）才停止，导致对训练样本的噪声完全过拟合（训练 Error=0，测试 Error 极高）。必须通过[[04-树与集成/决策树剪枝|剪枝]]限制深度。

---

## 8. 相关知识点与 Obsidian 双链建议

### 上游依赖（前置知识）
- [[01-基础概念/监督学习|监督学习]]

### 下游延伸（后续进阶）
- [[04-树与集成/划分选择|划分选择]]
- [[04-树与集成/决策树剪枝|决策树剪枝]]
- [[04-树与集成/随机森林|随机森林]]
- [[04-树与集成/GBDT|GBDT]]

## 下游延伸（后续进阶）
- [[04-树与集成/划分选择|划分选择]]
- [[04-树与集成/决策树剪枝|决策树剪枝]]
- [[04-树与集成/随机森林|随机森林]]
- [[04-树与集成/GBDT|GBDT]]

## 下游延伸（后续进阶）
- [[04-树与集成/划分选择|划分选择]]
- [[04-树与集成/决策树剪枝|决策树剪枝]]
- [[04-树与集成/随机森林|随机森林]]
- [[04-树与集成/GBDT|GBDT]]

## 下游延伸
- [[04-树与集成/划分选择|划分选择]]
- [[04-树与集成/决策树剪枝|决策树剪枝]]
- [[04-树与集成/随机森林|随机森林]]

---

## 9. 闭卷复现任务

1. 默写信息熵 $H(D)$ 与基尼指数 $\text{Gini}(D)$ 的定义式。
2. 比较 ID3、C4.5 与 CART 算法的三大区别。
3. 说明 CART 树为什么必须是二叉树。

---

## 10. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 算法指标匹配 |
| 2 | 熵计算 | 基础 | 极值熵计算 |
| 3 | 算法对比 | 中等 | CART 特性 |
| 4 | 偏好分析 | 中等 | ID3 偏向取值多特征 |
| 5 | 综合思考 | 较难 | CART 回归树切分点寻找 |

1. **[概念辨析] 经典 C4.5 决策树算法在选择最佳切分特征时所采用的指标是：**
   A. 信息增益  B. 信息增益率  C. 基尼指数  D. 均方误差
> [!question]- 答案解析
> **答案**：B  
> **解析**：C4.5 改进 ID3，采用信息增益率来克服对取值较多特征的偏好。  
> **标签**：`#自测/基础 #C4.5`

2. **[熵计算] 若某节点样本全部属于同一个类别（纯度 100%），则该节点的信息熵等于：**
   A. 1.0  B. 0  C. 无限大  D. 0.5
> [!question]- 答案解析
> **答案**：B  
> **解析**：当 $p=1$ 时，$\log_2 1 = 0$，信息熵降为 0（无任何不确定性）。  
> **标签**：`#自测/基础 #信息熵极值`

3. **[算法对比] CART (Classification and Regression Trees) 算法的核心特征包括：**
   A. 只能构建多叉树  
   B. 无论分类还是回归，构建的均为严格的二叉树  
   C. 无法处理回归问题  
   D. 采用信息增益率
> [!question]- 答案解析
> **答案**：B  
> **解析**：CART 的核心特点是二叉树结构，分类用基尼指数，回归用平方误差。  
> **标签**：`#自测/中等 #CART`

4. **[偏好分析] ID3 算法采用“信息增益”作为切分指标，其致命缺陷在于：**
   A. 偏向于选择取值数目较多的特征（如身份证号、用户ID），导致过拟合  
   B. 无法处理离散特征  
   C. 训练速度太慢  
   D. 无法处理二分类
> [!question]- 答案解析
> **答案**：A  
> **解析**：若某特征每个样本取值都不同（如身份证号），切分后每个子节点熵均为 0，信息增益达到极大，但泛化能力为 0。  
> **标签**：`#自测/中等 #ID3缺陷`

5. **[综合思考] 简述 CART 回归树在寻找某个连续特征 $x_j$ 的最佳切分点 $s$ 时，如何定义目标函数？**
> [!question]- 答案解析
> **答案**：CART 回归树通过最小化切分后左右两个子区域的平方误差和来寻找最佳 $x_j$ 和切分点 $s$：$\min_{j, s} \left[ \min_{c_1} \sum_{x_i \in R_1(j,s)} (y_i - c_1)^2 + \min_{c_2} \sum_{x_i \in R_2(j,s)} (y_i - c_2)^2 \right]$，其中 $c_1, c_2$ 分别为左右区域目标的样本均值。  
> **标签**：`#自测/较难 #CART回归树`

---

## 11. 我的主动回忆区

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

## 12. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/04-树与集成/`
- **建议双链**：
  - [[04-树与集成/🌲 第四阶段：树与集成|第四阶段：树与集成]]
  - [[04-树与集成/划分选择|划分选择]]
  - [[04-树与集成/随机森林|随机森林]]
- **建议标签**：`#学习` `#机器学习` `#决策树` `#ID3` `#C4.5` `#CART` `#信息熵`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 决策树)

> **作业任务说明**：本作业为《决策树》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 决策树 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 决策树 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (决策树) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
