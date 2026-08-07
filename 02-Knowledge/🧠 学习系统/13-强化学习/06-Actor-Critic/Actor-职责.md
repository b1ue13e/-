---
type: study
topic: "Actor-职责"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Actor-职责", "Actor 的职责"]
upstream: ["[[PG-梯度]]", "[[策略梯度]]"]
tags: [学习, 强化学习]
---

# Actor-职责

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
Actor-Critic 把"策略"与"价值"拆成两个角色。Actor 就是那个策略网络，负责出动作并被优化。

## 正式定义 / 公式
Actor = 策略 π_θ(a|s)。它用 critic 提供的"优势 A"做策略梯度更新：
∇_θ J ≈ E[ ∇_θ log π_θ(a|s) · A(s,a) ]
相比 REINFORCE 用裸回报，actor 用 critic 估计的优势，方差更低。

## 最小手算例子
critic 给出 A(s,a1)=+0.5：actor 朝增大 π(a1) 方向更新 θ（步长 α·0.5·∇log π）。

## 对比与常见错误
- 与 critic：actor 学"做什么"，critic 学"多好"，二者互相提供信号。
- 常见错误：让 actor 用原始 G_t 而非优势——那退回高方差 REINFORCE。

## 闭卷自测
1. Actor-Critic 中 actor 负责什么？
2. actor 用什么信号更新？
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
