---
type: study
topic: "贝尔曼-V期望"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["贝尔曼-V期望", "贝尔曼期望方程（V）"]
upstream: ["[[V函数-公式]]"]
tags: [学习, 强化学习]
---

# 贝尔曼-V期望

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
V^π(s) 的递归形式能否写成一个统一方程？这就是贝尔曼期望方程——它把"一步转移"和"剩余价值"连起来，是 DP/TD 的理论基础。

## 正式定义 / 公式
V^π(s) = Σ_a π(a|s) Σ_{s'} P(s'|s,a) [ R(s,a,s') + γ V^π(s') ]
对动作按策略加权，对下一状态按转移加权，取"奖励+折扣后续价值"的期望。

## 最小手算例子
2 状态 MDP：V(s1)=1·1·[1+0.9·V(s2)]=1+0.9·0=1。✓（与「V函数-定义」一致）

## 对比与常见错误
- 常见错误：把 V^π(s') 写成 V*(s')——期望方程用的是当前策略的 V^π，不是最优 V*。

## 闭卷自测
1. 默写贝尔曼期望方程（V）。
2. 方程里"期望"对哪些随机变量取？
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
