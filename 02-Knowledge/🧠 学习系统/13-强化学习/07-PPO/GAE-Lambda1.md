---
type: study
topic: "GAE-Lambda1"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["GAE-Lambda1", "GAE(1)"]
upstream: ["[[GAE-Lambda]]", "[[蒙特卡洛方法]]"]
tags: [学习, 强化学习]
---

# GAE-Lambda1

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
另一边界 λ=1 让 GAE 退化为蒙特卡洛式优势，便于理解偏差随 λ 增大的变化。

## 正式定义 / 公式
A_t^GAE(1) = Σ_{l=0}^∞ γ^l δ_{t+l} = (Σ_{l=0}^∞ γ^l r_{t+l}) − V(s_t) = G_t − V(s_t)
即标准 MC 优势：实际回报减状态价值。

## 最小手算例子
若从 t 起的折扣回报 G_t=5.0，V(s_t)=4.2，则 A≈0.8。

## 对比与常见错误
- 与 GAE(0)：GAE(1) 无偏但方差高。
- 常见错误：认为 GAE(1) 仍需 bootstrapping——它已用真实全程回报，无 V 外推。

## 闭卷自测
1. GAE(1) 退化成什么？
2. 为何它方差高却无偏？
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
