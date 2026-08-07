---
type: study
topic: "TRPO对比-步长"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO对比-步长", "TRPO 对比：步长选择"]
upstream: ["[[TRPO家族]]", "[[TRPO-KL]]"]
tags: [学习, 强化学习]
---

# TRPO对比-步长

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
TRPO 用 KL 阈值 δ 控制步长，比手动调学习率更稳，但 δ 本身也要调。

## 正式定义 / 公式
TRPO 步长≈由 δ 隐式决定（满足 KL≤δ 的最大步）；
PPO 用 clip 范围 ε 间接控步长。两者都试图"自动"限制更新幅度。

## 最小手算例子
<!-- NUMEX2 -->步长控制：TRPO 用 KL 硬约束 KL≤δ=0.01 并线搜保证不越界；PPO 用 ε=0.2 软裁剪，步长更宽松、实现更简单。

δ 太大→近似失效、不稳定；δ 太小→学习慢。需在信任域框架下调 δ。

## 对比与常见错误
- 常见错误：以为 TRPO "不用调步长"——δ 就是它的步长超参。

## 闭卷自测
1. TRPO 如何控制步长？
2. δ 过大/过小的影响？
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
