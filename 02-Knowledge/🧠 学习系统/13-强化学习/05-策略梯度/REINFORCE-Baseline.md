---
type: study
topic: "REINFORCE-Baseline"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["REINFORCE-Baseline", "REINFORCE 基线减方差"]
upstream: ["[[REINFORCE-高方差]]", "[[基线-状态价值]]"]
tags: [学习, 强化学习]
---

# REINFORCE-Baseline

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
在不引入偏差的前提下大幅降低 REINFORCE 方差：减去一个与动作无关的基线 b(s_t)。

## 正式定义 / 公式
∇_θ J ≈ E[ Σ_t ∇_θ log π_θ(a_t|s_t) · (G_t − b(s_t)) ]
若 b(s_t) 与 a_t 独立，则 E[∇log π · b] = 0，梯度仍无偏；方差因 (G_t−b) 更小而下降。
常用基线：常数（平均回报）或状态价值 V_φ(s)（critic）。

## 最小手算例子
b(s)=0.3 为常数，G_t=1：权重由 1 变 0.7，缩小幅值；期望不变（因 b 与动作独立）。

## 对比与常见错误
- 与优势：当 b=V(s_t)，(G_t−V) 即优势 A_t 的 MC 估计（见「优势-估计」）。
- 常见错误：让基线依赖 a_t——会引入偏差，破坏无偏性。

## 闭卷自测
1. 基线为什么能降方差且不引入偏差？
2. 基线能否依赖动作？
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
