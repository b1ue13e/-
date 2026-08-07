---
type: study
topic: "TRPO对比-复杂"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO对比-复杂", "TRPO 对比：实现复杂度"]
upstream: ["[[TRPO家族]]", "[[TRPO简介]]"]
tags: [学习, 强化学习]
---

# TRPO对比-复杂

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
TRPO 理论上漂亮，但工程复杂（CG+线搜+KL 计算）。这是它被 PPO 取代的主因之一。

## 正式定义 / 公式
TRPO 每次更新需：估计 Fisher-vector 积、CG 迭代、KL 线搜——实现与调参都不轻。
PPO 仅用裁剪（clip）即近似同等效果，代码量小很多。

## 最小手算例子
同样 AC 框架，TRPO 需额外 ~50 行 CG/线搜逻辑；PPO 几行 clip 即可。

## 对比与常见错误
- 常见错误：为"理论优雅"硬上 TRPO——多数场景 PPO 性价比更高。

## 闭卷自测
1. TRPO 的实现复杂度在哪？
2. 为何 PPO 更流行？
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
