---
type: study
topic: "Critic-结构"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Critic-结构", "Critic 网络结构"]
upstream: ["[[Critic-职责]]", "[[V函数-公式]]"]
tags: [学习, 强化学习]
---

# Critic-结构

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
Critic 通常也是神经网络：输入状态、输出标量价值 V。

## 正式定义 / 公式
V_φ(s) ∈ ℝ，一个回归头。也可估 Q（QAC 用 Q，见「QAC」）。
结构常比 actor 简单（只需标量输出）。

## 最小手算例子
CartPole：critic 为 MLP，输入 4 维状态，输出 1 个 V 值。

## 对比与常见错误
- 与 actor 结构：输出维度不同（1 vs |A| 或分布参数）。
- 常见错误：让 critic 输出"动作维度"却当 V 用——需明确是 V 还是 Q。

## 闭卷自测
1. critic 网络输入/输出？
2. V-critic 与 Q-critic 结构差异？
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
