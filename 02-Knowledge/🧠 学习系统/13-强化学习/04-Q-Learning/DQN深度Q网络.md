---
title: "DQN 深度 Q 网络 (Deep Q-Network)"
course: "强化学习"
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
upstream: ["[[DQN-函数逼近]]", "[[经验回放与目标网络]]"]
tags:
  - 强化学习
  - DQN
  - 深度Q网络
  - 经验回放
  - 目标网络
  - 深度学习
type: study
topic: "DQN深度Q网络"
status: completed
created: 2026-07-31
---

# DQN 深度 Q 网络 (Deep Q-Network)

## 1. DQN 深度 Q 网络的定义与突破

**DQN 深度 Q 网络 (Deep Q-Network)** 的核心定义是：将深度卷积神经网络 (CNN) 作为函数近似器去逼近高维连续状态空间下的 Q 值函数 $Q(s, a; \theta)$，并通过**经验回放 (Experience Replay)** 与**目标网络 (Target Network)** 两大核心机制解决非独立同分布 (Non-i.i.d.) 采样与目标值震荡问题的端到端强化学习算法。DQN 深度 Q 网络由 Mnih 等人于 2013 年在 DeepMind 提出，并于 2015 年发表于 *Nature*。

**基本性质**：DQN 深度 Q 网络实现了从原始像素输入直接输出控制动作的端到端学习，在 49 款 Atari 2600 经典游戏上达到了超越人类玩家的平均水平，开创了深度强化学习 (Deep RL) 的新纪元。

---

## 2. 核心四大稳定机制与目标函数形式化推导

**三大失稳根源（死三角 Dead Triad）**：
在强化学习中同时使用**函数近似 (Function Approximation)**、**异策略 (Off-Policy)** 与**时序差分 (Bootstrapping)** 会引发训练发散崩溃。DQN 深度 Q 网络针对性地引入了四大稳定机制。

**四大稳定机制与损失函数推导**：
1. **经验回放缓冲区 $\mathcal{D}$ (Experience Replay)**：将转移样本 $(s_t, a_t, r_{t+1}, s_{t+1}, \text{done})$ 存入循环队列 $\mathcal{D}$，训练时随机均匀采样 Batch 数据。打断样本时间相关性，使数据满足 i.i.d. 假设；
2. **独立目标网络 (Target Network $\theta^-$)**：使用独立的参数 $\theta^-$ 计算 TD 目标，且 $\theta^-$ 仅每隔 $C$ 步才从主网络同步一次 ($\theta^- \leftarrow \theta$)：
$$y_t^{\text{DQN}} = r_{t+1} + \gamma (1 - \text{done}) \max_{a'} Q(s_{t+1}, a'; \theta^-)$$
3. **均方误差 / Huber 损失函数**：
$$L(\theta) = \mathbb{E}_{(s,a,r,s',\text{done}) \sim \mathcal{D}} \left[ \left( y^{\text{DQN}} - Q(s, a; \theta) 
\right)^2 
\right]$$
4. **梯度剪裁 (Gradient Clipping)**：使用 Huber Loss 防止 TD Error 爆炸。

---

## 3. DQN 及其演进扩展对比

| 算法 Variant | 核心改进机制 | 解决的问题 | 典型公式差异 |
|:---|:---|:---|:---|
| **Vanilla DQN** | 经验回放 + 目标网络 | 采样非 i.i.d.、目标发散 | $y = r + \gamma \max_{a'} Q(s', a'; \theta^-)$ |
| **Double DQN** | **选择与评估解耦** | **消去 Q 值高估偏差** | $y = r + \gamma Q(s', \mathbf{\arg\max_{a'} Q(s', a'; \theta)}; \theta^-)$ |
| **Dueling DQN** | 拆分为 V(s) 与 A(s,a) | 区分状态价值与动作优势 | $Q(s,a) = V(s) + \left(A(s,a) - \frac{1}{|\mathcal{A}|}\sum A
\right)$ |
| **Prioritized Replay (PER)** | 基于 $|TD\_error|$ 优先级采样 | 提升高价值误报样本利用率 | 采样概率 $P(i) \propto |\delta_i|^\alpha$ |

**局限（误区）**：DQN 深度 Q 网络仅能处理**有限离散动作空间**，无法直接输出连续动作（如机器人关节扭矩）；处理连续动作须改用 DDPG 或 SAC 算法。

关联知识点推荐：[[Q-Learning算法]]、[[PPO近端策略优化]]、[[SAC软Actor-Critic]]、[[回归损失函数|均方误差MSE与Huber损失]]。

---

## 4. Python PyTorch 风格 DQN 损失与经验回放自测断言

```python
import numpy as np
from collections import deque
import random

class ReplayBuffer:
    """经验回放缓冲区"""
    def __init__(self, capacity: int = 1000):
        self.buffer = deque(maxlen=capacity)

    def push(self, s, a, r, s_next, done):
        self.buffer.append((s, a, r, s_next, done))

    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        s, a, r, s_next, done = zip(*batch)
        return np.array(s), np.array(a), np.array(r), np.array(s_next), np.array(done)

def compute_dqn_target(r: np.ndarray, s_next: np.ndarray, done: np.ndarray,
                       q_target_next: np.ndarray, gamma: float = 0.99) -> np.ndarray:
    """
    计算 DQN TD Target
    推导: y = r + gamma * (1 - done) * max_{a'} Q_target(s', a')
    """
    max_q_next = np.max(q_target_next, axis=-1)
    target = r + gamma * (1.0 - done.astype(float)) * max_q_next
    return target

if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)

    buffer = ReplayBuffer(capacity=100)
    for i in range(50):
        buffer.push(s=i, a=i%2, r=1.0, s_next=i+1, done=(i==49))

    assert len(buffer.buffer) == 50

    s, a, r, s_next, done = buffer.sample(batch_size=10)
    assert len(s) == 10

    fake_q_target_next = np.array([[1.0, 2.0], [0.5, 0.2], [3.0, 1.0], [0.0, 0.0], [1.0, 1.0],
                                   [0.1, 0.2], [2.0, 2.5], [1.1, 0.9], [4.0, 3.0], [0.0, 0.0]])
    target_q = compute_dqn_target(r, s_next, done, fake_q_target_next, gamma=0.9)

    # 自测验证 1: 样本 0 done=False -> y = 1.0 + 0.9*2.0 = 2.8
    assert abs(target_q[0] - 2.8) < 1e-5

    # 自测验证 2: 终止状态 done=True 样本 -> target_q == r
    r_done = np.array([5.0])
    s_done = np.array([99])
    done_flag = np.array([True])
    q_done_next = np.array([[100.0, 200.0]])
    target_done = compute_dqn_target(r_done, s_done, done_flag, q_done_next, gamma=0.9)
    assert target_done[0] == 5.0

    print("DQN 深度 Q 网络经验回放采样与 TD Target 计算验证成功！")
    print("DQN 深度 Q 网络单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Mnih, V., et al. (2013). Playing Atari with deep reinforcement learning. *NIPS Workshop on Deep Learning*. URL: https://arxiv.org/abs/1312.5602
- Mnih, V., et al. (2015). Human-level control through deep reinforcement learning. *Nature*, 518(7540), 529-533. DOI: https://doi.org/10.1038/nature14236
- van Hasselt, H., Guez, A., & Silver, D. (2016). Deep reinforcement learning with double Q-learning. *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI '16)*, 30(1), 2094-2100. DOI: https://doi.org/10.1609/aaai.v30i1.10295
- Wang, Z., et al. (2016). Dueling network architectures for deep reinforcement learning. *International Conference on Machine Learning (ICML '16)*, 1995-2003. URL: https://arxiv.org/abs/1511.06581
## 学完后可以完成

```dataview
TABLE assignment_level, source_type FROM "03-Projects"
WHERE contains(requires, this.file.link)
```
## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```

## 闭卷自测
1. DQN 如何用神经网络逼近 Q 函数？
2. 经验回放为何能打破样本相关性？
3. 目标网络如何稳定 Q 学习训练？
