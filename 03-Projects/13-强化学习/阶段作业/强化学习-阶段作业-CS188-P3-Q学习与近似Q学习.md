---
type: project
project_type: homework
course: "强化学习"
title: "强化学习-阶段作业-CS188-P3-Q学习与近似Q学习"
assignment_id: "CS188-P3"
assignment_level: stage
assignment_format: lab
stage_id: "04"
requires:
  - "[[MDP 与贝尔曼方程]]"
  - "[[动态规划：策略与值迭代]]"
  - "[[时序差分与 Q-Learning]]"
  - "[[探索与利用]]"
  - "[[🧭 强化学习-前置知识]]"
source_type: official_assignment
source_url: "https://inst.eecs.berkeley.edu/~cs188/fa24/assets/projects/rl/reinforcement.zip"
created: 2026-08-06
updated: 2026-08-06
status: ongoing
flow: project
tags: [作业, 强化学习, 阶段作业]
---

# 强化学习-阶段作业-CS188-P3-Q学习与近似Q学习

> 🎯 **作业目标**：在 Gridworld 与 Pacman 环境中实现 **Value Iteration、Policy Iteration、Q-Learning 与 Approximate Q-Learning**，通过官方 autograder，并对比「表格法 vs 特征化近似」在 Pacman 上的分数差异。这是本课程第一个**真正动手学 RL** 的阶段作业——你将从动态规划（已知模型）走到无模型时序差分（仅从经验学习）。

---

## 1. 身份与边界

- **身份**：强化学习课程阶段作业（stage 级），对应阶段 4（Q-Learning）。
- **对应知识**：`[[MDP 与贝尔曼方程]]`、`[[动态规划：策略与值迭代]]`、`[[时序差分与 Q-Learning]]`、`[[探索与利用]]`。
- **边界（允许 / 禁止）**：
  - ✅ 允许：补全 `valueIterationAgents.py` / `qlearningAgents.py` / `analysis.py`（及复用 `featureExtractors.py` 中 `SimpleExtractor`）。
  - ❌ 禁止：修改 `autograder.py`、`gridworld.py`、`pacman.py`、`game.py`；禁止在 Q-Learning 中直接读取转移概率或奖励函数（必须仅用 `(s,a,r,s')` 样本更新）。
  - ⚠️ Q-Learning 是 **off-policy**：更新目标用 `max_a Q(s',a)`，即便行为策略是 ε-greedy。

---

## 2. 环境与 Starter Code

- **官方来源**：UC Berkeley CS188 *Intro to AI* — Project 3: Reinforcement Learning。
- **获取方式**：官方压缩包 `https://inst.eecs.berkeley.edu/~cs188/fa24/assets/projects/rl/reinforcement.zip`（或镜像 `git clone https://github.com/jwb133/project3`）。
- **关键文件**：
  - `valueIterationAgents.py`：`ValueIterationAgent` / `PolicyIterationAgent`
  - `qlearningAgents.py`：`QLearningAgent` / `ApproximateQAgent`
  - `gridworld.py`（可视化）、`analysis.py`（分析题文字答案）、`featureExtractors.py`、`pacman.py`、`autograder.py`
- **运行方式**：

```bash
python gridworld.py -a value -i 100 -k 10                 # Value Iteration 收敛可视化
python gridworld.py -a q -k 50 -n 10 -l bridge            # Q-Learning 在桥问题上训练
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic
python autograder.py --project=reinforcement              # 官方自动评测（按题打分）
```

- **验收口径**：autograder 按 q1→q7 逐题打分（含分析题文字答案）；只允许补全规定文件。

---

## 3. 题目详述（自包含）

### Q1 — Value Iteration
在 `valueIterationAgents.py` 实现 `ValueIterationAgent`：
- `runValueIteration()`：对所有状态同步执行 Bellman 最优备份 `V(s) ← max_a Σ P(s'|s,a)[R + γV(s')]`，迭代至收敛。
- `getValue(s)` / `getPolicy(s)` / `getAction(s)` / `getQValue(s,a)`。
- 关键数据：小 MDP 上迭代收敛后 `getPolicy` 应给出最优动作；`gridworld.py -a value -i 100 -k 10` 可见收敛。

### Q2 — Policy Iteration
实现 `PolicyIterationAgent`：`evaluatePolicy()`（策略评估，解 `V^π`）与 `policyIteration()`（评估→贪心改进循环）。
- 对比：PI 通常轮数少于 VI，但每轮更重；两者最终 `getPolicy` 一致。

### Q3 — Q-Learning
实现 `QLearningAgent`：
- `getQValue(s,a)`、`computeValueFromQValues(s)`（取 max）、`computeActionFromQValues(s)`（ε-greedy 选动作）、`getAction(s)`（ε 概率随机探索）、`update(s,a,r,s')`。
- 更新式：`Q(s,a) ← Q(s,a) + α[r + γ·max_a' Q(s',a') − Q(s,a)]`。
- 关键数据：Gridworld 上 `update` 单步数值可被单测校验（见下方断言）。

### Q4 — 分析题：Epsilon-Greedy
在 `analysis.py` 回答：固定其他参数，改变探索率 ε 对最终策略与收敛速度的影响；给出直觉与 Gridworld 实验证据。

### Q5 — 分析题：Bridge Crossing
分析 `bridge` 布局：折扣因子 γ、环境噪音（随机转移概率）、存活奖励（living reward）如何共同决定 Pacman 是否敢过桥；用实验数据支撑结论。

### Q6 — Q-Learning 与 Pacman
用 Q3 的 `QLearningAgent` 在 `mediumClassic` 训练（参数如 `-x 50 -n 60`），报告最终平均分；说明 ε-greedy 探索的作用。

### Q7 — Approximate Q-Learning
实现 `ApproximateQAgent`：线性 Q 函数 `Q(s,a)=Σ_i w_i·f_i(s,a)` 与权重更新
`w_i ← w_i + α·(r + γ·max_a' Q(s',a') − Q(s,a))·f_i(s,a)`。
- 特征：最近鬼距离、最近食物距离、停驻惩罚（`SimpleExtractor`）。
- 评测：在 `mediumClassic` 上对比「表格 Q-Learning vs 近似 Q-Learning」最终分数。

---

## 4. 提交产物

- 修改后文件：`valueIterationAgents.py`、`qlearningAgents.py`、`analysis.py`（仅这三个）。
- 提交形式：打包三文件 + `README`（≤250 字：各题得分、表格 vs 近似 Q 在 Pacman 的最终分对比、Q4/Q5 的核心结论）。
- 附：Q3 `update` 单测通过截图或终端输出（可选但推荐）。

---

## 5. 评分 Rubric（满分 100）

| 维度 | 分值 | 标准 |
| :--- | :---: | :--- |
| 动态规划（Q1/Q2） | 25 | VI/PI 收敛且 `getPolicy` 最优；PI 轮数合理 |
| Q-Learning 正确性（Q3/Q6） | 30 | `update` 数值正确；Pacman 训练后得分显著提升 |
| 分析题（Q4/Q5） | 20 | 结论有实验支撑、直觉正确 |
| 近似 Q-Learning（Q7） | 20 | 权重更新式正确；近似法分数 > 表格法 |
| 代码与 README | 5 | 仅改规定文件、说明清晰 |

---

## 6. 基础要求、必要提示与常见错误

- **必要提示**：Q-Learning 单步更新用 `max_a' Q(s',a')`（下一状态的最优动作值），而不是 `computeActionFromQValues(s')`（那会带入 ε-greedy 探索）；二者差异正是 off-policy 的关键。
- **常见错误**：① 在 `computeValueFromQValues` 里对空动作集返回 `0` 而非 `-inf`，导致错误贪心；② 把 `update` 写成 `Q ← α·target`（漏了旧值项）；③ Approximate Q 的 `getWeights` 未初始化新特征权重为 0；④ 用 `s'` 的 ε-greedy 动作而非 `max` 构造 TD 目标。
- **本地断言（快速定位 bug）**：

```python
from qlearningAgents import QLearningAgent
agent = QLearningAgent(alpha=0.5, epsilon=0.0, gamma=0.9)
agent.setQValue((1, 1), "East", 0.0)
agent.update((1, 1), "East", 10.0, (2, 1), [(2, 1, "North")])
# Q ← Q + α·(r + γ·max Q(s') − Q) = 0 + 0.5·(10 + 0.9·0 − 0) = 5.0
assert abs(agent.getQValue((1, 1), "East") - 5.0) < 1e-9
```

---

## 7. 可选进阶任务（非主任务前置）

- 在 `mediumClassic` 上系统扫描 (α, γ, ε) 画热力图，找出最优超参区。
- 自设计一组特征（如「被鬼包围度」），对比 `SimpleExtractor` 的分数。
- 把 Approximate Q 的线性函数换成小网络（函数近似），观察泛化增益。

---

## 8. 自检清单

- [ ] `autograder.py --project=reinforcement` q1–q7 通过
- [ ] 上述 `test_q_update` 断言通过（数值正确）
- [ ] Pacman 上近似 Q 分数 > 表格 Q 分数
- [ ] Q4/Q5 结论有 Gridworld 实验数据

---

## 9. 来源与后续入口

- **来源**：题号、要求、布局与评分口径翻译自 UC Berkeley CS188 Project 3（教育用途），保持原题意图；本地未改写公式与提交语义。
- **后续入口**：本作业后进入 `[[强化学习-阶段作业-HW02-DQN与PPO连续动作控制|阶段作业 HW02 DQN 与 PPO 连续控制]]`（深度 RL），或挑战 `[[强化学习-大作业-从表格Q学习到深度策略梯度|大作业：从表格 Q 到深度策略梯度]]`。
- **复习卡**：`[[时序差分与 Q-Learning]]`、`[[动态规划：策略与值迭代]]`、`[[探索与利用]]`。

---

## 🃏 知识内化卡片

- Q：Value Iteration 与 Policy Iteration 的收敛方式有何区别？
- A：VI 对全部状态同步执行 Bellman 最优备份直到值函数收敛（轮数可能很多）；PI 先对当前策略做策略评估，再贪心改进策略，通常轮数更少但每轮计算更重。
- Q：为什么 Q-Learning 是 off-policy 算法？
- A：更新目标使用贪心策略的 `max_a Q(s',a)`，而非行为策略本身；即使按 ε-greedy 探索采样，也能直接学习最优 Q 值，行为策略只影响样本分布。
- Q：Approximate Q-Learning 的权重更新式是什么？
- A：`w_i ← w_i + α·(r + γ·max_a' Q(s',a') − Q(s,a))·f_i(s,a)`，即 TD 误差乘以对应特征值；线性特征组合让价值泛化到从未访问过的状态。
- Q：为什么加入「最近鬼距离 / 停驻惩罚」特征能提升 Pacman 表现？
- A：鬼距离特征让 agent 学会避险，停驻惩罚抑制原地不动；表格 Q-Learning 无法在连续/大状态上泛化，近似 Q 用特征把相似状态绑定，采样效率与最终分数更高。
