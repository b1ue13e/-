---
type: study
topic: "分布式-ApeX"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["分布式-ApeX", "Ape-X DQN"]
upstream: ["[[经验回放与目标网络]]", "[[DQN深度Q网络]]"]
tags: [学习, 强化学习]
---

# 分布式-ApeX

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
单机 DQN 采样慢，如何用大量并行 actor 加速数据收集？

## 正式定义 / 公式
Ape-X：一组并行 actor 各自用 ε-greedy 探索、把转移写入共享优先级经验池；单个 learner 用 PER 采样更新 Q 网络，再把新参数推回 actor。

## 最小手算例子
50 个 actor 同时玩 Atari，learner 每秒更新数千步。

## 对比与常见错误
- 与 DQN：Ape-X 是 DQN 的分布式数据并行版。
- 常见错误：以为 actor 也更新网络——actor 只采样、learner 才更新。

## 闭卷自测
1. Ape-X 如何并行化 DQN？
2. actor 与 learner 职责如何划分？
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
