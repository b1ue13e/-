---
type: study
topic: "Critic-职责"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Critic-职责", "Critic 的职责"]
upstream: ["[[V函数-定义]]", "[[基线-状态价值]]"]
tags: [学习, 强化学习]
---

# Critic-职责

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
Critic 是"评论家"：估计价值函数，给 actor 提供低方差的优势信号。

## 正式定义 / 公式
Critic 近似 V_φ(s)（或 Q）作为基线/优势：
A(s,a) ≈ r + γ V_φ(s') − V_φ(s)
它把"回报"换成"一步自举优势"，降低 actor 更新方差。

## 最小手算例子
actor 在 s 选 a 得 r=+1、s'；critic 给 V(s)=0.4、V(s')=0.5：A=1+0.9·0.5−0.4=1.05。

## 对比与常见错误
- 与 actor：critic 不直接出动作，只评价值。
- 常见错误：把 critic 当"真值"——V_φ 是估计，有误差，故优势有偏。

## 闭卷自测
1. Critic 在 AC 中负责什么？
2. 它如何帮 actor 降方差？
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
