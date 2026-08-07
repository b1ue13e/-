---
type: study
topic: "Agent定义"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["Agent定义", "核心术语对照"]
tags: [学习, 强化学习]
---

# Agent定义

> 所属模块：[[🧭 阶段1-基础与本质|返回阶段页]] · 主线：核心术语对照
> 主教材：Sutton & Barto 2e, §1.1–1.3

## 动机

强化学习研究"**智能体（Agent）如何通过与环境的试错交互，学会最大化长期收益**"。理解"智能体"是理解整门课的第一个钉子：后面所有概念（状态、动作、策略、价值）都围绕"智能体"与"环境"的交互循环定义。

## 正式定义 / 公式

- **智能体（Agent）**：在环境中**感知状态、做出决策、获取奖励**的学习者/决策者，是我们要训练的对象。
- **环境（Environment）**：Agent 之外、接收动作并返回下一状态与奖励的一切（物理世界、模拟器、游戏引擎）。
- 二者构成**闭环**：Agent 输出动作 $a_t$ → 环境返回 $s_{t+1}, r_{t+1}$ → Agent 据新状态再决策。

## 最小手算例子

下棋 AI：AI 是 Agent，棋盘规则与对手是 Environment。AI 落子（动作）→ 环境返回新棋盘（状态）与胜负/局势评分（奖励）。


量化：以围棋为例，棋盘 19×19=361 个交叉点，Agent 每步要从 361 个合法落子动作中选 1 个，环境返回新棋盘与胜负评分——可见 Agent 面对的动作空间可以极大。
## 对比与常见错误

- **Agent $\neq$ 整个系统**：环境（含对手、物理规律）不在 Agent 内；常有人把"环境"算进 Agent，导致状态/奖励定义混乱。
- **Agent 不一定是人形**：可以是 PID 控制器、推荐系统、交易算法。
- **感知 $\neq$ 完全观测**：Agent 看到的是"观测" $o_t$，未必等于真实状态 $s_t$（部分可观测问题留后）。

## 闭卷自测
- 画出 Agent–Environment 闭环并标注 $s_t,a_t,r_{t+1}$。
- 举一个"环境在 Agent 外"的反例（若把环境算进 Agent 会出什么错）。

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
