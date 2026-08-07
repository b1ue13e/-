---
type: study
topic: "超参-K"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["超参-K", "PPO 更新轮数"]
upstream: ["[[A2C家族]]", "[[PPO近端策略优化]]"]
tags: [学习, 强化学习]
---

# 超参-K

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
同一批数据要反复更新几轮，需要 K 控制复用程度。

## 正式定义 / 公式
K（epochs）：每收集一批数据后，用 PPO 目标在其 minibatch 上更新 K 次。常用 K=3–10；太大易过拟合该批、偏离 on-policy 假设。

## 最小手算例子
采 2048 步 → 分 minibatch → 重复更新 4 轮。

## 对比与常见错误
- 与 超参-Minibatch：K 是轮数、minibatch 是每轮大小。
- 常见错误：K 过大导致策略偏离采集时太远、训练不稳。

## 闭卷自测
1. PPO 的 K epoch 是什么？
2. K 过大有何后果？
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
