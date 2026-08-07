---
type: study
topic: "VQ关系-V从Q"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["VQ关系-V从Q", "V^π(s)=Σ_a π(a|s)Q^π(s,a)"]
upstream: ["[[V函数-定义]]", "[[Q函数-定义]]"]
tags: [学习, 强化学习]
---

# VQ关系-V从Q

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
V 和 Q 描述同一策略的好坏，只是粒度不同（状态 vs 状态-动作）。它们之间如何换算？

## 正式定义 / 公式
V^π(s) = Σ_a π(a|s) · Q^π(s,a)
即 V 是 Q 在策略 π 下的加权平均。

## 最小手算例子
s1 下 π(右)=0.6、π(左)=0.4，Q(s1,右)=1、Q(s1,左)=0：
V(s1)=0.6·1 + 0.4·0 = 0.6。

## 对比与常见错误
- 常见错误：把权重当成 1/|A|（均匀）——权重是策略 π(a|s)，不一定均匀。

## 闭卷自测
1. 由 Q 求 V 的公式？
2. 权重是什么、能否均匀？
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
