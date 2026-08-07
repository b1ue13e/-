---
type: study
topic: "DQN-经验回放"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DQN-经验回放", "Experience Replay"]
upstream: ["[[DQN-函数逼近]]", "[[QL-更新]]"]
tags: [学习, 强化学习]
---

# DQN-经验回放

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
在线 RL 样本强相关、且用过即丢很浪费。经验回放把转移 (s,a,r,s') 存进缓冲池，随机采样训练，打破相关性、提高数据效率。

## 正式定义 / 公式
维护缓冲区 D；每步存 (s_t,a_t,r_{t+1},s_{t+1})；训练时从 D 随机 mini-batch 采样，用 Q-learning 目标更新 θ。
损失：L(θ)=E[(r+γ max_{a'}Q_{θ^-}(s',a') − Q_θ(s,a))^2]。

## 最小手算例子
Agent 连续交互，缓冲存数万条；每次梯度更新随机抽 32 条，使相邻样本不再连续相关，训练更稳。

## 对比与常见错误
- 与"在线只用最新样本"：回放降低方差、提升利用率，但引入"离线数据"——off-policy 天然适配 Q-learning。
- 常见错误：缓冲无限增长——实际设固定容量，旧经验被覆盖（FIFO）。

## 闭卷自测
1. 经验回放解决哪两个问题？
2. 为什么它天然适配 Q-learning（而非 SARSA）？
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
