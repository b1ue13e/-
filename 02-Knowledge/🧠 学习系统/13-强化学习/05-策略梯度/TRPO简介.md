---
type: study
topic: "TRPO简介"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO简介", "TRPO 简介"]
upstream: ["[[NPG]]", "[[PG-梯度]]"]
tags: [学习, 强化学习]
---

# TRPO简介

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
NPG 需算大 Fisher 矩阵求逆，昂贵。TRPO 用"信任域 + KL 约束"在近似下获得同样好处，且实现更可行。

## 正式定义 / 公式
TRPO 求解：
max_θ E[ (π_θ/π_old) · A ]   受限于   KL(π_old || π_θ) ≤ δ
用共轭梯度近似自然梯度、线性搜索满足 KL 约束，限制单步策略变化幅度。

## 最小手算例子

每步先算优势与旧策略，更新后检查 KL 是否超 δ；超了就缩小步长，防止策略崩溃（呼应「REINFORCE-不稳定」）。


量化：典型 KL 步长上限 δ=0.01（常用 0.01–0.02）。若新策略相对旧策略 KL(π_new‖π_old)=0.03>δ，就把步长折半重算，保证不越过信任域、防止策略崩溃。
## 对比与常见错误
- 与 PPO：PPO 用 clipped 目标近似同一思想，更简单（详见阶段7）。
- 常见错误：以为 TRPO 是"无约束二阶"——KL 约束正是它稳定与可行的关键。

## 闭卷自测
1. TRPO 优化什么问题、加什么约束？
2. 它与 PPO 的关系？
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
