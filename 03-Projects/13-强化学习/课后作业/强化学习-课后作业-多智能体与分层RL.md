---
type: project
project_type: homework
course: "强化学习"
title: "强化学习-课后作业-多智能体与分层RL"
assignment_id: "RL-HW13"
assignment_level: lesson
assignment_format: exercise
stage_id: "10"
source_type: local_integration_task
accessed: "2026-08-07"
license: "[待验证]"
source: "本课程（强化学习）自编形成性练习，参考原始论文（见文末）；非任何名校官方作业，不冒充官方题面。"
created: 2026-08-07
status: ongoing
flow: project
tags: [作业, 强化学习, 课后作业, 广度补全]
requires:
  - "[[多智能体RL概述]]"
  - "[[IQL (Independent Q-Learning)]]"
  - "[[MADDPG]]"
  - "[[Self-Play与PSRO]]"
  - "[[分层RL与Options]]"
---

# 强化学习-课后作业-多智能体与分层RL

> 🎯 **作业目标**：阶段10 MARL(IQL/MADDPG/PSRO)与分层RL(Options)的理解。对应阶段10（多智能体与分层RL）。

---

## 1. 身份与边界

- **身份**：课后作业(lesson级)，对应阶段10（多智能体与分层RL）。
- **对应知识**：多智能体RL概述 / IQL / MADDPG / Self-Play与PSRO / 分层RL与Options。
- **边界**：✅ 允许纸笔推导与博弈矩阵分析；❌ 禁止冒充官方作业。

---

## 2. 题目详述（自包含）

### Q1 — 联合收益矩阵
两智能体各 2 动作，联合收益：(a1,a1)=0, (a1,a2)=1, (a2,a1)=1, (a2,a2)=−1。
- 合作目标（max 联合回报）最优解是什么？若两智能体各自自私会收敛到哪个（囚徒困境式）？

### Q2 — IQL 更新
写出 IQL 每个智能体的 Q 更新式；为何在对手也在学时理论不保证收敛？

### Q3 — MADDPG 的 CTDE
训练期中心 Critic 看到什么、执行期 Actor 看到什么？为何中心化训练能缓解非平稳？

### Q4 — PSRO 种群
石头剪刀布：种群先 {石头} → 加布 → 加剪刀 → 趋近均匀纳什。说明 PSRO 用"种群"解决了 Self-Play 的什么问题。

### Q5 — Options 三要素
分层RL 中 Option 由哪三部分构成？时间抽象为何能降低长程任务的探索难度？

---

## 3. 评分 Rubric（满分100）

| 维度 | 分值 | 标准 |
| :--- | :---: | :--- |
| Q1 收益矩阵 | 20 | 合作最优与自私均衡正确 |
| Q2 IQL | 20 | 更新式与不收敛理由正确 |
| Q3 MADDPG | 20 | CTDE 训练/执行区分正确 |
| Q4 PSRO | 20 | 种群作用正确 |
| Q5 Options | 20 | 三要素与降难解释正确 |

---

## 4. 参考论文（知识点来源，非官方作业）

Tan 1993 (IQL); Lowe 2017 (MADDPG); Silver 2017 / Lanctot 2017 (Self-Play/PSRO); Sutton 1999 (Options)。

---

## 5. 环境与 Starter（可直接运行）

> 纯标准库实现。存为 `starter_hw13.py` 后 `python starter_hw13.py`，观察 CTDE 联合 critic 与最简 self-play。

```python
import random
random.seed(0)
def joint_critic(obs_list, W, b):
    x=[v for o in obs_list for v in o]
    return sum(W[i]*x[i] for i in range(len(x))) + b
n_agents=3; obs_dim=2
W=[random.uniform(-1,1) for _ in range(n_agents*obs_dim)]; b=0.0
obs_list=[[random.random() for _ in range(obs_dim)] for _ in range(n_agents)]
q=joint_critic(obs_list, W, b)
print("agents:",n_agents,"joint-obs dim:",n_agents*obs_dim,"Q=",round(q,4))
def player(s,o): return 1 if s>o else 0
wins=sum(player(random.random(), random.random()) for _ in range(100))
print("self-play random vs random wins/100 =", wins)
```

---

## 6. 来源声明（诚实标注）

本作业 `source_type: local_integration_task`，为**本课程（强化学习）自编形成性练习**。
- 诚实说明：非任何名校官方作业，不冒充官方题面；题面与验收由本课程独立制定，参考下列原始论文作为知识点来源（论文引用不等于官方作业）。
- 许可：[待验证]；访问日期 2026-08-07。
