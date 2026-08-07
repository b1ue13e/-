---
type: study
topic: "A2C-损失"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A2C-损失", "A2C 损失函数"]
upstream: ["[[A2C-批量]]", "[[Actor-更新]]", "[[Critic-更新]]"]
tags: [学习, 强化学习]
---

# A2C-损失

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
A2C 的总损失 = actor 损失 + critic 损失（常加熵项）。

## 正式定义 / 公式
L = − E[ log π_θ(a|s) · A ] + c_v E[ (V_φ(s) − y)^2 ] − c_e H(π_θ)
三项：策略梯度（带优势）、价值 MSE、熵正则（鼓励探索）。

## 最小手算例子
单样本：actor 项 −logπ(a1)·1.05；critic 项 (V(s)−1.45)^2；熵项 −c_e·H。三项加权求和反传。

## 对比与常见错误
- 与单纯 PG：多了 critic MSE 与熵项。
- 常见错误：漏掉熵项导致探索不足、或熵系数过大扰训练。

## 闭卷自测
1. 写出 A2C 的总损失构成。
2. 熵项起什么作用？
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
