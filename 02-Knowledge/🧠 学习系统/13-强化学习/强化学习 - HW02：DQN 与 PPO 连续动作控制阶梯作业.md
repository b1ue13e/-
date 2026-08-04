---
title: "强化学习-题型-DQN与PPO连续动作控制阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "强化学习作业"
course: "13-强化学习"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["强化学习", "DQN", "PPO算法"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|机器学习]]"]
related: ["[[机器学习-题型-李宏毅式分类与深层模型阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/13-强化学习/🗺️ 强化学习学习路径|强化学习学习路径]]"]
downstream: []
tags: [学习, 13-强化学习, 作业, 实战, 阶梯作业]
aliases: ["CS285-HW02-DQN与PPO作业"]
---

# 强化学习 - HW02：DQN 与 PPO 连续动作控制阶梯作业

> 🎯 **作业目标**：手写 Value/Policy Iteration、构建带 Replay Buffer 的 DQN，以及实现连续动作空间下的 PPO (Proximal Policy Optimization)。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-rl/hw02_dqn_ppo.ipynb`
- **开源标杆仓库**：[berkeleydeeprlcourse/homework_fall2023](https://github.com/berkeleydeeprlcourse/homework_fall2023) (UCB CS285)
- **核心依赖**：`gymnasium` / `gym`, `torch`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 Reward / 环境 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 收敛步数 < 50 | 在 Gym GridWorld 表格型环境中实现 Value Iteration 与 Policy Iteration。 |
| 🟡 **L2 - Medium Baseline** | Reward ≥ 200 (CartPole-v1) | **实现 Deep Q-Network (DQN)**：加入 Replay Buffer 与 Target Network，使用 $\epsilon$-greedy 探索。 |
| 🔴 **L3 - Strong Baseline** | Reward ≥ 250 (LunarLander-v2) | **手写 PPO 算法**：剪切概率比 (Clipped Surrogate Objective)、GAE (Generalized Advantage Estimation)。 |
| 👑 **L4 - Boss Baseline** | 采样效率提升 5x | 实现 Model-Based RL (MBPO / World Models)，在 3D BipedalWalker / HalfCheetah 上加速训练。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import torch

def test_ppo_clipped_loss():
    from rl_solvers import ppo_loss
    
    log_probs_old = torch.tensor([-0.5, -0.5])
    log_probs_new = torch.tensor([-0.4, -0.8])
    advantages = torch.tensor([1.0, -1.0])
    
    loss = ppo_loss(log_probs_new, log_probs_old, advantages, clip_eps=0.2)
    assert not torch.isnan(loss), "PPO Loss 不得计算为 NaN"
```

---

## 🃏 Anki 卡片

- Q: PPO 算法中为何对 Policy Ratio $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$ 施加 $\text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)$ 剪切限制？
- A: 剪切限制可以限制新旧策略之间的更新幅度，防止当优势函数 $A_t > 0$ 或 $A_t < 0$ 时新策略步长过大导致 Policy 崩溃，保证了策略优化的近端单调改进。
