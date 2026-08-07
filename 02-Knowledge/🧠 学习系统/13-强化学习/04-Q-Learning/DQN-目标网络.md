---
type: study
topic: "DQN-目标网络"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DQN-目标网络", "Target Network"]
upstream: ["[[DQN-函数逼近]]", "[[QL-更新]]"]
tags: [学习, 强化学习]
---

# DQN-目标网络

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
Q-learning 目标用"同一套在不断移动的 Q_θ"算 max，导致目标随时间剧烈波动、训练发散。目标网络用一份"缓慢更新的旧参数 θ^-"算目标，稳定训练。

## 正式定义 / 公式
目标：y = r + γ max_{a'} Q_{θ^-}(s', a')，其中 θ^- 周期性（或软）从 θ 同步：
θ^- ← θ（每隔 C 步）或 θ^- ← τθ + (1−τ)θ^-（软更新，Polyak）。

## 最小手算例子
每 1000 步把在线网络参数复制给目标网络；其间目标值由"旧"网络提供，避免目标追着自己跑。

## 对比与常见错误
- 与"共用同一网络"：共用会让 TD 目标非平稳，易发散；目标网络是关键稳定手段。
- 常见错误：目标网络同步太频繁（≈无）或太稀疏（目标过时）——需调 C 或 τ。

## 闭卷自测
1. 目标网络解决什么问题？
2. 两种同步方式（硬/软）分别是什么？
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
