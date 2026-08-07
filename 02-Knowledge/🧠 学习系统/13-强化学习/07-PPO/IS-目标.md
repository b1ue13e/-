---
type: study
topic: "IS-目标"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["IS-目标", "IS 策略梯度"]
upstream: ["[[IS-比率]]", "[[策略梯度]]"]
tags: [学习, 强化学习]
---

# IS-目标

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
有了比率，就能写出 off-policy 的策略梯度目标，用旧策略数据训新策略。

## 正式定义 / 公式
off-policy 策略梯度：
∇_θ J ≈ E_{τ~μ}[ ρ(τ) · ∇_θ log π_θ(τ) · R(τ) ]
或更常见地用优势：
∇_θ J ≈ E[ (Π_{t'} ρ_{t'}) · ∇_θ log π_θ(a_t|s_t) · A^π(s_t,a_t) ]。

## 最小手算例子
<!-- NUMEX -->IS 权重 w=P(a|s)/Q(a|s)。若行为策略 Q 在 a 处概率 0.1、目标策略 P 处 0.5 ⇒ w=5（该转移对目标更重要，需加权）；PPO 用截断 w 防权重爆炸。

单步情形：用 μ 采的 (s,a,r) 乘 ρ_t 后做梯度上升。

## 对比与常见错误
- 与 on-policy PG：多了 ρ 加权，但要求 μ 与 π 行为相近。
- 常见错误：忽视分布偏移导致高方差（见 IS-问题）。

## 闭卷自测
1. off-policy 策略梯度为何要乘比率？
2. 它对行为策略有什么要求？
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
