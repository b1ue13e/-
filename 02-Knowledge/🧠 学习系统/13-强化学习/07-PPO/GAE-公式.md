---
type: study
topic: "GAE-公式"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["GAE-公式", "GAE(λ) 公式"]
upstream: ["[[GAE-单步]]", "[[TD-0]]"]
tags: [学习, 强化学习]
---

# GAE-公式

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
单步优势偏差大、MC 方差大，能否把多步 TD 误差按权重叠加，连续调节偏差—方差？

## 正式定义 / 公式
广义优势估计：
A_t^GAE(λ) = Σ_{l=0}^∞ (γλ)^l δ_{t+l}
其中 δ_{t+l} = r_{t+l} + γ V(s_{t+l+1}) − V(s_{t+l})。
它把从 t 开始的各步 TD 误差做指数加权平均，λ 控制多远处的信息权重。

## 最小手算例子
δ_t=0.58, δ_{t+1}=0.3, γ=0.99, λ=0.95 → A≈0.58 + 0.94·0.3 + ...。

## 对比与常见错误
- 与单步：GAE 是单步的多步推广。
- 常见错误：误以为 (γλ)^l 把折扣和偏差—方差系数混为一谈——γ 管时间折扣，λ 管偏差—方差。

## 闭卷自测
1. GAE 公式如何把多步 TD 误差组合？
2. 指数权重 (γλ)^l 里 γ 与 λ 各管什么？
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
