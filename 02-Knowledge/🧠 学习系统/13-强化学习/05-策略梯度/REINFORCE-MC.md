---
type: study
topic: "REINFORCE-MC"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["REINFORCE-MC", "REINFORCE 算法"]
upstream: ["[[PG-梯度]]", "[[蒙特卡洛方法]]"]
tags: [学习, 强化学习]
---

# REINFORCE-MC

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
REINFORCE 是最早、最朴素的策略梯度算法：直接用蒙特卡洛整幕回报估计策略梯度。

## 正式定义 / 公式
对每条轨迹 τ=(s_0,a_0,r_1,…)：
∇_θ J ≈ ∇_θ log p_θ(τ) · G_0，其中 log p_θ(τ)=Σ_t log π_θ(a_t|s_t) + log P(s_{t+1}|s_t,a_t)
环境动态项在期望下被消去，只剩：
∇_θ J ≈ Σ_t ∇_θ log π_θ(a_t|s_t) · G_t

## 最小手算例子
一条轨迹在 s 选 a1 得 G_t=+1，∇log π(a1|s)=0.4 → 梯度 +0.4。θ ← θ + α·0.4。

## 对比与常见错误
- 与带基线的 PG：REINFORCE 原始版用原始 G_t，方差大；加基线/优势可大幅降方差。
- 常见错误：把 REINFORCE 当成 on-policy TD——它用整幕 MC 回报，是典型的 MC 策略梯度。

## 闭卷自测
1. REINFORCE 用什么估计梯度？
2. 为什么环境动态项会消去？
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
