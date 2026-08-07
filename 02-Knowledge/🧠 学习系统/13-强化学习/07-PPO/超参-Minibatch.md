---
type: study
topic: "超参-Minibatch"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["超参-Minibatch", "小批量"]
upstream: ["[[A2C家族]]"]
tags: [学习, 强化学习]
---

# 超参-Minibatch

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
K 轮更新中，每轮要把 batch 切成多小的片。

## 正式定义 / 公式
minibatch：把一批数据再随机切成小块（如 64 或 256），逐块做 SGD。太小噪声大、太大欠随机化。

## 最小手算例子
2048 步 → 切成 8 个 256 的 minibatch。

## 对比与常见错误
- 与 超参-Batch：batch 总、minibatch 切片。
- 常见错误：minibatch 与 batch 同大——失去多次 SGD 的意义。

## 闭卷自测
1. minibatch 与 batch 的关系？
2. 它如何影响 K 轮更新？
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
