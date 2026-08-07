---
type: study
topic: "A3C家族"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A3C家族", "A3C 家族"]
upstream: ["[[A2C家族]]", "[[Actor-Critic架构]]"]
tags: [学习, 强化学习]
---

# A3C家族

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
A3C（Asynchronous Advantage Actor-Critic）是 AC 的异步并行版，开创"多 worker 异步更新"。

## 正式定义 / 公式
多个 worker 异步地与全局网络交互、异步地用各自梯度更新全局参数（无锁）。
每个 worker 有局部网络，定期与全局同步。

## 最小手算例子
4 worker 各自独立跑环境，算出梯度后直接异步推给全局网络，互不等待。

## 对比与常见错误
- 与 A2C：A3C 异步、无 barrier；A2C 同步批量。
- 常见错误：以为 A3C "更快一定更好"——异步有陈旧梯度，且 GPU 利用差。

## 闭卷自测
1. A3C 是什么？
2. A3C 与 A2C 的核心差异？
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
