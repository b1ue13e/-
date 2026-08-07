---
type: study
topic: "V函数-公式"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["V函数-公式", "V^π(s) 的期望展开"]
upstream: ["[[V函数-定义]]"]
tags: [学习, 强化学习]
---

# V函数-公式

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
期望要能计算，需要把 G_t 展开成奖励和折扣的形式。

## 正式定义 / 公式
V^π(s) = E_π [ Σ_{k=0}^∞ γ^k R_{t+k+1} | S_t = s ]
或等价写成递归的期望形式：
V^π(s) = E_π [ R_{t+1} + γ V^π(S_{t+1}) | S_t = s ]

## 最小手算例子
沿用 2 状态 MDP：V^π(s1)=E[R+γV(s2)]=1+0.9·0=1。与定义式一致。

## 对比与常见错误
- 两个式子等价：一个是"展开求和"，一个是"递归一步+剩余"。后者就是贝尔曼期望方程的雏形。
- 常见错误：把 γ^0 的奖励写成 R_t 而不是 R_{t+1}——t 时刻的奖励是 R_{t+1}。

## 闭卷自测
1. 写出 V^π(s) 的两种等价公式。
2. 折扣因子 γ 在公式里作用是什么？
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
