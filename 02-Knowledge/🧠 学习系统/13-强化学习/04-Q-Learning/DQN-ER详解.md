---
type: study
topic: "DQN-ER详解"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DQN-ER详解", "经验回放详解"]
upstream: ["[[DQN-经验回放]]"]
tags: [学习, 强化学习]
---

# DQN-ER详解

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
经验回放看似简单，但有工程细节决定成败：容量、采样、与函数逼近的配合。

## 正式定义 / 公式
- 容量：固定大小环形缓冲，新经验覆盖最旧（避免分布严重过时）。
- 采样：均匀随机 mini-batch（基础版）；进阶见 PER（优先经验回放）。
- 配合：因采样打乱时序，必须 off-policy（Q-learning）才能用历史数据。

## 最小手算例子
CartPole 训练：缓冲容量 10^5，每步存一条，每次更新抽 32 条；早期样本被逐步覆盖，保持数据"新鲜度"。

## 对比与常见错误
- 与 PER：均匀回放对"重要经验"一视同仁；PER 按 TD 误差优先采样（见 PER）。
- 常见错误：缓冲过小导致几乎无打乱、过大导致陈旧——需按任务调容量。

## 闭卷自测
1. 经验回放的三个关键工程点？
2. 为什么回放要求 off-policy？
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
