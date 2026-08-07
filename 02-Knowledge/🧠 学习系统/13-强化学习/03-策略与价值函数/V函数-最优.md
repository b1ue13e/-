---
type: study
topic: "V函数-最优"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["V函数-最优", "最优状态价值 V*(s)"]
upstream: ["[[V函数-定义]]"]
tags: [学习, 强化学习]
---

# V函数-最优

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
我们最终想要"最好的"策略，对应"最好的"价值函数——最优状态价值函数 V*。

## 正式定义 / 公式
V*(s) = max_π V^π(s) = max_π E_π[G_t | S_t=s]
即对所有策略取最大。它满足贝尔曼最优方程（见「贝尔曼-V最优」）。

## 最小手算例子
上面 2 状态 MDP 只有一种非终止策略，V*(s1)=1。若 s1 还有动作"停留"拿 0，则最优仍取 step，V*(s1)=1。

## 对比与常见错误
- 常见错误：认为 V*(s) 依赖某个具体策略——V* 是"跨所有策略"的最大值，本身不直接对应单一可执行策略（需配合 Q* 取贪心得到 π*）。

## 闭卷自测
1. V*(s) 的定义？
2. V* 与具体策略 π 的关系？
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
