---
type: study
topic: "IS-含义"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["IS-含义", "重要性采样"]
upstream: ["[[策略梯度]]"]
tags: [学习, 强化学习]
---

# IS-含义

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
想用行为策略 μ 采集的样本去估计目标策略 π 下的期望，怎么办？

## 正式定义 / 公式
重要性采样：若 q(x)>0 处必有 p(x)>0，则
E_{x~p}[f(x)] = E_{x~q}[ f(x)·p(x)/q(x) ]
用采样分布 q 的样本，乘以密度比 p/q（重要性权重）得到 p 下的无偏估计。

## 最小手算例子
p 取 2 个值、q 取另 2 个值，算 ρ=p/q，对 f 加权平均即得 p 下的期望。

## 对比与常见错误
- 与直接采样：IS 让"用旧数据估新策略"成为可能。
- 常见错误：忽略支撑集条件（q=0 而 p>0 时权重爆炸）。

## 闭卷自测
1. 重要性采样解决什么问题？
2. 无偏性依赖什么前提？
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
