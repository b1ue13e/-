---
type: study
topic: "PPO家族"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PPO家族", "PPO 家族"]
upstream: ["[[TRPO家族]]", "[[TRPO简介]]", "[[Actor-Critic架构]]"]
tags: [学习, 强化学习]
---

# PPO家族

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
PPO（Proximal Policy Optimization）是 TRPO 的实用近似：用裁剪目标限制更新幅度，简单高效，是现代默认。

## 正式定义 / 公式
裁剪代理目标：
L^{CLIP} = E[ min( ρ_t A_t, clip(ρ_t,1−ε,1+ε) A_t ) ]，ρ_t = π_θ/π_old
超出比例 [1−ε,1+ε] 的优势被裁掉，近似 KL 约束（详见阶段7）。

## 最小手算例子
ρ_t=1.2, ε=0.2, A_t=+1：clip 到 1.2→1.2 仍在 [0.8,1.2]，计入 1.2·1；若 ρ=1.5 则裁到 1.2。

## 对比与常见错误
- 与 TRPO：PPO 用 clip 近似信任域，省 CG/线搜。
- 常见错误：以为 PPO 无约束——clip 正是对更新幅度的隐式约束。

## 闭卷自测
1. PPO 的裁剪目标是什么？
2. PPO 与 TRPO 的关系？
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
