---
type: study
topic: "QL-更新"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["QL-更新", "Q-Learning 更新规则"]
upstream: ["[[Q函数-定义]]", "[[TD-误差]]"]
tags: [学习, 强化学习]
---

# QL-更新

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
Q-Learning 是经典 Off-Policy TD 控制算法，直接学最优动作价值 Q*，不依赖行为策略。

## 正式定义 / 公式
Q(s_t, a_t) ← Q(s_t, a_t) + α [ r_{t+1} + γ max_{a'} Q(s_{t+1}, a') − Q(s_t, a_t) ]
目标用 max_{a'} Q(s', a')——对未来动作取最优，与行为策略无关。

## 最小手算例子
2 状态 A→B(term)，right→B(R=+1)。γ=0.9, α=0.5, Q 初 0。在 (A,right) 得 r=+1,s'=B：
目标 = 1 + 0.9·max_a'Q(B,a') = 1 + 0 = 1；误差 = 1 − 0 = 1；Q(A,right) ← 0.5。

## 对比与常见错误
- 与 SARSA：Q-learning 目标取 max（最优），SARSA 取行为策略选的 a'。
- 常见错误：把 Q-learning 写成用 a'（实际下一动作）——那会变成 SARSA。

## 闭卷自测
1. 写出 Q-Learning 更新式。
2. 为什么 Q-learning 是 off-policy？
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
