---
created: 2026-08-07
type: study
course: "强化学习"
title: "FeUdal 层级RL (Feudal Hierarchy)"
topic: "FeUdal 层级RL (Feudal Hierarchy)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, 分层, feudal]
upstream: ["[[分层RL概述与temporal abstraction]]", "[[Actor-Critic架构]]"]
concept: ["FeUdal", "Manager", "Worker", "子目标"]
sources:
  - "Vezhnevets et al. 2017 (FeUdal Networks)"
---
# FeUdal 层级RL (Feudal Hierarchy)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
FeUdal Networks 借"封建制度"比喻：Manager（领主）制定**子目标（goal/方向）**给 Worker（封臣），Worker 在一段时间内执行。关键创新是让子目标是**隐空间里的方向**（而非具体状态），并且 Manager 与 Worker **共享底层表征**、各自用不同时间尺度，缓解长程信用分配。

## 正式定义 / 公式
- **Manager**：在 c 步的时间尺度上输出子目标 g_t（隐空间方向，如状态表征的差分 d_t = h(s_t) − h(s_{t−c})）。
- **Worker**：策略 π(a_t | s_t, g_t)，被鼓励让状态表征变化朝 g_t（用 (g_t · h(s_{t+1}))^2 之类的内在奖励对齐）。
- 两者**只通过隐空间目标耦合**：Manager 不直接发动作，Worker 不对 Manager 的每一步负责，只在 c 步后由外部奖励做信用分配。梯度经表征回溯。

## 最小手算例子
迷宫找钥匙：Manager 每 10 步定一个方向"往左上"（隐空间目标），Worker 在 10 步内用具体动作逼近该方向。即便中途细节变化，只要整体方向对、最终拿到钥匙，Manager 得正反馈——长程规划被拆成"粗略方向序列"。

## 对比与常见错误
- 与 Option-Critic：FeUdal 用隐空间方向而非离散选项，梯度可端到端；
- 与 HAC：HAC 用显式状态子目标 + 层级 HER，FeUdal 用隐方向。
- **常见错误**：Manager 时间尺度 c 设错（太短→退化扁平，太长→低层学不动）；Worker 内在奖励权重压过外部奖励。

## 闭卷自测
1. FeUdal 的 Manager 与 Worker 如何解耦？子目标为什么用"隐空间方向"而非"具体状态"？
2. 相比离散选项（Option），FeUdal 的表达/训练优势在哪？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
