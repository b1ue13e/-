---
created: 2026-08-07
type: study
course: "强化学习"
title: "Dyna-Q+与探索奖励 (Dyna-Q+ & Exploration Bonus)"
topic: "Dyna-Q+与探索奖励 (Dyna-Q+ & Exploration Bonus)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, 模型基, 探索]
upstream: ["[[Dyna-Q与背景规划]]", "[[模型基RL概述]]"]
concept: ["Dyna-Q+", "探索奖励", "模型不确定性", "乐观"]
sources:
  - "Sutton & Barto Ch.8.3"
---
# Dyna-Q+与探索奖励 (Dyna-Q+ & Exploration Bonus)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Sutton & Barto Ch.8.3`
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
Dyna-Q 假设模型学到的就是真模型。一旦真实环境发生**变化**（例如某扇门从锁着变开着），旧模型会持续给出错误预测，而智能体早已"自信地"不再探索被低估的状态。Dyna-Q+ 在规划时给"很久没访问过的状态-动作"额外加探索奖励，主动回头复查。

## 正式定义 / 公式
记录每个 (s,a) 上次被真实访问距现在的步数 τ(s,a)。在**规划（仿真）更新**使用的奖励上叠加一个随闲置时间增长的奖励项：

  r̄_bonus = r + κ·√τ

其中 κ 是小常数。这样长期未被验证的 (s,a) 在想象中显得"更香"，规划器会优先去仿真它们，从而触发真实回访、刷新模型。真实更新仍用环境给的真实 r，奖励项只用于规划侧的优先级/价值估计。

## 最小手算例子
环境在第 1000 步把终点的门打开（奖励从 −1 变 +10）。Dyna-Q 因模型里该转移仍为旧值，几乎不回头；Dyna-Q+ 中那些 τ 很大的 (s,a) 拿到 κ√τ 的想象奖励，规划器把"通往门"的状态推高，智能体很快真实走过去发现变化，模型随之修正。

## 对比与常见错误
- 与普通 ε-贪婪：Dyna-Q+ 的探索是**定向、基于模型不确定性**的，不是均匀随机。
- 与 RND/好奇心（阶段9）：Dyna-Q+ 用"状态访问年龄"当代理，不训练额外网络，更轻量。
- **常见错误**：κ 过大导致智能体在想象中无限"留恋"旧状态、真实交互被荒废；κ 应与真实奖励尺度匹配。

## 闭卷自测
1. Dyna-Q+ 的探索奖励加在真实更新还是规划更新上？为什么？
2. 它如何发现"环境已变化"这一事实？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
