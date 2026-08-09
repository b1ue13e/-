---
created: 2026-08-07
type: study
course: "强化学习"
title: "分层RL概述与 Temporal Abstraction (Hierarchical RL Overview)"
topic: "分层RL概述与 Temporal Abstraction (Hierarchical RL Overview)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习, 分层, 时序抽象]
upstream: ["[[分层RL与Options]]", "[[MDP 与贝尔曼方程]]"]
concept: ["分层RL", "时序抽象", "子目标", "选项"]
sources:
  - "Sutton et al. 1999 (Options); Bacon et al. 2017 (Option-Critic); Barto 2003 (HRL)"
---
# 分层RL概述与 Temporal Abstraction (Hierarchical RL Overview)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
很多任务天然有层级："去超市"= 出门→走路→推门→拿东西… 在原始动作（左移1cm）上直接学，既要管长期目标又管微操，又慢又脆。分层 RL（HRL）引入**时序抽象**：高层选"子目标/选项"（如"走到门口"），低层在一段时间内执行它。这把长程信用分配和探索变得可行。

## 正式定义 / 公式
- **半马尔可夫选项（Option）** ω = (I_ω  initiation set, π_ω policy, β_ω termination)：在状态满足 I_ω 时可启动，按 π_ω 执行直到以 β_ω(s) 概率终止。
- 选项把 MDP 提升为**半 MDP（SMDP）**：高层在"选项层面"做决策，时间步长为选项持续长度。
- 一般框架：Manager 输出子目标 g_t，Worker 输出原始动作 a_t 去达 g_t；奖励可在层级间传递（内部/外部奖励）。

## 最小手算例子
四足机器人过障碍：低层学"抬腿/落脚"等基础动作（选项），高层学"先跨左前腿再迈右后腿"的子目标序列。高层无需关心每个关节扭矩，只在"选项"粒度规划，样本效率和可解释性都更好。

## 对比与常见错误
- 与扁平 RL：HRL 把信用分配拆成"选项级 + 动作级"，缓解长程稀疏奖励。
- 与技能发现（DIAYN）：DIAYN 无监督发现技能；HRL 常用目标任务驱动选项/子目标学习。
- **常见错误**：子目标空间设计不当→低层学不会达目标；高层频繁改子目标→低层来不及执行；层级奖励权重失衡。

## 闭卷自测
1. 时序抽象解决扁平 RL 的什么痛点？选项（option）由哪三部分定义？
2. HRL 与纯技能发现（DIAYN）的目标导向有何不同？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
