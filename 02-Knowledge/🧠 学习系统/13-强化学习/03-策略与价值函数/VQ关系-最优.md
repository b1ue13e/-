---
type: study
topic: "VQ关系-最优"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["VQ关系-最优", "V*=max_a Q*, Q*=E[R+γmax Q*]"]
upstream: ["[[V函数-最优]]", "[[Q函数-最优]]"]
tags: [学习, 强化学习]
---

# VQ关系-最优

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
最优价值函数之间也有同样的换算关系，而且因为"取最大"，形式更简洁。

## 正式定义 / 公式
V*(s) = max_a Q*(s,a)
Q*(s,a) = E[ R + γ max_{a'} Q*(S',a') ]
即最优下 V 是 Q 对动作取最大；Q 是"奖励 + 折扣后最优"。

## 最小手算例子
s1 两动作：Q*(s1,step)=1、Q*(s1,stay)=0 → V*(s1)=max(1,0)=1。

## 对比与常见错误
- 常见错误：在最优关系里仍写 Σ_a π(a|s)——最优时不再有策略加权，直接取 max。

## 闭卷自测
1. 最优下 V 与 Q 的关系？
2. 最优关系为何用 max 而非加权平均？
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
