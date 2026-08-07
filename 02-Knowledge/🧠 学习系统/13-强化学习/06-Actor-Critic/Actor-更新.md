---
type: study
topic: "Actor-更新"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Actor-更新", "Actor 更新规则"]
upstream: ["[[Actor-输出]]", "[[优势-TD]]", "[[策略梯度定理与REINFORCE]]"]
tags: [学习, 强化学习]
---

# Actor-更新

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
把 critic 的优势接到策略梯度上，得到 actor 的实际更新。

## 正式定义 / 公式
θ ← θ + α · ∇_θ log π_θ(a|s) · A(s,a)
A 常取 TD 形式 A≈r+γV(s')−V(s)（见「优势-TD」）。
可加熵项 −β H(π) 鼓励探索（见 PPO）。

## 最小手算例子
(s,a,r,s')=(s,a1,+1,s'), V(s)=0.4,V(s')=0.5,γ=0.9：A=1+0.9·0.5−0.4=1.05；θ←θ+α·∇logπ·1.05。

## 对比与常见错误
- 与 REINFORCE 更新：仅把 G_t 换成优势 A，方差更低、可在线。
- 常见错误：用 critic 的 V 直接当动作价值——应经 A=…−V 转成"相对优势"。

## 闭卷自测
1. 写出 actor 更新式。
2. 优势 A 在这里怎么来？
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
