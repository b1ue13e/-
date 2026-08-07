---
type: study
topic: "RLHF-KL"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["RLHF-KL", "RLHF 的 KL 惩罚"]
upstream: ["[[IS-KL]]", "[[PPO近端策略优化]]"]
tags: [学习, 强化学习]
---

# RLHF-KL

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
RLHF 中 KL 惩罚是防止模型"钻 RM 空子"的关键正则。

## 正式定义 / 公式
对每步策略加 KL 到参考策略 π_ref（通常是 SFT 模型）：
L = E[ r_φ − β·KL(π_θ ‖ π_ref) ]
β 控制约束强度，越大越保守。

## 最小手算例子
β=0.1 时模型小幅优化 RM；β 过大则几乎不动、像回退到 SFT。

## 对比与常见错误
- 与 IS-KL：同样用 KL 度量策略距离，这里作惩罚项。
- 常见错误：β=0 完全信任 RM——必现 reward hacking。

## 闭卷自测
1. RLHF 中 KL 惩罚防什么？
2. β 过大会怎样？
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
