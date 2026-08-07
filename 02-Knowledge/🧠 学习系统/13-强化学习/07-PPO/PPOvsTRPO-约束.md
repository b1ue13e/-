---
type: study
topic: "PPOvsTRPO-约束"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PPOvsTRPO-约束", "PPO 与 TRPO 约束对比"]
upstream: ["[[TRPO-信任区域]]", "[[PPOClip-目标]]"]
tags: [学习, 强化学习]
---

# PPOvsTRPO-约束

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
PPO 与 TRPO 都追求"限制更新步幅"，但约束方式完全不同。

## 正式定义 / 公式
- TRPO：硬约束  KL(π_old‖π) ≤ δ，用共轭梯度在约束下求最优步；
- PPO：软约束  通过 clip 概率比率间接限制步幅，无显式 KL 限制。
二者目标一致——保证单调改进、避免崩溃。

## 最小手算例子
<!-- NUMEX2 -->约束形式：TRPO 硬约束 KL≤δ；PPO 用 L^CLIP=min(r·A, clip(r,1−ε,1+ε)·A) 软约束，超出部分梯度截断。

TRPO 每步需解一个带 KL 约束的子问题；PPO 只需在 minibatch 上做若干次 SGD。

## 对比与常见错误
- 与 PPOClip：PPO 用 clip 近似 TRPO 的信任区域。
- 常见错误：认为 PPO 完全不用 KL——带 KL 惩罚的变体（PPO-penalty）也常用。

## 闭卷自测
1. PPO 与 TRPO 如何分别限制步幅？
2. 为何说 PPO 是 TRPO 的一阶近似？
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
