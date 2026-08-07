---
type: study
topic: "V函数-定义"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["V函数-定义", "状态价值函数 V^π(s)"]
upstream: ["[[回报定义]]", "[[MDP 与贝尔曼方程]]"]
tags: [学习, 强化学习]
---

# V函数-定义

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
我们怎么判断"某个状态好不好"？最直接：从这一状态出发、按当前策略一直走，未来能拿到的（折扣）回报平均有多少。这就是状态价值函数 V^π(s)。

## 正式定义 / 公式
状态价值函数（state value function）：
V^π(s) = E_π [ G_t | S_t = s ]
即在状态 s 出发、之后始终遵循策略 π 的条件下，回报 G_t 的期望。

## 最小手算例子
2 状态 MDP：s1→（动作 step）→s2（终止），转移概率 1，奖励 R=+1，γ=0.9，s2 终止故 V(s2)=0。
V^π(s1) = E[ R + γ·0 ] = 1 + 0.9·0 = 1。

## 对比与常见错误
- 与 Q 函数：V 只看状态，Q 同时看状态-动作对。
- 常见错误：漏掉"条件于 π"——V 的值依赖于所用策略，换策略值就变（记为 V^π）。

## 闭卷自测
1. V^π(s) 的定义与含义？
2. 为什么 V 要标注上标 π？
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
