---
type: study
topic: "PG-似然比"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PG-似然比", "似然比技巧 score function"]
upstream: ["[[PG-目标函数]]", "[[策略-参数化]]"]
tags: [学习, 强化学习]
---

# PG-似然比

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
策略往往只能采样、不能求梯度（如离散/连续分布）。似然比技巧（score function）让我们用 ∇log π 得到对参数 θ 的梯度，而不需要知道环境动态。

## 正式定义 / 公式
∇_θ π_θ(a|s) = π_θ(a|s) · ∇_θ log π_θ(a|s)
故 ∇_θ E[f(a)] = E[ f(a) · ∇_θ log π_θ(a) ]
把 f 取为带权回报，即得策略梯度（见「PG-梯度」）。

## 最小手算例子
softmax π_θ(a1)=σ(θ)：∇_θ log π(a1)=1−σ(θ)。梯度方向由"当前概率的余项"给出，自动适配分布形状。

## 对比与常见错误
- 常见错误：忘记乘 π 本身——∇log π 已含"除以 π"的效果，公式里不再显式出现 π（被约掉）。
- 与自动微分：现代框架直接对 log π·优势 做反向传播，正是此技巧的工程实现。

## 闭卷自测
1. 似然比技巧的核心等式？
2. 为什么它不需要环境模型？
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
