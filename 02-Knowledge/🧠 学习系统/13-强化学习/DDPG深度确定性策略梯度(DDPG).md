---
title: "DDPG深度确定性策略梯度(DDPG)"
date: "2026-08-03"
type: concept
course: "强化学习"
importance: "A"
tags: [学习, 强化学习, 深度强化学习, 连续控制]
upstream: [DQN深度Q网络, PolicyGradient策略梯度, Actor-Critic架构]
downstream: [SAC软Actor-Critic, TD3算法]
status: learning
---

# DDPG深度确定性策略梯度(DDPG)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：DDPG 是将 DQN 成功扩展到连续动作空间（Continuous Action Space）的里程碑算法。在自动驾驶、机器人控制（例如 Mujoco 环境）中，动作往往是连续的力矩或角度，DQN 无法处理，而 DDPG 完美解决了这个问题，是学习现代连续控制算法（如 TD3, SAC）的必经之路。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 在 DQN 中，我们需要对每一个离散动作计算 Q 值，然后使用 $\max_a Q(s, a)$ 选出最优动作。但是，如果动作是一个连续的值（比如方向盘转角 $-90^\circ \sim +90^\circ$），这个 $\max_a$ 操作就变成了一个在连续空间求极值的非凸优化问题，计算代价高得无法接受。我们需要一种算法，能够在连续动作空间高效地找到最优动作。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是 DQN 和确定性策略梯度（DPG）的结合体。它使用了 DQN 中的经验回放池（Replay Buffer）和目标网络（Target Network），同时采用了 Actor-Critic 架构。
- **实际应用场景**：所有需要输出连续控制信号的场景，如机械臂抓取、四足机器人行走、无人机姿态控制。
- **高频题型/任务**：在 OpenAI Spinning Up 或 Stable-Baselines3 中复现 DDPG 算法，解决 Pendulum 或 HalfCheetah 环境，并观察由于 Q 值高估导致的训练不稳定现象。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景（各 200 字以内）：

1. **[[DQN深度Q网络]]**：理解经验回放池（打破样本相关性）和目标网络（让训练目标稳定）的两大技巧。
2. **[[Actor-Critic架构]]**：理解一个网络（Actor）负责给出动作，另一个网络（Critic）负责打分（评价动作的好坏）。

---

## 4. 用直觉语言解释它

> «“这东西其实就像一个盲人运动员和一个严厉的教练在训练。”»

- **直觉类比/几何图像**：
  - **Actor（运动员）**：负责输出一个具体的动作（注意是**确定性**动作，不是概率分布）。
  - **Critic（教练）**：负责给这个动作打分。
  - **训练过程**：运动员做动作，教练打分，并告诉运动员：“如果你把动作往这边偏一点点，你的分数会更高（这就是 Q 值对动作的梯度）。” 运动员根据这个梯度来调整自己的动作输出。
- **一句话直觉本质**：使用 Critic 网络的梯度来指导确定性 Actor 网络更新，并利用 DQN 的技巧稳定训练过程。

---

## 5. 正式定义、核心公式、符号解释

### 1. 网络结构
DDPG 包含 4 个神经网络：
- $Q_\phi (s, a)$：Critic 网络，评估在状态 $s$ 下采取动作 $a$ 的价值。
- $\mu_\theta (s)$：Actor 网络，输出状态 $s$ 下的确切动作 $a$。
- $Q_{\phi_{targ}} (s, a)$：Critic 目标网络。
- $\mu_{\theta_{targ}} (s)$：Actor 目标网络。

### 2. Critic 更新 (类似 DQN)
损失函数为最小化均方误差 (MSE)：
$$ L(\phi) = \mathbb{E}_{(s,a,r,s',d) \sim \mathcal{D}} \left[ \left( Q_\phi(s,a) - y \right)^2 \right] $$
其中目标值 $y = r + \gamma (1-d) Q_{\phi_{targ}}(s', \mu_{\theta_{targ}}(s'))$

### 3. Actor 更新 (确定性策略梯度)
我们希望 Actor 输出的动作能让 Critic 评分最高：
$$ \max_\theta \mathbb{E}_{s \sim \mathcal{D}} \left[ Q_\phi(s, \mu_\theta(s)) \right] $$
利用链式法则，Actor 的策略梯度为：
$$ \nabla_\theta J(\theta) \approx \mathbb{E}_{s} \left[ \nabla_a Q_\phi(s, a)|_{a=\mu_\theta(s)} \nabla_\theta \mu_\theta(s) \right] $$

### 4. 软更新 (Soft Update)
为了稳定训练，目标网络不直接复制当前网络，而是像指数移动平均一样缓慢更新：
$$ \phi_{targ} \leftarrow \tau \phi + (1-\tau) \phi_{targ} $$
$$ \theta_{targ} \leftarrow \tau \theta + (1-\tau) \theta_{targ} $$
（$\tau$ 通常取很小的值，如 $0.005$）

---

## 6. 推导思路和思想来源

- **最初困难**：如果用普通的随机策略（Stochastic Policy, 比如输出高斯分布的均值和方差），动作空间越大，需要的采样数据就越多。而且对于有些问题，最优策略本身就是确定性的。
- **关键“转念”**：David Silver 提出的 DPG 定理证明了：即使策略是确定性的，策略梯度也是存在的，并且只依赖于 Q 函数对动作的导数。把这个理论和 DQN 强大的神经网络拟合能力结合，就诞生了 DDPG。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（DDPG 的探索机制）
- **题目**：既然 Actor 输出的是确定性动作（给定 $s$ 总是输出同一个 $a$），那它在环境中该如何**探索（Exploration）**？
- **解题思路与关键步骤**：
  在训练阶段收集经验时，我们手动在 Actor 输出的动作上加上**噪声**（Noise）。
  $$ a = \text{clip}(\mu_\theta(s) + \mathcal{N}, a_{min}, a_{max}) $$
  通常使用 Ornstein-Uhlenbeck (OU) 噪声（一种相关性噪声，适合物理控制）或者简单的高斯噪声。
- **结论**：测试时去掉噪声直接输出确定性动作，训练时加噪声鼓励探索。

---

## 8. 常见误区和易混概念

### 误区 1：DDPG 输出的是动作概率分布
- **关键区别**：普通的 Policy Gradient（如 PPO）输出的是一个分布（比如高斯分布的 $\mu$ 和 $\sigma$），然后在环境中 sample 出动作。DDPG 的 Actor 输出的就是**具体的动作值**（比如直接输出 2.5 rad/s 的转速），所以叫“确定性”。

### 误区 2：DDPG 很好训练
- **实际情况**：DDPG 出名地脆弱（brittle）且对超参数极度敏感。它存在严重的 **Q值高估** 问题，这直接导致了后续 TD3 算法（Twin Delayed DDPG）的诞生。

---

## 9. 相关知识点与 Obsidian 双链建议

- 下游延伸：[[TD3算法]]（解决 Q 值高估）、[[🎯 SAC 算法 (Soft Actor-Critic)]]（将最大熵引入连续控制，更加稳定）。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下问题：
- [ ] 1. 为什么 DQN 不能直接用于连续动作空间？DDPG 是如何解决的？
- [ ] 2. 默写 DDPG 中 Actor 的策略梯度公式（链式法则展开）。
- [ ] 3. 什么是目标网络的“软更新 (Soft Update)”？

---

## 11. 自测题：5 道 (待补充)

---

## 12. 我的主动回忆区
(留空给后续复习填写)

---

## 13. 给 Obsidian 的归档建议
- **适合文件夹**：`02-Knowledge/🧠 学习系统/13-强化学习/06-Actor-Critic`
- **建议标签**：`#学习` `#强化学习` `#DDPG` `#连续控制`
