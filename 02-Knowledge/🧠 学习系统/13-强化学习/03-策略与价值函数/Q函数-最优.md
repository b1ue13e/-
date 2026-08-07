---
type: study
topic: "Q函数-最优"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Q函数-最优", "最优动作价值 Q*(s,a)"]
upstream: ["[[Q函数-定义]]"]
tags: [学习, 强化学习]
---

# Q函数-最优

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
和 V* 对应，Q 的最优版本 Q* 在值函数方法中更常用，因为它直接给出"每状态该选哪个动作"。

## 正式定义 / 公式
Q*(s,a) = max_π Q^π(s,a)
满足贝尔曼最优方程：
Q*(s,a) = E[ R + γ max_{a'} Q*(S',a') ]
（见「贝尔曼-Q最优」）

## 最小手算例子
2 状态：Q*(s1,step)=1（唯一动作）。若 s1 有 step/stay，则 Q*(s1,step)=1, Q*(s1,stay)=0。

## 对比与常见错误
- 常见错误：混淆 Q*(s,a) 与 V*(s)。关系：V*(s)=max_a Q*(s,a)（见「VQ关系-最优」）。

## 闭卷自测
1. Q*(s,a) 的定义与最优方程？
2. 如何用 Q* 得到 V*？
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
