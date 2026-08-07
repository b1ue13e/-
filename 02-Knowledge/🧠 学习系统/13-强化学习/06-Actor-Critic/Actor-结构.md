---
type: study
topic: "Actor-结构"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Actor-结构", "Actor 网络结构"]
upstream: ["[[Actor-职责]]", "[[参数化-神经网络]]"]
tags: [学习, 强化学习]
---

# Actor-结构

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
actor 通常是一个神经网络：输入状态、输出动作分布参数。

## 正式定义 / 公式
离散：网络输出 logits → softmax 得 π_θ(a|s)。
连续：网络输出 (μ, log σ) → 高斯 π_θ(a|s)=𝒩(μ,σ)。
结构即普通策略网络（同「参数化-神经网络」）。

## 最小手算例子
CartPole：actor 为 2 层 MLP，输入 4 维状态，输出 2 维 logits。

## 对比与常见错误
- 与 critic 结构：actor 输出"分布"，critic 输出"标量价值"，结构不同。
- 常见错误：actor 与 critic 共享底层却未小心初始化——可能互相拖累（可共享也可独立）。

## 闭卷自测
1. actor 网络输入/输出是什么？
2. 离散与连续动作的输出形式？
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
