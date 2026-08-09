---
created: 2026-08-07
type: study
course: "强化学习"
title: "TD3+BC (TD3 + Behavior Cloning)"
topic: "TD3+BC (TD3 + Behavior Cloning)"
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习]
upstream: ["[[TD3 (Twin Delayed DDPG)]]", "[[离线 RL 与模仿学习]]"]
concept: ["离线RL", "行为克隆", "TD3", "简单有效"]
sources:
  - "Fujimoto & Gu, 2021, 'A Minimalist Approach to Offline RL'"
---
# TD3+BC (TD3 + Behavior Cloning)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Offline RL 综述 / TD3+BC 原文`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
离线 RL 常被复杂正则（CQL/BCQ）占据。TD3+BC 证明：在 TD3 上加一个简单的 BC 惩罚项，就能以极少代码超过多数专门离线算法，强调"简单 baseline 被低估"。

## 正式定义 / 公式
损失 = TD3 的 actor 损失 + λ · E_{(s,a)~D}[ (π(s) − a)^2 ]（BC 项，约束策略不偏离数据集动作 a）。λ 控制偏离程度。

## 最小手算例子
数据集动作 a=0.5，策略当前输出 π(s)=0.8，λ=1：BC 项 = (0.8−0.5)^2 = 0.09，把策略往 0.5 拉。
若 λ=0 退化成普通 TD3（可能 OOD 漂移）；λ 过大则退化为纯 BC、放弃回报优化。

## 对比与常见错误
- 与 TD3：多了 BC 正则项；与 CQL/BCQ：实现简单得多（无 VAE、无额外 Q 正则）。
- 常见错误：λ 选错导致欠拟合（λ 大）或过估计（λ 小）。

## 闭卷自测
1. TD3+BC 相比 TD3 多了什么、为什么离线有效？
2. λ 过大/过小各有什么后果？

## 直觉：TD3+BC 用“一行 BC 惩罚”打赢复杂方法
多数离线算法靠 VAE/正则堆复杂度。TD3+BC 只在 TD3 的 actor 损失上追加 λ·(π(s)−a)² 的“行为克隆惩罚”，约束策略别偏离数据集动作，就常以极少代码超过 CQL/BCQ。启示：离线 RL 里“简单且贴近数据”的 baseline 常被低估，应先跑它再上重武器；λ 太大欠拟合、太小回到 OOD 漂移。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
