---
type: study
topic: "MAB-对比分析"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["MAB", "对比分析"]
upstream: ["[[MAB-EpsilonGreedy]]", "[[MAB-UCB1]]", "[[MAB-TS]]"]
tags: [学习, 强化学习]
---

# MAB-对比分析

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：多臂老虎机
> 前置：[[MAB-EpsilonGreedy]] · [[MAB-UCB1]] · [[MAB-TS]]

## 动机

三种主流 bandit 算法的取舍决定工程选型：实现成本、理论保证、样本效率各不相同。

## 正式定义 / 公式

| 算法 | 探索方式 | 理论遗憾 | 实现难度 | 适用 |
|:---|:---|:---|:---|:---|
| $\varepsilon$-greedy | 均匀随机 | $O(T)$（固定 $\varepsilon$） | 最简 | 基线、调试 |
| UCB1 | 不确定性上界 | $O(\sqrt{T\ln T})$ | 中 | 需理论保证 |
| 汤普森采样 | 后验抽样 | 近 $O(\sqrt{T})$ | 中 | 实践首选 |

## 最小手算例子

- 快速验证：先用 $\varepsilon$-greedy（配衰减）。
- 理论严谨/可解释：UCB1。
- 在线服务/样本贵：汤普森采样。

## 对比与常见错误

- **用固定 $\varepsilon$ 当生产方案**：遗憾线性，长期差。
- **忽视奖励尺度**：UCB/TS 对尺度敏感，先归一化。

## 闭卷自测
- 三算法遗憾量级各是什么？
- 何时优先选汤普森采样？

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
