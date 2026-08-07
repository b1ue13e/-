---
type: study
topic: "随机性MDP"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["随机性", "MDP"]
upstream: ["[[MDP-转移概率]]"]
tags: [学习, 强化学习]
---

# 随机性MDP

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：转移概率
> 前置：[[MDP-转移概率]]

## 动机

绝大多数现实环境是随机的；这是 RL 与确定性规划的根本区别，也是期望、方差、探索出现的根源。

## 正式定义 / 公式

- **随机性 MDP**：对 $(s,a)$，$P(s'\mid s,a)$ 是非退化分布，下一状态按概率采样。
- 价值是期望 $v_\pi(s)=\mathbb{E}[G_t\mid s]$；同动作不同结果。

## 最小手算例子

掷骰子走格：同样"前进 3"可能因骰子结果落到不同格；规划须用期望。

## 对比与常见错误

- **用单次结果当期望**：随机下需多次采样估计价值。
- **忽视探索**：随机环境更需探索以估计各臂/状态。

## 闭卷自测
- 随机 MDP 的价值为何是期望？
- 与确定性 MDP 训练差异？

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```
