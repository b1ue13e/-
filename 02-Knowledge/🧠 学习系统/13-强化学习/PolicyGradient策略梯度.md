---
title: "PolicyGradient 策略梯度算法 (Policy Gradient Algorithm)"
course: "13-强化学习"
tags:
  - 强化学习
  - PolicyGradient
  - 策略梯度
  - REINFORCE
  - 策略表达
  - 似然比技巧
type: knowledge_card
status: completed
created: 2026-08-01
---

# PolicyGradient 策略梯度算法 (Policy Gradient Algorithm)

## 1. PolicyGradient 策略梯度算法的定义与蒙特卡洛策略更新

**PolicyGradient 策略梯度算法 (Policy Gradient Algorithm)** 的核心定义是：一种通过参数化策略函数 $\pi_\theta(a|s)$ 直接对策略参数 $\theta$ 计算期望回报的目标函数梯度，并沿着**梯度上升方向**更新策略以最大化累积期望奖励的无模型强化学习算法。由 Ronald J. Williams 于 1992 年在 REINFORCE 算法中提出。

**基本性质与动机**：区别于基于 Value 的算法 (如 Q-Learning 只能处理离散动作)，PolicyGradient 策略梯度算法能够天然处理**连续动作空间**以及**随机性最优策略 (Stochastic Policy)**；然而，纯蒙特卡洛策略梯度存在**高方差 (High Variance)** 与**采样效率低下**的缺点。

---

## 2. 策略梯度定理 (Policy Gradient Theorem) 形式化推导

**目标函数假设**：
设轨迹为 $\tau = (s_0, a_0, s_1, a_1, \dots, s_T, a_T)$，其发生的概率密度为 $P(\tau; \theta) = \mu(s_0) \prod_{t=0}^T \pi_\theta(a_t|s_t) P(s_{t+1}|s_t, a_t)$，轨迹总回报为 $R(\tau) = \sum_{t=0}^T \gamma^t r_t$。

优化目标为求解期望回报最大化：
$$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}[R(\tau)] = \int P(\tau; \theta) R(\tau) d\tau$$

**推导过程（Log-Derivative / 对数似然比技巧 Log-Likelihood Ratio Trick）**：
1. 对目标函数偏导：
$$

\nabla_\theta J(\theta) = \int 

\nabla_\theta P(\tau; \theta) R(\tau) d\tau$$
2. 利用对数求导恒等式 $

\nabla_\theta P(\tau; \theta) = P(\tau; \theta) 

\nabla_\theta \log P(\tau; \theta)$：
$$

\nabla_\theta J(\theta) = \int P(\tau; \theta) 

\nabla_\theta \log P(\tau; \theta) R(\tau) d\tau = \mathbb{E}_{\tau \sim \pi_\theta} \left[ 

\nabla_\theta \log P(\tau; \theta) R(\tau) 
\right]$$
3. 将轨迹概率 $P(\tau;\theta)$ 取对数，因为初始分布 $\mu(s_0)$ 与环境状态转移 $P(s_{t+1}|s_t, a_t)$ 与参数 $\theta$ 无关，偏导为 0：
$$\log P(\tau; \theta) = \log \mu(s_0) + \sum_{t=0}^T \log \pi_\theta(a_t|s_t) + \sum_{t=0}^T \log P(s_{t+1}|s_t, a_t)$$
$$

\nabla_\theta \log P(\tau; \theta) = \sum_{t=0}^T 

\nabla_\theta \log \pi_\theta(a_t|s_t)$$
4. **REINFORCE 策略梯度公式**：
$$

\nabla_\theta J(\theta) = \mathbb{E}_{\tau} \left[ \sum_{t=0}^T 

\nabla_\theta \log \pi_\theta(a_t|s_t) G_t 
\right]$$
5. **因此**，环境状态转移概率 $P(s_{t+1}|s_t, a_t)$ 在求导中被完全消除，算法无需环境概率模型即可直接更新策略参数。

---

## 3. PolicyGradient 策略梯度与 Q-Learning 及 Actor-Critic 对比

| 维度 | PolicyGradient (REINFORCE) | Q-Learning (Value-based) | Actor-Critic 架构 |
|:---|:---|:---|:---|
| **控制范式** | **Policy-based (直接优化策略)** | Value-based (间接由 Q 推导) | **Policy + Value 混合融合** |
| **动作空间** | **连续 / 离散动作空间均可** | 仅限离散动作空间 ($\arg\max Q$) | 连续 / 离散动作空间均可 |
| **方差与偏差** | **高方差 (High Variance)、无偏差** | 低方差、有偏差 (bootstrapping) | **低方差、低偏差平衡** |
| **更新范式** | 回合制 Monte Carlo 离线更新 | 单步 TD(0) 在线更新 | 单步 TD(0) / n-step 在线更新 |

**局限（误区与反例）**：未加入 Baseline 的 REINFORCE 算法更新极为剧烈，容易陷入局部极小值；此外学习率设置过大可能导致策略坍塌 (Policy Collapse)。

关联知识点推荐：[[Actor-Critic架构]]、[[PPO近端策略优化]]、[[SAC软Actor-Critic]]、[[均方误差MSE与Huber损失]]。

---

## 4. Python 手写 Softmax 策略梯度 REINFORCE 更新自测断言

```python
import numpy as np

def softmax(logits: np.ndarray) -> np.ndarray:
    exps = np.exp(logits - np.max(logits))
    return exps / np.sum(exps)

def compute_policy_gradient(logits: np.ndarray, action: int, reward: float) -> np.ndarray:
    """
    对策略 \pi(a|s) = Softmax(logits) 计算 REINFORCE 梯度 dLog(\pi(a|s))/dLogits * G_t
    """
    probs = softmax(logits)
    # d log \pi(a|s) / d logits = e_a - probs
    grad_log_pi = -probs.copy()
    grad_log_pi[action] += 1.0
    return grad_log_pi * reward

if __name__ == "__main__":
    np.random.seed(42)
    logits = np.array([1.0, 2.0, 0.5])  # 3 个离散动作

    # 1. 尝试对动作 0 (目前概率低) 给予正向回报 +10.0
    grad = compute_policy_gradient(logits, action=0, reward=10.0)

    # 梯度更新 logits_new = logits + lr * grad
    logits_new = logits + 0.1 * grad

    # 自测验证 1: 更新后动作 0 的概率必须显著提升
    p_old = softmax(logits)[0]
    p_new = softmax(logits_new)[0]
    assert p_new > p_old, f"概率未能提升: {p_old:.4f} -> {p_new:.4f}"

    # 自测验证 2: 梯度之和必须严格为 0 (概率归一化约束)
    assert abs(np.sum(grad)) < 1e-5

    print(f"PolicyGradient 策略梯度更新成功: 动作0概率 {p_old*100:.2f}% -> {p_new*100:.2f}%")
    print("PolicyGradient 策略梯度算法 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Williams, R. J. (1992). Simple statistical gradient-following algorithms for connectionist reinforcement learning. *Machine Learning*, 8(3-4), 229-256. DOI: https://doi.org/10.1007/BF00992696 URL: https://link.springer.com/article/10.1007/BF00992696
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. Chapter 13 (Policy Gradient Methods). ISBN: 978-0262039246. URL: https://incompleteideas.net/book/the-book-2nd.html
- Sutton, R. S., McAllester, D., Singh, S., & Mansour, Y. (1999). Policy gradient methods for reinforcement learning with function approximation. *Advances in Neural Information Processing Systems (NIPS '99)*, 12, 1057-1063. URL: https://papers.nips.cc/paper/1713-policy-gradient-methods-for-reinforcement-learning-with-function-approximation
