---
type: study
topic: "DQN-TN详解"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DQN-TN详解", "目标网络详解"]
upstream: ["[[DQN-目标网络]]"]
tags: [学习, 强化学习]
---

# DQN-TN详解

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
目标网络是 DQN 稳定训练的核心技巧，细节（同步频率/方式）影响收敛质量。

## 正式定义 / 公式
硬更新：每 C 步 θ^- ← θ；软更新（Polyak）：θ^- ← τθ + (1−τ)θ^-，τ 很小（如 0.001），每步微调。
动机：让 TD 目标 y 在一段时间内"冻结"，减少非平稳性。

## 最小手算例子
Atari DQN 原论文：硬更新每 10000 步同步一次；现代实现多用软更新（如 DDPG/TD3 的 τ=0.005）。

## 对比与常见错误
- 与"无目标网络"：无则目标随 θ 实时漂移，Q 值易振荡/发散。
- 常见错误：硬更新间隔过长使 θ^- 严重滞后、训练偏慢；过短近似无效果。

## 闭卷自测
1. 硬更新与软更新的权衡？
2. 目标网络为何能稳定训练？
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
