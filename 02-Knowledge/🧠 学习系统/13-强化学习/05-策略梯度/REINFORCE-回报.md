---
type: study
topic: "REINFORCE-回报"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["REINFORCE-回报", "REINFORCE 的回报项"]
upstream: ["[[REINFORCE-MC]]", "[[回报定义]]"]
tags: [学习, 强化学习]
---

# REINFORCE-回报

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
REINFORCE 更新里"回报"具体指什么？是整幕回报 G_0 还是局部 G_t？这是容易混淆的点。

## 正式定义 / 公式
每个时间步 t 用从 t 起的折扣回报 G_t = Σ_{k≥0} γ^k r_{t+k+1} 作权重（不是仅 G_0）。
完整形式：∇_θ J ≈ Σ_t ∇_θ log π_θ(a_t|s_t) · G_t。

## 最小手算例子
t=0 时 G_0 含全程；t=2 时 G_2 只含从第三步起的回报。每步用"自己之后的回报"加权。

## 对比与常见错误
- 常见错误：对所有 t 都用 G_0——正确是每步用对应的 G_t（从该步起算）。

## 闭卷自测
1. REINFORCE 中每步用哪个回报？
2. 为何用 G_t 而非 G_0？
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
