---
type: study
topic: "折扣-Gamma"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["折扣-Gamma", "策略梯度中的折扣 γ"]
upstream: ["[[回报定义]]"]
tags: [学习, 强化学习]
---

# 折扣-Gamma

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
策略梯度的目标也含折扣因子 γ；它影响"未来奖励的重视程度"与"梯度尺度"。

## 正式定义 / 公式
目标 J(θ)=E[ Σ_t γ^t r_{t+1} ]；梯度里每个 G_t 也是折扣回报。
γ 小→重短期；γ 大→重长期。γ→1 时近似平均奖励/无折扣目标。

## 最小手算例子
γ=0.9：第 3 步奖励权重 0.81；γ=0.99 权重 0.97——长期信号保留更多。

## 对比与常见错误
- 与值方法：γ 作用一致（折扣回报），但策略梯度还需处理"每步折扣"的实现细节。
- 常见错误：忽略 γ 对梯度幅值的影响——长幕累积 γ^t 会缩放梯度，需配合优势/归一。

## 闭卷自测
1. 折扣 γ 在策略梯度目标里起什么作用？
2. γ 大小如何影响学习？
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
