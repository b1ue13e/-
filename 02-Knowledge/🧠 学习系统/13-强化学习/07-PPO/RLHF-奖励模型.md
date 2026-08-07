---
type: study
topic: "RLHF-奖励模型"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["RLHF-奖励模型", "RM 作为奖励"]
upstream: ["[[RLHF-RM]]"]
tags: [学习, 强化学习]
---

# RLHF-奖励模型

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
训好的奖励模型在 RL 阶段如何被当作"环境奖励"使用。

## 正式定义 / 公式
RLHF 的奖励函数取 RM 输出加 KL 惩罚：
r_total(s,a) = r_φ(prompt, response) − β·KL(π_θ(·|s) ‖ π_ref(·|s))
RM 提供主奖励，KL 项防止策略偏离参考模型太远。

## 最小手算例子
<!-- NUMEX2 -->RM 架构：在 SFT 模型接标量头，目标对齐人类偏好；常加 KL 正则 β=0.1 防止 reward hacking。

回答越长越"安全"被 RM 误奖（reward hacking）时，KL 项把策略拉回 π_ref 抑制过拟合。

## 对比与常见错误
- 与 RLHF-RM：RM 是来源，本卡是它在 RL 中的用法。
- 常见错误：只用 RM 不加 KL——易触发奖励作弊。

## 闭卷自测
1. RLHF 中 RM 如何充当奖励？
2. 为何要在奖励中加 KL 惩罚？
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
