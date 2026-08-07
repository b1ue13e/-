---
type: study
topic: "Epsilon衰减"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["Epsilon衰减", "探索衰减"]
upstream: ["[[Epsilon-Greedy]]"]
tags: [学习, 强化学习]
---

# Epsilon衰减

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：探索策略
> 前置：[[Epsilon-Greedy]]

## 动机

固定 $\varepsilon$ 在训练后期仍浪费探索。衰减让 Agent "先广撒网、后精耕"，提升收敛质量。

## 正式定义 / 公式

- **衰减调度**：$\varepsilon_t=\max(\varepsilon_{\min},\, \varepsilon_0\cdot \gamma^t)$ 或 $\varepsilon_t=\varepsilon_0/(1+kt)$。
- 早期高 $\varepsilon$ 充分探索，后期趋近于 $\varepsilon_{\min}$ 专注利用。

## 最小手算例子

$\varepsilon_0=1.0,\gamma=0.99$：第 1 步全随机，第 100 步约 $0.37$，第 500 步约 $0.0066$，基本只利用。

## 对比与常见错误

- **衰减过快**：还没探索够就几乎不试，错过最优臂。
- **衰减过慢**：后期仍在随机，方差大、难收敛。
- **与 $\varepsilon$-greedy 混用错配**：衰减应作用于同一个 $\varepsilon$ 参数。

## 闭卷自测
- 给出两种常见 $\varepsilon$ 衰减公式。
- 衰减过快的主要风险？

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
