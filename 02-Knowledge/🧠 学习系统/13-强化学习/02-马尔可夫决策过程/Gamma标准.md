---
type: study
topic: "Gamma标准"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["折扣", "Gamma标准"]
upstream: ["[[MDP-折扣因子]]"]
tags: [学习, 强化学习]
---

# Gamma标准

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：折扣因子 γ
> 前置：[[MDP-折扣因子]]

## 动机

$\gamma\in(0,1)$ 是标准设置；理解"取多大"是调参第一课。

## 正式定义 / 公式

- 典型值 $\gamma=0.9\sim0.99$：在"重视长远"与"保证收敛/低方差"间权衡。
- 越接近 1 越重视长期，但回报方差大、学习更慢更不稳。

## 最小手算例子

Atari 常用 $\gamma=0.99$；机械臂抓取常用 $0.95\sim0.99$；短时任务可用 $0.9$。

## 对比与常见错误

- **过大（≈1）**：方差大、易发散、需更多样本。
- **过小（≈0）**：短视，忽略长程因果（信用分配失败）。

## 闭卷自测
- 标准 $\gamma$ 一般取何范围？依据是什么？
- 如何据任务时长选 $\gamma$？

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```
