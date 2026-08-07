---
type: study
topic: "QL-异策略"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["QL-异策略", "Q-Learning Off-Policy"]
upstream: ["[[QL-更新]]", "[[探索与利用]]"]
tags: [学习, 强化学习]
---

# QL-异策略

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
"Off-Policy"意味着"行为策略（用来交互）"与"目标策略（被学习/优化）"可以不同。Q-learning 正是这样：用 ε-greedy 交互，却学贪心最优 Q*。

## 正式定义 / 公式
行为策略 π_b（如 ε-greedy）生成数据；目标策略 π = 贪心（a=argmax_a Q(s,a)）。
因为更新目标是 r+γ max Q(s',a')，只依赖 Q 与奖励，不依赖 π_b 的具体形式 → off-policy。

## 最小手算例子
<!-- NUMEX2 -->Q-learning 是 off-policy：行为策略 ε=0.1 选动作，但用贪心 maxₐ'Q 做目标。例：Q(s,a)=0，选 a 得 r=1，下一状态 max Q=0.5，α=0.1, γ=0.9 ⇒ Q←0+0.1×(1+0.9×0.5−0)=0.145（与所选动作无关，只看最优）。

即便行为策略随机选了"左"（探索），Q-learning 仍按"右"更优去更新目标（max 取右），学习不被行为策略带偏。

## 对比与常见错误
- 与 SARSA（on-policy）：SARSA 目标用行为策略选的 a'，行为策略的探索会"污染"学到的价值。
- 常见错误：以为用了 ε-greedy 就是 on-policy——关键看"更新目标"是否依赖行为策略。

## 闭卷自测
1. 什么是 off-policy？Q-learning 如何体现？
2. 行为策略与目标策略在 Q-learning 中各是什么？
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
