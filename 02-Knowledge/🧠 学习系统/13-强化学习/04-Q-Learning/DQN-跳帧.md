---
type: study
topic: "DQN-跳帧"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DQN-跳帧", "Frame Skip / 跳帧"]
upstream: ["[[DQN-函数逼近]]"]
tags: [学习, 强化学习]
---

# DQN-跳帧

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
在视频游戏等高频环境中，相邻帧高度相似。重复动作若干帧（跳帧）既减少决策频率、又保留时序信息，大幅加速训练。

## 正式定义 / 公式
每 k 帧才选一次动作，期间重复该动作（k=4 常见）。
效果：单幕时间步减少 k 倍，_agent 交互/网络前向次数同步减少。

## 最小手算例子
Atari Breakout：每 4 帧决策一次，中间 3 帧重复动作。单幕从数万步降到数千步，训练提速数倍且性能几乎不变。

## 对比与常见错误
- 与"每帧决策"：每帧决策慢且冗余；跳帧近似无损但快。
- 常见错误：跳帧过大导致动作不够细（如平台跳跃错过窗口）。

## 闭卷自测
1. 跳帧解决什么问题？
2. 跳帧过大有何风险？
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
