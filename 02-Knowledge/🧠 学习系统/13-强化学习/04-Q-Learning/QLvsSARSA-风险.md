---
type: study
topic: "QLvsSARSA-风险"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["QLvsSARSA-风险", "Q-Learning vs SARSA：风险偏好"]
upstream: ["[[QLvsSARSA-策略]]", "[[QLvsSARSA-目标]]"]
tags: [学习, 强化学习]
---

# QLvsSARSA-风险

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
因为有/无探索的"目标"不同，两者面对危险（如悬崖）时表现迥异。

## 正式定义 / 公式
- Q-learning（off-policy）：学最优 Q*，目标恒取 max——"乐观"，可能选贴边的高回报高风险动作。
- SARSA（on-policy）：目标含行为策略的探索，会把"探索误入危险"的代价算进去——"保守"，主动绕开危险区。

## 最小手算例子
<!-- NUMEX2 -->风险敏感度：SARSA 将探索噪声纳入更新→对危险状态更保守；Q-learning 只盯最优→训练早期易因偶然成功而冒险。安全关键场景倾向 SARSA 或受约束 Q-learning。

悬崖行走：Q-learning 学到贴边直走（最短、但一步踏空即死）；SARSA 学到离悬崖一格走（略长但稳）。在线（边学边用）时 SARSA 往往活得更久。

## 对比与常见错误
- 常见错误：认为 Q-learning "一定更好"——在训练期就要实际执行（online）且有致命危险时，SARSA 更安全。

## 闭卷自测
1. 为何 SARSA 更"保守"？
2. 何时 Q-learning 的风险偏好反而是缺点？
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
