---
created: 2026-08-07
type: study
course: "强化学习"
title: "SQIL 软Q模仿 (Soft Q Imitation Learning)"
topic: "SQIL 软Q模仿 (Soft Q Imitation Learning)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: algorithm
status: learning
importance: "C"
tags: [学习, 强化学习, 模仿学习, 离线]
upstream: ["[[行为克隆BC]]", "[[SAC软Actor-Critic]]"]
concept: ["SQIL", "软Q", "离线模仿", "奖励塑形"]
sources:
  - "Reddy et al. 2019 (SQIL)"
---
# SQIL 软Q模仿 (Soft Q Imitation Learning)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
行为克隆（BC）简洁但受分布偏移之苦；GAIL 效果好但训练不稳、要对抗。SQIL 走中间路线：**把模仿变成离线 RL**——给专家转移奖励 +1、其它转移奖励 0，用软 Q 学习（SAC 的 Q 部分）去拟合，零环境交互即可学会专家行为，且天然抗偏移。

## 正式定义 / 公式
构造数据：专家转移 (s,a,s') 标 r=+1，非专家（随机/生成）转移标 r=0。用软 Bellman 更新训练 Q（温度 α→∞ 的 SAC 形式）：

  Q(s,a) ← r + γ·α·log Σ_{a'} exp(Q(s',a')/α)

最优 Q 在专家状态-动作上最高，策略 π(a|s)∝exp(Q/α) 退化为"只在专家动作上集中"。无需环境采样，纯离线。

## 最小手算例子
仅有 100 条专家驾驶片段（无环境）。SQIL 把每条标 +1，再随机造负样本标 0，离线训 Q。相比 BC 在非专家状态崩溃，SQIL 学到"偏离专家动作→Q 低→被抑制"，分布偏移被软 Q 的保守性兜住。

## 对比与常见错误
- 与 BC：SQIL 是离线 RL 而非监督，对偏移更鲁棒，但需构造负样本。
- 与 GAIL：SQIL 无对抗、训练稳定，但表达力/样本效率居中。
- **常见错误**：负样本不足或全来自单一策略 → Q 高估非专家区域；温度 α 设错影响 π 集中度。

## 闭卷自测
1. SQIL 如何把"模仿"转成"离线 RL"？专家/非专家转移分别标什么奖励？
2. 它相比 BC 为何更抗分布偏移？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
