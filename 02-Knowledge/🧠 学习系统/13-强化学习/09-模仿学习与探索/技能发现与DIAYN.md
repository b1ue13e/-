---
created: 2026-08-07
type: study
course: "强化学习"
title: "技能发现与 DIAYN (Skill Discovery & DIAYN)"
topic: "技能发现与 DIAYN (Skill Discovery & DIAYN)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, 探索, 多样性, 无监督]
upstream: ["[[探索与利用基础]]", "[[SAC软Actor-Critic]]"]
concept: ["DIAYN", "技能发现", "互信息", "多样性"]
sources:
  - "Eysenbach et al. 2018 (DIAYN)"
---
# 技能发现与 DIAYN (Skill Discovery & DIAYN)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
没有外部奖励时，智能体该探索什么？DIAYN 主张：**先无监督地学一堆"彼此可区分、且有趣"的技能（skills）**，将来有任务时直接挑技能组合即可。它把"探索"变成"发现多样行为"，是**无监督 RL / 技能发现**的代表。

## 正式定义 / 公式
把策略条件化于离散技能 z：π(a|s,z)。最大化互信息目标：

  max_π I(S; Z) − I(A; Z | S)  ≈  E[ log q_φ(z|s) − log p(z) ]

即：状态 s 要能透露"当前是哪个技能 z"（技能间可区分），但动作 a 不能透露 z（技能靠状态差异而非固定动作区分，行为更自然）。用 SAC 优化，q_φ(z|s) 是判别器。学到的 z 对应"向左走""跳跃"等多样技能。

## 最小手算例子
蚂蚁机器人无奖励。DIAYN 训出 10 个技能：有的让它顺时针转、有的向前冲、有的翻滚。之后接"到某点"的外部奖励时，只需在高层选"向前冲"技能，立刻可用——无需从零探索 locomotion。

## 对比与常见错误
- 与 RND/ICM（单智能体内在奖励）：DIAYN 产出的是**一套可复用技能库**，而非单步新奇度。
- 与课程学习：DIAYN 是任务前的能力储备，课程学习是任务中的难度调度。
- **常见错误**：q_φ 太弱→技能不可分；把 I(A;Z|S) 项丢掉→技能退化为固定动作。

## 闭卷自测
1. DIAYN 的目标里 I(S;Z) 和 I(A;Z|S) 各自在鼓励/抑制什么？
2. 为何说 DIAYN 是"无监督探索"而非"内在奖励探索"？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
