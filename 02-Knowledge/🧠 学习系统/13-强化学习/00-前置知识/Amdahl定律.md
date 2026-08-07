---
type: study
topic: "Amdahl 定律"
course: "强化学习"
created: 2026-08-06
status: completed
stage_moc: "[[🧭 强化学习-前置知识]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Amdahl定律", "并行加速", "分布式"]
upstream: ["[[概率论基础]]"]
tags: [前置, 工程, 分布式, 强化学习]
---

# Amdahl 定律（并行加速上限）

> 所属模块：[[🧭 强化学习-前置知识|前置知识]]

## 动机
分布式 RL 用多 worker 并行采样本质是"并行化"问题。Amdahl 定律给出加速比的上限，提醒我们：若串行部分占比高，加再多机器也快不了多少。

## 定义与公式
整体加速比 S = 1 / ((1 − p) + p/s)，其中 p 是可并行部分比例，s 是这部分理想的加速倍数。

## 最小手算例子
若 90% 工作可并行（p=0.9），理想 s=10：S = 1 / (0.1 + 0.9/10) = 1 / 0.19 ≈ 5.26。即便 s→∞，S 上限 = 1/(1−p) = 10。串行 10% 把加速死死限制在 10 倍。

## 对比与常见错误
- 与 Gustafson 定律互补：后者从"固定时间做更多工作"角度放宽假设。
- 常见错误：以为 worker 数 = 线性加速；忽视环境重置、通信、参数同步这些串行瓶颈。

## 闭卷自测
1. 写出 Amdahl 公式。
2. p=0.9 时加速比上限是多少？
3. 为什么加机器收益会饱和？

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
