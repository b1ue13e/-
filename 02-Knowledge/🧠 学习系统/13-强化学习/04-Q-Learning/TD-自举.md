---
type: study
topic: "TD-自举"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TD-自举", "bootstrapping"]
upstream: ["[[TD-0]]", "[[值迭代]]"]
tags: [学习, 强化学习]
---

# TD-自举

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
"自举（bootstrapping）"指用自己（或其他状态的）当前估计去更新自己。这是 TD 与 DP 的共同特征，也是它不需要完整轨迹的原因。

## 正式定义 / 公式
自举 = 用 V(s_{t+1})（当前估计，非真实值）作为更新目标的一部分：
目标 = r_{t+1} + γ V(s_{t+1})
对照 MC 目标 = G_t（真实整幕回报，无自举）。

## 最小手算例子
TD(0) 用 V(s2)=0（估计）算目标 1；若改用真实 G_t（等幕结束）才是 MC。自举让 TD 每步即可更新。

## 对比与常见错误
- 与 MC：MC 不自举（无偏但高方差、需幕末）；TD 自举（有偏但低方差、可在线）。
- 常见错误：以为自举一定更准——自举引入偏差，但方差更小、学习更快。

## 闭卷自测
1. 什么是自举？TD 与 DP 在哪点相同？
2. 自举的代价与收益？
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
