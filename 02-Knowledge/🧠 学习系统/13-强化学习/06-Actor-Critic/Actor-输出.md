---
type: study
topic: "Actor-输出"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Actor-输出", "Actor 输出层"]
upstream: ["[[Actor-结构]]", "[[策略-参数化]]"]
tags: [学习, 强化学习]
---

# Actor-输出

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
输出层决定动作如何被采样；这是 actor 与环境的接口。

## 正式定义 / 公式
离散：softmax(logits) → 按概率采样动作。
连续：从 𝒩(μ,σ) 采样（reparameterization：a=μ+σ·ε）。
输出经采样得到实际执行的 a。

## 最小手算例子
logits=(2,0) → π≈(0.88,0.12)；采样大概率取 a1；训练时仍按分布采以保持可微。

## 对比与常见错误
- 常见错误：部署/训练都 argmax——训练需采样保探索与可微（见「参数化-连续」）。

## 闭卷自测
1. actor 输出层在两种动作空间下分别是什么？
2. 为何训练时采样而非 argmax？
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
