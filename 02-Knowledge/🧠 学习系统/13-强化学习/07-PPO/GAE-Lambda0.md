---
type: study
topic: "GAE-Lambda0"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["GAE-Lambda0", "GAE(0)"]
upstream: ["[[GAE-Lambda]]"]
tags: [学习, 强化学习]
---

# GAE-Lambda0

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
先看 GAE 的边界情形 λ=0，它退化为最简单的单步优势。

## 正式定义 / 公式
A_t^GAE(0) = δ_t = r_t + γ V(s_{t+1}) − V(s_t)
这正是单步 TD 误差。

## 最小手算例子
V(s_t)=1.0, r_t=0.5, γ=0.9, V(s_{t+1})=1.2 → A=0.58（同 GAE-单步）。

## 对比与常见错误
- 与 GAE(1)：GAE(0) 偏差大、方差小；GAE(1) 相反。
- 常见错误：认为 GAE(0) 无偏——它受 V_φ 估计误差影响，并非无偏。

## 闭卷自测
1. GAE(0) 等于什么？
2. 它的偏差—方差倾向如何？
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
