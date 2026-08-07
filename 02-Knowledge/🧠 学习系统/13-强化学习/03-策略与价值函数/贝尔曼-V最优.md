---
type: study
topic: "贝尔曼-V最优"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["贝尔曼-V最优", "贝尔曼最优方程（V）"]
upstream: ["[[V函数-最优]]", "[[贝尔曼-V期望]]"]
tags: [学习, 强化学习]
---

# 贝尔曼-V最优

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
最优价值 V* 也满足一个方程——贝尔曼最优方程，是值迭代、Q-learning 的理论根。

## 正式定义 / 公式
V*(s) = max_a Σ_{s'} P(s'|s,a) [ R(s,a,s') + γ V*(s') ]
对动作取最大（而不是按策略加权）。

## 最小手算例子
2 状态：V*(s1)=max_{step,stay} [1+0.9·0, 0+0.9·0] = max(1,0)=1。✓

## 对比与常见错误
- 常见错误：在最优方程里仍写 Σ_a π(a|s)——最优方程没有具体策略，直接 max。

## 闭卷自测
1. 默写贝尔曼最优方程（V）。
2. 最优方程与期望方程的关键差异？
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
