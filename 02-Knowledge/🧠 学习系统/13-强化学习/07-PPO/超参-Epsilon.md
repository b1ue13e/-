---
type: study
topic: "超参-Epsilon"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["超参-Epsilon", "PPO 裁剪 ε"]
upstream: ["[[PPOClip-Epsilon]]"]
tags: [学习, 强化学习]
---

# 超参-Epsilon

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
裁剪范围 ε 直接决定信任区域宽度。

## 正式定义 / 公式
ε 限定概率比率 r_t∈[1−ε,1+ε]。连续控制常 0.2，Atari 常 0.1–0.2。

## 最小手算例子
ε=0.2 → 新旧策略动作概率比限在 0.8–1.2。

## 对比与常见错误
- 与 超参-K：ε 管单步约束、K 管复用轮数。
- 常见错误：ε 与探索 ε-greedy 混淆——二者无关。

## 闭卷自测
1. PPO 的 ε 与探索的 ε 有何不同？
2. 如何选 ε？
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
