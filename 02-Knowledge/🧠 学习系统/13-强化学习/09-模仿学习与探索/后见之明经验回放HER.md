---
created: 2026-08-07
type: study
course: "强化学习"
title: "后见之明经验回放 HER (Hindsight Experience Replay)"
topic: "后见之明经验回放 HER (Hindsight Experience Replay)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: algorithm
status: learning
importance: "A"
tags: [学习, 强化学习, 探索, 稀疏奖励]
upstream: ["[[内在奖励与好奇心]]", "[[经验回放与目标网络]]"]
concept: ["HER", "目标条件", "稀疏奖励", "后见之明"]
sources:
  - "Andrychowicz et al. 2017 (HER)"
---
# 后见之明经验回放 HER (Hindsight Experience Replay)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
很多目标导向任务奖励极稀疏（"拿到门钥匙才 +1，否则 0"）。随机探索几乎永远拿不到正奖励，学习信号枯竭。HER 的洞见很朴素：**即使没达成原目标，也可以把"实际到达的状态"当成一个已达成的目标来学习**——从失败中也能提取"如何到达某处"的经验。

## 正式定义 / 公式
目标条件任务用 (s, a, r, s', g) 表示，奖励 r = f(s', g)。训练时：
1. 正常用真实目标 g 存一条转移。
2. **再存若干条"虚拟"转移**：把 g' 换成轨迹中实际出现过的某状态 s'_achieved，奖励改为 f(s', g')（通常为正，因为"到达了 g'"）。
这样即便原目标失败，智能体仍学到"从 A 走到实际到达点"的子技能。常用策略：future（取同轨迹后续状态）、final、random。

## 最小手算例子
机械臂要把方块推到目标点 (5,5)，但推到了 (3,2)。普通 RL 得 0 分、无信号；HER 把目标重标为 (3,2)→这次转移变"成功"，学到"如何把方块推到 (3,2)"。多次后，到达各点的子技能拼出抵达 (5,5) 的能力。

## 对比与常见错误
- 与好奇心/内在奖励：HER 不改奖励本身，而是**重标目标**制造稠密信号；内在奖励是添额外奖励。
- 与课程学习：都缓解稀疏奖励，HER 在经验层面，课程学习在任务层面。
- **常见错误**：虚拟目标全用 final→只学"到终点"忽略中途；目标空间设计错→重标无意义。

## 闭卷自测
1. HER 如何"从失败中提取学习信号"？它重标的是什么？
2. HER 与加内在奖励两种稀疏奖励解法，机制区别在哪？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
