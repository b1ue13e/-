---
created: 2026-08-07
type: study
course: "强化学习"
title: "Self-Play 与 PSRO"
topic: "Self-Play 与 PSRO"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习]
upstream: ["[[多智能体RL概述]]"]
concept: ["Self-Play", "PSRO", "博弈", "纳什"]
sources:
  - "Silver et al. 2017 (AlphaGo Zero); Lanctot et al. 2017 (PSRO)"
---
# Self-Play 与 PSRO

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`AlphaGo Zero / PSRO 原文`
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
对手也是学习者时，固定对手策略会过拟合。Self-Play 让智能体与自身历史版本对弈，持续提升；PSRO 把对手种群（而非单一）纳入，逼近纳什均衡。

## 正式定义 / 公式
Self-Play：用当前策略 π 同时当对手；PSRO：维护策略种群 Π，每轮加入"对种群最佳响应"π*，用 meta-博弈求解（如纳什）选混合。

## 最小手算例子
石头剪刀布：种群先有 {石头}；最佳响应=布；加入 {石头,布}；再最佳响应=剪刀；种群 {石头,布,剪刀} 趋近均匀纳什。
单 Self-Play 可能只在自己循环里震荡，PSRO 保证覆盖。

## 对比与常见错误
- 与固定对手训练：Self-Play/PSRO 避免策略崩坏、更鲁棒；代价是计算种群。
- 常见错误：只用单一固定对手导致过拟合；忽视对手策略的多样性。

## 闭卷自测
1. Self-Play 相比固定对手有何优势与风险？
2. PSRO 用"种群"解决了 Self-Play 的什么问题？

## 直觉：把对手也当成要击败的环境
Self-Play 让 Agent 与自己历史版本对弈，对手随训练同步变强，自然产生课程。PSRO 进一步：维护一个“对手策略池”，每轮用 best response 针对整个池、再把新策略加入池，逼近博弈的 Nash 均衡。用于 AlphaGo/扑克等零和博弈。注意：非传递博弈里“最佳响应链”可能环游不收敛，需要种群层面的均衡求解而非单点 best response。

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
