---
type: study
topic: "超参-Lambda"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["超参-Lambda", "GAE λ"]
upstream: ["[[GAE-Lambda]]"]
tags: [学习, 强化学习]
---

# 超参-Lambda

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
PPO 的优势估计质量几乎由 λ 决定。

## 正式定义 / 公式
λ 是 GAE 的偏差—方差系数：A_t^GAE(λ)=Σ(γλ)^l δ_{t+l}。常用 0.9–0.98（即 GAE-Lambda95）。

## 最小手算例子
λ=0.95 在偏差与方差间取平衡，是事实默认值。

## 对比与常见错误
- 与 超参-Gamma：不要混淆，λ 专属于 GAE。
- 常见错误：把 λ 当作折扣率调节——它只调偏差—方差。

## 闭卷自测
1. PPO 中 λ 的常用取值？
2. 它与 γ 的区别？
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
