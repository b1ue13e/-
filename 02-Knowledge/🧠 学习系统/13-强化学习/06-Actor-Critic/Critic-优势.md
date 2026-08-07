---
type: study
topic: "Critic-优势"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Critic-优势", "Critic 提供优势"]
upstream: ["[[Critic-结构]]", "[[优势-定义]]"]
tags: [学习, 强化学习]
---

# Critic-优势

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
Critic 的核心产物是"优势"——actor 据此更新。

## 正式定义 / 公式
一步优势：A(s,a) ≈ r + γ V(s') − V(s)（critic 的 TD 误差）
多步/GAE：见「优势-n步」「优势-GAE」。
Critic 把轨迹信息压缩成每步优势，喂给 actor。

## 最小手算例子
<!-- NUMEX2 -->Critic 估 V 或 Q。Advantage A(s,a)=Q(s,a)−V(s)。离散例：V=0.5，两动作 Q=[0.7,0.3] ⇒ A=[+0.2,−0.2]（相对平均的优劣方向）。

单步 (s,a,r,s')：critic 算 δ=r+γV(s')−V(s)，即为该步优势，直接用于 actor 更新。

## 对比与常见错误
- 与固定基线：critic 提供"状态相关"基线，比常数更优（见「基线-状态价值」）。
- 常见错误：把 critic 输出的 V 直接当优势——需做 A=…−V 的差值。

## 闭卷自测
1. critic 给 actor 的是什么信号？
2. 一步优势如何由 critic 得到？
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
