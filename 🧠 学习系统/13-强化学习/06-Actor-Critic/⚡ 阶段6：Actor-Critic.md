---
type: stage
topic: 阶段6：Actor-Critic架构
tags:
- 强化学习
- 算法阶段
- Actor-Critic
created: 2026-04-11
status: ongoing
difficulty: intermediate
concept: []
prerequisites: []
related: []
phase: 6
duration: 5-6周
---

# ⚡ 阶段6：Actor-Critic架构

> **目标**：结合Value-Based和Policy-Based的优势，掌握Actor-Critic系列算法。
> 
> **周期**：预计 5-6 周

---

## 📊 阶段进度

```dataviewjs
const total = dv.pages('"🧠 学习系统/13-强化学习/06-Actor-Critic"').length - 1;
const completed = dv.pages('"🧠 学习系统/13-强化学习/06-Actor-Critic"').where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段进度: ${progress}%** (${completed}/${total} 模块)`);
```

---

## 🎭 Actor-Critic架构

> 两个网络分工协作，优势互补。

### Actor（执行者）

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **网络结构** | 策略网络 π_θ(a\|s) | ⬜ | [[Actor-结构]] |
| **职责** | 负责选择动作 | ⬜ | [[Actor-职责]] |
| **更新依据** | 根据Critic的反馈更新 | ⬜ | [[Actor-更新]] |
| **输出** | 动作概率分布或动作参数 | ⬜ | [[Actor-输出]] |

### Critic（评论者）

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **网络结构** | 价值网络 V(s) 或 Q(s,a) | ⬜ | [[Critic-结构]] |
| **职责** | 负责评估动作好坏 | ⬜ | [[Critic-职责]] |
| **更新目标** | 最小化TD误差 | ⬜ | [[Critic-更新]] |
| **优势** | 比蒙特卡洛更低的方差估计 | ⬜ | [[Critic-优势]] |

### 分工协作流程

```
1. Actor选择动作 a ~ π_θ(a|s)
2. 执行动作，获得 r, s'
3. Critic评估: δ = r + γV(s') - V(s)  (TD误差)
4. Critic更新: 最小化 δ²
5. Actor更新: θ ← θ + α * ∇log π_θ(a|s) * δ
```

### 🎯 Actor-Critic架构检查点
- [ ] 能区分Actor和Critic的职责
- [ ] 理解为什么需要两个网络
- [ ] 能画出Actor-Critic的结构图
- [ ] 理解两者的更新流程

---

## 📊 优势函数 (Advantage Function)

> Actor-Critic的核心，策略梯度的方差缩减利器。

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **定义** | A(s,a) = Q(s,a) - V(s) | ⬜ | [[🧠 学习系统/13-强化学习/06-Actor-Critic/优势-定义|优势-定义]] |
| **直观意义** | 动作a比平均水平好多少 | ⬜ | [[🧠 学习系统/13-强化学习/06-Actor-Critic/优势-直观|优势-直观]] |
| **符号含义** | A > 0: 动作好；A < 0: 动作差 | ⬜ | [[优势-符号]] |
| **Actor更新** | 使用A而非原始回报G | ⬜ | [[优势-更新]] |

### 优势函数估计

| 估计方法 | 公式 | 偏差-方差权衡 | 状态 | 笔记 |
|:---|:---|:---|:---:|:---|
| **单步TD** | A = r + γV(s') - V(s) | 低方差，有偏差 | ⬜ | [[优势-TD]] |
| **n步回报** | A = Σγ^i r_{t+i} + γ^n V(s_{t+n}) - V(s) | 平衡 | ⬜ | [[优势-n步]] |
| **GAE** | 广义优势估计 | 可调参数 | ⬜ | [[优势-GAE]] |

### 🎯 优势函数检查点
- [ ] 能写出优势函数的定义式
- [ ] 理解优势函数的直观含义
- [ ] 能用TD误差估计优势
- [ ] 理解优势如何减小方差

---

## 🔄 A2C / A3C算法

> 经典的Actor-Critic实现。

### A2C (Advantage Actor-Critic)

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **同步更新** | 同步环境交互与梯度更新 | ⬜ | [[A2C-同步]] |
| **批量更新** | 收集N步经验后批量更新 | ⬜ | [[A2C-批量]] |
| **损失函数** | 策略损失 + 价值损失 + 熵正则 | ⬜ | [[A2C-损失]] |
| **实现简单** | 相比A3C更容易实现 | ⬜ | [[A2C-简单]] |

### A3C (Asynchronous A-C)

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **异步并行** | 多线程并行交互环境 | ⬜ | [[A3C-异步]] |
| **全局网络** | 共享的全局Actor和Critic | ⬜ | [[A3C-全局]] |
| **去相关** | 异步打破样本相关性 | ⬜ | [[A3C-去相关]] |
| **无需经验回放** | 并行替代经验回放 | ⬜ | [[A3C-无ER]] |

### A2C/A3C算法流程

```python
for iteration:
    # 收集N步经验
    states, actions, rewards, next_states = [], [], [], []
    for step in range(N):
        a = Actor.choose_action(s)
        s', r, done = env.step(a)
        存储经验
        s = s'
    
    # 计算优势
    A = compute_advantages(rewards, values, next_value)
    
    # 更新Critic
    value_loss = (returns - values).pow(2).mean()
    
    # 更新Actor
    policy_loss = -(log_probs * A.detach()).mean()
    entropy_loss = -entropy_bonus * entropy.mean()
    
    total_loss = policy_loss + c1 * value_loss + entropy_loss
    反向传播更新
```

### 🎯 A2C/A3C检查点
- [ ] 能实现A2C算法
- [ ] 理解A2C和A3C的区别
- [ ] 理解为什么A3C不需要经验回放
- [ ] 能调优损失函数中的系数

---

## 🛡️ TRPO (Trust Region Policy Optimization)

> 信任区域方法，保证策略单调改进。

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **信任区域** | 限制策略更新幅度 | ⬜ | [[TRPO-信任区域]] |
| **KL约束** | KL散度约束策略变化 | ⬜ | [[TRPO-KL]] |
| **单调改进** | 理论保证策略不恶化 | ⬜ | [[TRPO-单调]] |
| **共轭梯度** | 避免计算Fisher信息矩阵 | ⬜ | [[TRPO-CG]] |

### TRPO目标函数

```
最大化: E[ π_θ(a|s) / π_θold(a|s) * A(s,a) ]
约束:   KL(π_θold || π_θ) ≤ δ
```

### TRPO vs 普通PG

| 特性 | 普通策略梯度 | TRPO | 状态 | 笔记 |
|:---|:---|:---|:---:|:---|
| **更新步长** | 固定学习率 | 自适应 | ⬜ | [[TRPO对比-步长]] |
| **稳定性** | 可能崩溃 | 稳定 | ⬜ | [[TRPO对比-稳定]] |
| **实现复杂度** | 简单 | 复杂 | ⬜ | [[TRPO对比-复杂]] |
| **数据效率** | 一般 | 高 | ⬜ | [[TRPO对比-效率]] |

### 🎯 TRPO检查点
- [ ] 理解信任区域的思想
- [ ] 理解KL散度的作用
- [ ] 知道TRPO的理论保证
- [ ] 了解共轭梯度的作用

---

## 🔗 Actor-Critic家族关系

| 算法 | 特点 | 前身 | 后继 | 状态 | 笔记 |
|:---|:---|:---|:---|:---:|:---|
| **QAC** | 用Q代替V | Q-Learning | A2C | ⬜ | [[QAC]] |
| **A2C** | 同步Advantage AC | QAC | PPO | ⬜ | [[A2C家族]] |
| **A3C** | 异步并行 | A2C | - | ⬜ | [[A3C家族]] |
| **TRPO** | 信任区域 | 自然PG | PPO | ⬜ | [[TRPO家族]] |
| **PPO** | 简化TRPO | TRPO | - | ⬜ | [[PPO家族]] |

---

## 🛠️ 阶段项目

| 项目 | 内容 | 技能点 | 状态 | 笔记 |
|:---|:---|:---|:---:|:---|
| **A2C实现** | 完整实现A2C算法 | Actor-Critic基础 | ⬜ | [[项目-A2C]] |
| **CartPole Actor-Critic** | 用AC解决CartPole | 离散动作AC | ⬜ | [[项目-CartPoleAC]] |
| **连续控制AC** | 解决Pendulum或MountainCar连续版 | 连续动作AC | ⬜ | [[项目-连续AC]] |
| **算法对比** | 对比REINFORCE、A2C、A3C性能 | 算法分析 | ⬜ | [[项目-AC对比]] |

---

## 📝 学习清单

```dataviewjs
dv.table(
    ["主题", "类型", "状态", "更新日期"],
    dv.pages('"🧠 学习系统/13-强化学习/06-Actor-Critic"')
        .where(p => !p.file.path.includes("⚡"))
        .sort(p => p.file.name)
        .map(p => [
            p.file.link,
            p.topic || "-",
            p.status || "ongoing",
            p.file.mtime.toFormat("yyyy-MM-dd")
        ])
);
```

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[🧠 学习系统/13-强化学习/06-Actor-Critic/🎭 阶段5：策略梯度|返回阶段5]] | [[🗺️ 强化学习学习路径\|返回总览]] | [[🧠 学习系统/13-强化学习/06-Actor-Critic/🚀 阶段7：PPO|进入阶段7]] |

---

## 📚 推荐资源

| 类型 | 资源 | 说明 |
|:---|:---|:---|
| 📖 教材 | 《Reinforcement Learning: An Introduction》第13章 | Actor-Critic基础 |
| 📄 论文 | "Asynchronous Methods for Deep RL" (A3C) | A3C原文 |
| 📄 论文 | "Trust Region Policy Optimization" (TRPO) | TRPO原文 |
| 🎬 视频 | CS285 Berkeley Lecture 6-7 | Actor-Critic详解 |
| 💻 代码 | OpenAI Baselines A2C/A3C | 官方实现参考 |

---

*阶段创建：2026-04-11*
