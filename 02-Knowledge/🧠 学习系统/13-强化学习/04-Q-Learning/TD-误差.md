---
type: study
topic: "TD-误差"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TD-误差", "TD error δ_t"]
upstream: ["[[TD-0]]"]
tags: [学习, 强化学习]
---

# TD-误差

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
TD 更新里方括号那一项是个"误差信号"，量化"当前估计"与"一步自举目标"的差距。理解它有助于看懂 SARSA / Q-learning / TD-λ 的更新本质。

## 正式定义 / 公式
TD 误差：
δ_t = r_{t+1} + γ V(s_{t+1}) − V(s_t)   （对 V）
或 δ_t = r_{t+1} + γ Q(s_{t+1}, a_{t+1}) − Q(s_t, a_t)   （对 Q，on-policy）
TD 更新即 V(s_t) ← V(s_t) + α δ_t。

## 最小手算例子
沿用 TD-0 例子：δ = 1 + 0.9·0 − 0 = 1。它就是这一步的"惊喜程度"——比预期（0）多拿了 1。

## 对比与常见错误
- 与 MC 误差 G_t − V(s_t)：MC 误差用整幕回报，TD 误差只用一步自举。
- 常见错误：认为 δ_t 是"真实误差"——它是用估计减估计，本身有偏（但无偏于真实回报在极限处）。

## 闭卷自测
1. 写出 V 与 Q 两种 TD 误差。
2. 为什么说 TD 误差是自举的？
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
