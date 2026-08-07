---
type: study
topic: "REINFORCE-更新"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["REINFORCE-更新", "REINFORCE 更新规则"]
upstream: ["[[REINFORCE-MC]]", "[[PG-梯度]]"]
tags: [学习, 强化学习]
---

# REINFORCE-更新

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
把梯度变成可执行的参数更新步骤。

## 正式定义 / 公式
θ ← θ + α · Σ_t ∇_θ log π_θ(a_t|s_t) · G_t
或更常见（带基线 b）：θ ← θ + α · ∇_θ log π_θ(a_t|s_t) · (G_t − b)
（基线版见「REINFORCE-Baseline」「优势-估计」。）

## 最小手算例子
一步 (s,a,G)=(s,a1,+1)，∇log π=0.4，α=0.1：θ ← θ + 0.1·0.4·1 = θ+0.04。

## 对比与常见错误
- 与 Q-learning 更新：REINFORCE 更新策略参数（概率），Q-learning 更新价值表/网络。
- 常见错误：忘记步长 α 或把 G_t 当标量加到 logits 上（应先乘梯度）。

## 闭卷自测
1. 写出 REINFORCE 参数更新式。
2. 它更新的是什么量？
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
