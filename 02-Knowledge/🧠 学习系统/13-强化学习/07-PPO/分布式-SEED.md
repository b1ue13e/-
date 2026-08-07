---
type: study
topic: "分布式-SEED"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["分布式-SEED", "SEED RL"]
upstream: ["[[A2C家族]]"]
tags: [学习, 强化学习]
---

# 分布式-SEED

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
推理（环境交互）常常比训练更慢，如何把推理和训练解耦提速？

## 正式定义 / 公式
SEED：把环境仿真放到带加速硬件的"推理引擎"上，actor 仅负责前向与收集，learner 集中做反向；通过高效的 RPC 把观测/动作在引擎与 learner 间传输，大幅降低单步延迟。

## 最小手算例子
<!-- NUMEX2 -->SEED：actor 与 learner 共置同进程（每 TPU 核一 actor+learner），零网络传输。例数千核并行，延迟从毫秒级降到微秒级。

learner GPU 算动作 → 引擎 GPU 跑环境 → 回传下一观测，流水线化。

## 对比与常见错误
- 与 A2C：SEED 强调 actor-learner 物理分离与低延迟通信。
- 常见错误：把 SEED 当普通多进程——核心是引擎化推理。

## 闭卷自测
1. SEED 如何解耦推理与训练？
2. 它解决的主要瓶颈是什么？
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
