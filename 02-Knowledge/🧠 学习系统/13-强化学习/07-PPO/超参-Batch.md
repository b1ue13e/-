---
type: study
topic: "超参-Batch"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["超参-Batch", "采批大小"]
upstream: ["[[A2C家族]]"]
tags: [学习, 强化学习]
---

# 超参-Batch

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
每次更新前收集多少环境步，影响方差与吞吐。

## 正式定义 / 公式
batch（rollout length × num_envs，如 2048 步或 128×16）：越大优势估计越稳、方差越低，但 on-policy 陈旧度上升、单轮延迟增加。

## 最小手算例子
128 并行环境 × 16 步 = 2048 步一批。

## 对比与常见错误
- 与 超参-Minibatch：batch 是采集总量，minibatch 是更新切片。
- 常见错误：batch 过小 → 优势噪声大、训练抖动。

## 闭卷自测
1. PPO 的 batch 大小指什么？
2. 它如何影响方差？
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
