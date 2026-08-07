---
type: study
topic: "IS-比率"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["IS-比率", "重要性权重"]
upstream: ["[[IS-含义]]", "[[策略梯度]]"]
tags: [学习, 强化学习]
---

# IS-比率

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
把 IS 用到策略梯度上时，需要具体的比率表达式。

## 正式定义 / 公式
单步动作比率：
ρ_t = π_θ(a_t|s_t) / μ(a_t|s_t)
整条轨迹比率是各步乘积：ρ(τ) = Π_t π_θ(a_t|s_t)/μ(a_t|s_t)。
比率衡量目标策略与行为策略在同一状态-动作上的概率差异。

## 最小手算例子
μ 下 a 概率 0.2，π 下 0.4 → ρ=2，意味着该样本在 π 下重要性加倍。

## 对比与常见错误
- 与 IS-含义：比率就是密度比 p/q 在策略上的实例化。
- 常见错误：把单步比率当轨迹比率——长轨迹的乘积会让权重指数漂移。

## 闭卷自测
1. 重要性比率 ρ_t 怎么算？
2. 轨迹比率与单步比率的关系？
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
