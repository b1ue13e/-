---
type: study
topic: "PPOvsTRPO-效率"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PPOvsTRPO-效率", "PPO 与 TRPO 样本/计算效率"]
upstream: ["[[PPOvsTRPO-约束]]"]
tags: [学习, 强化学习]
---

# PPOvsTRPO-效率

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
从计算与样本两个角度看两种算法的性价比。

## 正式定义 / 公式
- 计算效率：PPO 每步只需前向/反向 + SGD；TRPO 额外做 CG 迭代，单次更新更贵。
- 样本效率：二者都复用 on-policy 多轮更新（PPO 的 K epoch），相当接近。

## 最小手算例子
<!-- NUMEX2 -->效率：PPO 复用一批数据 K=4–10 轮更新；TRPO 每批也多次 CG 但更贵。PPO 墙钟时间通常更短。

同一 GPU，PPO 每秒可处理更多更新批次。

## 对比与常见错误
- 与 PPOvsTRPO-实现：计算效率源于实现差异。
- 常见错误：把"计算更快"等同于"样本更少"——样本效率主要看数据复用。

## 闭卷自测
1. PPO 在计算效率上为何占优？
2. 样本效率上二者关系如何？
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
