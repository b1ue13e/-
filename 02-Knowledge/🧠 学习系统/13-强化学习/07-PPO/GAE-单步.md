---
type: study
topic: "GAE-单步"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["GAE-单步", "单步优势估计"]
upstream: ["[[优势-定义]]", "[[TD-0]]"]
tags: [学习, 强化学习]
---

# GAE-单步

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
优势 A(s,a) 需要知道 Q 与 V，但二者都未知。能否用 critic 的单步 TD 误差就地估计优势，而不等整条轨迹？

## 正式定义 / 公式
单步（λ=0）优势就是 TD 误差：
δ_t = r_t + γ V_φ(s_{t+1}) − V_φ(s_t) ≈ A(s_t, a_t)
它用下一状态的 V 估计替代了真实后续回报，偏差小但方差较低。

## 最小手算例子
V(s_t)=1.0, r_t=0.5, γ=0.9, V(s_{t+1})=1.2 → δ_t = 0.5 + 0.9·1.2 − 1.0 = 0.58。

## 对比与常见错误
- 与 MC 优势：单步优势方差小、偏差大；MC 无偏但方差大。
- 常见错误：把 δ_t 当成无偏优势——它依赖 V_φ 的估计误差。

## 闭卷自测
1. 单步优势估计与 TD 误差是什么关系？
2. 它的偏差与方差特点？
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
