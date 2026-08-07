---
type: study
topic: "GAE-Lambda95"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["GAE-Lambda95", "GAE(0.95)"]
upstream: ["[[GAE-Lambda]]"]
tags: [学习, 强化学习]
---

# GAE-Lambda95

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
理论边界不实用，实践中 PPO 几乎都用 λ≈0.95，需要理解这个经验默认值的由来。

## 正式定义 / 公式
取 λ=0.95（常见 0.9–0.98）：A_t^GAE(0.95) = Σ_{l=0}^∞ (0.99·0.95)^l δ_{t+l}
指数 (γλ)^l 衰减快，只用近若干步 TD 误差，兼顾低偏差与低方差。

## 最小手算例子
(γλ)=0.94 → 第 5 步权重已约 0.73，第 10 步约 0.54，远步影响迅速衰减。

## 对比与常见错误
- 与 λ=0/1：0.95 是二者的折中，最常用。
- 常见错误：以为 λ 越接近 1 越好——过接近 1 会把高方差 MC 尾巴带回来。

## 闭卷自测
1. 为何 PPO 常用 λ≈0.95？
2. 它相比 λ=0 和 λ=1 的平衡点是什么？
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
