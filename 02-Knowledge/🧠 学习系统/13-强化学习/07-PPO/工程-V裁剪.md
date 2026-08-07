---
type: study
topic: "工程-V裁剪"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["工程-V裁剪", "价值裁剪"]
upstream: ["[[PPOClip-目标]]", "[[优势-定义]]"]
tags: [学习, 强化学习]
---

# 工程-V裁剪

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
价值网络若预测离谱，会让 GAE 优势失真，需要限制其目标范围。

## 正式定义 / 公式
价值裁剪：对价值损失也做 clip，使 V_φ(s_t) 不偏离旧值 V_old 超出 ε_V：
V_loss = max( (V−R)^2, (clip(V, V_old−ε_V, V_old+ε_V) − R)^2 )
或仅裁剪优势/回报。防止单步大误差主导梯度。

## 最小手算例子
R=2.0, V_old=1.0, ε_V=0.2 → V 被约束在 [0.8,1.2] 附近。

## 对比与常见错误
- 与 PPOClip：价值裁剪借鉴了策略裁剪思想。
- 常见错误：只裁剪策略不裁剪价值——价值爆炸仍会拖垮优势。

## 闭卷自测
1. 为何要对价值网络做裁剪？
2. 价值裁剪如何保护 GAE？
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
