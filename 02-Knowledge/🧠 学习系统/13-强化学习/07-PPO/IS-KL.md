---
type: study
topic: "IS-KL"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["IS-KL", "策略间 KL 散度"]
upstream: ["[[IS-目标]]", "[[策略梯度]]"]
tags: [学习, 强化学习]
---

# IS-KL

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
直接用比率做 off-policy 容易失控，需要一种"距离"来约束两策略别差太远。

## 正式定义 / 公式
KL 散度（对动作分布）：
KL(π_θ ‖ μ) = E_{a~π_θ}[ log π_θ(a|s) − log μ(a|s) ]
它衡量 π 相对 μ 的平均对数概率差，非负但不对称。

## 最小手算例子
两伯努利策略 p=(0.5,0.5)、q=(0.9,0.1) → KL(p‖q)≈0.37，反向更大。

## 对比与常见错误
- 与 IS-比率：KL 用对数差，比率用比值；都描述策略距离。
- 常见错误：以为 KL 对称——KL(p‖q)≠KL(q‖p)。

## 闭卷自测
1. 策略间 KL 散度如何定义？
2. 为何说 KL 不对称？
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
