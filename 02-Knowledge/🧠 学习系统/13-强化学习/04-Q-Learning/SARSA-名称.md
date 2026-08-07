---
type: study
topic: "SARSA-名称"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["SARSA-名称", "SARSA 名字由来"]
upstream: ["[[Q函数-定义]]"]
tags: [学习, 强化学习]
---

# SARSA-名称

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
SARSA 是经典 On-Policy TD 控制算法。名字来自它用的五元组 (S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1}) —— 状态、动作、奖励、下一状态、下一动作。

## 正式定义 / 公式
缩写 State-Action-Reward-State-Action，对应一次转移中依次出现的五个量：
(S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1})
更新目标用"下一动作 A_{t+1}"（由同一行为策略选出）。

## 最小手算例子
在 s1 用 ε-greedy 选 a=right，得 r=+1、s2；再用同策略选 a'=right。五元组 (s1,right,+1,s2,right) 即 SARSA 所用。

## 对比与常见错误
- 常见错误：把 SARSA 名字当成某人缩写——它直接来自五元组顺序。

## 闭卷自测
1. SARSA 名字代表哪五个量？
2. 为什么强调"同一策略"选 A_{t+1}？
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
