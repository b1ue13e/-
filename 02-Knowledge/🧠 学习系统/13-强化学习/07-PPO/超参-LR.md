---
type: study
topic: "超参-LR"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["超参-LR", "学习率"]
upstream: ["[[PPO近端策略优化]]"]
tags: [学习, 强化学习]
---

# 超参-LR

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
学习率决定每次更新步幅，对 RL 稳定性极敏感。

## 正式定义 / 公式
PPO 常用 Adam，LR 在 1e-4–3e-4（连续控制）或 2.5e-4（Atari）量级，配合线性衰减。

## 最小手算例子
默认 3e-4，训练末期线性降到 0。

## 对比与常见错误
- 与 工程-梯度裁剪：LR 是优化步长、裁剪是梯度上限。
- 常见错误：直接套用监督学习的 LR（常偏大）→ RL 崩溃。

## 闭卷自测
1. PPO 常用 LR 量级？
2. 为何不能照搬监督学习 LR？
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
