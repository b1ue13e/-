---
created: 2026-08-07
type: study
course: "强化学习"
title: "AIRL 对抗逆强化 (Adversarial IRL)"
topic: "AIRL 对抗逆强化 (Adversarial IRL)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, IRL, 对抗, GAIL]
upstream: ["[[GAIL]]", "[[最大熵逆强化学习MaxEntIRL]]"]
concept: ["AIRL", "对抗训练", "奖励塑形", "占用度量"]
sources:
  - "Fu et al. 2018 (AIRL)"
---
# AIRL 对抗逆强化 (Adversarial IRL)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
GAIL 直接学一个"判别器"来区分专家与生成轨迹，等价于在对抗地匹配占用度量，但**它不显式给出可迁移的奖励 r**。AIRL（Adversarial IRL）把 GAIL 重新解释为 IRL：用特殊结构的判别器，在对抗训练的同时恢复出**真正的、可迁移的奖励函数**，从而把"模仿"和"反推奖励"统一起来。

## 正式定义 / 公式
判别器采用可分解形式：

  D(s,a) = exp(f(s,a)) / (exp(f(s,a)) + π(a|s))

其中 f(s,a) = g(s,a) − γ h(s') + h(s)（含势函数 h，抵消奖励塑形歧义）。对抗目标让 D 区分专家/策略轨迹，等价于最大化"策略在 g 上的期望 − 熵正则"，即 MaxEnt IRL。训练出的 g 就是学到的奖励；再用任意 RL 算法在此 r 上训练，可脱离专家数据继续优化。

## 最小手算例子
机械臂叠毛巾：GAIL 训出的策略只能在原分布内模仿；AIRL 额外给出 r，可把任务目标稍改（叠更高的毛巾）后用 r 做 RL 微调，无需新示范——因为 r 是"关于任务"的、可迁移的，而非"关于动作"的。

## 对比与常见错误
- 与 GAIL：AIRL 是 GAIL 的可解释/可迁移版本，多出一个显式奖励 g。
- 与 MaxEnt IRL：AIRL 用对抗式采样代替昂贵的期望特征计算，扩展到高维。
- **常见错误**：忘记势函数 h 项 → 学到的 g 含奖励塑形歧义，迁移时失真。

## 闭卷自测
1. AIRL 的判别器结构为何能"同时做 GAIL 和对抗 IRL"？
2. 相比 GAIL，AIRL 多得到了什么、为何更可迁移？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
