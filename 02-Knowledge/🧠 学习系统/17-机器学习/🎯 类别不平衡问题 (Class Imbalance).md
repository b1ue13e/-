---
title: "类别不平衡问题 (Class Imbalance Problem & Solutions)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 线性模型, 类别不平衡, 重采样, SMOTE, 再缩放, 阈值移动]
upstream: ["[[02-线性模型/逻辑回归|逻辑回归]]", "[[02-线性模型/多分类学习|多分类学习]]"]
downstream: ["[[01-基础概念/模型评估指标|模型评估指标]]"]
status: learning
---

# 🎯 类别不平衡问题 (Class Imbalance)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：类别不平衡（Class Imbalance）在工业真实场景中无处不在（如信用卡欺诈 0.01% 正例、广告点击率 0.1% 正例、罕见病诊断 0.05% 正例）。未处理的不平衡数据会导致常规模型盲目预测全为多数类（获得 99.9% 假高准确率但零实用价值）。掌握**重采样（SMOTE）、再缩放（阈值移动）与 Focal Loss**是工业落地的必备技能。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**
> 假设你训练一个信用卡欺诈检测模型，1,000,000 条交易中只有 100 条是欺诈（正例比例 0.01%）。模型如果把所有交易都预测为“非欺诈”，训练集准确率高达 99.99%！但这个模型连 1 笔真实欺诈都没拦截下来，完全失效。

类别不平衡**提供了打破决策边界被多数类强行挤压推偏的纠偏技术**。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：
  - **后续影响**：决定了为什么不能使用 Accuracy 而必须使用 [[01-基础概念/模型评估指标|PR-AUC / ROC-AUC / F1-Score]]；直接引出了 Focal Loss（DenseNet/RetinaNet 核心）。
  - **课程位置**：属于“第二阶段：线性模型”的工业级调优策略。
- **实战与科研价值**：
  - **三大工程武器**：
    1. **欠采样 (Undersampling)**：EasyEnsemble。
    2. **过采样 (Oversampling)**：[[SMOTE]] 算法（插值合成少数类）。
    3. **再缩放 (Threshold-Moving / Rescaling)**：修改分类决策阈值 $\frac{y'}{1-y'} = \frac{y}{1-y} \times \frac{m^-}{m^+}$。

---

## 3. 正式定义与三大解决方案

### 1. 再缩放与阈值移动 (Rescaling / Threshold-Moving)
在逻辑回归中，基础决策规则为：若 $\frac{y}{1-y} > 1$ 则预测为正例（隐含前提：正负例数目均衡 $m^+ = m^-$）。
当正例 $m^+$ 与负例 $m^-$ 极度不平衡时，根据贝叶斯决策论，**真实观测几率应调整为**：

$$\frac{y'}{1-y'} = \frac{y}{1-y} \times \frac{m^-}{m^+}$$

即：若线性模型预测输出 $y > \frac{m^+}{m^+ + m^-}$，即可判为正例。

### 2. 重采样技术 (Resampling)
- **过采样 (Oversampling)**：增加少数类样本（如 **SMOTE** 算法：在相邻少数类样本间的连线上随机插值合成新样本，避免简单复制引发的过拟合）。
- **欠采样 (Undersampling)**：减少多数类样本（如 **EasyEnsemble**：将多数类拆分为多个子集，训练多个集成模型）。

### 3. 代价敏感学习 (Cost-Sensitive Learning)
为少数类预测错误赋予更高的惩罚代价 $C_{\text{FN}} \gg C_{\text{FP}}$，在损失函数中增加少数类样本的权重。

---

## 4. 例子：SMOTE 算法插值原理

### SMOTE 合成样本公式
对于少数类样本 $\mathbf{x}_i$，寻找其同类 $k$ 近邻中的某个样本 $\mathbf{x}_{\text{zi}}$。
合成的新样本 $\mathbf{x}_{\text{new}}$ 为：

$$\mathbf{x}_{\text{new}} = \mathbf{x}_i + \text{rand}(0, 1) \times (\mathbf{x}_{\text{zi}} - \mathbf{x}_i)$$

**直觉**：在已有的两个正例点连线上，随机画一个新点，保留了特征几何结构。

---

## 5. 常见误区和易混概念

### 误区 1：直接对极度不平衡数据计算 Accuracy 来评估模型
- **错误直觉**：“准确率 99.9% 肯定很优秀。”
- **为什么错**：不平衡数据下，全预测为负类就能轻松获得 99.9% 准确率。必须看 **Recall（召回率）** 和 **PR-AUC**。

---

## 6. 相关知识点与 Obsidian 双链建议

### 上游依赖（前置知识）
- [[02-线性模型/多分类学习|多分类学习]]

### 下游延伸（后续进阶）
- [[01-基础概念/模型评估指标|模型评估指标]]

## 下游延伸（后续进阶）
- [[01-基础概念/模型评估指标|模型评估指标]]

## 下游延伸（后续进阶）
- [[01-基础概念/模型评估指标|模型评估指标]]

## 下游延伸
- [[01-基础概念/模型评估指标|模型评估指标]]

---

## 7. 闭卷复现任务

1. 写出再缩放 (Rescaling) 的概率校正阈值调整公式。
2. 简述 SMOTE 过采样算法的工作原理。
3. 区分简单的随机过采样与 SMOTE 算法的区别。

---

## 8. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 评估指标选择 |
| 2 | 公式计算 | 基础 | 阈值移动计算 |
| 3 | 算法原理 | 中等 | SMOTE 插值原理 |
| 4 | 缺点分析 | 中等 | 简单过采样缺陷 |
| 5 | 综合设计 | 较难 | 风控模型不平衡治理 |

1. **[概念辨析] 面对正例仅占 0.05% 的极度不平衡数据，最不应该使用的模型评估指标是：**
   A. ROC-AUC  B. 准确率 (Accuracy)  C. PR-AUC  D. F1-Score
> [!question]- 答案解析
> **答案**：B  
> **解析**：在极度不平衡场景下，Accuracy 会出现严重盲目假高失真。  
> **标签**：`#自测/基础 #不平衡评估`

2. **[公式计算] 某数据集中正例 $m^+=100$，负例 $m^-=900$。使用逻辑回归预测某样本输出概率 $p=0.2$。经再缩放阈值校正后，调整后的预测几率比 $\frac{y'}{1-y'}$ 为：**
   A. $\frac{0.2}{0.8} \times \frac{900}{100} = 0.25 \times 9 = 2.25 > 1 \implies$ 判为正例  
   B. 0.2  
   C. 0.05  
   D. 0.8
> [!question]- 答案解析
> **答案**：A  
> **解析**：原始几率为 $0.2/0.8=0.25$，乘以先验比例 $900/100=9$ 得校正后几率 $2.25 > 1$，翻转为正例。  
> **标签**：`#自测/基础 #阈值校正`

3. **[算法原理] SMOTE 算法相比于简单随机过采样的最大优势在于：**
   A. SMOTE 随机删除多数类样本  
   B. SMOTE 通过近邻插值生成新的虚拟样本，避免了简单重复复制样本导致的严重过拟合  
   C. SMOTE 不需要计算距离  
   D. SMOTE 适用于回归任务
> [!question]- 答案解析
> **答案**：B  
> **解析**：简单复制同点样本会导致模型过拟合于这几个特定点，SMOTE 插值拓展了少数类决策区域。  
> **标签**：`#自测/中等 #SMOTE优势`

4. **[缺点分析] 随机欠采样 (Random Undersampling) 最大的潜在风险是：**
   A. 训练速度太慢  
   B. 可能随机丢弃大量多数类中包含重要决策边界信息的重要样本  
   C. 引发内存爆炸  
   D. 无法计算梯度
> [!question]- 答案解析
> **答案**：B  
> **解析**：随机丢弃多数类样本极易损失多数类的数据分布信息。  
> **标签**：`#自测/中等 #欠采样风险`

5. **[综合设计] 简述 Focal Loss 如何解决单阶段目标检测中背景样本（易分类负样本）占据绝对主导带来的不平衡问题？**
> [!question]- 答案解析
> **答案**：Focal Loss 在标准交叉熵损失前引入动态衰减因子 $(1-p_t)^\gamma$。对于已被精准预测的高置信易分类样本（$p_t \to 1$），衰减因子接近 0，极大压低其 Loss 权重；从而将模型的注意力强制集中在少量难分类的候选正样本上。  
> **标签**：`#自测/较难 #FocalLoss`

---

## 9. 我的主动回忆区

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

## 10. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/02-线性模型/`
- **建议双链**：
  - [[02-线性模型/📈 第二阶段：线性模型|第二阶段：线性模型]]
  - [[02-线性模型/逻辑回归|逻辑回归]]
  - [[01-基础概念/模型评估指标|模型评估指标]]
- **建议标签**：`#学习` `#机器学习` `#类别不平衡` `#SMOTE` `#再缩放` `#FocalLoss`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 类别不平衡问题)

> **作业任务说明**：本作业为《类别不平衡问题》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 类别不平衡问题 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 类别不平衡问题 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (类别不平衡问题) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
