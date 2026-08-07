---
type: study
topic: "Q函数-公式"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Q函数-公式", "Q^π(s,a) 的期望展开"]
upstream: ["[[Q函数-定义]]"]
tags: [学习, 强化学习]
---

# Q函数-公式

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
同 V，把 Q 的期望展开成可计算形式。

## 正式定义 / 公式
Q^π(s,a) = E_π [ Σ_{k=0}^∞ γ^k R_{t+k+1} | S_t=s, A_t=a ]
递归形式：
Q^π(s,a) = E_π [ R_{t+1} + γ Q^π(S_{t+1}, A_{t+1}) | S_t=s, A_t=a ]

## 最小手算例子
2 状态 MDP：Q^π(s1,step)=E[R+γQ(s2,·)]，而 s2 终止 Q=0，故 =1。

## 对比与常见错误
- 常见错误：递归式里第二步仍写 V 而非 Q——严格递归应回到 Q（因第一步固定了 a，其后动作由 π 决定，是 Q 的自举）。

## 闭卷自测
1. 写出 Q^π(s,a) 的两种公式。
2. 递归形式里为什么回到 Q 而不是 V？
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
