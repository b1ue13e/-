---

type: study

topic: "DQN (Deep Q-Network)"

course: "机器学习"

created: 2026-08-06

status: ongoing

stage_moc: "[[🧭 阶段5-其他方法]]"

flow: knowledge

kind: concept

upstream: ["[[机器学习-Q-Learning]]"]

source: "周志华《机器学习》第6–10、13–16章"
source_url: "https://book.douban.com/subject/26708119/"
accessed: 2026-08-07
license: "[待验证]"

---



# DQN (Deep Q-Network)



## 为什么学



表格型 [[机器学习-Q-Learning]] 用 `Q(s,a)` 查表，状态/动作空间一大或连续就存不下、泛化不了。**DQN 用神经网络近似 Q 函数**，把 Q-learning 扩展到高维感知输入（如图像像素），是深度强化学习走向实用的起点。



## 定义与公式



- 目标：学一个网络 `Q(s,a;θ)` 逼近最优动作价值 `Q*(s,a)`。

- 损失（TD 误差平方）：

  `L(θ) = E[( r + γ·max_{a'} Q_target(s',a';θ⁻) − Q(s,a;θ) )²]`

  其中 `Q_target` 是**目标网络**（参数 `θ⁻`，缓慢同步），`γ` 是折扣因子。

- 两条稳定训练的关键技巧：

  1. **经验回放（Replay Buffer）**：把 `(s,a,r,s')` 存入缓冲，训练时随机采样小批量，打破样本间的时间相关性。

  2. **目标网络（Target Network）**：用一份滞后更新的网络计算 `max_{a'} Q_target`，避免「自己追自己」导致发散。



## 最小例子



- 环境：离散动作迷宫。状态用 one-hot 或图像表示。

- 训练循环：ε-贪婪选动作 → 执行得 `(s,a,r,s')` → 入缓冲 → 采样批量 → 用目标网络算 TD 目标 → 梯度下降更新 `θ` → 每隔 `C` 步把 `θ` 拷贝给 `θ⁻`。



## 常见错误



- 不用目标网络，直接 `r + γ·max_a' Q(s',a';θ)` 当目标 → 训练震荡甚至不收敛。

- 回放池与在线策略分布不一致时仍用 on-policy 视角解释 → DQN 本质是 off-policy。

- 把 Q 网络输出当成概率 → 它输出的是**价值估计**，不是动作概率（那是策略梯度/A2C 的做法）。



## 前后连接



- 前置：[[机器学习-Q-Learning]]（TD 学习与 ε-贪婪）、[[机器学习-神经网络]]、[[机器学习-反向传播算法]]

- 进阶：Double DQN（缓解过估）、Dueling DQN、Prioritized Replay

- 返回：[[🧭 阶段1-基础概念]]







## 可执行示例（Python）



```python

import numpy as np



# 极小示意：在线网络 θ 与目标网络 θ⁻（用线性近似 Q(s,a)=s·θ）

rng = np.random.default_rng(0)

theta = rng.normal(0, 0.1, (4, 2))

theta_minus = theta.copy()           # 目标网络：滞后同步

Q = lambda th, s: s @ th



s, a, r, s2, gamma = np.array([1.0, 0.5, -0.3, 0.2]), 1, 1.0, np.array([0.8, 0.4, -0.1, 0.3]), 0.9

td_target = r + gamma * Q(theta_minus, s2).max()   # 用目标网络算 TD 目标

td_pred = Q(theta, s)[a]

print(f"TD 目标={td_target:.3f}, 预测={td_pred:.3f}, 损失={(td_target - td_pred) ** 2:.3f}")

```

> 运行环境：Python 3.11+、numpy。示意 TD 目标如何借助目标网络计算，避免「自己追自己」发散。



## 检索练习（闭卷自检）



- 用自己的话复述 **DQN (Deep Q-Network)** 要解决的问题，并举一個它适用的真实场景。

- 对比 **DQN (Deep Q-Network)** 与最相近的概念（如 [[机器学习-Q-Learning]]）的异同，说清各自的适用边界与失败模式。

- 闭卷写出 **DQN (Deep Q-Network)** 的关键步骤 / 公式 / 算法要点，再回卡核对；把错处记入 [[机器学习-错题整理]]。

- （可选）用一份玩具数据集把 **DQN (Deep Q-Network)** 的核心方法跑通，并记录与 Spine（周志华 / Hands-on ML / MML）结果的差异。

## 学完后可以完成



> 下面由作业 `requires` 自动反查：学完本卡后可完成的课后作业、阶段作业与大作业（单一事实源，不手动维护）。



```dataview

LIST

FROM "03-Projects"

WHERE type = "project" AND contains(map(requires, (r) => r.path), this.file.name)

SORT assignment_level ASC, file.name ASC

```

