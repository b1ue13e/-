---
type: study
topic: "NPG"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["NPG", "Natural Policy Gradient"]
upstream: ["[[PG-梯度]]", "[[演进-连续优化]]"]
tags: [学习, 强化学习]
---

# NPG

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
自然策略梯度（NPG）用 Fisher 信息矩阵做二阶更新，是 TRPO 的前身，理论上更稳。

## 正式定义 / 公式
更新：θ_{new} = θ + α F(θ)^{−1} ∇_θ J
F(θ) = E_{s,a~π_θ}[ ∇log π ∇log π^⊤ ]（Fisher 信息矩阵）
约束在"策略分布变化"意义上步长，而非原始参数步长。

## 最小手算例子
<!-- NUMEX -->自然梯度 = F⁻¹∇J，F 为 Fisher 信息矩阵。例 F=diag(2,1)、∇J=[1,1] ⇒ 自然梯度=[0.5,1]（沿最陡信赖方向更新，步长由 F 归一，对参数尺度不变）。

两种参数化同样 Δθ 可能让 KL(π_θ||π_{θ+Δθ}) 差很多；NPG 用 F 使每次更新的 KL 近似恒定。

## 对比与常见错误
- 与 TRPO：TRPO 用约束优化近似 NPG（避免显式求 F^{−1} 的大矩阵）。
- 常见错误：以为 NPG=普通二阶牛顿——它度量的是策略分布空间，不是损失曲面。

## 闭卷自测
1. NPG 的更新式？
2. 它和 TRPO 的关系？
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
