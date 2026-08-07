---
type: study
topic: "GAE-Lambda"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["GAE-Lambda", "GAE 的 λ 参数"]
upstream: ["[[GAE-公式]]"]
tags: [学习, 强化学习]
---

# GAE-Lambda

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
GAE 里最关键的旋钮是 λ，它直接决定偏差与方差的取舍。

## 正式定义 / 公式
λ ∈ [0,1] 是 GAE 的超参数：
- λ→0：更接近单步 TD 优势（低方差、高偏差）；
- λ→1：更接近蒙特卡洛优势（高方差、低偏差）。
A_t^GAE(λ) = Σ_{l=0}^∞ (γλ)^l δ_{t+l}。

## 最小手算例子
λ=0 时 A_t=δ_t；λ=1 时 A_t=δ_t+γδ_{t+1}+γ²δ_{t+2}+…，即整条轨迹回报减 V。

## 对比与常见错误
- 与 γ：γ 是标准折扣，λ 是 GAE 专属的偏差—方差系数。
- 常见错误：把 λ 当折扣率调小——λ 调小只是更偏向单步。

## 闭卷自测
1. λ 在 GAE 中控制什么？
2. λ=0 与 λ=1 分别对应哪种优势？
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
