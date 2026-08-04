---
title: "SAC 算法 (Soft Actor-Critic)"
date: 2026-07-27
type: concept
course: "强化学习 / 深度 RL"
importance: "A"
tags: [学习, 强化学习, 深度RL, SAC, SoftActorCritic, 最大熵强化学习, 连续控制, Off-Policy]
upstream: ["[[02-Knowledge/🧠 学习系统/07-最优化方法/05-专题应用/策略梯度|策略梯度]]", "[[13-强化学习/03-无模型学习/Actor-Critic|Actor-Critic]]"]
downstream: ["[[15-控制与机器人学/机器人控制|机器人连续控制]]"]
status: learning
---

# 🎯 SAC 算法 (Soft Actor-Critic)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：SAC（Soft Actor-Critic）由 Tuomas Haarnoja 等人于 2018 年提出，是**连续动作空间（Continuous Control）下最强、最稳定、采样效率最高的 Off-Policy 深度强化学习算法之一**。它通过引入**最大熵强化学习框架（Maximum Entropy RL）**，在优化传统累积奖励的同时最大化策略的动作熵（Entropy）。搞懂 SAC 的 Soft Q 迭代、重参数化策略求导以及自动温度系数调节，是掌握复杂机器人控制与真实物理系统 RL 的必备核心。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (we 遇到了什么麻烦)**：
> 传统的连续动作强化学习算法（如 DDPG、PPO）：
> - **DDPG (Off-Policy)**：虽然采样效率高，但对超参数极度敏感，训练过程极易崩溃，且策略极易过早坍缩到局部最优动作（陷入死胡同）；
> - **PPO (On-Policy)**：训练非常稳定，但因为是 On-Policy，需要海量的环境交互数据，在真实的机器人训练中（物理机器人磨损）代价高昂到不可接受。
> 我们迫切需要一种**既具备 Off-Policy 高采样效率、又具备极强抗噪稳定性，且能自发保持强探索能力（绝不过早早熟收敛）**的算法。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：SAC 将“最大熵”思想优雅注入 Actor-Critic 架构，证明了“做尽可能多的尝试（高熵）同时拿高分”能够大幅提升算法的鲁棒性。它是现代机器人学（Legged Locomotion, 机械臂抓取）与模拟器转真实世界（Sim-to-Real）的绝度主力算法。
- **实际应用场景**：四足机器人行走控制、双足人形机器人保持平衡、机械臂复杂装配、自动驾驶连续转向速度控制。
- **高频考点/任务**：最大熵 RL 目标函数 $\mathbb{E} [R + \alpha \mathcal{H}(\pi)]$、Soft Bellman 方程与 Soft Q 递推、策略网络重参数技巧 (Reparameterization Trick)、自动温度系数 $\alpha$ 的梯度更新公式、PyTorch 手写 SAC 关键模块。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[13-强化学习/03-无模型学习/Actor-Critic|Actor-Critic 架构]]**：Actor 网络 $\pi_{\phi}(a|s)$ 负责输出动作，Critic 网络 $Q_{\theta}(s, a)$ 负责评估动作价值。
2. **[[14-概率图模型/变分推断|香农熵 (Shannon Entropy)]]**：衡量概率分布不确定性的指标：$\mathcal{H}(\pi(\cdot|s)) = \mathbb{E}_{a \sim \pi} [-\ln \pi(a|s)]$。熵越大，动作越随机/不确定；熵为 0，动作变成确定性死板选择。

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：SAC 就像一个**既追求高薪又极其热爱尝试新事物的自由职业者**：
  - 传统 RL 就像死板的打工人：一旦发现做某份工作能赚 100 块（局部最优），就会一辈子死守这份工作，哪怕旁边有赚 1000 块的机会也绝不尝试；
  - SAC 职业者在决策时，目标不仅是“赚钱（累积奖励 $R$）”，还要求“保持生活的多样性与新鲜感（动作熵 $\mathcal{H}$）”！
  - 在薪水相近的几种选择里，他一定会选择**最不死板、最富有探索空间的方式**去完成。
  - 结果：他不仅赚到了高薪，还因为尝试过极其丰富的场景，当外界环境突发变化（如摔倒、滑倒）时，他能瞬间做出最鲁棒的应对！
- **为什么很自然**：高熵带来了天然的随机探索，防止策略退化为确定性冲动；同时也为后续的环境扰动留足了“退路”！
- **一句话直觉本质**：在目标函数中加入动作熵最大化，用 Soft Bellman 方程与双 Q 网络实现鲁棒的高效 Off-Policy 连续控制。

---

## 5. 正式定义、核心公式、符号解释

### 1. 最大熵强化学习目标函数
SAC 寻求最大化累积期望奖励与动作熵的加权和：
$$J(\pi) = \sum_{t=0}^T \mathbb{E}_{(s_t, a_t) \sim \rho_{\pi}} \left[ r(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot \mid s_t)) \right]$$
其中 $\alpha$ 为**温度系数 (Temperature Parameter)**，控制奖励与熵的相对权重。

### 2. Soft Q 值的 Bellman 递推目标
引入 Soft 状态价值 $V_{\psi}(s) = \mathbb{E}_{a \sim \pi} [Q_{\theta}(s, a) - \alpha \ln \pi(a \mid s)]$，Soft Q 的 TD 目标为：
$$y = r(s, a) + \gamma \mathbb{E}_{s' \sim p} \left[ V_{\bar{\psi}}(s') \right] = r(s, a) + \gamma \mathbb{E}_{s', a' \sim \pi} \left[ \min(Q_{\bar{\theta}_1}, Q_{\bar{\theta}_2})(s', a') - \alpha \ln \pi(a' \mid s') \right]$$

### 3. Actor (策略网络) 的重参数更新目标
使用高斯分布重参数技巧 $a_\phi(s, \epsilon) = \tanh(\mu_\phi(s) + \sigma_\phi(s) \odot \epsilon)$，通过最小化 KL 散度更新策略：
$$J_{\pi}(\phi) = \mathbb{E}_{s \sim \mathcal{D}, \epsilon \sim \mathcal{N}} \left[ \alpha \ln \pi_{\phi}(a_{\phi}(s, \epsilon) \mid s) - \min(Q_{\theta_1}, Q_{\theta_2})(s, a_{\phi}(s, \epsilon)) \right]$$

### 4. 自动温度系数 $\alpha$ 梯度更新目标
设期望的目标熵为 $\mathcal{H}_0$（通常设为 $- \dim(A)$）：
$$J(\alpha) = \mathbb{E}_{a \sim \pi} \left[ -\alpha \left( \ln \pi(a \mid s) + \mathcal{H}_0 \right) \right]$$

### 5. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\alpha$ | 温度系数 (Temperature) | $(0, +\infty)$ | 自动微调；大则强探索，小则重奖励 |
| $\mathcal{H}(\pi)$ | 策略在状态 $s$ 下的动作熵 | $[0, +\infty)$ | $\mathcal{H} = \mathbb{E}[-\ln \pi(a\mid s)]$ |
| $Q_{\theta_1}, Q_{\theta_2}$ | 双 Soft Q 评估网络 (Clipped Double-Q) | $\mathbb{R}$ | 采用最小值抑制 Q 值过高估计 |
| $\tanh$ | 动作空间截断函数 | $[-1, +1]^d$ | 将高斯输出有界化约束到物理动作范围 |

---

## 6. 推导思路和思想来源

- **最初困难**：在连续动作空间下（如关节力矩 $a \in [-1, 1]^6$），传统 Actor-Critic 很难在动作采样与确定性更新之间做出平衡。直接使用高斯分布 Policy 往往会导致方差过快收敛到 0，失去探索。
- **关键转念 1（加入 Soft 价值与熵）**：
  在 Bellman 方程中加上熵项 $-\alpha \ln \pi(a|s)$！
  这使得最优策略变成了**玻尔兹曼分布 (Boltzmann Distribution)**：
  $$\pi^*(a \mid s) \propto \exp\left( \frac{1}{\alpha} Q^*(s, a) \right)$$
  即：奖励高的动作概率指数级增大，但奖励相近的动作保持概率平摊，绝不一刀切！
- **关键转念 2（双 Q 消除过高估计 + 重参数求导）**：
  1. 引入类似 TD3 的双 Q 机制 $\min(Q_1, Q_2)$，彻底解决 Off-Policy 训练中 Q 值虚高的通病；
  2. 采用可微的 Tanh 高斯重参数技巧 $a = \tanh(\mu + \sigma \epsilon)$，使得 Policy 网络的梯度可以无缝跨越采样节点直接向后传播！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（Soft Q 目标值计算手算）
- **题目**：某状态 $s'$ 下，下一个动作 $a'$ 的概率 $\pi(a'|s') = 0.2$ ($\implies \ln \pi(a'|s') = -1.61$）。双 Q 网络预测分别为 $Q_1(s', a') = 10.0, Q_2(s', a') = 8.0$。温度系数 $\alpha = 0.5$，即时奖励 $r = 2.0$，折扣因子 $\gamma = 0.9$。求 TD 目标 $y$。
- **解答过程**：
  1. 选取双 Q 的最小值：$\min(Q_1, Q_2) = \min(10.0, 8.0) = 8.0$。
  2. 计算带熵修正的 Soft 价值：
     $$V(s') = \min(Q) - \alpha \ln \pi(a' \mid s') = 8.0 - 0.5 \times (-1.61) = 8.0 + 0.805 = 8.805$$
  3. 计算 TD 目标：
     $$y = r + \gamma V(s') = 2.0 + 0.9 \times 8.805 = 2.0 + 7.9245 = 9.9245$$
- **🤔 追问**：为什么 Soft 价值 $8.805$ 比单纯的 Q 值 $8.0$ 还要高？
  - *答*：因为该动作的概率分布具有不确定性（高熵），探索熵奖励额外贡献了 $+0.805$ 的价值！

### 例子 2：中等例子（Tanh 高斯分布的雅可比行列式修正）
当将高斯变量 $x \sim \mathcal{N}(\mu, \sigma^2)$ 通过 $a = \tanh(x)$ 映射到 $[-1, 1]$ 时，计算概率密度 $\ln \pi(a|s)$ 必须使用变量替换公式（加入雅可比行列式修正）：
$$\ln \pi(a \mid s) = \ln \pi_{gaussian}(x \mid s) - \sum_{i=1}^d \ln \left( 1 - \tanh^2(x_i) + \epsilon_{eps} \right)$$
这一步在 SAC 的代码实现中极其关键，缺少它会导致熵计算产生巨大偏差！

### 例子 3：实际应用（PyTorch 手写 SAC 高斯策略与 Actor/Critic 更新）

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal

class GaussianPolicy(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=256, action_scale=1.0):
        super().__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.mean_linear = nn.Linear(hidden_dim, action_dim)
        self.log_std_linear = nn.Linear(hidden_dim, action_dim)
        self.action_scale = action_scale

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        mean = self.mean_linear(x)
        log_std = self.log_std_linear(x)
        log_std = torch.clamp(log_std, min=-20, max=2) # 数值裁剪
        return mean, log_std

    def sample(self, state):
        mean, log_std = self.forward(state)
        std = log_std.exp()
        normal = Normal(mean, std)
        
        # 1. 重参数技巧采样 u ~ N(mean, std)
        x_t = normal.rsample() 
        y_t = torch.tanh(x_t)   # 映射到 [-1, 1]
        action = y_t * self.action_scale
        
        # 2. 计算 log_prob (带 Tanh 雅可比行列式修正)
        log_prob = normal.log_prob(x_t)
        # 修正项: log(1 - tanh^2(x))
        log_prob -= torch.log(self.action_scale * (1 - y_t.pow(2)) + 1e-6)
        log_prob = log_prob.sum(dim=-1, keepdim=True)
        
        return action, log_prob, torch.tanh(mean) * self.action_scale

# 验证代码
policy = GaussianPolicy(state_dim=10, action_dim=2)
state = torch.randn(4, 10) # Batch=4
action, log_prob, _ = policy.sample(state)
print("SAC 输出动作维度:", action.shape)    # [4, 2]
print("对应 log_prob 维度:", log_prob.shape) # [4, 1]
```

---

## 8. 常见误区和易混概念

### 误区 1：SAC 中的温度系数 $\alpha$ 是一个全程固定不变的超参数
- **错误直觉**：“$\alpha$ 就像学习率一样，在训练开始前手动设为 0.2 就行了。”
- **为什么错**：固定 $\alpha$ 极其危险！在训练初期需要大 $\alpha$ 强力探索；到了训练后期需要小 $\alpha$ 精细收敛。原始 SAC 论文需要手动调 $\alpha$，而 SAC v2（Haarnoja 2018b）引入了**自动温度系数调节算法**，让 $\alpha$ 随着当前策略的实际熵值自动梯度更新！
- **正确理解**：SAC v2 中 $\alpha$ 是一个可导参数，能自动维系目标熵 $\mathcal{H}_0$。

### 概念对比表

| 算法 | On/Off-Policy | 动作空间类型 | 探索控制机制 | 稳定性 & 采样效率 |
| :--- | :--- | :--- | :--- | :--- |
| **PPO** | **On-Policy** | 离散 & 连续 | 策略熵正则项 + 剪支 Clip | 极稳定，但采样效率偏低 |
| **DDPG** | **Off-Policy** | 纯连续 | 外部加高斯/OU动作噪声 | 采样效率高，但极易崩溃 |
| **SAC** | **Off-Policy** | **纯连续 (也可扩展离散)** | **内置最大熵框架 + 自动 $\alpha$** | **高采样效率 + 顶级稳定性** |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[13-强化学习/03-无模型学习/Actor-Critic|Actor-Critic]]：SAC 算法的基础网络架构原型。
- [[14-概率图模型/变分推断|变分推断]]：香农熵与 KL 散度目标的数学基石。

### 下游延伸
- [[15-控制与机器人学/机器人控制|机器人连续控制]]：SAC 在四足机器人与机械臂中的实际部署。

### 横向关联
- [[13-强化学习/03-无模型学习/TD3|TD3]] ↔ [[13-强化学习/SAC 算法|SAC]]：两大连续动作 Off-Policy 巅峰，TD3 采用确定性策略加噪声，SAC 采用最大熵高斯概率策略。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚 SAC 算法解决什么问题（连续动作下高采样效率与高稳定性的最大熵 Off-Policy 控制）。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像追求高薪同时热爱探索新事物的自由职业者……”»）。
- [ ] 3. 写出最大熵强化学习的目标函数公式。
- [ ] 4. 写出带熵修正的 Soft Q 值 TD 目标公式。
- [ ] 5. 说明为什么使用双 Q 网络 $\min(Q_1, Q_2)$。
- [ ] 6. 解释 Tanh 高斯重参数技巧对于 Actor 网络优化的必要性。
- [ ] 7. 手算包含熵修正的 Soft Q 目标值。
- [ ] 8. 对比 PPO、DDPG 与 SAC 的优缺点与使用场景。
- [ ] 9. 手写包含 Tanh 雅可比修正的 PyTorch 高斯策略采样代码。
- [ ] 10. 简述 SAC 在真实物理机器人训练中的优势。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | SAC 的 Policy 属于确定性还是概率性 |
| 2 | 公式计算 | 基础 | Soft TD 目标代入计算 |
| 3 | 条件判断 | 中等 | 温度系数 $\alpha \to 0$ 时 SAC 的退化现象 |
| 4 | 变式/综合 | 中等 | 自动温度系数 $\alpha$ 的更新逻辑 |
| 5 | 开放/推导 | 较难 | 推导 Tanh 变换后的概率密度修正公式 |

### 题目与解析

#### 1. 关于 SAC (Soft Actor-Critic) 算法，下列说法错误的是？
- A. SAC 是一种 Off-Policy 算法，可以使用 Replay Buffer 经验池
- B. SAC 算法仅支持一维离散动作空间，无法用于连续控制
- C. SAC 在损失函数中显式加入了动作的香农熵
- D. SAC 使用了双 Q 网络来缓解过高估计问题

> [!question]- 答案解析
> - **答案**：B
> - **解析**：SAC 专门为连续动作空间（Continuous Action Spaces）设计，是连续控制领域最强大的算法之一（后续也推出了离散扩展版）。
> - **对应误区**：误区 1。

#### 2. 当 SAC 的温度系数 $\alpha \to 0$ 时，SAC 算法会退化为哪个经典算法？
> [!question]- 答案解析
> - **答案**：退化为类似于 DDPG / TD3 的标准确定性 Actor-Critic 算法。
> - **解析**：当 $\alpha = 0$ 时，熵奖励项 $\alpha \mathcal{H}$ 归零，Soft Bellman 方程退化为传统的普通 Bellman 方程，最大熵探索机制失效。

#### 3. 为什么在 SAC 中，目标熵 $\mathcal{H}_0$ 通常被启发式地设定为 $- \dim(\mathcal{A})$（即动作维度的负数）？
> [!question]- 答案解析
> - **答案**：代表在每个动作维度上期望保持适度的各向同性不确定性。
> - **解析**：对于被 $\tanh$ 截断到 $[-1, 1]$ 的一维独立高斯分布，其标准高斯熵约为 1 左右。设定目标熵为 $-\text{action\_dim}$ 可以为不同维度的机器人关节提供与维度成正比的合理探索自由度。

#### 4. 在 SAC 的自动温度系数更新公式 $J(\alpha) = \mathbb{E} [ -\alpha (\ln \pi(a|s) + \mathcal{H}_0) ]$ 中，当当前策略的熵高于目标熵（即 $-\ln \pi(a|s) > \mathcal{H}_0$）时，$\alpha$ 会如何变化？
> [!question]- 答案解析
> - **答案**：$\alpha$ 的梯度为负，$\alpha$ 会自动减小。
> - **解析**：当当前熵过高（说明策略已经足够随机）时，算法自动降低温度 $\alpha$，把更多注意力转向最大化奖励 $R$；反之，当熵过低（策略陷入死板）时，$\alpha$ 会自动增大，强迫策略增加探索。

#### 5. 【证明/推导】已知 $y = \tanh(x)$，证明其导数关系统满足 $1 - y^2$，并简述为何变量替换需要加上 $\ln(1 - y^2)$ 项。
> [!question]- 答案解析
> - **证明**：
>   由 $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$，求导得：
>   $$\frac{d}{dx} \tanh(x) = 1 - \tanh^2(x) = 1 - y^2$$
>   根据概率密度变量变换定理：$p_Y(y) = p_X(x) \cdot \left| \frac{dx}{dy} \right| = p_X(x) \cdot \frac{1}{1 - y^2}$。
>   取对数即得：$\ln p_Y(y) = \ln p_X(x) - \ln(1 - y^2)$。
>   这保证了概率密度在经过非线性 Tanh 压缩后积分依然严格归一化为 1！

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

- **归档目录**：`02-Knowledge/🧠 学习系统/13-强化学习/`
- **建议双链**：
