---
type: study
topic: "PPOvsTRPO-效果"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PPOvsTRPO-效果", "PPO 与 TRPO 最终效果"]
upstream: ["[[PPOvsTRPO-约束]]"]
tags: [学习, 强化学习]
---

# PPOvsTRPO-效果

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
效果层面，更简单的 PPO 是否真的不如复杂的 TRPO？

## 正式定义 / 公式
大量实证表明：PPO（裁剪版）在多数连续控制与 Atari 任务上达到或超越 TRPO，且调参更友好、更稳定。

## 最小手算例子
<!-- NUMEX2 -->效果：Atari/连续控制基准上 PPO 与 TRPO 最终性能相当，PPO 方差更小、调参更省；TRPO 理论单调保证更强但收益有限。

MuJoCo 基准：PPO 与 TRPO 最终回报接近，PPO 曲线更平滑、超参更鲁棒。

## 对比与常见错误
- 与 PPOvsTRPO-实现：简单带来可复现性优势。
- 常见错误：盲目相信"理论上更严格就更好"——工程效果常反超。

## 闭卷自测
1. PPO 与 TRPO 在最终效果上谁更好？
2. PPO 为何更受工业界欢迎？
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
