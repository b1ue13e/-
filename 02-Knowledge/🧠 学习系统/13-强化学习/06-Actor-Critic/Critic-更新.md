---
type: study
topic: "Critic-更新"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Critic-更新", "Critic 更新规则"]
upstream: ["[[Critic-优势]]", "[[TD-误差]]"]
tags: [学习, 强化学习]
---

# Critic-更新

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
Critic 自身也要训练——用 TD 误差最小化价值预测误差。

## 正式定义 / 公式
L(φ) = E[ (V_φ(s) − y)^2 ],  y = r + γ V_φ(s')（bootstrap 目标）
φ ← φ − β ∇_φ L(φ)
即 critic 用 TD(0) 回归训练（见「TD-误差」「值迭代」）。

## 最小手算例子
(s,r,s')=(s,+1,s'), V(s)=0.4, V(s')=0.5,γ=0.9：y=1+0.9·0.5=1.45；critic 朝 y 调 V(s) 由 0.4→更靠近 1.45。

## 对比与常见错误
- 与 actor 更新：critic 做监督回归（MSE），actor 做策略梯度（似然比）。
- 常见错误：用 actor 的 ∇log π 更新 critic——critic 用自己的 MSE 梯度。

## 闭卷自测
1. 写出 critic 损失与更新。
2. critic 与 actor 的更新方式有何本质不同？
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
