---
title: "强化学习-题型-CS188-P3-Pacman强化学习阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "强化学习作业"
course: "13-强化学习"
created: 2026-08-03
updated: 2026-08-03
date: 2026-08-03
status: learning
difficulty: advanced
importance: A
concept: ["价值迭代", "策略迭代", "Q-Learning", "近似Q-Learning", "特征工程"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/13-强化学习/MDP与贝尔曼方程|MDP与贝尔曼方程]]", "[[02-Knowledge/🧠 学习系统/13-强化学习/价值迭代与策略迭代|价值迭代与策略迭代]]", "[[02-Knowledge/🧠 学习系统/13-强化学习/Q-Learning算法|Q-Learning算法]]", "[[02-Knowledge/🧠 学习系统/13-强化学习/探索与利用|探索与利用]]"]
related: ["[[强化学习 - CS188-P1：Pacman 搜索阶梯作业]]", "[[强化学习 - CS188-P2：多智能体搜索阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/13-强化学习/🧭 开源作业体系-强化学习|开源作业体系-强化学习]]"]
downstream: []
tags: [学习, 13-强化学习, 作业, 实战, 阶梯作业]
aliases: ["CS188-P3-RL", "Pacman强化学习作业"]
---

# 强化学习 - CS188-P3：Pacman 强化学习阶梯作业

> 🎯 **作业目标**：在 Gridworld 与 Pacman 环境中实现 Value Iteration、Policy Iteration、Q-Learning 与 Approximate Q-Learning（特征：最近鬼距离 / 食物距离 / 停驻惩罚），通过 CS188 官方 autograder，并对比表格法 vs 特征化近似的分数差异。

---

## 1. ⚙️ 环境与 Starter Code（CS188 官方 Pacman 项目）

- **官方来源**：Berkeley CS188 Intro to AI Project 3 Reinforcement Learning（http://ai.berkeley.edu/project_overview.html）
- **关键文件**：`valueIterationAgents.py`（ValueIterationAgent）、`qlearningAgents.py`（QLearningAgent、ApproximateQAgent）、`gridworld.py`（可视化）、`analysis.py`（策略分析题）、`featureExtractors.py`（特征提取器）、`pacman.py`、`autograder.py`
- **核心依赖**：Python 3 + 官方 pacman 项目包（表格法 RL，无深度学习依赖）
- **运行方式**：

```bash
python gridworld.py -a value -i 100 -k 10                 # Value Iteration 收敛可视化
python gridworld.py -a q -k 50 -n 10 -l bridge            # Q-Learning 在桥问题上训练
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic   # 特征化 Q-Learning
python autograder.py -q q1 -q q2                          # 官方自动评测（按题打分）
```

- **验收口径**：autograder 按 q1 Value Iteration → q7 Approximate Q-Learning 逐题打分（含分析题文字答案）；只允许补全 `valueIterationAgents.py` / `qlearningAgents.py` / `analysis.py`，不得修改评测逻辑。

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 评测环境 / 验收 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | Gridworld，autograder q1-q2 | 实现 `ValueIterationAgent`：`runValueIteration`（全状态同步 Bellman 备份）、`getValue` / `getPolicy` / `getQValue`；完成 `policiesMatch` 一致性检查（q2）；`python gridworld.py -a value -i 100 -k 10` 显示收敛。 |
| 🟡 **L2 - Medium Baseline** | Gridworld，autograder q4-q5（analysis） | 完成 `analysis.py` 分析题：q4 epsilon-greedy（探索参数 ε 对策略的影响）、q5 bridge crossing（桥问题上折扣因子 γ / 噪音 / 活奖励的影响）；用 Gridworld 可视化验证分析结论。 |
| 🔴 **L3 - Strong Baseline** | smallGrid / mediumClassic，autograder q3 + q6 | 实现 `QLearningAgent`：`getQValue` / `computeValueFromQValues` / `computeActionFromQValues` / `update`（TD 更新式），ε-greedy 探索（q3 在 Gridworld 通过，q6 在 Pacman 上训练后得分显著提升）。 |
| 👑 **L4 - Boss Baseline** | mediumClassic，autograder q7 | 实现 `ApproximateQAgent`：线性 Q 函数 Q(s,a)=Σ wᵢ·fᵢ(s,a) 与权重更新；特征采用最近鬼距离、最近食物距离、停驻惩罚（`SimpleExtractor`）；对比表格 Q-Learning 与 Approximate Q-Learning 的最终分数。 |

---

## 3. 🧪 自动化测试 Harness（官方 autograder + Python 断言）

```bash
# 官方 autograder 全量评测（P3 共 7 题）
python autograder.py --project=reinforcement
# 单题复跑
python autograder.py -q q1   # value iteration
python autograder.py -q q6   # q-learning
python autograder.py -q q7   # approximate q
```

```python
# 本地轻量断言：Q-Learning 单步 TD 更新正确性
from qlearningAgents import QLearningAgent

def test_q_update():
    agent = QLearningAgent(alpha=0.5, epsilon=0.0, gamma=0.9)
    agent.setQValue((1, 1), "East", 0.0)
    agent.update((1, 1), "East", 10.0, (2, 1), [(2, 1, "North")])
    # Q ← Q + α·(r + γ·max Q(s') − Q) = 0 + 0.5·(10 + 0.9·0 − 0) = 5.0
    assert abs(agent.getQValue((1, 1), "East") - 5.0) < 1e-9
```

> 注：官方评测以 autograder 输出为准；本地断言校验核心更新式的数值正确性，便于快速定位 bug。

---

## 🃏 Anki 卡片

- Q: Value Iteration 与 Policy Iteration 的收敛方式有何区别？
- A: VI 对全部状态同步执行 Bellman 最优备份直到值函数收敛（轮数可能很多）；PI 先对当前策略做策略评估，再贪心改进策略，通常轮数更少但每轮计算更重。
- Q: 为什么 Q-Learning 是 off-policy 算法？
- A: 更新目标使用贪心策略的 max_a Q(s',a)，而非行为策略本身；即使按 ε-greedy 探索采样，也能直接学习最优 Q 值，行为策略只影响样本分布。
- Q: Approximate Q-Learning 的权重更新式是什么？
- A: wᵢ ← wᵢ + α·(r + γ·max_a Q(s',a) − Q(s,a))·fᵢ(s,a)，即 TD 误差乘以对应特征值；线性特征组合让价值泛化到从未访问过的状态。
- Q: 为什么加入「最近鬼距离 / 停驻惩罚」特征能提升 Pacman 表现？
- A: 鬼距离特征让 agent 学会避险（价值泛化到危险区域），停驻惩罚抑制原地不动；表格 Q-Learning 无法在连续/大状态上泛化，近似 Q 用特征把相似状态绑定，采样效率与最终分数更高。

---
