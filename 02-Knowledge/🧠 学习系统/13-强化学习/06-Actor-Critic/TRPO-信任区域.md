---
type: study
topic: "TRPO-信任区域"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO-信任区域", "TRPO 信任域"]
upstream: ["[[TRPO简介]]", "[[NPG]]"]
tags: [学习, 强化学习]
---

# TRPO-信任区域

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
普通 PG 步长难设、易崩。TRPO 把更新限制在"策略分布变化不大"的信任域内，稳定改进。

## 正式定义 / 公式
每步在 KL(π_θ || π_{θ+Δ}) ≤ δ 的约束下最大化带重要性权重的优势目标（见「TRPO-KL」「TRPO-单调」）。

## 最小手算例子
<!-- NUMEX -->概率比 r=π_new/π_old。若 r=1.5、裁剪 ε=0.2，则被压到 1.2（PPO 的 clip 同源思路）；TRPO 直接约束 KL(π_new‖π_old)≤δ=0.01 而非硬裁剪。

更新前算新旧策略 KL，若超阈值 δ 就缩小步长，避免策略剧变（呼应「REINFORCE-不稳定」）。

## 对比与常见错误
- 与 NPG：TRPO 用约束近似 NPG 的自然梯度，避免求大 Fisher 逆。
- 常见错误：把 TRPO 当无约束二阶——KL 约束正是其稳定关键。

## 闭卷自测
1. TRPO 的"信任域"是什么？
2. 它相对普通 PG 解决什么问题？
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
