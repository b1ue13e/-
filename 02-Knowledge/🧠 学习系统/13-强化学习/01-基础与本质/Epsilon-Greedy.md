---
type: study
topic: "Epsilon-Greedy"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["Epsilon-Greedy", "探索策略"]
upstream: ["[[探索与利用]]"]
tags: [学习, 强化学习]
---

# Epsilon-Greedy

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：探索策略
> 前置：[[探索与利用]]

## 动机

最朴素也最常用的探索策略：以概率 $\varepsilon$ 随机、其余贪心。是理解"探索如何落地"的入口。

## 正式定义 / 公式

- 每一步：以 $\varepsilon$ 均匀随机选动作；以 $1-\varepsilon$ 选当前估值最高 $\arg\max_a \hat Q(a)$。
- 期望每步以 $\varepsilon$ 概率在"探索"。

## 最小手算例子

$\varepsilon=0.1$：90% 时间拉已知最好臂，10% 时间随便试一台，避免错过更好的。

## 对比与常见错误

- **$\varepsilon$ 太大**：几乎纯随机，学得太慢。
- **$\varepsilon$ 太小**：陷在次优臂（贪心陷阱）。
- **固定 $\varepsilon$ 不衰减**：后期仍过度探索，遗憾线性增长。

## 闭卷自测
- 写出 $\varepsilon$-greedy 的选择规则。
- 为何固定 $\varepsilon$ 的累计遗憾是 $O(T)$ 而非次线性？

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
