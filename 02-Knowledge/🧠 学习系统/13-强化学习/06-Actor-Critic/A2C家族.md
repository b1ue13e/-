---
type: study
topic: "A2C家族"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A2C家族", "A2C 家族"]
upstream: ["[[Actor-Critic架构]]", "[[优势-GAE]]"]
tags: [学习, 强化学习]
---

# A2C家族

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
A2C（Advantage Actor-Critic）是 AC 的同步并行实用版：多个环境同步收集、同步更新。

## 正式定义 / 公式
多 worker 同步执行，收集一批轨迹后用 GAE 估计优势，统一更新 actor/critic。
同步意味着所有 worker 用同一套参数、步调一致。

## 最小手算例子
4 个并行环境各跑一段，收集后合并，用 GAE 算优势，一次梯度更新全局参数。

## 对比与常见错误
- 与 A3C：A2C 同步、实现简单、易在 GPU 批量；A3C 异步。
- 常见错误：把 A2C 当"单环境 AC"——它强调多环境并行批量。

## 闭卷自测
1. A2C 是什么？
2. A2C 与 A3C 的关键区别？
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
