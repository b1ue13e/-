---
type: stage
topic: 阶段4：Q-Learning算法
tags:
- 强化学习
- 算法阶段
- Q-Learning
created: 2026-04-11
status: ongoing
difficulty: intermediate
concept: []
prerequisites: []
related: []
phase: 4
duration: 5-6周
---

# 🧠 阶段4：Q-Learning算法

> **目标**：掌握Value-Based方法，理解TD学习、Q-Learning与DQN。
> 
> **周期**：预计 5-6 周

---

## 📊 阶段进度

```dataviewjs
const total = dv.pages('"🧠 学习系统/13-强化学习/04-Q-Learning"').length - 1;
const completed = dv.pages('"🧠 学习系统/13-强化学习/04-Q-Learning"').where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段进度: ${progress}%** (${completed}/${total} 模块)`);
```

---

## 🔄 TD学习 (Temporal Difference)

> 结合蒙特卡洛和动态规划的优势。

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **TD(0)** | V(s) ← V(s) + α[r + γV(s') - V(s)] | ⬜ | [[TD-0]] |
| **TD误差** | δ = r + γV(s') - V(s) | ⬜ | [[TD-误差]] |
| **自举 (Bootstrapping)** | 用当前估计更新估计 | ⬜ | [[TD-自举]] |
| **采样** | 不需要完整轨迹 | ⬜ | [[TD-采样]] |

### TD vs MC vs DP

| 方法 | 采样 | 自举 | 适用场景 | 状态 | 笔记 |
|:---|:---:|:---:|:---|:---:|:---|
| **蒙特卡洛** | ✓ | ✗ | 回合制任务 | ⬜ | [[MC方法]] |
| **TD(0)** | ✓ | ✓ | 在线学习 | ⬜ | [[TD0对比]] |
| **动态规划** | ✗ | ✓ | 已知模型 | ⬜ | [[DP方法]] |

### 🎯 TD学习检查点
- [ ] 理解TD(0)的更新规则
- [ ] 能区分TD误差和MC误差
- [ ] 理解自举的概念和作用
- [ ] 比较TD和MC的优缺点

---

## 🎮 SARSA算法

> On-Policy TD控制算法。

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **算法名称** | State-Action-Reward-State-Action | ⬜ | [[SARSA-名称]] |
| **更新规则** | Q(s,a) ← Q(s,a) + α[r + γQ(s',a') - Q(s,a)] | ⬜ | [[SARSA-更新]] |
| **On-Policy** | 行为策略与目标策略相同 | ⬜ | [[SARSA-同策略]] |
| **收敛性** | 满足GLIE条件时收敛 | ⬜ | [[SARSA-收敛]] |

### SARSA算法流程

```
初始化 Q表
for 每个 episode:
    获取初始状态 s，使用策略选择动作 a
    while 未终止:
        执行动作 a，获得 r, s'
        使用策略选择新动作 a'
        Q[s][a] += α * (r + γ * Q[s'][a'] - Q[s][a])
        s, a = s', a'
```

### 🎯 SARSA检查点
- [ ] 能实现SARSA算法
- [ ] 理解On-Policy的含义
- [ ] 能解释SARSA的名字由来
- [ ] 理解ε-贪心在SARSA中的作用

---

## 🧠 Q-Learning算法

> Off-Policy TD控制算法，RL的经典算法。

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **更新规则** | Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') - Q(s,a)] | ⬜ | [[QL-更新]] |
| **Off-Policy** | 行为策略与目标策略不同 | ⬜ | [[QL-异策略]] |
| **最大化偏差** | max操作引入的过估计问题 | ⬜ | [[QL-最大化偏差]] |
| **收敛性** | 满足条件时收敛到Q* | ⬜ | [[QL-收敛]] |

### Q-Learning算法流程

```
初始化 Q表
for 每个 episode:
    获取初始状态 s
    while 未终止:
        使用ε-greedy选择动作 a
        执行动作，获得 r, s'
        TD目标 = r + γ * max(Q[s'])
        TD误差 = TD目标 - Q[s][a]
        Q[s][a] += α * TD误差
        s = s'
```

### Q-Learning vs SARSA

| 特性 | Q-Learning | SARSA | 状态 | 笔记 |
|:---|:---|:---|:---:|:---|
| **策略类型** | Off-Policy | On-Policy | ⬜ | [[QLvsSARSA-策略]] |
| **更新目标** | max_a' Q(s',a') | Q(s',a') | ⬜ | [[QLvsSARSA-目标]] |
| **风险偏好** | 更激进(乐观) | 更保守 | ⬜ | [[QLvsSARSA-风险]] |
| **应用场景** | 确定性环境 | 随机性环境 | ⬜ | [[QLvsSARSA-应用]] |

### 🎯 Q-Learning检查点
- [ ] 能实现Q-Learning算法
- [ ] 区分On-Policy和Off-Policy
- [ ] 理解为什么Q-Learning是Off-Policy
- [ ] 能对比Q-Learning和SARSA的适用场景

---

## 🏗️ DQN (Deep Q-Network)

> 用神经网络近似Q函数，解决维度灾难。

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **函数逼近** | Q(s,a;θ) 用神经网络表示 | ⬜ | [[DQN-函数逼近]] |
| **经验回放** | Experience Replay Buffer | ⬜ | [[DQN-经验回放]] |
| **目标网络** | Target Network 稳定训练 | ⬜ | [[DQN-目标网络]] |
| **Huber Loss** | 平滑L1损失 | ⬜ | [[DQN-损失]] |

### DQN关键技术

| 技术 | 作用 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **经验回放** | 打破样本相关性，提高数据利用率 | ⬜ | [[DQN-ER详解]] |
| **目标网络** | 减少目标值波动，稳定训练 | ⬜ | [[DQN-TN详解]] |
| **ε-衰减** | 渐进式减少探索 | ⬜ | [[DQN-衰减]] |
| **跳帧 (Frame Skip)** | 加速训练 | ⬜ | [[DQN-跳帧]] |

### DQN改进算法

| 算法 | 改进点 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **Double DQN** | 解耦选择与评估，减少过估计 | ⬜ | [[Double-DQN]] |
| **Dueling DQN** | 分离V和A估计 | ⬜ | [[Dueling-DQN]] |
| **Prioritized ER** | 优先采样重要经验 | ⬜ | [[PER]] |
| **Noisy Nets** | 参数化探索替代ε-贪心 | ⬜ | [[NoisyNets]] |
| **Categorical DQN** | 学习价值分布而非期望 | ⬜ | [[C51]] |
| **Rainbow** | 整合六种改进 | ⬜ | [[Rainbow]] |

### 🎯 DQN检查点
- [ ] 理解为什么需要函数逼近
- [ ] 能实现基础DQN
- [ ] 理解经验回放的作用
- [ ] 理解目标网络的作用
- [ ] 了解至少两种DQN改进

---

## ⚠️ Value-Based局限性

| 问题 | 说明 | 解决方案 | 状态 | 笔记 |
|:---|:---|:---|:---:|:---|
| **维度灾难** | 状态空间大时Q表内存爆炸 | 函数逼近 | ⬜ | [[局限-维度灾难]] |
| **连续状态** | 无法直接处理连续状态空间 | 神经网络 | ⬜ | [[局限-连续状态]] |
| **连续动作** | 无法处理连续动作空间 | 策略梯度方法 | ⬜ | [[局限-连续动作]] |
| **离散动作限制** | max操作在连续动作上困难 | Actor-Critic | ⬜ | [[局限-离散限制]] |

---

## 🛠️ 阶段项目

| 项目 | 内容 | 技能点 | 状态 | 笔记 |
|:---|:---|:---|:---:|:---|
| **迷宫求解器** | 用Q-Learning求解迷宫 | Q-Learning实现 | ⬜ | [[项目-迷宫QL]] |
| **CartPole DQN** | 用DQN解决CartPole问题 | DQN实现 | ⬜ | [[项目-CartPoleDQN]] |
| **SARSA对比实验** | 对比Q-Learning和SARSA在悬崖问题上的表现 | 算法对比 | ⬜ | [[项目-悬崖对比]] |
| **Atari Breakout** | 实现DQN玩Breakout游戏 | 图像输入处理 | ⬜ | [[项目-Breakout]] |

---

## 📝 学习清单

```dataviewjs
dv.table(
    ["主题", "类型", "状态", "更新日期"],
    dv.pages('"🧠 学习系统/13-强化学习/04-Q-Learning"')
        .where(p => !p.file.path.includes("🧠"))
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
| [[🧠 学习系统/13-强化学习/04-Q-Learning/📊 阶段3：策略与价值函数|返回阶段3]] | [[🗺️ 强化学习学习路径\|返回总览]] | [[🧠 学习系统/13-强化学习/04-Q-Learning/🎭 阶段5：策略梯度|进入阶段5]] |

---

## 📚 推荐资源

| 类型 | 资源 | 说明 |
|:---|:---|:---|
| 📖 教材 | 《Reinforcement Learning: An Introduction》第5-6章 | TD学习与Q-Learning |
| 📄 论文 | "Playing Atari with Deep Reinforcement Learning" (DQN) | 深度强化学习开山之作 |
| 📄 论文 | "Human-level control through deep RL" (Nature DQN) | Nature版本DQN |
| 💻 代码 | Stable-Baselines3 DQN实现 | 高质量参考实现 |

---

*阶段创建：2026-04-11*
