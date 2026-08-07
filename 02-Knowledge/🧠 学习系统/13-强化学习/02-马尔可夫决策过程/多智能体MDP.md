---
type: study
topic: "多智能体MDP"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["多智能体", "MARL"]
upstream: ["[[MDP-状态空间]]", "[[MDP-动作空间]]"]
tags: [学习, 强化学习]
---

# 多智能体MDP

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 扩展
> 前置：[[MDP-状态空间]] · [[MDP-动作空间]]

## 动机

多个 Agent 同时决策时，单 Agent 眼中的环境因他人而随机——这是多智能体 RL 的起点。

## 正式定义 / 公式

- **多智能体 MDP（MMDP / Dec-POMDP）**：状态转移依赖**联合动作** $a=(a_1,\dots,a_n)$。
- 关系可分为**合作**（共享回报）、**竞争**（零和）、**混合**。
- 对单个 Agent，他人即环境的一部分，问题变成随机 MDP。

## 最小手算例子

足球 AI：11 个 Agent 联合动作决定球权转移；合作进球、竞争抢断。

## 对比与常见错误

- **假设他人静止**：把对手当固定环境会失败。
- **忽略非平稳性**：对手策略在变，经验可能过期。

## 闭卷自测
- 多智能体 MDP 的转移依赖什么？
- 对单个 Agent 它表现为哪类 MDP？

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
