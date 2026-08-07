---
type: study
topic: "AC简介"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["AC简介", "Actor-Critic 简介"]
upstream: ["[[PG-梯度]]", "[[V函数-定义]]"]
tags: [学习, 强化学习]
---

# AC简介

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
策略梯度用 MC 回报方差大；若用一个"评论家" V 在线估计优势，就能低方差、在线更新——这就是 Actor-Critic 思想（详见阶段6）。

## 正式定义 / 公式
Actor（策略 π_θ）产出动作；Critic（价值 V_φ）评估状态/动作，提供优势 A≈r+γV(s')−V(s)。
策略梯度用 critic 给的优势更新，无需等幕末。

## 最小手算例子
<!-- NUMEX2 -->AC 同时学策略 π(a|s) 与价值 V(s)。优势 A=Q−V：若 Q(s,a)=0.7, V(s)=0.5 ⇒ A=+0.2（该动作优于平均），actor 沿 +A·∇lnπ 更新。

每步：actor 选 a，环境给 r、s'；critic 算 TD 误差 δ=r+γV(s')−V(s) 作优势；actor 用 δ·∇log π 更新，critic 用 δ 更新 V。

## 对比与常见错误
- 与 REINFORCE：AC 用 bootstrap 优势（低方差、在线）；REINFORCE 用 MC 回报（无偏、高方差）。
- 常见错误：把 AC 当成"全新算法"——它本质是"带 critic 基线的策略梯度"。

## 闭卷自测
1. Actor-Critic 的核心思想？
2. 它相对 REINFORCE 的方差/偏差特征？
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
