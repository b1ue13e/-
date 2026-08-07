---
type: study
topic: "Rainbow"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Rainbow", "Rainbow DQN"]
upstream: ["[[Double-DQN]]", "[[Dueling-DQN]]", "[[PER]]", "[[NoisyNets]]", "[[C51]]"]
tags: [学习, 强化学习]
---

# Rainbow

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
DQN 的多种改进各解决一面问题。Rainbow 把它们整合进一个算法，取得远超单点的性能。

## 正式定义 / 公式
Rainbow = Double DQN + Dueling + PER + Noisy Nets + C51 +（原版还含多步学习 n-step 与分布式）。
各组件互补：DDQN 抑过估计、Dueling 提质效、PER 提数据效率、Noisy 提探索、C51 用分布信息。

## 最小手算例子
<!-- NUMEX2 -->Rainbow 融合 7 项：DDQN + 优先回放 + Dueling + 多步 + Distributional + NoisyNet + C51。例在 57 款 Atari 上中位数超人类 100%+。

Atari 基准上，Rainbow 相比单点 DQN 改进，人类归一化得分大幅领先；消融实验显示各组件均贡献。

## 对比与常见错误
- 与单点改进：Rainbow 不是简单堆叠，而是统一框架；但并非所有组合都正相互作用，需调参。
- 常见错误：以为"堆越多越好"——组件间可能有耦合/开销，需依任务取舍。

## 闭卷自测
1. Rainbow 整合了哪些 DQN 改进？
2. 为什么说它是"集成"而非简单堆叠？
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
