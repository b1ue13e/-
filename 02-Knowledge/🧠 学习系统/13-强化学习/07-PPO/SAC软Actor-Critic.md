---
type: study
topic: "SAC 软 Actor-Critic"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["SAC", "软 Actor-Critic", "最大熵 RL", "离线策略"]
upstream: ["[[Actor-Critic架构]]", "[[策略与策略空间]]"]
tags: [学习, 强化学习]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

# SAC 软 Actor-Critic (Soft Actor-Critic)

## 1. SAC 软 Actor-Critic 的定义与最大熵框架

**SAC 软 Actor-Critic (Soft Actor-Critic)** 的核心定义是：一种基于**最大熵强化学习 (Maximum Entropy RL)** 框架的离散与连续动作空间**异策略 (Off-Policy)** Actor-Critic 算法。SAC 软 Actor-Critic 由 Tuomas Haarnoja 等人于 2018 年在 UC Berkeley 提出。

**基本性质**：传统 RL 仅最大化期望累积奖励 $\sum r_t$；而 SAC 软 Actor-Critic 在目标函数中额外加入了策略动作分布的**香农熵 $\mathcal{H}(\pi(\cdot|s_t))$**。这使得 SAC 软 Actor-Critic 鼓励策略在探索高奖励动作的同时保持尽可能的随机性（策略多样性），从而极大增强了算法对局部最优解的免疫力与鲁棒性。

---

## 2. 软贝尔曼最优方程与软 Q / 策略更新形式化推导

**最大熵目标函数**：
$$J(\pi) = \sum_{t=0}^T \mathbb{E}_{(s_t, a_t) \sim 
\rho_\pi} \left[ r(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot|s_t)) 
\right]$$

其中 $\alpha > 0$ 为**熵温度系数 (Temperature Parameter)**，控制奖励与探索熵之间的相对比重。

**推导过程（软 Q 值与策略重参数化）**：
1. **软贝尔曼方程 (Soft Bellman Equation)**：
$$Q^{\text{soft}}(s, a) = r(s, a) + \gamma \mathbb{E}_{s' \sim P} \left[ V^{\text{soft}}(s') 
\right]$$
$$V^{\text{soft}}(s) = \mathbb{E}_{a \sim \pi} \left[ Q^{\text{soft}}(s, a) - \alpha \ln \pi(a|s) 
\right]$$
2. **Double Q 技巧（Clipped Double-Q）**：维护两个独立的 Q 网络 $Q_{\theta_1}, Q_{\theta_2}$，取最小值防止高估：
$$y_t^{\text{SAC}} = r_t + \gamma (1 - \text{done}) \left( \min_{i=1,2} Q_{\bar{\theta}_i}(s_{t+1}, a_{t+1}) - \alpha \ln \pi_\phi(a_{t+1}|s_{t+1}) 
\right)$$
3. **策略网络更新 (Reparameterization Trick)**：设 $a = f_\phi(\epsilon; s), \epsilon \sim \mathcal{N}(0, I)$：
$$J_\pi(\phi) = \mathbb{E}_{s \sim \mathcal{D}, \epsilon \sim \mathcal{N}} \left[ \alpha \ln \pi_\phi(f_\phi(\epsilon; s)|s) - \min_{i=1,2} Q_{\theta_i}(s, f_\phi(\epsilon; s)) 
\right]$$
4. **温度系数 $\alpha$ 自动调节**：自动约束策略熵不低于目标熵 $\bar{\mathcal{H}}$：
$$J(\alpha) = \mathbb{E}_{a \sim \pi} \left[ -\alpha \ln \pi(a|s) - \alpha \bar{\mathcal{H}} 
\right]$$

---

## 3. SAC 软 Actor-Critic 与 PPO / DDPG 的区别与对比

| 维度 | SAC (Soft Actor-Critic) | DDPG (深度确定性策略梯度) | PPO (近端策略优化) |
|:---|:---|:---|:---|
| **策略属性** | **Off-Policy (异策略)** | Off-Policy (异策略) | **On-Policy (同策略)** |
| **动作分布** | **高斯随机策略 + 最大熵** | 确定性策略 $a = \mu(s) + \text{Noise}$ | 高斯随机策略 |
| **样本效率** | **极高** (经验回放重复利用) | 较高 | 较低 |
| **探索机制** | **内在熵最大化自动探索** | 外在叠加加性噪声 (OU噪声) | 策略本身高斯方差 |
| **超参数敏感度**| 低 ($\alpha$ 自动调节，极强鲁棒) | 极高 (易陷入发散/死锁) | 较低 (PPO-Clip 保护) |

**局限（误区）**：SAC 软 Actor-Critic 需要同时维护 2 个 Q 网络、2 个 Target Q 网络、1 个 Policy 网络以及 1 个 Alpha 温度参数，内存与算力开销相对更大。

关联知识点推荐：[[PPO近端策略优化]]、[[DQN深度Q网络]]、[[Q-Learning算法]]、[[梯度下降与优化器|梯度下降与Adam优化器]]。

---

## 4. Python SAC 软 TD Target 与自动温度 $\alpha$ 更新自测断言

```python
import numpy as np

def compute_sac_td_target(r: float, done: bool, q1_next: float, q2_next: float,
                         log_prob_next: float, alpha: float, gamma: float = 0.99) -> float:
    """
    SAC 软 TD Target 计算
    y = r + gamma * (1 - done) * (min(Q1, Q2) - alpha * log_prob)
    """
    if done:
        return float(r)
    min_q_next = min(q1_next, q2_next)
    soft_v_next = min_q_next - alpha * log_prob_next
    return float(r + gamma * soft_v_next)

if __name__ == "__main__":
    r = 1.0
    q1_next, q2_next = 10.0, 12.0
    log_prob_next = -1.5
    alpha = 0.2
    gamma = 0.9

    target = compute_sac_td_target(r, False, q1_next, q2_next, log_prob_next, alpha, gamma)
    assert abs(target - 10.27) < 1e-5

    target_high_entropy = compute_sac_td_target(r, False, q1_next, q2_next, -5.0, alpha, gamma)
    assert target_high_entropy > target

    assert compute_sac_td_target(5.0, True, 100.0, 100.0, -2.0, 0.2) == 5.0

    print(f"SAC 软 Actor-Critic 软 TD Target 验证成功: 标准 Target = {target:.2f}")
    print("SAC 软 Actor-Critic 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Haarnoja, T., Zhou, A., Abbeel, P., & Levine, S. (2018). Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. *International Conference on Machine Learning (ICML '18)*, 1861-1870. DOI: https://doi.org/10.48550/arXiv.1801.01290
- Haarnoja, T., et al. (2018). Soft actor-critic algorithms and applications. *arXiv preprint arXiv:1812.05905*. URL: https://arxiv.org/abs/1812.05905
- Fujimoto, S., Hoof, H., & Meger, D. (2018). Addressing function approximation error in actor-critic methods (TD3). *International Conference on Machine Learning (ICML '18)*, 1587-1596. URL: https://arxiv.org/abs/1802.09477
- Christodoulou, P. (2019). Soft actor-critic for discrete action settings. *arXiv preprint arXiv:1910.07207*. URL: https://arxiv.org/abs/1910.07207

## 闭卷自测
1. SAC 的最大熵目标是什么？
2. SAC 为何天然适合连续控制？
3. SAC 与标准 AC 的核心区别？

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
