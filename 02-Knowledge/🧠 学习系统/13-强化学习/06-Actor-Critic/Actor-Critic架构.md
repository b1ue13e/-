---
type: study
topic: "Actor-Critic 架构"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Actor-Critic 架构", "Actor-Critic", "优势函数", "TD误差"]
upstream: ["[[策略梯度]]", "[[V函数（状态价值函数）]]", "[[Q函数（动作价值函数）]]", "[[优势函数]]"]
tags: [学习, 强化学习]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

# Actor-Critic 架构 (Actor-Critic Architecture)

## 1. Actor-Critic 架构的定义与双网协作机制

**Actor-Critic 架构 (Actor-Critic Architecture)** 的核心定义是：一种结合基于策略 (Policy-based) 与基于价值 (Value-based) 方法的强化学习并行框架，通过 **Actor (演员/策略网)** 输出动作分布并执行探索，通过 **Critic (评论家/价值网)** 评估状态价值并引导 Actor 策略更新。由 Konda & Tsitsiklis 于 2000 年建立收敛性证明。

**基本性质与协作分工**：
1. **Actor (策略网络 $\pi_\theta(a|s)$)**：根据 Critic 提供的反馈梯度向量调整参数 $\theta$，实现连续或离散动作的最佳控制；
2. **Critic (价值网络 $V_\phi(s)$ 或 $Q_\phi(s, a)$)**：利用单步 TD(0) 误差计算状态价值，逼近真实期望回报；
3. **优势函数 (Advantage Function $A(s, a)$)**：引入 $A(s, a) = Q(s, a) - V(s)$ 作为 Actor 更新的 Baseline 权重，**大幅降低策略梯度的估计方差**。

---

## 2. TD 误差优势函数与梯度更新形式化推导

**策略梯度带基线 (Baseline) 假设**：
在策略梯度中引入与动作 $a$ 无关的基线 $b(s)$，有 $\mathbb{E}_{a \sim \pi} [



\nabla_\theta \log \pi_\theta(a|s) b(s)] = 0$。

**推导过程（优势函数与单步 TD 误差等价性）**：
1. 将基线设定为状态价值函数 $b(s) = V^\pi(s)$，定义**优势函数 (Advantage Function)**：
$$A^\pi(s_t, a_t) = Q^\pi(s_t, a_t) - V^\pi(s_t)$$
2. 采用单步 TD(0) 估计动作价值 $Q^\pi(s_t, a_t) \approx r_t + \gamma V_\phi(s_{t+1})$，代入优势函数：
$$A(s_t, a_t) \approx \delta_t = r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t)$$
其中 $\delta_t$ 称为**时序差分误差 (TD Error)**；
3. **Actor 策略网络梯度更新式**：
$$



\nabla_\theta J(\theta) = \mathbb{E} \left[ 



\nabla_\theta \log \pi_\theta(a_t|s_t) \delta_t 
\right]$$
4. **Critic 价值网络梯度更新式**：通过 MSE 损失最小化 TD 误差：
$$L(\phi) = \frac{1}{2} \left( r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t) 
\right)^2 \Rightarrow 



\nabla_\phi L(\phi) = -\delta_t 



\nabla_\phi V_\phi(s_t)$$
5. **因此**，用单步估算 $\delta_t$ 替换全轨迹累积回报 $G_t$，将策略更新从回合制 (Monte Carlo) 转化为单步在线 (TD Online) 学习。

---

## 3. Actor-Critic 架构与 REINFORCE 及 DQN 全方位对比

| 维度 | REINFORCE 策略梯度 | DQN (Deep Q-Network) | Actor-Critic 架构 |
|:---|:---|:---|:---|
| **网络组成** | 仅 Actor 策略网络 | 仅 Critic Q 网络 | **Actor 策略网络 + Critic 价值网络** |
| **更新时机** | 回合结束后 (Episode End) | 单步 TD(0) 经验回放 | **单步在线 (TD Online) / n-Step** |
| **方差与偏差** | **高方差 (High Variance)** | 高偏差 (Overestimation) | **低方差、低偏差良好平衡** |
| **代表算法演进** | 原始 REINFORCE | DQN / Double DQN / Dueling | **A2C / A3C / PPO / DDPG / SAC** |

**局限（误区与反例）**：若 Critic 网络的估计产生严重偏差 (Bootstrapping Bias)，Actor 策略网络将在错误的引导下收敛至非最优策略；对此现代算法（如 TD3 / SAC）引入双 Critic 机制 (Twin-Critic) 抑制过估计。

关联知识点推荐：[[PolicyGradient策略梯度]]、[[PPO近端策略优化]]、[[SAC软Actor-Critic]]、[[DQN深度Q网络]]。

---

## 4. Python 手写 Actor-Critic 单步 TD(0) 联合更新自测断言

```python
import numpy as np

def actor_critic_step(v_curr: float, v_next: float, reward: float, gamma: float = 0.99) -> tuple:
    """
    计算单步 Actor-Critic 的 TD 误差与更新项
    """
    # 1. 计算 TD 误差 \delta = r + \gamma * V(s') - V(s)
    td_error = reward + gamma * v_next - v_curr
    return float(td_error)

if __name__ == "__main__":
    v_curr = 2.0
    v_next = 3.0
    reward = 1.0
    gamma = 0.9

    # TD target = 1.0 + 0.9 * 3.0 = 3.7
    # td_error = 3.7 - 2.0 = 1.7
    td_err = actor_critic_step(v_curr, v_next, reward, gamma)

    # 自测验证 1: TD 误差计算精确断言
    assert abs(td_err - 1.7) < 1e-5, f"TD 误差不符: {td_err}"

    # 自测验证 2: 若奖励增加，优势/TD 误差必须单调增加
    td_err_high = actor_critic_step(v_curr, v_next, reward=5.0, gamma=gamma)
    assert td_err_high > td_err, "更高 Reward 应带来更高正向优势"

    print(f"Actor-Critic 架构 单步 TD 误差 = {td_err:.4f}")
    print("Actor-Critic 架构 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Konda, V. R., & Tsitsiklis, J. N. (2000). Actor-critic algorithms. *Advances in Neural Information Processing Systems (NIPS '00)*, 12, 1008-1014. URL: https://papers.nips.cc/paper/1786-actor-critic-algorithms
- Mnih, V., Badia, A. P., Mirza, M., Graves, A., Lillicrap, T., Harley, T., Silver, D., & Kavukcuoglu, K. (2016). Asynchronous methods for deep reinforcement learning (A3C/A2C). *International Conference on Machine Learning (ICML '16)*, 1928-1937. URL: https://proceedings.mlr.press/v48/mnih16.html
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. Chapter 13.5 (Actor-Critic Methods). ISBN: 978-0262039246. URL: https://incompleteideas.net/book/the-book-2nd.html

## 闭卷自测
1. Actor-Critic 中 Actor 与 Critic 各自负责什么？
2. 优势函数 A(s,a)=Q−V 在 AC 中起什么作用？
3. 为何 AC 能比 REINFORCE 显著降低策略梯度的方差？

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
