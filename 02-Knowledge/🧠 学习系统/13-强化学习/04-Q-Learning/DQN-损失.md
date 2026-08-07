---
type: study
topic: "DQN-损失"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DQN-损失", "DQN Huber Loss"]
upstream: ["[[DQN-函数逼近]]", "[[DQN-目标网络]]"]
tags: [学习, 强化学习]
---

# DQN-损失

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
DQN 用"均方 TD 误差"训练，但实际常用 Huber Loss（平滑 L1）：对异常大的 TD 误差不那么敏感，训练更稳。

## 正式定义 / 公式
δ = y − Q_θ(s,a)，y 为 TD 目标。
Huber(δ) = { 0.5 δ^2,            |δ|≤1
           { |δ| − 0.5,         |δ|>1
梯度在 |δ| 大时线性增长（不像 MSE 平方爆炸）。

## 最小手算例子
某步 TD 误差 δ=10：MSE 贡献 100；Huber 贡献 9.5——对离群样本惩罚更小，避免单步把网络带偏。

## 对比与常见错误
- 与 MSE：MSE 对离群敏感、易梯度爆炸；Huber 在误差大时更鲁棒。
- 常见错误：把 Huber 当成分类交叉熵——DQN 是回归（拟合 Q 值），用回归损失。

## 闭卷自测
1. DQN 用的是什么损失？为什么用 Huber 而非纯 MSE？
2. Huber 在大小误差时分别是什么形式？
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
