---
type: study
topic: "A2C-同步"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A2C-同步", "A2C 同步更新"]
upstream: ["[[A2C家族]]", "[[A2C-简单]]"]
tags: [学习, 强化学习]
---

# A2C-同步

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
A2C 的"同步"指：等所有 worker 完成本轮收集，再统一更新，再广播新参数。

## 正式定义 / 公式
Barrier 同步：workers 收集 → 汇总梯度/优势 → 中心更新 → 广播参数 → workers 继续。
避免异步带来的陈旧梯度（stale gradients）。

## 最小手算例子
4 worker 各跑 20 步后齐步等待，中心合并更新，再同时拿到新参数。

## 对比与常见错误
- 与 A3C 异步：同步无陈旧梯度但需等最慢 worker；异步更快但梯度可能旧。
- 常见错误：以为同步一定慢——GPU 批量下同步常更高效。

## 闭卷自测
1. A2C 的同步指什么？
2. 同步的代价与收益？
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
