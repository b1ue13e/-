---
type: study
topic: "TRPO对比-效率"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO对比-效率", "TRPO 对比：样本/计算效率"]
upstream: ["[[TRPO家族]]"]
tags: [学习, 强化学习]
---

# TRPO对比-效率

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
从计算效率看，TRPO 的 CG/线搜比 PPO 的 clip 更贵。

## 正式定义 / 公式
TRPO 每步多次前向/反向估 Fisher 与 KL，单步成本高；
PPO 复用普通梯度+裁剪成批更新，吞吐更高。

## 最小手算例子
<!-- NUMEX2 -->样本效率：TRPO 每轮需采足量 on-policy 数据（如 2048 步）且多次 CG 迭代；PPO 复用 K=4–10 轮更省。同预算下 PPO 通常快 1–3×。

同硬件下，PPO 每秒更新步数常高于 TRPO（省去 CG/线搜）。

## 对比与常见错误
- 常见错误：认为"复杂=效果好"——效率与最终性能需权衡。

## 闭卷自测
1. TRPO 与 PPO 在计算效率上差异？
2. 如何权衡选哪个？
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
