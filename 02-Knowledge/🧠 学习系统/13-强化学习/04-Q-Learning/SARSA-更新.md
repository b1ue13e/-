---
type: study
topic: "SARSA-更新"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["SARSA-更新", "SARSA 更新规则"]
upstream: ["[[Q函数-定义]]", "[[TD-误差]]"]
tags: [学习, 强化学习]
---

# SARSA-更新

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
SARSA 在 Q(s,a) 上做 On-Policy TD 更新：用行为策略实际选出的下一动作 a' 构造目标。

## 正式定义 / 公式
Q(s_t, a_t) ← Q(s_t, a_t) + α [ r_{t+1} + γ Q(s_{t+1}, a_{t+1}) − Q(s_t, a_t) ]
注意目标是 r + γ Q(s', a')，其中 a' 由当前（行为）策略在 s' 选出。

## 最小手算例子
2 状态 A→B(term)，right→B(R=+1)，left→A(R=0)。γ=0.9, α=0.5, Q 初 0。在 (A,right) 得 r=+1,s'=B；行为策略在 B 无动作（终止）则 Q(B,·)=0。
目标 = 1 + 0.9·0 = 1，误差 = 1 − 0 = 1，Q(A,right) ← 0.5。

## 对比与常见错误
- 与 Q-learning：SARSA 目标是 r+γQ(s',a')（a' 由行为策略选）；Q-learning 目标是 r+γ max_{a'}Q(s',a')。
- 常见错误：把 SARSA 目标写成 max——那是 Q-learning（off-policy）的做法。

## 闭卷自测
1. 写出 SARSA 更新式。
2. SARSA 与 Q-learning 更新目标的区别？
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
