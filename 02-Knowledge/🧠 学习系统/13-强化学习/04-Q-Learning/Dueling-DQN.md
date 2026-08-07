---
type: study
topic: "Dueling-DQN"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Dueling-DQN", "Dueling DQN"]
upstream: ["[[DQN-函数逼近]]"]
tags: [学习, 强化学习]
---

# Dueling-DQN

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
很多状态下"选哪个动作"差别不大，价值主要来自"状态本身好坏"。Dueling DQN 把 Q 拆成状态价值 V 与优势 A 分别估计，提升学习效率。

## 正式定义 / 公式
Q(s,a;θ,α,β) = V(s;θ,β) + ( A(s,a;θ,α) − mean_{a'} A(s,a';θ,α) )
V 估"状态多好"，A 估"相对平均动作好多少"；减均值是为可辨识性（否则 V、A 各自不唯一）。

## 最小手算例子
在多数动作等价的状态，Dueling 只需 V 网络学好状态价值，A 近似 0；表格/标准 DQN 却要在各动作上分别拟合，浪费容量。

## 对比与常见错误
- 与标准 DQN：Dueling 改的是"网络结构"（输出头），不基于新损失；可与 DDQN/PER 叠加。
- 常见错误：忘记减 A 的均值——不减去则 V、A 存在平移歧义，训练不稳。

## 闭卷自测
1. Dueling DQN 把 Q 拆成什么？
2. 为什么要减去优势均值？
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
