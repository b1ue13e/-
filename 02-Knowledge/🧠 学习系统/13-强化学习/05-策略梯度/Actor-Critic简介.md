---
title: "Actor-Critic 简介"
type: study
topic: "Actor-Critic 简介"
course: 强化学习
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
upstream: ["[[策略梯度定理与REINFORCE]]", "[[优势函数]]", "[[基线方法]]"]
tags: [学习, 强化学习, Actor-Critic, 策略梯度]
---

# Actor-Critic 简介

> **⏱ 预计耗时**：20–30 分钟
> **🎯 行为目标**：完成本卡后，
> - 说出 Actor-Critic 的核心思想；
> - 写出 critic 给出的优势与单步更新流程；
> - 对比 AC 与 REINFORCE 的方差/偏差特征。

## 0. 学习边界
- **类别**：**A 类（核心概念，必须深挖）**——Actor-Critic 是"带 critic 基线的策略梯度"，把 MC 回报换成在线 bootstrap 优势，是阶段6的主角。

---

## 1. 核心思想（AC简介）
策略梯度用 MC 回报方差大；若用"评论家" V 在线估计优势，就能低方差、在线更新——这就是 Actor-Critic。
- Actor（策略 π_θ）产出动作；Critic（价值 V_φ）评估状态/动作，提供优势 A ≈ r + γV(s′) − V(s)。
- 策略梯度用 critic 给的优势更新，无需等幕末。

## 2. 更新流程 + 手算
每步：actor 选 a，环境给 r、s′；critic 算 TD 误差 δ = r + γV(s′) − V(s) 作优势；actor 用 δ·∇logπ 更新，critic 用 δ 更新 V。
**手算**：Q(s,a)=0.7, V(s)=0.5 ⇒ A=+0.2（该动作优于平均），actor 沿 +A·∇lnπ 更新。

## 3. 与 REINFORCE / 值方法对比
- 与 REINFORCE：AC 用 bootstrap 优势（低方差、在线）；REINFORCE 用 MC 回报（无偏、高方差）。
- 本质：AC 是"带 critic 基线的策略梯度"，不是全新算法。
- 常见错误：把 AC 当成"全新算法"——本质即带 critic 基线的策略梯度。

## 4. 闭卷自测
1. Actor-Critic 的核心思想？
2. 它相对 REINFORCE 的方差/偏差特征？
3. 优势 A 如何由 critic 给出？

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
