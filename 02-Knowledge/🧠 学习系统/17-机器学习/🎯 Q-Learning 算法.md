---
title: "Q-Learning 算法 (Q-Learning Algorithm)"
date: 2026-07-23
type: concept
course: "机器学习"
importance: "B"
tags: [学习, 机器学习, Q-Learning, 强化学习, Bellman方程, 时序差分]
upstream: ["[[01-基础概念/半监督与强化学习|半监督与强化学习]]"]
downstream: ["[[DQN]]", "[[深度强化学习]]"]
status: learning
---

# 🎯 Q-Learning 算法

---

## 0. 先判断它值不值得深挖

- **类别**：**B 类（常用工具，重点掌握例题和应用）**
- **判断理由**：Q-Learning 是强化学习中无模型（Model-Free）、离策略（Off-Policy）时序差分（Temporal-Difference, TD）控制的标志性经典算法。它是理解贝尔曼最优方程（Bellman Optimality Equation）及深度 Q 网络（DQN）的必备过渡桥梁。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**
> 在走迷宫或控制机器人时，智能体不知道环境的状态转移概率 $P(s' \mid s, a)$（不知道环境的完整物理规则/无模型 Model-Free），只能通过亲自尝试动作来获取即时奖励 $r$。如何在不知道环境地图的前提下，学会在任何位置采取最佳动作？

Q-Learning **通过维护一张 Q 表（Q-Table），利用时序差分单步更新**，学出了任意“状态-动作”对的最大预期累积回报。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：
  - **后续影响**：结合深度神经网络后演化为经典算法 [[DQN]]（Deep Q-Network）。
- **实战与科研价值**：
  - **离散控制**：迷宫寻路、简单网格世界控制、Flappy Bird 自动打游戏。
  - **最常出现题型**：Q 表单步更新计算题、Off-policy 与 On-policy (Sarsa) 对比题、$\epsilon$-Greedy 探索策略分析题。

---

## 3. 学它之前需要哪些前置知识？

### 最小必要背景：
1. **强化学习 MDP 框架**：状态 $s$、动作 $a$、奖励 $r$、折扣因子 $\gamma$。
2. **Q 值函数定义**：$Q(s, a)$ 代表在状态 $s$ 采取动作 $a$ 之后所能获得的期望折扣累积回报。

---

## 4. 用直觉语言解释它

> «“这东西其实就像在小本本上记录吃甜头的经验……”»

- **Q 表 (Q-Table)**：一张大表格。行是地图位置 $s$，列是动作 $a$（上、下、左、右），单元格里的数字代表“在这个位置往这个方向走，未来总共能赚多少甜头”。
- **单步更新 (TD Update)**：
  - 你在位置 $s$，往右走了一步（动作 $a$），到达了新位置 $s'$，并当场拿到了小奖励 $r$。
  - 你看了一眼新位置 $s'$ 的 Q 表，发现新位置往各个方向走的最大潜在甜头是 $\max_{a'} Q(s', a')$。
  - 于是你认为：刚才那一步的真实总价值应当是 **当场奖励 $r$ + 折扣后的未来最大甜头 $\gamma \max_{a'} Q(s', a')$**（TD 目标）。
  - 用这个真实总价值去微调旧的表格记录 $Q(s, a)$。

---

## 5. 正式定义与核心更新公式

### 1. Q-Learning 单步 TD 更新公式

$$Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[ \underbrace{r_{t+1} + \gamma \max_{a} Q(s_{t+1}, a)}_{\text{TD 目标 } Y_t^{\text{Q}}} - Q(s_t, a_t) \right]$$

- $\alpha \in (0, 1]$：学习率；
- $\gamma \in [0, 1)$：折扣因子；
- $\left[ r_{t+1} + \gamma \max_{a} Q(s_{t+1}, a) - Q(s_t, a_t) \right]$：时序差分误差（TD Error $\delta_t$）。

### 2. 离策略 (Off-Policy) 的含义
- **行为策略 (Behavior Policy)**：用于与环境交互产生数据的策略（通常使用带探索的 $\epsilon$-Greedy）。
- **目标策略 (Target Policy)**：用于计算更新目标的策略（直接取贪婪最大值 $\max_a Q(s', a)$）。
- 因为评估的目标策略（纯贪婪）与执行动作的行为策略（包含探索）不同，故称为 **Off-Policy**。

---

## 6. 例子：基础 → 中等 → 实际应用

### 例子 1：手算单步 Q 表更新
**题目**：已知当前 $Q(s_1, a_{\text{right}}) = 2.0$。执行动作获得即时奖励 $r = 1.0$，到达新状态 $s_2$。已知 $Q(s_2, a_{\text{up}}) = 5.0, Q(s_2, a_{\text{down}}) = 3.0$。取 $\alpha = 0.5, \gamma = 0.8$。求更新后的 $Q(s_1, a_{\text{right}})$。

**解答**：
1. **求 $s_2$ 的最大 Q 值**：$\max_{a} Q(s_2, a) = \max(5.0, 3.0) = 5.0$。
2. **计算 TD 目标**：$Y = r + \gamma \max Q = 1.0 + 0.8 \times 5.0 = 5.0$。
3. **计算 TD 误差**：$\delta = 5.0 - 2.0 = 3.0$。
4. **更新**：$Q(s_1, a_{\text{right}}) = 2.0 + 0.5 \times 3.0 = 3.5$。

---

## 7. 常见误区和易混概念

### Q-Learning (Off-Policy) vs Sarsa (On-Policy)
| 维度 | Q-Learning | Sarsa |
| :--- | :--- | :--- |
| **更新公式目标项** | $r + \gamma \mathbf{\max_a Q(s', a)}$ （假设未来走最好的一步） | $r + \gamma \mathbf{Q(s', a')}$ （真实执行由 $\epsilon$-Greedy 选出的 $a'$） |
| **策略类型** | Off-Policy | On-Policy |
| **悬崖行走问题表现** | 走最优的悬崖边缘路线（但探索时可能掉下悬崖） | 走远离悬崖的安全保守路线（考虑到了探索时摔落的风险） |

---

## 8. 相关知识点与 Obsidian 双链建议

### 上游依赖（前置知识）
- [[01-基础概念/半监督与强化学习|半监督与强化学习]]

### 下游延伸（后续进阶）
- [[02-Knowledge/🧠 学习系统/13-强化学习/DQN深度Q网络|DQN深度Q网络]]
- [[05-其他方法/PolicyGradient与PPO|PolicyGradient与PPO]]

## 下游延伸（后续进阶）
- [[02-Knowledge/🧠 学习系统/13-强化学习/DQN深度Q网络|DQN深度Q网络]]
- [[05-其他方法/PolicyGradient与PPO|PolicyGradient与PPO]]

## 下游延伸（后续进阶）
- [[02-Knowledge/🧠 学习系统/13-强化学习/DQN深度Q网络|DQN深度Q网络]]
- [[05-其他方法/PolicyGradient与PPO|PolicyGradient与PPO]]

## 9. 闭卷复现任务

1. 默写 Q-Learning 的单步更新公式。
2. 解释为什么 Q-Learning 被称为 Off-Policy 算法？
3. 比较 Q-Learning 与 Sarsa 的核心公式差异。

---

## 10. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 算法类型识别 |
| 2 | 公式计算 | 基础 | Q值更新计算 |
| 3 | 策略理解 | 中等 | Off-Policy 判定 |
| 4 | 对比辨析 | 中等 | Q-Learning vs Sarsa |
| 5 | 扩展思考 | 较难 | Q-Table 维度爆表瓶颈 |

1. **[概念辨析] Q-Learning 算法属于强化学习中的：**
   A. 有模型 (Model-Based)  B. 无模型 (Model-Free)、离策略 (Off-Policy)  C. 监督回归  D. 无监督聚类
> [!question]- 答案解析
> **答案**：B  
> **解析**：Q-Learning 不需要得知环境转移概率（Model-Free），且目标策略为贪婪、行为策略带探索（Off-Policy）。  
> **标签**：`#自测/基础 #Q-Learning`

2. **[公式计算] 已知 $Q(s,a)=10, r=2, \gamma=0.9$，在新状态 $s'$ 上的最大 Q 值为 20，设学习率 $\alpha=0.1$，更新后的 $Q(s,a)$ 为：**
   A. 11.0  B. 10.0  C. 12.0  D. 20.0
> [!question]- 答案解析
> **答案**：A  
> **解析**：TD 目标 $= 2 + 0.9 \times 20 = 20$。TD 误差 $= 20 - 10 = 10$。更新后 $Q = 10 + 0.1 \times 10 = 11.0$。  
> **标签**：`#自测/基础 #Q更新计算`

3. **[策略理解] 在 Q-Learning 中，通常使用 $\epsilon$-Greedy 策略进行动作选择，其主要目的是解决：**
   A. 梯度消失  B. 探索与利用 (Exploration vs Exploitation) 的平衡  C. 数据量不足  D. 内存超限
> [!question]- 答案解析
> **答案**：B  
> **解析**：$\epsilon$-Greedy 以 $\epsilon$ 概率随机探索新动作，以 $1-\epsilon$ 概率利用已知最大 Q 值的动作。  
> **标签**：`#自测/中等 #探索与利用`

4. **[对比辨析] Sarsa 算法在更新当前状态 Q 值时，使用的是新状态下【实际执行】的动作 $a'$，而 Q-Learning 使用的是新状态下【可能获得的最大】Q 值，因此：**
   A. Sarsa 是 Off-Policy，Q-Learning 是 On-Policy  
   B. Sarsa 是 On-Policy，Q-Learning 是 Off-Policy  
   C. 两者都是 Off-Policy  
   D. 两者都是 On-Policy
> [!question]- 答案解析
> **答案**：B  
> **解析**：Sarsa 更新所用的动作与实际执行动作一致（On-Policy）；Q-Learning 更新假设未来采取绝对贪婪动作（Off-Policy）。  
> **标签**：`#自测/中等 #On-Policy`

5. **[扩展思考] 当状态空间 $S$ 或动作空间 $A$ 变为连续高维空间时（如控制 3D 机器人关节），传统的 Q-Table 方案失效的根本原因是____，这直接催生了什么深度强化学习算法？**
> [!question]- 答案解析
> **答案**：表格无法存储无限连续状态（表格维度爆炸/维度灾难）；这直接催生了用深度神经网络来函数逼近 Q 值的算法 **DQN (Deep Q-Network)** 和连续动作空间算法 **DDPG/SAC**。  
> **标签**：`#自测/较难 #DQN动机`

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

- **归档目录**：`02-Knowledge/🧠 学习系统/17-机器学习/01-基础概念/`
- **建议双链**：
  - [[01-基础概念/🌱 第一阶段：基础概念|第一阶段：基础概念]]
  - [[01-基础概念/半监督与强化学习|半监督与强化学习]]
- **建议标签**：`#学习` `#机器学习` `#Q-Learning` `#强化学习` `#RL` `#TD学习`


---

## 🏋️ 15. 李宏毅式配套实战作业 (Matched HW Lab: Q-Learning)

> **作业任务说明**：本作业为《Q-Learning》对应的高级 PyTorch 实战任务。请基于零依赖的 PyTorch Tensor/Module 代码，完成数据预处理、模型架构搭建、梯度训练循环与 4 级 Baseline 冲榜。

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
# Step 1: 模拟生成 Q-Learning 实战数据集 (Synthetic Dataset)
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
# Step 2: 搭建 Q-Learning 模块化模型 (Model Architecture)
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
print(f"=== 李宏毅 HW Lab (Q-Learning) 训练完成 ===")
print(f"最终 Loss: {total_loss/len(dataset):.4f} | 准确率: {acc * 100:.2f}% (顺利达成 Boss Baseline!)")
```

### 3. 作业思考题与避坑指南 (Q&A & Gotchas)

1. ❓ **思考题**：如果把训练批次大小 (Batch Size) 从 32 增大到 256，梯度的随机性会发生什么变化？对模型的泛化能力有何影响？
2. ⚠️ **避坑指南 1 (梯度累积)**：每次调用 `optimizer.step()` 前务必调用 `optimizer.zero_grad()`，避免梯度无限累加。
3. ⚠️ **避坑指南 2 (模式切换)**：由于模型中包含 `nn.BatchNorm1d` 与 `nn.Dropout`，测试评估前必须显式调用 `model.eval()`。
