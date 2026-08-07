---
type: study
topic: "PPOClip-Epsilon"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PPOClip-Epsilon", "PPO 裁剪范围"]
upstream: ["[[PPOClip-函数]]"]
tags: [学习, 强化学习]
---

# PPOClip-Epsilon

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
裁剪目标里唯一的超参数 ε 直接决定信任区域大小，需要讲清取值经验。

## 正式定义 / 公式
ε 是裁剪半宽：比率 r_t 被限制在 [1−ε, 1+ε]。常用 ε=0.1–0.3（连续控制常 0.2，Atari 常 0.1–0.2）。

## 最小手算例子
ε=0.2 → 允许新旧策略概率比在 0.8–1.2 之间，超出部分被截断。

## 对比与常见错误
- 与 PPOClip-目标：ε 是其中的 clip 区间参数。
- 常见错误：ε 过大形同无约束、过小则学习缓慢。

## 闭卷自测
1. ε 在 PPO 裁剪中起什么作用？
2. ε 过大或过小分别有什么后果？
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
