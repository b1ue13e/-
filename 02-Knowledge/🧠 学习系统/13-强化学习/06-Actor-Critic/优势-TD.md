---
type: study
topic: "优势-TD"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["优势-TD", "TD 优势估计"]
upstream: ["[[优势-定义]]", "[[TD-误差]]"]
tags: [学习, 强化学习]
---

# 优势-TD

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
最常用、最低延迟的优势估计：一步 TD 误差。

## 正式定义 / 公式
A(s,a) ≈ r_{t+1} + γ V_φ(s_{t+1}) − V_φ(s_t)
即 critic 的 TD 误差。偏差低延迟、在线可得，但方差/偏差来自 V_φ 误差与单步近似。

## 最小手算例子
r=+1,γ=0.9,V(s)=0.4,V(s')=0.5：A=1+0.45−0.4=1.05，actor 立刻用此更新。

## 对比与常见错误
- 与 MC 优势（G_t−V）：TD 优势在线、低方差但有偏；MC 无偏但高方差。
- 常见错误：把 TD 优势当无偏——它依赖 V_φ 估计，有偏。

## 闭卷自测
1. 写出 TD 形式优势估计。
2. 它相对 MC 优势 bias/variance 特征？
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
