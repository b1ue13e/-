---
created: 2026-08-07
type: study
course: "强化学习"
title: "GAIL (Generative Adversarial IL)"
topic: "GAIL (Generative Adversarial IL)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[行为克隆BC]]", "[[策略梯度定理与REINFORCE]]"]
concept: ["GAIL", "对抗", "判别器即奖励", "学徒学习"]
sources:
  - "Ho & Ermon 2016, 'Generative Adversarial Imitation Learning'"
---
# GAIL (Generative Adversarial IL)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`GAIL 原文`
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
BC 不会超过专家、且依赖状态标注。GAIL 把 IL 看成"匹配专家状态-动作占用度量"：用一个判别器 D 当奖励，让策略的占用分布逼近专家。

## 正式定义 / 公式
奖励 r(s,a) = −log D(s,a)（或 log(1−D)）；交替：用 RL（如 TRPO）更新策略最大化该奖励；用 (s,a) 专家 vs 策略样本更新 D 区分二者。

## 最小手算例子
判别器 D 初值 0.5（不分）；策略采样被 D 判"像专家"得高奖励。
设某转移 D=0.8（判为策略产生），r = −ln(0.8) = 0.223（低奖励）；专家转移 D=0.2，r = −ln(0.2) = 1.609（高奖励）。策略被推向专家占用。

## 对比与常见错误
- 与 BC：GAIL 不依赖逐状态标注、可超越专家占用；需对抗训练，不稳。
- 常见错误：判别器过强导致奖励全 0/1（梯度消失）；混淆"奖励 = −logD"符号。

## 闭卷自测
1. GAIL 中判别器如何充当奖励？
2. GAIL 与 BC 的根本差异？

## 直觉：把“像不像专家”当成奖励
行为克隆不会处理分布偏移；GAIL 用 GAN 思路——判别器 D 区分“专家轨迹”与“learner 轨迹”，其对数几率 −log(1−D) 直接当奖励喂给策略梯度。于是 learner 在最大化回报的过程中被迫模仿专家占有分布，等价于最小化与专家的策略 occupancy 距离（逆 RL 的对偶）。训练稳定性和模式崩塌是实战难点，常与熵奖励/梯度惩罚配合。

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
