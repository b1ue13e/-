---
type: study
topic: "RLHF-背景"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["RLHF-背景", "RLHF 简介"]
upstream: ["[[PPO近端策略优化]]"]
tags: [学习, 强化学习]
---

# RLHF-背景

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
大语言模型仅做监督学习会"不会听话"，需要用人类反馈把模型对齐到人的偏好。

## 正式定义 / 公式
RLHF（基于人类反馈的强化学习）三阶段流水线：
1) SFT 监督微调；2) 训练奖励模型 RM；3) 用 RL（通常 PPO）优化策略以最大化 RM 给出的奖励（带 KL 惩罚）。

## 最小手算例子

用户问"如何道歉"，RM 给礼貌回答更高分，PPO 推动策略生成更礼貌的回复。


量化：典型 3 阶段——① SFT 监督微调；② 用约 50000 条人工偏好对比样本训练奖励模型 RM；③ 以 RM 为奖励做 PPO。偏好数据规模直接决定 RM 的质量上限。
## 对比与常见错误
- 与 策略梯度：RLHF 把人类偏好变成奖励信号，本质是策略优化。
- 常见错误：以为 RLHF 是全新算法——它复用 PPO/策略梯度，只是奖励来自 RM。

## 闭卷自测
1. RLHF 三阶段是什么？
2. 为何要在 RLHF 中用 PPO？
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
