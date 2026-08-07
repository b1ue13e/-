---
type: study
topic: "REINFORCE-高方差"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["REINFORCE-高方差", "REINFORCE 高方差"]
upstream: ["[[REINFORCE-MC]]", "[[REINFORCE-无偏]]"]
tags: [学习, 强化学习]
---

# REINFORCE-高方差

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
REINFORCE 最大的实际缺点是方差大：整幕回报 G_t 受后续所有随机性影响，单步估计很"抖"。

## 正式定义 / 公式
Var( Σ_t ∇log π · G_t ) 随轨迹长度与奖励噪声放大；长幕、稀疏奖励下尤甚。
后果：需要大量并行样本、学习率小、训练慢。

## 最小手算例子
<!-- NUMEX -->单幕回报 G 方差大。设两幕 G=[10,2]，均值 6；用基线 b=6 后优势=[4,−4]（零均值、偏置更小）。无基线时梯度 ∝ 原始 G，噪声直接进更新——这是 REINFORCE 高方差的根因。

某步动作好，但后续碰巧拿到低奖励 → G_t 低 → 该步被错误惩罚；反之亦反。单条轨迹噪声大。

## 对比与常见错误
- 与减方差手段：基线（baseline）、优势（advantage）、critic（Actor-Critic）都为此而生。
- 常见错误：靠"调小 α"硬扛高方差——应从估计本身降方差。

## 闭卷自测
1. REINFORCE 为何高方差？
2. 哪些技术用来降方差？
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
