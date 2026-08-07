---
type: study
topic: "Q函数-定义"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Q函数-定义", "动作价值函数 Q^π(s,a)"]
upstream: ["[[V函数-定义]]", "[[回报定义]]"]
tags: [学习, 强化学习]
---

# Q函数-定义

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
有时我们不仅关心"这个状态好不好"，还关心"在这个状态**做某个动作**好不好"。这引出了动作价值函数 Q^π(s,a)。

## 正式定义 / 公式
动作价值函数（action-value function）：
Q^π(s,a) = E_π [ G_t | S_t = s, A_t = a ]
即在 s 执行 a、之后遵循 π 的条件下，回报的期望。

## 最小手算例子
沿用 2 状态 MDP，s1 只有动作 step，奖励 +1：
Q^π(s1, step) = E[R + γV(s2)] = 1 + 0.9·0 = 1 = V^π(s1)。

## 对比与常见错误
- 与 V：V 对"状态"打分；Q 对"状态-动作"打分。当策略给定，V(s)=Σ_a π(a|s)Q(s,a)（见「VQ关系-V从Q」）。
- 常见错误：把 Q(s,a) 当成"在 s 之后全程都做 a"——实际只在第一步做 a，之后回到策略 π。

## 闭卷自测
1. Q^π(s,a) 的定义？
2. Q 与 V 的核心区别？
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
