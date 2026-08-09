---
created: 2026-08-07
type: study
course: "强化学习"
title: "分层RL与 Options (HRL)"
topic: "分层RL与 Options (HRL)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[多智能体RL概述]]", "[[MDP 与贝尔曼方程]]"]
concept: ["分层RL", "Options", "半马尔可夫", "时间抽象"]
sources:
  - "Sutton et al. 1999 (Options framework); Bacon 2017 (Option-Critic)"
---
# 分层RL与 Options (HRL)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Options 框架 / Option-Critic`
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
长程任务（如"做饭"）难以端到端学。分层 RL 用时间抽象：高层选"子目标/选项"，低层执行具体动作，把长任务拆成可复用的短时序技能。

## 正式定义 / 公式
Options = ( initiation set I, policy π_ω, termination β )；高层在宏观步选选项，选项内低层执行直到终止 β(s)=1，再回高层。半马尔可夫决策过程 (SMDP) 描述跨选项转移。

## 最小手算例子
任务"取杯→倒水→喝"，3 个选项。每选项约 5 步微观动作；总步数 15。
若端到端直接学，需探索 15 步长链（稀疏）；分层后高层每步决策只 3 选项，探索空间骤降。

## 对比与常见错误
- 与扁平 RL：HRL 提供时间抽象、可复用技能，但需设计/学习选项结构。
- 常见错误：选项终止条件设计不当导致选项永不结束/立即终止；高层与低层奖励未对齐。

## 闭卷自测
1. Option 由哪三个部分构成？
2. 分层 RL 为何能降低探索难度？

## 直觉：用“临时子目标”降低时序 credit 难度
扁平 RL 在长任务里信用分配难。分层 RL 引入 Options（子策略 + 终止条件）作为“临时动作”，高层选 Option、低层执行，时间抽象让探索与迁移更高效。半马尔可夫 Option 有初始化集、策略、β(s) 终止函数。代价：选项集与终止条件需精心设计，否则徒增复杂度；高层选项粒度太细则退化为扁平。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
