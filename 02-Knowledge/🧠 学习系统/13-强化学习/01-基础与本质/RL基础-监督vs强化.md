---
type: study
topic: "RL基础-监督vs强化"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["RL基础", "监督学习", "无监督学习"]
upstream: ["[[RL基础-序列决策]]"]
tags: [学习, 强化学习]
---

# RL基础-监督vs强化

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：RL概览

## 动机

建立 RL 在机器学习版图中的定位，避免把它当"带奖励的监督学习"误用。

## 正式定义 / 公式

| 维度 | 监督学习 | 无监督学习 | 强化学习 |
|:---|:---|:---|:---|
| 数据 | 带标签 $(x,y)$ | 无标签 $x$ | 交互轨迹 $(s,a,r,s')$ |
| 信号 | 即时正确/错误 | 无显式信号 | 延迟、稀疏奖励 |
| 目标 | 拟合 $P(y\mid x)$ | 发现结构 | 最大化长期回报 |
| 决策 | 独立预测 | — | 序列依赖决策 |

## 最小手算例子

图像分类：给图贴标签（监督）。聚类：无标签分组（无监督）。Agent 学走路：每步动作影响后续，只有到达终点才给奖励（RL）。


量化：一条 100 步的轨迹往往只在终点拿 1 个稀疏奖励，而监督学习每条样本都有 1 个即时标签；奖励的稀疏 + 延迟正是 RL 信用分配更难的根源。
## 对比与常见错误

- **把 RL 当监督**：用专家轨迹直接监督可能退化成模仿学习，失去探索最优的能力。
- **奖励延迟误判**：监督的"即时误差"直觉在 RL 中失效，需信用分配（credit assignment）。

## 闭卷自测
- 监督与 RL 在"信号时机"和"决策依赖"上两点根本区别？
- 模仿学习为何不等同于 RL？

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
