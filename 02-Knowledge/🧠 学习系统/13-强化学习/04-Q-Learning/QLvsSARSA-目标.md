---
type: study
topic: "QLvsSARSA-目标"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["QLvsSARSA-目标", "Q-Learning vs SARSA：更新目标"]
upstream: ["[[QL-更新]]", "[[SARSA-更新]]"]
tags: [学习, 强化学习]
---

# QLvsSARSA-目标

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
更新目标的差异是两者数学上的根本不同，也解释了风险偏好差异。

## 正式定义 / 公式
- Q-learning 目标：r + γ max_{a'} Q(s', a')
- SARSA 目标：r + γ Q(s', a')，a' 由行为策略选出

## 最小手算例子
<!-- NUMEX -->数值：Q(s,a)=0，α=0.1，r=1.0，γ=0.9。Q-learning 取 maxₐ'Q(s',a')=0.5 ⇒ Q←0+0.1×(1+0.9×0.5−0)=0.145。SARSA 用实际下一步动作 Q(s',a')=0.3 ⇒ Q←0.127（更保守、更接近在线策略）。

若 s' 处行为策略多半选"安全动作"（Q 较低），SARSA 目标偏低（保守）；Q-learning 目标取 max（乐观）。

## 对比与常见错误
- 常见错误：把 SARSA 目标写成 max——那是 Q-learning 标志。

## 闭卷自测
1. 写出两者更新目标并圈出关键差异。
2. 该差异如何导致风险偏好不同？
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
