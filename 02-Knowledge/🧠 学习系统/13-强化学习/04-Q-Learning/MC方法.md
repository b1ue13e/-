---
type: study
topic: "MC方法"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["MC方法", "蒙特卡洛方法"]
upstream: ["[[回报定义]]", "[[轨迹定义]]"]
tags: [学习, 强化学习]
---

# MC方法

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
蒙特卡洛（MC）是最朴素的"从经验学"：用完整一幕的真实回报去估计价值。思路直观，但需要幕能终止。

## 正式定义 / 公式
V^π(s) ≈ 平均(所有经过 s 的幕的回报 G)
每幕结束用 G_t 做更新：V(s_t) ← V(s_t) + α (G_t − V(s_t))
首次访问 / 每次访问 MC 区别是否对同一幕中重复出现的 s 多次计数。

## 最小手算例子
2 状态链跑一幕：s1→step→s2(term, R=+1)。G=1。V(s1) ← 0 + α(1−0)。多幕平均趋近 1。

## 对比与常见错误
- 与 TD：MC 无自举、无偏但高方差、需幕末；TD 自举、可在线。
- 常见错误：在"不终止"的环境用 MC——MC 要求每幕有终点。

## 闭卷自测
1. MC 如何估计 V？
2. MC 与 TD 的核心trade-off？
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
