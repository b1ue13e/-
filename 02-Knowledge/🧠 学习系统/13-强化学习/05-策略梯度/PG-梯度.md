---
type: study
topic: "PG-梯度"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PG-梯度", "策略梯度定理"]
upstream: ["[[PG-目标函数]]", "[[PG-似然比]]"]
tags: [学习, 强化学习]
---

# PG-梯度

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
把目标函数梯度写成可采样的形式，就得到策略梯度定理——整个策略梯度家族的理论基石。

## 正式定义 / 公式
策略梯度定理：
∇_θ J(θ) = E_{τ~π_θ} [ Σ_t ∇_θ log π_θ(a_t|s_t) · G_t ]
其中 G_t 为从 t 起的回报（或含基线/优势的形式，见「优势-定义」）。
用蒙特卡洛回报得到 REINFORCE；用优势可降方差。

## 最小手算例子
一条轨迹在 s 选 a1 得 G=+1，且 ∇log π(a1|s)=0.4：对 θ 的梯度贡献 +0.4·1。多次采样取平均即近似 ∇J。

## 对比与常见错误
- 与值方法：这里是"对策略参数"的梯度；值方法对价值参数。
- 常见错误：把 G_t 写成整幕回报 G_0——正确应是从时刻 t 起的局部回报 G_t。

## 闭卷自测
1. 写出策略梯度定理。
2. 梯度里为什么是 ∇log π 乘 G_t？
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
