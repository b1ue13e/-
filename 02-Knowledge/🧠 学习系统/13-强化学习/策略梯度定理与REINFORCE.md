---
title: "策略梯度定理与REINFORCE"
date: "2026-08-03"
type: concept
course: "强化学习"
importance: "A"
tags: [学习, 强化学习]
upstream: [PolicyGradient策略梯度, 探索与利用, MDP与贝尔曼方程]
downstream: [Actor-Critic架构, PPO近端策略优化]
status: learning
concept: ["策略梯度定理", "REINFORCE算法", "基线减方差"]
prerequisites: ["策略梯度", "探索与利用", "条件期望"]
related: ["Actor-Critic架构", "PPO近端策略优化", "Q-Learning算法"]
flow: project
kind: concept
template: Obsidian单知识点深度学习模板
created: 2026-08-03
---

# 策略梯度定理与REINFORCE

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：策略梯度是深度 RL 中"直接优化策略"这一大范式的**理论起点**（Sutton & Barto Ch.13），REINFORCE 是它最简单的实现；HW04（Spinning Up REINFORCE 练习）直接要求独立推导策略梯度定理并写最小实现，跳过它则 [[PPO近端策略优化]]、[[Actor-Critic架构]] 全部失去根基。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 值函数方法（[[Q-Learning算法]]、[[DQN深度Q网络]]）的决策依赖 $\arg\max_a Q(s,a)$：动作空间巨大或**连续**时这个 max 根本没法算；而且值函数方法学到的策略往往是确定性的，探索与利用的平衡要靠 $\varepsilon$-greedy 这种外部机制硬塞。
> 因此必须换个思路：**直接把策略参数化** $\pi_\theta(a \mid s)$，用梯度上升最大化期望回报 $J(\theta)$。但新麻烦来了——$J(\theta)$ 是"关于 $\theta$ 的分布的期望"，$\theta$ 藏在期望的积分里，$\nabla_\theta$ 不能直接搬进期望。**策略梯度定理**解决"梯度怎么算"，**REINFORCE** 解决"梯度怎么用蒙特卡洛采样估计"。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是策略优化族（REINFORCE → Actor-Critic → A2C/A3C → PPO/TRPO）的**共同推导源头**；[[PPO近端策略优化]] 的目标函数就是策略梯度 + 信赖域约束，[[Actor-Critic架构]] 只是把 $Q^\pi$ 的估计从 MC 换成 TD。
- **实际应用场景**：连续控制（机器人、Pendulum/CartPole）、无法求 $\arg\max$ 的高维/随机策略场景；几乎所有现代策略优化算法的损失函数里都藏着 $\nabla \log \pi_\theta$。
- **高频题型/任务**：推导策略梯度定理（score function 技巧）；手写 REINFORCE 更新式；解释 baseline 为什么不影响期望；HW04 的 Spinning Up 习题 1（推导 REINFORCE 的梯度估计）。

---

## 3. 学它之前需要哪些前置知识？

1. **[[PolicyGradient策略梯度]]**：策略参数化 $\pi_\theta(a \mid s)$ 与目标 $J(\theta)=\mathbb{E}_{\tau\sim\pi_\theta}[G_0]$ 的直觉——本节是该笔记的严格化与推导。
2. **[[探索与利用]]**：随机策略 $\pi_\theta$ 天然携带探索（概率本身就是探索），这是策略梯度方法相对值函数方法的优势来源。
3. **[[MDP与贝尔曼方程]]**：$Q^\pi(s,a)$ 与折扣回报 $G_t$ 的定义、马尔可夫性质——定理中"未来部分可替换为 $Q^\pi$"依赖因果性。

---

## 4. 用直觉语言解释它

> «"策略梯度定理说的是：想让期望总回报变大，就沿着'每条轨迹被采到的概率上升最快'的方向推，推多大力由这条轨迹的回报决定——回报高的轨迹多推，回报低的轨迹少推甚至反推。REINFORCE 则是'用一次实际采样的回报当打分'的粗糙版：考得好就照这个答题风格继续，考砸了就改。"»

- **直觉类比/几何图像**：$\nabla_\theta \log \pi_\theta(a \mid s)$ 是"动作 $a$ 的概率密度上升最快的方向"，乘以回报 $G$ 作带符号步长——"顺着高分轨迹的方向爬山"。
- **为什么很自然**：$\nabla \pi = \pi \cdot \nabla \log \pi$ 把"分布本身的变化"重写成"每个样本携带可求导的权重"，期望里只剩对 $\log \pi$ 求导，可在不知道环境模型的情况下采样估计。**一句话直觉本质**：**"按回报加权的对数概率上升"——把"对分布的梯度"偷换成"对 log 密度的梯度的期望"。**

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义
- **目标函数**：$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}\left[\sum_{t=0}^{T} \gamma^t r_t\right]$，其中轨迹 $\tau = (s_0, a_0, r_0, s_1, \dots)$。
- **策略梯度定理**（Sutton & Barto Ch.13）：$\nabla_\theta J(\theta) = \mathbb{E}_{s \sim d^\pi,\, a \sim \pi_\theta}\left[ \nabla_\theta \log \pi_\theta(a \mid s)\, Q^\pi(s, a) \right]$，$d^\pi$ 为 on-policy 状态分布。
- **score function 技巧**：$\nabla_\theta \pi_\theta(a\mid s) = \pi_\theta(a\mid s)\,\nabla_\theta \log \pi_\theta(a\mid s)$。

### 2. 核心公式
REINFORCE 更新（episodic，无 baseline）：
$$\theta \leftarrow \theta + \alpha\, \gamma^t\, G_t\, \nabla_\theta \log \pi_\theta(a_t \mid s_t)$$

带 baseline 的 REINFORCE（方差更小、期望不变）：
$$\theta \leftarrow \theta + \alpha\, \gamma^t\, \big(G_t - b(s_t)\big)\, \nabla_\theta \log \pi_\theta(a_t \mid s_t)$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\theta$ | 策略网络参数 | $\mathbb{R}^p$ | 可学习参数 |
| $\pi_\theta(a\mid s)$ | 随机策略 | 概率分布 | 如 softmax / 高斯 |
| $\tau$ | 一条轨迹 | 状态-动作-奖励序列 | 采样单位 |
| $G_t$ | 从 $t$ 起的折扣回报 | 实数 | 蒙特卡洛估计量 |
| $Q^\pi(s,a)$ | 动作价值 | 实数 | 定理中的"打分" |
| $b(s)$ | 基线函数 | 实数（只依赖 $s$） | 常见取 $V^\pi(s)$ 或其估计 |
| $d^\pi(s)$ | on-policy 状态分布 | 概率分布 | 含折扣权重的稳态分布 |
| $\alpha$ | 学习率 | 正实数 | 步长 |

### 4. 常见变体与适用条件
- **变体**：REINFORCE with baseline（最常用）；leave-one-out / 奖励归一化；与 critic 结合即 [[Actor-Critic架构]]（$Q^\pi$ 用函数近似代替 MC 回报）。**适用条件**：策略可微（softmax、高斯等）；**限制条件**：纯 REINFORCE 方差大、样本效率低；on-policy 无法用 [[经验回放与目标网络]] 复用旧数据。

---

## 6. 推导思路和思想来源

- **最初困难与直接方法局限**：$\nabla_\theta J(\theta)$ 的期望对 $\theta$ 双重依赖（轨迹分布 $\propto \prod_t \pi_\theta$ 与回报都含 $\theta$），直接 $\nabla \mathbb{E}[f] = \mathbb{E}[\nabla f]$ 是错的；对 $p_\theta(\tau)$ 积分求导又需要环境转移 $P$——而 RL 假设无模型。
- **关键"转念"**：**score function（对数导数）技巧**——$\nabla p_\theta(\tau) = p_\theta(\tau) \nabla \log p_\theta(\tau)$，把"对分布的梯度"变成"样本自身的可测权重"，期望里只剩 $\log$ 项，天然可采样估计。
- **推导主线与动机**：$J(\theta)=\int p_\theta(\tau)R(\tau)d\tau$ → $\nabla J = \int p_\theta \nabla\log p_\theta \, R = \mathbb{E}[\nabla\log p_\theta(\tau) R(\tau)]$ → 展开 $\log p_\theta(\tau)=\log p(s_0)+\sum_t \big[\log \pi_\theta(a_t|s_t)+\log P(s_{t+1}|s_t,a_t)\big]$，环境项与 $\theta$ 无关被消掉 → $\nabla J = \mathbb{E}\big[\sum_t \nabla\log\pi_\theta(a_t|s_t)\, R(\tau)\big]$ → **因果性**：$t$ 时刻决策只影响 $t$ 及以后回报，$R(\tau)$ 换为 $G_t$ 再换为 $Q^\pi(s_t,a_t)$ 即得定理。
- **baseline 为什么成立**：$\mathbb{E}[\nabla\log\pi\, b(s)] = b(s)\sum_a \nabla\pi_\theta(a|s) = b(s)\nabla 1 = 0$，所以减 $b(s)$ **不改变期望、只压低方差**；最优 baseline 正比于 $G_t$ 的方差加权形式（Schulman 推导），实践中常用 $V^\pi(s)$ 估计。
- **为什么自然得到此结论**：对数导数把"概率空间上的梯度"翻译成"样本空间上的权重"，这是 MC 估计的唯一可行入口——一切策略梯度算法都长着同一副骨架。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）
- **题目**：单步 bandit：动作 $a\in\{a_1,a_2\}$，softmax 策略 $\pi_\theta(a_1)=\frac{e^{\theta_1}}{e^{\theta_1}+e^{\theta_2}}$，回报 $R(a_1)=3,\ R(a_2)=1$，$\theta=(0,0)$。求 $\nabla J(\theta)$。
- **解题思路与关键步骤**：$\pi(a_1)=\pi(a_2)=0.5$；$\nabla_{\theta_1}\log\pi(a_1)=1-\pi(a_1)=0.5$，$\nabla_{\theta_1}\log\pi(a_2)=-\pi(a_1)=-0.5$；故 $\nabla_{\theta_1}J = 0.5\times 0.5\times 3 + (-0.5)\times 0.5\times 1 = 0.5 > 0$，同理 $\nabla_{\theta_2}J = -0.5$。**最终答案**：$\nabla J = (0.5, -0.5)$。**易错点**：$\nabla_{\theta_i}\log\pi(a_j)$ 对 $i\ne j$ 不是 0（softmax 交叉耦合），漏掉会算错方向。
- **🤔 追问**：若换成确定性策略 $a_1$ 恒被选？——$\nabla\log\pi$ 处处为 0（或未定义），梯度消失，这正是策略必须保持随机的原因。

### 例子 2：中等例子（条件判断与多步推理）
- **题目与完整解答**：轨迹 $(s_0,a_0,r_0=1),(s_1,a_1,r_1=2)$，$\gamma=1$，$\log\pi$ 的梯度分别为 $g_0=(-0.5,0.5),\ g_1=(0.3,-0.3)$。REINFORCE 无 baseline：$g_0 G_0 + g_1 G_1 = 3(-0.5,0.5)+2(0.3,-0.3)=(-0.9,0.9)$；用 baseline $b=V=2$：$(3-2)g_0+(2-2)g_1=(-0.5,0.5)$——**方向反转**！baseline 不是"微调"，而是重定"什么算好轨迹"。**易错点**：$G_t$ 从 $r_t$ 开始折扣，不含过去奖励。

### 例子 3：实际应用例子（真实场景/代码）
- **实际价值与转化**：HW04 用 PyTorch 实现 REINFORCE 跑 Pendulum/CartPole：策略为高斯分布 $\mathcal{N}(\mu_\theta(s), \sigma^2)$，损失取 `-log_prob * G` 做梯度下降（负号把梯度上升变下降）。对应 [[项目-CartPolePG]]、[[项目-PendulumPG]]、[[项目-PGBaseline]]。
```python
for step in range(ep_len):                      # 采集一条轨迹（策略为高斯分布）
    dist = policy(torch.tensor(s)); a = dist.sample()
    log_probs.append(dist.log_prob(a)); s, r, done, _ = env.step(a.numpy())
    rewards.append(r)
G = 0.0; loss = 0.0
for t in reversed(range(ep_len)):               # 倒推折扣回报
    G = gamma * G + rewards[t]
    loss = loss - log_probs[t] * G              # 梯度上升 = -loss 下降
loss.backward(); optimizer.step()               # 等价于 theta += alpha*G*grad log pi
```
- **实际价值**：一行 `loss = -log_prob * G` 就是 REINFORCE 的全部灵魂；HW04 报告的"回报方差"正是 baseline 消融实验的观测对象。

---

## 8. 常见误区和易混概念

### 误区 1：把 $\nabla \log \pi_\theta(a|s)$ 当成"动作的更新量"
- **错误直觉与为什么错**：以为梯度会"把动作 $a$ 往某方向推"（如 $a + \alpha\nabla\log\pi$）；实际上 $\nabla \log \pi$ 是**概率密度对参数的梯度**，作用是"让 $a$ 被选中的概率上升"，动作是采样的、不是梯度更新的。
- **正确理解**：参数更新 $\theta \leftarrow \theta + \alpha G\nabla\log\pi$ 改变的是策略分布的形状。

### 误区 2：以为 baseline 会改变梯度期望（或必须取最优值）
- **错误直觉与为什么错**：$G_t - b(s)$ 把回报"缩小"了，更新会偏；但 $\mathbb{E}[\nabla\log\pi \cdot b(s)]=0$（第 6 节），期望严格不变，bias 只影响方差。
- **正确理解**：任何只依赖 $s$（不依赖 $a$）的函数都能当 baseline；$V^\pi(s)$ 方便且接近最优。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| 策略梯度定理 | 目标对 $\theta$ 的梯度怎么算 | 期望内只对 $\log\pi$ 求导，打分用 $Q^\pi$ | 一切策略优化算法 |
| REINFORCE | 梯度怎么估计 | MC 采样 $G_t$ 替 $Q^\pi$，无偏高方差 | 入门/小规模任务 |
| Actor-Critic | 如何降方差 | 用 TD 估计 $Q^\pi$ 或优势，有偏低方差 | 大规模/连续控制 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[PolicyGradient策略梯度]]：直觉版策略梯度（本笔记是其严格推导与定理表述）。
- [[探索与利用]]：随机策略自带探索，解释"为什么必须保持 $\pi_\theta$ 随机"。

### 下游延伸
- [[Actor-Critic架构]]：把 $Q^\pi$ 的 MC 估计换成 critic 网络（TD），REINFORCE → Actor-Critic 的方差优化路线。
- [[PPO近端策略优化]]：在策略梯度目标上加 clip 信赖域约束，是 REINFORCE 的工程化继承者（HW05）。

### 横向关联
- [[Q-Learning算法]] ↔ 本知识点：值函数法（隐式策略，$\arg\max$）vs 策略法（显式 $\pi_\theta$）；一个是 off-policy 一个是 on-policy。
- [[价值迭代与策略迭代]] ↔ 本知识点：DP 路线靠贝尔曼最优方程"先求值再取 $\max$"间接得到策略，策略梯度路线直接对 $J(\theta)$ 做梯度上升——两种求解最优策略路线的对照。

### 应用场景
- [[项目-CartPolePG]]、[[项目-PendulumPG]]：REINFORCE 最小实现与训练曲线；[[项目-PGBaseline]]：baseline 减方差消融实验（HW04 验收项）。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚策略梯度定理解决什么问题。
- [ ] 2. 用直觉语言解释"按回报加权的对数概率上升"。
- [ ] 3. 写出策略梯度定理的完整表达式。
- [ ] 4. 写出 REINFORCE 更新式（含与不含 baseline 两种）。
- [ ] 5. 解释 $\nabla \log \pi$、$G_t$、$b(s)$、$d^\pi$ 各是什么。
- [ ] 6. 讲出推导主线：对数导数 → 展开轨迹概率 → 因果性替换 $Q^\pi$。
- [ ] 7. 手算单步 bandit 的 $\nabla J$。
- [ ] 8. 说出两个误区（梯度方向误解、baseline 期望误解）。
- [ ] 9. 说出它与 Actor-Critic、PPO、Q-Learning 的关系。
- [ ] 10. 说出一个真实应用场景（连续控制/HW04），并证明 $\mathbb{E}[\nabla\log\pi]=0$。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | score function 技巧的作用 |
| 2 | 公式运用 | 基础 | softmax 策略的 $\nabla\log\pi$ 计算 |
| 3 | 条件判断 | 中等 | 策略梯度 vs 值函数方法的选择 |
| 4 | 变式/综合 | 中等 | 因果性：$R(\tau)$ 为何可换 $G_t$ |
| 5 | 开放/证明/建模 | 较难 | 证明 baseline 不变期望、只减方差 |

### 题目与解析

#### 1. 什么是 score function（对数导数）技巧？没有它策略梯度定理无法推导？
> [!question]- 答案解析
> - **答案**：$\nabla_\theta \pi_\theta = \pi_\theta \nabla_\theta \log \pi_\theta$，把"对分布的梯度"改写为"分布 × 对 log 密度的梯度"，使 $\nabla J = \mathbb{E}[\nabla\log\pi \cdot Q]$ 可被采样估计。
> - **解析**：没有它，$\nabla_\theta \int p_\theta R$ 需要知道环境模型 $P$；有了它，梯度变成样本上的可测权重，RL 才能无模型地估计梯度。**易错原因**：忘记期望里 $p_\theta$ 与 $\theta$ 的耦合是问题根源。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 2. softmax 策略 $\pi(a_1)=0.7,\ \pi(a_2)=0.3$（参数 $\theta_1,\theta_2$），写出 $\nabla_{\theta_1}\log\pi(a_1)$ 与 $\nabla_{\theta_1}\log\pi(a_2)$。
> [!question]- 答案解析
> - **答案**：$\nabla_{\theta_1}\log\pi(a_1)=1-0.7=0.3$；$\nabla_{\theta_1}\log\pi(a_2)=-0.7$。
> - **解析**：softmax 交叉耦合 $\partial \log\pi_i/\partial\theta_j = \mathbf{1}[i=j]-\pi_j$：选中动作梯度是"1 减自身概率"，未选中是"负的自身概率"；易错点是误以为 $\theta_1$ 只影响 $\pi(a_1)$。

#### 3. 任务的动作空间是 21 维连续向量，你选值函数方法（DQN）还是策略梯度？为什么？
> [!question]- 答案解析
> - **答案**：策略梯度。连续空间里 $\arg\max_a Q(s,a)$ 无法枚举或不可微求解；策略梯度直接输出动作分布参数，天然适配连续动作。
> - **解析**：值函数法要求动作空间可求 max；策略法只要求策略可微、可采样。这也是 HW04/HW05 连续控制任务（Pendulum/LunarLander）选择策略梯度系的原因。

#### 4. 推导中为何能把整条轨迹回报 $R(\tau)$ 换成 $G_t$（进而换成 $Q^\pi(s_t,a_t)$）？
> [!question]- 答案解析
> - **答案**：因果性——$\nabla\log\pi_\theta(a_t|s_t)$ 只影响 $t$ 时刻及之后的回报；$R_{<t}$ 与 $a_t$ 独立，且 $\mathbb{E}[\nabla\log\pi \cdot R_{<t}]=0$（$\nabla\log\pi$ 条件期望为零），故 $R(\tau)$ 可替换为 $G_t=\sum_{k\ge t}\gamma^{k-t}R_k$，再按定义替换为 $Q^\pi$。这也是 Actor-Critic 用 TD 估计的伏笔。

#### 5. （推导题）证明：对任意只依赖状态 $s$ 的 $b(s)$，$\mathbb{E}_{a\sim\pi_\theta}\big[\nabla_\theta\log\pi_\theta(a|s)\,b(s)\big]=0$；并由此说明 REINFORCE with baseline 期望不变。
> [!question]- 答案解析
> - **答案**：$\mathbb{E}[\nabla\log\pi\, b]=b(s)\sum_a \pi_\theta(a|s)\nabla\log\pi_\theta(a|s) = b(s)\sum_a \nabla\pi_\theta(a|s) = b(s)\,\nabla_\theta\!\sum_a \pi_\theta(a|s) = b(s)\nabla_\theta 1 = 0$；故 $\mathbb{E}[(G_t-b)\nabla\log\pi]=\mathbb{E}[G_t\nabla\log\pi]$，期望不变。
> - **解析**：$b$ 越接近 $G_t$ 的条件均值 $V^\pi$，方差越小——"减方差"术语的数学来源，也是 HW04 消融实验的理论依据（对应误区 2）。

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

### 我的错误与卡点
-

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/13-强化学习/05-策略梯度/`（策略梯度阶段子目录）
- **关联已有笔记**：[[🧭 开源作业体系-强化学习]]、[[PolicyGradient策略梯度]]、[[Actor-Critic架构]]、[[PPO近端策略优化]]、[[探索与利用]]
- **建议标签**：`#学习` `#强化学习` `#策略梯度` `#REINFORCE` `#概念`
- **拆分建议**：暂不需要；若 HW04 推导卡壳，可拆"策略梯度定理证明题型笔记"（题型笔记）。
