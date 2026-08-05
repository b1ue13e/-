---
title: "强化学习 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "强化学习 4-Tier 阶梯作业规范"
course: "强化学习"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [强化学习, 4Tier作业, 阶梯作业, 编程实战, PyTest, CS188]
---

# 🕹️ 强化学习 4-Tier 阶梯作业全景规范说明书 (Sutton & Berkeley CS188 范式)

> 本说明书为 **13-强化学习** 路径（基于 Sutton 《Reinforcement Learning (2e)》与 Berkeley CS188/CS285）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ Gymnasium / PettingZoo 环境调用 / 状态-动作空间封装 / 算例求解
🟡 L2 - Medium Baseline   │ 衰减因子/探索率调参 / Replay Buffer / Target Network 稳定训练
🔴 L3 - Strong Baseline   │ [核心] 不调用 RL 库，从零手撕 Q-Learning / Policy Gradient / PPO / Actor-Critic 算法
👑 L4 - Boss Baseline     │ 连续控制 (MuJoCo) 冲榜 / 样本效率优化 / 分布式 RL / 形式化收敛证明
```

---

## 🎯 强化学习阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 栅格世界与 MDP 状态-动作转移 (Markov Decision Process)
- **开源溯源**：Sutton Ch 3 / Berkeley CS188 Project 2
- 🟢 **L1**: 在 4x4 GridWorld 中定义状态空间 $S$、动作空间 $A$、转移概率 $P(s'|s,a)$ 与奖励函数 $R(s,a,s')$。
- 🟡 **L2**: 计算固定策略下的折现累计回报 $G_t = \sum_{k=0}^\infty \gamma^k R_{t+k+1}$ 并画出价值热力图。
- 🔴 **L3 (手撕核心)**：**从零手撕 Bellman 期望方程 (Bellman Expectation Equation) 线性方程组求解器**：
  $$ V_\pi(s) = \sum_{a \in A} \pi(a|s) \sum_{s', r} P(s', r | s, a) [r + \gamma V_\pi(s')] $$
- 👑 **L4**: 证明有界奖励下贝尔曼算子的压缩映射性质 (Contraction Mapping Property)。

### 2. HW02 - 动态规划：策略迭代与价值迭代 (Policy & Value Iteration)
- **开源溯源**：Sutton Ch 4 / Berkeley CS188 Pacman Project 2
- 🟢 **L1**: 使用 Python 跑通 GridWorld 策略评估。
- 🟡 **L2**: 实现策略改进 (Policy Improvement) 与价值迭代收敛判断（$\max_s |V_{k+1}(s) - V_k(s)| < \epsilon$）。
- 🔴 **L3 (手撕核心)**：**从零手撕 Bellman 最优算子 (Bellman Optimality Operator) 价值迭代迭代器**：
  $$ V^*(s) = \max_{a \in A} \sum_{s', r} P(s', r | s, a) [r + \gamma V^*(s')] $$
- 👑 **L4**: 针对大规模状态空间实现异步动态规划 (Asynchronous DP / In-Place DP)。

### 3. HW03 - 蒙特卡洛方法与 Temporal-Difference (MC & TD(0) Learning)
- **开源溯源**：Sutton Ch 5 & Ch 6 / CS188 Pacman
- 🟢 **L1**: 在 Blackjack (21点) 环境中收集轨迹，计算 First-Visit MC 状态价值。
- 🟡 **L2**: 实现 On-Policy $\epsilon$-greedy MC 控制与 Off-Policy 重要性采样 (Importance Sampling)。
- 🔴 **L3 (手撕核心)**：**从零手撕 TD(0) 增量更新与 SARSA 算法**：
  $$ Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha [R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)] $$
- 👑 **L4**: 实现 n-step TD 算法，并在不同 $n$ 下绘制偏差-方差权衡曲线。

### 4. HW04 - Q-Learning 与 Pacman 吃到豆人吃吃吃 (Model-Free Control)
- **开源溯源**：Sutton Ch 6 / Berkeley CS188 Pacman Project 3
- 🟢 **L1**: 跑通 CS188 Pacman 游戏环境与 Q-Learning Agent 框架。
- 🟡 **L2**: 设计吃豆人离散状态特征（如最近豆子距离、幽灵距离），实现 Approximate Q-Learning。
- 🔴 **L3 (手撕核心)**：**手撕 Model-Free Q-Learning 离线策略更新公式**：
  $$ Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha [R_{t+1} + \gamma \max_{a} Q(S_{t+1}, a) - Q(S_t, A_t)] $$
- 👑 **L4**: 实现 Double Q-Learning 消除 Q 值的过高估计 (Overestimation Bias)。

### 5. HW05 - 深度 Q 网络 (DQN & Double DQN & Dueling DQN)
- **开源溯源**：DQN (Mnih et al., 2015) / CS285
- 🟢 **L1**: 使用 PyTorch `nn.Module` 构建 Q 网络并在 CartPole-v1 上跑通。
- 🟡 **L2**: 加入 Replay Buffer (经验回放) 与 Target Network 周期性更新。
- 🔴 **L3 (手撕核心)**：**手写 Prioritized Experience Replay (PER) 优先经验回放**（基于 SumTree 数据结构实现抽样与重要性采样权重 $w_i = (N \cdot P(i))^{-\beta}$ 修正）。
- 👑 **L4**: 实现 Dueling DQN 结构（分离 Value 函数 $V(s)$ 与 Advantage 函数 $A(s,a)$）。

### 6. HW06 - 策略梯度算法 (REINFORCE & Policy Gradient)
- **开源溯源**：Sutton Ch 13 / CS285
- 🟢 **L1**: 在 LunarLander-v2 环境使用 Softmax 策略网络跑通 REINFORCE。
- 🟡 **L2**: 引入 Reward-to-go (未来累计回报) 与状态价值 Baseline 降低方差。
- 🔴 **L3 (手撕核心)**：**从零手撕 Policy Gradient 似然比梯度公式 (Likelihood Ratio Gradient)**：
  $$ \nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^T \nabla_\theta \ln \pi_\theta(A_t|S_t) G_t \right] $$
- 👑 **L4**: 实现 Natural Policy Gradient (NPG) 与 Fisher 信息矩阵因子化。

### 7. HW07 - Actor-Critic 与 PPO 策略优化 (A2C & PPO)
- **开源溯源**：PPO (Schulman et al., 2017) / CS285
- 🟢 **L1**: 实现同步 Advantage Actor-Critic (A2C) 基础结构。
- 🟡 **L2**: 计算 Generalized Advantage Estimation (GAE($\gamma, \lambda$))。
- 🔴 **L3 (手撕核心)**：**从零手撕 PPO-Clip 截断概率比率目标函数 (Clipped Surrogate Objective)**：
  $$ L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t) \right] $$
- 👑 **L4**: 在 MuJoCo 连续控制环境 (HalfCheetah / Ant) 上跑通并评估样本效率。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-rl/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-rl/tests/test_hw02_dp.py
pytest 03-Projects/projects-rl/tests/test_hw04_qlearning.py
pytest 03-Projects/projects-rl/tests/test_hw07_ppo.py
```
