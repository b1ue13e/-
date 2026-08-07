---
type: study
topic: "A3C-去相关"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A3C-去相关", "A3C 样本去相关"]
upstream: ["[[A3C-异步]]", "[[A3C-无ER]]"]
tags: [学习, 强化学习]
---

# A3C-去相关

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
多个并行 worker 在不同状态起步、各跑一段，样本天然去相关——这是 A3C 不依赖经验回放的原因。

## 正式定义 / 公式
并行 n 个独立环境，样本来自不同轨迹的不同段，相关性远低于单环境连续样本。
故无需 DQN 式经验回放来打破相关。

## 最小手算例子
4 worker 在 4 个不同状态各跑 20 步，合并的 80 样本彼此分散，近似独立。

## 对比与常见错误
- 与 DQN 经验回放：A3C 用"并行去相关"替代"缓冲回放"。
- 常见错误：在 A3C 里硬加经验回放——多此一举，并行已去相关。

## 闭卷自测
1. A3C 如何使样本去相关？
2. 为何因此它不用经验回放？
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
