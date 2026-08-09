---
title: "DQN 的改进与变体"
type: study
topic: "DQN 的改进与变体"
course: "强化学习"
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
upstream: ["[[DQN深度Q网络]]", "[[经验回放与目标网络]]", "[[探索与利用]]"]
tags: [强化学习, DQN, Double-DQN, Dueling, C51, Rainbow, 分布RL]
concept: ["Double DQN", "Dueling DQN", "C51", "Noisy Nets", "Rainbow", "优先经验回放"]
---

# DQN 的改进与变体

> 原版 DQN（经验回放 + 目标网络 + 函数逼近）在高维离散动作上取得突破，但仍有三大病灶：最大化高估、结构浪费、探索与状态无关。下面的改进各解决一面，Rainbow 把它们整合。

## 1. Double DQN（去最大化偏差）

标准 DQN 的 max 在"选动作"和"评价值"上都用同一（目标）网络，放大最大化偏差、过估计 Q。Double DQN 把"选择"与"评估"解耦：

- 用在线网络 θ 选最优动作：$a^*=\arg\max_{a'}Q_\theta(s',a')$
- 用目标网络 θ^- 评估：$y=r+\gamma Q_{\theta^-}(s',a^*)$

即"在线网选、目标网评"，消除同一网络既选又评带来的正向偏差。例：若 $Q_\text{online}(s',\cdot)=[0.9,0.4]$ 选中 a1，$Q_\text{target}(s',a1)=0.8$ ⇒ $y=r+\gamma\cdot0.8$（动作选择与价值估计解耦，抑制 Q 过高估计）。Double DQN 几乎同成本，显著降低过估计、提升稳定性。常见错误：以为 DDQN 用"两个独立随机初始化网络"——实际上仍共享训练，只是选/评分离。

## 2. Dueling DQN（拆分状态价值与优势）

很多状态下"选哪个动作"差别不大，价值主要来自"状态本身好坏"。Dueling DQN 把 Q 拆成状态价值 V 与优势 A 分别估计：

$$Q(s,a;\theta,\alpha,\beta)=V(s;\theta,\beta)+\big(A(s,a;\theta,\alpha)-\mathrm{mean}_{a'}A(s,a';\theta,\alpha)\big)$$

V 估"状态多好"，A 估"相对平均动作好多少"；减均值是为可辨识性（否则 V、A 各自不唯一）。在多数动作等价的状态，Dueling 只需 V 网络学好状态价值，A 近似 0；标准 DQN 却要在各动作上分别拟合，浪费容量。Dueling 改的是"网络结构"（输出头），不基于新损失；可与 DDQN/PER 叠加。常见错误：忘记减 A 的均值——不减去则 V、A 存在平移歧义，训练不稳。

## 3. C51（分布式 RL 先驱）

标准 DQN 学"期望回报" Q（一个标量）。C51 改为学"回报的价值分布" $Z(s,a)$，用分布信息做更丰富、更稳的决策。建模分布 $Z(s,a)$ 为在固定支撑 $\{z_0..z_{N-1}\}$ 上的类别分布（N=51 故称 C51）：

$$Z(s,a)=\sum_i p_i(s,a)\,z_i$$

Bellman 更新作用在分布上（投影到支撑）；动作选择取"分布期望最大"或按风险偏好不同（如选中位数）。某状态两个动作期望相同，但一个回报方差大（风险高）。C51 能看到分布差异，按风险偏好择优；标准 DQN 只看期望会忽略风险。C51 是 QR-DQN/IQN 等分布 RL 的先驱。常见错误：把 C51 当成"学多个 Q 值取平均"——它学的是单个回报分布的类别概率。

## 4. Noisy Nets（状态相关的探索）

ε-greedy 的探索与"当前状态"无关，且衰减后探索减弱。Noisy Nets 把探索"装进网络参数"：每层加参数化噪声，状态相关的探索、训练末自动减弱。权重替换为 $W=\mu+\sigma\odot\varepsilon$，ε 每前向采样，μ、σ 是可学习参数；σ 被优化使网络学会"在哪里该有随机性"，推理时可关噪声取确定性。Noisy DQN 不再用 ε-greedy，仅靠参数噪声探索；训练后期 σ 自动趋小，探索自然衰减。与 ε-greedy 比：状态相关、自动衰减、可端到端学习。常见错误：部署时忘了关噪声——线上应用应取 μ（确定性）以保证稳定。

## 5. Rainbow（集成而非堆叠）

DQN 的多种改进各解决一面问题。Rainbow 把它们整合进一个算法，取得远超单点的性能。Rainbow = Double DQN + Dueling + PER + Noisy Nets + C51（+ 原版还含多步学习 n-step 与分布式）。各组件互补：DDQN 抑过估计、Dueling 提质效、PER 提数据效率、Noisy 提探索、C51 用分布信息。在 57 款 Atari 上中位数超人类 100%+。消融实验显示各组件均贡献。Rainbow 不是简单堆叠，而是统一框架；但并非所有组合都正相互作用，需调参。常见错误：以为"堆越多越好"——组件间可能有耦合/开销，需依任务取舍。

## 6. DQN 的训练工程细节

- **跳帧（Frame Skip）**：视频游戏等高频环境中相邻帧高度相似。每 k 帧才选一次动作、期间重复该动作（k=4 常见），既减少决策频率又保留时序信息，大幅加速训练。跳帧过大导致动作不够细（如平台跳跃错过窗口）。Atari Breakout：每 4 帧决策一次，单幕从数万步降到数千步，训练提速数倍且性能几乎不变。
- **ε 衰减**：DQN 行为策略通常 ε-greedy。固定 ε 难兼顾"早期多探索、后期多利用"——故用衰减：$\epsilon_t=\max(\epsilon_{\min},\epsilon_0\cdot d^t)$（指数）或线性降到 ε_min。前期 ε 大（多随机探索），后期 ε 小（多贪心利用）。衰减太快导致探索不足、错过好动作；太慢则训练慢。

## 7. 闭卷自测

1. Double DQN 如何缓解最大化偏差？"选"与"评"分别用哪个网络？
2. Dueling DQN 把 Q 拆成什么？为什么要减去优势均值？
3. C51 与 DQN 在学习目标上的根本区别？为何分布信息有助于决策？
4. Noisy Nets 如何实现探索？与 ε-greedy 比有何优势？
5. Rainbow 整合了哪些 DQN 改进？为什么说它是"集成"而非简单堆叠？
6. 跳帧解决什么问题？ε 衰减过快/过慢的代价？

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
