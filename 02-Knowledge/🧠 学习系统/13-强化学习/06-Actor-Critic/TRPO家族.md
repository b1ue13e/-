---
type: study
topic: "TRPO家族"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO家族", "TRPO 家族总览"]
upstream: ["[[TRPO-信任区域]]", "[[TRPO-CG]]"]
tags: [学习, 强化学习]
---

# TRPO家族

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
TRPO 是一族"信任域策略优化"方法的代表，理解其谱系有助于衔接 PPO。

## 正式定义 / 公式
谱系：自然梯度(NPG) → TRPO(约束优化+CG) → PPO(clip 近似，见阶段7)。
共同点：限制单步策略变化、用优势做更新。

## 最小手算例子
<!-- NUMEX2 -->TRPO 家族：原版 TRPO（CG+线搜）、PPO-Clip（裁剪替代约束）、PPO-Penalty（KL 惩罚）。共同点：限制策略更新幅度，避免破坏式大步。

同一任务可先试 TRPO，再换 PPO（实现更简单、效果相近）。

## 对比与常见错误
- 与 PPO：PPO 用裁剪目标近似 KL 约束，省去 CG/线搜。
- 常见错误：把 TRPO 与 PPO 当完全不同路线——PPO 是 TRPO 的实用近似。

## 闭卷自测
1. TRPO 家族包含哪些方法？
2. TRPO 与 PPO 的关系？
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
