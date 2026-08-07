---
type: study
topic: "PPOClip-函数"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PPOClip-函数", "裁剪代理函数"]
upstream: ["[[PPOClip-目标]]"]
tags: [学习, 强化学习]
---

# PPOClip-函数

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
把裁剪目标拆开，看清它在 A>0 与 A<0 两种情形下的行为。

## 正式定义 / 公式
对单个时间步：
- 若 A_t > 0（应增大概率）：目标被截在 1+ε，即 r_t 超过 1+ε 后不再贡献增益；
- 若 A_t < 0（应减小概率）：目标被截在 1−ε，即 r_t 低于 1−ε 后不再贡献减益。
min 再取两者较小者，温和抑制超出信任区域的方向。

## 最小手算例子
A_t=−1, r_t=0.6, ε=0.2 → clip 到 0.8，目标=0.8·(−1)=−0.8（比 −0.6 更不坏）。

## 对比与常见错误
- 与 PPOClip-目标：本卡是逐情形解读。
- 常见错误：以为裁剪只在 A>0 生效——A<0 也裁剪。

## 闭卷自测
1. 当 A_t>0 与 A_t<0 时裁剪分别保护什么？
2. min 运算符的作用是什么？
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
