---
type: study
topic: "QAC"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["QAC", "Q Actor-Critic"]
upstream: ["[[Actor-Critic架构]]", "[[Q函数-定义]]"]
tags: [学习, 强化学习]
---

# QAC

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
多数 AC 用 V-critic；也可用 Q-critic：critic 估 Q(s,a)，优势直接 A=Q(s,a)−V(s) 或仅用 Q。

## 正式定义 / 公式
critic 估 Q_φ(s,a)（动作维度输出）。
优势：A(s,a)=Q_φ(s,a)−V_φ(s)（需另估 V，或用平均 Q 近似 V）；或 actor 直接用 Q 选动作。
连续动作下 Q-critic 难（需 max/积分），故 V-critic 更常见。

## 最小手算例子
离散动作：critic 输出 2 个 Q；A(a1)=Q(a1)−mean(Q)。连续动作下多用 V-critic。

## 对比与常见错误
- 与 V-critic：Q-critic 直接给动作价值但连续动作不便；V-critic 更通用。
- 常见错误：连续动作硬上 Q-critic——需处理 max_a Q，回归值方法的老问题。

## 闭卷自测
1. Q Actor-Critic 与 V-critic 区别？
2. 为何连续动作少用 Q-critic？
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
