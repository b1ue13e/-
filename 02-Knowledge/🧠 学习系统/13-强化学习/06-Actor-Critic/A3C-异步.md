---
type: study
topic: "A3C-异步"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A3C-异步", "A3C 异步更新"]
upstream: ["[[A3C家族]]", "[[A3C-全局]]"]
tags: [学习, 强化学习]
---

# A3C-异步

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
A3C 的"异步"是性能关键：worker 不互相等待，异步推梯度。

## 正式定义 / 公式
worker 算完梯度立即异步应用到全局（如 Hogwild 式无锁更新）。
不同 worker 用"略旧"参数，梯度天然带多样性。

## 最小手算例子
worker 1 在 t 时刻更新全局；worker 2 在 t+ε 用更新后的全局参数继续——时间错开。

## 对比与常见错误
- 与同步：异步省等待但梯度可能陈旧（stale）。
- 常见错误：以为异步"白赚速度无代价"——陈旧梯度可能降收敛质量。

## 闭卷自测
1. A3C 异步更新如何工作？
2. 异步的代价？
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
