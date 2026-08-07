---
type: study
topic: "MAB-EpsilonGreedy"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["MAB", "Epsilon-Greedy"]
upstream: ["[[MAB-问题定义]]", "[[Epsilon-Greedy]]"]
tags: [学习, 强化学习]
---

# MAB-EpsilonGreedy

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：多臂老虎机
> 前置：[[MAB-问题定义]] · [[Epsilon-Greedy]]

## 动机

把 $\varepsilon$-greedy 落到老虎机场景：用样本均值估价值，再用 $\varepsilon$-greedy 选臂。

## 正式定义 / 公式

1. 初始化 $\hat Q(a)=0,\,N(a)=0$。
2. 每步以 $\varepsilon$ 随机选臂，否则选 $\arg\max_a\hat Q(a)$。
3. 观测 $R$，用增量式更新 $\hat Q(a)$ 与 $N(a)$。

## 最小手算例子

10 臂问题，运行数千步后 $\varepsilon=0.1$ 的累计奖励明显高于纯贪心（因贪心可能卡在初始侥幸高的臂）。

## 对比与常见错误

- **与乐观初始化混淆**：$\varepsilon$-greedy 靠随机探索；乐观初值靠"先当最好"驱动探索，二者可叠加但概念不同。
- **$\varepsilon$ 不衰减**：见 [[Epsilon衰减]]。

## 闭卷自测
- 口述 MAB-$\varepsilon$-greedy 的 3 步流程。
- 它相比纯贪心为何 regret 更低？

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
