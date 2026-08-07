---
type: study
topic: "超参-Gamma"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["超参-Gamma", "折扣因子 γ"]
upstream: ["[[折扣-回报]]", "[[回报定义]]"]
tags: [学习, 强化学习]
---

# 超参-Gamma

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
γ 决定智能体有多"短视"，是 RL 最基础超参。

## 正式定义 / 公式
回报 G_t = Σ_{l=0}^∞ γ^l r_{t+l}。γ∈[0,1]：越接近 1 越重视长远奖励；越接近 0 越短视。

## 最小手算例子
r=(1,1,1,...)，γ=0.9 → G_t≈10；γ=0.5 → ≈2。

## 对比与常见错误
- 与 超参-Lambda：γ 是回报折扣，λ 是 GAE 偏差—方差系数。
- 常见错误：γ=1 在无界情节下回报可能发散。

## 闭卷自测
1. γ 控制什么？
2. γ 过大会有什么风险？
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
