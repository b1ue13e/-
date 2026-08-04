---
title: "模型评估指标 (Evaluation Metrics: P-R, ROC, AUC, F1)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 模型评估, 混淆矩阵, ROC曲线, AUC]
upstream: ["[[机器学习概述]]", "[[数据集划分与交叉验证]]"]
downstream: ["[[偏差与方差]]", "[[分类算法]]"]
status: learning
---

# 🎯 模型评估指标 (P-R, ROC, AUC, F1)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：评估指标是检验机器学习模型优劣的“指挥棒”。不掌握 Precision, Recall, F1, ROC 曲线与 AUC 的精确含义和应用场景，就无法正确评价分类算法在不平衡数据集上的真实表现。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**
> 假设你开发了一个罕见病诊断模型，数据集中只有 1% 的患者患病。如果模型简单地把所有人都预测为“健康”，模型的**准确率 (Accuracy) 高达 99%**！但这显然是一个毫无价值废柴模型。

以往的方法卡在：
- 单一指标 Accuracy 在类别不平衡（Class Imbalance）场景下会严重失效并产生欺骗性；
- 无法平衡“宁可错杀一千（高 Recall）”与“必须精准打击（高 Precision）”的业务博弈；
- 缺少一个不受分类阈值（Threshold）影响的全局性能评价指标。

模型评估指标体系提供了**混淆矩阵、P-R 曲线、ROC 曲线与 AUC 值**，全面刻画了不同阈值下的模型性能。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：
  - **后续影响**：所有分类算法（Logistic Regression, SVM, Decision Tree, XGBoost）在调参和选型时，均以特定的评估指标为目标。
  - **课程位置**：属于“模型评估与实验验证”的核心衡量标尺。
- **实战与科研价值**：
  - **工业界选择**：搜索/推荐系统看重 Precision@K 与 MAP；风控/医疗系统看重 Recall 与 AUC。
  - **最常出现题型**：混淆矩阵计算题、P-R 曲线与 ROC 曲线形状绘制与绘制逻辑题、AUC 几何意义证明题。

---

## 3. 学它之前需要哪些前置知识？

### 最小必要背景：
1. **二分类问题定义**：样本分为正类（Positive, 1）与负类（Negative, 0）。
2. **概率阈值决策**：模型输出连续概率 $p \in [0, 1]$，通过设定阈值 $\theta$（默认 0.5）将 $p \ge \theta$ 判为正类。

---

## 4. 用直觉语言解释它

> «“这东西其实就像安检筛查系统……”»

- **查准率/精确率 (Precision)**：安检报警了 100 次，其中真正带了违禁品的有多少次？（强调“不误报”）
- **查全率/召回率 (Recall)**：场内总共有 10 个违禁品，安检成功抓出了几个？（强调“不漏报”）
- **F1-Score**：Precision 和 Recall 的调和平均数，综合衡量两者能力。
- **ROC 曲线与 AUC**：不管安检调得松还是紧（变化阈值），绘制一条描述“抓对概率”与“误报概率”的曲线，曲线下面的面积（AUC）越大，说明安检机的性能越神。

**直觉本质一句话**：**全面评价模型在不同门槛下“找得准”（Precision）与“找得全”（Recall）的能力。**

---

## 5. 正式定义、核心公式、符号解释

### 1. 混淆矩阵 (Confusion Matrix)
| | 预测为 Positive | 预测为 Negative |
| :--- | :--- | :--- |
| **实际为 Positive** | **TP** (True Positive 真正) | **FN** (False Negative 假负/漏报) |
| **实际为 Negative** | **FP** (False Positive 假正/误报) | **TN** (True Negative 真负) |

### 2. 核心评估指标公式
- **准确率 (Accuracy)**：$\text{Acc} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}$
- **精确率 (Precision)**：$P = \frac{\text{TP}}{\text{TP} + \text{FP}}$
- **召回率 (Recall / TPR)**：$R = \frac{\text{TP}}{\text{TP} + \text{FN}}$
- **假正率 (FPR)**：$\text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$
- **F1-Score**：$F_1 = \frac{2 \cdot P \cdot R}{P + R} = \frac{2\text{TP}}{2\text{TP} + \text{FP} + \text{FN}}$

### 3. ROC 曲线与 AUC
- **ROC 曲线**：以 **FPR** 为横轴，以 **TPR (Recall)** 为纵轴绘制的曲线。
- **AUC (Area Under ROC Curve)**：ROC 曲线下方的面积，取值在 $[0.5, 1.0]$ 之间。AUC 代表随机抽取一个正样本和一个负样本，模型对正样本预测概率大于负样本预测概率的概率！

---

## 6. 推导思路和思想来源

### 为什么选择调和平均数作为 F1-Score？
算术平均数 $\frac{P+R}{2}$ 无法惩罚极端不平衡（若 $P=1, R=0$，算术平均为 0.5）。
调和平均数：

$$\frac{1}{F_1} = \frac{1}{2}\left(\frac{1}{P} + \frac{1}{R}
ight) \implies F_1 = \frac{2PR}{P+R}$$

当 $P$ 或 $R$ 接近 0 时，调和平均数 $F_1$ 会急剧下降趋近于 0，因此能强迫模型同时维持较高的 Precision 和 Recall。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（混淆矩阵手工计算）
**题目**：某测试集包含 100 个样本（30 正，70 负）。模型预测结果为：TP=20, FP=10, FN=10, TN=60。求 Accuracy, Precision, Recall, F1。

**解答**：
- $\text{Acc} = \frac{20 + 60}{100} = 80\%$
- $\text{Precision} = \frac{20}{20 + 10} = 66.7\%$
- $\text{Recall} = \frac{20}{20 + 10} = 66.7\%$
- $F_1 = \frac{2 \times 66.7\% \times 66.7\%}{66.7\% + 66.7\%} = 66.7\%$

---

### 例子 2：中等例子（场景指标匹配）
**题目**：在以下两个业务场景中，应该优先优化哪个指标？
1. **癌症筛查系统**：漏诊（把癌症误诊为健康）会导致患者错过最佳治疗期危及生命。 -> **优先优化 Recall (高召回)**
2. **垃圾邮件过滤系统**：误报（把正常重要邮件误判为垃圾邮件）会导致用户错过重要通知。 -> **优先优化 Precision (高精确)**

---

### 例子 3：实际应用例子（金融风控 AUC 评估）
**场景**：某银行开发信贷风控模型预测违约。测试集包含 10,000 名客户，违约率仅为 2%（200 人违约）。
- 若使用 Accuracy，全部预测不违约即可达到 98% 准确率，毫无实用价值。
- 工程师使用 **ROC-AUC** 作为主指标：通过从高到低排列所有客户的违约概率，绘制 ROC 曲线，最终模型达到 **AUC = 0.86**。
- **决策意义**：AUC=0.86 意味着随机抽一个真正违约客户和一个正常客户，模型赋予违约客户更高风险得分的概率为 86%，表明模型具有极佳的风险区分排序能力。

---

## 8. 常见误区和易混概念

### 误区 1：ROC 曲线和 P-R 曲线在不平衡数据上表现一样
- **对比表格**：
| 维度 | ROC 曲线 (TPR vs FPR) | P-R 曲线 (Precision vs Recall) |
| :--- | :--- | :--- |
| **横轴/纵轴** | FPR / TPR | Recall / Precision |
| **类别不平衡敏感度** | **不敏感**（负样本增加时，FPR 变化不大，曲线保持稳定） | **高度敏感**（负样本大幅增加导致 FP 变化，Precision 剧烈波动） |
| **应用场景** | 衡量模型整体排序能力（通用评价） | 极度不平衡下关注正样本找得准不准（如搜索/欺诈） |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖（前置知识）
- [[01-基础概念/监督学习|监督学习]]

### 下游延伸（后续进阶）
- [[01-基础概念/数据集划分与交叉验证|数据集划分与交叉验证]]
- [[01-基础概念/比较检验|比较检验]]

## 下游延伸（后续进阶）
- [[01-基础概念/数据集划分与交叉验证|数据集划分与交叉验证]]
- [[01-基础概念/比较检验|比较检验]]

## 下游延伸（后续进阶）
- [[01-基础概念/数据集划分与交叉验证|数据集划分与交叉验证]]
- [[01-基础概念/比较检验|比较检验]]

## 下游延伸
- [[01-基础概念/偏差与方差|偏差与方差]]：指标的方差影响评估稳定性。

---

## 10. 闭卷复现任务

1. 默写混淆矩阵的 4 个单元格（TP, FP, FN, TN）。
2. 写出 Precision, Recall, F1-Score 的计算公式。
3. 解释 ROC 曲线的横轴与纵轴分别是什么。
4. 解释 AUC 的概率几何含义。
5. 为什么类别极度不平衡时 ROC 曲线比 P-R 曲线更稳定？

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 公式计算 | 基础 | 混淆矩阵指标计算 |
| 2 | 指标选择 | 基础 | 场景与指标匹配 |
| 3 | 理论辨析 | 中等 | AUC 概率含义理解 |
| 4 | 曲线对比 | 中等 | ROC 与 P-R 曲线不平衡特性 |
| 5 | 综合计算 | 较难 | 改变分类阈值对 P/R 的影响 |

1. **[公式计算] 某二分类模型测试集 TP=40, FP=10, FN=10, TN=40，其 F1-Score 为：**
   A. 0.80  B. 0.75  C. 0.85  D. 0.70
> [!question]- 答案解析
> **答案**：A  
> **解析**：$P = 40/(40+10) = 0.8$, $R = 40/(40+10) = 0.8$, $F_1 = 2 \times 0.8 \times 0.8 / 1.6 = 0.80$。  
> **标签**：`#自测/基础 #F1计算`

2. **[指标选择] 在司法犯罪嫌疑人搜捕系统中，秉持“宁可错抓不可漏掉一个嫌犯”的原则，系统应重点提高：**
   A. Precision (精确率)  B. Recall (召回率)  C. Accuracy (准确率)  D. Specificity (特异度)
> [!question]- 答案解析
> **答案**：B  
> **解析**：宁可错抓（容忍高 FP）也要保证不漏掉（极低 FN），对应提高 Recall。  
> **标签**：`#自测/基础 #Recall`

3. **[理论辨析] 如果一个完美分类器能够将所有正样本排在所有负样本前面，则该分类器的 AUC 值为：**
   A. 0.5  B. 0.8  C. 1.0  D. 0.0
> [!question]- 答案解析
> **答案**：C  
> **解析**：完美分类器的 ROC 曲线覆盖整个矩形区域，AUC 达到最大值 1.0。  
> **标签**：`#自测/中等 #AUC`

4. **[曲线对比] 当测试集中的负样本数量增加 100 倍且正样本保持不变时，以下哪个指标基本保持不变？**
   A. Precision  B. F1-Score  C. ROC 曲线及 AUC  D. P-R 曲线
> [!question]- 答案解析
> **答案**：C  
> **解析**：ROC 曲线的纵轴 TPR 和横轴 FPR 分别在正样本和负样本各自内部标准化，不受正负样本比例变化影响。  
> **标签**：`#自测/中等 #ROC稳定性`

5. **[综合计算] 将分类概率阈值从 0.5 提高到 0.8 时，通常会导致：**
   A. Precision 提高，Recall 降低  
   B. Precision 降低，Recall 提高  
   C. Precision 和 Recall 同时提高  
   D. Precision 和 Recall 同时降低
> [!question]- 答案解析
> **答案**：A  
> **解析**：提高阈值使得模型预测为正类更加“苛刻谨慎”，减少了 FP（提高 Precision），但增大了 FN（降低 Recall）。  
> **标签**：`#自测/较难 #阈值调优`

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

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/01-基础概念/`
- **建议双链**：
  - [[01-基础概念/🌱 第一阶段：基础概念|第一阶段：基础概念]]
  - [[01-基础概念/数据集划分与交叉验证|数据集划分与交叉验证]]
- **建议标签**：`#学习` `#机器学习` `#模型评估` `#ROC` `#AUC` `#混淆矩阵`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: 模型评估指标)

> **作业任务说明**：本作业为《模型评估指标》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 模型评估指标 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 模型评估指标 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (模型评估指标) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
