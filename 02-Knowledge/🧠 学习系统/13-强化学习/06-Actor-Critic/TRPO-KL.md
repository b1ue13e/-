---
type: study
topic: "TRPO-KL"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO-KL", "TRPO 的 KL 约束"]
upstream: ["[[TRPO-信任区域]]", "[[策略-参数化]]"]
tags: [学习, 强化学习]
---

# TRPO-KL

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
信任域用什么度量"策略变化大小"？用策略间的 KL 散度。

## 正式定义 / 公式
约束：KL( π_{θ_old}(·|s) ‖ π_{θ_new}(·|s) ) ≤ δ（对每个 s 或对状态平均）
KL 衡量"动作分布"偏移程度，比参数 Δθ 更贴合策略实际变化。

## 最小手算例子
<!-- NUMEX -->离散例：p=[0.5,0.5], q=[0.8,0.2]，则 KL(p‖q)=0.5·ln(0.5/0.8)+0.5·ln(0.5/0.2)≈0.223 nat。TRPO 约束 KL(π_new‖π_old)≤δ，δ 常取 0.01。

两策略 softmax 差一点但概率分布差很多时，KL 能捕捉；参数 Δθ 小 ≠ 分布变化小。

## 对比与常见错误
- 常见错误：用 L2(Δθ) 当信任域——参数距离不等于策略分布距离。

## 闭卷自测
1. TRPO 用什么约束策略变化？
2. 为何用 KL 而非参数距离？
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
