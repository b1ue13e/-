---
type: study
topic: "A2C-简单"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A2C-简单", "A2C 基本流程"]
upstream: ["[[A2C家族]]"]
tags: [学习, 强化学习]
---

# A2C-简单

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
最简 A2C：单（或少量）环境的 AC 循环。

## 正式定义 / 公式
循环：用当前策略交互若干步 → 用优势更新 actor/critic → 重复。
即「Actor-Critic架构」的基本在线版。

## 最小手算例子
<!-- NUMEX -->优势 A=G−V：某步回报 G=5、价值 V(s)=3 ⇒ A=+2（正向，应增强该动作）；若 V(s)=5 ⇒ A=0（与平均持平，不应调整）。

每收集 T 步：(s,a,r,s') 算 TD/GAE 优势，更新 θ、φ，继续。

## 对比与常见错误
- 与完整 A2C：简单版不一定多 worker 批量；完整版强调并行批量。
- 常见错误：以为简单版不用优势——AC 核心仍是优势更新。

## 闭卷自测
1. 简单 A2C 的流程？
2. 它与完整 A2C 的差异？
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
