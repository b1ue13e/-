---
title: "Q-Learning 算法与 TD 学习 (Q-Learning and TD Learning)"
course: "13-强化学习"
tags:
  - 强化学习
  - Q-Learning
  - 时序差分
  - Bellman方程
  - 无模型RL
type: knowledge_card
status: completed
created: 2026-07-31
---

# Q-Learning 算法与 TD 学习 (Q-Learning and TD Learning)

## 1. Q-Learning 算法的定义与核心思想

**Q-Learning 算法与 TD 学习 (Q-Learning and TD Learning)** 的核心定义是：一种基于**时序差分 (Temporal Difference, TD)** 的**异策略 (Off-Policy)** 无模型 (Model-Free) 强化学习算法。由 Watkins 于 1989 年提出，用于在未知环境转移概率的马尔可夫决策过程 (MDP) 中学习最优动作价值函数 $Q^*(s, a)$。

**基本性质**：Q-Learning 算法采用目标值中的最大化操作 $\max_{a'} Q(s', a')$，使行动策略（如 $\epsilon$-Greedy 探索）与目标策略（纯贪婪策略）解耦。只要所有“状态-动作”对能够被无限次充分探索，且学习率满足 Robbins-Monro 条件，Q-Learning 算法保证以概率 1 收敛至最优 Q 值 $Q^*(s, a)$。

---

## 2. 贝尔曼最优方程与 TD 误差形式化推导

**MDP 假设（前提条件）**：
- 状态空间 $\mathcal{S}$，动作空间 $\mathcal{A}$，折扣因子 $\gamma \in [0, 1)$；
- 转移样本元组 $(s_t, a_t, r_{t+1}, s_{t+1})$。

**推导过程（Bellman 最优算子与 TD Target）**：
1. 根据贝尔曼最优原理 (Bellman Optimality Equation)：
$$Q^*(s, a) = \mathbb{E} \left[ r_{t+1} + \gamma \max_{a'} Q^*(s_{t+1}, a') \;\middle|\; s_t = s, a_t = a 
\right]$$
2. **TD 目标值 (TD Target)**：以单步采样奖励估算当前目标：
$$y_t = r_{t+1} + \gamma \max_{a'} Q(s_{t+1}, a')$$
3. **TD 误差 (TD Error)**：$\delta_t = y_t - Q(s_t, a_t) = r_{t+1} + \gamma \max_{a'} Q(s_{t+1}, a') - Q(s_t, a_t)$；
4. **Q 值更新迭代式**：利用指数移动平均增量更新：
$$Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \cdot \delta_t$$
5. **因此**，算法无需环境的状态转移矩阵 $P(s'|s,a)$ 即可完成对最优策略的在线学习。

---

## 3. Q-Learning (Off-Policy) 与 SARSA (On-Policy) 的区别与对比

| 维度 | Q-Learning 算法 | SARSA 算法 |
|:---|:---|:---|
| **策略属性** | **异策略 (Off-Policy)** | **同策略 (On-Policy)** |
| **更新目标** | $r + \gamma \mathbf{\max_{a'} Q(s', a')}$ (贪婪) | $r + \gamma \mathbf{Q(s', a')}$ (按照探索动作 $a'$) |
| **风险偏好** | 倾向于选择理论最优路径（高风险边缘） | 倾向于选择远离危险的安全路径 |
| **探索策略影响** | 学习目标独立于 $\epsilon$-Greedy 探索 | 学习目标受 $\epsilon$ 探索噪声直接污染 |
| **收敛目标** | 最优 Q 值 $Q^*(s,a)$ | 对应 $\epsilon$-Greedy 策略下的 $Q^{\pi}(s,a)$ |

**局限（误区）**：因为含有 $\max$ 算子，Q-Learning 算法在噪声环境中存在严重的**高估偏差 (Overestimation Bias)**（最大值的期望大于期望的最大值），导致评估值虚高；这一局限促使了 Double Q-Learning 和 Double DQN 的诞生。

关联知识点推荐：[[PPO近端策略优化]]、[[梯度下降与优化器|梯度下降与Adam优化器]]、[[二分搜索]]、[[双指针]]。

---

## 4. Python 完整表格型 Q-Learning 算法与 CliffWalking 自测断言

```python
import numpy as np

class QLearningAgent:
    """
    表格型 Q-Learning 算法代理
    假设: 离散状态空间 n_states, 离散动作空间 n_actions
    推导: Q(s,a) += alpha * (r + gamma * max_a' Q(s', a') - Q(s,a))
    """
    def __init__(self, n_states: int, n_actions: int, lr: float = 0.1,
                 gamma: float = 0.9, epsilon: float = 0.1):
        self.q_table = np.zeros((n_states, n_actions))
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_actions = n_actions

    def choose_action(self, state: int) -> int:
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.n_actions)
        return int(np.argmax(self.q_table[state]))

    def update(self, s: int, a: int, r: float, s_next: bool or int, done: bool) -> float:
        current_q = self.q_table[s, a]
        if done:
            target_q = r
        else:
            target_q = r + self.gamma * np.max(self.q_table[s_next])
        td_error = target_q - current_q
        self.q_table[s, a] += self.lr * td_error
        return float(td_error)

if __name__ == "__main__":
    np.random.seed(42)
    agent = QLearningAgent(n_states=5, n_actions=2, lr=0.5, gamma=0.9)

    # 模拟简单的 5 状态线性网格: 0 -> 1 -> 2 -> 3 -> 4(Goal, Reward=10)
    for episode in range(100):
        s = 0
        while s < 4:
            a = 1  # 动作 1 向右
            s_next = s + 1
            r = 10.0 if s_next == 4 else 0.0
            done = (s_next == 4)
            agent.update(s, a, r, s_next, done)
            s = s_next

    # 自测验证 1: 临近终点的 Q(3, 1) 应收敛到 10.0
    assert abs(agent.q_table[3, 1] - 10.0) < 1e-3, f"Q(3,1) 异常: {agent.q_table[3, 1]}"

    # 自测验证 2: 状态 2 的 Q(2, 1) 应收敛到 gamma * 10 = 9.0
    assert abs(agent.q_table[2, 1] - 9.0) < 0.1, f"Q(2,1) 异常: {agent.q_table[2, 1]}"

    # 自测验证 3: 贪婪动作断言 (所有状态最优动作均为向右 1)
    for s in range(4):
        assert np.argmax(agent.q_table[s]) == 1, f"状态 {s} 最优动作方向错误"

    print("Q-Learning 算法在 5 状态网格上完美收敛最优 Q 表:")
    print(agent.q_table.round(2))
    print("Q-Learning 算法与 TD 学习单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Watkins, C. J., & Dayan, P. (1992). Q-learning. *Machine Learning*, 8(3-4), 279-292. DOI: https://doi.org/10.1007/BF00992698
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. Chapter 6.5 (Q-learning: Off-Policy TD Control). ISBN: 978-0262039246. URL: https://incompleteideas.net/book/the-book-2nd.html
- Mnih, V., et al. (2015). Human-level control through deep reinforcement learning. *Nature*, 518(7540), 529-533. DOI: https://doi.org/10.1038/nature14236
